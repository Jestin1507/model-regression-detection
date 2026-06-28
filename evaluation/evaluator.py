"""
Evaluator
"""

from pathlib import Path
from datetime import datetime

from app.classifier import TicketClassifier
from app.config import (
    LLM_PROVIDER,
    GEMINI_MODEL,
    GROQ_MODEL,
)

from utils.file_manager import FileManager


class Evaluator:

    def __init__(
        self,
        dataset_path,
        prompt_name="current",
    ):

        self.dataset_path = Path(dataset_path)

        self.output_file = Path(
            "reports/json/evaluation_results.json"
        )

        self.classifier = TicketClassifier(
            prompt_name=prompt_name,
        )

        self.prompt_name = prompt_name

    def evaluate(self):

        dataset = FileManager.load_json(
            self.dataset_path
        )

        results = []

        model_name = (
            GEMINI_MODEL
            if LLM_PROVIDER == "gemini"
            else GROQ_MODEL
        )

        print("=" * 80)
        print(
            f"Evaluating Prompt: {self.prompt_name}"
        )
        print("=" * 80)

        for index, sample in enumerate(
            dataset,
            start=1,
        ):

            prediction = self.classifier.classify(
                sample["text"]
            )

            record = {

                "id": index,

                "provider": LLM_PROVIDER,

                "model": model_name,

                "prompt_version": self.prompt_name,

                "timestamp": datetime.now().isoformat(),

                "text": sample["text"],

                "expected": sample[
                    "expected_category"
                ],

                "predicted": prediction,

                "correct": prediction
                == sample["expected_category"],
            }

            results.append(record)

            print(
                f"[{index}/{len(dataset)}] "
                f"{'✅' if record['correct'] else '❌'} "
                f"{record['predicted']}"
            )

        FileManager.save_json(
            self.output_file,
            results,
        )

        return results