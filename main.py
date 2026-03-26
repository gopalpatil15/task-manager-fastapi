from utils import load_tasks, save_tasks
from services import add_task, get_tasks, update_task, delete_task

tasks = load_tasks()

# Add
tasks = add_task(tasks, "Learn API", "high")

# Update id=1
tasks = update_task(tasks, 1, "Master FastAPI")

# Delete id=2
tasks = delete_task(tasks, 2)

save_tasks(tasks)

print(tasks)