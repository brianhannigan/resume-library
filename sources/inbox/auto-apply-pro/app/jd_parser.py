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
