from fastapi import APIRouter


# Importar routers
from src.api.v1.cattle import router as cattle_router
from src.api.v1.health import router as health_event_router
from src.api.v1.reminder import router as reminder_router
from src.api.v1.heat_event import router as heat_event_router  


# Router principal
api_router = APIRouter()


# Incluir routers
api_router.include_router(cattle_router)
api_router.include_router(health_event_router)
api_router.include_router(reminder_router)
api_router.include_router(heat_event_router) 
