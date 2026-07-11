# backend/app/services/ingestion/embedder.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.services.core.interfaces import EmbeddingService
from pydantic import SecretStr

from typing import List

class GeminiEmbedder(EmbeddingService):
    def __init__(self, api_key: SecretStr):
        self.embedder = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            api_key=api_key.get_secret_value()
        )
    
    async def embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.embed_documents(texts)