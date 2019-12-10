from datetime import datetime, timedelta
import pymongo
from bson.objectid import ObjectId
import os
import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.responses import Response

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "de372b58ab557051ca9e22c79d7e738dbac311b02872e9e03a9b7846c4c840aa"
ALGORITHM = "HS256"


mongo=os.environ['MONGO']
username=os.environ['MONGO_USER']
password=os.environ['MONGO_PASSWORD']


data_client = pymongo.MongoClient(mongo,
                                username=username,
                                password=password,
                                authSource='admin',
                                authMechanism='SCRAM-SHA-256')

database = data_client["appdata"]
logins_collection = database["users"]


class TokenData(BaseModel):
    sub: str = None
    exp: int


class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    gender: str
    age: int
    is_disabled: bool = None
    role: str = "user"
    sub: str
    exp: int



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

app = FastAPI(openapi_prefix="/api/translator")


def get_login_by_id(token):
    user_dict = logins_collection.find_one({"_id": ObjectId(token.sub)})
    user = User(**user_dict, id=str(user_dict["_id"]), sub=token.sub, exp=token.exp)
    return user

def create_access_token(*, data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        exp: int = payload.get("exp")
        if id is None:
            raise credentials_exception
        token_data = TokenData(sub=id, exp=exp)
    except PyJWTError:
        raise credentials_exception
    user = get_login_by_id(token_data)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/")
def test():
    return {"message": "success"}

@app.get("/translate")
def translate_access_token(response: Response, user: User = Depends(get_current_active_user)):
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data=user.dict())
    response.headers["x-token"] = "Bearer " + access_token.decode()
    # print(response.headers)
    return {"message": "success"}

