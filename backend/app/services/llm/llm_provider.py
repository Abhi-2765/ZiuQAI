# backend/app/services/llm/llm_provider.py
from app.services.core.interfaces import LLMService
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

class GeminiLLM(LLMService):
    """
    Concrete implementation of LLMService for Google Gemini.
    """
    def __init__(self, api_key: SecretStr, model_name: str = "gemini-2.5-flash", temperature: float = 0.2):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            api_key=SecretStr(api_key)
        )

    async def generate(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return str(response.content)
