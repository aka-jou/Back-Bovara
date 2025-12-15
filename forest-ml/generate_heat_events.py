import random
import uuid
from datetime import datetime, timedelta, date
import pandas as pd

# IDs de vacas proporcionados
CATTLE_IDS = [
    "508570c8-a218-4761-9402-bba87740b874",
    "67bbce36-2be7-40e8-b67d-99a33081b348",
    "38e96986-1713-4692-8a2d-9ba71af46f39",
    "74996de8-8432-43f9-96f1-28408dc0f8f4",
    "c4356576-30bd-4936-bc43-4baf2b98de07",
    "a297b7d3-6cea-4ed4-b2e6-fc1e2dd90f4a",
    "2de0f685-50b0-4bd9-a946-d94472e2cd73",
    "796fd4ce-26a5-432b-abe1-b1e4376fc176",
    "e6e43f01-b420-417f-ac24-38c80a61c8ca",
    "08ed8a86-49ae-4f9d-9a8a-5247a50b4f0b",
    "a0babefa-4124-41bc-a5bf-9cf851c7dcbd",
    "43455f44-0470-4aa1-aef6-e3f7125ce09a",
    "80683f50-08e3-4bd4-9040-2e0518c3577e",
    "dc2afacc-e835-450e-92fc-5b3076959215",
    "bcda213b-c99d-4b70-8ead-25b4e94e545d",
    "094911fa-57d6-44d8-8b4f-583fd8a4fab8",
    "b26f2af0-96bc-4444-acac-dd8bbd230740",
    "23261ffb-ece8-4af9-95ec-7e43ea6a964a",
    "d6fde476-0dda-477c-8fa0-a0a6ee7fdf3f",
    "1914a8e7-90ae-4f6d-a281-0056bb7e207d",
    "0ee61ad6-c79c-4b6f-ab63-2739b6609a52",
    "e36acfdc-e6c2-46e1-8ab5-576b8308808d",
    "3420384d-9061-4c27-aa52-57c917f745b4",
    "47b6f7b6-bb34-43dd-9547-fe30da858da1",
    "c29c51d0-1a28-48c5-be04-9a19caf32a55",
    "973ecddc-f079-4ef4-8748-0ade370c7713",
    "0dae6431-8455-4b19-a3bd-6b99dc74b33b",
    "1b46effb-ee18-43ad-b175-76198e72deaa",
    "bbe2bf41-cc47-47a3-a20a-7dec7e7faf49",
    "22f18598-8f34-497d-8684-fafe93e51a63",
    "61398590-503b-4ba8-8676-8d820e46b250",
    "0dc501f5-031c-40c7-87c7-339d2da0bbbc",
    "e603d647-fbfe-48bf-a32f-134eed33d246",
    "105089fa-bc47-45a1-ab27-adfede1e03d4",
    "410ca15f-226f-4afb-87a7-3facf79c1a1a",
    "2027cfc1-eb50-4ffa-ad00-7cbe24e21c4b",
    "690b7988-0b89-49f4-98b0-0162a1941ca3",
    "01c1749f-6efc-40a8-925d-4bee5edcb869",
    "701a4e9f-103d-48e6-9d62-551d412363d2",
    "eaf2ea62-b77e-4b9b-9203-8b26aecef2f4",
    "d0944a74-88f3-4bcd-962c-60f5615402d2",
    "96f4cea7-fe7c-414e-9187-4c051d362b49",
    "885ede42-8c99-4714-838e-d08b90fb331e",
    "53cf079b-afc7-44c2-ae57-4bab253b2db0",
    "28b9a9be-fc58-406b-9691-75d4f1fc9ef0",
    "014a4a38-0732-407c-9d89-b228ae5a9cc7",
    "a2f820cb-a2d8-4ab0-b001-33c2e3a4dd23",
    "7ecd7799-15f9-47e9-a2bc-10f7733909bd",
    "ccdeba6e-9d93-421e-baf0-853bbd2aff89",
    "f355f251-4c90-489c-b6d2-469e9d8d08e5"
]

# Enums
VAGINAL_DISCHARGE = ['seco', 'turbio', 'cristalino']
VULVA_SWELLING = ['normal', 'leve', 'alta']
COMPORTAMIENTO = ['mugido', 'nerviosismo', 'monta_a_otras', 'inquietud', 'olfatea', 'lame_genitales']


def generate_heat_events():
    """Generar eventos de celo sintéticos hasta la fecha objetivo"""
    heat_events = []
    
    # Fecha límite exacta solicitada
    TARGET_DATE = date(2025, 12, 14)
    
    # Solo usar las primeras 30 vacas (hembras)
    female_cattle = CATTLE_IDS[:30]
    
    for cattle_id in female_cattle:
        # Fecha inicial (entre 6-12 meses atrás desde la fecha objetivo)
        days_ago = random.randint(180, 365)
        start_date = TARGET_DATE - timedelta(days=days_ago)
        
        # Ciclo base (19-23 días, promedio 21)
        base_cycle = random.randint(19, 23)
        
        current_date = start_date
        
        # Bucle basado en FECHA, no en cantidad fija de eventos
        while current_date <= TARGET_DATE:
            
            # Decidir si fue inseminada (30% de probabilidad)
            was_inseminated = random.random() < 0.3
            insemination_date = current_date if was_inseminated else None
            
            # Si fue inseminada, decidir si confirmó preñez (70% éxito)
            pregnancy_confirmed = None
            if was_inseminated:
                pregnancy_confirmed = random.random() < 0.7
            
            # Generar síntomas
            allows_mounting = random.choice([True, False])
            vaginal_discharge = random.choice(VAGINAL_DISCHARGE)
            vulva_swelling = random.choice(VULVA_SWELLING)
            comportamiento = random.choice(COMPORTAMIENTO)
            
            event = {
                'id': str(uuid.uuid4()),
                'cattle_id': cattle_id,
                'heat_date': current_date,
                'allows_mounting': allows_mounting,
                'vaginal_discharge': vaginal_discharge,
                'vulva_swelling': vulva_swelling,
                'comportamiento': comportamiento,
                'was_inseminated': was_inseminated,
                'insemination_date': insemination_date,
                'pregnancy_confirmed': pregnancy_confirmed,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            heat_events.append(event)
            
            # Calcular siguiente fecha: Ciclo base + variación (±2 días)
            cycle_variation = random.randint(-2, 2)
            current_date = current_date + timedelta(days=base_cycle + cycle_variation)
    
    return heat_events



def save_to_csv():
    """Generar y guardar CSV"""
    print("Generando eventos de celo...")
    
    heat_events = generate_heat_events()
    
    df = pd.DataFrame(heat_events)
    
    # Guardar CSV
    df.to_csv('synthetic_heat_events.csv', index=False)
    
    print(f"\n✅ CSV generado:")
    print(f"   - {len(heat_events)} eventos de celo")
    print(f"   - Para {len(set([e['cattle_id'] for e in heat_events]))} vacas")
    print(f"\nArchivo: synthetic_heat_events.csv")
    
    # Estadísticas
    print(f"\nDistribución de eventos por vaca:")
    events_per_cattle = df.groupby('cattle_id').size()
    print(f"   - Promedio: {events_per_cattle.mean():.1f}")
    print(f"   - Mínimo: {events_per_cattle.min()}")
    print(f"   - Máximo: {events_per_cattle.max()}")
    
    print(f"\nInseminaciones: {df['was_inseminated'].sum()}")
    print(f"Preñeces confirmadas: {df['pregnancy_confirmed'].sum()}")


if __name__ == "__main__":
    save_to_csv()
