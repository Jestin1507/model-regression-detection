from pathlib import Path


def load_prompt(prompt_path: Path) -> str:
    """
    Load a prompt from a text file.

    Args:
        prompt_path (Path): Path to the prompt file.

    Returns:
        str: Prompt content as a string.
    """
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8").strip()