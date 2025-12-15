# core-service/src/api/v1/cattle.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID

from src.infrastructure.database import get_db
# from src.infrastructure.auth.dependencies import get_current_user, UserAuth  # ❌ QUITAR
from src.application.cattle_service import CattleService
from src.schemas.cattle import (
    CattleCreate,
    CattleUpdate,
    CattleResponse,
    CattleListResponse,
    GenderEnum,
)

router = APIRouter()  # ✅ SIN prefix aquí



@router.post(
    "",
    response_model=CattleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cattle(
    cattle_data: CattleCreate,
    db = Depends(get_db),
):
    """Registrar nuevo animal"""
    try:
        service = CattleService(db)
        result = service.create_cattle(
            name=cattle_data.name,
            lote=cattle_data.lote,
            breed=cattle_data.breed,
            gender=cattle_data.gender.value,
            birth_date=cattle_data.birth_date,
            weight=cattle_data.weight,
            fecha_ultimo_parto=cattle_data.fecha_ultimo_parto,
        )
        return result["cattle"]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=CattleListResponse,
)
async def get_cattle_list(
    gender: Optional[GenderEnum] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db = Depends(get_db),
):
    """Listar todo el ganado"""
    service = CattleService(db)
    result = service.get_all_cattle(
        gender=gender.value if gender else None,
        skip=skip,
        limit=limit,
    )
    return CattleListResponse(
        total=result["total"],
        cattle=result["cattle"],
    )


@router.get(
    "/search",
    response_model=list[CattleResponse],
)
async def search_cattle(
    query: str = Query(..., min_length=1, description="Buscar por número de lote"),
    db = Depends(get_db),
):
    """Buscar ganado por número de lote"""
    service = CattleService(db)
    cattle = service.search_by_lote(query)
    return cattle


@router.get(
    "/{cattle_id}",
    response_model=CattleResponse,
)
async def get_cattle(
    cattle_id: UUID,
    db = Depends(get_db),
):
    """Obtener un animal específico"""
    service = CattleService(db)
    cattle = service.get_cattle(cattle_id)
    
    if not cattle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado",
        )
    
    return cattle


@router.put(
    "/{cattle_id}",
    response_model=CattleResponse,
)
async def update_cattle(
    cattle_id: UUID,
    cattle_data: CattleUpdate,
    db = Depends(get_db),
):
    """Actualizar información del animal"""
    service = CattleService(db)
    
    update_dict = cattle_data.model_dump(exclude_unset=True)
    if "gender" in update_dict and update_dict["gender"]:
        update_dict["gender"] = update_dict["gender"].value
    
    cattle = service.update_cattle(
        cattle_id,
        **update_dict,
    )
    
    if not cattle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado",
        )
    
    return cattle


@router.delete(
    "/{cattle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cattle(
    cattle_id: UUID,
    db = Depends(get_db),
):
    """Eliminar animal"""
    service = CattleService(db)
    deleted = service.delete_cattle(cattle_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado",
        )
