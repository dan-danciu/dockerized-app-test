from fastapi import Depends, APIRouter, HTTPException
from models.models import BaseUser, User
from models.db import users_collection
import pymongo
from security import security
from typing import List

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(security.user)):
    return current_user

@router.get("/find", response_model=List[User])
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

@router.put("/add", responses={403: {"description": "Operation forbidden"},
                                401: {"description": "Not authenticated"}})
def add_item(user: BaseUser, current_user: User = Depends(security.admin)):
    try:
        response = users_collection.insert_one(user.dict())
        res = { "success": True, "_id": str(response.inserted_id) }
    except pymongo.errors.DuplicateKeyError:
        res = { "success": False, "error": "E-mail address already exists in database." }
    return res