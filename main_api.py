# -------------------------
# 🚀 Import required modules
# -------------------------

from fastapi import FastAPI   # FastAPI framework to create APIs
from utils import load_tasks, save_tasks  # file handling functions
from services import add_task, delete_task  # business logic
from pydantic import BaseModel  # for request validation
from typing import List  # for response type hint


# -------------------------
# 🚀 Create FastAPI app
# -------------------------

app = FastAPI()
# 👉 This initializes your API server
# 👉 All endpoints will be attached to this "app"


# -------------------------
# 📦 Pydantic Models (Data Schema)
# -------------------------

class TaskCreate(BaseModel):
    title: str
    priority: str

    # 👉 Defines structure of incoming request body
    # 👉 Client MUST send:
    # {
    #   "title": "...",
    #   "priority": "..."
    # }


class TaskUpdate(BaseModel):
    title: str

    # 👉 Used when updating task
    # 👉 Only title is allowed to change


class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str

    # 👉 Defines how response should look
    # 👉 Helps FastAPI validate output
    # 👉 Also improves Swagger docs


# -------------------------
# 🌐 API ENDPOINTS
# -------------------------

# =========================
# 🟢 GET /tasks
# =========================

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    # 👉 This endpoint is used to FETCH all tasks

    # Step 1: Load data from JSON file
    tasks = load_tasks()

    # 👉 load_tasks():
    # reads file → converts JSON → Python list

    # Step 2: Return tasks
    return tasks

    # 👉 FastAPI automatically converts Python → JSON
    # 👉 response_model ensures correct structure


# =========================
# 🟢 POST /tasks
# =========================

@app.post("/tasks")
def create_task(task: TaskCreate):
    # 👉 This endpoint creates a NEW task

    # Step 1: Receive request body
    # Example:
    # {
    #   "title": "Learn FastAPI",
    #   "priority": "high"
    # }

    # 👉 FastAPI automatically:
    # - validates data
    # - converts JSON → Python object (task)

    # Step 2: Load existing tasks
    tasks = load_tasks()

    # Step 3: Add new task using business logic
    tasks = add_task(tasks, task.title, task.priority)

    # 👉 add_task():
    # - generates unique ID
    # - creates new dict
    # - appends to list

    # Step 4: Save updated tasks
    save_tasks(tasks)

    # 👉 save_tasks():
    # Python list → JSON → file

    # Step 5: Return response
    return {"message": "Task added successfully"}

    # 👉 This is sent back to client


# =========================
# 🟢 PUT /tasks/{task_id}
# =========================

@app.put("/tasks/{task_id}")
def update_task_api(task_id: int, task: TaskUpdate):
    # 👉 Updates existing task

    # task_id → comes from URL
    # task → comes from request body

    # Step 1: Load tasks
    tasks = load_tasks()

    # Step 2: Search for task
    for t in tasks:
        if t["id"] == task_id:

            # Step 3: Update value
            t["title"] = task.title

            # Step 4: Save changes
            save_tasks(tasks)

            return {"message": "Task updated successfully"}

    # Step 5: If not found
    return {"error": "Task not found"}

    # 👉 Important: handle edge case


# =========================
# 🔴 DELETE /tasks/{task_id}
# =========================

@app.delete("/tasks/{task_id}")
def delete_task_api(task_id: int):
    # 👉 Deletes a task

    # Step 1: Load tasks
    tasks = load_tasks()

    # Step 2: Remove task using logic
    new_tasks = delete_task(tasks, task_id)

    # 👉 delete_task():
    # filters list → removes matching id

    # Step 3: Check if deletion happened
    if len(new_tasks) == len(tasks):
        return {"error": "Task not found"}

    # Step 4: Save updated list
    save_tasks(new_tasks)

    # Step 5: Return response
    return {"message": "Task deleted successfully"}


@app.put("/tasks/{task_id}/complete")
def complete_task_api(task_id: int):
    # Marks a task as completed

    # Step 1: Load tasks
    tasks = load_tasks()

    # Step 2: Search for task
    for t in tasks:
        if t["id"] == task_id:

            # Step 3: Update status
            t["status"] = "completed"

            # Step 4: Save changes
            save_tasks(tasks)

            return {"message": "Task marked as completed"}

    # Step 5: If not found
    return {"error": "Task not found"}

@app.get("/tasks/completed")
def get_completed_tasks():

    tasks  = load_tasks()

    completed_tasks = []
    for task in tasks:
        if task["status"] == "completed":
            completed_tasks.append(task)

    return completed_tasks

@app.get("/tasks/search")
def search_tasks(query: str):
    tasks = load_tasks()

    matched_tasks = []
    for task in tasks:
        if query.lower() in task["title"].lower():
            matched_tasks.append(task)

    return matched_tasks

@app.get("/tasks/filter")
def filter_tasks(priority: str):
    tasks = load_tasks()

    filtered_tasks = []

    for task in tasks:
        if task.get("priority", "").lower() == priority.lower():
            filtered_tasks.append(task)

    return filtered_tasks