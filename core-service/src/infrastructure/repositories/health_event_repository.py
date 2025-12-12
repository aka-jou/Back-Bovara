# src/infrastructure/repositories/health_event_repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.models.health_event import HealthEvent


class HealthEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> HealthEvent:
        """Crear nuevo evento de salud"""
        event = HealthEvent(**kwargs)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_by_id(self, event_id: UUID) -> Optional[HealthEvent]:
        """Obtener evento por ID"""
        return self.db.query(HealthEvent).filter(HealthEvent.id == event_id).first()

    def get_by_cattle(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener todos los eventos de un animal"""
        return (
            self.db.query(HealthEvent)
            .filter(HealthEvent.cattle_id == cattle_id)
            .order_by(HealthEvent.application_date.desc())
            .all()
        )

    def get_vaccines_by_cattle(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener solo vacunas de un animal"""
        return (
            self.db.query(HealthEvent)
            .filter(
                HealthEvent.cattle_id == cattle_id,
                HealthEvent.event_type == "vaccine"
            )
            .order_by(HealthEvent.application_date.desc())
            .all()
        )

    def get_by_cattle_and_id(
        self, 
        event_id: UUID, 
        cattle_id: UUID
    ) -> Optional[HealthEvent]:
        """Obtener evento específico de un animal"""
        return (
            self.db.query(HealthEvent)
            .filter(
                HealthEvent.id == event_id,
                HealthEvent.cattle_id == cattle_id
            )
            .first()
        )

    def update(self, event_id: UUID, **updates) -> Optional[HealthEvent]:
        """Actualizar evento"""
        event = self.get_by_id(event_id)
        if not event:
            return None
        
        for key, value in updates.items():
            if value is not None:
                setattr(event, key, value)
        
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete(self, event_id: UUID) -> bool:
        """Eliminar evento"""
        event = self.get_by_id(event_id)
        if not event:
            return False
        
        self.db.delete(event)
        self.db.commit()
        return True

    def get_upcoming_doses(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener próximas dosis programadas"""
        from datetime import datetime
        today = datetime.now().date()
        
        return (
            self.db.query(HealthEvent)
            .filter(
                HealthEvent.cattle_id == cattle_id,
                HealthEvent.next_dose_date >= today
            )
            .order_by(HealthEvent.next_dose_date)
            .all()
        )
