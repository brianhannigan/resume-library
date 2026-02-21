from __future__ import annotations
import os
import yaml
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()

def load_config() -> Dict[str, Any]:
    with open("config.yaml", "r", encoding="utf-8") as f:
        y = yaml.safe_load(f) or {}
    y.setdefault("defaults", {})
    y.setdefault("automation", {})
    y.setdefault("paths", {})
    return y

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
RATE_MIN = int(os.getenv("RATE_LIMIT_MIN_MS", "250"))
RATE_MAX = int(os.getenv("RATE_LIMIT_MAX_MS", "800"))
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
DEFAULT_PROFILE = os.getenv("DEFAULT_PROFILE", "software-engineer")
CFG = load_config()
