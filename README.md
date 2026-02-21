Resume Library Generator System

A structured, reproducible resume generation system designed to:

Maintain a single source-of-truth career inventory

Generate multiple job-targeted resume variants

Enforce defensible language

Produce DOCX / PDF / TXT outputs

Log provenance for traceability

Support USAJobs 2-page mode

Scale across cybersecurity, engineering, and compliance roles

System Overview

This repository separates:

Content (Blocks) — long-form master career inventory

Profiles (Blueprints) — role-specific resume configurations

Generator (Assembler) — builds formatted outputs

Variants (Outputs) — final resumes ready to submit

Provenance Logs — traceability for every build

The system is designed to behave like software, not a static document.

High-Level Architecture
sources/ (optional raw resumes, inbox docs)
        │
        ▼
blocks/ (source-of-truth bullet inventory)
  blocks/experience/*.md
  blocks/projects/*.md
  blocks/skills/*.md
        │
        ▼
generator/profiles/*.json (resume blueprints)
        │
        ▼
generator/build_resume.py (assembly pipeline)
        │
        ├── DOCX
        ├── PDF
        ├── TXT
        └── provenance.json
        ▼
variants/ (final resume outputs)
Repository Structure
resume-library/
│
├── README.md
│
├── blocks/
│   ├── experience/
│   │   ├── logn_pacific.md
│   │   ├── utrs.md
│   │   └── consulting.md
│   ├── projects/
│   └── skills/
│
├── generator/
│   ├── build_resume.py
│   ├── requirements.txt
│   ├── profiles/
│   │   ├── siem.json
│   │   ├── soc.json
│   │   └── grc.json
│   ├── logs/
│   └── output/
│
├── variants/          (generated resumes)
└── sources/           (optional raw source resumes)
System Design Philosophy

Blocks are long and complete.

Profiles select what matters.

Modes determine how much gets shown.

Outputs are reproducible and traceable.

Functional Requirements
FR-1: Source-of-Truth Inventory

All experience content lives in blocks/.

Blocks may include headings, but bullets must start with -.

Blocks should remain comprehensive.

FR-2: Profile-Driven Variants

Each profile JSON defines:

summary

tagline

contact

experience roles (each referencing a block file)

skills

projects

certifications

education

FR-3: Multi-Format Output

Generator must produce:

DOCX

PDF

TXT (ATS-safe)

FR-4: Mode-Based Trimming

Supported modes:

usajobs

Aggressive trimming

Fewer bullets per role

Optimized for ≤2 pages

standard

Balanced presentation

full

Maximum bullet inclusion

FR-5: Provenance Logging

Each build writes:

generator/logs/<resume>.provenance.json

Includes:

timestamp

mode

profile name

block paths used

bullets included

FR-6: Deterministic Builds

Given unchanged blocks + profile + mode,
the same output should be generated consistently.

Non-Functional Requirements
NFR-1: Defensible Language

Avoid inflated claims unless verified.

Prefer:

Supported

Contributed

Participated

Implemented

Developed

Collaborated

NFR-2: ATS Compatibility

Clean UTF-8 output

Minimal special characters

No emoji

No Unicode bullets (prefer -)

NFR-3: Windows First

Must run under PowerShell

Compatible with Python 3.x

NFR-4: Encoding Safe

Support UTF-8 with BOM input

Avoid JSON comments

Profile Schema Specification

Example: generator/profiles/siem.json

{
  "output_name": "SIEM_Engineer",
  "summary": "...",
  "skills": ["..."],
  "experience": [
    {
      "company": "UTRS, Inc",
      "title": "Senior Software Engineer",
      "dates": "2011-2025",
      "block": "blocks/experience/utrs.md",
      "max_bullets": 10
    }
  ]
}
Build Pipeline Specification
Step 1: Load Profile JSON

Validate file exists

Parse JSON

Step 2: Read Block Files

Extract lines starting with -

Ignore template artifacts

Step 3: Apply Mode Rules

Cap bullets per role

Optionally trim long bullets

Reduce skills/projects count in USAJobs mode

Step 4: Assemble Resume Sections

Name

Contact

Tagline

Summary

Experience

Skills

Projects

Certifications

Education

Step 5: Write Outputs

DOCX

PDF

TXT

Provenance JSON

Operating Procedure
Edit Experience Content

Modify:

blocks/experience/*.md
Edit Headline / Summary / Skills

Modify:

generator/profiles/<profile>.json
Build Resume

From generator/:

python build_resume.py siem --outdir ..\variants --mode usajobs --year 2026

Other modes:

python build_resume.py siem --outdir ..\variants --mode standard
python build_resume.py siem --outdir ..\variants --mode full
Provenance Log Example
generator/logs/Brian_Hannigan_SIEM_Engineer_2026.provenance.json

Contains:

{
  "generated_at": "...",
  "mode": "usajobs",
  "profile": "SIEM_Engineer",
  "experience": [
    {
      "role": "UTRS, Inc | Senior Software Engineer | 2011-2025",
      "block": "blocks/experience/utrs.md",
      "bullets_used": [...]
    }
  ]
}
Control Points (How to Redirect the System)
Control Point A: Block Granularity

Option A — One file per employer (current)

Option B — One file per employer per theme:

utrs_security.md

utrs_engineering.md

utrs_training.md

Option B gives finer control and better USAJobs precision.

Control Point B: Page Enforcement

To guarantee 2-page compliance:

Enforce 10pt font

0.5–0.7" margins

Limit bullets to 4 per role

This can be hard-coded into build_docx().

Control Point C: Strict Defensibility Mode

Future enhancement:

Flag high-claim verbs

Warn on "led", "architected", "owned"

Output review report

Control Point D: Source Trace Mapping

Optional future addition:

Map each block bullet to a specific original resume source

Enable full traceability chain

Known Risks and Mitigation
Risk	Cause	Mitigation
Bullets cut mid-sentence	aggressive trim	Keep bullets under 140 chars
Encoding artifacts	copy from Word	Use ASCII punctuation
JSON load errors	comments in JSON	JSON must be pure
Resume too long	full mode used	switch to usajobs mode
Recommended Best Practices

Keep blocks comprehensive.

Keep bullets concise.

Avoid Unicode punctuation.

Use - only for bullets.

Never put comments inside JSON.

Expansion Roadmap

Planned enhancements:

ATS keyword density scoring

Clearance flag support

Automatic job description keyword injection

PDF styling themes

Resume comparison diff mode

Word margin enforcement

Strict compliance mode

Multi-profile batch build

CLI config file support

System Summary

This repository transforms resume building from:

Static document editing

into:

Structured, reproducible, traceable output generation.

Blocks contain truth.

Profiles define intent.

Modes enforce constraints.

Generator assembles results.

Variants are deployable.

Provenance ensures traceability.
