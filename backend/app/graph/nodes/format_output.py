# backend/app/graph/nodes/format_output.py
from app.graph.state import QuizGraphState

async def format_output(state: QuizGraphState) -> dict:
    # Any final transformations can be placed here.
    # Currently, the validate step ensures that questions are correctly formatted.
    return {"questions": state.get("questions", [])}
