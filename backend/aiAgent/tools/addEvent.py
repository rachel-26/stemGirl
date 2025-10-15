# backend/aiAgent/tools/addEvent.py
import json, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/events.json")


def addEventTool(name, date, location, description):
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)

    with open(DATA_PATH, "r") as f:
        events = json.load(f)

    events.append(
        {"name": name, "date": date, "location": location, "description": description}
    )

    with open(DATA_PATH, "w") as f:
        json.dump(events, f, indent=4)

    return f"Event '{name}' added successfully!"
