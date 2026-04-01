import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import Depends

load_dotenv()

# --- DATABASE SETUP (Run this once) ---
def create_tables():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,              -- <--- ADDED THIS LINE
            status VARCHAR(20) DEFAULT 'pending',
            priority VARCHAR(20) DEFAULT 'medium',
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    for command in commands:
        cursor.execute(command)
    conn.commit()
    cursor.close()
    
    # Check if user_id column exists, if not add it
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks' AND column_name = 'user_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE tasks ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE")
        conn.commit()
        print("Added user_id column")
    
    # Check tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    print("Tables:", cursor.fetchall())
    
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks'")
    print("Tasks columns:", cursor.fetchall())
    
    cursor.close()
    conn.close()
    print("Tables created successfully!")

# --- FASTAPI DEPENDENCY ---
def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor 
    )
    try:
        yield conn
    finally:
        conn.close()


def fetch_task(conn, user_id):
    cursor = conn.cursor()
    # RealDictCursor already makes these dictionaries!
    cursor.execute("SELECT id, title, description, status, priority FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    return tasks

def update_task(conn, task_id: int, title: str, description: str, priority: str, user_id: int):
    cursor = conn.cursor()
    try:
        # We use 'AND user_id = %s' for security
        cursor.execute(
            """
            UPDATE tasks 
            SET title = %s, description = %s, priority = %s 
            WHERE id = %s AND user_id = %s
            RETURNING id
            """,
            (title, description, priority, task_id, user_id)
        )
        updated_row = cursor.fetchone()
        conn.commit()
        
        if not updated_row:
            return {"status": "error", "message": "Task not found or unauthorized"}
            
        return {"status": "success", "updated_id": task_id}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()

def insert_task(conn, title, description, priority, user_id):
    cursor = conn.cursor()
    try:
        # Use 'user_id' to match your CREATE TABLE command
        cursor.execute(
            "INSERT INTO tasks (title, description, priority, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (title, description, priority, user_id)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return {"status": "success", "message": "Task added to DB", "id": new_id}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()


def delete_task_db(conn, task_id: int, user_id: int):
    cursor = conn.cursor()
    try:
        # 1. Added the missing '= %s'
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id", 
            (task_id, user_id)
        )
        deleted_row = cursor.fetchone()
        conn.commit()

        if not deleted_row:
            return {"status": "error", "message": "Task not found or not yours"}

        return {"status": "success", "message": f"Task {task_id} deleted"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        # 2. ONLY close the cursor
        cursor.close()