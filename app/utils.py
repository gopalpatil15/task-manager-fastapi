import json
from app.config import DATA_FILE

def load_tasks():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    # write to data.json
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

