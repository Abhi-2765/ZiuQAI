# splitters.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, splitter: str = "RecursiveCharacterTextSplitter"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = splitter
    
    def split(self, documents):
        if self.splitter == "RecursiveCharacterTextSplitter":
            return RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap).split_documents(documents)