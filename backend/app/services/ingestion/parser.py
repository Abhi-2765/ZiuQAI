# backend/app/services/ingestion/parser.py
import os
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader
from app.services.core.interfaces import ParsingService
from fastapi import UploadFile

from typing import List

class FileParser(ParsingService):
    def __init__(self):
        pass 

    async def parse(self, file: UploadFile):
        suffix = self._get_suffix(file.filename)

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            documents = self._load_documents(temp_path, suffix)

            text = "\n\n".join([doc.page_content for doc in documents])

            return text

        finally:
            os.remove(temp_path)

    def _get_suffix(self, filename: str) -> str:
        if not filename:
            raise ValueError("File must have a name")

        return os.path.splitext(filename)[1].lower()

    def _load_documents(self, file_path: str, suffix: str) -> List:
        """
        Select appropriate loader or parse directly
        """
        if suffix == ".pdf":
            loader = PyMuPDFLoader(file_path)
            return loader.load()
        elif suffix == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            class TextDoc:
                def __init__(self, text):
                    self.page_content = text
            return [TextDoc(content)]
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def parse_local_file(self, file_path: str) -> str:
        """Parse a file already saved on local disk. Returns extracted text."""
        suffix = self._get_suffix(os.path.basename(file_path))
        documents = self._load_documents(file_path, suffix)
        return "\n\n".join([doc.page_content for doc in documents])