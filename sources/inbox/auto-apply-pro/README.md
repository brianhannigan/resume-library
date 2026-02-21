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
