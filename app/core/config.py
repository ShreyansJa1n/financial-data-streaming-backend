from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Market Data Service"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL", "ostgresql://blockhouse:blockhouse@localhost:5432/blockhouse_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ALGORITHM: str = "HS256"
    
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPICS: list[str] = ["price_events"]
    
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

    class Config:
        env_file = "/app/.env"
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