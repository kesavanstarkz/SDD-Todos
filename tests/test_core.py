import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from todo import core, storage
from todo import cli


class TestTodoCore(unittest.TestCase):
    def setUp(self):
        self.empty_tasks = []

    def test_ac1_add_first_task(self):
        """AC-1 (FR-1): Given an empty list, when I add 'buy milk',

        then the list has one pending task with ID 1.
        """
        tasks = []
        new_task = core.add_task(tasks, "buy milk")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(new_task["id"], 1)
        self.assertEqual(new_task["description"], "buy milk")
        self.assertFalse(new_task["done"])
        self.assertEqual(tasks[0], {"id": 1, "description": "buy milk", "done": False})

    def test_ac2_list_tasks(self):
        """AC-2 (FR-2): Given 2 tasks, when I list,

        then both appear with their status.
        """
        tasks = [
            {"id": 1, "description": "buy milk", "done": False},
            {"id": 2, "description": "clean room", "done": True},
        ]
        formatted = core.format_task_list(tasks)

        self.assertEqual(len(formatted), 2)
        # Verify both appear with ID, description, and status (pending/done)
        self.assertIn("1", formatted[0])
        self.assertIn("buy milk", formatted[0])
        self.assertIn("pending", formatted[0].lower())

        self.assertIn("2", formatted[1])
        self.assertIn("clean room", formatted[1])
        self.assertIn("done", formatted[1].lower())

    def test_ac3_mark_task_done(self):
        """AC-3 (FR-3): Given task 1 is pending, when I mark it done,

        then list shows it as done.
        """
        tasks = [
            {"id": 1, "description": "buy milk", "done": False},
        ]
        updated = core.mark_done(tasks, 1)

        self.assertTrue(updated["done"])
        self.assertTrue(tasks[0]["done"])

        formatted = core.format_task_list(tasks)
        self.assertIn("done", formatted[0].lower())

    def test_ac4_delete_task(self):
        """AC-4 (FR-4): Given task 2 exists, when I delete it,

        then it no longer appears and other IDs are unchanged.
        """
        tasks = [
            {"id": 1, "description": "buy milk", "done": False},
            {"id": 2, "description": "clean room", "done": False},
            {"id": 3, "description": "read book", "done": False},
        ]
        deleted = core.delete_task(tasks, 2)

        self.assertEqual(deleted["id"], 2)
        self.assertEqual(len(tasks), 2)
        remaining_ids = [t["id"] for t in tasks]
        self.assertNotIn(2, remaining_ids)
        self.assertEqual(remaining_ids, [1, 3])
        self.assertEqual(tasks[0]["id"], 1)
        self.assertEqual(tasks[1]["id"], 3)

    def test_ac5_persistence_between_sessions(self):
        """AC-5 (FR-5): Given I added a task and exited,

        when I run list in a new session, then the task is still there.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")

            # Session 1: add task and save
            session1_tasks = storage.load_tasks(file_path)
            self.assertEqual(session1_tasks, [])
            core.add_task(session1_tasks, "buy milk")
            storage.save_tasks(session1_tasks, file_path)

            # Session 2: start new session by loading from storage
            session2_tasks = storage.load_tasks(file_path)
            self.assertEqual(len(session2_tasks), 1)
            self.assertEqual(session2_tasks[0]["id"], 1)
            self.assertEqual(session2_tasks[0]["description"], "buy milk")
            self.assertFalse(session2_tasks[0]["done"])

    def test_ac6_done_unknown_id(self):
        """AC-6 (FR-6): When I run done 99 and no task 99 exists,

        then I see an error message and the list is unchanged.
        """
        tasks = [
            {"id": 1, "description": "buy milk", "done": False}
        ]
        with self.assertRaises(ValueError) as ctx:
            core.mark_done(tasks, 99)

        self.assertIn("99", str(ctx.exception))
        # List must remain unchanged
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 1)
        self.assertFalse(tasks[0]["done"])

    def test_fr6_empty_description(self):
        """FR-6: Clear error for an empty description, and list not modified."""
        tasks = [{"id": 1, "description": "buy milk", "done": False}]

        for empty_val in ["", "   ", "\t\n"]:
            with self.assertRaises(ValueError) as ctx:
                core.add_task(tasks, empty_val)
            self.assertIn("empty", str(ctx.exception).lower())

        self.assertEqual(len(tasks), 1)

    def test_fr6_delete_unknown_id(self):
        """FR-6: Clear error for unknown ID on delete, and list not modified."""
        tasks = [{"id": 1, "description": "buy milk", "done": False}]

        with self.assertRaises(ValueError) as ctx:
            core.delete_task(tasks, 42)

        self.assertIn("42", str(ctx.exception))
        self.assertEqual(len(tasks), 1)


class TestStorage(unittest.TestCase):
    def test_load_non_existent_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "nonexistent.json")
            tasks = storage.load_tasks(file_path)
            self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")
            data = [{"id": 1, "description": "task 1", "done": False}]
            storage.save_tasks(data, file_path)
            loaded = storage.load_tasks(file_path)
            self.assertEqual(loaded, data)


class TestCLI(unittest.TestCase):
    def test_cli_add_and_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")
            with patch.dict(os.environ, {"TODO_FILE": file_path}):
                # Add task via CLI
                cli.main(["add", "buy", "milk"])

                # List tasks via CLI
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    cli.main(["list"])
                    output = mock_stdout.getvalue()
                    self.assertIn("1", output)
                    self.assertIn("buy milk", output)
                    self.assertIn("pending", output.lower())

    def test_cli_done_and_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")
            with patch.dict(os.environ, {"TODO_FILE": file_path}):
                cli.main(["add", "buy milk"])
                cli.main(["done", "1"])

                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    cli.main(["list"])
                    output = mock_stdout.getvalue()
                    self.assertIn("done", output.lower())

                cli.main(["delete", "1"])
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    cli.main(["list"])
                    output = mock_stdout.getvalue()
                    self.assertNotIn("buy milk", output)

    def test_cli_ac6_done_unknown_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")
            with patch.dict(os.environ, {"TODO_FILE": file_path}):
                cli.main(["add", "buy milk"])
                with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                    with self.assertRaises(SystemExit) as cm:
                        cli.main(["done", "99"])
                    self.assertNotEqual(cm.exception.code, 0)
                    self.assertIn("99", mock_stderr.getvalue())

                # Verify list is unchanged
                tasks = storage.load_tasks(file_path)
                self.assertEqual(len(tasks), 1)
                self.assertFalse(tasks[0]["done"])

    def test_cli_empty_description_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "todo.json")
            with patch.dict(os.environ, {"TODO_FILE": file_path}):
                with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                    with self.assertRaises(SystemExit) as cm:
                        cli.main(["add", "   "])
                    self.assertNotEqual(cm.exception.code, 0)
                    self.assertIn("empty", mock_stderr.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
