from fastapi import APIRouter, Depends
from services.redis_cache import redis_cache
from services.db import db
from auth.jwt_bearer import JWTBearer

router = APIRouter()

@router.get("/products", dependencies=[Depends(JWTBearer())])
async def get_products():
    """
    Fetch all products. First, check Redis cache. If not found, query PostgreSQL and cache the result.
    """
    # Check if products are cached
    cached_products = await redis_cache.get("products")
    if cached_products:
        return {"source": "cache", "products": cached_products}

    # Fetch products from PostgreSQL
    query = "SELECT id, name, price FROM products"
    products = await db.fetch_all(query)

    # Convert Decimal objects to float for JSON serialization
    serialized_products = [
        {"id": product["id"], "name": product["name"], "price": float(product["price"])}
        for product in products
    ]

    # Cache the serialized products
    await redis_cache.set("products", serialized_products)
    return {"source": "database", "products": serialized_products}
