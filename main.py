from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints.inventory import router as inventory_router
from app.core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{settings.PROJECT_NAME} starting in {settings.ENVIRONMENT} mode")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created/verified successfully")
    except Exception as e:
        print(f"Database warning (continuing): {str(e)[:200]}")
    yield
    print("Application shutting down...")

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Stock Inventory API is running", "env": settings.ENVIRONMENT}