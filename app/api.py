from fastapi import FastAPI, Response, APIRouter, Depends, HTTPException, status
from app.models import TaskCreate, TaskUpdate, TaskResponse, UserCreate, UserLogin, Token
from app.utils import load_tasks, save_tasks
from app.services import add_task, delete_task
from app.db import get_connection, fetch_task, update_task
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    # For simplicity, hardcoded. In production, check DB.
    if username == "admin" and password == "password":
        return {"username": username}
    return False

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return username

# Create router for API endpoints
router = APIRouter()

# Auth endpoints
@router.post("/register", response_model=Token)
def register(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    # TODO: Save user to DB
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    user_auth = authenticate_user(user.username, user.password)
    if not user_auth:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# =========================
# GET /tasks
# =========================

@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(current_user: str = Depends(get_current_user)):
    # This endpoint is used to FETCH all tasks

    # Step 1: Load data from JSON file
    tasks = load_tasks()

    # load_tasks():
    # reads file → converts JSON → Python list

    # Step 2: Return tasks
    return tasks

    # FastAPI automatically converts Python → JSON
    # response_model ensures correct structure


# =========================
# POST /tasks
# =========================

@router.post("/tasks")
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    #  This endpoint creates a NEW task

    # Step 1: Receive request body
    # Example:
    # {
    #   "title": "Learn FastAPI",
    #   "priority": "high"
    # }

    # FastAPI automatically:
    # - validates data
    # - converts JSON → Python object (task)

    # Step 2: Load existing tasks
    tasks = load_tasks()

    # Step 3: Add new task using business logic
    tasks = add_task(tasks, task.title, task.priority)

    #   add_task():
    # - generates unique ID
    # - creates new dict
    # - appends to list

    # Step 4: Save updated tasks
    save_tasks(tasks)

    # save_tasks():
    # Python list → JSON → file

    # Step 5: Return response
    return {"message": "Task added successfully"}

    # This is sent back to client


# =========================
#  PUT /tasks/{task_id}
# =========================

@router.put("/tasks/{task_id}")
def update_task_api(task_id: int, task: TaskUpdate, current_user: str = Depends(get_current_user)):
    #  Updates existing task

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

    # Important: handle edge case


# =========================
# DELETE /tasks/{task_id}
# =========================

@router.delete("/tasks/{task_id}")
def delete_task_api(task_id: int):
    #  Deletes a task

    # Step 1: Load tasks
    tasks = load_tasks()

    # Step 2: Remove task using logic
    new_tasks = delete_task(tasks, task_id)

    # delete_task():
    # filters list → removes matching id

    # Step 3: Check if deletion happened
    if len(new_tasks) == len(tasks):
        return {"error": "Task not found"}

    # Step 4: Save updated list
    save_tasks(new_tasks)

    # Step 5: Return response
    return {"message": "Task deleted successfully"}


@router.put("/tasks/{task_id}/complete")
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

@router.get("/tasks/completed")
def get_completed_tasks():

    tasks  = load_tasks()

    completed_tasks = []
    for task in tasks:
        if task["status"] == "completed":
            completed_tasks.append(task)

    return completed_tasks

@router.get("/tasks/search")
def search_tasks(query: str):
    tasks = load_tasks()

    matched_tasks = []
    for task in tasks:
        if query.lower() in task["title"].lower():
            matched_tasks.append(task)

    return matched_tasks

@router.get("/tasks/filter")
def filter_tasks(priority: str):
    tasks = load_tasks()

    filtered_tasks = []

    for task in tasks:
        if task.get("priority", "").lower() == priority.lower():
            filtered_tasks.append(task)

    return filtered_tasks

@router.get("/")
def read_root():
    return {"message": "Task Manager API is running"}

@router.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

# =========================
# DB connection check
# =========================

@router.get("/test-db")
def test_de():
    conn = get_connection()
    return {"message":"DB connected successfully"}

@router.post("/db_task")
def create_task_db(title: str, priority: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Use lowercase %s for PostgreSQL/MySQL or '?' for SQLite
        # 2. Ensure variables are passed as a tuple: (title, priority)
        cursor.execute(
            "INSERT INTO tasks (title, priority) VALUES (%s, %s)",
            (title, priority)
        )
        conn.commit()
    except Exception as e:
        # If something goes wrong, undo the changes
        conn.rollback()
        return {"error": str(e)}
    finally:
        # This runs even if the code crashes, preventing memory leaks
        cursor.close()  # Fixed the 'colse' typo
        conn.close()

    return {"message": "Task added to DB"}


@router.get("/get_task")
def fetch_all_task():
    db_task = fetch_task()

    # If the list is empty, return a message instead of just []
    if not db_task:
        return {"message": "Database connected, but no tasks found. Please add a task using /db_task first."}

    return db_task


@router.put("/update_task_db/{task_id}")
def update_task_endpoint(task_id: int, task_data: TaskUpdate):

    # 1. Extract values from the Pydantic model
    new_title = task_data.title
    #new_priority = task_data.priority # If your model has this

    # 2. Call the Service Function (The one that talks to PostgreSQL)
    # This replaces the "for loop" because SQL finds the ID instantly
    db_result = update_task(task_id, new_title)

    # 3. Check if the database actually found that ID
    if db_result is None:
        # Return Error if ID 999 doesn't exist
        return {"error": "Task not found in Database"}

    # 4. Return Success
    return {"message": "Task updated successfully", "updated_task": db_result}


@router.delete("/tasks_db/{task_id}")
def delete_taskdb(task_id: int):

    db_result = delete_task(task_id)
    if db_result is None:
        # Return Error if ID 999 doesn't exist
        return {"error": "Task not found in Database"}

    # 4. Return Success
    return {"message": "Task deleted successfully", "delete_task": db_result}