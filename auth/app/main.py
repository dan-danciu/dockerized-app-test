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

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "de372b58ab557051ca9e22c79d7e738dbac311b02872e9e03a9b7846c4c840aa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


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
logins_collection.create_index([("username", pymongo.ASCENDING)], name="username_index", unique=True, partialFilterExpression = { "username": { "$exists": True }})


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None


class User(BaseModel):
    id: str
    username: str
    is_disabled: bool = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    print(pwd_context.hash(password))
    return pwd_context.hash(password)


def get_login_by_id(id: str):
    user_dict = logins_collection.find_one({"_id": ObjectId(id)})
    return UserInDB(**user_dict, id=str(user_dict["_id"]))

def get_login_by_username(username: str):
    user_dict = logins_collection.find_one({"username": username})
    return UserInDB(**user_dict, id=str(user_dict["_id"]))


def authenticate_user(username: str, password: str):
    user = get_login_by_username(username)
    print(get_password_hash(password))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
