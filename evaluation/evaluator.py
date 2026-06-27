"""
Evaluator

Runs the golden dataset through the selected LLM
and stores evaluation results.
"""

from pathlib import Path
from datetime import datetime

from app.classifier import TicketClassifier
from app.config import LLM_PROVIDER, GEMINI_MODEL, GROQ_MODEL
from utils.file_manager import FileManager


class Evaluator:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)

        self.output_file = Path(
            "reports/json/evaluation_results.json"
        )

        self.classifier = TicketClassifier()

    def evaluate(self):

        dataset = FileManager.load_json(self.dataset_path)

        results = []

        model_name = (
            GEMINI_MODEL
            if LLM_PROVIDER == "gemini"
            else GROQ_MODEL
        )

        print("=" * 80)
        print(f"Running evaluation on {len(dataset)} samples...")
        print("=" * 80)

        for index, sample in enumerate(dataset, start=1):

            prediction = self.classifier.classify(sample["text"])

            record = {

                "id": index,

                "provider": LLM_PROVIDER,

                "model": model_name,

                "timestamp": datetime.now().isoformat(),

                "prompt_version": "v1",

                "text": sample["text"],

                "expected": sample["expected_category"],

                "predicted": prediction,

                "correct": prediction == sample["expected_category"],
            }

            results.append(record)

            status = "✅" if record["correct"] else "❌"

            print(
                f"[{index:02d}/{len(dataset)}] "
                f"{status} "
                f"Expected: {record['expected']:<20}"
                f"Predicted: {record['predicted']}"
            )

        FileManager.save_json(
            self.output_file,
            results,
        )

        print("\nEvaluation results saved.")

        return results