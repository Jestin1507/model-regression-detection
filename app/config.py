from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# -----------------------------
# Project Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"
DATASET_DIR = PROJECT_ROOT / "datasets"
REPORTS_DIR = PROJECT_ROOT / "reports"

# -----------------------------
# LLM Configuration
# -----------------------------

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

TEMPERATURE = float(os.getenv("TEMPERATURE", 0))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

CURRENT_PROMPT = PROMPTS_DIR / "current.txt"