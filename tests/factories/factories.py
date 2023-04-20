import datetime
import uuid

from factory import SubFactory
from models import models
from tests.factories.utils import AsyncFactory


class TemplateForPaymentFactory(AsyncFactory):
    class Meta:
        model = models.TemplateForPayment

    id = 0
    name = "test1"
    payee_name = "test1"
    payee_account_number = "test1"
    template_purpose_of_payment = "test1"
    BIC = "test1"
    INN = "test1"


class TransferTypeFactory(AsyncFactory):
    class Meta:
        model = models.TransferType

    id = 0
    type_name = "AUTOPAYMENTS"
    currency_code = "test"
    min_commission = 1
    max_commission = 1
    percent_commission = 1
    commission_fix = 1
    min_sum = 1


class PayeeFactory(AsyncFactory):
    class Meta:
        model = models.Payee

    id = 0
    type = "INDIVIDUALS"
    name = "test"
    INN = "test"
    BIC = "test"
    payee_account_number = "test"
    payee_card_number = "test"


class TransferOrderFactory(AsyncFactory):
    class Meta:
        model = models.TransferOrder

    id = 0
    created_at = datetime.datetime.utcnow()
    transfer_type_id = SubFactory(TransferTypeFactory).get_factory().id
    purpose = "test"
    remitter_card_number = "test"
    payee_id = SubFactory(PayeeFactory).get_factory().id
    sum = 100
    sum_commission = 1
    completed_at = datetime.datetime.utcnow()
    status = "DRAFT"
    authorization_code = "test"
    currency_exchange = 1000
    is_favorite = False
    start_date = datetime.datetime.utcnow()
    periodicity = "WEEKLY"
    client_id = uuid.uuid4()
