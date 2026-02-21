from __future__ import annotations
from typing import Protocol, Dict, Any

class ApplyContext(dict):
    """Holds profile data, resume/cover paths, and config flags."""

class SiteAdapter(Protocol):
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        ...
