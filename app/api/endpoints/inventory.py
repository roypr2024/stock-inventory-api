from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.redis import get_redis

router = APIRouter(tags=["Inventory"])

# Health check endpoint to verify API is running and can connect to DB and Redis
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "sqlite (local)",
        "message": "API is ready for development"
    }

# Test endpoint to verify Redis connection (optional, can be removed later)
@router.get("/cache-test")
async def cache_test():
    redis = await get_redis()
    try:
        await redis.set("test_key", "Hello from Redis!", ex=60)
        value = await redis.get("test_key")
        return {"cache_status": "working", "value": value}
    except Exception as e:
        return {"cache_status": "not connected (OK for local dev)", "error": str(e)}