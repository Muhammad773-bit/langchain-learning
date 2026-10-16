# agent.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

def load_csv(path):
    return pd.read_csv(path)

def ask_llm(question, df):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not found in .env file")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    prompt = PromptTemplate(
        input_variables=["question", "columns"],
        template="""
You are a Python pandas expert.

The dataframe is named df.
Columns are: {columns}

Question:
{question}

Return ONLY valid pandas code.
No explanation.
"""
    )

    final_prompt = prompt.format(
        question=question,
        columns=", ".join(df.columns)
    )

    response = llm.invoke(final_prompt)
    return response.content
