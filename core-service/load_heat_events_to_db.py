import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from datetime import datetime
from uuid import UUID
from sqlalchemy import text

from src.infrastructure.database import SessionLocal


def load_heat_events_from_csv(csv_path: str):
    """Cargar eventos de celo desde CSV a la base de datos"""
    print(f"Cargando heat events desde {csv_path}...")
    
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    
    try:
        count = 0
        for _, row in df.iterrows():
            # Preparar valores
            heat_date = pd.to_datetime(row['heat_date']).date()
            allows_mounting = bool(row['allows_mounting']) if pd.notna(row['allows_mounting']) else None
            vaginal_discharge = row['vaginal_discharge'] if pd.notna(row['vaginal_discharge']) else None
            vulva_swelling = row['vulva_swelling'] if pd.notna(row['vulva_swelling']) else None
            comportamiento = row['comportamiento'] if pd.notna(row['comportamiento']) else None
            was_inseminated = bool(row['was_inseminated']) if pd.notna(row['was_inseminated']) else False
            insemination_date = pd.to_datetime(row['insemination_date']).date() if pd.notna(row['insemination_date']) else None
            pregnancy_confirmed = bool(row['pregnancy_confirmed']) if pd.notna(row['pregnancy_confirmed']) else None
            
            # Insert SQL
            query = text("""
                INSERT INTO heat_events (
                    id, cattle_id, heat_date, allows_mounting,
                    vaginal_discharge, vulva_swelling, comportamiento,
                    was_inseminated, insemination_date, pregnancy_confirmed,
                    created_at, updated_at
                ) VALUES (
                    :id, :cattle_id, :heat_date, :allows_mounting,
                    :vaginal_discharge, :vulva_swelling, :comportamiento,
                    :was_inseminated, :insemination_date, :pregnancy_confirmed,
                    :created_at, :updated_at
                )
            """)
            
            db.execute(query, {
                'id': row['id'],
                'cattle_id': row['cattle_id'],
                'heat_date': heat_date,
                'allows_mounting': allows_mounting,
                'vaginal_discharge': vaginal_discharge,
                'vulva_swelling': vulva_swelling,
                'comportamiento': comportamiento,
                'was_inseminated': was_inseminated,
                'insemination_date': insemination_date,
                'pregnancy_confirmed': pregnancy_confirmed,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
            
            count += 1
        
        db.commit()
        print(f"✅ {count} eventos de celo insertados")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


def main():
    """Cargar datos sintéticos de heat events"""
    print("🚀 Iniciando carga de heat events...")
    print("=" * 50)
    
    csv_file = "synthetic_heat_events.csv"
    
    if not Path(csv_file).exists():
        print(f"❌ No se encuentra {csv_file}")
        print(f"   Primero ejecuta: python generate_heat_events.py")
        return
    
    try:
        load_heat_events_from_csv(csv_file)
        print("=" * 50)
        print("✅ Carga completa exitosa")
        
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")


if __name__ == "__main__":
    main()
