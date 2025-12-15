from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.infrastructure.database import get_db
from src.schemas.health_event import HealthEventCreate, HealthEventResponse
from src.application.health_event_service import HealthEventService

router = APIRouter()


@router.post("", response_model=HealthEventResponse, status_code=status.HTTP_201_CREATED)  # ✅ AGREGAR ESTE DECORADOR
def create_health_event(
    health_event: HealthEventCreate,
    db: Session = Depends(get_db)
):
    service = HealthEventService(db)
    result = service.create_health_event(
        cattle_id=health_event.cattle_id,
        event_type=health_event.event_type.value,
        disease_name=health_event.disease_name,
        medicine_name=health_event.medicine_name,
        application_date=health_event.application_date,
        administration_route=health_event.administration_route.value if health_event.administration_route else None,
        dosage=health_event.dosage,
        veterinarian_name=health_event.veterinarian_name,
        notes=health_event.notes
    )
    return result


@router.get("/cattle/{cattle_id}", response_model=List[HealthEventResponse])
def get_health_events_by_cattle(
    cattle_id: UUID,
    db: Session = Depends(get_db)
):
    service = HealthEventService(db)
    events = service.get_events_by_cattle(cattle_id)
    return events
