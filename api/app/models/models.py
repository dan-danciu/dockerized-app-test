from pydantic import BaseModel

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
    username: str = None
    is_disabled: bool = True
    role: str = "user"