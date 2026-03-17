# loader.py

import os
from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

class IBaseLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        pass

class PDFFileLoader(IBaseLoader):
    def load(self, file_path: str) -> List[Document]:
        return PyPDFLoader(file_path).load()

class TextFileLoader(IBaseLoader):
    def load(self, file_path: str) -> List[Document]:
        return TextLoader(file_path, encoding='utf-8').load()

class DocxFileLoader(IBaseLoader):
    def load(self, file_path: str) -> List[Document]:
        return UnstructuredWordDocumentLoader(file_path).load()

class DocumentLoaderFactory:
    _loaders = {
        ".pdf": PDFFileLoader(),
        ".txt": TextFileLoader(),
        ".docx": DocxFileLoader(),
        ".doc": DocxFileLoader(),
    }

    @classmethod
    def get_loader(cls, file_path: str) -> IBaseLoader:
        ext = os.path.splitext(file_path)[1].lower()
        loader = cls._loaders.get(ext)
        if not loader:
            raise ValueError(f"Unsupported file extension: {ext}")
        return loader

class UniversalLoader:
    """Consolidated loader and chunker for various document types."""
    def __init__(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.file_path = file_path
        self._loader = DocumentLoaderFactory.get_loader(file_path)
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_and_split(self) -> List[Document]:
        docs = self._loader.load(self.file_path)
        return self._splitter.split_documents(docs)