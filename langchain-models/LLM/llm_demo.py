# langchain_models/LLM/llm_demo.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

res = llm.invoke("What is LangChain?")
print(res.content)
