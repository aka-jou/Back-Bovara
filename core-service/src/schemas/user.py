# src/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    ranch_name: Optional[str] = None  # ✅ NUEVO


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    ranch_name: Optional[str] = None  # ✅ NUEVO


class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

