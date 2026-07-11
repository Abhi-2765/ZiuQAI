# backend/app/models/__init__.py
"""
The primary use of an __init__.py file within a directory in Python is to signal to the Python interpreter that the directory 
should be treated as a package or subpackage [1]. This enables you to import modules, classes, and variables from files within 
that directory using standard import statements
"""
from .users import User
from .quizes import Quiz
from .participants import Participant
from .questions import Question
from .user_responses import UserResponse
from .chat_session import ChatSession
from .chat_message import ChatMessage
from .quiz_resource import QuizResource
from .document import Document
from .chunk import Chunk

__all__ = [
    "User",
    "Quiz",
    "Participant",
    "Question",
    "UserResponse",
    "ChatSession",
    "ChatMessage",
    "QuizResource",
    "Document",
    "Chunk",
]