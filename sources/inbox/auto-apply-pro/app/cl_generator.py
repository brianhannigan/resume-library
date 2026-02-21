from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .config import CFG, LLM_PROVIDER, LLM_API_KEY

def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(CFG["paths"]["templates_dir"]),
        autoescape=select_autoescape()
    )

def rules_based_cover_letter(job_desc: str, profile: Dict[str, Any], tone: str, template_name: str) -> str:
    env = _env()
    tmpl = env.get_template(f"{template_name}.jinja2")
    return tmpl.render(
        job_desc=job_desc[:4000],
        profile=profile,
        tone=tone,
    )

def maybe_llm_generate(job_desc: str, profile: Dict[str, Any], tone: str) -> str | None:
    if not LLM_PROVIDER or not LLM_API_KEY:
        return None
    prompt = f"""
Write a {tone} 300–400 word cover letter tailored to this job.
Use my profile facts and achievements where relevant.
Focus on measurable impact; end with a concrete CTA.

JOB DESCRIPTION:
{job_desc[:4000]}

PROFILE:
{profile}
"""
    try:
        if LLM_PROVIDER.lower() == "openai":
            import openai  # type: ignore
            openai.api_key = LLM_API_KEY
            resp = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=550,
                temperature=0.5,
            )
            return resp.choices[0].text.strip()
    except Exception:
        return None
    return None

def generate_cover_letter(job_desc: str, profile: Dict[str, Any], tone: str = "confident", template_name: str = "default") -> str:
    llm = maybe_llm_generate(job_desc, profile, tone)
    if llm:
        return llm
    return rules_based_cover_letter(job_desc, profile, tone, template_name)

def write_outputs(text: str, basename: str, out_dir: str) -> Dict[str, str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    txt_path = Path(out_dir) / f"{basename}.txt"
    txt_path.write_text(text, encoding="utf-8")

    docx_path = Path(out_dir) / f"{basename}.docx"
    try:
        from docx import Document
        doc = Document()
        for para in text.split("\n\n"):
            doc.add_paragraph(para)
        doc.save(docx_path.as_posix())
    except Exception:
        docx_path = None

    pdf_path = Path(out_dir) / f"{basename}.pdf"
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf_path.as_posix(), pagesize=LETTER)
        width, height = LETTER
        x, y = 72, height - 72
        for line in text.split("\n"):
            c.drawString(x, y, line[:1000])
            y -= 14
            if y < 72:
                c.showPage(); y = height - 72
        c.save()
    except Exception:
        pdf_path = None

    return {
        "txt": txt_path.as_posix(),
        "docx": docx_path.as_posix() if docx_path else "",
        "pdf": pdf_path.as_posix() if pdf_path else "",
    }
