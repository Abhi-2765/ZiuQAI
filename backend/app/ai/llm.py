# llm.py

from abc import ABC, abstractmethod
from typing import Any
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.core.config import settings

class ILLMProvider(ABC):
    @abstractmethod
    def get_llm(self) -> Any:
        pass

    @abstractmethod
    def get_embeddings(self) -> Any:
        pass

class GoogleAIProvider(ILLMProvider):
    def __init__(self, model_name: str, embedding_model_name: str):
        self._llm = GoogleGenerativeAI(
            model=model_name, 
            google_api_key=settings.GOOGLE_API_KEY
        )
        self._embeddings = GoogleGenerativeAIEmbeddings(
            model=embedding_model_name, 
            google_api_key=settings.GOOGLE_API_KEY
        )

    def get_llm(self) -> GoogleGenerativeAI:
        return self._llm

    def get_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        return self._embeddings

class LLMFactory:
    @staticmethod
    def get_provider(provider_type: str = "google") -> ILLMProvider:
        if provider_type == "google":
            return GoogleAIProvider(
                model_name="gemini-1.5-flash", 
                embedding_model_name="models/embedding-001"
            )
        raise ValueError(f"Unknown provider type: {provider_type}")

# Singleton instance for the app
ai_provider = LLMFactory.get_provider()
llm = ai_provider.get_llm()
embeddings = ai_provider.get_embeddings()
