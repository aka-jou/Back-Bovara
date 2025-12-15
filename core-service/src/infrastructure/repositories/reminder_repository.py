# src/infrastructure/repositories/reminder_repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.models.reminder import Reminder


class ReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Reminder:
        """Crear nuevo recordatorio"""
        reminder = Reminder(**kwargs)
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def get_by_id(self, reminder_id: UUID) -> Optional[Reminder]:
        """Obtener recordatorio por ID"""
        return self.db.query(Reminder).filter(Reminder.id == reminder_id).first()

    # ✅ AGREGAR ESTOS MÉTODOS PÚBLICOS (sin user_id)
    
    def get_all(
        self,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Reminder]:
        """Obtener todos los recordatorios (sin filtro de user)"""
        query = self.db.query(Reminder)
        
        if status:
            query = query.filter(Reminder.status == status)
        
        if start_date:
            query = query.filter(Reminder.reminder_date >= start_date)
        
        if end_date:
            query = query.filter(Reminder.reminder_date <= end_date)
        
        return query.order_by(Reminder.reminder_date).offset(skip).limit(limit).all()

    def get_today_reminders(self) -> List[Reminder]:
        """Obtener recordatorios de hoy (sin filtro de user)"""
        from datetime import datetime
        today = datetime.now().date()
        
        return (
            self.db.query(Reminder)
            .filter(
                Reminder.reminder_date == today,
                Reminder.status == "pending"
            )
            .order_by(Reminder.reminder_date)
            .all()
        )

    # ============================================
    # MÉTODOS CON USER_ID (legacy - puedes mantenerlos por compatibilidad)
    # ============================================

    def get_by_user(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Reminder]:
        """Obtener recordatorios de un usuario con filtros"""
        query = self.db.query(Reminder).filter(Reminder.user_id == user_id)
        
        if status:
            query = query.filter(Reminder.status == status)
        
        if start_date:
            query = query.filter(Reminder.reminder_date >= start_date)
        
        if end_date:
            query = query.filter(Reminder.reminder_date <= end_date)
        
        return query.order_by(Reminder.reminder_date).offset(skip).limit(limit).all()

    def get_pending_reminders(self, user_id: UUID) -> List[Reminder]:
        """Obtener recordatorios pendientes"""
        return (
            self.db.query(Reminder)
            .filter(
                Reminder.user_id == user_id,
                Reminder.status == "pending"
            )
            .order_by(Reminder.reminder_date)
            .all()
        )

    def get_by_id_and_user(
        self, 
        reminder_id: UUID, 
        user_id: UUID
    ) -> Optional[Reminder]:
        """Obtener recordatorio específico de un usuario"""
        return (
            self.db.query(Reminder)
            .filter(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id
            )
            .first()
        )

    def count_by_user(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> int:
        """Contar recordatorios de un usuario"""
        query = self.db.query(Reminder).filter(Reminder.user_id == user_id)
        
        if status:
            query = query.filter(Reminder.status == status)
        
        if start_date:
            query = query.filter(Reminder.reminder_date >= start_date)
        
        if end_date:
            query = query.filter(Reminder.reminder_date <= end_date)
        
        return query.count()

    def update(self, reminder_id: UUID, **updates) -> Optional[Reminder]:
        """Actualizar recordatorio"""
        reminder = self.get_by_id(reminder_id)
        if not reminder:
            return None
        
        for key, value in updates.items():
            if value is not None:
                setattr(reminder, key, value)
        
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def mark_completed(self, reminder_id: UUID) -> Optional[Reminder]:
        """Marcar recordatorio como completado"""
        return self.update(reminder_id, status="completed")

    def mark_cancelled(self, reminder_id: UUID) -> Optional[Reminder]:
        """Marcar recordatorio como cancelado"""
        return self.update(reminder_id, status="cancelled")

    def delete(self, reminder_id: UUID) -> bool:
        """Eliminar recordatorio"""
        reminder = self.get_by_id(reminder_id)
        if not reminder:
            return False
        
        self.db.delete(reminder)
        self.db.commit()
        return True
