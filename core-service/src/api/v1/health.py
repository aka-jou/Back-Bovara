# src/api/v1/health.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from uuid import UUID
from datetime import date

from src.infrastructure.database import get_db
from src.infrastructure.auth.dependencies import get_current_user, UserAuth
from src.application.health_event_service import HealthEventService
from src.schemas.health_event import (
    HealthEventCreate,
    HealthEventUpdate,
    HealthEventResponse,
)

router = APIRouter(
    prefix="/health-events",
    tags=["Health Events"],
)


@router.post(
    "",
    response_model=HealthEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_health_event(
    event_data: HealthEventCreate,
    current_user: UserAuth = Depends(get_current_user),
    db = Depends(get_db),
):
    """Registrar nuevo evento de salud"""
    service = HealthEventService(db)
    
    try:
        event = service.create_health_event(
            cattle_id=event_data.cattle_id,
            owner_id=current_user.id,
            **event_data.model_dump(exclude={"cattle_id"})
        )
        return event
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/cattle/{cattle_id}",
    response_model=List[HealthEventResponse],
)
async def get_cattle_health_events(
    cattle_id: UUID,
    current_user: UserAuth = Depends(get_current_user),
    db = Depends(get_db),
):
    """Obtener historial de salud de un animal"""
    service = HealthEventService(db)
    events = service.get_events_by_cattle(cattle_id, current_user.id)
    return events


@router.get(
    "/{event_id}",
    response_model=HealthEventResponse,
)
async def get_health_event(
    event_id: UUID,
    current_user: UserAuth = Depends(get_current_user),
    db = Depends(get_db),
):
    """Obtener evento específico"""
    service = HealthEventService(db)
    event = service.get_event_by_id(event_id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    
    return event


@router.put(
    "/{event_id}",
    response_model=HealthEventResponse,
)
async def update_health_event(
    event_id: UUID,
    event_data: HealthEventUpdate,
    current_user: UserAuth = Depends(get_current_user),
    db = Depends(get_db),
):
    """Actualizar evento de salud"""
    service = HealthEventService(db)
    
    update_dict = event_data.model_dump(exclude_unset=True)
    event = service.update_event(event_id, **update_dict)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_health_event(
    event_id: UUID,
    current_user: UserAuth = Depends(get_current_user),
    db = Depends(get_db),
):
    """Eliminar evento de salud"""
    service = HealthEventService(db)
    deleted = service.delete_event(event_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
