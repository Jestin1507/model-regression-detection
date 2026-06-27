"""
Evaluation Engine

Runs the classifier against the golden dataset and reports accuracy.
"""

import json
import time
from pathlib import Path

from app.classifier import TicketClassifier


class Evaluator:
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        self.classifier = TicketClassifier()

    def load_dataset(self):
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self):

        dataset = self.load_dataset()

        total = len(dataset)
        correct = 0
        results = []

        print("=" * 80)
        print(f"Running evaluation on {total} samples...")
        print("=" * 80)

        for index, sample in enumerate(dataset, start=1):

            expected = sample["expected_category"]

            while True:
                try:
                    prediction = self.classifier.classify(sample["text"])
                    break

                except Exception as e:

                    print("\n⚠ Gemini rate limit reached.")
                    print("Waiting 35 seconds before retrying...\n")

                    time.sleep(35)

            is_correct = prediction == expected

            if is_correct:
                correct += 1

            results.append(
                {
                    "id": sample["id"],
                    "text": sample["text"],
                    "expected": expected,
                    "predicted": prediction,
                    "correct": is_correct,
                }
            )

            status = "✅" if is_correct else "❌"

            print(
                f"[{index:02}/{total}] {status} "
                f"Expected: {expected:<20} "
                f"Predicted: {prediction}"
            )

            # Free Gemini = 5 requests/minute
            if index != total:
                time.sleep(12)

        accuracy = (correct / total) * 100

        print("\n" + "=" * 80)
        print(f"Accuracy : {accuracy:.2f}%")
        print(f"Correct  : {correct}")
        print(f"Wrong    : {total-correct}")
        print(f"Total    : {total}")
        print("=" * 80)

        return results