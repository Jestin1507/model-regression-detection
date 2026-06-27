"""
Evaluator

Runs the golden dataset through the classifier
and stores predictions in reports/json/evaluation_results.json
"""

from pathlib import Path

from app.classifier import TicketClassifier
from utils.file_manager import FileManager


class Evaluator:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)

        self.output_file = Path(
            "reports/json/evaluation_results.json"
        )

        # Create the classifier only once
        self.classifier = TicketClassifier()

    def evaluate(self):

        dataset = FileManager.load_json(self.dataset_path)

        results = []

        print("=" * 80)
        print(f"Running evaluation on {len(dataset)} samples...")
        print("=" * 80)

        for index, sample in enumerate(dataset, start=1):

            prediction = self.classifier.classify(sample["text"])

            result = {
                "id": index,
                "text": sample["text"],
                "expected": sample["expected_category"],
                "predicted": prediction,
                "correct": prediction == sample["expected_category"],
            }

            results.append(result)

            status = "✅" if result["correct"] else "❌"

            print(
                f"[{index:02d}/{len(dataset)}] "
                f"{status} "
                f"Expected: {sample['expected_category']:<20}"
                f"Predicted: {prediction}"
            )

        FileManager.save_json(
            self.output_file,
            results
        )

        print("\nEvaluation results saved successfully!")

        return results