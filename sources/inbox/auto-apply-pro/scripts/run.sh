#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
