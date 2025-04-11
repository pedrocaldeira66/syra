# syra/core/memory/knowledge_store.py

import os
import json
from syra.config import config

KNOWLEDGE_PATH = config.get("memory", {}).get("knowledge_path", "./data/knowledge.json")

def _ensure_store():
    if not os.path.exists(KNOWLEDGE_PATH):
        os.makedirs(os.path.dirname(KNOWLEDGE_PATH), exist_ok=True)
        with open(KNOWLEDGE_PATH, "w") as f:
            json.dump({}, f)

def load_knowledge():
    _ensure_store()
    with open(KNOWLEDGE_PATH, "r") as f:
        return json.load(f)

def save_knowledge(data):
    _ensure_store()
    with open(KNOWLEDGE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def update_fact(topic, fact):
    knowledge = load_knowledge()
    knowledge[topic] = fact
    save_knowledge(knowledge)

def get_fact(topic):
    return load_knowledge().get(topic)

def forget(topic):
    knowledge = load_knowledge()
    if topic in knowledge:
        del knowledge[topic]
        save_knowledge(knowledge)