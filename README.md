Resume Library Generator (Enterprise System)

A structured, reproducible resume-generation system designed to:

Maintain a single source-of-truth career inventory

Generate multiple job-targeted resume variants

Enforce defensible language

Produce DOCX / PDF / TXT outputs

Log provenance for traceability

Support USAJobs ≤ 2-page constraints

Scale across cybersecurity, engineering, and compliance roles

System Philosophy

This repository treats resume building like software.

Instead of editing multiple Word documents:

Blocks contain truth.

Profiles define intent.

Modes enforce constraints.

Generator assembles artifacts.

Provenance logs provide traceability.

You update once → regenerate everywhere.

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
├── variants/          # generated resume artifacts
└── sources/           # optional raw resume documents
High-Level Architecture
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
Sequence Diagram
Component Diagram
Build Modes
Mode	Purpose	Behavior
usajobs	Federal submissions	Aggressive trimming, ≤2 pages
standard	Balanced version	Moderate bullet count
full	Comprehensive	Maximum bullet inclusion
Functional Requirements
FR-1 Source-of-Truth Inventory

All experience content lives in blocks/.

Bullets must begin with -.

FR-2 Profile-Driven Variants

Profiles define:

summary

tagline

contact

experience blocks

skills

projects

certifications

education

FR-3 Multi-Format Output

Generator produces:

DOCX

PDF

TXT

FR-4 Mode-Based Trimming

Mode determines bullet caps and content density.

FR-5 Provenance Logging

Every build generates:

generator/logs/<resume>.provenance.json

Contains:

timestamp

profile

mode

block file paths

bullets used

Non-Functional Requirements

Defensible language by default

Windows-compatible

ATS-friendly plain text output

Encoding-safe reads/writes

Deterministic output for stable inputs

Operating Instructions
Edit master inventory

Modify:

blocks/experience/*.md
Edit resume blueprint

Modify:

generator/profiles/*.json
Build

From generator/:

python build_resume.py siem --outdir ..\variants --mode usajobs --year 2026
USAJobs 2-Page Enforcement Strategy

To guarantee compliance:

10pt font

0.5"–0.7" margins

Max 3–4 bullets per role

Limited skills + projects

If output exceeds 2 pages, adjust:

bullet caps

font size

margins in build_docx()

Product Requirements Document (PRD)
Problem

Managing multiple resume versions manually creates:

duplication

inconsistencies

formatting drift

lost edits

Solution

A deterministic generator that:

stores master career data in blocks

builds role-specific variants

logs exactly what content was used

Goals

Single source of truth

Fast variant generation

USAJobs compliance

Provenance traceability

Scalable architecture

Non-Goals

Auto-scraping job descriptions (future enhancement)

AI content generation without human validation

Success Criteria

Build completes cleanly

Outputs generated in expected directory

Provenance file matches resume content

USAJobs mode reliably ≤2 pages

Control Points (How to Redirect the System)
Block Granularity

Option A: One file per employer
Option B: Split employer by theme (security vs engineering vs training)

Mode Policies

Adjust bullet caps and trimming behavior.

Strict Defensibility Mode

Add automated checks for inflated verbs.

Keyword Injection Mode (Future)

Inject ATS keyword clusters dynamically.

Known Risks
Risk	Cause	Mitigation
Mid-sentence cuts	aggressive trimming	shorten bullets
Encoding artifacts	copy from Word	use ASCII punctuation
JSON errors	invalid formatting	pure JSON only
Length overflow	too many bullets	tighten mode rules
Roadmap

Planned Enhancements:

Resume lint (defensibility + length checker)

Batch build all profiles

GitHub Actions CI

Keyword density scoring

Automated diff comparison between variants

Clearance tagging

PDF styling themes

Summary

This repository transforms resume management from manual document editing into:

A structured, reproducible build system.

Blocks contain truth.
Profiles define intent.
Modes enforce constraints.
Generator assembles outputs.
Logs provide traceability.
