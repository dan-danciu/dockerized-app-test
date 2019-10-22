from fastapi import FastAPI
from typing import List
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
users_collection = database["users"]
users_collection.create_index([("email", pymongo.ASCENDING)], name="email_index", unique=True)
users_collection.create_index([("first_name", "text"), 
                                ("last_name", "text")])

app = FastAPI(openapi_prefix="/api")

class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    gender: str
    age: int


@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/user/{user_id}", response_model=User)
def read_item(user_id: str):
    res = users_collection.find_one({"_id": ObjectId(user_id)})
    return User(**res, id=str(res["_id"]))

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
def add_item(user: User):
    try:
        response = users_collection.insert_one(user.dict())
        res = { "success": True, "_id": str(response.inserted_id) }
    except pymongo.errors.DuplicateKeyError:
        res = { "success": False, "error": "E-mail address already exists in database." }
    return res

