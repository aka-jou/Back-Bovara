from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from typing import Optional, Dict


class ClusteringService:
    def __init__(self, db: Session):
        self.db = db
        self.n_clusters = 4
        self.kmeans = None
        self.scaler = StandardScaler()
    
    def _get_health_stats(self) -> pd.DataFrame:
        query = text("""
            SELECT 
                c.id as cattle_id,
                c.name,
                c.lote,
                COUNT(he.id) as total_eventos,
                COUNT(CASE WHEN he.event_type = 'vaccine' THEN 1 END) as total_vacunas,
                COUNT(CASE WHEN he.event_type = 'treatment' THEN 1 END) as total_tratamientos,
                COUNT(CASE WHEN he.event_type = 'illness' THEN 1 END) as total_enfermedades
            FROM cattle c
            LEFT JOIN health_events he ON c.id = he.cattle_id
            GROUP BY c.id, c.name, c.lote
        """)
        
        result = self.db.execute(query)
        data = result.fetchall()
        
        df = pd.DataFrame(data, columns=[
            'cattle_id', 'name', 'lote', 
            'total_eventos', 'total_vacunas', 
            'total_tratamientos', 'total_enfermedades'
        ])
        
        return df
    
    def train_model(self) -> Dict:
        df = self._get_health_stats()
        
        if len(df) < 10:
            raise ValueError("Necesitas al menos 10 registros de ganado para clustering")
        
        features = df[['total_eventos', 'total_vacunas', 'total_tratamientos', 'total_enfermedades']].values
        features_scaled = self.scaler.fit_transform(features)
        
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        df['cluster'] = self.kmeans.fit_predict(features_scaled)
        
        cluster_stats = df.groupby('cluster')[['total_eventos', 'total_vacunas', 'total_tratamientos', 'total_enfermedades']].mean()
        
        return {
            "total_cattle": len(df),
            "clusters_created": self.n_clusters,
            "cluster_distribution": df['cluster'].value_counts().to_dict(),
            "cluster_stats": cluster_stats.to_dict()
        }
    
    def predict_cluster(self, cattle_id: UUID) -> Optional[Dict]:
        query = text("""
            SELECT 
                c.id as cattle_id,
                c.name,
                c.lote,
                COUNT(he.id) as total_eventos,
                COUNT(CASE WHEN he.event_type = 'vaccine' THEN 1 END) as total_vacunas,
                COUNT(CASE WHEN he.event_type = 'treatment' THEN 1 END) as total_tratamientos,
                COUNT(CASE WHEN he.event_type = 'illness' THEN 1 END) as total_enfermedades
            FROM cattle c
            LEFT JOIN health_events he ON c.id = he.cattle_id
            WHERE c.id = :cattle_id
            GROUP BY c.id, c.name, c.lote
        """)
        
        result = self.db.execute(query, {"cattle_id": str(cattle_id)})
        data = result.fetchone()
        
        if not data:
            return None
        
        if self.kmeans is None:
            self.train_model()
        
        features = np.array([[
            data.total_eventos,
            data.total_vacunas,
            data.total_tratamientos,
            data.total_enfermedades
        ]])
        
        features_scaled = self.scaler.transform(features)
        cluster = int(self.kmeans.predict(features_scaled)[0])
        
        cluster_label = self._get_cluster_label(
            data.total_eventos,
            data.total_vacunas,
            data.total_tratamientos,
            data.total_enfermedades
        )
        
        return {
            "cattle_id": str(cattle_id),
            "name": data.name,
            "lote": data.lote,
            "cluster_id": cluster,
            "cluster_type": cluster_label,
            "health_stats": {
                "total_eventos": data.total_eventos,
                "total_vacunas": data.total_vacunas,
                "total_tratamientos": data.total_tratamientos,
                "total_enfermedades": data.total_enfermedades
            }
        }
    
    def _get_cluster_label(self, eventos: int, vacunas: int, tratamientos: int, enfermedades: int) -> str:
        if eventos <= 1:
            return "Ganado Sano"
        elif vacunas >= 3 and tratamientos <= 1 and enfermedades == 0:
            return "Mantenimiento Regular"
        elif enfermedades >= 2 or tratamientos >= 4:
            return "Alta Atención Médica"
        elif tratamientos >= 2:
            return "Ganado en Tratamiento"
        else:
            return "Mantenimiento Regular"
    
    def get_all_clusters(self) -> Dict:
        df = self._get_health_stats()
        
        if self.kmeans is None:
            self.train_model()
        
        features = df[['total_eventos', 'total_vacunas', 'total_tratamientos', 'total_enfermedades']].values
        features_scaled = self.scaler.transform(features)
        df['cluster'] = self.kmeans.predict(features_scaled)
        
        df['cluster_type'] = df.apply(
            lambda row: self._get_cluster_label(
                row['total_eventos'],
                row['total_vacunas'],
                row['total_tratamientos'],
                row['total_enfermedades']
            ),
            axis=1
        )
        
        result = []
        for _, row in df.iterrows():
            result.append({
                "cattle_id": str(row['cattle_id']),
                "name": row['name'],
                "lote": row['lote'],
                "cluster_id": int(row['cluster']),
                "cluster_type": row['cluster_type'],
                "health_stats": {
                    "total_eventos": int(row['total_eventos']),
                    "total_vacunas": int(row['total_vacunas']),
                    "total_tratamientos": int(row['total_tratamientos']),
                    "total_enfermedades": int(row['total_enfermedades'])
                }
            })
        
        return {
            "total_cattle": len(result),
            "cattle": result
        }
