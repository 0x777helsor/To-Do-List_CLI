#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_STORE = Path.home() / ".task_cli_tasks.json"


def load_tasks(store: Path) -> list[dict]:
    if not store.exists():
        return []
    try:
        data = json.loads(store.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        raise SystemExit(f"Could not read task store: {store}")


def save_tasks(store: Path, tasks: list[dict]) -> None:
    try:
        store.parent.mkdir(parents=True, exist_ok=True)
        store.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Could not save task store: {exc}")


def next_id(tasks: list[dict]) -> int:
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(store: Path, title: str) -> None:
    title = title.strip()
    if not title:
        raise SystemExit("A task description cannot be empty.")
    tasks = load_tasks(store)
    task = {"id": next_id(tasks), "title": title}
    tasks.append(task)
    save_tasks(store, tasks)
    print(f'Added task {task["id"]}: {task["title"]}')


def list_tasks(store: Path) -> None:
    tasks = load_tasks(store)
    if not tasks:
        print("No tasks yet. Add one with: task_cli.py add Buy groceries")
        return
    print("\033[1;32mTasks\033[0m")
    print("-----")
    for task in tasks:
        print(f'{task["id"]:>3}. {task["title"]}')


def delete_task(store: Path, task_id: int) -> None:
    tasks = load_tasks(store)
    kept = [task for task in tasks if task["id"] != task_id]
    if len(kept) == len(tasks):
        raise SystemExit(f"No task with ID {task_id}.")
    save_tasks(store, kept)
    print(f"Deleted task {task_id}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="Add, list, and delete items from a persistent text task list.",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=DEFAULT_STORE,
        help=f"JSON task file (default: {DEFAULT_STORE})",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add a task")
    add.add_argument("title", nargs="+", help="Task description")
    commands.add_parser("list", aliases=["view"], help="View all tasks")
    delete = commands.add_parser("delete", aliases=["remove", "rm"], help="Delete a task by ID")
    delete.add_argument("id", type=int, help="ID shown by the list command")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    store: Path = args.store.expanduser()
    if args.command == "add":
        add_task(store, " ".join(args.title))
    elif args.command in {"list", "view"}:
        list_tasks(store)
    elif args.command in {"delete", "remove", "rm"}:
        delete_task(store, args.id)


if __name__ == "__main__":
    main()
