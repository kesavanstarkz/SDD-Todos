# Plan: Todo CLI

## Tech Choices
- Python 3, standard library only (argparse, json). Keeps setup trivial.

## Data Model
Task = { "id": int, "description": str, "done": bool }
Stored as a JSON list in `~/.todo.json`.

## Layout
- todo/cli.py      -> parses commands
- todo/storage.py  -> load/save JSON
- todo/core.py     -> add, list, done, delete logic
- tests/test_core.py

## Decisions
- IDs always increment (answers the open question; avoids confusion).
- `list` shows everything, with a status marker.

## Requirement Mapping
| Requirement | Satisfied by              |
|-------------|---------------------------|
| FR-1..FR-4  | core.py functions         |
| FR-5        | storage.py                |
| FR-6        | validation in core.py     |