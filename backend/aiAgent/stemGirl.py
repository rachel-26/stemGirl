# backend/aiAgent/stemGirl.py

from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict, List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START, END

from backend.aiAgent.tools.addEvent import addEventTool
from backend.aiAgent.tools.listEvent import listEventsTool
from backend.aiAgent.mentorMatch import suggestMentors
from backend.aiAgent.opportunityFinder import findOpportunities
from backend.aiAgent.summarizer import summarizeResults


# TypedDict for structured state
class STEMGirlState(TypedDict):
    messages: List[str]
    response: str
    events: List[Dict]
    opportunities: List[Dict]
    mentors: str
    summary: str


# Initialize state
def create_initial_state() -> STEMGirlState:
    return STEMGirlState(
        messages=[], response="", events=[], opportunities=[], mentors="", summary=""
    )


# Core STEMGirl conversation
def stemGirlConversation(state: STEMGirlState) -> STEMGirlState:
    userMessage = state["messages"][-1]
    msg_lower = userMessage.lower()

    # Initialize LLM
    llm = init_chat_model(model="gpt-4o", model_provider="openai")

    # LLM prompt
    prompt = ChatPromptTemplate.from_template(
        """
    You are STEMGirl — an AI mentor guiding girls in STEM.
    You answer questions kindly, provide useful resources, and
    guide them to events, opportunities, or mentors when needed.

    User: {userMessage}
    STEMGirl:
    """
    )

    # Get LLM response
    response = llm.invoke(prompt.format(userMessage=userMessage))
    state["response"] = response.content


    # Handle tools
    if "add event" in msg_lower:
        state["events"].append(
            addEventTool(
                "Tech Girls Expo",
                "2025-11-01",
                "Dar es Salaam",
                "STEM Fair for students.",
            )
        )
    elif "list events" in msg_lower or "show events" in msg_lower:
        state["events"].extend(listEventsTool())

    if "mentor" in msg_lower:
        state["mentors"] = suggestMentors(userMessage)

    if "competition" in msg_lower or "opportunity" in msg_lower or "event" in msg_lower:
        state["opportunities"].extend(findOpportunities(userMessage))


    # Summarize conversation
    summary_prompt = f"Summarize the following STEMGirl conversation concisely:\n\n{state['response']}"
    state["summary"] = summarizeResults(summary_prompt)

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
    #state["messages"] = ["Can you suggest STEM competitions for girls?"]
    state["messages"].append("Can you suggest STEM competitions for girls?")

    state = stemGirlConversation(state)

    print("Response:", state["response"])
    print("Events:", state["events"])
    print("Opportunities:", state["opportunities"])
    print("Mentors:", state["mentors"])
    print("Summary:", state["summary"])
