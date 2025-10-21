# backend/api/chatAgent.py
from fastapi import APIRouter
from pydantic import BaseModel
import os
from openai import OpenAI

# Initialize router
router = APIRouter()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Request model
class ChatRequest(BaseModel):
    message: str


@router.post("/chatAgent")
async def chat_agent(request: ChatRequest):
    """
    A friendly AI agent that chats normally with the user.
    It also knows that events related to their interest
    are already generated in the events panel.
    """
    user_message = request.message

    system_prompt = (
        "You are STEMGirl, a friendly AI assistant helping girls explore opportunities "
        "in STEM and technology. You already know the user's STEM interest and that "
        "related events have been generated in the events panel. "
        "Chat naturally like ChatGPT — give helpful, engaging, and friendly answers."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.8,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("ChatAgent Error:", e)
        reply = f"Sorry, I couldn’t connect to the AI server right now.\n\nDetails: {str(e)}"

    return {"response": reply}
