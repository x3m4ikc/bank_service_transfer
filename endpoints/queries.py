from models.models import TemplateForPayment
from sqlalchemy import Select, select


def retrieve_template_query(template_id) -> Select:
    query = select(
        TemplateForPayment.id,
        TemplateForPayment.name,
        TemplateForPayment.payee_name,
        TemplateForPayment.payee_account_number,
        TemplateForPayment.template_purpose_of_payment,
        TemplateForPayment.BIC,
        TemplateForPayment.INN,
    ).where(TemplateForPayment.id == template_id)

    return query
