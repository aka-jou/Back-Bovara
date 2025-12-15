from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.services.clustering_service import ClusteringService
from src.schemas.clustering_schemas import (
    ClusterPredictionResponse,
    TrainClusteringResponse,
    AllClustersResponse
)

router = APIRouter(prefix="/clustering", tags=["Clustering"])


@router.post(
    "/train",
    response_model=TrainClusteringResponse,
    status_code=status.HTTP_200_OK
)
def train_clustering_model(db: Session = Depends(get_db)):
    """Entrenar modelo de clustering"""
    try:
        service = ClusteringService(db)
        result = service.train_model()
        
        return {
            "total_cattle": result["total_cattle"],
            "clusters_created": result["clusters_created"],
            "cluster_distribution": result["cluster_distribution"],
            "message": "Modelo entrenado exitosamente"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error entrenando modelo: {str(e)}"
        )


@router.get(
    "/predict/{cattle_id}",
    response_model=ClusterPredictionResponse,
    status_code=status.HTTP_200_OK
)
def predict_cattle_cluster(
    cattle_id: UUID,
    db: Session = Depends(get_db)
):
    """Predecir cluster de un ganado específico"""
    try:
        service = ClusteringService(db)
        result = service.predict_cluster(cattle_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ganado no encontrado"
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error prediciendo cluster: {str(e)}"
        )


@router.get(
    "/all",
    response_model=AllClustersResponse,
    status_code=status.HTTP_200_OK
)
def get_all_clusters(db: Session = Depends(get_db)):
    """Obtener clusters de todo el ganado"""
    try:
        service = ClusteringService(db)
        result = service.get_all_clusters()
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo clusters: {str(e)}"
        )
