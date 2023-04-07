from db.database import get_db
from fastapi import APIRouter, Depends, Query, status
from schemas.schemas import TemplateForExchangeRatesSchema, TemplateForPaymentSchema
from services.crud import get_exchange_rates, get_template_for_payment
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1")


@router.get(
    "/template-details", name="template_details", status_code=200, response_model=TemplateForPaymentSchema
)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    """Get template for payment by ID"""
    template_object = await get_template_for_payment(session, template_id)
    return template_object


@router.get("/rates", status_code=status.HTTP_200_OK, response_model=TemplateForExchangeRatesSchema)
async def get_rates(
    currency_from: str = Query(..., max_length=3, min_length=3),
    currency_to: str = Query(..., max_length=3, min_length=3),
    units: float = 100,
):
    """Get exchange rates"""
    results = await get_exchange_rates(currency_from, currency_to, units)
    return results
