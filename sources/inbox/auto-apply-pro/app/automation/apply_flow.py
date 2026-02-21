from __future__ import annotations
from datetime import datetime
from typing import Dict
from playwright.sync_api import sync_playwright
from ..config import HEADLESS, RATE_MIN, RATE_MAX, CFG
from ..adapters.generic import GenericAdapter
from ..adapters.greenhouse import GreenhouseAdapter
from ..adapters.lever import LeverAdapter
from ..adapters.workday import WorkdayAdapter
from ..automation.utils import jitter
from ..database import get_session
from ..models import Application, AuditEvent

DOMAIN_MAP = {
    "greenhouse.io": GreenhouseAdapter,
    "lever.co": LeverAdapter,
    "myworkdayjobs.com": WorkdayAdapter,
}

def pick_adapter(url: str):
    for dom, cls in DOMAIN_MAP.items():
        if dom in url:
            return cls()
    return GenericAdapter()

def manual_gate(page, filled_fields: Dict):
    path = f"out/manual_gate_{datetime.utcnow().timestamp():.0f}.png"
    page.screenshot(path=path, full_page=True)
    print(f"[Manual-Gate] Review screenshot: {path}")
    resp = input("Proceed with submit? (y/N): ").strip().lower()
    return resp == "y"

def apply_once(url: str, ctx: dict, confirm: bool = True, dry_run: bool = False) -> Dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.set_default_timeout(10000)
        page.goto(url)
        jitter(RATE_MIN, RATE_MAX)
        adapter = pick_adapter(url)
        filled = adapter.apply(page, ctx)

        if dry_run or CFG["defaults"].get("observe_only", True):
            result = {"submitted": False, "reason": "dry_run", "filled": filled}
        else:
            proceed = True
            if confirm:
                proceed = manual_gate(page, filled)
            if proceed:
                clicked = False
                for sel in ["button[type='submit']", "button:has-text('Submit')", "text=Submit"]:
                    try:
                        page.locator(sel).first.click()
                        clicked = True
                        break
                    except Exception:
                        pass
                result = {"submitted": clicked, "filled": filled}
            else:
                result = {"submitted": False, "reason": "user_cancel", "filled": filled}
        browser.close()
        return result

def log_result(url: str, result: Dict, context: dict) -> int:
    with get_session() as s:
        app = Application(
            datetime_utc=datetime.utcnow(),
            company=context.get("company",""),
            title=context.get("title",""),
            source="autoapply",
            location=context.get("location",""),
            job_url=url,
            status="submitted" if result.get("submitted") else "generated",
            salary_min=context.get("salary_min"),
            salary_max=context.get("salary_max"),
            contact_name=context.get("contact_name"),
            contact_email=context.get("contact_email"),
            profile_used=context.get("profile_used"),
            resume_path=context.get("resume_pdf"),
            cover_letter_path=context.get("cover_letter_path"),
            notes=context.get("notes"),
            error=context.get("error"),
        )
        s.add(app); s.commit(); s.refresh(app)
        ae = AuditEvent(
            application_id=app.id,
            ts=datetime.utcnow(),
            event_type="apply" if result.get("submitted") else "dry_run",
            message="Application flow executed",
            json_blob=str(result),
        )
        s.add(ae); s.commit()
        return app.id
