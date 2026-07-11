# backend/app/services/llm/prompts.py

QUIZ_GENERATION_PROMPT = """You are an expert quiz generator. Your task is to generate high-quality questions based on the provided context.

Context:
{context}

Requirements:
1. Question Count: {question_count}
2. Difficulty: {difficulty}
3. Question Types allowed: {question_types}

Format your output strictly as a JSON array of objects. Do not include markdown code block syntax (like ```json). Just return the raw JSON.
Each object must have the following fields:
- "question": The text of the question.
- "question_type": Must be one of "scq" (single choice), "mcq" (multiple choice), "tof" (true/false), "fib" (fill in the blank). Only generate question types that are allowed.
- "options": A list of string options for "scq", "mcq", and "tof". For "tof", options must be exactly ["True", "False"]. For "fib", this field must be null.
- "correct_answer": The correct answer. For "scq" and "tof", it must match one of the options exactly. For "mcq", it must be a comma-separated list of the correct option values (e.g. "Option A, Option C"). For "fib", it is the exact text representing the blank answer.

Ensure the questions are accurate to the context, and cover key concepts.
"""
