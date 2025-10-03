#!/usr/bin/env python3
import sys, os, json
FILE = "todos.json"

def load():
    return json.load(open(FILE)) if os.path.exists(FILE) else []

def save(todos):
    json.dump(todos, open(FILE, "w"))

todos = load()

if len(sys.argv) > 1:
    cmd, *args = sys.argv[1:]
    if cmd == "add":
        todos.append(" ".join(args))
        save(todos)
        print("b        for i, t in enumerate(todos, 1):
            print(f"{i}. {t}")
    elif cmd == "clear":
    else:
        print("Unknown command")
else:
    print("Usage: todo add 'task' | todo list | todo clear")        save([])
        print("p
