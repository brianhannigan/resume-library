from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

def load_profile_json(name: str = "software-engineer") -> Dict[str, Any]:
    path = Path(f"profiles/{name}.json")
    if not path.exists():
        path = Path("profiles/software-engineer.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_txt(path: str = "profiles/main_resume.txt") -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")
