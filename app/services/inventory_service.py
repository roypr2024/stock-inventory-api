import json
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryResponse, InventoryListResponse
from app.core.redis import get_redis
from app.core.config import settings

class InventoryService:

    @staticmethod
    async def get_cache_key(account_id: str, product_code: Optional[str] = None):
        if product_code:
            return f"inventory:{account_id}:{product_code}"
        return f"inventory:{account_id}:all"

    @staticmethod
    async def get_stock(
        db: AsyncSession,
        account_id: str,
        product_code: Optional[str] = None
    ) -> InventoryListResponse:
        
        cache_key = InventoryService.get_cache_key(account_id, product_code)
        redis = await get_redis()

        # Try cache first
        try:
            cached = await redis.get(cache_key)
            if cached:
                data = json.loads(cached)
                return InventoryListResponse(**data)
        except:
            pass  # Redis not available → continue to DB (important for local)

        # Query database
        if product_code:
            stmt = select(Inventory).where(
                and_(Inventory.account_id == account_id, 
                     Inventory.product_code == product_code)
            )
        else:
            stmt = select(Inventory).where(Inventory.account_id == account_id)

        result = await db.execute(stmt)
        records = result.scalars().all()

        response = InventoryListResponse(
            total=len(records),
            records=[InventoryResponse.model_validate(r) for r in records]
        )

        # Store in cache
        try:
            await redis.set(
                cache_key, 
                json.dumps(response.model_dump()), 
                ex=settings.CACHE_TTL_SECONDS
            )
        except:
            pass  # Redis optional in local dev

        return response

    @staticmethod
    async def clear_cache(account_id: Optional[str] = None):
        """Clear cache after flat file load (called from Azure Function later)"""
        try:
            redis = await get_redis()
            if account_id:
                await redis.delete(f"inventory:{account_id}:all")
            else:
                # Pattern delete not straightforward in redis-py, so we can skip or implement later
                pass
        except:
            pass