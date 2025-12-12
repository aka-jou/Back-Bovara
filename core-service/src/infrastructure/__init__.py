# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://bovara_user:bovara_password@localhost:5433/bovara_core"
    auth_service_url: str = "http://localhost:8000"
    jwt_secret_key: str = "dev-secret-key-CHANGE-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
