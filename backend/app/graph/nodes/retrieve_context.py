# backend/app/graph/nodes/retrieve_context.py
from app.graph.state import QuizGraphState

# Max characters of context to send to the LLM (~3k tokens)
MAX_CONTEXT_CHARS = 12000

async def retrieve_context(state: QuizGraphState) -> dict:
    """
    If context was pre-loaded by the generate endpoint (local files),
    just apply truncation. Otherwise return empty context.
    """
    context = state.get("context", "")
    
    if not context:
        # No pre-loaded context — this means no files were uploaded
        return {"context": ""}
    
    # Truncate to stay within token budget
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n\n[...context truncated for token efficiency...]"
    
    return {"context": context}
