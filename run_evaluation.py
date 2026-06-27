from pathlib import Path

from evaluation.evaluator import Evaluator

DATASET = Path("datasets/golden_dataset.json")

evaluator = Evaluator(DATASET)

results = evaluator.evaluate()