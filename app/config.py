# Configuration settings for Task Manager

# Database connection string
DATABASE_URL = "postgresql://username:password@localhost:5432/task_manager"

# JSON data file path
DATA_FILE = "data/data.json"

# App settings
APP_TITLE = "Task Manager API"
APP_DESCRIPTION = "A simple task management API with FastAPI"
APP_VERSION = "1.0.0"

# JWT settings
SECRET_KEY = "your-secret-key-here"  # Change this to a secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30