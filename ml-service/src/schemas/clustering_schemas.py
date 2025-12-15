from pydantic import BaseModel
from typing import Dict


class HealthStats(BaseModel):
    total_eventos: int
    total_vacunas: int
    total_tratamientos: int
    total_enfermedades: int


class ClusterPredictionResponse(BaseModel):
    cattle_id: str
    name: str
    lote: str
    cluster_id: int
    cluster_type: str
    health_stats: HealthStats


class TrainClusteringResponse(BaseModel):
    total_cattle: int
    clusters_created: int
    cluster_distribution: Dict[int, int]
    message: str = "Modelo entrenado exitosamente"


class AllClustersResponse(BaseModel):
    total_cattle: int
    cattle: list
