"""
Utility functions for reading and writing JSON files.
"""

import json
from pathlib import Path


class FileManager:

    @staticmethod
    def load_json(path: Path):

        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:

                content = f.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except json.JSONDecodeError:
            return []

    @staticmethod
    def save_json(path: Path, data):

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )