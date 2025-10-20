# backend/aiAgent/stemGirl.py
from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict, List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from datetime import datetime
import re, json

# Import tools
from backend.aiAgent.tools.addEvent import addEventTool
from backend.aiAgent.tools.listEvent import listEventsTool
from backend.aiAgent.mentorMatch import suggestMentors
from backend.aiAgent.opportunityFinder import findOpportunities
from backend.aiAgent.summarizer import summarizeResults
from backend.aiAgent.tools.eventRAG import queryEvents
from backend.api.state import userContext


# -----------------------------
# TypedDict for structured state
# -----------------------------
class STEMGirlState(TypedDict):
    messages: List[str]
    response: str
    events: List[str]
    opportunities: List[Dict]
    mentors: str
    summary: str


# -----------------------------
# Initialize state
# -----------------------------
def create_initial_state() -> STEMGirlState:
    return STEMGirlState(
        messages=[], response="", events=[], opportunities=[], mentors="", summary=""
    )


# -----------------------------
# Helper: parse events from STEMGirl text
# -----------------------------
def parse_events_from_text(text: str) -> List[Dict]:
    events = []
    lines = text.split("\n")
    for line in lines:
        m = re.match(r"\d+\.\s\*\*(.+?)\*\*\s*(?:\((.*?)\))?:\s*(.+)", line)
        if m:
            name = m.group(1).strip()
            date = m.group(2).strip() if m.group(2) else "TBD"
            description = m.group(3).strip()
            location = "Online"

            # Extract Link if present
            linkMatch = re.search(r"Link:\s*(https?://\S+)", line)
            link = linkMatch.group(1).strip() if linkMatch else ""

            events.append(
                {
                    "name": name,
                    "date": date,
                    "location": location,
                    "description": description,
                    "link": link,
                }
            )
    return events


# -----------------------------
# Core STEMGirl conversation
# -----------------------------
def stemGirlConversation(state: STEMGirlState) -> STEMGirlState:
    userMessage = state["messages"][-1] if state["messages"] else ""
    msgLower = userMessage.lower()
    userInterest = userContext.get("interest", "STEM")
    print(f"The Current user interest :{userInterest}")

    # Initialize LLM
    llm = init_chat_model(model="gpt-4o", model_provider="openai")
    today = datetime.now().strftime("%B %d, %Y")

    # Prompt
    promptText = f""" The user is interested in {userInterest}
You are STEMGirl — an AI mentor guiding girls in STEM.
You answer questions kindly, provide useful resources, and
guide them to events, opportunities, or mentors when needed relevant to their interest.

Today is {today}. When listing events, always give upcoming events (dates after today) in the future, not past events.
Include event name, exact date (month, day, year), and optionally location.
Format: Output ALL events in a JSON array, even if there is only one event.
    "name": "Event Name",
    "date": "Month Day, Year",
    "location": "City or Online",
    "description": "Short description"
    "link":"URL"

Make as many as you can.

User: {userMessage}
STEMGirl:
"""
    prompt = ChatPromptTemplate.from_template(promptText)

    # Get LLM response
    response = llm.invoke(prompt.format(userMessage=userMessage))
    state["response"] = response.content

    # -----------------------------
    # Handle events automatically
    # -----------------------------
    if "event" in msgLower or "add event" in msgLower or "upcoming events" in msgLower:
        eventsToAdd = []

        # Try to extract JSON inside ```json ... ```
        jsonMatch = re.search(
            r"```json(.*?)```", state["response"], re.DOTALL | re.IGNORECASE
        )
        if jsonMatch:
            jsonText = jsonMatch.group(1).strip()
        else:
            arrayMatch = re.search(r"\[.*\]", state["response"], re.DOTALL)
            jsonText = arrayMatch.group(0).strip() if arrayMatch else None

        if jsonText:
            try:
                eventsToAdd = json.loads(jsonText)
                if isinstance(eventsToAdd, dict):
                    eventsToAdd = [eventsToAdd]
            except json.JSONDecodeError:
                print("JSON decode error:", re)
                print("JSON text was:", jsonText)
                eventsToAdd = []

            if eventsToAdd:
                savedEvents = [
                    addEventTool(
                        e.get("name", "Unnamed Event"),
                        e.get("date", "TBD"),
                        e.get("location", "Online"),
                        e.get("description", ""),
                        e.get("link", ""),
                    )
                    for e in eventsToAdd
                ]
                state["events"].extend(
                    [f"{e['name']} saved to JSON!" for e in savedEvents]
                )

        else:
            state["events"].append(
                "Failed to parse events from LLM output. Ensure the response is valid JSON."
            )

            print("Extracted JSON text:\n", jsonText)
            print("Parsed events:\n", eventsToAdd)

        # Also query RAG for event questions
        ragResponse = queryEvents(userMessage)
        if ragResponse:
            state["response"] += f"\n\n{ragResponse}"

    # -----------------------------
    # List events
    # -----------------------------
    elif "list events" in msgLower or "show events" in msgLower:
        eventText = listEventsTool()
        state["events"].append(eventText)

    # -----------------------------
    # Handle mentors
    # -----------------------------
    if "mentor" in msgLower:
        state["mentors"] = suggestMentors(userMessage)

    # -----------------------------
    # Handle opportunities
    # -----------------------------
    if "competition" in msgLower or "opportunity" in msgLower:
        state["opportunities"].extend(findOpportunities(userMessage))

    # -----------------------------
    # Summarize conversation
    # -----------------------------
    summaryPrompt = f"Summarize the following STEMGirl conversation concisely:\n\n{state['response']}"
    state["summary"] = summarizeResults(summaryPrompt)

    return state


# -----------------------------
# Create LangGraph agent
# -----------------------------
def createStemGirlAgent():
    graph = StateGraph(STEMGirlState)
    graph.add_node("chat", stemGirlConversation)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)
    return graph.compile()


# -----------------------------
# Test run
# -----------------------------
if __name__ == "__main__":
    state = create_initial_state()
    state["messages"].append("Can you suggest STEM competitions and events for girls?")
    state = stemGirlConversation(state)

    print("Response:\n", state["response"])


# print("\nEvents:\n", state["events"])
# print("\nOpportunities:\n", state["opportunities"])
# print("\nMentors:\n", state["mentors"])
# print("\nSummary:\n", state["summary"])
