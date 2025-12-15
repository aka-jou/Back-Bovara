from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.services.multimodal_forecasting_service import MultimodalForecastingService
from src.schemas.multimodal_schemas import (
    TrainModelResponse,
    MultimodalPredictionResponse
)

router = APIRouter(prefix="/forecasting", tags=["Multimodal Heat Forecasting"])


@router.post(
    "/train",
    response_model=TrainModelResponse,
    status_code=status.HTTP_200_OK
)
def train_forecasting_models(db: Session = Depends(get_db)):
    """Entrenar modelos Random Forest y XGBoost para forecasting"""
    try:
        service = MultimodalForecastingService(db)
        result = service.train_models()
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error entrenando modelos: {str(e)}"
        )


@router.get(
    "/predict/{cattle_id}",
    response_model=MultimodalPredictionResponse,
    status_code=status.HTTP_200_OK
)
def predict_next_heat(
    cattle_id: UUID,
    db: Session = Depends(get_db)
):
    """Predecir próximo celo usando ML multimodal"""
    try:
        service = MultimodalForecastingService(db)
        result = service.predict_next_heat(cattle_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ganado no encontrado"
            )
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error prediciendo celo: {str(e)}"
        )
