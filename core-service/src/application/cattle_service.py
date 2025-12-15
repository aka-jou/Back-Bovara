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
        
        # ✅ Sin owner_id - necesitas ajustar el repository.create() también
        # Si tu tabla cattle REQUIERE owner_id, puedes usar un UUID fijo o NULL
        cattle = self.cattle_repo.create(
            name=name,
            lote=lote,
            breed=breed,
            gender=gender,
            birth_date=birth_date,
            weight=weight,
            fecha_ultimo_parto=fecha_ultimo_parto,
        )
        
        return {"cattle": cattle}

    def get_all_cattle(
        self,
        gender: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> dict:
        """Obtener todo el ganado con filtros"""
        
        cattle_list = self.cattle_repo.get_all(
            gender=gender,
            skip=skip,
            limit=limit,
        )
        
        total = self.cattle_repo.count_all(gender)
        
        return {
            "total": total,
            "cattle": cattle_list,
        }

    def get_cattle(self, cattle_id: UUID) -> Optional:
        """Obtener animal específico"""
        return self.cattle_repo.get_by_id(cattle_id)

    def update_cattle(
        self,
        cattle_id: UUID,
        **updates
    ) -> Optional:
        """Actualizar animal"""
        cattle = self.get_cattle(cattle_id)
        if not cattle:
            return None
        
        return self.cattle_repo.update(cattle_id, **updates)

    def delete_cattle(self, cattle_id: UUID) -> bool:
        """Eliminar animal"""
        cattle = self.get_cattle(cattle_id)
        if not cattle:
            return False
        
        return self.cattle_repo.delete(cattle_id)

    def search_by_lote(self, query: str) -> List:
        """Buscar por número de lote"""
        return self.cattle_repo.search_by_lote(query)
