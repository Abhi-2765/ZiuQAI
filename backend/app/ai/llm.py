# llm.py

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.core.config import settings

class LLM:
    def __init__(self, model_name: str = "gemini-2.5-flash", embedding_model_name: str = "gemini-embedding-001"):
        self.llm = GoogleGenerativeAI(model_name=model_name, api_key=settings.GOOGLE_API_KEY)
        self.embedding_model = GoogleGenerativeAIEmbeddings(model_name=embedding_model_name, api_key=settings.GOOGLE_API_KEY)
    
    def get_llm(self):
        return self.llm
    
    def get_embedding_model(self):
        return self.embedding_model

llm = LLM("gemini-3.0-flash", "gemini-embedding-001")
