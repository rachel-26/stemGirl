# backend/aiAgent/tools/listEvent.py
import json, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/events.json")


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
