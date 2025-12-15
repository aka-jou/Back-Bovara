from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class CattleCreate(BaseModel):
    name: str
    lote: str
    breed: Optional[str] = None
    gender: GenderEnum
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    fecha_ultimo_parto: Optional[date] = None


class CattleUpdate(BaseModel):
    name: Optional[str] = None
    lote: Optional[str] = None
    breed: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    fecha_ultimo_parto: Optional[date] = None


class CattleResponse(BaseModel):
    id: UUID
    owner_id: Optional[UUID] = None  # ✅ CAMBIAR AQUÍ
    name: str
    lote: str
    breed: Optional[str] = None
    gender: GenderEnum
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    fecha_ultimo_parto: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CattleListResponse(BaseModel):
    total: int
    cattle: list[CattleResponse]
