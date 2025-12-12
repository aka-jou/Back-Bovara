# src/infrastructure/schemas/ranch.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class RanchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=500)
    size_hectares: Optional[float] = Field(None, gt=0)

class RanchCreate(RanchBase):
    pass

class RanchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=500)
    size_hectares: Optional[float] = Field(None, gt=0)

class RanchResponse(RanchBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    cattle_count: int = 0

    class Config:
        from_attributes = True
