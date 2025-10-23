from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Allow frontend to fetch from any origin (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Absolute path to your JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.path.join(BASE_DIR, "aiAgent/data/events.json")
SAVED_EVENTS_FILE = os.path.join(BASE_DIR, "aiAgent/data/savedEvents.json")


@app.get("/getEvents")
async def get_events():
    if not os.path.exists(EVENTS_FILE):
        return JSONResponse([])
    with open(EVENTS_FILE, "r") as f:
        getEvents = json.load(f)
    return JSONResponse(getEvents)


@app.get("/saved-events")
async def get_saved_events():
    if not os.path.exists(SAVED_EVENTS_FILE):
        return JSONResponse([])
    with open(SAVED_EVENTS_FILE, "r") as f:
        saved_events = json.load(f)
    return JSONResponse(saved_events)
