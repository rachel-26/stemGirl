#from langchain.chat_models import ChatOpenAI
from langchain.chat_models import init_chat_model


def summarizeResults(text: str):
    #llm = ChatOpenAI(model="gpt-4o-mini")
    llm = init_chat_model(model = "gpt-4o", model_provider = "openai")

    prompt = f"Summarize the following results into 3 concise bullet points:\n\n{text}"
    summary = llm.invoke(prompt)
    return {"summary": summary.content}
