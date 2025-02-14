from fastapi import APIRouter, Depends
from database.collections import get_user_collection, init_db
from models.auth_model import UserLoginSchema, UserRegisterSchema, UserRegisterResponseSchema
from controllers.auth_controller.auth_controller import register_controller, login_controller

auth = APIRouter()


@auth.post('/register', response_model=UserRegisterResponseSchema)
async def register(user: UserRegisterSchema, userEntity=Depends(get_user_collection)):
    return await register_controller(user.username, user.email, user.password, user.firstname, user.lastname, userEntity)


@auth.post('/login')
async def login(user: UserLoginSchema, userEntity=Depends(get_user_collection)):
    return await login_controller(user.email, user.password, userEntity)
