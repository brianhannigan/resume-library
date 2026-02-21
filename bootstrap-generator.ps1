param(
    [switch]$Force
)

function Ensure-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "Created dir: $path"
    }
}

function Ensure-File($path, $content) {
    if ((Test-Path $path) -and -not $Force) {
        Write-Host "Exists: $path"
        return
    }
    $parent = Split-Path $path -Parent
    if ($parent -and -not (Test-Path $parent)) {
        Ensure-Dir $parent
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
    Write-Host "Created file: $path"
}

# Directories
Ensure-Dir "generator"
Ensure-Dir "generator\profiles"
Ensure-Dir "generator\output"

# ==============================
# build_resume.py
# ==============================

$buildPy = @"
import json
import argparse
from pathlib import Path
from datetime import datetime
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / "blocks"
OUT_DEFAULT = Path(__file__).resolve().parent / "output"

def load_profile(name):
    path = Path(__file__).resolve().parent / "profiles" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))

def read_block(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8")

def extract_bullets(text):
    bullets = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("-", "*", "•")):
            bullets.append(s.lstrip("-*• ").strip())
    return bullets

def build_docx(profile, sections, out):
    doc = Document()
    doc.add_heading("Brian Hannigan", level=1)
    doc.add_paragraph(profile["summary"])

    doc.add_heading("Experience", level=2)
    for sec in sections:
        doc.add_heading(sec["title"], level=3)
        for b in sec["bullets"]:
            doc.add_paragraph(b, style="List Bullet")

    doc.add_heading("Skills", level=2)
    doc.add_paragraph(", ".join(profile["skills"]))
    doc.save(out)

def build_pdf(profile, sections, out):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(out)
    elements = []

    elements.append(Paragraph("<b>Brian Hannigan</b>", styles["Heading1"]))
    elements.append(Paragraph(profile["summary"], styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    for sec in sections:
        elements.append(Paragraph(f"<b>{sec['title']}</b>", styles["Normal"]))
        for b in sec["bullets"]:
            elements.append(Paragraph(f"- {b}", styles["Normal"]))
        elements.append(Spacer(1, 0.15 * inch))

    elements.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    elements.append(Paragraph(", ".join(profile["skills"]), styles["Normal"]))

    pdf.build(elements)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("--outdir", default=str(OUT_DEFAULT))
    args = parser.parse_args()

    profile = load_profile(args.profile)
    sections = []

    for block in profile["experience_blocks"]:
        text = read_block(block["block"])
        bullets = extract_bullets(text)[:block.get("max_bullets", 6)]
        sections.append({
            "title": block["title"],
            "bullets": bullets
        })

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    year = datetime.now().year
    base = f"Brian_Hannigan_{profile['output_name']}_{year}"
    docx_out = outdir / f"{base}.docx"
    pdf_out = outdir / f"{base}.pdf"

    build_docx(profile, sections, docx_out)
    build_pdf(profile, sections, pdf_out)

    print("Generated:")
    print(docx_out)
    print(pdf_out)

if __name__ == "__main__":
    main()
"@

Ensure-File "generator\build_resume.py" $buildPy

# ==============================
# requirements.txt
# ==============================

Ensure-File "generator\requirements.txt" @"
python-docx
reportlab
"@

# ==============================
# siem.json
# ==============================

Ensure-File "generator\profiles\siem.json" @"
{
  "output_name": "SIEM_Engineer",
  "summary": "Cyber Security Support Analyst focused on SIEM engineering, KQL detection development, Tenable vulnerability management, and DISA STIG compliance.",
  "skills": ["Microsoft Sentinel", "KQL", "Tenable", "DISA STIG", "PowerShell", "EDR", "Azure"],
  "experience_blocks": [
    {
      "title": "Log(N) Pacific — Cyber Security Support Analyst",
      "block": "blocks/experience/logn_pacific.md",
      "max_bullets": 8
    },
    {
      "title": "UTRS — Senior Software Engineer / Secure Systems Engineer",
      "block": "blocks/experience/utrs.md",
      "max_bullets": 6
    }
  ]
}
"@

Write-Host ""
Write-Host "Generator scaffold created successfully." -ForegroundColor Green