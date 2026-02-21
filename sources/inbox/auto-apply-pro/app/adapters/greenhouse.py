from __future__ import annotations
from typing import Dict, Any
from .base import ApplyContext
from ..automation.utils import human_type, jitter

class GreenhouseAdapter:
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        filled = {}
        mapping = {
            "#first_name": ctx.get("first_name"),
            "#last_name": ctx.get("last_name"),
            "#email": ctx.get("contact_email"),
            "#phone": ctx.get("contact_phone"),
            "input[name='urls[LinkedIn]']": ctx.get("linkedin_url"),
            "input[name='urls[GitHub]']": ctx.get("github_url"),
        }
        for sel, val in mapping.items():
            try:
                page.locator(sel).fill(str(val))
                filled[sel] = val
                jitter(150, 350)
            except Exception:
                pass
        try:
            page.set_input_files("input[type='file']", ctx.get("resume_pdf"))
            filled["resume_upload"] = True
        except Exception:
            filled["resume_upload"] = False
        try:
            page.locator("textarea[name='cover_letter_text']").fill(ctx.get("cover_letter_text", ""))
            filled["cover_letter"] = True
        except Exception:
            filled["cover_letter"] = False
        return filled
