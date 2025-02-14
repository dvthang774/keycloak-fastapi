from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from database.entity.user_entity import User
from database.collections import init_db
from middlewares.error_exception import custom_exception_handler

from routes.user import user as userRouter
from routes.auth import auth as authRouter
from routes.service1 import service1 as service1Router
from routes.service2 import service2 as service2Router
from util.response_schema import success_response

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
   return custom_exception_handler(request, exc)


# startup event
@app.on_event("startup")
async def startup_event():
    db = init_db()
    await User.create_indexes(db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
deployedTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.get('/')
async def index():
    return success_response("Welcome to FastAPI", {
        "deployedTime": deployedTime
    })

app.include_router(authRouter, tags=['auth'], prefix='/api/v1/auth')
app.include_router(userRouter, tags=['user'], prefix='/api/v1/users')
app.include_router(service1Router, tags=['service1'], prefix='/api/v1/service1')
app.include_router(service2Router, tags=['service2'], prefix='/api/v1/service2')
