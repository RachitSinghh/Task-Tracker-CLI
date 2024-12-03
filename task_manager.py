import json
import os
import argparse

FILE_PATH = "tasks.json"

def load_task():
    if not os.path.exists(FILE_PATH):
        return []
    with open (FILE_PATH, 'r')as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(FILE_PATH, "w") as file: 
        json.dump(tasks, file, indent=4)

parser = argparse.ArgumentParser(description="Task Manger CLI")
parser.add_argument("action", help="Action to perform", choices=["add", "update","delete", "mark", "list"])
parser.add_argument("--id", type=int, help="Task ID(for update, delete, or Mark)")
parser.add_argument("--title", type=str, help="Task title(for add or update)")
parser.add_argument("--status", type=str, choices=["in progress", "done", "not done"], help="Task status")

args = parser.parse_args()

def add_task(title):
    tasks = load_task()
    tasks_id = max([task['id'] for task in tasks], default=0) + 1
    tasks.append({"id": tasks_id, "title":title, "status":"not done"})
    save_tasks(tasks)
    print(f"Task added with ID {tasks_id}")

def update_task(task_id, title):
    tasks = load_task()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            save_tasks(tasks)
            print(f"Task {task_id} updated")
            return 
    print(f"Task {task_id} not found")
    
def delete_task(task_id):
    tasks = load_task()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted")

def mark_task(task_id, status):
    tasks = load_task()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return 
    print(f"Task {task_id} not found")

def list_tasks(filter_status=None):
    tasks = load_task()
    filtered = [task for task in tasks if filter_status is None or task["status"] == filter_status]
    for task in filtered:
        print(f"ID: {task['id']} | Title: {task['title']} | Status: {task['status']}")
    if not filtered:
        print("No tasks found")


if __name__ == "__main__":
    tasks = load_task()

    if args.action == 'add' and args.title:
        add_task(args.title)
    elif args.action == "update" and args.id and args.title:
        update_task(args.id, args.title)
    elif args.action == "delete" and args.id:
        delete_task(args.id)
    elif args.action == "mark" and args.id and args. status:
        mark_task(args.id, args.status)
    elif args.action == "list":
        list_tasks(args.status)
    else:
        print("Invalid arguemetns. Use --help for guidance")    