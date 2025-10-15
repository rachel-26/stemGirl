import os
from dotenv import load_dotenv
from backend.aiAgent.stemGirl import stemGirlConversation, create_initial_state

# Load API key
load_dotenv()

# Initialize the state
state = create_initial_state()
state["message"] = "hi am looking for AI bootcamp or workshop opportunities in Africa, can you please help me?"

# Run the STEMGirl conversation
state = stemGirlConversation(state)

# Print the results
print("STEMGirl says:", state["response"])
print("Opportunities:", state["opportunities"])
print("Mentors:", state["mentors"])
print("Summary:", state["summary"])
