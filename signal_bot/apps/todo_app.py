import json
import re
from datetime import datetime, timezone
from pathlib import Path

from signal_bot.app_interface import CommandApp


class TodoApp(CommandApp):
    def __init__(self, data_dir: str | None = None):
        self.data_dir = Path(data_dir)
        self.todos: dict[str, list[dict]] = {}

    @property
    def name(self) -> str:
        return "todo"

    @property
    def description(self) -> str:
        return "A todo app to manage your life using signaalbot"

    HELP_TEXT = (
        "Available commands:\n"
        "  add <task>     - Add a new todo\n"
        "  list           - List your todos\n"
        "  done <number>  - Mark a todo as complete\n"
        "  undo <number>  - Unmark a completed todo\n"
        "  remove <number> - Remove a todo\n"
        "  clear          - Remove all todos\n"
        "  projects       - List all projects\n"
        "  contexts       - List all contexts\n"
        "  report         - Show open/completed counts\n"
        "  help           - Show this help message"
    )

    @staticmethod
    def _sanitise_sender(sender: str) -> str:
        return re.sub(r"\D", "", sender)

    def handle(self, args: str, sender: str = "") -> str:
        sender = self._sanitise_sender(sender)
        self._load(sender)
        parts = args.strip().split(maxsplit=1)
        command = parts[0].lower() if parts else ""

        if command == "add":
            return self._add(parts[1] if len(parts) > 1 else "", sender)
        elif command == "list":
            return self._list(parts[1] if len(parts) > 1 else "", sender)
        elif command == "done":
            return self._done(parts[1] if len(parts) > 1 else "", sender)
        elif command == "undo":
            return self._undo(parts[1] if len(parts) > 1 else "", sender)
        elif command == "remove":
            return self._remove(parts[1] if len(parts) > 1 else "", sender)
        elif command == "clear":
            return self._clear(sender)
        elif command == "projects":
            return self._projects(sender)
        elif command == "contexts":
            return self._contexts(sender)
        elif command == "report":
            return self._report(sender)

        return self.HELP_TEXT

    @staticmethod
    def _parse_priority(task: str) -> tuple[str | None, str]:
        match = re.match(r"^\(([A-Za-z])\)\s*", task)
        if match:
            return match.group(1).upper(), task[match.end():]
        return None, task

    @staticmethod
    def _parse_projects(task: str) -> list[str]:
        return re.findall(r"(?:^|\s)\+(\S+)", task)

    @staticmethod
    def _parse_contexts(task: str) -> list[str]:
        return re.findall(r"(?:^|\s)@(\S+)", task)

    def _add(self, task: str, sender: str) -> str:
        task = task.strip()
        if not task:
            return "Please provide a task. Usage: add <task>"
        priority, task = self._parse_priority(task)
        projects = self._parse_projects(task)
        contexts = self._parse_contexts(task)
        if sender not in self.todos:
            self.todos[sender] = []
        now = datetime.now(timezone.utc).isoformat()
        self.todos[sender].append({"task": task, "done": False, "priority": priority, "projects": projects, "contexts": contexts, "created_at": now})
        self._save(sender)
        return f"Added: {task}"

    def _sorted_items(self, sender: str) -> list[dict]:
        items = self.todos.get(sender, [])
        return sorted(items, key=lambda x: (x.get("priority") is None, x.get("priority") or ""))

    def _list(self, arg: str, sender: str) -> str:
        all_items = self._sorted_items(sender)
        filter_arg = arg.strip() if arg else ""
        filtered = []
        for i, item in enumerate(all_items, 1):
            if filter_arg:
                if filter_arg.startswith("@"):
                    context_filter = filter_arg.lstrip("@")
                    if context_filter not in item.get("contexts", []):
                        continue
                else:
                    project_filter = filter_arg.lstrip("+")
                    if project_filter not in item.get("projects", []):
                        continue
            filtered.append((i, item))
        if not filtered:
            return "No todos yet. Use 'add <task>' to create one."
        lines = []
        for i, item in filtered:
            status = "✓" if item["done"] else " "
            priority = f"({item['priority']}) " if item.get("priority") else ""
            lines.append(f"{i}. [{status}] {priority}{item['task']}")
        return "\n".join(lines)

    def _projects(self, sender: str) -> str:
        items = self.todos.get(sender, [])
        counts: dict[str, int] = {}
        for item in items:
            for project in item.get("projects", []):
                counts[project] = counts.get(project, 0) + 1
        if not counts:
            return "No projects found."
        lines = []
        for project in sorted(counts):
            lines.append(f"  +{project} ({counts[project]})")
        return "Projects:\n" + "\n".join(lines)

    def _contexts(self, sender: str) -> str:
        items = self.todos.get(sender, [])
        counts: dict[str, int] = {}
        for item in items:
            for context in item.get("contexts", []):
                counts[context] = counts.get(context, 0) + 1
        if not counts:
            return "No contexts found."
        lines = []
        for context in sorted(counts):
            lines.append(f"  @{context} ({counts[context]})")
        return "Contexts:\n" + "\n".join(lines)

    def _report(self, sender: str) -> str:
        items = self.todos.get(sender, [])
        completed = sum(1 for item in items if item.get("done"))
        open_count = len(items) - completed
        return f"{open_count} open, {completed} completed"

    def _done(self, arg: str, sender: str) -> str:
        try:
            num = int(arg)
        except ValueError:
            return "Invalid todo number."
        items = self._sorted_items(sender)
        if num < 1 or num > len(items):
            return "Invalid todo number."
        item = items[num - 1]
        item["done"] = True
        item["completed_at"] = datetime.now(timezone.utc).isoformat()
        self._save(sender)
        return f"Completed: {item['task']}"

    def _undo(self, arg: str, sender: str) -> str:
        try:
            num = int(arg)
        except ValueError:
            return "Invalid todo number."
        items = self._sorted_items(sender)
        if num < 1 or num > len(items):
            return "Invalid todo number."
        item = items[num - 1]
        if not item["done"]:
            return "Not marked as done."
        item["done"] = False
        item.pop("completed_at", None)
        self._save(sender)
        return f"Undone: {item['task']}"

    def _remove(self, arg: str, sender: str) -> str:
        try:
            num = int(arg)
        except ValueError:
            return "Invalid todo number."
        items = self._sorted_items(sender)
        if num < 1 or num > len(items):
            return "Invalid todo number."
        item = items[num - 1]
        self.todos[sender].remove(item)
        self._archive(sender, [item])
        self._save(sender)
        return f"Removed: {item['task']}"

    def _clear(self, sender: str) -> str:
        items = self.todos.get(sender, [])
        self._archive(sender, items)
        self.todos[sender] = []
        self._save(sender)
        return "All todos cleared."

    def _sender_path(self, sender: str) -> Path | None:
        if not self.data_dir:
            return None
        return self.data_dir / "todo" / f"{sender}.json"

    def _archive_path(self, sender: str) -> Path | None:
        if not self.data_dir:
            return None
        return self.data_dir / "todo" / f"{sender}-archive.json"

    def _archive(self, sender: str, items: list[dict]) -> None:
        path = self._archive_path(sender)
        if not path or not items:
            return
        now = datetime.now(timezone.utc).isoformat()
        for item in items:
            item["archived_at"] = now
        existing = []
        if path.exists():
            existing = json.loads(path.read_text())
        existing.extend(items)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(existing))

    def _load(self, sender: str) -> None:
        path = self._sender_path(sender)
        if path and path.exists():
            self.todos[sender] = json.loads(path.read_text())

    def _save(self, sender: str) -> None:
        path = self._sender_path(sender)
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(self.todos.get(sender, [])))
