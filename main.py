import uvicorn
from db.database import engine
from endpoints.templates import router
from fastapi import FastAPI
from models.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
