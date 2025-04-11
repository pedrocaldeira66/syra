# syra/core/memory/memory_index.py

import os
import json
import difflib
from syra.config import config
from syra.core.memory.memory import get_memory

INDEX_LIMIT = int(config.get("memory", {}).get("index_limit", 50))

def search_memory(query, max_results=3, threshold=0.5):
    memory = get_memory()
    if not memory:
        return []

    recent = memory[-INDEX_LIMIT:]
    scored = []

    for entry in recent:
        combined = entry["user"] + " " + entry["syra"]
        ratio = difflib.SequenceMatcher(None, query.lower(), combined.lower()).ratio()
        if ratio >= threshold:
            scored.append((ratio, entry))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [match[1] for match in scored[:max_results]]

def summarize_results(results):
    return "\n".join([f"User: {r['user']}\nSYRA: {r['syra']}" for r in results])