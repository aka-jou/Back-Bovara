from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.clustering_service import ClusteringService
from src.schemas import (
    ClusterPredictionResponse,
    TrainModelResponse,
    AllClustersResponse
)

app = FastAPI(
    title="Bovara ML Service",
    description="Servicio de Machine Learning para clustering de ganado",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Bovara ML Service",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/v1/clustering/predict/{cattle_id}",
            "train": "/api/v1/clustering/train",
            "all_clusters": "/api/v1/clustering/all"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ml-service"}


@app.post(
    "/api/v1/clustering/train",
    response_model=TrainModelResponse,
    status_code=status.HTTP_200_OK
)
def train_clustering_model(db: Session = Depends(get_db)):
    """Entrenar modelo de clustering con todos los datos"""
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


@app.get(
    "/api/v1/clustering/predict/{cattle_id}",
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


@app.get(
    "/api/v1/clustering/all",
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
