import asyncpg
from decouple import config

DATABASE_URL = f"postgresql://{config('POSTGRES_USER', default='demo_user')}:" \
               f"{config('POSTGRES_PASSWORD', default='demo_pass')}@" \
               f"{config('POSTGRES_HOST', default='localhost')}:" \
               f"{config('POSTGRES_PORT', default=5432)}/" \
               f"{config('POSTGRES_DB', default='demo_db')}"

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def disconnect(self):
        await self.pool.close()

    async def fetch_all(self, query: str):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)


db = Database()
