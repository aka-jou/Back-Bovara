# src/domain/entities/ranch.py
from datetime import datetime
from typing import Optional
from uuid import UUID

class Ranch:
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        name: str,
        location: Optional[str] = None,
        size_hectares: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.location = location
        self.size_hectares = size_hectares
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
