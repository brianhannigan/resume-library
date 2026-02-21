# Job Harvester (Starter Kit)

Pull **new job postings** from multiple sources and save them to CSV/JSON.
- ✅ **USAJOBS** (official API — reliable & ToS-compliant)
- ✅ **RSS/Atom feeds** (e.g., **Indeed** query RSS, corporate career RSS, Workable/Greenhouse feeds, etc.)

> This starter avoids brittle scraping. You can add more providers later (Lever/Greenhouse JSON, Workday, Ashby) or a Playwright module for sites without APIs.

---

## Quick Start

1) **Python 3.11+** recommended.
2) Install deps:

```bash
pip install -r requirements.txt
```

3) Copy the example config and edit it:

```bash
cp config.example.yml config.yml
```

4) Export your USAJOBS credentials (free to get):
   - Get a key from https://developer.usajobs.gov/
   - Set environment variables (PowerShell):
```powershell
$env:USAJOBS_API_KEY="YOUR_KEY"
$env:USAJOBS_USER_AGENT="youremail@example.com"
```
   - Or Bash:
```bash
export USAJOBS_API_KEY="YOUR_KEY"
export USAJOBS_USER_AGENT="youremail@example.com"
```

5) Run a fetch for **today**:

```bash
python job_harvester.py --since today --config config.yml --out out
```

6) Results:
- CSV: `out/jobs_YYYY-MM-DD.csv`
- JSON: `out/jobs_YYYY-MM-DD.json`

---

## Sources supported

### USAJOBS (API)
- Filters by keywords, locations, remote, and posted date.
- Set **USAJOBS_API_KEY** and **USAJOBS_USER_AGENT** env vars.

### RSS (incl. Indeed query RSS)
- Any RSS/Atom URL in `config.yml -> rss_feeds`.
- Example for Indeed RSS:
  - US: `https://www.indeed.com/rss?q=python+developer&l=New+York%2C+NY`
  - Remote example: `https://www.indeed.com/rss?q=python+developer+remote`

> Tip: Add many feeds (keyword/location variants). The harvester will deduplicate by URL.

---

## Example commands

Fetch today only:
```bash
python job_harvester.py --since today
```

Fetch last 3 days:
```bash
python job_harvester.py --since "3d"
```

Fetch since an absolute date:
```bash
python job_harvester.py --since "2025-08-30"
```

Filter with keywords (must match title or description):
```bash
python job_harvester.py --since today -k "C#,.NET,Python,DevSecOps"
```

Only remote roles:
```bash
python job_harvester.py --since today --remote-only
```

Save to a custom folder:
```bash
python job_harvester.py --since today --out ./exports
```

---

## Extending

- Add providers (e.g., Lever, Greenhouse) by following the `collect_*` pattern in the script.
- Add a Playwright module if you truly need to navigate sites without feeds/APIs. Be mindful of ToS and robots.txt.
- For LinkedIn/Indeed web pages: prefer **RSS** or **official/company APIs** where available. Avoid scraping when prohibited.

---

## Output schema

Each job is normalized to:
```json
{
  "source": "usajobs|rss",
  "company": "string or null",
  "title": "string",
  "location": "string or null",
  "remote": true/false/null,
  "url": "string",
  "posted_at": "ISO8601 string or null",
  "description": "string or null",
  "raw": { ... provider specific fields ... }
}
```

---

## Notes

- If a source is temporarily down, the harvester continues and logs the error.
- Use cron/Task Scheduler to run daily and commit `out/` to GitHub to keep history (CSV is ATS-friendly).

---
