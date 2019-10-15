from fastapi import FastAPI
import pymongo
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

app = FastAPI()


@app.get("/")
async def read_root():
    return {"status": "running"}


@app.get("/item")
async def read_item(item_id: int = None):
    if not item_id:
        return users.find_one()
    return users.find_one({"_id": item_id})