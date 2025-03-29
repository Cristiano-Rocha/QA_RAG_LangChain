import os
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model=os.getenv('GEMINI_MODEL'),
    temperature=0,
    max_tokens=None,
    max_retries=2,
    api_key=os.getenv('GOOGLE_API_KEY')
)