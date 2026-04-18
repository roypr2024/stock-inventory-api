from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import inventory
import asyncio

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Account-wise & Product-wise Stock Inventory API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS (allow calls from other applications)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inventory.router, prefix=settings.API_V1_STR)

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Stock Inventory API is running!", "environment": settings.ENVIRONMENT}

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("Application starting...")

# Note: Redis connection is lazy-initialized in get_redis(), so we don't need to do anything here for Redis.
@app.on_event("shutdown")
async def shutdown_event():
    from app.core.redis import close_redis
    await close_redis()
    print("Application shutting down...")