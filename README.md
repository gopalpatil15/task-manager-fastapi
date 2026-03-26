# Task Manager API (FastAPI)

## 🚀 Description
A RESTful Task Manager API built using FastAPI and Python, supporting CRUD operations, filtering, search, and task status management with a modular backend architecture and lightweight file-based persistence (extensible to databases).

## 💡 Highlights
- Designed modular backend architecture separating API, services, and utility layers
- Implemented RESTful APIs with filtering, search, and task status management
- Structured request validation using Pydantic models

## 🛠 Tech Stack
- Python
- FastAPI
- Pydantic
- JSON (file-based storage)

## 📦 Project Structure
- `data.json`: persisted task storage (JSON array)
- `main.py`: demo script for service usage
- `main_api.py`: FastAPI server with API endpoints
- `services.py`: business logic (CRUD operations)
- `utils.py`: JSON load/save helpers

## 📌 Features
- Create, update, delete tasks
- Mark tasks as completed
- Get all tasks and completed tasks
- Search tasks by keyword
- Filter tasks by priority

## 📡 API Endpoints
- `GET /tasks` → Get all tasks  
- `POST /tasks` → Create new task  
- `PUT /tasks/{task_id}` → Update task  
- `DELETE /tasks/{task_id}` → Delete task  
- `PUT /tasks/{task_id}/complete` → Mark task as completed  
- `GET /tasks/completed` → Get completed tasks  
- `GET /tasks/search?keyword=...` → Search tasks  
- `GET /tasks/filter?priority=...` → Filter tasks by priority  

## 🛠 How it works
- Tasks are stored in `data.json` as a list of dictionaries
- Business logic is handled in `services.py`
- File persistence is managed using `utils.py`
- FastAPI exposes REST endpoints in `main_api.py`

## ▶️ Run Locally

1. Activate virtual environment:
```bash
venv\Scripts\activate

2. Install dependencies:



pip install fastapi uvicorn

3. Start the server:



uvicorn main_api:app --reload

4. Open API docs:
http://127.0.0.1:8000/docs



📝 Usage Examples

Create a Task

curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "priority": "high"}'

Get All Tasks

curl -X GET "http://127.0.0.1:8000/tasks"

Search Tasks

curl -X GET "http://127.0.0.1:8000/tasks/search?keyword=learn"

Filter by Priority

curl -X GET "http://127.0.0.1:8000/tasks/filter?priority=high"

🧪 Testing

Run the demo script:

python main.py

🔄 Future Improvements

Integrate PostgreSQL for scalable database persistence

Implement JWT-based authentication

Improve validation and error handling

Add automated testing


📁 Sample Data

The project uses a simple JSON file (data.json) to simulate persistent storage with sample tasks.

🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a pull request


📄 License

MIT License — free to use and modify

---

