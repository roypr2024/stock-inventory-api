from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    PROJECT_NAME: str = "Stock Inventory API"

    # Database
    #DATABASE_URL: str = "sqlite+aiosqlite:///./stock_inventory.db"
    DATABASE_URL: str = "mssql+pyodbc://sqladmin:Admin@1234!@sql-stock-inv.database.windows.net/stockinventorydb?driver=ODBC+Driver+18+for+SQL+Server"
    # For Azure SQL later: "mssql+pyodbc://sqladmin:Password@server.database.windows.net/db?driver=ODBC+Driver+18+for+SQL+Server"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 7200   # 2 hours (since file updates every 3-4 hrs)

    # API
    API_V1_STR: str = "/api/v1"
    FILE_SEPARATOR: str = "|"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()