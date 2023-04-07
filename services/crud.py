from fastapi import HTTPException, status
from pydantic import ValidationError
from schemas.schemas import TemplateForExchangeRatesSchema, TemplateForPaymentSchema

from .currency import get_exchange_info
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


async def get_exchange_rates(currency_from, currency_to, units):
    try:
        currency_from = currency_from.upper()
        currency_to = currency_to.upper()
        exchange_rate = get_exchange_info(currency_from, currency_to, units)

        result = TemplateForExchangeRatesSchema(
            currency_from=currency_from, currency_to=currency_to, exchange_rate=exchange_rate, units=units
        )

        return result
    except ValidationError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problems")
    except BaseException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problems")
