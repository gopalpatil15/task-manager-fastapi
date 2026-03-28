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
├── data/             # JSON data storage
├── tests/            # Test suite
├── docs/             # Documentation
├── main.py           # Entry point
└── requirements.txt  # Dependencies
```

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