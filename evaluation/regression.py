"""
Regression Detection Engine

Stores evaluation history and detects if model performance
has improved or regressed.
"""

import json
from pathlib import Path
from datetime import datetime


class RegressionDetector:

    def __init__(self):
        self.history_file = Path("evaluation/history.json")

    def _load_history(self):

        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:

                content = f.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except json.JSONDecodeError:
            return []

    def _save_history(self, history):

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def check(self, accuracy):

        history = self._load_history()

        current = {
            "run": len(history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accuracy": round(float(accuracy), 4),
        }

        print("\n")
        print("=" * 80)
        print("REGRESSION DETECTION")
        print("=" * 80)

        if len(history) == 0:

            print("✅ First evaluation run.")
            print("History created.")

        else:

            previous = history[-1]["accuracy"]

            print(f"Previous Accuracy : {previous:.2%}")
            print(f"Current Accuracy  : {accuracy:.2%}")

            if accuracy > previous:
                print("\n📈 MODEL IMPROVED")

            elif accuracy < previous:
                print("\n🚨 REGRESSION DETECTED")

            else:
                print("\n➖ No Change")

        history.append(current)

        self._save_history(history)

        print("\nHistory saved successfully.")