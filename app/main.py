from fastapi import FastAPI

from app.core.config import settings
from app.gateway.runtime_function import lifespan
from app.api.v1.devices import router as device_router
from app.api.v1.conifg import router as config_router
from app.api.v1.health import router as health_router
from app.api.v1.runtime import router as runtime_router
from app.api.v1.plugins import router as plugin_router
from app.api.v1.tags import router as tag_router
from app.api.v1.variables import router as variable_router

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(
    config_router,
    prefix="/configs",
    tags=["Configs"],
)

app.include_router(
    device_router,
    prefix="/devices",
    tags=["Devices"],
)

app.include_router(
    runtime_router,
    prefix="/runtime",
    tags=["Runtime"],
)

app.include_router(
    plugin_router,
    prefix="/plugins",
    tags=["Plugins"],
)

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    variable_router,
    prefix="/variables",
    tags=["Variables"],
)

app.include_router(
    tag_router,
    prefix="/tags",
    tags=["Tags"],
)

@app.get("/")
async def root():
    return {
        "message": "Python IoT Gateway"
    }