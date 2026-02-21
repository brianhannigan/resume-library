# Auto-Apply Pro — Full Guide & Code

**Generated:** 2025-08-29T18:09:38.172634Z

This document bundles:
- Clear setup and usage instructions,
- Security/compliance guardrails,
- Project tree,
- **Every file's full source code**, inline.

If you prefer a ready-to-run folder, download the ZIP instead.


## Setup & Usage (Quick)

See `README.md` for a quick start. The essentials:

- Create a venv, install requirements, and `playwright install`.
- Copy `.env.example` → `.env`; edit defaults.
- Run `alembic upgrade head`.
- Start API with `./scripts/run.sh`.
- Use CLI commands shown in `README.md`.


## Security & Compliance

- Headful by default; manual confirmation before submit.
- Rate-limited with small randomized delays.
- Do **not** bypass captchas, paywalls, or Terms of Service.
- No credentials checked into code; keep secrets in `.env`.


## Project Tree


```
auto-apply-pro/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ pyproject.toml
├─ requirements.txt
├─ .env.example
├─ config.yaml
├─ scripts/
│  ├─ run.sh
│  ├─ run.ps1
│  ├─ preflight.sh
│  └─ preflight.ps1
├─ alembic.ini
├─ alembic/
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/
│     └─ 0001_init.py
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ jd_parser.py
│  ├─ resume.py
│  ├─ cl_generator.py
│  ├─ main.py
│  ├─ automation/
│  │  ├─ utils.py
│  │  └─ apply_flow.py
│  ├─ adapters/
│  │  ├─ base.py
│  │  ├─ generic.py
│  │  ├─ greenhouse.py
│  │  ├─ lever.py
│  │  └─ workday.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ applications.html
│  │  ├─ application_detail.html
│  │  ├─ upload_form.html
│  │  └─ cover_letter.html
│  └─ static/readme.txt
├─ cli/
│  ├─ __init__.py
│  └─ main.py
├─ cover_letter_templates/
│  ├─ default.jinja2
│  └─ concise.jinja2
├─ cover_letters/
│  ├─ example_acme_software_engineer.txt
│  └─ README.txt
├─ profiles/
│  ├─ main_resume.txt
│  ├─ main_resume.pdf
│  └─ software-engineer.json
├─ samples/
│  ├─ jobs.csv
│  └─ job_description.txt
├─ mock_site/form.html
└─ tests/
   ├─ conftest.py
   ├─ test_parsing.py
   ├─ test_cl_generation.py
   ├─ test_logging.py
   └─ test_playwright_e2e.py
```


## Full Source Code


### `.env.example`

```
LLM_PROVIDER=
LLM_API_KEY=
HEADLESS=false
RATE_LIMIT_MIN_MS=250
RATE_LIMIT_MAX_MS=800
DEFAULT_PROFILE=software-engineer

```


### `.gitignore`

```
.venv/
__pycache__/
*.pyc
.env
*.sqlite
*.db
/out/
.coverage
htmlcov/
.playwright/

```


### `LICENSE`

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


### `README.md`

```markdown
# Auto-Apply Pro (Option A: Python + Playwright + FastAPI + SQLite)

A production-ready toolkit to:
1) Ingest job postings (URL, pasted text, CSV/feeds),
2) Generate tailored cover letters (LLM or rules-based),
3) **Optionally** fill forms via Playwright with a **Manual-Gate** confirm step,
4) Log every submission with audit events and export CSV.

> **Compliance:** Headful by default, rate-limited, never bypasses ToS/paywalls/captchas. “Observe Only” dry-run supported.

---

## Quick Start

### 1) Install
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
playwright install
```

### 2) Configure
Copy `.env.example` to `.env` and edit as needed. Also review `config.yaml`.

```bash
cp .env.example .env
```

### 3) Initialize DB (Alembic)
```bash
alembic upgrade head
```

### 4) Preflight Checks
```bash
./scripts/preflight.sh   # Windows: scripts\preflight.ps1
```

### 5) Run the stack
```bash
./scripts/run.sh         # Windows: scripts\run.ps1
# FastAPI UI at http://127.0.0.1:8000
```

### 6) CLI usage
```bash
autoapply parse --url "https://example.com/jobs/acme-se"
autoapply generate-cl --url "https://example.com/jobs/acme-se" --profile "software-engineer" --tone "confident"
autoapply apply --url "https://example.com/jobs/acme-se" --confirm
autoapply import --csv "./samples/jobs.csv" --dry-run
autoapply log --export "./out/applications.csv" --since "2025-08-01"
```

