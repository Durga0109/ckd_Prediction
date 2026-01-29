"""
Configuration settings for the CKD Clinical System
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    app_name: str = "CKD Clinical System"
    app_version: str = "1.0.0"
    
    # Database
    database_url: str = "sqlite:///./ckd_clinical.db"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ML Models Path
    ml_models_path: str = "../"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()
