# src/application/cattle_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from src.infrastructure.repositories.cattle_repository import CattleRepository
from src.exceptions import CattleNotFoundException


class CattleService:
    def __init__(self, db: Session):
        self.db = db
        self.cattle_repo = CattleRepository(db)

    def create_cattle(
        self,
        owner_id: UUID,
        name: str,
        lote: str,
        breed: Optional[str],
        gender: str,
        birth_date: Optional[date],
        weight: Optional[float],
        fecha_ultimo_parto: Optional[date] = None,
    ) -> dict:
        """Crear nuevo animal"""
        
        # Verificar que el lote no exista
        existing = self.cattle_repo.get_by_lote(lote)
        if existing:
            raise ValueError(f"Ya existe un animal con el lote {lote}")
        
        cattle = self.cattle_repo.create(
            owner_id=owner_id,
            name=name,
            lote=lote,
            breed=breed,
            gender=gender,
            birth_date=birth_date,
            weight=weight,
            fecha_ultimo_parto=fecha_ultimo_parto,
        )
        
        return {"cattle": cattle}

    def get_user_cattle(
        self,
        owner_id: UUID,
        gender: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> dict:
        """Obtener ganado del usuario con filtros"""
        
        cattle_list = self.cattle_repo.get_by_owner(
            owner_id=owner_id,
            gender=gender,
            skip=skip,
            limit=limit,
        )
        
        total = self.cattle_repo.count_by_owner(owner_id, gender)
        
        return {
            "total": total,
            "cattle": cattle_list,
        }

    def get_cattle(self, cattle_id: UUID, owner_id: UUID) -> Optional:
        """Obtener animal específico"""
        return self.cattle_repo.get_by_id_and_owner(cattle_id, owner_id)

    def update_cattle(
        self,
        cattle_id: UUID,
        owner_id: UUID,
        **updates
    ) -> Optional:
        """Actualizar animal"""
        cattle = self.get_cattle(cattle_id, owner_id)
        if not cattle:
            return None
        
        return self.cattle_repo.update(cattle_id, **updates)

    def delete_cattle(self, cattle_id: UUID, owner_id: UUID) -> bool:
        """Eliminar animal"""
        cattle = self.get_cattle(cattle_id, owner_id)
        if not cattle:
            return False
        
        return self.cattle_repo.delete(cattle_id)

    def search_by_lote(self, query: str, owner_id: UUID) -> List:
        """Buscar por número de lote"""
        return self.cattle_repo.search_by_lote(query, owner_id)
