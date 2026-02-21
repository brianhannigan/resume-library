from __future__ import annotations
from typing import Dict, Any
from .base import ApplyContext

class WorkdayAdapter:
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        filled = {}
        try:
            page.locator("input[type='email']").first.fill(ctx.get("contact_email",""))
            filled["email"] = True
        except Exception:
            filled["email"] = False
        return filled
