from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def suggestMentors(query: str):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("""
    Suggest online mentorship programs, women in STEM networks,
    and accessible mentors based on this user interest:
    "{query}"

    Include at least 3 suggestions with short descriptions and URLs.
    """)
    response = llm.invoke(prompt.format(query=query))
    return {"mentors": response.content}
