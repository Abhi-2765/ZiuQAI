from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = """
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

SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT)

GENERATION_PROMPT = """
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

{
  "questions": [
    {
      "type": "SCQ | MCQ | FIB | TOF",
      "question": "string",
      "options": ["string"] | null,
      "answer": "string | [string] | boolean"
    }
  ]
}
"""

GENERATION_PROMPT = HumanMessagePromptTemplate.from_template(GENERATION_PROMPT)


REGENERATE_PROMPT = """
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

{
  "questions": [
    {
      "type": "{question_type}",
      "question": "string",
      "options": ["string"] | null,
      "answer": "string | [string] | boolean"
    }
  ]
}
"""

REGENERATE_PROMPT = HumanMessagePromptTemplate.from_template(REGENERATE_PROMPT)
