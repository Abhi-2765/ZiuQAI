# backend/app/services/retrieval/retriever.py

from typing import List
import os

from app.services.core.interfaces import RetrieverService, EmbeddingService
from langchain_postgres import PGVector


class LangchainRetriever(RetrieverService):
    def __init__(self, embedding_model: EmbeddingService, quiz_id: int, uid: int):
        self.embedding_model = embedding_model

        self.vectorstore = PGVector(
            collection_name=f"quiz_{quiz_id}",
            connection_string=os.getenv("DATABASE_URL"),
            embedding_function=self.embedding_model.embedder
        )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": 5,
                "filter": {
                    "quiz_id": quiz_id,
                    "user_id": uid
                }
            }
        )

    async def retrieve(self, query: str) -> List[str]:
        docs = await self.retriever.ainvoke(query)
        return [doc.page_content for doc in docs]