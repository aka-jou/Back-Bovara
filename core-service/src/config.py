from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/bovara_core"
    auth_service_url: str = "http://localhost:8000"
    jwt_secret_key: str = "tu-clave-secreta-super-segura-cambiar-en-produccion-123456"
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
print(f"🔑 JWT Secret Key cargada: {settings.jwt_secret_key}")
