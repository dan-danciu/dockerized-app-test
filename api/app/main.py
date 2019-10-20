from fastapi import FastAPI
import pymongo
from bson.objectid import ObjectId
from pydantic import BaseModel
import os

mongo=os.environ['MONGO']
username=os.environ['MONGO_USER']
password=os.environ['MONGO_PASSWORD']

data_client = pymongo.MongoClient(mongo,
                                username=username,
                                password=password,
                                authSource='admin',
                                authMechanism='SCRAM-SHA-256')

database = data_client["appdata"]
users = database["users"]
users.create_index([("email", pymongo.ASCENDING)], unique=True)

app = FastAPI(openapi_prefix="/api")

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    age: int


@app.get("/")
async def read_root():
    return {"status": "running"}


@app.get("/user")
async def read_item(user_id: str = None):
    print(user_id)
    if not user_id:
        res = users.find_one()
        res['_id'] = str(res['_id'])
        return res
    res = users.find_one({"_id": ObjectId(user_id)})
    res['_id'] = str(res['_id'])
    return res

@app.put("/user")
async def add_item(user: User):
    try:
        response = users.insert_one(user.dict())
        res = { "success": True, "_id": str(response.inserted_id) }
    except pymongo.errors.DuplicateKeyError as err:
        res = { "success": False, "error":err }
    return res

