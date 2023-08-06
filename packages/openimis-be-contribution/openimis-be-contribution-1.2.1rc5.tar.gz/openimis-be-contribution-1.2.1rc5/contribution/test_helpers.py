import uuid

from contribution.models import Payer, Premium
from payer.test_helpers import create_test_payer


def create_test_premium(policy_id, with_payer=True, custom_props=None):
    payer = create_test_payer() if with_payer else None

    premium = Premium.objects.create(
        **{
            "policy_id": policy_id,
            "payer_id": payer.id if payer else None,
            "amount": 1000,
            "receipt": "Test receipt",
            "pay_date": "2019-01-01",
            "pay_type": Payer.PAYER_TYPE_OTHER,
            "validity_from": "2019-01-01",
            "audit_user_id": -1,
            **(custom_props if custom_props else {})
        }
    )

    return premium
