def add_task(tasks, title, priority):
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    task = {
        "id": new_id,
        "title": title,
        "status": "pending",
        "priority": priority
    }
    tasks.append(task)
    return tasks

def get_tasks(tasks):
    return tasks

def update_task(tasks, task_id, new_title):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            return True, tasks
    return False, tasks

def delete_task(tasks, task_id):
    tasks = [task for task in tasks if task["id"] != task_id]
    return tasks
    