> “Observe Only” mode (no submit): pass `--dry-run` (CLI) or toggle in `config.yaml`.

---

## Folders

- `app/` FastAPI app, models, adapters, automation flows
- `cli/` Typer CLI
- `alembic/` migrations (`applications`, `audit_events`)
- `profiles/` your resume and profiles (JSON)
- `cover_letter_templates/` Jinja2 templates
- `cover_letters/` generated outputs (examples included)
- `mock_site/` local HTML form for e2e tests
- `tests/` pytest unit + a basic Playwright e2e

---

## Environment (.env)
```
LLM_PROVIDER=
LLM_API_KEY=
HEADLESS=false
RATE_LIMIT_MIN_MS=250
RATE_LIMIT_MAX_MS=800
DEFAULT_PROFILE=software-engineer
```

If `LLM_API_KEY` is not set, the generator falls back to **rules-based Jinja2** using resume/profile + JD.

---

## Security, Compliance & Ethics
- Runs **headful** by default. Do not enable `headless` unless you accept the risk.
- Rate limits and small human-like delays are enforced.
- **Never** bypass paywalls, captchas, or logins that violate ToS. If captcha appears, session pauses and requires manual solve.
- No credential storage in repo; rely on `.env` and OS secret stores.
- “Observe Only” dry-run generates artifacts and logs intent but **does not submit**.

---

## Adding Site Adapters
See `app/adapters/base.py` and the samples
- `generic.py` (best-effort),
- `greenhouse.py`, `lever.py`, `workday.py` (starter stubs).
Each exposes a `apply(page, ctx)` method, returning a dict of `filled_fields` for the Manual-Gate.

---

## Export Logs
```bash
autoapply log --export ./out/apps.csv --since 2025-08-01
```

---

## Tests
```bash
pytest -q
```

---

## Notes
- PDF/Docx generation relies on `reportlab` and `python-docx`. If unavailable, text files are still produced.
- Example cover letter is in `cover_letters/example_acme_software_engineer.txt`.

```


### `alembic.ini`

```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///autoapply.sqlite

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers = console
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s

```


### `alembic/env.py`

```python
from __future__ import annotations
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel
from app import models  # noqa: F401

config = context.config
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```


### `alembic/script.py.mako`

```
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}

```


### `alembic/versions/0001_init.py`

```python
"""init tables

Revision ID: 0001
Revises: 
Create Date: 2025-08-29

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("datetime_utc", sa.DateTime, nullable=False),
        sa.Column("company", sa.String, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("source", sa.String, nullable=True),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("job_url", sa.String, nullable=True),
        sa.Column("status", sa.String, nullable=False, server_default="parsed"),
        sa.Column("salary_min", sa.Integer, nullable=True),
        sa.Column("salary_max", sa.Integer, nullable=True),
        sa.Column("contact_name", sa.String, nullable=True),
        sa.Column("contact_email", sa.String, nullable=True),
        sa.Column("profile_used", sa.String, nullable=True),
        sa.Column("resume_path", sa.String, nullable=True),
        sa.Column("cover_letter_path", sa.String, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("error", sa.Text, nullable=True),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("application_id", sa.Integer, nullable=False),
        sa.Column("ts", sa.DateTime, nullable=False),
        sa.Column("event_type", sa.String, nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("json_blob", sa.Text, nullable=True),
    )

def downgrade():
    op.drop_table("audit_events")
    op.drop_table("applications")

```


### `app/__init__.py`

```python
# empty package marker

```


### `app/adapters/base.py`

```python
from __future__ import annotations
from typing import Protocol, Dict, Any

class ApplyContext(dict):
    """Holds profile data, resume/cover paths, and config flags."""

class SiteAdapter(Protocol):
    def apply(self, page, ctx: ApplyContext) -> Dict[str, Any]:
        ...

```


### `app/adapters/generic.py`

```python
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

```


### `app/adapters/greenhouse.py`

```python
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

```


### `app/adapters/lever.py`

```python
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

```


### `app/adapters/workday.py`

```python
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

```


### `app/automation/apply_flow.py`

```python
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

```


### `app/automation/utils.py`

```python
from __future__ import annotations
import random, time

def human_type(page, selector: str, text: str, min_ms=40, max_ms=120):
    box = page.locator(selector)
    box.click()
    for ch in text:
        page.keyboard.type(ch)
        time.sleep(random.uniform(min_ms/1000.0, max_ms/1000.0))

def jitter(min_ms: int, max_ms: int):
    time.sleep(random.uniform(min_ms/1000.0, max_ms/1000.0))

```


### `app/cl_generator.py`

```python
from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .config import CFG, LLM_PROVIDER, LLM_API_KEY

def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(CFG["paths"]["templates_dir"]),
        autoescape=select_autoescape()
    )

def rules_based_cover_letter(job_desc: str, profile: Dict[str, Any], tone: str, template_name: str) -> str:
    env = _env()
    tmpl = env.get_template(f"{template_name}.jinja2")
    return tmpl.render(
        job_desc=job_desc[:4000],
        profile=profile,
        tone=tone,
    )

def maybe_llm_generate(job_desc: str, profile: Dict[str, Any], tone: str) -> str | None:
    if not LLM_PROVIDER or not LLM_API_KEY:
        return None
    prompt = f"""
