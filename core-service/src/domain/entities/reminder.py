# src/domain/entities/reminder.py
from enum import Enum
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class ReminderType(str, Enum):
    VACCINE = "vaccine"
    CHECKUP = "checkup"
    TREATMENT = "treatment"
    GENERAL = "general"


class ReminderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Reminder:
    """Entidad de dominio para recordatorios"""
    
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        title: str,
        reminder_date: date,
        reminder_type: ReminderType = ReminderType.GENERAL,
        description: Optional[str] = None,
        cattle_id: Optional[UUID] = None,
        health_event_id: Optional[UUID] = None,
        status: ReminderStatus = ReminderStatus.PENDING,
        completed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.reminder_date = reminder_date
        self.reminder_type = reminder_type
        self.description = description
        self.cattle_id = cattle_id
        self.health_event_id = health_event_id
        self.status = status
        self.completed_at = completed_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def mark_completed(self) -> None:
        """Marcar recordatorio como completado"""
        self.status = ReminderStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def mark_cancelled(self) -> None:
        """Marcar recordatorio como cancelado"""
        self.status = ReminderStatus.CANCELLED
    
    def is_pending(self) -> bool:
        """Verificar si está pendiente"""
        return self.status == ReminderStatus.PENDING
    
    def is_overdue(self) -> bool:
        """Verificar si está vencido"""
        return self.is_pending() and self.reminder_date < date.today()
