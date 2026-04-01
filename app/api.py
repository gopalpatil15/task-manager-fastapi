from fastapi import FastAPI, Response, APIRouter, Depends, HTTPException, status, Query
from app.models import TaskCreate, TaskUpdate, TaskResponse, UserCreate, UserLogin, Token
from app.db import get_connection, fetch_task, update_task, insert_task, delete_task_db
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import psycopg2.extras

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- AUTH DEPENDENCY ---
def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(get_connection)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Fetch the actual user ID from the DB
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user # Returns the RealDictCursor dictionary
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter()

# --- AUTH ENDPOINTS ---

@router.post("/register", status_code=201)
def register(user: UserCreate, conn = Depends(get_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_pwd = get_password_hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            (user.username, hashed_pwd)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    finally:
        cursor.close()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    conn = Depends(get_connection)
):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
    db_user = cursor.fetchone()
    cursor.close()

    if not db_user or not pwd_context.verify(form_data.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "current_user": {
            "id": db_user["id"],
            "username": db_user["username"]
        }
    }

# --- TASK ENDPOINTS (DB ONLY) ---

@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(conn = Depends(get_connection), current_user = Depends(get_current_user)):
    # Pass BOTH conn and user_id to your fetch_task function
    return fetch_task(conn, current_user["id"])

@router.post("/tasks", status_code=201)
async def create_task(
    task: TaskCreate, 
    conn = Depends(get_connection),
    current_user = Depends(get_current_user)
):
    # Match the 5 arguments defined in insert_task
    result = insert_task(
        conn, 
        task.title, 
        task.description, 
        task.priority, 
        current_user["id"]  # This is the 'user_id'
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.put("/tasks/{task_id}")
async def update_existing_task(
    task_id: int, 
    task_data: TaskUpdate, 
    conn = Depends(get_connection),
    current_user = Depends(get_current_user)
):
    result = update_task(conn, task_id, task_data.title, task_data.description, task_data.priority, current_user["id"])
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.delete("/tasks/{task_id}")
async def delete_task_endpoint(
    task_id: int, 
    conn = Depends(get_connection),
    current_user = Depends(get_current_user)
):
    # Call the delete function from db.py
    result = delete_task_db(conn, task_id, current_user["id"])
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.get("/")
def read_root():
    return {"message": "Task Manager API is running on PostgreSQL"}





