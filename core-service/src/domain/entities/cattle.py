# src/domain/entities/cattle.py
from datetime import datetime, date
from typing import Optional
from uuid import UUID
from enum import Enum

class CattleStatus(str, Enum):
    ACTIVE = "active"
    SOLD = "sold"
    DECEASED = "deceased"
    QUARANTINE = "quarantine"

class ReproductiveStatus(str, Enum):
    EMPTY = "empty"
    PREGNANT = "pregnant"
    LACTATING = "lactating"
    DRY = "dry"

class Cattle:
    def __init__(
        self,
        id: UUID,
        ranch_id: UUID,
        owner_id: UUID,
        name: str,
        tag_number: str,
        birth_date: date,
        breed: str,
        gender: str,
        lot: str,
        status: CattleStatus = CattleStatus.ACTIVE,
        reproductive_status: Optional[ReproductiveStatus] = None,
        weight: Optional[float] = None,
        last_birth_date: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.ranch_id = ranch_id
        self.owner_id = owner_id
        self.name = name
        self.tag_number = tag_number
        self.birth_date = birth_date
        self.breed = breed
        self.gender = gender
        self.lot = lot
        self.status = status
        self.reproductive_status = reproductive_status
        self.weight = weight
        self.last_birth_date = last_birth_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
