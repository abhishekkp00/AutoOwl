"""Configuration settings for voice_notion_agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env at project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
STT_MODEL = os.getenv("STT_MODEL", "whisper-large-v3-turbo")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.8-27b")
