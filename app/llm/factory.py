from app.config import LLM_PROVIDER


class LLMFactory:

    @staticmethod
    def get_client():

        if LLM_PROVIDER == "gemini":
            from app.llm.gemini_client import GeminiClient
            return GeminiClient()

        elif LLM_PROVIDER == "groq":
            from app.llm.groq_client import GroqClient
            return GroqClient()

        raise ValueError(f"Unsupported provider: {LLM_PROVIDER}")