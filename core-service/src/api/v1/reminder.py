# src/api/v1/reminder.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import date

from src.infrastructure.database import get_db
from src.application.reminder_service import ReminderService
from src.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
)
# from src.infrastructure.auth.dependencies import get_current_user  # ❌ COMENTADO


router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)

# ✅ User ID temporal
TEMP_USER_ID = UUID("12345678-1234-5678-1234-567812345678")


@router.post(
    "",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Crear recordatorio"""
    service = ReminderService(db)
    
    reminder = service.create_reminder(
        user_id=TEMP_USER_ID,  # ✅ USANDO USER TEMPORAL
        **reminder_data.model_dump()
    )
    
    return reminder


@router.get(
    "",
    response_model=List[ReminderResponse],
)
async def get_reminders(
    status: Optional[str] = Query(None, description="pending, completed, cancelled"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Listar recordatorios del usuario"""
    service = ReminderService(db)
    
    reminders = service.get_user_reminders(
        user_id=TEMP_USER_ID,  # ✅ USANDO USER TEMPORAL
        status=status,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    
    return reminders


@router.get(
    "/today",
    response_model=List[ReminderResponse],
)
async def get_today_reminders(
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Obtener recordatorios de hoy"""
    service = ReminderService(db)
    return service.get_today_reminders(TEMP_USER_ID)  # ✅ USANDO USER TEMPORAL


@router.get(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
async def get_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Obtener recordatorio específico"""
    service = ReminderService(db)
    reminder = service.get_reminder(reminder_id, TEMP_USER_ID)  # ✅ USANDO USER TEMPORAL
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    
    return reminder


@router.put(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
async def update_reminder(
    reminder_id: UUID,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Actualizar recordatorio"""
    service = ReminderService(db)
    
    update_dict = reminder_data.model_dump(exclude_unset=True)
    reminder = service.update_reminder(reminder_id, TEMP_USER_ID, **update_dict)  # ✅ USANDO USER TEMPORAL
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    
    return reminder


@router.patch(
    "/{reminder_id}/complete",
    response_model=ReminderResponse,
)
async def complete_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Marcar recordatorio como completado"""
    service = ReminderService(db)
    reminder = service.complete_reminder(reminder_id, TEMP_USER_ID)  # ✅ USANDO USER TEMPORAL
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    
    return reminder


@router.delete(
    "/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),  # ❌ COMENTADO
):
    """Eliminar recordatorio"""
    service = ReminderService(db)
    deleted = service.delete_reminder(reminder_id, TEMP_USER_ID)  # ✅ USANDO USER TEMPORAL
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
