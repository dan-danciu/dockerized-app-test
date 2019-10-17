from fastapi import FastAPI
import pymongo
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
async def read_item(user_id: int = None):
    if not user_id:
        return users.find_one()
    return users.find_one({"_id": user_id})

@app.put("/user")
async def add_item(user: User):
    res = users.insert_one(user.dict())
    return {"_id": str(res.inserted_id), "user_data": user.json()}