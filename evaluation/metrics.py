"""
Metrics Engine

Calculates evaluation metrics for the classifier.
"""

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


class MetricsEngine:

    @staticmethod
    def calculate(results):

        y_true = [item["expected"] for item in results]
        y_pred = [item["predicted"] for item in results]

        accuracy = accuracy_score(y_true, y_pred)

        report = classification_report(
            y_true,
            y_pred,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_true,
            y_pred,
        )

        return {
            "accuracy": accuracy,
            "classification_report": report,
            "confusion_matrix": matrix,
        }