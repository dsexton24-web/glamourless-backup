# GS Etsy Kit and Course Builder
# 1. Unpacks the new listing files (kits, courses, ebooks) into GS Etsy Upload Packages
# 2. Builds one toolkit zip per SKU from GS Etsy Supporting Docs
# Run it once. Safe to run again: it just overwrites what it made.
# Nothing is uploaded and nothing is deleted.

$Base     = 'G:\My Drive\Glamourless Systems Main'
$Packages = Join-Path $Base 'GS Etsy Upload Packages'
$Incoming = Join-Path $Base 'GS Etsy New Listing Files'
$Docs     = Join-Path $Base 'GS Etsy Supporting Docs'
$Report   = Join-Path $Incoming 'Kit Builder Report.txt'
$LogFile  = Join-Path $Incoming 'Kit Builder Log.txt'

$lines = New-Object System.Collections.Generic.List[string]
function Say($m) { Write-Host $m; $lines.Add($m) }
function L($p) { if ($p.StartsWith('\\?\')) { $p } else { '\\?\' + $p } }
function MakeDir($d) { [void][System.IO.Directory]::CreateDirectory((L $d)) }

try {
    Start-Transcript -LiteralPath $LogFile -Force | Out-Null
} catch { }

try {
    $ErrorActionPreference = 'Stop'
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    Say "PowerShell version: $($PSVersionTable.PSVersion)"

    # ---- Step 1: unpack the listing files ----
    $parts = Get-ChildItem -LiteralPath $Incoming -Filter '*.zip' | Sort-Object Name
    if (-not $parts) { throw "No part zips found in $Incoming" }
    $count = 0
    foreach ($z in $parts) {
        Say "Unpacking $($z.Name) ... this can take several minutes"
        $arc = [System.IO.Compression.ZipFile]::OpenRead($z.FullName)
        try {
            foreach ($e in $arc.Entries) {
                if ([string]::IsNullOrEmpty($e.Name)) { continue }
                $dest = Join-Path $Packages ($e.FullName -replace '/', '\')
                MakeDir (Split-Path $dest -Parent)
                [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, (L $dest), $true)
                $count++
                if ($count % 200 -eq 0) { Write-Host "  $count files unpacked" }
            }
        } finally { $arc.Dispose() }
    }
    Say "Unpacked $count files."

    # ---- Step 2: build the toolkit zips ----
    $list = Import-Csv -LiteralPath (Join-Path $Packages 'kit list.csv') -Encoding UTF8
    $ok = 0; $bad = 0; $i = 0
    foreach ($k in $list) {
        $i++
        $src = Join-Path $Docs $k.SourceFolder
        $kitDir = Join-Path $Packages $k.Key
        $zip = Join-Path $kitDir $k.ZipName
        if (-not [System.IO.Directory]::Exists((L $src))) { Say "MISSING source folder for $($k.Key): $src"; $bad++; continue }
        $files = [System.IO.Directory]::GetFiles((L $src)) | Where-Object { $_ -match '\.(docx|xlsx|pdf)$' }
        if (-not $files) { Say "NO DOCS in $src"; $bad++; continue }
        MakeDir $kitDir
        if ([System.IO.File]::Exists((L $zip))) { [System.IO.File]::Delete((L $zip)) }
        $arc = [System.IO.Compression.ZipFile]::Open((L $zip), 'Create')
        try {
            foreach ($f in $files) {
                [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($arc, $f, [System.IO.Path]::GetFileName($f), [System.IO.Compression.CompressionLevel]::Optimal)
            }
            $rm = Join-Path $kitDir 'Read Me First.txt'
            if ([System.IO.File]::Exists((L $rm))) {
                [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($arc, (L $rm), 'Read Me First.txt', [System.IO.Compression.CompressionLevel]::Optimal)
            }
        } finally { $arc.Dispose() }
        $mb = [math]::Round((New-Object System.IO.FileInfo (L $zip)).Length / 1MB, 2)
        if ($mb -gt 19.5) { Say "TOO BIG for Etsy (over 20 MB): $($k.Key) $mb MB"; $bad++ } else { $ok++ }
        if ($i % 20 -eq 0) { Write-Host "  $i of $($list.Count) toolkits done" }
    }
    Say "Toolkit zips built: $ok   Problems: $bad"
    Say 'Done. Next: open the uploader, pick the GS Etsy Upload Packages folder, click Upload all as drafts.'
}
catch {
    Say ''
    Say 'SOMETHING WENT WRONG:'
    Say $_.Exception.Message
    Say ("At line " + $_.InvocationInfo.ScriptLineNumber)
    Say 'Tell Claude: the details are in Kit Builder Log.txt in the GS Etsy New Listing Files folder.'
}
finally {
    try { $lines | Set-Content -LiteralPath $Report -Encoding UTF8 } catch { }
    try { Stop-Transcript | Out-Null } catch { }
    Read-Host 'Press Enter to close this window'
}
