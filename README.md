# Todo CLI (Spec-Driven Development)

A lightweight command-line todo manager built using Spec-Driven Development (SDD) principles with pure Python 3 standard library.

---

## Table of Contents

- [Project Files & Structure](#project-files--structure)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
  - [CLI Commands](#cli-commands)
  - [Optional Shell Alias](#optional-shell-alias)
- [Data Storage & Configuration](#data-storage--configuration)
- [Running Tests](#running-tests)
- [Specification & Acceptance Criteria](#specification--acceptance-criteria)

---

## Project Files & Structure

| File / Folder | Purpose |
|---------------|---------|
| [`spec.md`](spec.md) | **Product Specification**: Problem statement, user stories (US-1 to US-5), functional requirements (FR-1 to FR-6), acceptance criteria (AC-1 to AC-6), and non-goals. |
| [`plan.md`](plan.md) | **Technical Design Plan**: Technology choices, data models, file layout, and requirement-to-code mapping. |
| [`tasks.md`](tasks.md) | **Task Checklist**: Ordered task list (T1 to T7) tracking progress from test writing to implementation and manual verification. |
| [`todo/`](todo/) | **Application Package**: |
| ├── [`todo/core.py`](todo/core.py) | Business logic for adding, listing, completing, and deleting tasks, including validation. |
| ├── [`todo/storage.py`](todo/storage.py) | JSON file persistence (`load_tasks`, `save_tasks`). |
| ├── [`todo/cli.py`](todo/cli.py) | Command-line interface and argument parsing (`argparse`). |
| └── [`todo/__main__.py`](todo/__main__.py) | Module execution entrypoint (`python3 -m todo`). |
| [`tests/`](tests/) | **Automated Tests**: |
| └── [`tests/test_core.py`](tests/test_core.py) | `unittest` test suite covering core operations, storage, error cases, and CLI workflows. |

---

## Requirements

- **Python 3.9+** (Standard library only: `argparse`, `json`, `unittest`).
- No external packages or third-party dependencies required.

---

## How to Run

Run the tool as a Python module from the project root:

### CLI Commands

#### 1. Add a Task
Adds a task with an incrementing numeric ID.
```bash
python3 -m todo add "buy milk"
# or without quotes
python3 -m todo add buy milk
```

#### 2. List All Tasks
Displays all tasks with their ID, status (`[pending]` or `[done]`), and description.
```bash
python3 -m todo list
```
*Example Output:*
```text
1. [pending] buy milk
2. [done] clean room
```

#### 3. Mark a Task as Done
Marks a task completed by its numeric ID.
```bash
python3 -m todo done 1
```

#### 4. Delete a Task
Deletes a task by its numeric ID without altering remaining task IDs.
```bash
python3 -m todo delete 1
```

#### 5. Command Help
```bash
python3 -m todo --help
```

---

### Optional Shell Alias

For quicker usage without typing `python3 -m todo`, create an alias in your shell:

```bash
alias todo="python3 -m todo"
```
Then use it directly:
```bash
todo add "read book"
todo list
todo done 1
todo delete 1
```

---

## Data Storage & Configuration

- **Default Storage Location**: `~/.todo.json`
- **Data Format**: JSON array of tasks:
  ```json
  [
    {
      "id": 1,
      "description": "buy milk",
      "done": false
    }
  ]
  ```
- **Custom Storage File**: Override the storage location by setting the `TODO_FILE` environment variable:
  ```bash
  TODO_FILE="./custom_todos.json" python3 -m todo list
  ```

---

## Running Tests

Execute the full suite of unit and acceptance criterion tests:

```bash
python3 -m unittest discover tests
```

---

## Specification & Acceptance Criteria

| Criteria | Requirement | Status |
|----------|-------------|--------|
| **AC-1** | Add task to empty list creates task with ID 1 and pending status | Verified |
| **AC-2** | Listing displays ID, description, and status for all tasks | Verified |
| **AC-3** | Marking task done updates status to `[done]` | Verified |
| **AC-4** | Deleting a task removes it while preserving other task IDs | Verified |
| **AC-5** | Tasks persist across separate sessions / invocations | Verified |
| **AC-6** | Operations with unknown ID or empty descriptions display clear errors and preserve list state | Verified |
