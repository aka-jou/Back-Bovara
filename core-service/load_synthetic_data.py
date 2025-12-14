import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from datetime import datetime
from uuid import UUID

from src.infrastructure.database import SessionLocal
from src.infrastructure.models.cattle import Cattle
from src.infrastructure.models.health_event import HealthEvent


def load_cattle_data(csv_path: str):
    """Cargar datos de ganado desde CSV"""
    print(f"Cargando ganado desde {csv_path}...")
    
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    
    try:
        count = 0
        for _, row in df.iterrows():
            cattle = Cattle(
                id=UUID(row['id']),
                owner_id=UUID(row['owner_id']),
                name=row['name'],
                lote=row['lote'],
                breed=row['breed'] if pd.notna(row['breed']) else None,
                gender=row['gender'],
                birth_date=pd.to_datetime(row['birth_date']).date() if pd.notna(row['birth_date']) else None,
                weight=float(row['weight']) if pd.notna(row['weight']) else None,
                fecha_ultimo_parto=pd.to_datetime(row['fecha_ultimo_parto']).date() if pd.notna(row['fecha_ultimo_parto']) else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(cattle)
            count += 1
        
        db.commit()
        print(f"✅ {count} registros de ganado insertados")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


def load_health_events_data(csv_path: str):
    """Cargar eventos de salud desde CSV"""
    print(f"Cargando eventos de salud desde {csv_path}...")
    
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    
    try:
        count = 0
        for _, row in df.iterrows():
            event = HealthEvent(
                id=UUID(row['id']),
                cattle_id=UUID(row['cattle_id']),
                event_type=row['event_type'],
                disease_name=row['disease_name'] if pd.notna(row['disease_name']) else None,
                medicine_name=row['medicine_name'] if pd.notna(row['medicine_name']) else None,
                application_date=pd.to_datetime(row['application_date']).date(),
                administration_route=row['administration_route'] if pd.notna(row['administration_route']) else None,
                next_dose_date=pd.to_datetime(row['next_dose_date']).date() if pd.notna(row['next_dose_date']) else None,
                treatment_end_date=pd.to_datetime(row['treatment_end_date']).date() if pd.notna(row['treatment_end_date']) else None,
                dosage=row['dosage'] if pd.notna(row['dosage']) else None,
                veterinarian_name=row['veterinarian_name'] if pd.notna(row['veterinarian_name']) else None,
                notes=row['notes'] if pd.notna(row['notes']) else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(event)
            count += 1
        
        db.commit()
        print(f"✅ {count} eventos de salud insertados")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


def main():
    """Cargar todos los datos sintéticos"""
    print("🚀 Iniciando carga de datos sintéticos...")
    print("=" * 50)
    
    # Rutas de los archivos CSV
    cattle_csv = "synthetic_cattle.csv"
    health_events_csv = "synthetic_health_events.csv"
    
    # Verificar que existen los archivos
    if not Path(cattle_csv).exists():
        print(f"❌ No se encuentra {cattle_csv}")
        return
    
    if not Path(health_events_csv).exists():
        print(f"❌ No se encuentra {health_events_csv}")
        return
    
    try:
        # Cargar datos
        load_cattle_data(cattle_csv)
        load_health_events_data(health_events_csv)
        
        print("=" * 50)
        print("✅ Carga completa exitosa")
        
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")


if __name__ == "__main__":
    main()
