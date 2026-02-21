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
