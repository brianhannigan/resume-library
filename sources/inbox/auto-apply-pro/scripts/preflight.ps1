Write-Host "Checking Python..."
python -V
Write-Host "Checking Playwright..."
python -c "from playwright.sync_api import sync_playwright; print('Playwright import OK')"
Write-Host "Checking env..."
python -c "from dotenv import load_dotenv; load_dotenv(); print('ENV OK')"
Write-Host "Preflight OK."
