from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints.inventory import router as inventory_router
from app.core.database import engine, Base   # Import Base and engine
import asyncio

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Account & Product wise Stock Inventory API with Redis Cache",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    # Create all tables on startup (works for SQLite and later Azure SQL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"✅ {settings.PROJECT_NAME} started successfully in {settings.ENVIRONMENT} mode")
    print(f"📊 Database: {'SQLite (Local)' if 'sqlite' in settings.DATABASE_URL else 'Azure SQL'}")

@app.get("/")
async def root():
    return {
        "message": "Stock Inventory API is running",
        "environment": settings.ENVIRONMENT,
        "database": "SQLite" if "sqlite" in settings.DATABASE_URL else "Azure SQL"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)