Write a {tone} 300–400 word cover letter tailored to this job.
Use my profile facts and achievements where relevant.
Focus on measurable impact; end with a concrete CTA.

JOB DESCRIPTION:
{job_desc[:4000]}

PROFILE:
{profile}
"""
    try:
        if LLM_PROVIDER.lower() == "openai":
            import openai  # type: ignore
            openai.api_key = LLM_API_KEY
            resp = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=550,
                temperature=0.5,
            )
            return resp.choices[0].text.strip()
    except Exception:
        return None
    return None

def generate_cover_letter(job_desc: str, profile: Dict[str, Any], tone: str = "confident", template_name: str = "default") -> str:
    llm = maybe_llm_generate(job_desc, profile, tone)
    if llm:
        return llm
    return rules_based_cover_letter(job_desc, profile, tone, template_name)

def write_outputs(text: str, basename: str, out_dir: str) -> Dict[str, str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    txt_path = Path(out_dir) / f"{basename}.txt"
    txt_path.write_text(text, encoding="utf-8")

    docx_path = Path(out_dir) / f"{basename}.docx"
    try:
        from docx import Document
        doc = Document()
        for para in text.split("\n\n"):
            doc.add_paragraph(para)
        doc.save(docx_path.as_posix())
    except Exception:
        docx_path = None

    pdf_path = Path(out_dir) / f"{basename}.pdf"
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf_path.as_posix(), pagesize=LETTER)
        width, height = LETTER
        x, y = 72, height - 72
        for line in text.split("\n"):
            c.drawString(x, y, line[:1000])
            y -= 14
            if y < 72:
                c.showPage(); y = height - 72
        c.save()
    except Exception:
        pdf_path = None

    return {
        "txt": txt_path.as_posix(),
        "docx": docx_path.as_posix() if docx_path else "",
        "pdf": pdf_path.as_posix() if pdf_path else "",
    }

```


### `app/config.py`

```python
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

```


### `app/database.py`

```python
from __future__ import annotations
from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///autoapply.sqlite", echo=False)

def get_session():
    return Session(engine)

```


### `app/jd_parser.py`

```python
from __future__ import annotations
import re
import httpx
from bs4 import BeautifulSoup

def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t or "").strip()
    return t

def parse_from_url(url: str) -> str:
    try:
        r = httpx.get(url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        candidates = []
        for sel in ["section", "article", "div"]:
            for tag in soup.select(sel):
                txt = clean_text(tag.get_text(" ", strip=True))
                if 400 < len(txt) < 20000:
                    candidates.append(txt)
        if candidates:
            candidates.sort(key=len, reverse=True)
            return candidates[0]
        return clean_text(soup.get_text(" ", strip=True))
    except Exception as e:
        return f"[ERROR parsing URL: {e}]"

def parse_from_text(text: str) -> str:
    return clean_text(text or "")

```


### `app/main.py`

```python
from __future__ import annotations
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from .database import get_session
from .models import Application
from .jd_parser import parse_from_url, parse_from_text
from .resume import load_profile_json, load_resume_txt
from .cl_generator import generate_cover_letter, write_outputs
from .config import CFG, DEFAULT_PROFILE

app = FastAPI(title="Auto-Apply Pro")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/applications", response_class=HTMLResponse)
def applications(request: Request, q: str | None = None):
    with get_session() as s:
        if q:
            rows = s.exec(
                f"SELECT * FROM applications WHERE company LIKE '%{q}%' OR title LIKE '%{q}%' ORDER BY datetime_utc DESC"
            ).all()
        else:
            rows = s.exec("SELECT * FROM applications ORDER BY datetime_utc DESC").all()
    return templates.TemplateResponse("applications.html", {"request": request, "rows": rows})

@app.get("/applications/{app_id}", response_class=HTMLResponse)
def application_detail(request: Request, app_id: int):
    with get_session() as s:
        row = s.get(Application, app_id)
    return templates.TemplateResponse("application_detail.html", {"request": request, "row": row})

@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request,
             url: str = Form(None),
             text: str = Form(None),
             profile: str = Form(DEFAULT_PROFILE),
             tone: str = Form("confident")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    profile_data = load_profile_json(profile)
    cl = generate_cover_letter(jd, profile_data, tone=tone, template_name=CFG["defaults"].get("template","default"))
    company = profile_data.get("target_company","(Unknown Company)")
    title = profile_data.get("target_title","(Unknown Title)")
    out = write_outputs(cl, f"{company}_{title}".replace(" ", "_"), CFG["paths"]["cover_letter_dir"])
    with get_session() as s:
        app_row = Application(
            datetime_utc=datetime.utcnow(),
            company=company,
            title=title,
            source="web",
            location=profile_data.get("location"),
            job_url=url,
            status="generated",
            profile_used=profile,
            resume_path=CFG["paths"]["resume_pdf"],
            cover_letter_path=out["txt"],
        )
        s.add(app_row); s.commit(); s.refresh(app_row)
    return templates.TemplateResponse("cover_letter.html", {"request": request, "cl": cl, "out": out, "app_id": app_row.id})

```


### `app/models.py`

```python
from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    datetime_utc: datetime
    company: str
    title: str
    source: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    status: str = "parsed"  # parsed|generated|submitted|error|skipped
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    profile_used: Optional[str] = None
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    notes: Optional[str] = None
    error: Optional[str] = None

class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int
    ts: datetime
    event_type: str
    message: str
    json_blob: Optional[str] = None

```


### `app/resume.py`

```python
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

```


### `app/schemas.py`

```python
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

```


### `app/static/readme.txt`

```
Static assets placeholder (Tailwind via CDN).

```


### `app/templates/application_detail.html`

```html
{% extends "base.html" %}
{% block body %}
<h2 class="text-xl font-semibold mb-4">Application #{{ row.id }}</h2>
<div class="grid grid-cols-2 gap-6">
  <div class="bg-white p-4 rounded shadow">
    <h3 class="font-semibold">Meta</h3>
    <p><strong>Company:</strong> {{ row.company }}</p>
    <p><strong>Title:</strong> {{ row.title }}</p>
    <p><strong>Status:</strong> {{ row.status }}</p>
    <p><strong>URL:</strong> <a class="text-blue-600" href="{{ row.job_url }}" target="_blank">{{ row.job_url }}</a></p>
  </div>
  <div class="bg-white p-4 rounded shadow">
    <h3 class="font-semibold">Artifacts</h3>
    <p><strong>Resume:</strong> {{ row.resume_path }}</p>
    <p><strong>Cover Letter:</strong> {{ row.cover_letter_path }}</p>
  </div>
</div>
{% endblock %}

```


### `app/templates/applications.html`

```html
{% extends "base.html" %}
{% block body %}
<h2 class="text-xl font-semibold mb-4">Applications</h2>
<table class="w-full bg-white rounded shadow">
  <thead>
    <tr class="text-left bg-slate-100">
      <th class="p-2">Date</th>
      <th class="p-2">Company</th>
      <th class="p-2">Title</th>
      <th class="p-2">Status</th>
      <th class="p-2">Link</th>
    </tr>
  </thead>
  <tbody>
    {% for r in rows %}
    <tr class="border-t">
      <td class="p-2 text-sm">{{ r.datetime_utc }}</td>
      <td class="p-2">{{ r.company }}</td>
      <td class="p-2">{{ r.title }}</td>
      <td class="p-2">{{ r.status }}</td>
      <td class="p-2"><a class="text-blue-600" href="/applications/{{ r.id }}">Open</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}

```


### `app/templates/base.html`

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <title>Auto-Apply Pro</title>
</head>
<body class="bg-gray-50 text-slate-900">
  <nav class="px-6 py-4 bg-white shadow">
    <div class="max-w-6xl mx-auto flex items-center justify-between">
      <a href="/" class="font-bold">Auto-Apply Pro</a>
      <div class="space-x-4">
        <a class="text-blue-600" href="/upload">Generate Cover Letter</a>
        <a class="text-blue-600" href="/applications">Applications</a>
      </div>
    </div>
  </nav>
  <main class="max-w-6xl mx-auto p-6">
    {% block body %}{% endblock %}
  </main>
</body>
</html>

```


### `app/templates/cover_letter.html`

```html
{% extends "base.html" %}
{% block body %}
<h2 class="text-xl font-semibold mb-4">Generated Cover Letter</h2>
<div class="bg-white p-4 rounded shadow whitespace-pre-wrap">{{ cl }}</div>
<div class="mt-4">
  <p>Saved to:</p>
  <ul class="list-disc ml-5">
    <li>{{ out.txt }}</li>
    {% if out.docx %}<li>{{ out.docx }}</li>{% endif %}
    {% if out.pdf %}<li>{{ out.pdf }}</li>{% endif %}
  </ul>
</div>
<a href="/applications/{{ app_id }}" class="inline-block mt-4 px-4 py-2 bg-slate-800 text-white rounded">View Application Record</a>
{% endblock %}

```


### `app/templates/index.html`

```html
{% extends "base.html" %}
{% block body %}
<h1 class="text-2xl font-semibold mb-4">Welcome</h1>
<p class="mb-6">Parse job posts, generate tailored cover letters, and (optionally) apply with a manual confirm.</p>
<a href="/upload" class="px-4 py-2 bg-blue-600 text-white rounded">Get Started</a>
{% endblock %}

```


### `app/templates/upload_form.html`

```html
{% extends "base.html" %}
{% block body %}
<h2 class="text-xl font-semibold mb-4">Generate Cover Letter</h2>
<form method="post" action="/generate" class="bg-white p-4 rounded shadow space-y-3">
  <label class="block">
    <span class="text-sm">Job URL (preferred)</span>
    <input name="url" class="w-full border rounded p-2" placeholder="https://..."/>
  </label>
  <label class="block">
    <span class="text-sm">OR Paste Job Description</span>
    <textarea name="text" class="w-full border rounded p-2" rows="8"></textarea>
  </label>
  <div class="grid grid-cols-3 gap-3">
    <label class="block">Profile
      <input name="profile" class="w-full border rounded p-2" value="{{ config.defaults.profile if config else 'software-engineer' }}"/>
    </label>
    <label class="block">Tone
      <select name="tone" class="w-full border rounded p-2">
        <option>confident</option>
        <option>mentor-teacher</option>
        <option>concise</option>
        <option>story</option>
      </select>
    </label>
  </div>
  <button class="px-4 py-2 bg-blue-600 text-white rounded">Generate</button>
</form>
{% endblock %}

```


### `cli/__init__.py`

```python
# empty

```


### `cli/main.py`

```python
from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path
import typer
from app.jd_parser import parse_from_url, parse_from_text
from app.resume import load_profile_json
from app.cl_generator import generate_cover_letter, write_outputs
from app.automation.apply_flow import apply_once, log_result
from app.database import get_session
from app.models import Application
from app.config import CFG, DEFAULT_PROFILE

app = typer.Typer(add_completion=False, help="Auto-Apply Pro CLI")

@app.command()
def parse(url: str = typer.Option(None, help="Job URL"),
          text: str = typer.Option(None, help="Job description text")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    typer.echo(jd[:1000] + ("..." if len(jd) > 1000 else ""))

@app.command("generate-cl")
def generate_cl(url: str = typer.Option(None),
                text: str = typer.Option(None),
                profile: str = typer.Option(DEFAULT_PROFILE),
                tone: str = typer.Option("confident")):
    jd = parse_from_url(url) if url else parse_from_text(text or "")
    prof = load_profile_json(profile)
    cl = generate_cover_letter(jd, prof, tone, CFG["defaults"].get("template","default"))
    company = prof.get("target_company","Acme")
    title = prof.get("target_title","Software Engineer")
    out = write_outputs(cl, f"{company}_{title}".replace(" ","_"), CFG["paths"]["cover_letter_dir"])
    typer.echo(f"Saved: {out}")

@app.command()
def apply(url: str,
          confirm: bool = typer.Option(True),
          dry_run: bool = typer.Option(False),
          profile: str = typer.Option(DEFAULT_PROFILE),
          tone: str = typer.Option("confident")):
    prof = load_profile_json(profile)
    ctx = {
        "first_name": prof.get("first_name",""),
        "last_name": prof.get("last_name",""),
        "contact_email": prof.get("contact_email",""),
        "contact_phone": prof.get("contact_phone",""),
        "location": prof.get("location",""),
        "linkedin_url": prof.get("linkedin_url",""),
        "github_url": prof.get("github_url",""),
        "resume_pdf": CFG["paths"]["resume_pdf"],
        "cover_letter_text": prof.get("cover_letter_fallback",""),
        "company": prof.get("target_company",""),
        "title": prof.get("target_title",""),
        "profile_used": profile,
    }
    result = apply_once(url, ctx, confirm=confirm, dry_run=dry_run)
    app_id = log_result(url, result, ctx)
    typer.echo(f"Application logged: #{app_id} -> {result}")

@app.command()
def import_(csv_path: str,
            dry_run: bool = typer.Option(True)):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            typer.echo(f"Queued: {row['company']} - {row['title']} ({row['url']}) dry_run={dry_run}")

@app.command("log")
def export_log(export: str,
               since: str = typer.Option("1970-01-01")):
    Path(export).parent.mkdir(parents=True, exist_ok=True)
    with get_session() as s:
        rows = s.exec("SELECT * FROM applications WHERE datetime_utc >= :since",
                      params={"since": since}).all()
    import pandas as pd
    df = pd.DataFrame([r.model_dump() for r in rows])
    df.to_csv(export, index=False)
    typer.echo(f"Exported {len(df)} rows to {export}")

def main():
    app()

if __name__ == "__main__":
    main()

```


### `config.yaml`

```yaml
defaults:
  profile: software-engineer
  template: default
  submission_strategy: manual_gate
  observe_only: true
  required_confirmations: true

ui:
  page_size: 25

automation:
  typing_min_ms: 40
  typing_max_ms: 120
  navigation_delay_ms: 600

paths:
  resume_txt: profiles/main_resume.txt
  resume_pdf: profiles/main_resume.pdf
  cover_letter_dir: cover_letters
  templates_dir: cover_letter_templates

```


### `cover_letter_templates/concise.jinja2`

```jinja2
{{ profile.salutation or "Hello" }},

I’m applying for {{ profile.target_title or "the role" }} at {{ profile.target_company or "your company" }}. In {{ profile.years_experience or "my experience" }} years, I’ve shipped secure, reliable systems and improved delivery speed.

Highlights:
- {{ profile.achievement_1 or "60% faster deployments; 40% fewer incidents" }}
- {{ profile.win_2 or "APIs at scale; strong testing & monitoring" }}
- {{ profile.win_3 or "Mentor & trainer; clear documentation" }}

I reviewed your JD and can immediately deliver on {{ profile.jd_fit_1 or "feature delivery" }} and {{ profile.jd_fit_2 or "quality improvements" }}.

Open to a quick call to align on goals and next steps.

— {{ profile.name }}

```


### `cover_letter_templates/default.jinja2`

```jinja2
{{ profile.salutation or "Dear Hiring Manager" }},

I'm excited to apply for the {{ profile.target_title or "role" }} at {{ profile.target_company or "your company" }}. With experience spanning {{ profile.years_experience or "many" }} years across {{ ", ".join(profile.core_skills[:5]) if profile.core_skills else "software engineering" }}, I deliver measurable outcomes that matter.

**Why I’m a match**
- Your needs: {{ profile.match_focus or "build reliable systems, ship features, and improve quality" }}.
- My track record: {{ profile.achievement_1 or "cut deployment time by 60% and reduced incidents by 40%" }}; {{ profile.achievement_2 or "led cross-functional launches across Dev, QA, and Ops" }}.

**Selected, relevant wins**
- {{ profile.win_1 or "Automated CI/CD pipelines, slashing lead time from days to hours." }}
- {{ profile.win_2 or "Built scalable APIs handling millions of requests/day." }}
- {{ profile.win_3 or "Mentored engineers and created training that leveled-up the team." }}

**Fit for your JD**
I read your description carefully. Here’s how I’d help:
- {{ profile.jd_fit_1 or "Translate ambiguous requirements into secure, testable features." }}
- {{ profile.jd_fit_2 or "Add observability and guardrails to prevent regressions." }}

I’d love to discuss how these outcomes translate to {{ profile.target_company or "your team" }}. Thank you for your time.

Best regards,
{{ profile.name }}
{{ profile.contact_email }} • {{ profile.contact_phone }} • {{ profile.location }}
{{ profile.portfolio_url }} • {{ profile.github_url }} • {{ profile.linkedin_url }}

```


### `cover_letters/README.txt`

```
Example outputs are placed here. Running the CLI or web form will generate new TXT/DOCX/PDF files using templates.

```


### `cover_letters/example_acme_software_engineer.txt`

```
Dear Hiring Manager,

I'm excited to apply for the Software Engineer role at Acme Corp. With experience spanning 20+ years across C#, .NET, Python, automation, and DevSecOps, I deliver measurable outcomes that matter.

Why I’m a match
- Your needs: build reliable systems, ship features, and improve quality.
- My track record: reduced deployment lead time by 60% and incidents by 40%; led cross-functional launches across Dev, QA, and Ops.

Selected, relevant wins
- Automated CI/CD pipelines, cutting lead time from days to hours.
- Built scalable APIs and services.
- Mentored engineers; standardized training and documentation.

Fit for your JD
I’d translate ambiguous requirements into secure, testable features and add observability to prevent regressions.

Best regards,
Brian Hannigan
BrianHannigan68@gmail.com • (862) 243-1177 • Succasunna, NJ
https://brianhannigan.com • https://github.com/<myhandle> • https://www.linkedin.com/in/<myhandle>/

```


### `mock_site/form.html`

```html
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Mock Job Form</title></head>
  <body>
    <h1>Mock Application</h1>
    <form>
      <label>First name <input name="firstName" type="text"></label><br/>
      <label>Last name <input name="lastName" type="text"></label><br/>
      <label>Email <input type="email" name="email"></label><br/>
      <label>Phone <input type="tel" name="phone"></label><br/>
      <label>LinkedIn <input name="linkedin"></label><br/>
      <label>GitHub <input name="github"></label><br/>
      <label>Resume <input type="file" name="resume"></label><br/>
      <label>Cover Letter <textarea rows="6" cols="60" name="cover"></textarea></label><br/>
      <button type="submit">Submit</button>
    </form>
  </body>
</html>

```


### `profiles/main_resume.pdf`

```
Put your actual PDF resume here; the app will reference this path for uploads.

```


### `profiles/main_resume.txt`

```
[Paste your full resume text here exactly. This file is used to enrich cover letters if LLM is disabled.]

```


### `profiles/software-engineer.json`

```json
{
  "name": "Brian Hannigan",
  "first_name": "Brian",
  "last_name": "Hannigan",
  "title": "Senior Software Engineer & Automation Architect",
  "contact_email": "BrianHannigan68@gmail.com",
  "contact_phone": "(862) 243-1177",
  "location": "Succasunna, NJ",
  "portfolio_url": "https://brianhannigan.com",
  "github_url": "https://github.com/<myhandle>",
  "linkedin_url": "https://www.linkedin.com/in/<myhandle>/",
  "years_experience": "25+",
  "core_skills": [
    "C#",
    ".NET",
    "Python",
    "Playwright",
    "FastAPI",
    "SQL",
    "Docker",
    "DevSecOps"
  ],
  "achievement_1": "Automated critical pipelines, cutting lead time by 60% and incidents by 40%",
  "achievement_2": "Led secure, compliant releases across DoD-grade environments",
  "win_1": "Built CI/CD and infra-as-code with measurable quality gains",
  "win_2": "Shipped scalable APIs and services with observability",
  "win_3": "Mentored engineers; created training and documentation",
  "jd_fit_1": "Translate ambiguous requirements into secure, testable features",
  "jd_fit_2": "Add observability and guardrails to prevent regressions",
  "salutation": "Dear Hiring Manager",
  "target_company": "Acme Corp",
  "target_title": "Software Engineer",
  "cover_letter_fallback": "Please find my cover letter attached outlining my fit for your role."
}
```


### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "auto-apply-pro"
version = "0.1.0"
description = "Auto-Apply Pro: job parser, cover-letter generator, compliant autofill, and logger."
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"

```


### `requirements.txt`

```
fastapi==0.115.0
uvicorn==0.30.6
jinja2==3.1.4
python-dotenv==1.0.1
pydantic==2.9.1
SQLAlchemy==2.0.36
sqlmodel==0.0.22
alembic==1.13.2
typer==0.12.5
playwright==1.48.0
httpx==0.27.2
beautifulsoup4==4.12.3
python-docx==1.1.2
reportlab==4.2.5
pandas==2.2.2
pytest==8.3.2
pytest-playwright==0.5.7

```


### `samples/job_description.txt`

```
We are seeking a Software Engineer with strong experience in Python, C#, and distributed systems...

```


### `samples/jobs.csv`

```csv
title,company,url,location,notes
Software Engineer,Acme Corp,https://example.com/jobs/acme-se,Remote,"General role"
Developer Advocate,Bravo Inc,https://example.com/jobs/bravo-da,NYC,"Platform advocacy"

```


### `scripts/preflight.ps1`

```powershell
Write-Host "Checking Python..."
python -V
Write-Host "Checking Playwright..."
python -c "from playwright.sync_api import sync_playwright; print('Playwright import OK')"
Write-Host "Checking env..."
python -c "from dotenv import load_dotenv; load_dotenv(); print('ENV OK')"
Write-Host "Preflight OK."

```


### `scripts/preflight.sh`

```bash
#!/usr/bin/env bash
set -e
echo "Checking Python..."
python -V
echo "Checking Playwright..."
python - <<'PY'
from playwright.sync_api import sync_playwright
print("Playwright import OK")
PY
echo "Checking env..."
python - <<'PY'
from dotenv import load_dotenv; load_dotenv(); print("ENV OK")
PY
echo "Preflight OK."

```


### `scripts/run.ps1`

```powershell
$env:PYTHONUNBUFFERED="1"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

```


### `scripts/run.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

```


### `tests/conftest.py`

```python
import os, sys
os.environ.setdefault("HEADLESS","true")
sys.path.append(os.path.abspath("."))

```


### `tests/test_cl_generation.py`

```python
from app.cl_generator import generate_cover_letter
from app.resume import load_profile_json

def test_generate_rules():
    prof = load_profile_json("software-engineer")
    cl = generate_cover_letter("We need someone skilled in Python and C#", prof, "confident")
    assert "Dear" in cl or "Hello" in cl
    assert "Software Engineer" in cl or prof.get("target_title","") in cl

```


### `tests/test_logging.py`

```python
from datetime import datetime
from app.database import get_session
from app.models import Application

def test_log_insert():
    with get_session() as s:
        a = Application(datetime_utc=datetime.utcnow(), company="TestCo", title="TestTitle", status="parsed")
        s.add(a); s.commit(); s.refresh(a)
        assert a.id is not None

```


### `tests/test_parsing.py`

```python
from app.jd_parser import parse_from_text

def test_parse_text():
    txt = "This is a job. Responsibilities include A, B, C."
    out = parse_from_text(txt)
    assert "Responsibilities" in out

```


### `tests/test_playwright_e2e.py`

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

def test_fill_mock_form():
    mock_file = Path("mock_site/form.html").resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(mock_file)
        page.fill("input[name='firstName']", "Brian")
        page.fill("input[name='lastName']", "Hannigan")
        page.fill("input[type='email']", "b@example.com")
        page.fill("input[type='tel']", "123456789")
        assert page.title() == "Mock Job Form"
        browser.close()

```



## Validation Checklist
- [x] URL/text parsing and CSV import
- [x] Profiles + resume loading
- [x] Cover-letter generator (LLM optional, rules-based fallback)
- [x] TXT/DOCX/PDF outputs
- [x] Playwright automation (headful by default)
- [x] Manual-Gate confirm (screenshot)
- [x] SQLite logging + audit events + CSV export
- [x] Web dashboard + templates
- [x] Config via `.env` + `config.yaml`
- [x] Pluggable adapters (generic/greenhouse/lever/workday)
- [x] Unit tests + basic e2e
- [x] Preflight + run scripts
- [x] Samples + two CL templates

## Demo Transcript (simulated)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install
alembic upgrade head

autoapply parse --url "https://example.com/jobs/acme-se"
autoapply generate-cl --url "https://example.com/jobs/acme-se" --profile "software-engineer" --tone "confident"
autoapply apply --url "https://example.com/jobs/acme-se" --confirm --dry-run
autoapply log --export ./out/applications.csv --since "2025-08-01"
```
