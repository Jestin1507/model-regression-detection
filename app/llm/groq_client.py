"""
Groq Client
"""

from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.llm.base_client import BaseLLMClient


class GroqClient(BaseLLMClient):

    def __init__(self):

        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            temperature=0,
        )

        return response.choices[0].message.content.strip()