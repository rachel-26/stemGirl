from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from .opportunityFinder import findOpportunities
from .mentorMatch import suggestMentors
from .summarizer import summarizeResults
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from aiAgent.tools.addEvent import addEventTool
from aiAgent.tools.listEvent import listEventsTool
from aiAgent.mentorMatch import suggestMentors
from aiAgent.opportunityFinder import findOpportunities
from aiAgent.summarizer import summarizeResults


class STEMGirlState(TypedDict):
    message: str
    response: str
    opportunities: List[Dict]
    mentors: str
    summary: str

def create_initial_state() -> STEMGirlState:
    return STEMGirlState(
        message="",
        response="",
        opportunities=[],
        mentors="",
        summary=""
    )

def stemGirlConversation(state: STEMGirlState) -> STEMGirlState:
    userMessage = state["message"]
    llm = init_chat_model(model="gpt-4o", model_provider="openai")

    prompt = ChatPromptTemplate.from_template("""
    You are STEMGirl — an AI mentor guiding girls in STEM.
    You answer questions kindly, provide useful resources, and
    guide them to opportunities or mentors when needed.

    User: {userMessage}
    STEMGirl:
    """)

    response = llm.invoke(prompt.format(userMessage=userMessage))
    state["response"] = response.content

    if "competition" in userMessage.lower() or "event" in userMessage.lower():
        state["opportunities"].extend(findOpportunities(userMessage))
    elif "mentor" in userMessage.lower():
        state["mentors"] = suggestMentors(userMessage)

    summary_prompt = f"Summarize the following STEMGirl conversation concisely:\n\n{state['response']}"
    state["summary"] = summarizeResults(summary_prompt)

    return state

if __name__ == "__main__":
    state = create_initial_state()
    state["message"] = "Can you suggest STEM competitions for girls?"
    state = stemGirlConversation(state)
    print("Response:", state["response"])
    print("Opportunities:", state["opportunities"])
    print("Mentors:", state["mentors"])
    print("Summary:", state["summary"])
