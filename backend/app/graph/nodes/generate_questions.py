# backend/app/graph/nodes/generate_questions.py
import json
import re
from app.graph.state import QuizGraphState
from app.services.core.factory import get_llm_service
from app.services.llm.prompts import QUIZ_GENERATION_PROMPT, QUIZ_RETRY_PROMPT

async def generate_questions(state: QuizGraphState) -> dict:
    attempt = state.get("attempt", 0) + 1
    llm_service = get_llm_service()
    
    if attempt == 1:
        # First attempt: send full context
        prompt = QUIZ_GENERATION_PROMPT.format(
            context=state.get("context", ""),
            question_count=state.get("question_count", 5),
            difficulty=state.get("difficulty", "MEDIUM"),
            question_types=", ".join(state.get("question_types", ["mcq"]))
        )
    else:
        # Retry: skip resending context, just fix errors
        prompt = QUIZ_RETRY_PROMPT.format(
            raw_llm_output=state.get("raw_llm_output", ""),
            errors="\n".join(state.get("errors", [])),
            question_count=state.get("question_count", 5),
            question_types=", ".join(state.get("question_types", ["mcq"])),
            difficulty=state.get("difficulty", "MEDIUM")
        )
    
    try:
        response_text = await llm_service.generate(prompt)
        
        # Clean response text in case LLM wraps it in markdown code blocks
        clean_text = response_text.strip()
        clean_text = re.sub(r"```(?:json)?", "", clean_text).strip()
            
        questions = json.loads(clean_text)
        if not isinstance(questions, list):
            raise ValueError("LLM response is not a JSON list")
            
        return {"questions": questions, "attempt": attempt, "raw_llm_output": clean_text}
    except Exception as e:
        print(f"Error generating questions (attempt {attempt}): {e}")
        return {"questions": [], "attempt": attempt, "raw_llm_output": response_text if 'response_text' in dir() else ""}
