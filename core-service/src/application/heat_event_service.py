from typing import List, Optional
from uuid import UUID

from src.schemas.heat_event import HeatEventCreate, HeatEventUpdate
from src.infrastructure.models.heat_event import HeatEventModel
from src.infrastructure.repositories.heat_event_repository import HeatEventRepository


class HeatEventService:
    def __init__(self, repository: HeatEventRepository):
        self.repository = repository
    
    def create_heat_event(self, heat_event_data: HeatEventCreate) -> HeatEventModel:
        # ✅ Cambio: usar dict() en lugar de model_dump()
        heat_event = HeatEventModel(**heat_event_data.dict())
        return self.repository.create(heat_event)
    
    def get_heat_event(self, heat_event_id: UUID) -> Optional[HeatEventModel]:
        return self.repository.get_by_id(heat_event_id)
    
    def get_heat_events_by_cattle(self, cattle_id: UUID) -> List[HeatEventModel]:
        return self.repository.get_by_cattle_id(cattle_id)
    
    def update_heat_event(self, heat_event_id: UUID, update_data: HeatEventUpdate) -> Optional[HeatEventModel]:
        heat_event = self.repository.get_by_id(heat_event_id)
        if not heat_event:
            return None
        
        # ✅ Cambio: usar dict() en lugar de model_dump()
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(heat_event, key, value)
        
        return self.repository.update(heat_event)
    
    def delete_heat_event(self, heat_event_id: UUID) -> bool:
        return self.repository.delete(heat_event_id)
