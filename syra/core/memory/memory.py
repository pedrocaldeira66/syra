import os
import json
from datetime import datetime
from syra.config import load_config

config = load_config()
backend = config.get("memory", {}).get("backend", "file")
memory_path = config.get("memory", {}).get("path", "./data/memory.json")

_memory_buffer = []

def _ensure_file_exists():
    if not os.path.exists(memory_path):
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        with open(memory_path, "w") as f:
            json.dump([], f)

def save_interaction(user_input, response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "syra": response
    }

    if backend == "file":
        _ensure_file_exists()
        try:
            with open(memory_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(entry)

        with open(memory_path, "w") as f:
            json.dump(data, f, indent=2)

    elif backend == "inmem":
        _memory_buffer.append(entry)

    elif backend == "sqlite":
        print("[MEMORY] SQLite backend not yet implemented.")
    else:
        print(f"[MEMORY] Unknown memory backend: {backend}")

def get_memory():
    if backend == "file":
        _ensure_file_exists()
        try:
            with open(memory_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    elif backend == "inmem":
        return _memory_buffer
    else:
        return []