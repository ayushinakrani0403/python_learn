from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def ask_llm(question: str) -> str:
    response = llm.invoke(question)
    return response.content
