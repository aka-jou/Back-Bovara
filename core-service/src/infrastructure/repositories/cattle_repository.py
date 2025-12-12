from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.models.cattle import Cattle


class CattleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Cattle:
        """Crear nuevo animal"""
        cattle = Cattle(**kwargs)
        self.db.add(cattle)
        self.db.commit()
        self.db.refresh(cattle)
        return cattle

    def get_by_id(self, cattle_id: UUID) -> Optional[Cattle]:
        """Obtener por ID"""
        return self.db.query(Cattle).filter(Cattle.id == cattle_id).first()

    def get_by_id_and_owner(self, cattle_id: UUID, owner_id: UUID) -> Optional[Cattle]:
        """Obtener por ID y dueño"""
        return self.db.query(Cattle).filter(
            Cattle.id == cattle_id,
            Cattle.owner_id == owner_id
        ).first()

    def get_by_lote(self, lote: str) -> Optional[Cattle]:
        """Obtener por número de lote"""
        return self.db.query(Cattle).filter(Cattle.lote == lote).first()

    def get_by_owner(
        self,
        owner_id: UUID,
        gender: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Cattle]:
        """Obtener ganado de un usuario"""
        query = self.db.query(Cattle).filter(Cattle.owner_id == owner_id)
        
        if gender:
            query = query.filter(Cattle.gender == gender)
        
        return query.offset(skip).limit(limit).all()

    def count_by_owner(self, owner_id: UUID, gender: Optional[str] = None) -> int:
        """Contar ganado de un usuario"""
        query = self.db.query(Cattle).filter(Cattle.owner_id == owner_id)
        
        if gender:
            query = query.filter(Cattle.gender == gender)
        
        return query.count()

    def search_by_lote(self, query: str, owner_id: UUID) -> List[Cattle]:
        """Buscar por lote"""
        return self.db.query(Cattle).filter(
            Cattle.owner_id == owner_id,
            Cattle.lote.ilike(f"%{query}%")
        ).all()

    def update(self, cattle_id: UUID, **updates) -> Optional[Cattle]:
        """Actualizar animal"""
        cattle = self.get_by_id(cattle_id)
        if not cattle:
            return None
        
        for key, value in updates.items():
            if value is not None:
                setattr(cattle, key, value)
        
        self.db.commit()
        self.db.refresh(cattle)
        return cattle

    def delete(self, cattle_id: UUID) -> bool:
        """Eliminar animal"""
        cattle = self.get_by_id(cattle_id)
        if not cattle:
            return False
        
        self.db.delete(cattle)
        self.db.commit()
        return True
