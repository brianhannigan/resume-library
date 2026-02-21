#!/usr/bin/env python3
import os, textwrap, json, pathlib, yaml
from datetime import date, timedelta

SRC = pathlib.Path("resumes/master.md")
OUT = pathlib.Path("dist/posts")
OUT.mkdir(parents=True, exist_ok=True)

def load_frontmatter_and_body(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            _, fm, body = parts
            data = yaml.safe_load(fm) or {}
            return data, body.strip()
    return {}, text

fm, body = load_frontmatter_and_body(SRC)
name = fm.get("name", "Your Name")
headline = fm.get("headline", "Senior Software Engineer | Trainer | AI Automation")
skills = fm.get("skills", [])
certs  = fm.get("certifications", [])
highlights = fm.get("highlights", [])

posts = []

# Skill spotlights
for s in skills[:10]:
    posts.append(textwrap.dedent(f"""
Skill Spotlight: {s}

How I apply **{s}**:
• What it solves: …
• My approach: …
• Example win: …

#hiring #software #engineering #career
"""))

# Communication/training
posts.append(textwrap.dedent(f"""
I love translating complex systems into clear, actionable steps for teams and stakeholders.
3 ways I do that:
• Visual models + demos
• Clear SOPs + checklists
• Hands-on workshops with real-world scenarios
#training #communication #devrel
"""))

# Project highlights
for h in highlights[:10]:
    title = h.get('title','Project Highlight')
    context = h.get('context','')
    impact = h.get('impact','')
    tech = ', '.join(h.get('tech', []))
    posts.append(textwrap.dedent(f"""
Project Highlight: {title}
Context: {context}
Impact: {impact}
Tech: {tech}
#DoD #securecoding #automation #VR #AR
"""))

# Certifications
if certs:
    posts.append(textwrap.dedent("""
Proud of the credentials that back my work:
""") + "\n".join(f"- {c}" for c in certs))

# Write up to 30 posts
today = date.today()
for i, p in enumerate(posts[:30], start=1):
    (OUT / f"post_{i:02d}_{today.isoformat()}.md").write_text(p.strip()+"\n", encoding="utf-8")
print(f"Generated {min(30, len(posts))} posts → {OUT}")
