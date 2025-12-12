from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/bovara_auth"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Bovara Auth Service"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Permitir que funcione sin .env
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Singleton de configuración"""
    return Settings()

def get_settings() -> Settings:
    """Singleton de configuración"""
    s = Settings()
    print(f"🔑 Auth JWT Secret Key: {s.SECRET_KEY}")  # DEBUG
    return s