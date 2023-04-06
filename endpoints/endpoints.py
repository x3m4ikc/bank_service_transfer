from db.database import get_db
from fastapi import APIRouter, Depends, Query
from schemas.schemas import TemplateForPaymentSchema
from services.crud import get_exchange_rates, get_template_for_payment
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1")


@router.get("/template-details", status_code=200, response_model=TemplateForPaymentSchema)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    """Get template for payment by ID"""
    template_object = await get_template_for_payment(session, template_id)
    return template_object


@router.get("/rates", status_code=200)
async def get_rates(currencyCodeFrom: str, currencyCodeTo: str):
    """Get exchange rates"""
    results = await get_exchange_rates(currencyCodeFrom, currencyCodeTo)
    return results
