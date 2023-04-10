from db.database import get_db
from fastapi import APIRouter, Body, Depends, Query
from schemas.schemas import TemplateForPaymentSchema
from services.crud import get_template_for_payment, get_transfer_order
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1")


@router.get(
    "/template-details", name="template_details", status_code=200, response_model=TemplateForPaymentSchema
)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    """Get template for payment by ID"""
    template_object = await get_template_for_payment(session, template_id)
    return template_object


@router.patch("/payments/favorites", name="add_transfer_order_to_favorites", status_code=200)
async def add_transfer_order_to_favorites(
    transfer_order_id: int = Body(embed=True), session: AsyncSession = Depends(get_db)
):
    transfer_order = await get_transfer_order(session, transfer_order_id)

    return transfer_order
