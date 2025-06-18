from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Market Data Service"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    ALGORITHM: str = "HS256"
    
    ALPHA_VANTAGE_API_KEY: str = Field(..., env="ALPHA_VANTAGE_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        
class DevelopmentSettings(Settings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

class ProductionSettings(Settings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    WORKERS: int = 4
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30

class TestingSettings(Settings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"

def get_settings() -> Settings:
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()