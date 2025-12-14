import random
import uuid
from datetime import datetime, timedelta, date
from faker import Faker
import pandas as pd

fake = Faker(['es_MX'])

# Configuración
NUM_CATTLE = 90
NUM_HEALTH_EVENTS = 400
USER_ID = str(uuid.uuid4())

# Razas comunes en México
BREEDS = [
    'Brahman', 'Charolais', 'Angus', 'Hereford', 'Simmental',
    'Beefmaster', 'Brangus', 'Gelbvieh', 'Limousin', 'Holstein'
]

# Nombres comunes para ganado
CATTLE_NAMES = [
    'Bella', 'Paloma', 'Estrella', 'Luna', 'Rosa',
    'Toro', 'Bravo', 'Rey', 'Duque', 'Príncipe',
    'Bonita', 'Negra', 'Blanca', 'Colorada', 'Manchada'
]

EVENT_TYPES = ['vaccine', 'treatment', 'checkup', 'surgery', 'injury', 'illness', 'other']
ADMIN_ROUTES = ['oral', 'intramuscular', 'subcutaneous', 'intravenous', 'topical', 'other']

# Enfermedades y medicinas comunes
DISEASES = [
    'Fiebre aftosa', 'Brucelosis', 'Tuberculosis', 'Rabia', 'Parasitosis',
    'Mastitis', 'Neumonía', 'Diarrea', 'Dermatitis', None
]

MEDICINES = [
    'Ivermectina', 'Penicilina', 'Oxitetraciclina', 'Levamisol',
    'Albendazol', 'Vitamina A', 'Complejo B', 'Antiparasitario', None
]

VETERINARIANS = [
    'Dr. García López', 'Dra. Martínez Silva', 'Dr. Rodríguez Pérez',
    'Dra. Hernández Ruiz', 'Dr. López González', None
]


def generate_cattle_data():
    """Generar datos sintéticos de ganado"""
    cattle_data = []
    
    for i in range(NUM_CATTLE):
        gender = random.choice(['male', 'female'])
        birth_date = fake.date_between(start_date='-8y', end_date='-6m')
        
        # Solo hembras tienen fecha_ultimo_parto
        fecha_ultimo_parto = None
        if gender == 'female' and random.random() > 0.3:
            # 70% de hembras tienen historial de parto
            min_parto_date = birth_date + timedelta(days=730)  # Mínimo 2 años después de nacer
            max_parto_date = date.today() - timedelta(days=60)  # Hace mínimo 60 días
            
            # Solo asignar si la vaca es lo suficientemente vieja
            if min_parto_date <= max_parto_date:
                fecha_ultimo_parto = fake.date_between(
                    start_date=min_parto_date,
                    end_date=max_parto_date
                )
        
        cattle = {
            'id': str(uuid.uuid4()),
            'owner_id': USER_ID,
            'name': random.choice(CATTLE_NAMES) + f' {i+1}',
            'lote': f'L{1000 + i}',
            'breed': random.choice(BREEDS),
            'gender': gender,
            'birth_date': birth_date,
            'weight': round(random.uniform(250, 650), 2) if random.random() > 0.1 else None,
            'fecha_ultimo_parto': fecha_ultimo_parto,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        cattle_data.append(cattle)
    
    return cattle_data


def generate_health_events(cattle_data):
    """Generar eventos de salud distribuidos"""
    health_events = []
    
    # Distribución: 30% sanos, 50% normales, 20% alta atención
    num_healthy = int(NUM_CATTLE * 0.30)
    num_normal = int(NUM_CATTLE * 0.50)
    num_high_care = NUM_CATTLE - num_healthy - num_normal
    
    cattle_distribution = (
        [(c, random.randint(0, 1)) for c in cattle_data[:num_healthy]] +
        [(c, random.randint(2, 5)) for c in cattle_data[num_healthy:num_healthy + num_normal]] +
        [(c, random.randint(6, 15)) for c in cattle_data[num_healthy + num_normal:]]
    )
    
    for cattle, num_events in cattle_distribution:
        for _ in range(num_events):
            # Tipo de evento con distribución realista
            event_type = random.choices(
                EVENT_TYPES,
                weights=[40, 30, 20, 3, 3, 3, 1],
                k=1
            )[0]
            
            # Fecha del evento
            application_date = fake.date_between(
                start_date=cattle['birth_date'] + timedelta(days=30),
                end_date='today'
            )
            
            # Campos opcionales según tipo
            disease_name = random.choice(DISEASES) if event_type in ['illness', 'treatment'] else None
            medicine_name = random.choice(MEDICINES) if event_type in ['vaccine', 'treatment'] else None
            administration_route = random.choice(ADMIN_ROUTES) if medicine_name else None
            
            # Próxima dosis solo para vacunas
            next_dose_date = None
            if event_type == 'vaccine' and random.random() > 0.4:
                next_dose_date = application_date + timedelta(days=random.randint(30, 180))
            
            # Fecha fin de tratamiento
            treatment_end_date = None
            if event_type == 'treatment' and random.random() > 0.5:
                treatment_end_date = application_date + timedelta(days=random.randint(7, 30))
            
            event = {
                'id': str(uuid.uuid4()),
                'cattle_id': cattle['id'],
                'event_type': event_type,
                'disease_name': disease_name,
                'medicine_name': medicine_name,
                'application_date': application_date,
                'administration_route': administration_route,
                'next_dose_date': next_dose_date,
                'treatment_end_date': treatment_end_date,
                'dosage': f'{random.randint(1, 10)} ml' if medicine_name else None,
                'veterinarian_name': random.choice(VETERINARIANS),
                'notes': fake.sentence() if random.random() > 0.7 else None,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            health_events.append(event)
    
    return health_events


def save_to_csv():
    """Generar y guardar datasets"""
    print("Generando datos de ganado...")
    cattle_data = generate_cattle_data()
    
    print("Generando eventos de salud...")
    health_events = generate_health_events(cattle_data)
    
    # Convertir a DataFrames
    df_cattle = pd.DataFrame(cattle_data)
    df_health = pd.DataFrame(health_events)
    
    # Guardar CSVs
    df_cattle.to_csv('synthetic_cattle.csv', index=False)
    df_health.to_csv('synthetic_health_events.csv', index=False)
    
    print(f"\n✅ Dataset generado:")
    print(f"   - {len(cattle_data)} registros de ganado")
    print(f"   - {len(health_events)} eventos de salud")
    print(f"   - USER_ID: {USER_ID}")
    print(f"\nArchivos creados:")
    print(f"   - synthetic_cattle.csv")
    print(f"   - synthetic_health_events.csv")
    
    # Estadísticas
    print(f"\nDistribución de eventos por animal:")
    events_per_cattle = df_health.groupby('cattle_id').size()
    print(f"   - Promedio: {events_per_cattle.mean():.2f}")
    print(f"   - Mínimo: {events_per_cattle.min()}")
    print(f"   - Máximo: {events_per_cattle.max()}")
    
    print(f"\nDistribución por tipo de evento:")
    print(df_health['event_type'].value_counts())


if __name__ == "__main__":
    save_to_csv()