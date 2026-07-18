from fastapi import FastAPI

from app.core.config import settings
from app.gateway.runtime_function import lifespan

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "message": "Python IoT Gateway"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }