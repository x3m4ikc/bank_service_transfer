from typing import Any, Callable

from db.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Query, status
from models.models import TransfersTypes
from schemas.schemas import (
    TemplateForExchangeRatesSchema,
    TemplateForPaymentSchema,
    TransferOrderSchema,
)
from services.crud import (
    get_exchange_rates,
    get_template_for_payment,
    get_transfer_order,
    switch_field,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1")


@router.get(
    "/template-details", name="template_details", status_code=200, response_model=TemplateForPaymentSchema
)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    """Get template for payment by ID"""
    template_object = await get_template_for_payment(session, template_id)
    return template_object


@router.get(
    "/rates",
    name="exchange_currency",
    status_code=status.HTTP_200_OK,
    response_model=TemplateForExchangeRatesSchema,
)
async def get_rates(
    currency_from: str = Query(..., max_length=3, min_length=3),
    currency_to: str = Query(..., max_length=3, min_length=3),
    units: float = 100,
):
    """Get exchange rates"""
    results = await get_exchange_rates(currency_from, currency_to, units)
    return results


@router.patch(
    "/payments/favorites", name="add_transfer_order_to_favorites", response_model=TransferOrderSchema
)
async def add_transfer_order_to_favorites(
    transfer_order_id: int = Body(embed=True), session: AsyncSession = Depends(get_db)
):
    transfer_order_obj = await get_transfer_order(session, transfer_order_id)
    transfer_order = await switch_field(session, transfer_order_obj, "is_favorite")
    return transfer_order


@router.get(
    "/payments/paymentType",
    name="payment_types",
    status_code=status.HTTP_200_OK,
    response_model=list[TransfersTypes],
)
async def get_payment_type() -> list[Callable[[], Any]]:
    """Get payment types"""
    return [i.value for i in TransfersTypes]


@router.get(
    "/payments/favorites/{transfer_order_id:int}",
    name="payment_by_id",
    status_code=status.HTTP_200_OK,
    response_model=TransferOrderSchema,
)
async def retrieve_transfer_order_by_id(
    transfer_order_id: int = Path(), session: AsyncSession = Depends(get_db)
):
    transfer_order = await get_transfer_order(session, transfer_order_id)
    return transfer_order
