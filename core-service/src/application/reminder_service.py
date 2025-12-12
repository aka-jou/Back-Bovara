# src/application/reminder_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.repositories.reminder_repository import ReminderRepository


class ReminderService:
    def __init__(self, db: Session):
        self.db = db
        self.reminder_repo = ReminderRepository(db)

    def create_reminder(
        self,
        user_id: UUID,
        title: str,
        reminder_date: date,
        reminder_type: str,
        cattle_id: Optional[UUID] = None,
        description: Optional[str] = None,
    ):
        """Crear nuevo recordatorio"""
        
        reminder = self.reminder_repo.create(
            user_id=user_id,
            cattle_id=cattle_id,
            title=title,
            description=description,
            reminder_date=reminder_date,
            reminder_type=reminder_type,
            status="pending",
        )
        
        return reminder

    def get_user_reminders(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List:
        """Obtener recordatorios del usuario"""
        return self.reminder_repo.get_by_user(
            user_id=user_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit,
        )

    def get_today_reminders(self, user_id: UUID) -> List:
        """Obtener recordatorios de hoy"""
        return self.reminder_repo.get_today_reminders(user_id)

    def get_reminder(self, reminder_id: UUID, user_id: UUID) -> Optional:
        """Obtener recordatorio específico"""
        return self.reminder_repo.get_by_id_and_user(reminder_id, user_id)

    def update_reminder(self, reminder_id: UUID, user_id: UUID, **updates) -> Optional:
        """Actualizar recordatorio"""
        
        # Verificar que pertenece al usuario
        reminder = self.get_reminder(reminder_id, user_id)
        if not reminder:
            return None
        
        return self.reminder_repo.update(reminder_id, **updates)

    def complete_reminder(self, reminder_id: UUID, user_id: UUID) -> Optional:
        """Marcar como completado"""
        
        reminder = self.get_reminder(reminder_id, user_id)
        if not reminder:
            return None
        
        return self.reminder_repo.mark_completed(reminder_id)

    def delete_reminder(self, reminder_id: UUID, user_id: UUID) -> bool:
        """Eliminar recordatorio"""
        
        reminder = self.get_reminder(reminder_id, user_id)
        if not reminder:
            return False
        
        return self.reminder_repo.delete(reminder_id)
