# chromadb.py

from langchain_chroma import Chroma
from app.ai.llm import LLM 

embeddings = LLM.get_embedding_model()

vector_store = Chroma(
    collection_name="ZiuQAI",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)