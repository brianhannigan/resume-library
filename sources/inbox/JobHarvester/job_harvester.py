#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser
from dateutil.tz import gettz
import pytz
import requests
import feedparser
import yaml
import backoff

# -------- Utilities --------

def log(msg):
    print(f"[job-harvester] {msg}", flush=True)

def parse_since(since_str, tz_str="UTC"):
    tz = pytz.timezone(tz_str)
    now = datetime.now(tz)
    s = since_str.strip().lower()
    if s == "today":
        return tz.localize(datetime(now.year, now.month, now.day, 0, 0, 0))
    if s.endswith("d") and s[:-1].isdigit():
        days = int(s[:-1])
        return now - timedelta(days=days)
    try:
        dt = dtparser.parse(since_str)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt.astimezone(tz)
    except Exception:
        raise ValueError(f"Invalid --since value: {since_str}")

def to_iso(dt_obj):
    if not dt_obj:
        return None
    if isinstance(dt_obj, str):
        return dt_obj
    return dt_obj.astimezone(timezone.utc).isoformat()

def coalesce(*vals):
    for v in vals:
        if v not in (None, ""):
            return v
    return None

def boolish(val):
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in ("true", "yes", "1"):
        return True
    if s in ("false", "no", "0"):
        return False
    return None

def infer_remote_from_text(*fields):
    text = " ".join([f for f in fields if f]).lower()
    tokens = ["remote", "work from home", "wfh", "telework", "telecommute"]
    return any(t in text for t in tokens)

def dedup_by_url(items):
    seen = set()
    out = []
    for it in items:
        url = it.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(it)
    return out

# -------- USAJOBS --------

USAJOBS_ENDPOINT = "https://data.usajobs.gov/api/search"

def usajobs_enabled(cfg):
    return bool(cfg.get("usajobs", {}).get("enabled", False))

def _usajobs_headers():
    api_key = os.getenv("USAJOBS_API_KEY")
    user_agent = os.getenv("USAJOBS_USER_AGENT")
    if not api_key or not user_agent:
        raise RuntimeError("USAJOBS_API_KEY and USAJOBS_USER_AGENT must be set in env.")
    return {
        "Host": "data.usajobs.gov",
        "User-Agent": user_agent,
        "Authorization-Key": api_key,
        "Accept": "application/json",
    }

