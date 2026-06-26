"""
Gemini Client

This module is responsible for all communication with the Gemini API.
"""

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=TEMPERATURE,
            ),
            contents=user_prompt,
        )

        return response.text.strip()