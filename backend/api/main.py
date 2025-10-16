from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.aiAgent.stemGirl import createStemGirlAgent, create_initial_state

# Initialize FastAPI app
app = FastAPI(title="STEMGirl API", version="1.0")

# Create LangGraph agent once
graph = createStemGirlAgent()


# Define input schema for API requests
class ChatRequest(BaseModel):
    message: str


# Define response schema (optional but clean)
class ChatResponse(BaseModel):
    response: str
    events: list
    opportunities: list
    mentors: str
    summary: str


@app.post("/chat", response_model=ChatResponse)
def chat_with_stemgirl(request: ChatRequest):
    try:
        # Create a new conversation state
        state = create_initial_state()
        state["messages"].append(request.message)

        # Run the agent
        result = graph.invoke(state)

        # Return response as JSON
        return ChatResponse(
            response=result["response"],
            events=result["events"],
            opportunities=result["opportunities"],
            mentors=result["mentors"],
            summary=result["summary"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional: Keep your test run for CLI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
