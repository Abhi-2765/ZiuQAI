import operator
import json
from typing import Annotated, List, TypedDict, Optional
from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

from app.ai.llm import llm
from app.ai.chromadb import vector_store
from app.ai.prompts import (
    AGENT_SYSTEM_PROMPT, 
    AGENT_GENERATION_PROMPT, 
    AGENT_REGENERATE_PROMPT
)

class QuestionSchema(BaseModel):
    id: str = Field(description="Unique identifier for the question")
    question: str = Field(description="The question text")
    options: List[str] = Field(description="List of 4 options (A, B, C, D)")
    correct_answer: str = Field(description="The correct option")
    explanation: str = Field(description="Explanation for why the answer is correct")

class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]

class AgentState(TypedDict):
    document_id: str
    num_questions: int
    context: str
    questions: List[QuestionSchema]
    accepted_questions: List[str]   
    rejected_questions: List[str]   
    regeneration_attempts: int
    status: str

def retrieve_context_node(state: AgentState):
    docs = vector_store.similarity_search("", k=5) 
    context = "\n\n".join([doc.page_content for doc in docs])
    return {"context": context, "status": "retrieved"}

async def generate_questions_node(state: AgentState):
    structured_llm = llm.with_structured_output(QuestionListSchema)
    
    messages = [
        AGENT_SYSTEM_PROMPT.format(),
        AGENT_GENERATION_PROMPT.format(
            num_questions=state['num_questions'],
            context=state['context']
        )
    ]
    
    response = await structured_llm.ainvoke(messages)
    
    return {
        "questions": response.questions, 
        "status": "awaiting_review"
    }

async def regenerate_rejected_node(state: AgentState):
    if not state['rejected_questions']:
        return {"status": "all_accepted"}
    
    rejected_ids = state['rejected_questions']
    rejected_obj = [q for q in state['questions'] if q.id in rejected_ids]
    accepted_obj = [q for q in state['questions'] if q.id not in rejected_ids]
    
    structured_llm = llm.with_structured_output(QuestionListSchema)
    
    messages = [
        AGENT_SYSTEM_PROMPT.format(),
        AGENT_REGENERATE_PROMPT.format(
            num_to_regenerate=len(rejected_ids),
            context=state['context'],
            rejected_questions=[q.question for q in rejected_obj],
            accepted_questions=[q.question for q in accepted_obj]
        )
    ]
    
    response = await structured_llm.ainvoke(messages)
    
    new_questions = accepted_obj + response.questions
    
    return {
        "questions": new_questions,
        "rejected_questions": [],
        "regeneration_attempts": state['regeneration_attempts'] + 1,
        "status": "awaiting_review"
    }

def route_after_review(state: AgentState):
    if state.get('status') == "all_accepted" or not state.get('rejected_questions'):
        return END
    return "regenerate"

builder = StateGraph(AgentState)
builder.add_node("retrieve", retrieve_context_node)
builder.add_node("generate", generate_questions_node)
builder.add_node("regenerate", regenerate_rejected_node)
builder.add_node("human_review", lambda x: x)

builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "human_review")
builder.add_edge("regenerate", "human_review")

builder.add_conditional_edges("human_review", route_after_review, {
    END: END,
    "regenerate": "regenerate"
})
