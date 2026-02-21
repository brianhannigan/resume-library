#!/usr/bin/env python3
import pathlib, yaml, textwrap

SRC = pathlib.Path("resumes/master.md")
OUT = pathlib.Path("dist/linkedin")
OUT.mkdir(parents=True, exist_ok=True)

def load_frontmatter_and_body(path: pathlib.Path):
    t = path.read_text(encoding="utf-8")
    if t.startswith('---'):
        parts = t.split('---', 2)
        if len(parts) >= 3:
            _, fm, body = parts
            return yaml.safe_load(fm) or {}, body.strip()
    return {}, t

fm, body = load_frontmatter_and_body(SRC)

headlines = [
"Senior Software Engineer | Technical Trainer | AI Automation | DoD-Grade Secure Systems",
"Lead .NET/C# Engineer • DevSecOps • VR/AR Training Systems • Security+",
"Developer Advocate & Trainer | C#/.NET | Python | Secure SDLC | AI Automation",
"Principal Software Engineer | DoD Simulation & Training | Unity/Unreal | DevSecOps",
"AI-Powered Senior Engineer | Secure Training Systems | Communication-First Leader"
]
(OUT / "headline_options.txt").write_text("\n".join(headlines)+"\n", encoding="utf-8")

about = textwrap.dedent("""
Senior Software Engineer and Educator with 25+ years designing, building, and delivering secure, high‑performance software—including 15 years in mission‑critical DoD environments. I combine C#/.NET and Python engineering with AI‑powered automation, DevSecOps, and VR/AR training systems to translate complex systems into clear solutions for developers, stakeholders, and end users.

Highlights:
• Led classroom control systems to orchestrate dozens of networked simulators
• Hardened deployments with STIG/Nessus + CI/CD
• Delivered training and documentation that improved adoption and reduced support load

Strengths: Communication, training, developer experience (DX), secure SDLC, and turning ambiguity into repeatable processes.
""")
(OUT / "about.txt").write_text(about+"\n", encoding="utf-8")

bullets = [
"Designed and delivered secure training systems for DoD programs using C#/.NET and Python.",
"Implemented DevSecOps practices (code reviews, STIG baselines, Nessus scans) to harden deployments.",
"Built instructor operator stations enabling classroom orchestration and real‑time assistance.",
"Containerized services with Docker; automated builds with GitHub Actions/Azure DevOps.",
"Developed REST APIs and data pipelines (SQL Server/SQLite).",
"Led cross‑functional teams; mentored engineers; ran workshops and brown bags.",
"Created VR/AR prototypes (Unity/Unreal) to validate scenarios and accelerate buy‑in.",
"Optimized classroom networks (TCP/IP, SSL, SSH)."
]
(OUT / "experience_bullet_bank.txt").write_text("\n".join("• "+b for b in bullets)+"\n", encoding="utf-8")
print(f"Wrote LinkedIn pack → {OUT}")
