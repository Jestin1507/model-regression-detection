"""
Run Complete LLM Evaluation Pipeline
"""

from pathlib import Path

from app.config import (
    LLM_PROVIDER,
    CURRENT_PROMPT,
)

from evaluation.evaluator import Evaluator
from evaluation.metrics import MetricsEngine
from evaluation.regression import RegressionDetector

# ==========================================================
# DATASET
# ==========================================================

DATASET = Path(
    "datasets/golden_dataset.json"
)

# ==========================================================
# EVALUATION
# ==========================================================

evaluator = Evaluator(

    dataset_path=DATASET,

    prompt_name=CURRENT_PROMPT,

)

results = evaluator.evaluate()

# ==========================================================
# METRICS
# ==========================================================

metrics = MetricsEngine.calculate(
    results
)

accuracy = metrics["accuracy"]

print("\n")
print("=" * 80)
print("MODEL EVALUATION SUMMARY")
print("=" * 80)

print(f"\nProvider : {LLM_PROVIDER}")

print(f"Prompt   : {CURRENT_PROMPT}")

print(f"Accuracy : {accuracy:.2%}\n")

print(metrics["classification_report"])

print("\nConfusion Matrix\n")

print(metrics["confusion_matrix"])

# ==========================================================
# REGRESSION DETECTION
# ==========================================================

detector = RegressionDetector()

summary = detector.check(

    accuracy=accuracy,

    provider=LLM_PROVIDER,

    prompt_version=CURRENT_PROMPT,

)

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\n")
print("=" * 80)
print("FINAL RESULT")
print("=" * 80)

print(f"Status    : {summary['status']}")

print(f"Provider  : {summary['provider']}")

print(f"Prompt    : {summary['prompt']}")

print(f"Accuracy  : {summary['accuracy']:.2%}")

print(f"Change    : {summary['change']:.2%}")

print("=" * 80)