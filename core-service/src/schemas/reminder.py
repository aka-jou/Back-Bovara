# src/schemas/reminder.py
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional


class ReminderBase(BaseModel):
    cattle_id: Optional[UUID] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    reminder_date: date
    reminder_type: str = Field(..., pattern="^(vaccine|checkup|treatment|feeding|breeding|other)$")


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    cattle_id: Optional[UUID] = None
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    reminder_date: Optional[date] = None
    reminder_type: Optional[str] = Field(None, pattern="^(vaccine|checkup|treatment|feeding|breeding|other)$")
    status: Optional[str] = Field(None, pattern="^(pending|completed|cancelled)$")


class ReminderResponse(ReminderBase):
    id: UUID
    user_id: UUID
    status: str
    health_event_id: Optional[UUID] = None  # ✅ OPCIONAL
    completed_at: Optional[datetime] = None  # ✅ OPCIONAL
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
