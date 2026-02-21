# Resume Library Generator

A reproducible resume-generation system that keeps one source of truth and outputs role-targeted resume variants.

## What this repository does

- Maintains a single, editable career inventory.
- Generates job-targeted resume outputs.
- Produces ATS-friendly text artifacts.
- Keeps generated variants versioned in-repo.

## Current repository layout

```text
resume-library/
├── README.md
├── generate_resumes.py
├── resume_ui.py
├── resume_config.json
├── generator/
│   ├── build_resume.py
│   └── requirements.txt
├── resumes/
│   ├── README.md
│   └── *.txt / *.odt
├── variants/
│   └── *.docx / *.pdf
└── changelog/
    └── updates_2026.md
```

## How it works

1. Update source content and configuration.
2. Run a generator script.
3. Review generated variants in `variants/`.
4. Use text exports for ATS checks and copy/paste workflows.

## Build commands

From the repository root:

```bash
python generate_resumes.py
```

If you are using the profile-based generator:

```bash
cd generator
python build_resume.py siem --outdir ..\\variants --mode usajobs --year 2026
python build_resume.py siem --outdir ..\\variants --mode full --year 2026
```

## Build modes (profile-based generator)

| Mode | Purpose | Behavior |
|---|---|---|
| `usajobs` | Federal submissions | Aggressive trimming for shorter output |
| `standard` | Balanced submissions | Moderate bullet count |
| `full` | Comprehensive submissions | Maximum bullet inclusion |

## Output artifacts

Typical outputs include:

- `variants/*.docx`
- `variants/*.pdf`
- `resumes/*.txt`
- provenance logs (when using `generator/build_resume.py`)

## Notes

- Prefer ASCII punctuation in source text.
- Keep bullet statements concise to reduce trimming artifacts.
- Rebuild after any content or profile update to keep variants consistent.
