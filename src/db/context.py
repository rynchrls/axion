import json
import os


def getUserContext(username: str):
    try:
        with open("context.json", "r") as f:
            data = json.load(f)
        return data.get(username, [])[-25:]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def saveUserContext(username: str, role: str, content: str):
    data = {}
    with open("context.json", "r") as f:
        data = json.load(f)

    if username not in data:
        data[username] = []

    data[username].append({"role": role, "content": content})

    with open("context.json", "w") as f:
        json.dump(data, f, indent=4)
