"""
Regression Detection Engine
"""

from pathlib import Path
from datetime import datetime
import json


class RegressionDetector:

    def __init__(self):

        self.history_file = Path(
            "reports/json/comparison_history.json"
        )

        self.threshold = 0.03

    # ----------------------------------------------------

    def _load_history(self):

        if not self.history_file.exists():
            return []

        if self.history_file.stat().st_size == 0:
            return []

        try:

            with open(
                self.history_file,
                "r",
                encoding="utf-8",
            ) as f:

                return json.load(f)

        except json.JSONDecodeError:

            return []

    # ----------------------------------------------------

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

    # ----------------------------------------------------

    def check(
        self,
        accuracy,
        provider,
        prompt_version,
    ):

        history = self._load_history()

        print("\n")
        print("=" * 80)
        print("MODEL REGRESSION DETECTION")
        print("=" * 80)

        previous_accuracy = accuracy
        change = 0
        regression = False
        status = "Baseline"

        if history:

            previous_accuracy = history[-1]["accuracy"]

            change = accuracy - previous_accuracy

            regression = change < -self.threshold

            if regression:

                status = "Regression"

            elif change > 0:

                status = "Improved"

            elif change == 0:

                status = "No Change"

            else:

                status = "Healthy"

        current = {

            "evaluation_id": len(history) + 1,

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "provider": provider,

            "prompt": prompt_version,

            "accuracy": round(accuracy, 4),

            "previous_accuracy": round(previous_accuracy, 4),

            "change": round(change, 4),

            "threshold": self.threshold,

            "regression": regression,

            "status": status,

        }

        history.append(current)

        self._save_history(history)

        print(f"Provider            : {provider}")
        print(f"Prompt Version      : {prompt_version}")
        print(f"Previous Accuracy   : {previous_accuracy:.2%}")
        print(f"Current Accuracy    : {accuracy:.2%}")
        print(f"Accuracy Change     : {change:.2%}")
        print(f"Threshold           : {self.threshold:.2%}")
        print(f"Regression Status   : {status}")

        print("-" * 80)

        if regression:

            print("🚨 REGRESSION DETECTED")

        elif status == "Improved":

            print("📈 MODEL IMPROVED")

        elif status == "No Change":

            print("➖ NO CHANGE")

        elif status == "Healthy":

            print("🟢 WITHIN ACCEPTABLE RANGE")

        else:

            print("📌 BASELINE CREATED")

        print("-" * 80)

        return current