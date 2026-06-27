from pathlib import Path

from evaluation.evaluator import Evaluator
from evaluation.metrics import MetricsEngine
from evaluation.regression import RegressionDetector

# Dataset location
DATASET = Path("datasets/golden_dataset.json")

# -------------------------------
# Run Evaluation
# -------------------------------

evaluator = Evaluator(DATASET)

results = evaluator.evaluate()

# -------------------------------
# Calculate Metrics
# -------------------------------

metrics = MetricsEngine.calculate(results)

print("\n")
print("=" * 80)
print("MODEL METRICS")
print("=" * 80)

print(f"\nAccuracy : {metrics['accuracy']:.2%}\n")

print(metrics["classification_report"])

print("Confusion Matrix\n")

print(metrics["confusion_matrix"])

# -------------------------------
# Regression Detection
# -------------------------------

detector = RegressionDetector()

detector.check(metrics["accuracy"])