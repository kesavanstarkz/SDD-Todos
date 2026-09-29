# Spec: Todo CLI

## Problem & Goal
People who live in the terminal want to jot down and check off tasks without
opening a separate app. This tool lets a user manage a personal todo list from
the command line, with tasks saved between sessions.

## User Stories
- US-1: As a user, I can add a task so that I don't forget it.
- US-2: As a user, I can list my tasks so that I see what's pending.
- US-3: As a user, I can mark a task done so that I track progress.
- US-4: As a user, I can delete a task so that my list stays clean.
- US-5: As a user, I can close the program and find my tasks still there.

## Functional Requirements
- FR-1: The system shall add a task from a text description; each task gets a
  unique numeric ID.
- FR-2: The system shall list all tasks showing ID, description, and status
  (pending/done).
- FR-3: The system shall mark a task done by ID.
- FR-4: The system shall delete a task by ID.
- FR-5: Tasks shall persist between runs.
- FR-6: The system shall show a clear error for an unknown ID or an empty
  description, and shall not modify the list in that case.

## Non-Goals
- No due dates, priorities, or tags
- No multi-user support or syncing
- No GUI or web interface

## Acceptance Criteria
- AC-1 (FR-1): Given an empty list, when I add "buy milk", then the list has
  one pending task with ID 1.
- AC-2 (FR-2): Given 2 tasks, when I list, then both appear with their status.
- AC-3 (FR-3): Given task 1 is pending, when I mark it done, then list shows
  it as done.
- AC-4 (FR-4): Given task 2 exists, when I delete it, then it no longer
  appears and other IDs are unchanged.
- AC-5 (FR-5): Given I added a task and exited, when I run list in a new
  session, then the task is still there.
- AC-6 (FR-6): When I run `done 99` and no task 99 exists, then I see an error
  message and the list is unchanged.

## Open Questions
- Should deleted IDs be reused, or always increment?
- Should `list` hide completed tasks by default?