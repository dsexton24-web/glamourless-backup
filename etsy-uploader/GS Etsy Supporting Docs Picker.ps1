# GS Etsy Supporting Docs Picker
# COPIES (never moves or deletes) everything Etsy needs out of the SKU folders:
#   1. ALL supporting documents  -> GS Etsy Supporting Docs\<SKU folder>\   (log scores each one for Etsy value)
#   2. ALL HTML courses (IC-)    -> GS Etsy Courses#   3. Manuscripts from GS-0119 Survive AI Shift and GS-0197 Business Accelerator Pack -> GS Etsy Manuscripts# Lead magnets and Fix Something lane SKUs are left out (only the eligible list below is used).

$Root  = 'G:\My Drive\Glamourless Systems Main\Glamourless Systems Blueprints and Bundles'
$Base  = 'G:\My Drive\Glamourless Systems Main'
$OutSD = Join-Path $Base 'GS Etsy Supporting Docs'
$OutIC = Join-Path $Base 'GS Etsy Courses'
$OutMS = Join-Path $Base 'GS Etsy Manuscripts'
$ManuscriptPacks = @('GS-0119','GS-0197')
$Eligible = @('GS-0001','GS-0002','GS-0003','GS-0004','GS-0005','GS-0006','GS-0007','GS-0008','GS-0009','GS-0010','GS-0011','GS-0012','GS-0013','GS-0014','GS-0015','GS-0016','GS-0017','GS-0018','GS-0019','GS-0021','GS-0022','GS-0023','GS-0024','GS-0027','GS-0028','GS-0029','GS-0030','GS-0031','GS-0032','GS-0033','GS-0034','GS-0035','GS-0036','GS-0037','GS-0038','GS-0039','GS-0040','GS-0041','GS-0043','GS-0044','GS-0045','GS-0047','GS-0048','GS-0049','GS-0051','GS-0052','GS-0055','GS-0056','GS-0057','GS-0058','GS-0059','GS-0060','GS-0061','GS-0062','GS-0063','GS-0064','GS-0065','GS-0066','GS-0067','GS-0068','GS-0070','GS-0071','GS-0072','GS-0079','GS-0080','GS-0081','GS-0082','GS-0083','GS-0084','GS-0085','GS-0086','GS-0087','GS-0088','GS-0089','GS-0091','GS-0092','GS-0093','GS-0095','GS-0096','GS-0098','GS-0099','GS-0100','GS-0101','GS-0102','GS-0103','GS-0104','GS-0105','GS-0106','GS-0107','GS-0109','GS-0110','GS-0111','GS-0113','GS-0114','GS-0115','GS-0116','GS-0118','GS-0120','GS-0121','GS-0123','GS-0124','GS-0125','GS-0126','GS-0128','GS-0129','GS-0130','GS-0131','GS-0132','GS-0133','GS-0134','GS-0135','GS-0136','GS-0137','GS-0138','GS-0139','GS-0141','GS-0142','GS-0143','GS-0144','GS-0145','GS-0146','GS-0147','GS-0148','GS-0150','GS-0151','GS-0152','GS-0153','GS-0154','GS-0155','GS-0156','GS-0157','GS-0158','GS-0159','GS-0161','GS-0162','GS-0164','GS-0165','GS-0166','GS-0167','GS-0168','GS-0169','GS-0170','GS-0171','GS-0172','GS-0173','GS-0174','GS-0175','GS-0176','GS-0177','GS-0178','GS-0179','GS-0181','GS-0182','GS-0183','GS-0184','GS-0185','GS-0186','GS-0187','GS-0188','GS-0189','GS-0190','GS-0191','GS-0193','GS-0194','GS-0195','GS-0196','GS-0228','GS-0229','GS-0230','GS-0231','GS-0232','GS-0233','GS-0234','GS-0235','GS-0236','GS-0237','GS-0238','GS-0239','GS-0240','GS-0241','GS-0242','GS-0245','GS-0246','GS-0247','GS-0248','GS-0249','GS-0250','GS-0251','GS-0252','GS-0253','GS-0254','GS-0255','GS-0256','GS-0257','GS-0258','GS-0266','GS-0267','GS-0268','GS-0269','GS-0271','GS-0272','GS-0273','GS-0276','GS-0277','GS-0278','GS-0279','GS-0284','GS-0285','GS-0289','GS-0290','GS-0291','GS-0292','GS-0293','GS-0294','GS-0295','GS-0296','GS-0297','GS-0298','GS-0299') + $ManuscriptPacks

