from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
import pymongo
from bson.objectid import ObjectId
from pydantic import BaseModel
import os
import jwt
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

SECRET_KEY = "de372b58ab557051ca9e22c79d7e738dbac311b02872e9e03a9b7846c4c840aa"
ALGORITHM = "HS256"

mongo=os.environ['MONGO']
username=os.environ['MONGO_USER']
password=os.environ['MONGO_PASSWORD']
auth=os.environ['AUTH_SERVER']

data_client = pymongo.MongoClient(mongo,
                                username=username,
                                password=password,
                                authSource='admin',
                                authMechanism='SCRAM-SHA-256')

database = data_client["appdata"]
users_collection = database["users"]
users_collection.create_index([("email", pymongo.ASCENDING)], name="email_index", unique=True)
users_collection.create_index([("first_name", "text"), 
                                ("last_name", "text")])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=auth + "/token")

app = FastAPI(openapi_prefix="/api")


class TokenData(BaseModel):
    id: str = None

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    age: int

class User(BaseUser):
    id: str
    username: str
    is_disabled: bool = None
    role: str = "user"

class UserInDB(User):
    hashed_password: str

def get_login_by_id(id: str):
    user_dict = users_collection.find_one({"_id": ObjectId(id)})
    return UserInDB(**user_dict, id=str(user_dict["_id"]))

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


@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/findusers", response_model=List[User])
def finduser(search_string: str):
    users=[]
    #full text search based on text index is faster but it only matches full words
    #regex is slower but matches parts
    #ex: If you search dan, text search finds only people who are explicitly named Dan
    #but regex search finds all people that have dan wherever within their names or email
    #ft_query = {"$text": {"$search": search_string}}
    query = {"$or": [{ "first_name": { "$regex": search_string, "$options" :'i' }},
            { "last_name": { "$regex": search_string, "$options" :'i' }},
            { "email": { "$regex": search_string, "$options" :'i' }}]}
    cursor = users_collection.find(query)
    for doc in cursor:
        user = User(**doc, id = str(doc["_id"]))
        users.append(user)
    return users

@app.put("/user")
def add_item(user: BaseUser, current_user: User = Depends(get_current_active_user)):
    if not current_user.role == 'staff':
        raise HTTPException(status_code=400, detail="You are not authorised to perform this operation")
    try:
        response = users_collection.insert_one(user.dict())
        res = { "success": True, "_id": str(response.inserted_id) }
    except pymongo.errors.DuplicateKeyError:
        res = { "success": False, "error": "E-mail address already exists in database." }
    return res

