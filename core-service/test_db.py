# Crea un archivo test_db.py en la raíz de core-service
from src.infrastructure.database import engine

try:
    connection = engine.connect()
    print("✅ Conexión a base de datos exitosa")
    connection.close()
except Exception as e:
    print(f"❌ Error conectando a la base de datos: {e}")
