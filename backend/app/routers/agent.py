import os
import uuid
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List, Dict, Any

from app.ai.loaders import UniversalLoader
from app.ai.chromadb import vector_store
from app.ai.graph import builder, AgentState # Assuming compiled later or using builder
from app.models.documents import Document
from app.db.base import Base # Assuming some session management

router = APIRouter(tags=["AI Agent"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    num_questions: int = 5
):
    # 1. Save file locally
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid.uuid4()}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. Ingest into ChromaDB
    loader = UniversalLoader(file_path)
    chunks = loader.load_and_split()
    vector_store.add_documents(chunks)

    # 3. Create initial state
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "document_id": file.filename,
        "num_questions": num_questions,
        "questions": [],
        "accepted_questions": [],
        "rejected_questions": [],
        "regeneration_attempts": 0,
        "status": "started"
    }

    # Compile a transient graph for now or use a shared one
    # For HITL we NEED a checkpointer. I'll use a placeholder/Memory for now 
    # and instructions to setup PostgresSaver.
    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()
    app = builder.compile(checkpointer=checkpointer, interrupt_before=["human_review"])
    
    # Start graph
    result = await app.ainvoke(initial_state, config)
    
    return {
        "thread_id": thread_id,
        "document": file.filename,
        "questions": result.get("questions", []),
        "status": result.get("status")
    }

@router.post("/review/{thread_id}")
async def review_questions(
    thread_id: str,
    accepted_ids: List[str],
    rejected_ids: List[str]
):
    # This endpoint resumes the graph with user feedback
    # In a real setup, we'd fetch the existing app with Postgres checkpointer
    from langgraph.checkpoint.memory import MemorySaver 
    # (Note: MemorySaver won't work across requests in separate processes, 
    # but for local dev/demo it shows the logic. I'll explain Postgres approach.)
    
    # To properly implement this, we need the persisted state.
    # Logic:
    # 1. Update state with accepted/rejected IDs
    # 2. Invoke unblock
    
    return {"message": "Feedback received. Agent will process if needed."}
