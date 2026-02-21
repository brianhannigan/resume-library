# Resume Library Generator (Enterprise System)

A structured, reproducible resume-generation system designed to:

- Maintain a **single source-of-truth career inventory**
- Generate multiple job-targeted resume variants
- Enforce defensible language
- Produce DOCX / PDF / TXT outputs
- Log provenance for traceability
- Support USAJobs ≤ 2-page constraints
- Scale across cybersecurity, engineering, and compliance roles

---

## System Philosophy

This repository treats resume building like software.

Instead of editing multiple Word documents:

- **Blocks** contain truth.
- **Profiles** define intent.
- **Modes** enforce constraints.
- **Generator** assembles artifacts.
- **Provenance logs** provide traceability.

You update once → regenerate everywhere.

---

## Repository Structure

```text
resume-library/
├── README.md
├── blocks/
│   ├── experience/
│   │   ├── logn_pacific.md
│   │   ├── utrs.md
│   │   └── consulting.md
│   ├── projects/
│   └── skills/
├── generator/
│   ├── build_resume.py
│   ├── requirements.txt
│   ├── profiles/
│   │   ├── siem.json
│   │   ├── soc.json
│   │   └── grc.json
│   ├── logs/
│   └── output/
├── variants/          # generated resume artifacts
└── sources/           # optional raw resume documents

```
# High-Level Architecture

sources/ (raw resumes, docs, inbox)
        │
        ▼
blocks/ (master bullet inventory)
  blocks/experience/*.md
  blocks/projects/*.md
  blocks/skills/*.md
        │
        ▼
profiles/*.json (resume blueprints)
        │
        ▼
build_resume.py (assembler)
        │
        ├── DOCX
        ├── PDF
        ├── TXT
        └── provenance.json
        ▼
variants/



How the Parts Interact (Sequence Diagram)
System Components (UML-style Component Diagram)
Diagram is not supported.
Build Modes
Mode	Purpose	Behavior
usajobs	Federal submissions	Aggressive trimming, intended for ≤2 pages
standard	Balanced	Moderate bullet count
full	Comprehensive	Maximum bullet inclusion
Functional Requirements
FR-1: Source-of-Truth Inventory

All experience content lives in blocks/.

Bullets must begin with -.

Blocks should remain comprehensive (master inventory).

FR-2: Profile-Driven Variants

Profiles define:

name/contact/tagline/summary

experience roles (each points to a blocks/experience/*.md file)

skills, projects, certifications, education

FR-3: Multi-Format Output

Generator produces:

DOCX

PDF

TXT (ATS-friendly)

FR-4: Mode-Based Trimming

Mode determines:

bullets per role

trimming rules for long bullets

optional caps for skills/projects in USAJobs mode

FR-5: Provenance Logging

Every build generates:

generator/logs/<BaseName>.provenance.json

Includes:

timestamp

mode

profile/output name

role lines

block paths used

bullets included in the output

Non-Functional Requirements

Defensible language by default (avoid inflated claims unless verified)

Windows-compatible paths and tooling

ATS-friendly TXT output (clean, minimal formatting artifacts)

Encoding-safe reads/writes (supports utf-8-sig)

Deterministic output for stable inputs

Operating Instructions
Edit master inventory (truth)

Update:

blocks/experience/*.md

blocks/projects/*.md

blocks/skills/*.md

Best practice: use ASCII punctuation and - bullets only.

Edit resume blueprint (intent)

Update:

generator/profiles/*.json

Build output artifacts

From resume-library/generator/:

python build_resume.py siem --outdir ..\variants --mode usajobs --year 2026
python build_resume.py siem --outdir ..\variants --mode full --year 2026

Outputs:

variants/Brian_Hannigan_<OutputName>_<Year>.docx

variants/Brian_Hannigan_<OutputName>_<Year>.pdf

variants/Brian_Hannigan_<OutputName>_<Year>.txt

generator/logs/Brian_Hannigan_<OutputName>_<Year>.provenance.json

USAJobs ≤ 2-Page Enforcement Strategy

USAJobs resumes must be ≤ 2 pages.

This repo enforces that via:

--mode usajobs trimming rules (fewer bullets per role)

controlled section caps (skills/projects)

DOCX formatting enforcement (font/margins/spacing) inside build_docx() if needed

Recommended USAJobs formatting defaults:

Font: 10pt

Margins: 0.5"–0.7"

Max bullets per role: 3–4

Limit projects: 1–2

Limit skills: ~10–14

If your output still exceeds 2 pages:

reduce per-role bullet caps

shorten long bullets

enforce tighter DOCX margins + spacing in code

Control Points (How to Redirect the System)
A) Block Granularity

Option A: One file per employer (simple)

Option B: Split by employer + theme (more precise)

utrs_security.md

utrs_engineering.md

utrs_training.md

Option B reduces trimming surprises and improves job targeting.

B) Mode Policies

Tune how aggressive trimming is:

per-role bullet cap

per-bullet character cap

max skills/projects/certs counts

C) Strict Defensibility Mode (Future)

Add a validation step to flag:

“led”, “architected”, “owned”, “managed” (unless verified)

claims without evidence

overly long bullets for USAJobs mode

D) Source Trace Mapping (Optional)

Add a mapping file so each bullet can be traced back to:

original resume filename in sources/

extracted date/role context

Known Risks and Mitigation
Risk	Why it happens	Mitigation
Bullets cut mid-sentence	aggressive trimming	keep bullets short; trim at punctuation
Mojibake (â€” / â€¢)	copy/paste from Word/PDF	use ASCII punctuation; - bullets only
JSON decode errors	BOM/empty file/comments	pure JSON only; write UTF-8
Output location confusion	relative --outdir paths	always build to ..\variants
Roadmap

Planned enhancements:

Resume lint (defensibility + length checks)

Batch build all profiles

GitHub Actions CI (build artifacts on push)

ATS keyword density scoring + suggestions

Automated diff comparisons between variants

Clearance/environment tagging (only if defensible)

PDF styling themes

Product Requirements Document (PRD)
Problem

Managing many resume variants manually creates:

duplication

inconsistencies

formatting drift

content loss over time

Solution

A deterministic generator that:

stores master career content in blocks

produces job-specific variants from profiles

supports USAJobs constraints

logs exactly what content was used

Goals

Single source of truth

Fast variant generation

USAJobs compliance

Provenance traceability

Scalable architecture

Non-Goals

Automatic job scraping (future enhancement)

Fully automated AI rewriting without human validation

Success Criteria

Build completes cleanly on Windows

DOCX/PDF/TXT outputs appear in variants/

Provenance log matches actual resume content

USAJobs mode can be reliably tuned to ≤ 2 pages

Summary

This repository transforms resume management from manual document editing into a structured build pipeline:

Blocks contain truth.

Profiles define intent.

Modes enforce constraints.

Generator assembles outputs.

Provenance provides traceability.
