import argparse
from pathlib import Path

from evaluation.report_generator import ReportGenerator
from evaluation.evaluator import Evaluator
from evaluation.metrics import MetricsEngine
from evaluation.regression import RegressionDetector

# -------------------------------
# Command Line Arguments
# -------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--prompt",
    default="current",
    help="Prompt version (current, v1, v2, ...)"
)

args = parser.parse_args()

# -------------------------------
# Dataset
# -------------------------------

DATASET = Path("datasets/golden_dataset.json")

# -------------------------------
# Evaluation
# -------------------------------

evaluator = Evaluator(
    DATASET,
    prompt_name=args.prompt,
)

results = evaluator.evaluate()

# -------------------------------
# Metrics
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

detector.check(
    metrics["accuracy"],
    prompt_version=args.prompt,
)
report = ReportGenerator()
report.generate()