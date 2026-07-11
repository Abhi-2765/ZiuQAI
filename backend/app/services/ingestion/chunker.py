# backend/app/services/ingestion/chunker.py
from app.services.core.interfaces import SplittingService
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List

class TextSplitter(SplittingService):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    async def split(self, text: str) -> List[str]:
        return self.splitter.split_text(text)