@backoff.on_exception(backoff.expo, (requests.RequestException,), max_tries=5, jitter=backoff.full_jitter)
def _usajobs_request(params):
    r = requests.get(USAJOBS_ENDPOINT, headers=_usajobs_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def collect_usajobs(cfg, since_dt, keywords=None, remote_only=False):
    results = []
    params = {
        "ResultsPerPage": cfg.get("usajobs", {}).get("results_per_page", 50),
        "Page": 1,
    }

    kw = keywords or cfg.get("usajobs", {}).get("keywords") or []
    if isinstance(kw, list):
        params["Keyword"] = " ".join(kw)
    elif isinstance(kw, str):
        params["Keyword"] = kw

    locs = cfg.get("usajobs", {}).get("locations") or []
    if isinstance(locs, list) and locs:
        params["LocationName"] = ";".join(locs)
    elif isinstance(locs, str) and locs:
        params["LocationName"] = locs

    # USAJOBS date filter: DatePosted is in days (e.g., 1 for last 24h)
    days_ago = max(0, (datetime.now(since_dt.tzinfo) - since_dt).days)
    if days_ago <= 31:
        params["DatePosted"] = days_ago if days_ago > 0 else 1

    total_pages = 1
    page = 1
    while page <= total_pages:
        params["Page"] = page
        data = _usajobs_request(params)
        if not data or "SearchResult" not in data:
            break
        meta = data["SearchResult"].get("SearchResultSummary", {})
        total_pages = int(meta.get("UserArea", {}).get("NumberOfPages", 1)) or 1
        for obj in data["SearchResult"].get("SearchResultItems", []):
            d = obj.get("MatchedObjectDescriptor", {})
            title = d.get("PositionTitle")
            company = d.get("OrganizationName")
            url = d.get("PositionURI")
            location = ", ".join([coalesce(loc.get("CityName"), loc.get("CountrySubDivisionCode"), loc.get("CountryCode")) 
                                  for loc in d.get("PositionLocation", [])]) if d.get("PositionLocation") else None
            posted_raw = coalesce(d.get("PublicationStartDate"), d.get("PositionStartDate"))
            posted_at = None
            try:
                if posted_raw:
                    posted_at = dtparser.parse(posted_raw)
            except Exception:
                posted_at = None

            description = d.get("UserArea", {}).get("Details", {}).get("JobSummary")
            remote_inferred = infer_remote_from_text(title, location, description)
            remote_flag = remote_inferred

            item = {
                "source": "usajobs",
                "company": company,
                "title": title,
                "location": location,
                "remote": remote_flag,
                "url": url,
                "posted_at": to_iso(posted_at),
                "description": description,
                "raw": d,
            }
            # strict since filter
            if posted_at and posted_at.tzinfo is None:
                posted_at = posted_at.replace(tzinfo=timezone.utc)
            if not posted_at or posted_at >= since_dt:
                if not remote_only or remote_flag:
                    results.append(item)
        page += 1

    return results

# -------- RSS / Atom (Incl. Indeed) --------

@backoff.on_exception(backoff.expo, (Exception,), max_tries=5, jitter=backoff.full_jitter)
def _rss_fetch(url):
    return feedparser.parse(url)

def collect_rss(cfg, since_dt, keywords=None, remote_only=False):
    items = []
    feeds = cfg.get("rss_feeds", []) or []
    incl = None
    if keywords:
        incl = [k.strip().lower() for k in keywords if k.strip()]

    for f in feeds:
        name = f.get("name") or f.get("url")
        url = f.get("url")
        if not url:
            continue
        try:
            fp = _rss_fetch(url)
            for e in fp.entries:
                title = e.get("title")
                link = e.get("link")
                summary = e.get("summary") or e.get("description")
                published = e.get("published") or e.get("updated")
                posted_at = None
                if published:
                    try:
                        posted_at = dtparser.parse(published)
                    except Exception:
                        posted_at = None

                location = None
                # Many feeds include location somewhere in summary/title — best-effort only
                # Company is rarely standardized in RSS; leave None unless found.
                company = None

                remote_flag = infer_remote_from_text(title, summary)
                if remote_only and not remote_flag:
                    continue

                if incl:
                    hay = " ".join([x for x in [title, summary] if x]).lower()
                    if not any(k in hay for k in incl):
                        continue

                ok_by_date = (not posted_at) or (posted_at.tzinfo and posted_at >= since_dt) or (posted_at and posted_at.replace(tzinfo=timezone.utc) >= since_dt)
                if not ok_by_date:
                    continue

                items.append({
                    "source": "rss",
                    "company": company,
                    "title": title,
                    "location": location,
                    "remote": remote_flag,
                    "url": link,
                    "posted_at": to_iso(posted_at),
                    "description": summary,
                    "raw": { "feed": name, "entry": e },
                })
        except Exception as ex:
            log(f"RSS fetch failed for {name}: {ex}")
            continue
    return items

# -------- Main --------

def load_config(path):
    if not path or not os.path.exists(path):
        return {"defaults": {"timezone": "UTC"}, "rss_feeds": [], "usajobs": {"enabled": False}}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_outputs(items, out_dir, label_date):
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"jobs_{label_date}.json")
    csv_path = os.path.join(out_dir, f"jobs_{label_date}.csv")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(items, jf, ensure_ascii=False, indent=2)

    # CSV with stable columns
    cols = ["source", "company", "title", "location", "remote", "url", "posted_at", "description"]
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        w = csv.DictWriter(cf, fieldnames=cols)
        w.writeheader()
        for it in items:
            w.writerow({k: it.get(k) for k in cols})
    return json_path, csv_path

def main():
    ap = argparse.ArgumentParser(description="Download new job postings from multiple sources.")
    ap.add_argument("--since", required=True, help='Examples: "today", "3d", "2025-08-30"')
    ap.add_argument("--config", default="config.yml", help="Path to YAML config.")
    ap.add_argument("--out", default="out", help="Output folder.")
    ap.add_argument("-k", "--keywords", default="", help="Comma-separated keyword filters (applied after fetch).")
    ap.add_argument("--remote-only", action="store_true", help="Only keep remote roles (heuristic).")
    args = ap.parse_args()

    cfg = load_config(args.config)
    tz_str = cfg.get("defaults", {}).get("timezone", "UTC")
    since_dt = parse_since(args.since, tz_str=tz_str)

    kw_list = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else None

    all_items = []

    if usajobs_enabled(cfg):
        try:
            log("Fetching USAJOBS...")
            all_items.extend(collect_usajobs(cfg, since_dt, keywords=kw_list, remote_only=args.remote_only))
        except Exception as ex:
            log(f"USAJOBS error: {ex}")

    log("Fetching RSS feeds...")
    all_items.extend(collect_rss(cfg, since_dt, keywords=kw_list, remote_only=args.remote_only))

    # Dedup + sort (newest first if posted_at available)
    all_items = dedup_by_url(all_items)
    def sort_key(it):
        try:
            return dtparser.parse(it.get("posted_at") or "") or datetime.min.replace(tzinfo=timezone.utc)
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)
    all_items.sort(key=sort_key, reverse=True)

    label_date = datetime.now().strftime("%Y-%m-%d")
    json_path, csv_path = save_outputs(all_items, args.out, label_date)
    log(f"Saved: {json_path}")
    log(f"Saved: {csv_path}")
    log(f"Total jobs: {len(all_items)}")

if __name__ == "__main__":
    main()
