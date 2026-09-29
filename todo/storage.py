"""Storage module for persisting todo tasks in JSON format."""

import json
import os
from typing import List, Dict, Any, Optional

DEFAULT_STORAGE_PATH = os.path.expanduser("~/.todo.json")


def get_storage_path(filepath: Optional[str] = None) -> str:
    """Return the resolved storage file path."""
    if filepath is not None:
        return os.path.expanduser(str(filepath))
    return os.environ.get("TODO_FILE", DEFAULT_STORAGE_PATH)


def load_tasks(filepath: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load tasks from the JSON storage file.

    Returns an empty list if the file does not exist.
    """
    path = get_storage_path(filepath)
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: List[Dict[str, Any]], filepath: Optional[str] = None) -> None:
    """Save tasks to the JSON storage file."""
    path = get_storage_path(filepath)
    parent_dir = os.path.dirname(path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
