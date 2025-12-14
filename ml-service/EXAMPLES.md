# EJEMPLOS DE REQUEST Y RESPONSE PARA ML-SERVICE

## 1. ENTRENAR MODELO
POST http://localhost:8003/api/v1/clustering/train

Response:
{
  "total_cattle": 90,
  "clusters_created": 4,
  "cluster_distribution": {
    "0": 25,
    "1": 30,
    "2": 20,
    "3": 15
  },
  "message": "Modelo entrenado exitosamente"
}


## 2. PREDECIR CLUSTER DE UNA VACA (ejemplo con ID)
GET http://localhost:8003/api/v1/clustering/predict/12345678-1234-5678-1234-567812345678

Response:
{
  "cattle_id": "12345678-1234-5678-1234-567812345678",
  "name": "Bella 1",
  "lote": "L1000",
  "cluster_id": 1,
  "cluster_type": "Mantenimiento Regular",
  "health_stats": {
    "total_eventos": 4,
    "total_vacunas": 3,
    "total_tratamientos": 1,
    "total_enfermedades": 0
  }
}


## 3. OBTENER TODOS LOS CLUSTERS
GET http://localhost:8003/api/v1/clustering/all

Response:
{
  "total_cattle": 90,
  "cattle": [
    {
      "cattle_id": "12345678-1234-5678-1234-567812345678",
      "name": "Bella 1",
      "lote": "L1000",
      "cluster_id": 1,
      "cluster_type": "Mantenimiento Regular",
      "health_stats": {
        "total_eventos": 4,
        "total_vacunas": 3,
        "total_tratamientos": 1,
        "total_enfermedades": 0
      }
    },
    {
      "cattle_id": "87654321-4321-8765-4321-876543218765",
      "name": "Toro 2",
      "lote": "L1001",
      "cluster_id": 0,
      "cluster_type": "Ganado Sano",
      "health_stats": {
        "total_eventos": 1,
        "total_vacunas": 1,
        "total_tratamientos": 0,
        "total_enfermedades": 0
      }
    }
  ]
}


## TIPOS DE CLUSTER:
- "Ganado Sano": Pocos eventos (0-1)
- "Mantenimiento Regular": Vacunas regulares, pocos tratamientos
- "Alta Atención Médica": Muchas enfermedades o tratamientos
- "Ganado en Tratamiento": Tratamientos activos


## PARA PROBAR CON CURL:

# Entrenar modelo
curl -X POST http://localhost:8003/api/v1/clustering/train

# Predecir cluster (reemplaza el UUID con uno real de tu BD)
curl http://localhost:8003/api/v1/clustering/predict/12345678-1234-5678-1234-567812345678

# Obtener todos
curl http://localhost:8003/api/v1/clustering/all


## PARA EJECUTAR EL SERVICIO:
cd ml-service
pip install -r requirements.txt
python main.py

# Servicio corriendo en: http://localhost:8003
# Docs en: http://localhost:8003/docs
