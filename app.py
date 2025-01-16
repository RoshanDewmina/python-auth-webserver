from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.user import router as UserRouter
from routes.products import router as ProductRouter
from services.redis_cache import redis_cache
from services.db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Redis and the database
    await redis_cache.connect()
    await db.connect()
    yield
    # Shutdown: Close connections
    await redis_cache.close()
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(ProductRouter, prefix="/api", tags=["Products"])

@app.get("/")
def root():
    return {"message": "Welcome to the demo app with PostgreSQL and Redis!"}
