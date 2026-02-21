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
