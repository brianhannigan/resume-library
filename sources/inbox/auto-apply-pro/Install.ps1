# Requires: PowerShell 5+ and Python 3.11+
$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "➤ $msg" }
function Fail($msg) { Write-Host ""; Write-Host "$msg" -ForegroundColor Red; exit 1 }

# --- Project root check ---
if (!(Test-Path "requirements.txt")) { Fail "Run this from the project root (requirements.txt not found)" }
if (!(Test-Path "config.yaml")) { Fail "Run this from the project root (config.yaml not found)" }

# --- Python detection ---
$python = $env:PYTHON_BIN
if (-not $python) {
  if (Get-Command py -ErrorAction SilentlyContinue) { $python = "py" }
  elseif (Get-Command python -ErrorAction SilentlyContinue) { $python = "python" }
  else { Fail "Python not found. Install Python 3.11+ and re-run." }
}

# Version check
$ver = & $python - << 'PY'
import sys; print(".".join(map(str, sys.version_info[:3])))
PY
Write-Info "Python: $ver"
$maj,$min,$patch = $ver.Split(".")
if ([int]$maj -lt 3 -or ([int]$maj -eq 3 -and [int]$min -lt 11)) { Fail "Python 3.11+ required (found $ver)." }

# --- Virtualenv ---
Write-Info "Creating virtual environment (.venv)..."
& $python -m venv .venv

# Activate for this session
$venvActivate = ".\.venv\Scripts\Activate.ps1"
. $venvActivate

Write-Info "Upgrading pip..."
python -m pip install -U pip

# --- Dependencies ---
Write-Info "Installing requirements..."
pip install -r requirements.txt

# --- Playwright browsers ---
Write-Info "Installing Playwright browsers..."
playwright install

# --- Database migrations ---
Write-Info "Applying migrations (alembic upgrade head)..."
alembic upgrade head

# --- .env setup ---
if (!(Test-Path ".env")) {
  Write-Info "Creating .env from .env.example..."
  if (Test-Path ".env.example") {
    Copy-Item ".env.example" ".env"
  } else {
    @"
LLM_PROVIDER=
LLM_API_KEY=
HEADLESS=false
RATE_LIMIT_MIN_MS=250
RATE_LIMIT_MAX_MS=800
DEFAULT_PROFILE=software-engineer
"@ | Out-File -Encoding UTF8 ".env"
  }
}

# --- Convenience wrappers ---
New-Item -ItemType Directory -Force -Path "scripts" | Out-Null

# PowerShell wrapper for CLI
@'
param([Parameter(ValueFromRemainingArguments=$true)] [string[]]$Args)
$ROOT = Split-Path -Parent $PSScriptRoot
. "$ROOT\.venv\Scripts\Activate.ps1"
python -m cli.main @Args
'@ | Out-File -Encoding UTF8 "scripts\autoapply.ps1"
# Allow running this script locally
Unblock-File "scripts\autoapply.ps1"

# PowerShell wrapper to run API/UI
@'
$ROOT = Split-Path -Parent $PSScriptRoot
. "$ROOT\.venv\Scripts\Activate.ps1"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
'@ | Out-File -Encoding UTF8 "scripts\run.ps1"
Unblock-File "scripts\run.ps1"

# Optional preflight
@'
python -V
python - << "PY"
from dotenv import load_dotenv; load_dotenv(); print("ENV OK")
PY
python - << "PY"
from playwright.sync_api import sync_playwright
print("Playwright import OK")
PY
Write-Host "Preflight OK."
'@ | Out-File -Encoding UTF8 "scripts\preflight.ps1"
Unblock-File "scripts\preflight.ps1"

# --- Summary ---
@"
✅ Install complete!

Next steps:
  1) Activate venv     :  .\.venv\Scripts\Activate.ps1
  2) Run API/UI        :  .\scripts\run.ps1   (open http://127.0.0.1:8000)
  3) CLI examples      :  .\scripts\autoapply.ps1 parse --url "https://example.com/jobs/acme-se"
                          .\scripts\autoapply.ps1 generate-cl --url "..." --profile "software-engineer" --tone "confident"
                          .\scripts\autoapply.ps1 apply --url "..." --confirm --dry-run
                          .\scripts\autoapply.ps1 log --export .\out\apps.csv --since "2025-08-01"

Tip: Edit .env and config.yaml to adjust defaults (e.g., HEADLESS, rate limits, profile).
"@ | Write-Host
