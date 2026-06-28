"""
Regression Detection
"""

import json
from pathlib import Path
from datetime import datetime

from app.config import LLM_PROVIDER


class RegressionDetector:

    def __init__(self):

        self.history_file = Path(
            "reports/json/comparison_history.json"
        )

    def _load_history(self):

        if not self.history_file.exists():
            return []

        try:

            with open(
                self.history_file,
                "r",
                encoding="utf-8",
            ) as f:

                content = f.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except Exception:

            return []

    def _save_history(self, history):

        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.history_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                history,
                f,
                indent=4,
            )

    def check(
        self,
        accuracy,
        prompt_version="current",
    ):

        history = self._load_history()

        print("\n")
        print("=" * 80)
        print("REGRESSION DETECTION")
        print("=" * 80)

        if history:

            previous = history[-1]["accuracy"]

            print(
                f"Previous Accuracy : {previous:.2%}"
            )

            print(
                f"Current Accuracy  : {accuracy:.2%}"
            )

            if accuracy < previous:

                print("\n🚨 REGRESSION DETECTED")

            elif accuracy > previous:

                print("\n✅ IMPROVEMENT DETECTED")

            else:

                print("\n➖ No Change")

        else:

            print("✅ First evaluation run.")

        history.append({

            "timestamp": datetime.now().isoformat(),

            "provider": LLM_PROVIDER,

            "prompt": prompt_version,

            "accuracy": accuracy,

        })

        self._save_history(history)

        print("\nHistory saved successfully.")