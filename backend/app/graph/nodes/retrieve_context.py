# backend/app/graph/nodes/retrieve_context.py
from sqlalchemy import text
from app.db.base import engine
from app.graph.state import QuizGraphState

async def retrieve_context(state: QuizGraphState) -> dict:
    quiz_id = state["quiz_id"]
    collection_name = f"quiz_{quiz_id}"
    
    query = text("""
        SELECT e.document 
        FROM langchain_pg_embedding e
        JOIN langchain_pg_collection c ON e.collection_id = c.uuid
        WHERE c.name = :collection_name
    """)
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(query, {"collection_name": collection_name})
            documents = [row[0] for row in result.fetchall()]
        
        context = "\n\n".join(documents)
        return {"context": context}
    except Exception as e:
        print(f"Error retrieving context for quiz {quiz_id}: {e}")
        return {"context": ""}
