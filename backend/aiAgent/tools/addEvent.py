# backend/aiAgent/tools/addEvent.py
import json, os


def addEventTool(name, date, location, description):
    import json, os

    DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/events.json")

    # Ensure file exists
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)

    # Load existing events safely
    with open(DATA_PATH, "r") as f:
        try:
            events = json.load(f)
        except json.JSONDecodeError:
            events = []

    # Add new event
    events.append(
        {"name": name, "date": date, "location": location, "description": description}
    )

    # Save back to file
    with open(DATA_PATH, "w") as f:
        json.dump(events, f, indent=4)

    return f"Event '{name}' added successfully!"
