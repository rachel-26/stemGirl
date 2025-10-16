# backend/aiAgent/tools/listEvent.py
import json, os

# DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/events.json")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
DATA_PATH = os.path.join(DATA_DIR, "events.json")
os.makedirs(DATA_DIR, exist_ok=True)


def listEventsTool():
    if not os.path.exists(DATA_PATH):
        return "No events found yet."

    with open(DATA_PATH, "r") as f:
        events = json.load(f)

    if not events:
        return "No events available right now."

    text = "Here are the current STEM events:\n"
    for e in events:
        text += f"- {e['name']} ({e['date']} at {e['location']})\n"
    return text
