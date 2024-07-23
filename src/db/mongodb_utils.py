from motor.motor_asyncio import AsyncIOMotorClient

from src.config import MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT, MONGODB_URL

from .mongodb import db


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        str(MONGODB_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT,
    )


async def close_mongo_connection():
    db.client.close()
