from typing import Optional, List
from pydantic import EmailStr
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    # books: Optional[List[Book]] = None


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    
    # books: Optional[List[Book]] = None
    texts: Optional[List] = None


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    
    # books: Optional[List[Book]] = None
    texts: Optional[List] = None
    
    