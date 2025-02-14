from typing import List
from pydantic import BaseModel, EmailStr

class user_response_body(BaseModel):
    id: str 
    name: str 
    email: EmailStr 
    password: str


class get_all_user_response_schema(BaseModel):
    success: bool
    message: str
    data: List[user_response_body]