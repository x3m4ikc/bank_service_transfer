import uvicorn
from endpoints.endpoints import router
from fastapi import FastAPI

app = FastAPI()


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8002, host="0.0.0.0", reload=True)
