# backend/api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from backend.aiAgent.stemGirl import (
    createStemGirlAgent,
    create_initial_state,
    stemGirlConversation,
)
import json, os
from backend.aiAgent.tools.addEvent import addEventTool

addEventTool(
    name="AI Bootcamp for Girls",
    date="November 10, 2025",
    location="Online",
    description="A virtual AI learning experience for girls interested in machine learning.",
    link="https://example.com",
)

app = FastAPI(title="STEMGirl API")

EVENTS_PATH = os.path.join(os.path.dirname(__file__), "../aiAgent/data/events.json")


# Initialize the agent once
graph = createStemGirlAgent()


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    events: List[str]
    opportunities: List[Dict]
    mentors: str
    summary: str


# API endpoints
@app.get("/")
def root():
    return {"message": "Welcome to STEMGirl API. Use /chat endpoint to interact."}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """
    Send a message to STEMGirl agent and get the response along with events,
    opportunities, mentors, and a summary.
    """
    state = create_initial_state()
    state["messages"].append(req.message)

    # Run the agent
    result = graph.invoke(state)

    # Ensure opportunities is always a list of dicts
    normalizedOpportunities = []
    for o in state["opportunities"]:
        if isinstance(o, dict):
            normalizedOpportunities.append(o)
        elif isinstance(o, str):
            normalizedOpportunities.append({"title": o})
    result["opportunities"] = normalizedOpportunities

    # Ensure summary is a string
    if isinstance(state["summary"], dict) and "summary" in result["summary"]:
        result["summary"] = result["summary"]["summary"]
    else:
        result["summary"] = str(result["summary"])

    

    # Return structured response
    #state = stemGirlConversation(state)
    return ChatResponse(
        response=result["response"],
        events=result["events"],
        opportunities=result["opportunities"],
        mentors=result["mentors"],
        summary=result["summary"],
    )


@app.get("/events")
def get_events():
    """
    Return all saved STEM events from events.json.
    """
    if not os.path.exists(EVENTS_PATH):
        return {"events": []}

    with open(EVENTS_PATH, "r") as f:
        events = json.load(f)

    return {"events": events}
