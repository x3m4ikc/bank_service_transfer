from typing import List

import uvicorn
from db.database import engine, session_local
from fastapi import Depends, FastAPI
from models import models
from schemas.schemas import TemplateForPayment
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/api/v1/get-details/",
    response_model=TemplateForPayment | None,
)
def get_template(
    db: Session = Depends(get_db),
    # template_id: int = Query(...,)
) -> List[TemplateForPayment]:
    template = db.query(models.TemplateForPayment).all()
    # template = db.query(models.TemplateForPayment).get(id=template_id)
    print(template)
    return list(map(TemplateForPayment.from_orm(), template))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
