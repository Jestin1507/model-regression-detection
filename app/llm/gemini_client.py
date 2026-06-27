"""
Gemini Client
"""

import google.generativeai as genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.llm.base_client import BaseLLMClient


class GeminiClient(BaseLLMClient):

    def __init__(self):

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        prompt = f"""
{system_prompt}

Customer Message:
{user_prompt}
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()