from fastapi import APIRouter

from src.api.v1.cattle import router as cattle_router
from src.api.v1.health import router as health_event_router  # ✅ Importar
from src.api.v1.heat_event import router as heat_event_router
from src.api.v1.reminder import router as reminder_router

api_router = APIRouter()

api_router.include_router(cattle_router, prefix="/cattle", tags=["cattle"])
api_router.include_router(health_event_router, prefix="/health-events", tags=["health-events"])  # ✅ Registrar
api_router.include_router(heat_event_router, prefix="/heat-events", tags=["heat-events"])
api_router.include_router(reminder_router, prefix="/reminders", tags=["reminders"])
