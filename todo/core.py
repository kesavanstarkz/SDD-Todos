"""Core business logic for todo tasks."""

from typing import List, Dict, Any


def add_task(tasks: List[Dict[str, Any]], description: str) -> Dict[str, Any]:
    """Add a new task with a unique incrementing numeric ID.

    Raises ValueError if description is empty.
    """
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Task description cannot be empty.")

    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": next_id,
        "description": description.strip(),
        "done": False,
    }
    tasks.append(new_task)
    return new_task


def format_task(task: Dict[str, Any]) -> str:
    """Format a single task with ID, description, and status."""
    status = "done" if task.get("done") else "pending"
    return f"{task['id']}. [{status}] {task['description']}"


def format_task_list(tasks: List[Dict[str, Any]]) -> List[str]:
    """Format a list of tasks."""
    return [format_task(t) for t in tasks]


def mark_done(tasks: List[Dict[str, Any]], task_id: int) -> Dict[str, Any]:
    """Mark a task as done by its ID.

    Raises ValueError if task_id is invalid or not found.
    """
    if not isinstance(task_id, int):
        raise ValueError(f"Invalid task ID: {task_id}")

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return task
    raise ValueError(f"Task with ID {task_id} not found.")


def delete_task(tasks: List[Dict[str, Any]], task_id: int) -> Dict[str, Any]:
    """Delete a task by its ID.

    Raises ValueError if task_id is invalid or not found.
    """
    if not isinstance(task_id, int):
        raise ValueError(f"Invalid task ID: {task_id}")

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(i)
    raise ValueError(f"Task with ID {task_id} not found.")
