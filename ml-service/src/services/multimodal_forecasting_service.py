from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
from typing import Optional, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
from pathlib import Path


class MultimodalForecastingService:
    def __init__(self, db: Session):
        self.db = db
        self.rf_model = None
        self.xgb_model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.model_path = Path("models")
        self.model_path.mkdir(exist_ok=True)
    
    def _get_heat_history_with_cattle_info(self) -> pd.DataFrame:
        """Obtener historial completo de celos con info de cattle"""
        query = text("""
            SELECT 
                he.id,
                he.cattle_id,
                he.heat_date,
                he.allows_mounting,
                he.vaginal_discharge,
                he.vulva_swelling,
                he.comportamiento,
                he.was_inseminated,
                he.pregnancy_confirmed,
                c.birth_date,
                c.weight,
                c.fecha_ultimo_parto,
                c.breed
            FROM heat_events he
            JOIN cattle c ON he.cattle_id = c.id
            WHERE c.gender = 'female'
            ORDER BY he.cattle_id, he.heat_date
        """)
        
        result = self.db.execute(query)
        data = result.fetchall()
        
        if not data:
            raise ValueError("No hay datos de celo disponibles en la base de datos")
        
        df = pd.DataFrame(data, columns=[
            'id', 'cattle_id', 'heat_date', 'allows_mounting',
            'vaginal_discharge', 'vulva_swelling', 'comportamiento',
            'was_inseminated', 'pregnancy_confirmed', 'birth_date',
            'weight', 'fecha_ultimo_parto', 'breed'
        ])
        
        df['heat_date'] = pd.to_datetime(df['heat_date'])
        df['birth_date'] = pd.to_datetime(df['birth_date'])
        df['fecha_ultimo_parto'] = pd.to_datetime(df['fecha_ultimo_parto'])
        
        return df
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Crear features multimodales"""
        df['age_days'] = (df['heat_date'] - df['birth_date']).dt.days
        df['days_since_last_birth'] = (df['heat_date'] - df['fecha_ultimo_parto']).dt.days
        df['days_since_last_birth'] = df['days_since_last_birth'].fillna(0)
        
        df['next_heat_date'] = df.groupby('cattle_id')['heat_date'].shift(-1)
        df['days_to_next_heat'] = (df['next_heat_date'] - df['heat_date']).dt.days
        
        for lag in [1, 2, 3]:
            df[f'allows_mounting_lag{lag}'] = df.groupby('cattle_id')['allows_mounting'].shift(lag)
            df[f'vaginal_discharge_lag{lag}'] = df.groupby('cattle_id')['vaginal_discharge'].shift(lag)
            df[f'vulva_swelling_lag{lag}'] = df.groupby('cattle_id')['vulva_swelling'].shift(lag)
            df[f'comportamiento_lag{lag}'] = df.groupby('cattle_id')['comportamiento'].shift(lag)
        
        df['prev_heat_date_1'] = df.groupby('cattle_id')['heat_date'].shift(1)
        df['prev_heat_date_2'] = df.groupby('cattle_id')['heat_date'].shift(2)
        
        df['interval_lag1'] = (df['heat_date'] - df['prev_heat_date_1']).dt.days
        df['interval_lag2'] = (df['prev_heat_date_1'] - df['prev_heat_date_2']).dt.days
        
        df['avg_last_2_intervals'] = (df['interval_lag1'] + df['interval_lag2']) / 2
        
        return df
    
    def _encode_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Encodificar variables categóricas"""
        if fit:
            self.label_encoders = {
                'discharge': LabelEncoder(),
                'swelling': LabelEncoder(),
                'comportamiento': LabelEncoder(),
                'breed': LabelEncoder()
            }
            
            all_discharge = pd.concat([df[f'vaginal_discharge_lag{i}'].fillna('unknown') for i in [1,2,3]])
            all_swelling = pd.concat([df[f'vulva_swelling_lag{i}'].fillna('unknown') for i in [1,2,3]])
            all_comportamiento = pd.concat([df[f'comportamiento_lag{i}'].fillna('unknown') for i in [1,2,3]])
            
            self.label_encoders['discharge'].fit(all_discharge)
            self.label_encoders['swelling'].fit(all_swelling)
            self.label_encoders['comportamiento'].fit(all_comportamiento)
            self.label_encoders['breed'].fit(df['breed'].fillna('unknown'))
        
        for lag in [1, 2, 3]:
            df[f'vaginal_discharge_lag{lag}_encoded'] = self.label_encoders['discharge'].transform(
                df[f'vaginal_discharge_lag{lag}'].fillna('unknown')
            )
            df[f'vulva_swelling_lag{lag}_encoded'] = self.label_encoders['swelling'].transform(
                df[f'vulva_swelling_lag{lag}'].fillna('unknown')
            )
            df[f'comportamiento_lag{lag}_encoded'] = self.label_encoders['comportamiento'].transform(
                df[f'comportamiento_lag{lag}'].fillna('unknown')
            )
            df[f'allows_mounting_lag{lag}_int'] = df[f'allows_mounting_lag{lag}'].fillna(0).astype(int)
        
        df['breed_encoded'] = self.label_encoders['breed'].transform(df['breed'].fillna('unknown'))
        
        return df
    
    def train_models(self) -> Dict:
        """Entrenar modelos Random Forest y XGBoost"""
        df = self._get_heat_history_with_cattle_info()
        
        if len(df) < 50:
            raise ValueError("Se necesitan al menos 50 registros para entrenar")
        
        df = self._create_features(df)
        df = self._encode_features(df, fit=True)
        
        self.feature_columns = [
            'age_days', 'weight', 'days_since_last_birth', 'breed_encoded',
            'allows_mounting_lag1_int', 'vaginal_discharge_lag1_encoded',
            'vulva_swelling_lag1_encoded', 'comportamiento_lag1_encoded',
            'allows_mounting_lag2_int', 'vaginal_discharge_lag2_encoded',
            'vulva_swelling_lag2_encoded', 'comportamiento_lag2_encoded',
            'allows_mounting_lag3_int', 'vaginal_discharge_lag3_encoded',
            'vulva_swelling_lag3_encoded', 'comportamiento_lag3_encoded',
            'interval_lag1', 'interval_lag2', 'avg_last_2_intervals'
        ]
        
        df_train = df[df['days_to_next_heat'].notna()].copy()
        df_train = df_train.dropna(subset=['weight', 'interval_lag1'])
        
        if len(df_train) < 30:
            raise ValueError("Datos insuficientes después de filtrar")
        
        X = df_train[self.feature_columns].copy()
        y = df_train['days_to_next_heat'].copy()
        
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X, y)
        
        self.xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.xgb_model.fit(X, y)
        
        self._save_models()
        
        return {
            "total_records": len(df_train),
            "features_count": len(self.feature_columns),
            "message": "Modelos entrenados exitosamente"
        }
    
    def _save_models(self):
        """Guardar modelos y encoders"""
        joblib.dump(self.rf_model, self.model_path / "rf_model.pkl")
        joblib.dump(self.xgb_model, self.model_path / "xgb_model.pkl")
        joblib.dump(self.label_encoders, self.model_path / "label_encoders.pkl")
        joblib.dump(self.feature_columns, self.model_path / "feature_columns.pkl")
    
    def _load_models(self):
        """Cargar modelos guardados"""
        if not (self.model_path / "rf_model.pkl").exists():
            raise ValueError("Modelos no entrenados. Ejecutar /train primero")
        
        self.rf_model = joblib.load(self.model_path / "rf_model.pkl")
        self.xgb_model = joblib.load(self.model_path / "xgb_model.pkl")
        self.label_encoders = joblib.load(self.model_path / "label_encoders.pkl")
        self.feature_columns = joblib.load(self.model_path / "feature_columns.pkl")
    
    def predict_next_heat(self, cattle_id: UUID) -> Optional[Dict]:
        """Predecir próximo celo de una vaca"""
        if self.rf_model is None:
            self._load_models()
        
        cattle_id_str = str(cattle_id)
        
        # Verificar que la vaca existe
        check_query = text("""
            SELECT id::text as id, gender
            FROM cattle
            WHERE id::text = :cattle_id
        """)
        
        check_result = self.db.execute(check_query, {"cattle_id": cattle_id_str})
        cattle_row = check_result.fetchone()
        
        if not cattle_row:
            raise ValueError(f"Vaca {cattle_id} no encontrada")
        
        if cattle_row.gender != 'female':
            raise ValueError(f"Vaca {cattle_id} no es hembra")
        
        # Verificar registros de celo DIRECTOS
        heat_check_query = text("""
            SELECT 
                he.id,
                he.cattle_id::text as cattle_id,
                he.heat_date
            FROM heat_events he
            WHERE he.cattle_id::text = :cattle_id
            ORDER BY he.heat_date DESC
        """)
        
        heat_result = self.db.execute(heat_check_query, {"cattle_id": cattle_id_str})
        heat_rows = heat_result.fetchall()
        
        if len(heat_rows) < 3:
            raise ValueError(f"Se necesitan al menos 3 registros de celo. Tiene: {len(heat_rows)}")
        
        # Obtener datos COMPLETOS para esta vaca específica
        specific_query = text("""
            SELECT 
                he.id,
                he.cattle_id::text as cattle_id,
                he.heat_date,
                he.allows_mounting,
                he.vaginal_discharge,
                he.vulva_swelling,
                he.comportamiento,
                he.was_inseminated,
                he.pregnancy_confirmed,
                c.birth_date,
                c.weight,
                c.fecha_ultimo_parto,
                c.breed
            FROM heat_events he
            JOIN cattle c ON he.cattle_id = c.id
            WHERE he.cattle_id::text = :cattle_id
            ORDER BY he.heat_date
        """)
        
        result = self.db.execute(specific_query, {"cattle_id": cattle_id_str})
        data = result.fetchall()
        
        if not data:
            raise ValueError(f"No se pudo obtener datos completos para {cattle_id}")
        
        df_cattle = pd.DataFrame(data, columns=[
            'id', 'cattle_id', 'heat_date', 'allows_mounting',
            'vaginal_discharge', 'vulva_swelling', 'comportamiento',
            'was_inseminated', 'pregnancy_confirmed', 'birth_date',
            'weight', 'fecha_ultimo_parto', 'breed'
        ])
        
        df_cattle['heat_date'] = pd.to_datetime(df_cattle['heat_date'])
        df_cattle['birth_date'] = pd.to_datetime(df_cattle['birth_date'])
        df_cattle['fecha_ultimo_parto'] = pd.to_datetime(df_cattle['fecha_ultimo_parto'])
        
        if len(df_cattle) < 3:
            raise ValueError(f"Registros procesados: {len(df_cattle)} (requiere mínimo 3)")
        
        # Crear features
        df_cattle = self._create_features(df_cattle)
        df_cattle = self._encode_features(df_cattle, fit=False)
        
        # Obtener último registro con features válidos
        df_cattle_valid = df_cattle[df_cattle['interval_lag1'].notna()].copy()
        
        if len(df_cattle_valid) == 0:
            raise ValueError("No hay registros con intervalos calculables")
        
        last_heat = df_cattle_valid.iloc[-1]
        
        # Preparar features
        X_pred = pd.DataFrame([last_heat[self.feature_columns]])
        X_pred = X_pred.fillna(0).astype(float)
        
        # Predicciones
        pred_rf = float(self.rf_model.predict(X_pred)[0])
        pred_xgb = float(self.xgb_model.predict(X_pred)[0])
        pred_avg = (pred_rf + pred_xgb) / 2
        
        # Calcular próxima fecha
        last_heat_date = last_heat['heat_date'].date()
        predicted_date = last_heat_date + timedelta(days=int(round(pred_avg)))
        days_until = (predicted_date - date.today()).days
        
        # Confianza
        diff = abs(pred_rf - pred_xgb)
        if diff < 2:
            confidence = "Alta"
        elif diff < 5:
            confidence = "Media"
        else:
            confidence = "Baja"
        
        return {
            "cattle_id": str(cattle_id),
            "last_heat_date": str(last_heat_date),
            "predicted_days_rf": round(pred_rf, 2),
            "predicted_days_xgb": round(pred_xgb, 2),
            "predicted_days_avg": round(pred_avg, 2),
            "predicted_next_heat_date": str(predicted_date),
            "days_until_heat": days_until,
            "total_heat_records": len(df_cattle),
            "model_confidence": confidence
        }