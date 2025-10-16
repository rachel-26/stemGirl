from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict, List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from datetime import datetime
import re,json

# Import tools
from backend.aiAgent.tools.addEvent import addEventTool
from backend.aiAgent.tools.listEvent import listEventsTool
from backend.aiAgent.mentorMatch import suggestMentors
from backend.aiAgent.opportunityFinder import findOpportunities
from backend.aiAgent.summarizer import summarizeResults
from backend.aiAgent.tools.eventRAG import queryEvents


# TypedDict for structured state
class STEMGirlState(TypedDict):
    messages: List[str]  # must be a list
    response: str
    events: List[str]  # store text confirmations
    opportunities: List[Dict]
    mentors: str
    summary: str


# Initialize state
def create_initial_state() -> STEMGirlState:
    return STEMGirlState(
        messages=[], response="", events=[], opportunities=[], mentors="", summary=""
    )


# Helper: parse events from STEMGirl text
def parse_events_from_text(text: str) -> List[Dict]:
    """
    Extract events from STEMGirl text output.
    Returns a list of dicts with name, date, location, description.
    """
    events = []
    lines = text.split("\n")
    for line in lines:
        # Match lines like: 1. **Event Name (Date)**: Description
        m = re.match(r"\d+\.\s\*\*(.+?)\*\*\s*(?:\((.*?)\))?:\s*(.+)", line)
        if m:
            name = m.group(1).strip()
            date = m.group(2).strip() if m.group(2) else "TBD"
            description = m.group(3).strip()
            location = (
                "Online"  # Default, since most generated text does not include location
            )
            events.append(
                {
                    "name": name,
                    "date": date,
                    "location": location,
                    "description": description,
                }
            )
    return events


# Core STEMGirl conversation
def stemGirlConversation(state: STEMGirlState) -> STEMGirlState:
    # Take the latest user message
    if not state["messages"]:
        userMessage = ""
    else:
        userMessage = state["messages"][-1]

    msgLower = userMessage.lower()

    # Initialize LLM
    llm = init_chat_model(model="gpt-4o", model_provider="openai")

    today = datetime.now().strftime("%B %d, %Y")

    # Prompt
    promptText = f"""
You are STEMGirl — an AI mentor guiding girls in STEM.
You answer questions kindly, provide useful resources, and
guide them to events, opportunities, or mentors when needed.

Today is {today}. When listing events, always give upcoming events (dates after today) in the future, not past events.
Include event name, exact date (month, day, year), and optionally location.
Format: Output ALL events in a JSON array, even if there is only one event.
    "name": "Event Name",
    "date": "Month Day, Year",
    "location": "City or Online",
    "description": "Short description"

Make as many as you can.

User: {userMessage}
STEMGirl:
"""
    prompt = ChatPromptTemplate.from_template(promptText)

    # Get LLM response
    response = llm.invoke(prompt.format(userMessage=userMessage))
    state["response"] = response.content

    # --- 🔹 Handle tools based on user intent ---

        # Add events automatically from STEMGirl output
    if ("event" in msgLower or "add event" in msgLower or "upcoming events" in msgLower):
    # --- NEW: parse JSON directly from LLM output ---
        try:
            # Extract only the JSON block from the response (between ```json and ```)
            jsonMatch = re.search(r"```json(.*?)```", state["response"], re.DOTALL)
            if jsonMatch:
                jsonText = jsonMatch.group(1).strip()
            else:
                jsonText = state["response"].strip()

            eventsToAdd = json.loads(jsonText)
        except json.JSONDecodeError:
            eventsToAdd = []
        state["events"].append("Failed to parse events from LLM output. Ensure the response is valid JSON.")

        if isinstance(eventsToAdd, dict):
            eventsToAdd = [eventsToAdd]

        savedCount = 0
        for e in eventsToAdd:
            addEventTool(
                e["name"], e["date"], e.get("location", "Online"), e.get("description", "")
        )
        savedCount += 1

        if savedCount > 0:
            state["events"].append(f"{savedCount} events saved to JSON!")

        # Use RAG to answer event-related questions
        ragResponse = queryEvents(userMessage)
        if ragResponse:
            state["response"] += f"\n\n{ragResponse}"

    # List events
    elif "list events" in msgLower or "show events" in msgLower:
        eventText = listEventsTool()
        state["events"].append(eventText)

    # Handle mentors
    if "mentor" in msgLower:
        state["mentors"] = suggestMentors(userMessage)

    # Handle opportunities
    if "competition" in msgLower or "opportunity" in msgLower:
        state["opportunities"].extend(findOpportunities(userMessage))

    # Summarize conversation
    summaryPrompt = f"Summarize the following STEMGirl conversation concisely:\n\n{state['response']}"
    state["summary"] = summarizeResults(summaryPrompt)

    return state


# Create LangGraph agent
def createStemGirlAgent():
    graph = StateGraph(STEMGirlState)
    graph.add_node("chat", stemGirlConversation)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)
    return graph.compile()


# Test run
if __name__ == "__main__":
    state = create_initial_state()
    state["messages"].append("Can you suggest STEM competitions and events for girls?")
    state = stemGirlConversation(state)

    print("Response:\n", state["response"])
    print("\nEvents:\n", state["events"])
    print("\nOpportunities:\n", state["opportunities"])
    print("\nMentors:\n", state["mentors"])
    print("\nSummary:\n", state["summary"])
