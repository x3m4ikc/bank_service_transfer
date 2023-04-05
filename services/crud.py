from fastapi import HTTPException, status
from schemas.schemas import TemplateForPaymentSchema

from .queries import retrieve_template_query


async def get_template_for_payment(session, template_id):
    query = retrieve_template_query(template_id)
    data = await session.execute(query)
    template = data.first()

    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template for payment with id:{template_id} not found",
        )
    template_model = TemplateForPaymentSchema.from_orm(template[0])

    return template_model
