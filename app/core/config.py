from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Environment
    ENVIRONMENT: str = "local"          # local, dev, stage, prod
    DEBUG: bool = True

    # Database - will use SQLite locally, Azure SQL in cloud
    DATABASE_URL: str = "sqlite+aiosqlite:///./stock_inventory.db"
    # For Azure SQL later: mssql+pyodbc://...

    # Redis - local Redis or fake for development
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600       # 1 hour

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Stock Inventory API"

    # File separator (your flat file)
    FILE_SEPARATOR: str = "|"

settings = Settings()