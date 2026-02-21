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
