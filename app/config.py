"""
Application configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Project Paths
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_DIR = PROJECT_ROOT / "app"

PROMPTS_DIR = APP_DIR / "prompts"

CURRENT_PROMPT = "current"

# -------------------------------
# LLM Configuration
# -------------------------------

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models

GEMINI_MODEL = "gemini-2.5-flash"

GROQ_MODEL = "llama-3.1-8b-instant"