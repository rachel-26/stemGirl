import json
import os
from tempfile import NamedTemporaryFile
import shutil


def addEventTool(name, date, location, description, link=""):
    # Ensure path is absolute and consistent
    DATA_PATH = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "events.json")
    )
    print("Saving event to:", os.path.abspath(DATA_PATH))

    # Ensure folder exists
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    # Ensure file exists
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Load safely
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            events = json.load(f)
            if not isinstance(events, list):
                events = []
        except json.JSONDecodeError:
            events = []

    # Add event
    newEvent = {
        "name": name,
        "date": date,
        "location": location,
        "description": description,
        "link": link
    }
    events.append(newEvent)

    # Atomic write (avoid partial writes)
    tmp_file = NamedTemporaryFile(
        "w", delete=False, dir=os.path.dirname(DATA_PATH), encoding="utf-8"
    )
    json.dump(events, tmp_file, indent=4, ensure_ascii=False)
    tmp_file.close()
    shutil.move(tmp_file.name, DATA_PATH)

    return newEvent
