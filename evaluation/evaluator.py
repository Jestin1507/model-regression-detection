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

    # --------------------------------------------------

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

        total = len(dataset)

        print("=" * 80)
        print(f"Evaluating Prompt : {self.prompt_name}")
        print(f"Provider          : {LLM_PROVIDER}")
        print(f"Dataset Size      : {total}")
        print("=" * 80)

        for index, sample in enumerate(dataset, start=1):

            question = sample["question"]

            expected = sample["expected"]

            prediction = (
                self.classifier
                .classify(question)
                .strip()
            )

            correct = (
                prediction.lower()
                == expected.lower()
            )

            record = {

                "id": index,

                "provider": LLM_PROVIDER,

                "model": model_name,

                "prompt_version": self.prompt_name,

                "timestamp": datetime.now().isoformat(),

                "category": sample["category"],

                "difficulty": sample["difficulty"],

                "question": question,

                "expected": expected,

                "predicted": prediction,

                "correct": correct,

            }

            results.append(record)

            status = "✅" if correct else "❌"

            print(
                f"[{index:02d}/{total}] "
                f"{status} "
                f"{sample['category']:<12}"
                f"{prediction}"
            )

        FileManager.save_json(
            self.output_file,
            results,
        )

        correct_predictions = sum(
            r["correct"] for r in results
        )

        print("\n" + "=" * 80)
        print("EVALUATION COMPLETED")
        print("=" * 80)

        print(f"Samples Evaluated : {total}")
        print(f"Correct           : {correct_predictions}")
        print(f"Incorrect         : {total - correct_predictions}")

        print("=" * 80)

        return results