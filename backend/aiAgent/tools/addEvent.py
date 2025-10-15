import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/events.json")

def addEvent(event):
    """Add a new STEM event to the JSON store."""
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)

    with open(DATA_PATH, "r") as f:
        events = json.load(f)

    events.append(event)

    with open(DATA_PATH, "w") as f:
        json.dump(events, f, indent=2)

    return {"status": "success", "message": "Event added successfully!"}
