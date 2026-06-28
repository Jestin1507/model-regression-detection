"""
Category-wise Evaluation Metrics
"""

import pandas as pd


class CategoryMetrics:

    @staticmethod
    def calculate(results):

        df = pd.DataFrame(results)

        summary = []

        categories = sorted(df["expected"].unique())

        for category in categories:

            subset = df[df["expected"] == category]

            total = len(subset)

            correct = subset["correct"].sum()

            accuracy = correct / total if total else 0

            summary.append({

                "category": category,

                "total": total,

                "correct": int(correct),

                "incorrect": int(total - correct),

                "accuracy": round(accuracy * 100, 2),

            })

        return summary