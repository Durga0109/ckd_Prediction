"""
Configuration settings for the CKD Clinical System
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os

# Absolute path to project root (2 levels up from this file: backend/app/config.py -> root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


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
    
    # ML Models Path — absolute path to project root/trained_models where .pkl files live
    ml_models_path: str = os.path.join(PROJECT_ROOT, "trained_models")
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()
