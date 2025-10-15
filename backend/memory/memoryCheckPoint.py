import os
import json
from typing import Dict


MEMORY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "aiAgent", "data", "events.json"
)


def _ensure_memory_file():
    dirPath = os.path.dirname(MEMORY_PATH)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath, exist_ok=True)


if not os.path.exists(MEMORY_PATH):
    with open(MEMORY_PATH, "w") as f:
        json.dump({}, f)


def saveMemory(sessionId: str, data: Dict):
    _ensure_memory_file()
    with open(MEMORY_PATH, "r") as f:
        mem = json.load(f)
    mem[sessionId] = data
    with open(MEMORY_PATH, "w") as f:
        json.dump(mem, f, indent=2)
    return True


def loadMemory(sessionId: str):
   _ensure_memory_file()
