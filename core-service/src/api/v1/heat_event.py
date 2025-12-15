from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.infrastructure.database import get_db
from src.schemas.heat_event import HeatEventCreate, HeatEventUpdate, HeatEventResponse
from src.application.heat_event_service import HeatEventService
from src.infrastructure.repositories.heat_event_repository import HeatEventRepository  # ✅ Agregar

router = APIRouter()


@router.post("/", response_model=HeatEventResponse, status_code=status.HTTP_201_CREATED)
def create_heat_event(
    heat_event: HeatEventCreate,
    db: Session = Depends(get_db)
):
    # ✅ Crear repositorio primero, luego servicio
    repository = HeatEventRepository(db)
    service = HeatEventService(repository)
    result = service.create_heat_event(heat_event)
    return result


@router.get("/cattle/{cattle_id}", response_model=List[HeatEventResponse])
def get_heat_events_by_cattle(
    cattle_id: UUID,
    db: Session = Depends(get_db)
):
    repository = HeatEventRepository(db)
    service = HeatEventService(repository)
    events = service.get_heat_events_by_cattle(cattle_id)
    return events


@router.get("/{event_id}", response_model=HeatEventResponse)
def get_heat_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    repository = HeatEventRepository(db)
    service = HeatEventService(repository)
    event = service.get_heat_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Heat event not found")
    return event


@router.put("/{event_id}", response_model=HeatEventResponse)
def update_heat_event(
    event_id: UUID,
    heat_event_update: HeatEventUpdate,
    db: Session = Depends(get_db)
):
    repository = HeatEventRepository(db)
    service = HeatEventService(repository)
    event = service.update_heat_event(event_id, heat_event_update)
    if not event:
        raise HTTPException(status_code=404, detail="Heat event not found")
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_heat_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    repository = HeatEventRepository(db)
    service = HeatEventService(repository)
    success = service.delete_heat_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Heat event not found")
    return None
