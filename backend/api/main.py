from aiAgent.stemGirl import createStemGirlAgent


def runTest():
    graph = createStemGirlAgent()
    state = {"message": "Can you list STEM events?"}
    result = graph.invoke(state)
    print("STEMGirl says:", result["response"])


if __name__ == "__main__":
    runTest()
