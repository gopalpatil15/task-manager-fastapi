import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# --- DATABASE CONNECTION ---
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


# --- CREATE TABLES ---
def create_tables():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    try:
        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            )
        """)

        # TASKS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                priority VARCHAR(20) DEFAULT 'medium',
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()

        # DEBUG (Optional)
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        print("Tables:", cursor.fetchall())

        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks'")
        print("Tasks columns:", cursor.fetchall())

        print("Tables created successfully!")

    except Exception as e:
        conn.rollback()
        print("Error creating tables:", e)

    finally:
        cursor.close()
        conn.close()


# --- FETCH TASKS ---
def fetch_task(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, title, description, status, priority FROM tasks WHERE user_id = %s",
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()


# --- INSERT TASK ---
def insert_task(conn, title, description, priority, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO tasks (title, description, priority, user_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (title, description, priority, user_id)
        )
        new_id = cursor.fetchone()["id"]
        conn.commit()

        return {"status": "success", "id": new_id}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()


# --- UPDATE TASK ---
def update_task(conn, task_id, title, description, priority, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, description = %s, priority = %s
            WHERE id = %s AND user_id = %s
            RETURNING id
            """,
            (title, description, priority, task_id, user_id)
        )

        updated = cursor.fetchone()
        conn.commit()

        if not updated:
            return {"status": "error", "message": "Task not found or unauthorized"}

        return {"status": "success", "updated_id": updated["id"]}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()


# --- DELETE TASK ---
def delete_task_db(conn, task_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s AND user_id = %s
            RETURNING id
            """,
            (task_id, user_id)
        )

        deleted = cursor.fetchone()
        conn.commit()

        if not deleted:
            return {"status": "error", "message": "Task not found or not yours"}

        return {"status": "success", "deleted_id": deleted["id"]}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()