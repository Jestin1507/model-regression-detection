from app.config import LLM_PROVIDER

from app.llm.gemini_client import GeminiClient
from app.llm.groq_client import GroqClient


class LLMFactory:

    @staticmethod
    def get_client():

        if LLM_PROVIDER == "gemini":
            return GeminiClient()

        if LLM_PROVIDER == "groq":
            return GroqClient()

        raise ValueError(
            f"Unsupported provider: {LLM_PROVIDER}"
        )