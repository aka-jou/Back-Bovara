from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.schemas.heat_event import HeatEventCreate, HeatEventUpdate, HeatEventResponse
from src.application.heat_event_service import HeatEventService
from src.infrastructure.repositories.heat_event_repository import HeatEventRepository
from src.infrastructure.database import get_db

router = APIRouter(prefix="/heat-events", tags=["Heat Events"])


def get_heat_event_service(db: Session = Depends(get_db)) -> HeatEventService:
    repository = HeatEventRepository(db)
    return HeatEventService(repository)


@router.post("/", response_model=HeatEventResponse, status_code=201)
def create_heat_event(
    heat_event: HeatEventCreate,
    service: HeatEventService = Depends(get_heat_event_service)
):
    """Registrar un nuevo evento de celo"""
    return service.create_heat_event(heat_event)


@router.get("/{heat_event_id}", response_model=HeatEventResponse)
def get_heat_event(
    heat_event_id: UUID,
    service: HeatEventService = Depends(get_heat_event_service)
):
    """Obtener un evento de celo por ID"""
    heat_event = service.get_heat_event(heat_event_id)
    if not heat_event:
        raise HTTPException(status_code=404, detail="Evento de celo no encontrado")
    return heat_event


@router.get("/cattle/{cattle_id}", response_model=List[HeatEventResponse])
def get_heat_events_by_cattle(
    cattle_id: UUID,
    service: HeatEventService = Depends(get_heat_event_service)
):
    """Obtener todos los eventos de celo de una vaca"""
    return service.get_heat_events_by_cattle(cattle_id)


@router.put("/{heat_event_id}", response_model=HeatEventResponse)
def update_heat_event(
    heat_event_id: UUID,
    update_data: HeatEventUpdate,
    service: HeatEventService = Depends(get_heat_event_service)
):
    """Actualizar un evento de celo"""
    heat_event = service.update_heat_event(heat_event_id, update_data)
    if not heat_event:
        raise HTTPException(status_code=404, detail="Evento de celo no encontrado")
    return heat_event


@router.delete("/{heat_event_id}", status_code=204)
def delete_heat_event(
    heat_event_id: UUID,
    service: HeatEventService = Depends(get_heat_event_service)
):
    """Eliminar un evento de celo"""
    if not service.delete_heat_event(heat_event_id):
        raise HTTPException(status_code=404, detail="Evento de celo no encontrado")
