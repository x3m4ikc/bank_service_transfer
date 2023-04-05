from models.models import TemplateForPayment
from sqlalchemy import Select, select


def retrieve_template_query(template_id) -> Select:
    query = select(TemplateForPayment).where(TemplateForPayment.id == template_id)
    return query
