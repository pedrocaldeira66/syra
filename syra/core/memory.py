import os
import json
from dotenv import load_dotenv

load_dotenv()

MEMORY_BACKEND = os.getenv("MEMORY_BACKEND", "file")
MEMORY_PATH = os.getenv("MEMORY_PATH", "./data/memory.json")

class MemoryStore:
    def __init__(self):
        self.memory = []
        if MEMORY_BACKEND == "file":
            try:
                with open(MEMORY_PATH, "r") as f:
                    self.memory = json.load(f)
                print(f"[MEMORY] Loaded memory from {MEMORY_PATH}")
            except FileNotFoundError:
                print(f"[MEMORY] No existing memory found, starting fresh.")
            except json.JSONDecodeError:
                print(f"[MEMORY] Corrupted memory file. Starting fresh.")

    def update(self, perception):
        self.memory.append({"perception": perception})

    def log_interaction(self, perception, plan, action):
        self.memory.append({
            "perception": perception,
            "plan": plan,
            "action": action
        })

    def save(self):
        if MEMORY_BACKEND == "file":
            os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
            with open(MEMORY_PATH, "w") as f:
                json.dump(self.memory, f, indent=2)

    def __str__(self):
        return json.dumps(self.memory[-5:], indent=2)  # Last 5 entries for debug

def initialize(config):
    print(f"[INIT] Memory system initialized with backend: {MEMORY_BACKEND}")
