from fastapi import APIRouter, Depends, HTTPException
# from database.collections import get_user_collection, init_db
# from models.auth_model import UserLoginSchema, UserRegisterSchema, UserRegisterResponseSchema
from controllers.auth_controller.auth_controller import register_controller, login_controller
from auth.auth_config import keycloak_openid
from fastapi.security import OAuth2PasswordBearer

service1 = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Hàm giải mã token và lấy thông tin người dùng
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Giải mã token và lấy thông tin người dùng
        user_info = keycloak_openid.decode_token(token)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Kiểm tra quyền truy cập cho Service 1
@service1.get("/read")
async def read_service1(user_info: dict = Depends(get_current_user)):
    # Kiểm tra các roles từ token
    client_roles = user_info.get("resource_access", {}).get("service1-client", {}).get("roles", [])
    print('service1-read:',client_roles)
    if "service1-read" in client_roles:
        return {"message": "Access granted to read Service 1"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: No read access")

@service1.post("/create")
async def create_service1(user_info: dict = Depends(get_current_user)):
    # Kiểm tra các roles từ token
    client_roles = user_info.get("resource_access", {}).get("service1-client", {}).get("roles", [])

    if "service1-create" in client_roles:
        return {"message": "Access granted to create Service 1"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: No create access")

@service1.put("/update")
async def update_service1(user_info: dict = Depends(get_current_user)):
    # Kiểm tra các roles từ token
    client_roles = user_info.get("resource_access", {}).get("service1-client", {}).get("roles", [])

    if "service1-update" in client_roles:
        return {"message": "Access granted to update Service 1"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: No update access")

@service1.delete("/delete")
async def delete_service1(user_info: dict = Depends(get_current_user)):
    # Kiểm tra các roles từ token
    client_roles = user_info.get("resource_access", {}).get("service1-client", {}).get("roles", [])

    if "service1-delete" in client_roles:
        return {"message": "Access granted to delete Service 1"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: No delete access")
