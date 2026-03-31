# Task Manager API (FastAPI)

## 🚀 Description
A RESTful Task Manager API built using FastAPI and Python, supporting CRUD operations, filtering, search, and task status management with a modular backend architecture and both file-based and database persistence.

## 💡 Highlights
- Designed modular backend architecture separating API, services, models, and utility layers
- Implemented RESTful APIs with filtering, search, and task status management
- Structured request validation using Pydantic models
- Support for both JSON file storage and PostgreSQL database
- Automatic API documentation with Swagger UI

## 🛠 Tech Stack
- Python
- FastAPI
- Pydantic
- JSON (file-based storage)
- PostgreSQL (database storage)
- Uvicorn (ASGI server)

## 📦 Project Structure
```
task_manager/
├─ app/                   # Main application package
│  ├─ __init__.py         # Package marker
│  ├─ main.py             # FastAPI app creation & router inclusion
│  ├─ api.py              # All API routes
│  ├─ models.py           # Pydantic models (TaskCreate, TaskUpdate, etc.)
│  ├─ services.py         # Business logic (CRUD operations)
│  ├─ db.py               # Database functions
│  ├─ utils.py            # JSON load/save helpers
│  └─ config.py           # Settings & constants
│
├─ data/                  # Data storage
│  └─ data.json           # Task data (JSON storage)
│
├─ tests/                 # Test suite
│  └─ test_api.py         # Basic API tests
│
├─ docs/                  # Documentation
│  └─ README.md           # API documentation
│
├─ main.py                # Entry point
├─ requirements.txt       # Dependencies
└─ README.md              # Project overview
```

## 📌 Features
- Create, update, delete tasks (JSON + Database)
- Mark tasks as completed
- Get all tasks and completed tasks
- Search tasks by keyword
- Filter tasks by priority
- Database connection testing
- Modular and scalable architecture

## 📡 API Endpoints

### Tasks (JSON Storage)
- `GET /tasks` → Get all tasks
- `POST /tasks` → Create new task
- `PUT /tasks/{task_id}` → Update task
- `DELETE /tasks/{task_id}` → Delete task
- `PUT /tasks/{task_id}/complete` → Mark task as completed
- `GET /tasks/completed` → Get completed tasks
- `GET /tasks/search?query=...` → Search tasks
- `GET /tasks/filter?priority=...` → Filter tasks by priority

### Database Tasks
- `POST /db_task` → Create task in database
- `GET /get_task` → Get all database tasks
- `PUT /update_task_db/{task_id}` → Update database task
- `DELETE /tasks_db/{task_id}` → Delete database task

### Utility
- `GET /test-db` → Test database connection
- `GET /` → API status
- `GET /favicon.ico` → Favicon

## 🛠 How it works
- Tasks can be stored in `data/data.json` as a list of dictionaries (JSON mode)
- Tasks can also be stored in PostgreSQL database (DB mode)
- Business logic is handled in `app/services.py`
- File persistence is managed using `app/utils.py`
- Database operations are handled in `app/db.py`
- FastAPI exposes REST endpoints in `app/api.py`
- Pydantic models in `app/models.py` ensure data validation

## ▶️ Run Locally

1. Activate virtual environment:
```bash
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database (optional):
Update `app/config.py` with your PostgreSQL connection string:
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/task_manager"
```

4. Start the server:
```bash
python main.py
```
Or with uvicorn:
```bash
uvicorn app.main:app --reload
```

5. Open API docs:
http://127.0.0.1:8000/docs

## 📝 Usage Examples

### Create a Task (JSON)
```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "priority": "high"}'
```

### Get All Tasks
```bash
curl -X GET "http://127.0.0.1:8000/tasks"
```

### Update a Task
```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Master FastAPI", "priority": "high"}'
```

### Search Tasks
```bash
curl -X GET "http://127.0.0.1:8000/tasks/search?query=learn"
```

### Filter by Priority
```bash
curl -X GET "http://127.0.0.1:8000/tasks/filter?priority=high"
```

### Create Task in Database
```bash
curl -X POST "http://127.0.0.1:8000/db_task?title=Database%20Task&priority=medium"
```

### Update Database Task
```bash
curl -X PUT "http://127.0.0.1:8000/update_task_db/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated DB Task", "priority": "high"}'
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_api.py
```

## 🔄 Future Improvements

- [ ] Add JWT-based authentication
- [ ] Implement user management
- [ ] Add task categories/tags
- [ ] Improve error handling and validation
- [ ] Add rate limiting
- [ ] Implement caching
- [ ] Add API versioning
- [ ] Create Docker containerization
- [ ] Add CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
2. Create a feature branch
3. Commit your changes
4. Push and open a pull request


📄 License

MIT License — free to use and modify

---

