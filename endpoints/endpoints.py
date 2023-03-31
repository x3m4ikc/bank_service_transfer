from db.database import get_db
from fastapi import APIRouter, Depends, Query
from schemas.schemas import TemplateForPaymentSchema
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_template_for_payment

router = APIRouter(prefix="/api/v1", tags=["template"])


@router.get("/get-details", status_code=200, response_model=TemplateForPaymentSchema)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    """Get template for payment by ID"""
    template_object = await get_template_for_payment(session, template_id)
    return template_object
