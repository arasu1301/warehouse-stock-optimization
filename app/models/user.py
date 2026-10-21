from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    role: str = "operator"
