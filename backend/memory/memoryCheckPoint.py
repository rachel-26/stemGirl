# backend/memory/memoryCheckPoint.py
import json, os

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "../aiAgent/data/memory.json")


def saveMemory(key, value):
    memory = loadMemory()
    memory[key] = value
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=4)


def loadMemory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)
