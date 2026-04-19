import json
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryResponse, InventoryListResponse
from app.core.redis import get_redis
from app.core.config import settings

class InventoryService:

    @staticmethod
    def get_cache_key(account_id: str, product_code: Optional[str] = None):
        if product_code:
            return f"inventory:{account_id}:{product_code}"
        return f"inventory:{account_id}:all"

    @staticmethod
    def get_stock(
        db: Session,
        account_id: str,
        product_code: Optional[str] = None
    ) -> InventoryListResponse:
        
        cache_key = InventoryService.get_cache_key(account_id, product_code)
        redis = None

        # Try Redis cache first
        try:
            redis = get_redis()   # Note: get_redis is sync now? Wait, we'll fix this later
            cached = redis.get(cache_key)
            if cached:
                data = json.loads(cached)
                return InventoryListResponse(**data)
        except:
            pass  # Redis not available or error → continue to DB

        # Query database (synchronous)
        if product_code:
            stmt = select(Inventory).where(
                and_(Inventory.account_id == account_id, 
                     Inventory.product_code == product_code)
            )
        else:
            stmt = select(Inventory).where(Inventory.account_id == account_id)

        result = db.execute(stmt)
        records = result.scalars().all()

        response = InventoryListResponse(
            total=len(records),
            records=[InventoryResponse.model_validate(r) for r in records]
        )

        # Store in cache
        try:
            if redis:
                redis.set(cache_key, json.dumps(response.model_dump()), ex=settings.CACHE_TTL_SECONDS)
        except:
            pass

        return response