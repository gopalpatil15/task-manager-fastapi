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
    cursor.execute("SELECT id, title, status, priority FROM tasks where user_id = %s")
    tasks = cursor.fetchall()
    cursor.close()
    return tasks

def update_task(conn, task_id: int, new_title: str, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET title = %s WHERE id = %s and user_id = %s", (new_title, task_id))
        conn.commit()
        return {"status": "success", "updated_id": task_id}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}   
    finally:
        cursor.close()

def insert_task(conn, title, priority, user_id):
    cursor = conn.cursor()
    try:
        # Pass variables as a tuple to the execute method
        cursor.execute(
            "INSERT INTO tasks (title, priority, user_id) VALUES (%s, %s, %s)",
            (title, priority, user_id)
        )
        conn.commit()
        return {"status": "success", "message": "Task added to DB"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        # Only close the cursor. 
        # The 'conn' is closed by the get_connection dependency.
        cursor.close()


def insert_task(conn, title, priority, user_id):
    cursor = conn.cursor()
    try:
        # Pass variables as a tuple to the execute method
        cursor.execute(
            "INSERT INTO tasks (title, priority, user_id) VALUES (%s, %s, %s)",
            (title, priority, user_id)
        )
        conn.commit()
        return {"status": "success", "message": "Task added to DB"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        # Only close the cursor. 
        # The 'conn' is closed by the get_connection dependency.
        cursor.close()