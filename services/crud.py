from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.models import TransferOrder
from schemas.schemas import TemplateForExchangeRatesSchema, TemplateForPaymentSchema
from sqlalchemy.ext.asyncio import AsyncSession

from .currency import get_exchange_info
from .queries import get_transfer_order_query, retrieve_template_query


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
        if exchange_rate == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        result = TemplateForExchangeRatesSchema(
            currency_from=currency_from, currency_to=currency_to, exchange_rate=exchange_rate, units=units
        )

        return result
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problems")


async def get_transfer_order(session: AsyncSession, transfer_order_id: int):
    query = get_transfer_order_query(transfer_order_id)
    data = await session.execute(query)

    if query is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return data.scalars().first()


async def switch_field(session: AsyncSession, obj: TransferOrder, field: str) -> TransferOrder:
    obj_data = jsonable_encoder(obj)
    setattr(obj, field, not obj_data[field])
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
