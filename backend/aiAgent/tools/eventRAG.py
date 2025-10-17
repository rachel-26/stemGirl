# backend/aiAgent/tools/eventRAG.py
import json
import os,re
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

dataPath = os.path.join(os.path.dirname(__file__), "../data/events.json")


# Initialize embeddings and vector store
def createEventRag():
    if not os.path.exists(dataPath):
        return None

    with open(dataPath, "r") as f:
        events = json.load(f)

    if not events:
        return None

    # Combine event info for embeddings, include link
    eventTexts = [
        f"{e['name']} ({e['date']} at {e['location']}): {e['description']}\nLink: {e.get('link','')}"
        for e in events
    ]

    embeddings = OpenAIEmbeddings()
    vectorStore = FAISS.from_texts(eventTexts, embeddings)
    retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

    # Create RAG QA chain
    qaChain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o"),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return qaChain


# Function to query events
def queryEvents(question: str):
    qaChain = createEventRag()
    if not qaChain:
        return "No events available yet."

    result = qaChain.invoke({"query": question})
    answer = result.get("result", "")

    # Also attach links if present in source documents
    sources = result.get("source_documents", [])
    links = []
    for doc in sources:
        text = doc.page_content
        # Extract URL from text
        linkMatch = re.search(r"Link:\s*(https?://\S+)", text)
        if linkMatch:
            links.append(linkMatch.group(1))

    if links:
        answer += "\n\nLinks:\n" + "\n".join(links)

    return answer if answer else "I couldn't find any matching events."
