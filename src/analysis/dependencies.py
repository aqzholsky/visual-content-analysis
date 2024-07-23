from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.db.mongodb import get_database

DatabaseDependency = Annotated[AsyncIOMotorClient, Depends(get_database)]
