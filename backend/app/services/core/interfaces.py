# backend/app/services/core/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Any
from fastapi import UploadFile

class EmbeddingService(ABC):
    """Interface for generating vector embeddings from text."""
    
    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        pass


class RetrieverService(ABC):
    """Interface for retrieving relevant context paragraphs/chunks given a query."""
    
    @abstractmethod
    async def retrieve(self, query: str) -> List[str]:
        pass


class LLMService(ABC):
    """Interface for generating text using a Large Language Model."""
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Takes a prompt and returns the generated text response."""
        pass

class SplittingService(ABC):
    """Interface for splitting text into chunks."""
    @abstractmethod
    async def split(self, text: str) -> List[str]:
        """Takes a text and returns a list of chunks."""
        pass

class ParsingService(ABC):
    """Interface for parsing files."""
    @abstractmethod
    async def parse(self, file: UploadFile) -> str:
        """Takes a file and returns the text."""
        pass
