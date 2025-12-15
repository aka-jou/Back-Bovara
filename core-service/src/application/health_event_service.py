# src/application/health_event_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.repositories.health_event_repository import HealthEventRepository
from src.infrastructure.repositories.cattle_repository import CattleRepository
from src.infrastructure.models.health_event import HealthEvent


class HealthEventService:
    def __init__(self, db: Session):
        self.db = db
        self.health_repo = HealthEventRepository(db)
        self.cattle_repo = CattleRepository(db)

    def create_health_event(
        self,
        cattle_id: UUID,
        event_type: str,
        application_date: date,
        disease_name: Optional[str] = None,
        medicine_name: Optional[str] = None,
        administration_route: Optional[str] = None,
        next_dose_date: Optional[date] = None,
        treatment_end_date: Optional[date] = None,
        dosage: Optional[str] = None,
        veterinarian_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> HealthEvent:
        """Crear nuevo evento de salud"""
        
        # Verificar que el cattle existe (sin filtro de owner)
        cattle = self.cattle_repo.get_by_id(cattle_id)
        if not cattle:
            raise ValueError("Animal no encontrado")
        
        event = self.health_repo.create(
            cattle_id=cattle_id,
            event_type=event_type,
            disease_name=disease_name,
            medicine_name=medicine_name,
            application_date=application_date,
            administration_route=administration_route,
            next_dose_date=next_dose_date,
            treatment_end_date=treatment_end_date,
            dosage=dosage,
            veterinarian_name=veterinarian_name,
            notes=notes,
        )
        
        return event

    def get_events_by_cattle(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener todos los eventos de un animal"""
        
        # Verificar que el cattle existe
        cattle = self.cattle_repo.get_by_id(cattle_id)
        if not cattle:
            raise ValueError("Animal no encontrado")
        
        return self.health_repo.get_by_cattle(cattle_id)

    def get_event_by_id(self, event_id: UUID) -> Optional[HealthEvent]:
        """Obtener evento por ID"""
        return self.health_repo.get_by_id(event_id)

    def update_event(self, event_id: UUID, **updates) -> Optional[HealthEvent]:
        """Actualizar evento"""
        return self.health_repo.update(event_id, **updates)

    def delete_event(self, event_id: UUID) -> bool:
        """Eliminar evento"""
        return self.health_repo.delete(event_id)

    def get_vaccines_by_cattle(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener solo vacunas de un animal"""
        
        cattle = self.cattle_repo.get_by_id(cattle_id)
        if not cattle:
            raise ValueError("Animal no encontrado")
        
        return self.health_repo.get_vaccines_by_cattle(cattle_id)

    def get_upcoming_doses(self, cattle_id: UUID) -> List[HealthEvent]:
        """Obtener próximas dosis"""
        
        cattle = self.cattle_repo.get_by_id(cattle_id)
        if not cattle:
            raise ValueError("Animal no encontrado")
        
        return self.health_repo.get_upcoming_doses(cattle_id)
