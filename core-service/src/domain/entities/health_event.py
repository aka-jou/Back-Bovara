# src/domain/entities/health_event.py
from enum import Enum
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class EventType(str, Enum):
    VACCINATION = "vaccination"
    TREATMENT = "treatment"
    CHECKUP = "checkup"
    ILLNESS = "illness"


class AdministrationRoute(str, Enum):
    SUBCUTANEA = "Subcutánea"
    INTRAMUSCULAR = "Intramuscular"
    ORAL = "Oral"
    INTRAVENOSA = "Intravenosa"


class HealthEvent:
    """Entidad de dominio para eventos de salud del ganado"""
    
    def __init__(
        self,
        id: UUID,
        cattle_id: UUID,
        event_type: EventType,
        disease_name: str,
        medicine_name: str,
        application_date: date,
        administration_route: AdministrationRoute,
        next_dose_date: Optional[date] = None,
        treatment_end_date: Optional[date] = None,
        dosage: Optional[str] = None,
        veterinarian_name: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.cattle_id = cattle_id
        self.event_type = event_type
        self.disease_name = disease_name
        self.medicine_name = medicine_name
        self.application_date = application_date
        self.administration_route = administration_route
        self.next_dose_date = next_dose_date
        self.treatment_end_date = treatment_end_date
        self.dosage = dosage
        self.veterinarian_name = veterinarian_name
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_vaccination(self) -> bool:
        """Verificar si es una vacunación"""
        return self.event_type == EventType.VACCINATION
    
    def needs_follow_up(self) -> bool:
        """Verificar si necesita seguimiento"""
        return self.next_dose_date is not None or self.treatment_end_date is not None
