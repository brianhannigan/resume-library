from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
    libreoffice_path: str = ""  # optional; if empty we try PATH + common install location


def load_config() -> ResumeConfig:
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        base = asdict(ResumeConfig())
        base.update(data)
        return ResumeConfig(**base)
    cfg = ResumeConfig()
    save_config(cfg)
    return cfg


def save_config(cfg: ResumeConfig) -> None:
    CONFIG_PATH.write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")


# =========================
# DOC HELPERS
# =========================
def set_doc_margins(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)


def add_title(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_subtitle(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_section(doc: Document, title: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(title.upper())
    run.bold = True
    run.font.size = Pt(11.5)


def add_paragraph(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10.5)


def add_bullets(doc: Document, bullets: List[str]) -> None:
    for b in bullets:
        p = doc.add_paragraph(b, style="List Bullet")
        for r in p.runs:
            r.font.size = Pt(10.5)


def save_txt(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# =========================
# LIBREOFFICE EXPORT
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


def convert_with_libreoffice(docx_path: Path, fmt: str, cfg: ResumeConfig) -> Path:
    soffice = find_soffice(cfg)
    if not soffice:
        raise FileNotFoundError(
            "LibreOffice (soffice.exe) not found. Install LibreOffice or set libreoffice_path in resume_config.json"
        )

    # LibreOffice writes output to outdir with same base filename
    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--convert-to",
        fmt,
        "--outdir",
        str(docx_path.parent),
        str(docx_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    out = docx_path.parent / f"{docx_path.stem}.{fmt}"
    if not out.exists():
        raise RuntimeError(f"LibreOffice conversion ran but {fmt.upper()} was not created.")
    return out


# =========================
# CONTENT MODEL
# =========================
Section = Tuple[str, List[str] | str]  # (title, bullets OR paragraph)


def base_header_lines(cfg: ResumeConfig) -> List[str]:
    return [
        cfg.name,
        f"{cfg.location} | {cfg.phone} | {cfg.email}",
        f"LinkedIn: {cfg.linkedin} | GitHub: {cfg.github}",
        "",
    ]


def variant_filename_slug(variant: str) -> str:
    # Keep consistent filenames
    return f"brian-hannigan-{variant}"


def content_variant(variant: str) -> Tuple[str, List[str], List[Section]]:
    """
    Returns:
      summary, skills, sections (Experience/Projects/Education/Certifications/etc.)
    Note: This is intentionally ATS-friendly (plain titles, no tables).
    """

    # --- Shared project bullets (portable translator) ---
    translator_project = [
        "Designed and implemented Python-based REST services supporting OCR and AI translation workflows.",
        "Built HTTP endpoints with structured JSON request/response handling and robust validation.",
        "Integrated Tesseract OCR and local translation engines into modular, testable service boundaries.",
        "Implemented logging, error handling, and process monitoring to improve reliability and debuggability.",
        "Used Git for version control and iterative feature delivery; maintained clean repo organization and documentation.",
    ]

    # --- Shared UTRS bullets (truthful, role-appropriate framing) ---
    utrs_core = [
        "Designed and deployed simulation training ecosystems for U.S. Government/DoD programs across multiple sites.",
        "Built and sustained instructor/operator tooling, automation workflows, and repeatable deployment procedures.",
        "Produced clear technical documentation, SOPs, and handoff-ready training materials for long-term sustainment.",
        "Applied secure configuration practices and compliance expectations (e.g., DISA STIG alignment) in system deployments.",
        "Partnered with stakeholders to translate requirements into deliverable software/system outcomes in fast-paced environments.",
    ]

    # --- Shared security/compliance bullets ---
    security_core = [
        "Applied DISA STIG-aligned secure configuration standards and vulnerability scanning practices.",
        "Supported secure deployments through hardening, documentation, and compliance-focused engineering.",
        "Performed structured troubleshooting and remediation to reduce operational risk and improve system reliability.",
    ]

    # =========================
    # VARIANTS
    # =========================
    if variant == "general":
        summary = (
            "Senior Software Engineer, Technical Systems Architect, and Security-focused builder with 15+ years delivering "
            "secure, scalable systems across mission-critical environments. Experienced in backend services, automation, "
            "API-driven workflows, and deployment standardization. Known for disciplined execution, documentation, and "
            "stakeholder communication."
        )

        skills = [
            "Languages: Python, C#, SQL, Bash",
            "Backend: REST APIs, JSON, HTTP, Service-Oriented Design",
            "Databases: SQLite, SQL Server, MySQL (plus general relational modeling)",
            "Tools: Git, Docker, Windows, Linux",
            "Security: Hardening, compliance-aligned engineering, vulnerability scanning concepts",
            "Strengths: Debugging, documentation, requirements translation, cross-functional delivery",
        ]

        sections: List[Section] = [
            ("Featured Projects", [
                "Portable Translator (Python APIs, OCR + translation orchestration) — GitHub: github.com/brianhannigan/translator",
                *translator_project
            ]),
            ("Experience", [
                "UTRS, Inc — Lead Technical Instructor / Simulation Systems Engineer (2011–2025)",
                *utrs_core,
                *security_core,
            ]),
            ("Additional Experience", [
                "Web Developer • SharePoint/.NET Consultant • Software Engineer • Independent Consultant • Teacher (Technology & Special Education)",
            ]),
            ("Education", [
                "M.Ed., Special Education — New Jersey City University",
                "B.S., Criminal Justice — University of Delaware",
                "Programming Diploma — Chubb Institute",
            ]),
            ("Certifications & Credentials", [
                "CompTIA Security+ • InfraGard Member • SOC Core Skills • Active Defense & Cyber Deception • Red Team Summit • Hacking Humans",
            ]),
        ]
        return summary, skills, sections

    if variant == "python-backend":
        summary = (
            "Backend-focused Python Engineer and Systems Architect experienced building RESTful APIs, modular services, "
            "and data-driven workflows. Strong foundation in OOP, debugging, and performance-minded development with "
            "production discipline from mission-critical deployments."
        )

        skills = [
            "Python: APIs, services, tooling, scripting",
            "Backend: REST, JSON, HTTP, request validation, error handling",
            "Databases: SQLite, SQL fundamentals, relational modeling",
            "Tools: Git, Docker, Windows/Linux",
            "Engineering: OOP, data structures, debugging, logging",
        ]

        sections = [
            ("Featured Python Project", [
                "Portable Translator — Python Backend & API Services (GitHub: github.com/brianhannigan/translator)",
                *translator_project
            ]),
            ("Experience", [
                "UTRS, Inc — Technical Systems Engineer / Software Developer (2011–2025)",
                "Built automation and support tooling; produced repeatable deployment workflows and documentation.",
                "Delivered reliable systems under operational constraints; improved uptime through disciplined troubleshooting.",
                "Supported secure configurations and compliance-aligned deployment standards.",
            ]),
            ("Additional Technical Strengths", [
                "Comfortable working across product + engineering stakeholders to ship maintainable backend capabilities.",
                "Able to operate independently in remote environments; strong written communication and documentation habits.",
            ]),
            ("Education", [
                "M.Ed., Special Education — New Jersey City University",
                "B.S., Criminal Justice — University of Delaware",
                "Programming Diploma — Chubb Institute",
            ]),
            ("Certifications", [
                "CompTIA Security+ (plus continued professional development in GRC and cyber range labs)",
            ]),
        ]
        return summary, skills, sections

    if variant == "cybersecurity":
        summary = (
            "Cybersecurity Engineer and Systems Builder with experience supporting secure deployments, hardening, "
            "compliance-aligned engineering, and threat-hunting portfolio development (KQL/SIEM). Strong technical "
            "foundation across Windows/Linux systems, scripting, and operational troubleshooting."
        )

        skills = [
            "SIEM / Threat Hunting: KQL, investigation workflows, detection engineering concepts",
            "Hardening & Compliance: DISA STIG alignment, secure configuration, audit-ready documentation",
            "Vulnerability Management: scanning concepts, remediation workflows, risk tracking",
            "Tools: Git, PowerShell/Bash, Windows/Linux, Docker (as needed)",
            "Reporting: executive-ready summaries, SOPs, evidence collection organization",
        ]

        sections = [
            ("Security Portfolio", [
                "KQL Threat Hunting Beginner Guide — GitHub: github.com/brianhannigan/kql-threathunting-beginner-guide",
                "Threat hunt scenario experience and SOC-style labs (portfolio-driven).",
            ]),
            ("Experience", [
                "UTRS, Inc — Secure Systems / Technical Systems Engineer (2011–2025)",
                *security_core,
                "Produced documentation and deployment procedures supporting sustainment and audit readiness.",
                "Supported operational troubleshooting to improve reliability and reduce downtime.",
            ]),
            ("Key Projects", [
                "Portable Translator — local/offline system orchestration with logging and reliable service startup patterns.",
            ]),
            ("Education", [
                "M.Ed., Special Education — New Jersey City University",
                "B.S., Criminal Justice — University of Delaware",
            ]),
            ("Certifications & Credentials", [
                "CompTIA Security+ • InfraGard Member • SOC Core Skills • Active Defense & Cyber Deception • Red Team Summit • Hacking Humans",
            ]),
        ]
        return summary, skills, sections

    if variant == "ai-architect":
        summary = (
            "AI Systems Architect and offline-first builder focused on practical AI integration, model orchestration, and "
            "deployable workflows. Experienced delivering AI-enabled services (OCR + translation) with strong emphasis on "
            "reliability, security boundaries, and documentation."
        )

        skills = [
            "AI Systems: model orchestration, offline-first deployment patterns, pipeline design",
            "APIs & Services: REST, JSON, modular service boundaries, logging and observability",
            "Automation: scripting, repeatable deployments, configuration management patterns",
            "Tools: Python, Docker, Git, Windows/Linux",
            "Communication: executive briefings, documentation, training and enablement",
        ]

        sections = [
            ("Flagship AI Project", [
                "Portable Translator — Offline AI translation + OCR orchestration (GitHub: github.com/brianhannigan/translator)",
                *translator_project
            ]),
            ("Experience", [
                "UTRS, Inc — AI Advisor / Technical Systems Architect (2011–2025)",
                "Delivered training ecosystems and technical solutions with a strong focus on operational reliability.",
                "Created documentation, SOPs, and enablement materials supporting adoption and sustainment.",
                "Applied compliance-minded practices and secure configuration expectations to deployments.",
            ]),
            ("Selected Capabilities", [
                "Workflow mapping and value mapping approaches for aligning automation/AI to measurable outcomes.",
                "Risk-aware system design (security boundaries, reliability, maintainability).",
            ]),
            ("Education", [
                "M.Ed., Special Education — New Jersey City University",
                "B.S., Criminal Justice — University of Delaware",
            ]),
            ("Certifications", [
                "CompTIA Security+ • InfraGard Member • Continued AI/cyber professional development",
            ]),
        ]
        return summary, skills, sections

    if variant == "grc-analyst":
        summary = (
            "GRC Analyst and compliance-focused security professional with experience supporting secure deployments, "
            "evidence-driven documentation, and risk-aware engineering. Skilled in organizing artifacts, writing clear "
            "workpapers, and aligning technical realities to control expectations (HIPAA, NIST-style controls, SOC 2 concepts)."
        )

        skills = [
            "GRC: risk assessments, evidence collection, control mapping, gap tracking, remediation planning",
            "Framework Exposure: HIPAA Security Rule, NIST-style controls, SOC 2 concepts, audit support workflows",
            "Documentation: policies/procedures support, workpapers, stakeholder interview notes, audit trails",
            "Technical Depth: Windows/Linux basics, secure configuration expectations, vulnerability remediation concepts",
            "Tools: Excel/Sheets tracking, structured templates, repeatable reporting",
        ]

        sections = [
            ("Relevant Experience (Compliance + Documentation)", [
                "Secure deployments and compliance-aligned engineering practices in mission-critical environments.",
                "Produced SOPs, technical documentation, and sustainment materials that support audit readiness.",
                "Supported troubleshooting/remediation workflows to reduce risk and improve reliability.",
            ]),
            ("Security & Compliance Focus", [
                "DISA STIG alignment awareness, vulnerability scanning concepts, secure configuration practices.",
                "Evidence organization mindset: inventories, screenshots, logs, configuration baselines, and change tracking.",
            ]),
            ("Projects", [
                "Portable Translator — reliable local services with logging, error handling, and repeatable startup workflows.",
            ]),
            ("Education", [
                "M.Ed., Special Education — New Jersey City University",
                "B.S., Criminal Justice — University of Delaware",
            ]),
            ("Certifications & Professional Development", [
                "CompTIA Security+ • Active SOC/GRC course progression and portfolio-building",
            ]),
        ]
        return summary, skills, sections

    raise ValueError(f"Unknown variant: {variant}")


# =========================
# BUILD (DOCX/TXT/ODT/PDF)
# =========================
def build_variant(
    variant: str,
    cfg: ResumeConfig,
    also_odt: bool = False,
    also_pdf: bool = False,
) -> Dict[str, Path]:
    summary, skills, sections = content_variant(variant)

    out_dir = OUT / variant
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = variant_filename_slug(variant)
    docx_path = out_dir / f"{slug}.docx"
    txt_path = out_dir / f"{slug}.txt"

    # --- DOCX ---
    doc = Document()
    set_doc_margins(doc)

    add_title(doc, cfg.name)
    add_subtitle(doc, f"{cfg.location} | {cfg.phone} | {cfg.email}")
    add_subtitle(doc, f"LinkedIn: {cfg.linkedin} | GitHub: {cfg.github}")

    add_section(doc, "Professional Summary")
    add_paragraph(doc, summary)

    add_section(doc, "Core Skills")
    add_bullets(doc, skills)

    for title, body in sections:
        add_section(doc, title)
        if isinstance(body, str):
            add_paragraph(doc, body)
        else:
            add_bullets(doc, body)

    doc.save(str(docx_path))

    # --- TXT (ATS-friendly) ---
    lines: List[str] = []
    lines.extend(base_header_lines(cfg))
    lines.append("PROFESSIONAL SUMMARY")
    lines.append(summary)
    lines.append("")
    lines.append("CORE SKILLS")
    for s in skills:
        lines.append(f"- {s}")
    lines.append("")

    for title, body in sections:
        lines.append(title.upper())
        if isinstance(body, str):
            lines.append(body)
        else:
            for b in body:
                lines.append(f"- {b}")
        lines.append("")

    save_txt(txt_path, lines)

    result: Dict[str, Path] = {"docx": docx_path, "txt": txt_path}

    if also_odt:
        result["odt"] = convert_with_libreoffice(docx_path, "odt", cfg)

    if also_pdf:
        result["pdf"] = convert_with_libreoffice(docx_path, "pdf", cfg)

    return result


def ensure_folders() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for v in ["general", "python-backend", "cybersecurity", "ai-architect", "grc-analyst"]:
        (OUT / v).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    cfg = load_config()
    ensure_folders()
    # CLI quick test (generates one). Use UI for all variants.
    files = build_variant("python-backend", cfg, also_odt=False, also_pdf=False)
    print("Generated:", files)