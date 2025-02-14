import os
from enum import Enum
from fastapi import Depends
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from config.globals import DB_URI, DB_NAME, MONGO_USERS_COLLECTION


class Collections(Enum):
    USERS = MONGO_USERS_COLLECTION


def init_db():
    mongo_client = AsyncIOMotorClient(DB_URI)
    db = mongo_client[DB_NAME]
    return db


def get_user_collection(db=Depends(init_db)):
    return db[Collections.USERS.value]
