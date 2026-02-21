<#
index-inbox.ps1
Recursively indexes sources/inbox (including nested folders) and creates:
- sources/inbox/_inventory.csv
- sources/inbox/_inventory.md

Optional:
- -MakeFlatCopy creates sources/inbox_flat with copied files (originals untouched)
- -Force overwrites existing inventory files
#>

param(
  [string]$Inbox = "sources\inbox",
  [switch]$MakeFlatCopy,
  [switch]$Force
)

function Ensure-Dir {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path | Out-Null
  }
}

function Write-FileSafe {
  param(
    [string]$Path,
    [string]$Content
  )
  if ((Test-Path -LiteralPath $Path) -and (-not $Force)) {
    Write-Host "Exists (use -Force to overwrite): $Path"
    return
  }
  $parent = Split-Path -Parent $Path
  if ($parent) { Ensure-Dir $parent }
  Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
  Write-Host "Wrote: $Path"
}

if (-not (Test-Path -LiteralPath $Inbox)) {
  throw "Inbox folder not found: $Inbox"
}

# File types to index (add more if needed)
$exts = @(".docx", ".doc", ".pdf", ".odt", ".rtf", ".txt", ".md")

$files = Get-ChildItem -LiteralPath $Inbox -Recurse -File |
  Where-Object { $exts -contains $_.Extension.ToLowerInvariant() } |
  Sort-Object FullName

$records = @()
foreach ($f in $files) {
  $rel = Resolve-Path -LiteralPath $f.FullName | ForEach-Object {
    $_.Path.Substring((Resolve-Path -LiteralPath $Inbox).Path.Length).TrimStart('\','/')
  }

  $records += [pscustomobject]@{
    FileName     = $f.Name
    Extension    = $f.Extension.ToLowerInvariant()
    RelativePath = $rel
    FullPath     = $f.FullName
    SizeKB       = [math]::Round($f.Length / 1KB, 1)
    Modified     = $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
  }
}

# Output CSV
$csvPath = Join-Path $Inbox "_inventory.csv"
if ((Test-Path -LiteralPath $csvPath) -and (-not $Force)) {
  Write-Host "Exists (use -Force to overwrite): $csvPath"
} else {
  $records | Export-Csv -LiteralPath $csvPath -NoTypeInformation -Encoding UTF8
  Write-Host "Wrote: $csvPath"
}

# Output MD
$mdLines = New-Object System.Collections.Generic.List[string]
$mdLines.Add("# Inbox Inventory")
$mdLines.Add("")
$mdLines.Add("**Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
$mdLines.Add("")
$mdLines.Add("Total files indexed: **$($records.Count)**")
$mdLines.Add("")
$mdLines.Add("| File | Type | Size (KB) | Modified | Relative Path |")
$mdLines.Add("|---|---:|---:|---:|---|")

foreach ($r in $records) {
  $mdLines.Add("| $($r.FileName) | $($r.Extension) | $($r.SizeKB) | $($r.Modified) | $($r.RelativePath) |")
}

$mdPath = Join-Path $Inbox "_inventory.md"
Write-FileSafe -Path $mdPath -Content ($mdLines -join "`n")

# Optional: make flat copy (non-destructive)
if ($MakeFlatCopy) {
  $flatDir = "sources\inbox_flat"
  Ensure-Dir $flatDir

  foreach ($r in $records) {
    # Create a unique, stable filename: folder path + original name
    $safeRel = ($r.RelativePath -replace '[\\\/]+','__') -replace '[^\w\.\-__]','_'
    $dest = Join-Path $flatDir $safeRel

    if ((Test-Path -LiteralPath $dest) -and (-not $Force)) { continue }
    Copy-Item -LiteralPath $r.FullPath -Destination $dest -Force
  }

  Write-Host "Flat copy created at: $flatDir"
}

Write-Host ""
Write-Host "Done. Inventory generated." -ForegroundColor Green