#from langgraph.graph import init_chat_model
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

def findOpportunities(query: str):
    """
    Generates STEM opportunities, competitions, or workshops for girls.
    """

    llm = init_chat_model(model="gpt-4o", model_provider="openai")

    # Prompt the model to generate 3-5 opportunities based on the query
    prompt = ChatPromptTemplate.from_template("""
    You are an AI assistant that provides STEM opportunities for girls.
    Based on this query: "{query}", list 3-5 online or global STEM workshops,
    competitions, or programs. For each opportunity, include:
    - Title
    - Short description
    - Link (if available)
    """)

    response = llm.invoke(prompt.format(query=query))

    # Return as a dictionary
    return {"opportunities": response.content}
