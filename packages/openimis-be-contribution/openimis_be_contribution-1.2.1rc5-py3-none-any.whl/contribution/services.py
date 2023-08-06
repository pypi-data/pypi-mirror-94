import logging
from enum import Enum

from core.datetimes.shared import datetimedelta
from django.db import connection
from django.db.models import Sum
from django.db.transaction import atomic
from insuree.models import Insuree, Family, InsureePolicy
from location.apps import LocationConfig
from location.models import Location
from payment.models import Payment
from policy.models import Policy
from policy.services import policy_status_premium_paid
from product.models import Product

from .models import Premium, PayTypeChoices

logger = logging.getLogger(__name__)

# A fake family is used for funding
FUNDING_CHF_ID = "999999999"


class ByPolicyPremiumsAmountService(object):

    def __init__(self, user):
        self.user = user

    def request(self, policy_id):
        return Premium.objects.filter(
            policy_id=policy_id
        ).exclude(
            is_photo_fee=True
        ).aggregate(Sum('amount'))['amount__sum']


def last_date_for_payment(policy_id):
    policy = Policy.objects.get(id=policy_id)
    has_cycle = policy.product.has_cycle()

    if policy.stage == 'N':
        grace_period = policy.product.grace_period
    elif policy.stage == 'R':
        grace_period = policy.product.grace_period_renewal
    else:
        logger.error("policy stage should be either N or R, policy %s has %s", policy_id, policy.stage)
        raise Exception("policy stage should be either N or R")

    waiting_period = policy.product.waiting_period

    if has_cycle:
        # Calculate on fixed cycle
        start_date = policy.start_date

        last_date = start_date + datetimedelta(months=grace_period)
    else:
        # Calculate on Free Cycle
        if policy.stage == 'N':
            last_date = policy.enroll_date + datetimedelta(months=waiting_period)
        else:
            last_date = policy.expiry_date + datetimedelta(days=1) + datetimedelta(months=waiting_period)

    return last_date - datetimedelta(days=1)


@atomic
def add_fund(product_id, payer_id, pay_date, amount, receipt, audit_user_id, is_offline):
    product = Product.objects.filter(validity_to__isnull=True).get(id=product_id)
    # TODO check and/or document premium_adult
    product_value = product.lump_sum or product.premium_adult

    # Check if the family with CHFID
    # Original procedure here has a strange and useless join on isnull(,0), ignoring
    family = Insuree.objects.filter(validity_to__isnull=True).filter(chf_id=FUNDING_CHF_ID)\
        .filter(family__location_id=product.location_id).first()

    fundings = []
    funding_parent = None  # Top Funding has no parent, then the loop will chain them
    for level in LocationConfig.location_types:
        level_funding, funding_created = Location.objects.get_or_create(
            code=f"F{level}",
            name="Funding",
            parent=funding_parent,
            type=level,
            defaults=dict(audit_user_id=audit_user_id),
        )
        funding_parent = level_funding
        fundings.append(level_funding)
        if funding_created:
            logger.warning("Created funding at level %s", level)

    if not family:
        family = Family.objects.create(
            location_id=product.location_id,
            poverty=False,
            is_offline=is_offline,
            audit_user_id=audit_user_id,
        )
        insuree = Insuree.objects.create(
            family=family,
            chf_id=FUNDING_CHF_ID,
            last_name="Funding",
            other_names="Funding",
            pay_date=pay_date,
            gender=None,
            marital=None,
            head=True,
            card_issued=False,
            audit_user_id=audit_user_id,
            is_offline=is_offline,
        )
        family.head_insuree = insuree
        family.save()

    from core import datetimedelta
    policy = Policy.objects.create(
        family=family,
        enroll_date=pay_date,
        start_date=pay_date,
        effective_date=pay_date,
        expiry_date=pay_date + datetimedelta(months=product.insurance_period),
        status=Policy.STATUS_ACTIVE,
        value=product_value,
        product=product,
        officer_id=None,
        audit_user_id=audit_user_id,
        is_offline=is_offline,
    )

    InsureePolicy.objects.create(
        insuree=insuree,  # TODO Might not be assigned
        policy=policy,
        enrollment_date=policy.enroll_date,
        start_date=policy.start_date,
        effective_date=policy.effective_date,
        expiry_date=policy.expiry_date,
        audit_user_id=audit_user_id,
        is_offline=is_offline,
    )

    Premium.objects.create(
        policy=policy,
        payer_id=payer_id,
        amount=amount,
        receipt=receipt,
        pay_date=pay_date,
        type=PayTypeChoices.FUNDING
    )


class PremiumUpdateActionEnum(Enum):
    SUSPEND = "SUSPEND"
    ENFORCE = "ENFORCE"
    WAIT = "WAIT"


def premium_updated(premium, action):
    """
    if the contribution is lower than the policy value, action can override it or suspend the policy
    if it is right or too much, just activate it (enforce is still expected but just a warning)
    """
    policy = premium.policy
    policy.save_history()

    if action == PremiumUpdateActionEnum.SUSPEND.value:
        policy.status = Policy.STATUS_SUSPENDED
        policy.save()
        return

    if premium.amount == policy.value:
        policy_status_premium_paid(policy,
                                   premium.pay_date if premium.pay_date > policy.start_date else policy.start_date)
    elif premium.amount < policy.value:
        # suspend already handled
        if action == PremiumUpdateActionEnum.ENFORCE.value:
            policy_status_premium_paid(policy, premium.pay_date)
        # otherwise, just leave the policy unchanged
    elif premium.amount > policy.value:
        if action != PremiumUpdateActionEnum.ENFORCE.value:
            logger.warning("action on premiums larger than the policy value")
        policy_status_premium_paid(policy, premium.pay_date)
    else:
        logger.warning("The comparison between premium amount %s and policy value %s failed",
                       premium.amount, policy.value)
        raise Exception("Invalid combination or premium and policy amounts")

    if policy.status is not None and (
            policy.effective_date == premium.pay_date
            or policy.effective_date == policy.start_date):
        # Enforcing policy
        if policy.offline or not premium.is_offline:
            policy.save()
        if policy.status == Policy.STATUS_ACTIVE:
            _update_policy_insurees(policy)
    elif policy.effective_date:
        _activate_insurees(policy, premium.pay_date)


def _update_policy_insurees(policy):
    policy.insuree_policies.filter(validity_to__isnull=True).update(
        effective_date=policy.effective_date,
        start_date=policy.start_date,
        expiry_date=policy.expiry_date,
    )


def _activate_insurees(policy, pay_date):
    policy.insuree_policies.filter(validity_to__isnull=True).update(
        effective_date=pay_date,
    )

