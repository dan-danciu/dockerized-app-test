from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import pymongo
import os
import jwt
from jwt import PyJWTError
from bson.objectid import ObjectId
from models.models import User, TokenData
from typing import List
from models.db import users_collection
from starlette.status import HTTP_401_UNAUTHORIZED

SECRET_KEY = "de372b58ab557051ca9e22c79d7e738dbac311b02872e9e03a9b7846c4c840aa"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_login_by_id(id: str):
    user_dict = users_collection.find_one({"_id": ObjectId(id)})
    return User(**user_dict, id=str(user_dict["_id"]))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except PyJWTError:
        raise credentials_exception
    user = get_login_by_id(id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class AccessRoles:
    def __init__(self, role_list: List[str]):
        self.roles = role_list
    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role in self.roles:
            return user
        if user.role == 'admin':
            return user
        raise HTTPException(status_code=403, detail="You are not authorised to perform this operation")

any_user = get_current_active_user
admin = AccessRoles(['admin'])
dev_admin = AccessRoles(['admin', 'dev'])