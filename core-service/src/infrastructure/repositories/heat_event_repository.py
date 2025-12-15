from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from src.infrastructure.models.heat_event import HeatEventModel


class HeatEventRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, heat_event: HeatEventModel) -> HeatEventModel:
        self.db.add(heat_event)
        self.db.commit()
        self.db.refresh(heat_event)
        return heat_event
    
    def get_by_id(self, heat_event_id: UUID) -> Optional[HeatEventModel]:
        return self.db.query(HeatEventModel).filter(
            HeatEventModel.id == heat_event_id
        ).first()
    
    def get_by_cattle_id(self, cattle_id: UUID) -> List[HeatEventModel]:
        return self.db.query(HeatEventModel).filter(
            HeatEventModel.cattle_id == cattle_id
        ).order_by(HeatEventModel.heat_date.desc()).all()
    
    def update(self, heat_event: HeatEventModel) -> HeatEventModel:
        self.db.commit()
        self.db.refresh(heat_event)
        return heat_event
    
    def delete(self, heat_event_id: UUID) -> bool:
        heat_event = self.get_by_id(heat_event_id)
        if heat_event:
            self.db.delete(heat_event)
            self.db.commit()
            return True
        return False
