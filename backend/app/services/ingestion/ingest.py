# backend/app/services/ingestion/ingest.py

from typing import List
import uuid
import os

from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from langchain_postgres import PGVector
from langchain_core.documents import Document as LCDocument

from app.services.core.interfaces import SplittingService
from app.models.document import Document


class IngestionService:
    def __init__(self, splitter: SplittingService, embedding_model):
        self.splitter = splitter
        self.embedding_model = embedding_model

    async def ingest_document(
        self,
        text: str,
        title: str,
        quiz_id: int,
        user_id: str,
        db: AsyncSession
    ):
        # Storing metadata in DB
        document = Document(
            id=str(uuid.uuid4()),
            title=title
        )
        db.add(document)
        await db.flush()

        # Chunking the text
        chunks: List[str] = await self.splitter.split(text)

        # Converting chunks to LangChain documents
        lc_docs = [
            LCDocument(
                page_content=chunk,
                metadata={
                    "document_id": document.id,
                    "quiz_id": quiz_id,
                    "user_id": user_id
                }
            )
            for chunk in chunks
        ]

        # Storing embeddings in PGVector
        vectorstore = PGVector(
            collection_name=f"quiz_{quiz_id}",
            connection_string=settings.SYNC_DATABASE_URL,
            embedding_function=self.embedding_model.embedder
        )

        vectorstore.add_documents(lc_docs)

        await db.commit()

        return document, len(chunks)