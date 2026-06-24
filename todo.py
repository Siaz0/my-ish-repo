#!/usr/bin/env python3

import sys
import os
import json

FILE = "todos.json"

def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)

todos = load()

if len(sys.argv) > 1:
    cmd, *args = sys.argv[1:]

    if cmd == "add":
        task = " ".join(args)
        todos.append(task)
        save(todos)
        print("Task added.")

    elif cmd == "list":
        if not todos:
            print("No tasks found.")
        else:
            for i, task in enumerate(todos, 1):
                print(f"{i}. {task}")

    elif cmd == "clear":
        save([])
        print("All tasks cleared.")

    else:
        print("Unknown command.")

else:
    print("Usage:")
    print("  todo add 'task'")
    print("  todo list")
    print("  todo clear")
