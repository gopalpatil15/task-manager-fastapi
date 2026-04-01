# Task Manager API

A modern, modular Task Manager API built with FastAPI that supports both JSON file storage and PostgreSQL database persistence.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Access the API:**
   - API: http://127.0.0.1:8000
   - Documentation: http://127.0.0.1:8000/docs
   - Alternative docs: http://127.0.0.1:8000/redoc

## Features

- RESTful API design
- Task CRUD operations
- Search and filtering
- Task completion tracking
- JSON file storage
- PostgreSQL database support
- Pydantic data validation
- Automatic API documentation
- Modular architecture

## Project Structure

```
task_manager/
├── app/              # Application package
│   ├── api.py        # FastAPI endpoint definitions + auth
│   ├── db.py         # PostgreSQL connection + task DB operations
│   ├── models.py     # Pydantic request/response schemas
│   ├── services.py   # Business logic (optional layer)
│   └── utils.py      # Helpers and common utilities
├── data/             # JSON file storage option (fallback)
├── tests/            # Test suite
├── docs/             # Documentation
├── main.py           # Entry point
└── requirements.txt  # Dependencies
```

## Project Analysis & Update Notes

- `TaskCreate`/`TaskUpdate` schemas now include optional `description` and `priority` to align with DB fields.
- API token-based auth uses `OAuth2PasswordBearer` with JWT, and user-specific tasks are enforced by `user_id` checks.
- Database operations in `app/db.py` implement transactions with commit/rollback and row-level ownership guard (`WHERE user_id = %s`).
- `app/api.py` now returns detailed error HTTP codes for unauthorized or not-found operations.
- The previous bug ("TaskCreate has no attribute description") is resolved by ensuring model fields match endpoint usage.

## Quick Validation

1. Create records:
   - POST `/register` + POST `/login` to get bearer token.
   - POST `/tasks` with body `{"title": "Test", "description": "desc", "priority": "high"}`.
2. Read records:
   - GET `/tasks` authenticated.
3. Update/Delete records (user-scoped):
   - PUT `/tasks/{id}` and DELETE `/tasks/{id}`.
4. Run tests:
   - `pytest -q tests/test_api.py`.

## API Endpoints

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `GET /tasks/search` - Search tasks
- `GET /tasks/filter` - Filter by priority

## Documentation

For detailed API documentation, installation guide, and usage examples, see [docs/README.md](docs/README.md).

## License

MIT License - see [LICENSE](LICENSE) file for details.