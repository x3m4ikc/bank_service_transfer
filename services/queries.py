from models.models import TemplateForPayment, TransferOrder, TransferType
from sqlalchemy import Select, select


def retrieve_template_query(template_id) -> Select:
    query = select(TemplateForPayment).where(TemplateForPayment.id == template_id)
    return query


def get_transfer_order_query(transfer_order_id: int) -> Select:
    query = select(TransferOrder).where(TransferOrder.id == transfer_order_id)
    return query


def auto_payments_query(client_id: str) -> Select:
    query = (
        select(TransferOrder.id, TransferType.type_name)
        .join(TransferType, TransferOrder.id == TransferType.id)
        .where(TransferOrder.client_id == client_id, TransferType.type_name == "AUTOPAYMENTS")
    )
    return query
