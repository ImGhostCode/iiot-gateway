from fastapi import FastAPI

from app.core.config import settings
from app.gateway.runtime_function import lifespan
from app.api.v1.devices import router as device_router_v1
from app.api.v1.system_conifg import router as system_config_router_v1
from app.api.v1.health import router as health_router_v1
from app.api.v1.runtime import router as runtime_router_v1
from app.api.v1.plugins import router as plugin_router_v1
from app.api.v1.tags import router as tag_router_v1
from app.api.v1.variables import router as variable_router_v1
from app.api.v1.users import router as user_router_v1
from app.api.v1.auth import router as auth_router_v1

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


app.include_router(
    system_config_router_v1,
    prefix="/api/v1/system-config",
    tags=["System configs"],
)

app.include_router(
    device_router_v1,
    prefix="/api/v1/devices",
    tags=["Devices"],
)

app.include_router(
    runtime_router_v1,
    prefix="/api/v1/runtime",
    tags=["Runtime"],
)

app.include_router(
    plugin_router_v1,
    prefix="/api/v1/plugins",
    tags=["Plugins"],
)

app.include_router(
    health_router_v1,
    prefix="/api/v1/health",
    tags=["Health"],
)

app.include_router(
    variable_router_v1,
    prefix="/api/v1/variables",
    tags=["Variables"],
)

app.include_router(
    tag_router_v1,
    prefix="/api/v1/tags",
    tags=["Tags"],
)

app.include_router(
    user_router_v1,
    prefix="/api/v1/users",
    tags=["Users"],
)

app.include_router(
    auth_router_v1,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@app.get("/")
async def root():
    return {
        "message": "Python IoT Gateway"
    }