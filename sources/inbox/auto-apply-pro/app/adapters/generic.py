from __future__ import annotations
from typing import Dict, Any
from .base import ApplyContext
from ..automation.utils import human_type, jitter

class GenericAdapter:
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        """A best-effort generic filler using heuristics."""
        filled = {}
        text_map = {
            "input[name*='first']": ctx.get("first_name", ""),
            "input[name*='last']": ctx.get("last_name", ""),
            "input[type='email']": ctx.get("contact_email", ""),
            "input[type='tel'], input[name*=\"phone\"]": ctx.get("contact_phone", ""),
            "input[name*='city']": ctx.get("location", ""),
            "input[name*='linkedin']": ctx.get("linkedin_url", ""),
            "input[name*='github']": ctx.get("github_url", ""),
        }
        for sel, val in text_map.items():
            try:
                page.locator(sel).first.wait_for(timeout=1500)
                human_type(page, sel, str(val))
                filled[sel] = val
                jitter(200, 400)
            except Exception:
                pass
        try:
            ta = "textarea, [contenteditable='true']"
            page.locator(ta).first.fill(ctx.get("cover_letter_text", "")[:8000])
            filled["cover_letter"] = True
        except Exception:
            filled["cover_letter"] = False
        try:
            upload = page.locator("input[type='file']").first
            upload.set_input_files(ctx.get("resume_pdf"))
            filled["resume_upload"] = True
        except Exception:
            filled["resume_upload"] = False
        return filled
