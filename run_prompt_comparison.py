"""
Compare Multiple Prompt Versions
"""

from pathlib import Path
import json

from evaluation.category_metrics import CategoryMetrics
from evaluation.evaluator import Evaluator
from evaluation.metrics import MetricsEngine
from app.config import LLM_PROVIDER

PROMPTS = [
    "current",
    "v1",
    "v2",
]

DATASET = Path(
    "datasets/golden_dataset.json"
)

comparison_results = []

print("=" * 80)
print("PROMPT REGRESSION TESTING")
print("=" * 80)

baseline_accuracy = None

for prompt in PROMPTS:

    print(f"\nEvaluating Prompt : {prompt}")

    evaluator = Evaluator(

        dataset_path=DATASET,

        prompt_name=prompt,

    )

    results = evaluator.evaluate()

    metrics = MetricsEngine.calculate(results)

    category_summary = CategoryMetrics.calculate(results)

    accuracy = metrics["accuracy"]

    if baseline_accuracy is None:

        baseline_accuracy = accuracy

        change = 0

    else:

        change = accuracy - baseline_accuracy

    if change < -0.03:

        status = "REGRESSION"

    elif change < 0:

        status = "PASS"

    else:

        status = "PASS"

    comparison_results.append(

    {

        "provider": LLM_PROVIDER,

        "prompt": prompt,

        "accuracy": round(accuracy, 4),

        "change": round(change, 4),

        "status": status,

        "category_metrics": category_summary,

    }

)

    print(

        f"Accuracy : {accuracy:.2%}"

    )

Path(
    "reports/json"
).mkdir(
    parents=True,
    exist_ok=True,
)

with open(

    "reports/json/prompt_comparison.json",

    "w",

    encoding="utf-8",

) as f:

    json.dump(

        comparison_results,

        f,

        indent=4,

    )

print("\n")

print("="*80)

print("PROMPT COMPARISON")

print("="*80)

for item in comparison_results:

    print(

        f"{item['prompt']:<10}"

        f"{item['accuracy']:.2%}    "

        f"{item['status']}"

    )