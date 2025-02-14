from fastapi import APIRouter, Depends
# from auth.authBearer import JWTBearer
from database.collections import get_user_collection, init_db
from models.user_model import get_all_user_response_schema
from database.entity.user_entity import User
from util.response_schema import success_response

user = APIRouter()


@user.get('/', response_model=get_all_user_response_schema)
async def find_all_users(userEntity=Depends(get_user_collection)):
    # print("current_user:", current_user)
    data = await User.find_all_users(userEntity)
    return success_response("All Users " + str(len(data)), data)
