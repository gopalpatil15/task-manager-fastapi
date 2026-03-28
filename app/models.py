from pydantic import BaseModel
from typing import List


class TaskCreate(BaseModel):
    title: str
    priority: str

    #  Defines structure of incoming request body
    #  Client MUST send:
    # {
    #   "title": "...",
    #   "priority": "..."
    # }


class TaskUpdate(BaseModel):
    title: str
    priority: str

    #  Used when updating task
    #  Only title is allowed to change


class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str

    # Defines how response should look
    # Helps FastAPI validate output
    # Also improves Swagger docs