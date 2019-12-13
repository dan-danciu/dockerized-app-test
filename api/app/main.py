from fastapi import Depends, FastAPI, HTTPException, Header
import pymongo
from models.db import users_collection
from routers import users


app = FastAPI(openapi_prefix="/api",
            title="Supernice app",
            version="0.1.5")

@app.on_event("startup")
async def startup_event():
    users_collection.create_index(
        [("email", pymongo.ASCENDING)], 
        name="email_index", 
        unique=True)
    users_collection.create_index(
        [("first_name", "text"), 
        ("last_name", "text")])
    users_collection.create_index(
        [("username", pymongo.ASCENDING)], 
        name="username_index", 
        unique=True, 
        partialFilterExpression = { "username": { "$exists": True }})

@app.get("/")
def read_root():
    return {"status": "running"}


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
    )

