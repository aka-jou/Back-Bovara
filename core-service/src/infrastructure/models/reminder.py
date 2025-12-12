from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from src.infrastructure.database import Base


class ReminderTypeEnum(str, enum.Enum):
    vaccine = "vaccine"
    checkup = "checkup"
    treatment = "treatment"
    feeding = "feeding"
    breeding = "breeding"
    other = "other"


class ReminderStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # ✅ SIN ForeignKey
    cattle_id = Column(UUID(as_uuid=True), ForeignKey("cattle.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(200), nullable=False)
    description = Column(Text)
    reminder_date = Column(Date, nullable=False, index=True)
    reminder_type = Column(SQLEnum(ReminderTypeEnum), nullable=False)
    status = Column(SQLEnum(ReminderStatusEnum), default=ReminderStatusEnum.pending, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    cattle = relationship("Cattle", back_populates="reminders")
