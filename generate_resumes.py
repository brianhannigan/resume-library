from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, List

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resumes"
CONFIG_PATH = ROOT / "resume_config.json"


# =========================
# CONFIG
# =========================
@dataclass
class ResumeConfig:
    name: str = "BRIAN HANNIGAN"
    phone: str = "(862) 243-1177"
    email: str = "jobshannigan@gmail.com"
    linkedin: str = "linkedin.com/in/brianjhannigan"
    github: str = "github.com/brianhannigan"
    location: str = "Remote | 07876"
    libreoffice_path: str = ""


def load_config() -> ResumeConfig:
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        base = asdict(ResumeConfig())
        base.update(data)
        return ResumeConfig(**base)
    cfg = ResumeConfig()
    save_config(cfg)
    return cfg


def save_config(cfg: ResumeConfig):
    CONFIG_PATH.write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")


# =========================
# DOC HELPERS
# =========================
def set_doc_margins(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)


def add_title(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_subtitle(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_section(doc, title):
    p = doc.add_paragraph()
    run = p.add_run(title.upper())
    run.bold = True
    run.font.size = Pt(11.5)


def add_bullets(doc, bullets):
    for b in bullets:
        p = doc.add_paragraph(b, style="List Bullet")
        for r in p.runs:
            r.font.size = Pt(10.5)


def save_txt(path: Path, lines: List[str]):
    path.write_text("\n".join(lines), encoding="utf-8")


# =========================
# LIBREOFFICE
# =========================
def find_soffice(cfg: ResumeConfig) -> Optional[str]:
    if cfg.libreoffice_path and Path(cfg.libreoffice_path).exists():
        return cfg.libreoffice_path

    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    default = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
    if default.exists():
        return str(default)

    return None


def convert(docx_path: Path, fmt: str, cfg: ResumeConfig) -> Path:
    soffice = find_soffice(cfg)
    if not soffice:
        raise FileNotFoundError("LibreOffice not found.")

    cmd = [
        soffice,
        "--headless",
        "--convert-to",
        fmt,
        "--outdir",
        str(docx_path.parent),
        str(docx_path),
    ]
    subprocess.run(cmd, check=True)

    return docx_path.parent / f"{docx_path.stem}.{fmt}"


# =========================
# CONTENT TEMPLATES
# =========================
def content_for_variant(variant: str):
    summaries = {
        "general": "Senior Software Engineer and Systems Architect delivering secure, scalable enterprise systems.",
        "python-backend": "Backend-focused Python Engineer specializing in REST APIs and modular service design.",
        "cybersecurity": "Cybersecurity Engineer specializing in SIEM, detection engineering, and secure systems.",
        "ai-architect": "AI Systems Architect designing offline-first AI deployments and model orchestration.",
        "grc-analyst": "GRC Analyst specializing in compliance, risk assessments, HIPAA, SOC 2, and NIST alignment.",
    }

    skills = {
        "general": ["System Architecture", "Enterprise Applications", "Secure Deployment"],
        "python-backend": ["Python", "REST APIs", "SQL", "Git", "Docker"],
        "cybersecurity": ["SIEM", "KQL", "Threat Hunting", "STIGs", "Vulnerability Management"],
        "ai-architect": ["LLMs", "Model Hosting", "AI Integration", "Prompt Engineering"],
        "grc-analyst": ["NIST", "SOC 2", "HIPAA", "Risk Assessments", "Audit Documentation"],
    }

    return summaries[variant], skills[variant]


# =========================
# MAIN BUILDER
# =========================
def build_variant(
    variant: str,
    cfg: ResumeConfig,
    also_odt: bool = False,
    also_pdf: bool = False,
) -> Dict[str, Path]:

    summary, skills = content_for_variant(variant)

    out_dir = OUT / variant
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = Document()
    set_doc_margins(doc)

    add_title(doc, cfg.name)
    add_subtitle(doc, f"{cfg.location} | {cfg.phone} | {cfg.email}")
    add_subtitle(doc, f"LinkedIn: {cfg.linkedin} | GitHub: {cfg.github}")

    add_section(doc, "Professional Summary")
    doc.add_paragraph(summary)

    add_section(doc, "Core Skills")
    add_bullets(doc, skills)

    docx_path = out_dir / f"brian-hannigan-{variant}.docx"
    doc.save(str(docx_path))

    txt_path = out_dir / f"brian-hannigan-{variant}.txt"
    save_txt(txt_path, [cfg.name, summary] + skills)

    result = {"docx": docx_path, "txt": txt_path}

    if also_odt:
        result["odt"] = convert(docx_path, "odt", cfg)

    if also_pdf:
        result["pdf"] = convert(docx_path, "pdf", cfg)

    return result