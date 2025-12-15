from pydantic import BaseModel
from typing import Optional


class TrainModelResponse(BaseModel):
    total_records: int
    features_count: int
    message: str


class MultimodalPredictionResponse(BaseModel):
    cattle_id: str
    last_heat_date: str
    predicted_days_rf: float
    predicted_days_xgb: float
    predicted_days_avg: float
    predicted_next_heat_date: str
    days_until_heat: int
    total_heat_records: int
    model_confidence: str
