import psycopg2
from psycopg2.extras import RealDictCursor

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import Depends, HTTPException

load_dotenv()

def get_connection():
    # Ensure your .env has these exact keys!
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
        
def fetch_task():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status, priority FROM tasks")
    rows = cursor.fetchall()
    
    # Convert list of tuples into list of dictionaries
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "status": row[2],
            "priority": row[3]
        })
    
    cursor.close()
    conn.close()
    return tasks

def update_task(task_id: int, new_title: str): # Add parameters here
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Provide the values in a tuple as the second argument
        cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (new_title, task_id))
        
        # 2. IMPORTANT: You must commit for the change to save!
        conn.commit()
        
        return {"status": "success", "updated_id": task_id}
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return {"status": "error"}
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        
        conn.commit()

        return {"status": "success", "message": f"Task {task_id} deleted"}
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()