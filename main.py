from fastapi import FastAPI
from app.api import router
from app.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION

# Create FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Include the API router
app.include_router(router)

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)