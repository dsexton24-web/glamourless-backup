# GS Etsy Kit and Course Builder
# 1. Unpacks the new listing files (kits, courses, ebooks) into GS Etsy Upload Packages
# 2. Builds one toolkit zip per SKU from GS Etsy Supporting Docs
# Run it once. Safe to run again: it just overwrites what it made.
# Nothing is uploaded and nothing is deleted.

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$Base     = 'G:\My Drive\Glamourless Systems Main'
$Packages = Join-Path $Base 'GS Etsy Upload Packages'
$Incoming = Join-Path $Base 'GS Etsy New Listing Files'
$Docs     = Join-Path $Base 'GS Etsy Supporting Docs'
$Report   = Join-Path $Incoming 'Kit Builder Report.txt'
function L($p) { if ($p.StartsWith('\\?\')) { $p } else { '\\?\' + $p } }

$lines = New-Object System.Collections.Generic.List[string]
function Say($m) { Write-Host $m; $lines.Add($m) }

# ---- Step 1: unpack the listing files ----
$parts = Get-ChildItem -LiteralPath $Incoming -Filter '*.zip' | Sort-Object Name
if (-not $parts) { Say "No part zips found in $Incoming"; exit 1 }
$count = 0
foreach ($z in $parts) {
    Say "Unpacking $($z.Name) ..."
    $arc = [System.IO.Compression.ZipFile]::OpenRead($z.FullName)
    try {
        foreach ($e in $arc.Entries) {
            if ([string]::IsNullOrEmpty($e.Name)) { continue }
            $dest = Join-Path $Packages ($e.FullName -replace '/', '\')
            $dir = Split-Path $dest -Parent
            if (-not (Test-Path -LiteralPath (L $dir))) { New-Item -ItemType Directory -Path (L $dir) -Force | Out-Null }
            [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, (L $dest), $true)
            $count++
        }
    } finally { $arc.Dispose() }
}
Say "Unpacked $count files."

# ---- Step 2: build the toolkit zips ----
$list = Import-Csv -LiteralPath (Join-Path $Packages 'kit list.csv')
$ok = 0; $bad = 0
foreach ($k in $list) {
    $src = Join-Path $Docs $k.SourceFolder
    $kitDir = Join-Path $Packages $k.Key
    $zip = Join-Path $kitDir $k.ZipName
    if (-not (Test-Path -LiteralPath (L $src))) { Say "MISSING source folder for $($k.Key): $src"; $bad++; continue }
    $files = Get-ChildItem -LiteralPath (L $src) -File | Where-Object { $_.Extension -in '.docx', '.xlsx', '.pdf' }
    if (-not $files) { Say "NO DOCS in $src"; $bad++; continue }
    if (Test-Path -LiteralPath (L $zip)) { Remove-Item -LiteralPath (L $zip) -Force }
    $arc = [System.IO.Compression.ZipFile]::Open((L $zip), 'Create')
    try {
        foreach ($f in $files) {
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($arc, $f.FullName, $f.Name, 'Optimal') | Out-Null
        }
        $rm = Join-Path $kitDir 'Read Me First.txt'
        if (Test-Path -LiteralPath (L $rm)) {
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($arc, (L $rm), 'Read Me First.txt', 'Optimal') | Out-Null
        }
    } finally { $arc.Dispose() }
    $mb = [math]::Round((Get-Item -LiteralPath (L $zip)).Length / 1MB, 2)
    if ($mb -gt 19.5) { Say "TOO BIG for Etsy (over 20 MB): $($k.Key) $mb MB"; $bad++ } else { $ok++ }
}
Say "Toolkit zips built: $ok   Problems: $bad"
$lines | Set-Content -LiteralPath $Report -Encoding UTF8
Say "Report saved to $Report"
Say 'Done. Next: open the uploader, pick the GS Etsy Upload Packages folder, click Upload all as drafts.'
