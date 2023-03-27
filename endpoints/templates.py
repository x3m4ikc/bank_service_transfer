from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.models import TemplateForPayment
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1", tags=["template"])


@router.get("/get-details")
def get_template(template_id: int = Query(..., ge=0), session: Session = Depends(get_db)):
    template = session.query(TemplateForPayment).filter(TemplateForPayment.id == template_id).first()
    if template is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Template with id {template_id} not found"
        )
    return {"status": "success", "template": template}
