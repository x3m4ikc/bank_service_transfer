from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas.schemas import TemplateForPaymentSchema
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_template_for_payment

router = APIRouter(prefix="/api/v1", tags=["template"])


@router.get("/get-details", status_code=200, response_model=TemplateForPaymentSchema)
async def get_template(template_id: int = Query(), session: AsyncSession = Depends(get_db)):
    template = await get_template_for_payment(session, template_id)

    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template for payment with id:{template_id} not found",
        )

    return template._asdict()
