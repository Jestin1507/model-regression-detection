"""
Business logic for support ticket classification.
"""

from app.prompt_loader import load_prompt
from app.config import CURRENT_PROMPT
from app.llm.gemini_client import GeminiClient


class TicketClassifier:
    def __init__(self):
        self.client = GeminiClient()
        self.prompt = load_prompt(CURRENT_PROMPT)

    def classify(self, text: str) -> str:
        """
        Classify a support ticket into one of the predefined categories.
        """

        prediction = self.client.generate(
            system_prompt=self.prompt,
            user_prompt=text,
        )

        return prediction