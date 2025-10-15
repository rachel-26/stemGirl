from fastapi import FastAPI
from ..aiAgent.stemGirl import stemGirlConversation

app = FastAPI()
graph = stemGirlConversation()

@app.get("/")
def home():
    return {"message": "Welcome to STEM Girl Connect API"}

@app.post("/chat/")
def chat_with_agent(message: str):
    state = {"message": message}
    result = graph.invoke(state)
    return {"reply": result["response"]}
