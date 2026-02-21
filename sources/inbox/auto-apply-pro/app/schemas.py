from __future__ import annotations
from pydantic import BaseModel

class ParseRequest(BaseModel):
    url: str | None = None
    text: str | None = None

class GenerateRequest(BaseModel):
    url: str | None = None
    text: str | None = None
    profile: str | None = None
    tone: str | None = "confident"

class ApplyRequest(BaseModel):
    url: str
    confirm: bool = True
    dry_run: bool = False
    profile: str | None = None
    tone: str | None = "confident"
