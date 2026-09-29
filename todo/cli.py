"""Command line interface for Todo app using argparse."""

import argparse
import sys
from typing import List, Optional

from todo import core, storage


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A command-line todo list manager.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument(
        "description",
        nargs="+",
        help="Task description",
    )

    # list command
    subparsers.add_parser("list", help="List all tasks")

    # done command
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument(
        "id",
        type=int,
        help="Numeric ID of the task to mark done",
    )

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task by ID")
    delete_parser.add_argument(
        "id",
        type=int,
        help="Numeric ID of the task to delete",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Main CLI entrypoint."""
    parsed = parse_args(args)

    if not parsed.command:
        print("Usage: todo <command> [arguments]. Run 'todo --help' for details.")
        return

    tasks = storage.load_tasks()

    if parsed.command == "add":
        desc = " ".join(parsed.description).strip()
        try:
            new_task = core.add_task(tasks, desc)
            storage.save_tasks(tasks)
            print(f"Added task {new_task['id']}: {new_task['description']}")
        except ValueError as err:
            sys.stderr.write(f"Error: {err}\n")
            sys.exit(1)

    elif parsed.command == "list":
        if not tasks:
            print("No tasks found.")
        else:
            for line in core.format_task_list(tasks):
                print(line)

    elif parsed.command == "done":
        try:
            task = core.mark_done(tasks, parsed.id)
            storage.save_tasks(tasks)
            print(f"Marked task {task['id']} as done.")
        except ValueError as err:
            sys.stderr.write(f"Error: {err}\n")
            sys.exit(1)

    elif parsed.command == "delete":
        try:
            task = core.delete_task(tasks, parsed.id)
            storage.save_tasks(tasks)
            print(f"Deleted task {task['id']}: {task['description']}")
        except ValueError as err:
            sys.stderr.write(f"Error: {err}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
