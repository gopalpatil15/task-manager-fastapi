from pydantic import BaseModel
from typing import List, Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str

    #  Defines structure of incoming request body
    #  Client MUST send:
    # {
    #   "title": "...",
    #   "priority": "..."
    # }


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str

    #  Used when updating task
    #  Only title is allowed to change


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str

    # Defines how response should look
    # Helps FastAPI validate output
    # Also improves Swagger docs


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    current_user: dict 
    description: Optional[str] = None