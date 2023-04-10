from models.models import TemplateForPayment, TransferOrder
from sqlalchemy import Select, select


def retrieve_template_query(template_id) -> Select:
    query = select(TemplateForPayment).where(TemplateForPayment.id == template_id)
    return query


def get_transfer_order_query(transfer_order_id: int) -> Select:
    query = select(TransferOrder).where(TransferOrder.id == transfer_order_id)
    return query
