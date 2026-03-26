import json

def load_tasks():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    # write to data.json
    with open("data.json", "w") as f:
        json.dump(tasks, f, indent=4)

