from backend.aiAgent.stemGirl import createStemGirlAgent,create_initial_state



def runTest():
    graph = createStemGirlAgent()
    state = create_initial_state()               # ✅ ensures all keys exist
    state["messages"].append("Can you list STEM events?")
    result = graph.invoke(state)
    print("STEMGirl says:", result["response"])



if __name__ == "__main__":
    runTest()
