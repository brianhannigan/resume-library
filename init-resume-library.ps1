<# 
init-resume-library.ps1
Creates a structured resume-library layout:
- sources/master (ODT + MD + provenance)
- blocks (experience/skills/metrics/keywords)
- variants (role-specific outputs)
- job-targets (per-job packages)
- changelog

Safe by default: does NOT overwrite existing files.
Use -Force to overwrite placeholders if you want.
#>

param(
  [switch]$Force
)

function Ensure-Dir {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path | Out-Null
    Write-Host "Created dir: $Path"
  } else {
    Write-Host "Exists dir:  $Path"
  }
}

function Ensure-File {
  param(
    [string]$Path,
    [string]$Content = ""
  )
  if (Test-Path -LiteralPath $Path) {
    if ($Force) {
      Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
      Write-Host "Overwrote:   $Path"
    } else {
      Write-Host "Exists file: $Path"
    }
  } else {
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
      Ensure-Dir $parent
    }
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Host "Created file:$Path"
  }
}

# -------------------------------
# Directories
# -------------------------------
$dirs = @(
  "sources",
  "sources/master",

  "blocks",
  "blocks/experience",
  "blocks/skills",
  "blocks/metrics",
  "blocks/keywords",

  "variants",
  "variants/siem-engineer",
  "variants/vulnerability-mgmt",
  "variants/grc-analyst",
  "variants/software-architect",
  "variants/training-instructor",

  "job-targets",
  "job-targets/2026",

  "changelog"
)

foreach ($d in $dirs) { Ensure-Dir $d }

# -------------------------------
# Placeholder files (Markdown)
# -------------------------------
Ensure-File "sources/master/Brian_Hannigan_Master_CV_2026.md" @"
# Brian Hannigan — Master CV (2026)

> This is the Git-friendly source of truth (diffable).  
> The LibreOffice master lives alongside as ODT.

## Core Identity
- Name:
- Location:
- Email:
- LinkedIn:
- GitHub:

## Professional Summary (Variants)
- Summary A (Gov/Secure Systems):
- Summary B (Vuln Mgmt/SecOps):
- Summary C (SIEM/Detection):

## Experience (Full)
> Keep ALL bullets here (reference).  
> Also store modular bullets in /blocks/experience.

## Education
## Certifications
## Skills (Master List)
## Projects / Portfolio
## Metrics Bank (highlights)
"@

Ensure-File "sources/master/provenance.md" @"
# Provenance / Defensibility Log

Purpose:
- Track where each major bullet/metric came from (resume version, doc upload, message date, etc.)
- Helps ensure everything in job resumes is defensible.

Format:
- Date:
- Item:
- Source:
- Notes:

Examples:
- 2026-02-20 — Log(N) Pacific vulnerability reduction metrics — Provided by Brian (chat) — confirm reporting method used
"@

Ensure-File "changelog/updates_2026.md" @"
# Resume Library Changelog — 2026

## YYYY-MM-DD
- Added:
- Updated:
- Removed:
- Notes:
"@

# -------------------------------
# Blocks: Experience
# -------------------------------
Ensure-File "blocks/experience/logn_pacific.md" @"
# Log(N) Pacific — Cyber Security Support Analyst (Vulnerability Management & SecOps Intern)
**Dates:** 2025–Present

## Vulnerability Management (Bullets)
- [Add bullets here]

## Security Operations (Bullets)
- [Add bullets here]

## Tools
- Tenable, MDE, Sentinel, KQL, PowerShell, NSG/Firewall
"@

Ensure-File "blocks/experience/utrs.md" @"
# UTRS, Inc — Senior Software Engineer / Secure Systems Engineer
**Dates:** 2011–2025 (or Present if applicable)

## Secure Systems / Compliance (Bullets)
- [Add bullets here]

## Engineering / Delivery (Bullets)
- [Add bullets here]

## Tools
- Windows, Linux, PowerShell, Bash, STIG, Nessus, .NET, etc.
"@

Ensure-File "blocks/experience/consulting.md" @"
# Independent / Consulting — Software, Security, Automation
**Dates:** Various

- [Add bullets here]
"@

Ensure-File "blocks/experience/teaching.md" @"
# Teaching / Training — Technical Instruction / Curriculum
**Dates:** Various

- [Add bullets here]
"@

# -------------------------------
# Blocks: Skills
# -------------------------------
Ensure-File "blocks/skills/siem_detection.md" @"
# SIEM / Detection Engineering (Skills + Keywords)

## Skills
- KQL, Sentinel, MDE Advanced Hunting
- Detection logic, alert tuning, telemetry correlation
- MITRE ATT&CK mapping (as applicable)

## ATS Keywords
- SIEM, detections, analytics rules, log sources, alert triage, threat hunting
"@

Ensure-File "blocks/skills/vuln_mgmt.md" @"
# Vulnerability Management (Skills + Keywords)

## Skills
- Tenable scanning, remediation coordination, risk prioritization
- STIG compliance validation, secure configuration baselines
- PowerShell remediation automation

## ATS Keywords
- vulnerability management, Tenable, remediation, risk, STIG, compliance
"@

Ensure-File "blocks/skills/secure_systems.md" @"
# Secure Systems Engineering (Skills + Keywords)

- STIG hardening, baseline validation, secure deployments
- logging/audit review, configuration management
"@

Ensure-File "blocks/skills/software_engineering.md" @"
# Software Engineering (Skills + Keywords)

- C#, .NET, WPF, Python, REST APIs
- architecture, testing, deployment, documentation
"@

Ensure-File "blocks/skills/devsecops.md" @"
# DevSecOps (Skills + Keywords)

- CI/CD concepts, containerization, automation scripts
- secure build/release patterns (only if used)
"@

# -------------------------------
# Blocks: Metrics / Keywords
# -------------------------------
Ensure-File "blocks/metrics/metrics_bank.md" @"
# Metrics Bank (Use Only If Defensible)

Format:
- Metric:
- Context:
- Timeframe:
- Source (provenance link):

Examples:
- 100% reduction in critical vulns — server team — 2025–Present — Log(N) Pacific — (source)
"@

Ensure-File "blocks/keywords/ats_keyword_bank.md" @"
# ATS Keyword Bank (Grouped)

## SIEM / SOC
- SIEM, Sentinel, MDE, KQL, log analytics, detections, alert tuning, threat hunting

## Vulnerability Management
- Tenable, remediation, risk prioritization, STIG, compliance audits

## Secure Systems / Gov
- DISA STIG, secure configuration baseline, audit logs, mission systems

## Software Engineering
- C#, .NET, WPF, Python, REST APIs, architecture, testing
"@

# -------------------------------
# Repo README guidance
# -------------------------------
Ensure-File "README.md" @"
# resume-library

This repository is the source of truth for Brian Hannigan resume materials.

## Key Concept
- **sources/master** = long-form master CV (reference)
- **blocks/** = reusable bullet/skill modules (lego bricks)
- **variants/** = generated job-ready outputs
- **job-targets/** = per-application packages (JD + tailored resume + notes)
- **changelog/** = audit trail of changes

## Workflow
1. Add/update content in **blocks/** and **sources/master**
2. Generate targeted resumes into **variants/** or **job-targets/**
3. Commit changes with clear messages (history matters)
"@

Write-Host ""
Write-Host "Done. Resume library structure initialized." -ForegroundColor Green
Write-Host "Tip: Commit this as: 'chore: initialize resume-library structure'" -ForegroundColor Green