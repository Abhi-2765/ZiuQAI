# backend/app/services/core/factory.py
import os
from app.services.core.interfaces import LLMService, EmbeddingService, SplittingService, ParsingService
from app.services.llm.llm_provider import GeminiLLM
from app.services.ingestion.embedder import GeminiEmbedder
from app.services.ingestion.chunker import TextSplitter
from app.services.ingestion.parser import FileParser
from app.core.config import settings

def get_llm_service() -> LLMService:
    """
    Factory function to provide the correct LLM service based on environment configuration.
    This strictly enforces the Dependency Inversion Principle.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider == "gemini":
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")
        return GeminiLLM(api_key=api_key)
    else:
        raise ValueError(f"Unsupported LLM Provider: {provider}")

def get_embedding_service() -> EmbeddingService:
    
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "gemini":
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")
        return GeminiEmbedder(api_key=api_key)
    else:
        raise ValueError(f"Unsupported Embedding Provider: {provider}")

def get_splitting_service() -> SplittingService:
    return TextSplitter()

def get_parsing_service() -> ParsingService:
    return FileParser()