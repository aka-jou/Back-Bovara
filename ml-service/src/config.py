from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/bovara_core"
    model_path: str = "models/"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
