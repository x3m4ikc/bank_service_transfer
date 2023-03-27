from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.models import TemplateForPayment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1", tags=["template"])


@router.get("/get-details")
async def get_template(template_id: int = Query(..., ge=0), session: AsyncSession = Depends(get_db)):
    query = select(TemplateForPayment).where(TemplateForPayment.id == template_id)
    template = await session.execute(query)
    print(template)
    template_for_payment = template.first()[0]
    print(template_for_payment)
    if template is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Template with id {template_id} not found"
        )

    return template_for_payment
