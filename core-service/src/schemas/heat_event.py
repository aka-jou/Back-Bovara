from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class HeatEventCreate(BaseModel):
    cattle_id: UUID
    heat_date: date
    allows_mounting: Optional[bool] = None
    vaginal_discharge: Optional[str] = None
    vulva_swelling: Optional[str] = None
    comportamiento: Optional[str] = None
    was_inseminated: bool = False
    insemination_date: Optional[date] = None
    pregnancy_confirmed: Optional[bool] = None


class HeatEventUpdate(BaseModel):
    heat_date: Optional[date] = None
    allows_mounting: Optional[bool] = None
    vaginal_discharge: Optional[str] = None
    vulva_swelling: Optional[str] = None
    comportamiento: Optional[str] = None
    was_inseminated: Optional[bool] = None
    insemination_date: Optional[date] = None
    pregnancy_confirmed: Optional[bool] = None


class HeatEventResponse(BaseModel):
    id: UUID
    cattle_id: UUID
    heat_date: date
    allows_mounting: Optional[bool]
    vaginal_discharge: Optional[str]
    vulva_swelling: Optional[str]
    comportamiento: Optional[str]
    was_inseminated: bool
    insemination_date: Optional[date]
    pregnancy_confirmed: Optional[bool]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
