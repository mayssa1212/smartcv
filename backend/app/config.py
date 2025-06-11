import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Informations sur l'application
    APP_NAME: str = "SmartCV API"
    APP_DESCRIPTION: str = "API pour la gestion des CV intelligents"
    APP_VERSION: str = "0.1.0"
    
    # Configuration CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"]
    
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:121221@localhost:5432/smartcv")
    
    # Sécurité et authentification
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Clés API
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()



