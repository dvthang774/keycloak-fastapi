from database.entity.user_entity import User
from fastapi import HTTPException, status
from util.response_schema import success_response, error_response
from database.entity.user_entity import User
from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from auth.auth_config import keycloak_admin, keycloak_openid
from keycloak.exceptions import KeycloakAuthenticationError

async def register_controller(name: str, email: str, password: str, firstname:str, lastname: str, db):
    """
    Register new user controller
    """
    user = await User.find_one_user_by_email(email, db)
    if user:
        response = error_response("User with this email exist")
        print("user not found:", response)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=response)
    try:
        new_user = await User.create_user(name=name, email=email, password=password, firstname=firstname, lastname=lastname, userEntity=db)
        keycloak_admin.create_user({
            "email": f"{email}",
            "username": f"{name}",
            "enabled": True,
            "firstName": f"{firstname}",  # đổi "firstname" thành "firstName"
            "lastName": f"{lastname}",    # đổi "lastname" thành "lastName"
            "credentials": [{"value": password, "type": "password"}]  # Lưu mật khẩu là kiểu "password"
        })

        return success_response("User Registered", {
            "id": str(new_user.id),
            "username": new_user.name,
            "email": new_user.email,

        })
    except Exception as ex:
        print("exception under Register controller:", ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=error_response("Internal Server Error"))

# def authenticate_user(username: str, password: str) -> str:
#     """
#     Authenticate the user using Keycloak and return an access token.
#     """
#     try:
#         token = keycloak_openid.token(username, password)
#         return token["access_token"]
#     except KeycloakAuthenticationError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#         )

async def login_controller(email: str, password: str, db):
    """
    Login user controller
    """
    db_user = await User.find_one_user_by_email(email, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response(
            "User with this email does not exist"))
    try:
        isMatched = bcrypt.verify(password, db_user['password'])
        if not isMatched:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_response("Invalid password"))

        token = keycloak_openid.token(db_user['name'], password)
        return success_response("User Logged In", {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_in": token["expires_in"]
        })
    except Exception as e:
        print("exception under Login controller:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response(
            "Internal Server Error"), headers={"X-Error": str(e)})
