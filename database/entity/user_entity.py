from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    password: str
    lastname: str
    firstname: str
    createdAt: datetime
    updatedAt: datetime

    @classmethod
    async def create_user(cls, name: str, email: str, password: str, firstname: str, lastname: str, userEntity):
        hashed_password = bcrypt.hash(password)
        current_time = datetime.now()
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            'firstname': firstname,
            'lastname': lastname,
            "createdAt": current_time,
            "updatedAt": current_time
        }
        result = await userEntity.insert_one(user_data)
        user_id = str(result.inserted_id)
        return cls(id=user_id, name=name, email=email, password=hashed_password, firstname=firstname, lastname=lastname,createdAt=current_time, updatedAt=current_time)

    @staticmethod
    async def delete_user(user_id: str, userEntity):
        result = await userEntity.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @classmethod
    async def find_all_users(cls, userEntity):
        cursor = userEntity.find()
        users = []
        async for document in cursor:
            user_id = str(document["_id"])
            item = cls(
                id=user_id,
                name=document["name"],
                email=document["email"],
                firstname = document['firstname'],
                lastname = document['lastname'],
                password=document["password"],
                createdAt=document["createdAt"],
                updatedAt=document["updatedAt"]
            )
            users.append(item.dict())
        return users

    @classmethod
    async def find_one_user_by_id(cls, user_id: str, userEntity):
        document = await userEntity.find_one({"_id": ObjectId(user_id)})
        if not document:
            raise HTTPException(status_code=404, detail="User not found")
        return cls(
                id=user_id,
                name=document["name"],
                email=document["email"],
                firstname = document['firstname'],
                lastname = document['lastname'],
                password=document["password"],
                createdAt=document["createdAt"],
                updatedAt=document["updatedAt"]
            )

    @classmethod
    async def find_one_user_by_email(cls, user_email: str, userEntity):
        # Ensure this is awaited to work asynchronously
        return await userEntity.find_one({"email": user_email})

    @staticmethod
    async def update_user(user_id: str, name: str, email: str, userEntity):
        current_time = datetime.now()
        update_data = {"name": name, "email": email, "updatedAt": current_time}
        result = await userEntity.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return True

    @staticmethod
    async def create_indexes(db):
        await db["users"].create_index("id")
        await db["users"].create_index("email", unique=True)
