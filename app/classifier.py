"""
Business logic for support ticket classification.
"""

from pathlib import Path

from app.prompt_loader import load_prompt
from app.config import PROMPTS_DIR
from app.llm.factory import LLMFactory


class TicketClassifier:

    def __init__(self, prompt_name="current"):

        self.client = LLMFactory.get_client()

        prompt_path = PROMPTS_DIR / f"{prompt_name}.txt"

        self.prompt = load_prompt(prompt_path)

    def classify(self, text: str) -> str:

        prediction = self.client.generate(
            system_prompt=self.prompt,
            user_prompt=text,
        )

        return prediction.strip()