function Score-Doc($f) {
  $n = $f.BaseName; $s = 0
  if ($f.Extension -eq '.xlsx') { $s += 30 }
  if ($n -match 'Tracker|Dashboard|Calculator|Estimator|Spreadsheet|Workbook') { $s += 25 }
  if ($n -match 'Pricing|Price|Quote|Estimat|Bid') { $s += 20 }
  if ($n -match 'Contract|Forms|Agreement|Template|Intake|Proposal') { $s += 20 }
  if ($n -match 'Checklist|Inspection|Log') { $s += 15 }
  if ($n -match 'Script|Outreach|Sales|Pitch') { $s += 12 }
  if ($n -match 'Operations Manual|SOP|Playbook') { $s += 8 }
  if ($n -match 'Starter Kit|Launch Guide') { $s += 3 }
  if ($n -match 'Compliance|Legal|Regulat|Matrix|Escalation|UPL|Requirements') { $s -= 10 }
  $s += [math]::Min([math]::Round($f.Length / 10KB), 15)
  return $s
}

foreach ($p in @($OutSD,$OutIC,$OutMS)) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
$log = @(); $nSD = 0; $nIC = 0; $nMS = 0
$skuDirs = Get-ChildItem -Path $Root -Directory | Where-Object { $_.Name -match '^(GS-\d{4})' -and $Eligible -contains $Matches[1] } | Sort-Object Name
foreach ($d in $skuDirs) {
  $sku = $d.Name.Substring(0,7)
  $all = Get-ChildItem -Path $d.FullName -Recurse -File | Where-Object { $_.FullName -notmatch '\\(Blueprint|Archive)\\' }

  # Courses
  foreach ($c in ($all | Where-Object { $_.Name -match '^IC-' -and $_.Extension -eq '.html' })) {
    Copy-Item -LiteralPath $c.FullName -Destination $OutIC -Force; $nIC++
  }

  # Supporting docs (or manuscripts for the two collection packs)
  $docs = $all | Where-Object { $_.Extension -in '.docx','.xlsx','.pdf' -and $_.Name -notmatch '^(CV|MK|IC|HT)-' }
  if (-not $docs) { Write-Host "$sku  no supporting docs found" -ForegroundColor Yellow; continue }
  if ($ManuscriptPacks -contains $sku) { $dest = Join-Path $OutMS $d.Name } else { $dest = Join-Path $OutSD $d.Name }
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  foreach ($f in $docs) {
    Copy-Item -LiteralPath $f.FullName -Destination $dest -Force
    if ($ManuscriptPacks -contains $sku) { $nMS++ } else { $nSD++ }
    $log += [pscustomobject]@{ SKU = $sku; Folder = $d.Name; Document = $f.Name; Score = (Score-Doc $f); SizeKB = [math]::Round($f.Length/1KB) }
  }
  Write-Host "$sku  copied $($docs.Count) docs" -ForegroundColor Green
}
$log | Sort-Object Score -Descending | Export-Csv -Path (Join-Path $OutSD 'Supporting Docs Score Log.csv') -NoTypeInformation
Write-Host ""
Write-Host "Done. Supporting docs: $nSD   Courses: $nIC   Manuscripts: $nMS" -ForegroundColor Cyan
Read-Host "Press Enter to close"
