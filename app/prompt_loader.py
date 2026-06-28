"""
Prompt Loader
"""

from pathlib import Path


def load_prompt(prompt_path: Path) -> str:
    """
    Load a prompt file.
    """

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()