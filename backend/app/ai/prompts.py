from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT_TEXT = """
You are an expert academic quiz generator.

Your role is to generate high-quality, diverse, and non-redundant quiz questions 
strictly grounded in the provided context.

CRITICAL RULES:

1. You MUST use only the provided context. Do NOT use outside knowledge.
2. Do NOT repeat or rephrase existing questions.
3. Each generated question must test a DISTINCT concept.
4. Avoid testing the same idea in different wording.
5. All questions must be factually correct based on context.
6. Output MUST be valid JSON only. No extra text.
7. Follow the exact schema provided.
8. Randomize answer positions for choice-based questions.
9. Do not generate explanations outside the schema.

DIVERSITY REQUIREMENTS:
- Cover different concepts from the context.
- Avoid focusing repeatedly on the same paragraph.
- Avoid trivial rewordings.

If constraints cannot be satisfied, return fewer questions rather than violating rules.
"""

SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_TEXT)

GENERATION_PROMPT_TEXT = """
You are generating NEW questions for a quiz.

Topic: {topic}
Difficulty: {difficulty}
Number of Questions: {num_questions}
Question Types: {question_types}

Retrieved Context:
{context}

Already Existing Questions (DO NOT repeat or paraphrase these):
{existing_questions}

Additional Instructions:
{instructions}

OUTPUT FORMAT:

{{
  "questions": [
    {{
      "type": "SCQ | MCQ | FIB | TOF",
      "question": "string",
      "options": ["string"] | null,
      "answer": "string | [string] | boolean"
    }}
  ]
}}
"""

GENERATION_PROMPT = HumanMessagePromptTemplate.from_template(GENERATION_PROMPT_TEXT)

REGENERATE_PROMPT_TEXT = """
You must generate ONE replacement question.

Target Difficulty: {difficulty}
Target Question Type: {question_type}

Retrieved Context:
{context}

Question Being Replaced:
{old_question}

Existing Approved Questions (DO NOT duplicate or paraphrase):
{existing_questions}

Additional Instructions:
{instructions}

Requirements:
- The new question must test a DIFFERENT concept than the replaced one.
- It must not be semantically similar to any existing question.
- Follow the same difficulty level.
- Follow strict JSON format.

OUTPUT FORMAT:

{{
  "questions": [
    {{
      "type": "{question_type}",
      "question": "string",
      "options": ["string"] | null,
      "answer": "string | [string] | boolean"
    }}
  ]
}}
"""

REGENERATE_PROMPT = HumanMessagePromptTemplate.from_template(REGENERATE_PROMPT_TEXT)

# --- Agent Specific Prompts ---

AGENT_SYSTEM_PROMPT_TEXT = """
You are an expert educational content creator.
Your goal is to generate structured multiple-choice questions (MCQs) that are accurately grounded in the provided context.
Each question must have exactly 4 options and a clear explanation.
"""

AGENT_SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(AGENT_SYSTEM_PROMPT_TEXT)

AGENT_GENERATION_PROMPT_TEXT = """
Generate {num_questions} multiple choice questions based on the following context:

{context}

Each question must strictly follow this structure:
{{
  "id": "unique_string",
  "question": "text",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "exactly one of the options",
  "explanation": "reasoning"
}}
"""

AGENT_GENERATION_PROMPT = HumanMessagePromptTemplate.from_template(AGENT_GENERATION_PROMPT_TEXT)

AGENT_REGENERATE_PROMPT_TEXT = """
The following questions were rejected. Please generate {num_to_regenerate} NEW questions to replace them.

Retrieved Context:
{context}

Rejected Question Context/Topics (AVOID THESE):
{rejected_questions}

Previously Accepted Questions (AVOID DUPLICATING):
{accepted_questions}

Requirements:
- Use a slightly different reasoning approach for these new questions.
- Strictly follow the JSON schema provided earlier.
"""

AGENT_REGENERATE_PROMPT = HumanMessagePromptTemplate.from_template(AGENT_REGENERATE_PROMPT_TEXT)
