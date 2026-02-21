from __future__ import annotations
from typing import Dict, Any
from .base import ApplyContext

class LeverAdapter:
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        filled = {}
        for sel, val in {
            "input[name='name']": f"{ctx.get('first_name','')} {ctx.get('last_name','')}".strip(),
            "input[name='email']": ctx.get("contact_email"),
            "input[name='phone']": ctx.get("contact_phone"),
        }.items():
            try:
                page.locator(sel).fill(str(val))
                filled[sel] = val
            except Exception:
                pass
        try:
            page.set_input_files("input[type='file']", ctx.get("resume_pdf"))
            filled["resume_upload"] = True
        except Exception:
            filled["resume_upload"] = False
        try:
            page.locator("textarea").first.fill(ctx.get("cover_letter_text", ""))
            filled["cover_letter"] = True
        except Exception:
            filled["cover_letter"] = False
        return filled
