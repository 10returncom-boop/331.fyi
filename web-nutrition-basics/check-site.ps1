<#
.SYNOPSIS
  Nutrition & Life - Batch site checker (3 checks)
.DESCRIPTION
  1. Scan all HTML for SEO elements (title / meta description / OG / JSON-LD)
  2. Check all internal links and image paths
  3. Detect 404 broken links by comparing local file existence
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File check-site.ps1
#>

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Nutrition & Life - Site Check" -ForegroundColor Cyan
Write-Host "  Root: $root" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$htmlFiles = Get-ChildItem -Path $root -Recurse -Filter "*.html" | Where-Object { $_.FullName -notmatch "\\_backup\\" -and $_.FullName -notmatch "\\_shots\\" }
Write-Host "Scanned $($htmlFiles.Count) HTML files`n" -ForegroundColor Green

# ============================================================
# CHECK 1: SEO elements
# ============================================================
Write-Host "===== Check 1: SEO Elements =====" -ForegroundColor Yellow
$seoIssues = @()

foreach ($f in $htmlFiles) {
  $rel = $f.FullName.Replace($root, "").TrimStart("\")
  $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)

  if ($content -notmatch "<title>[^<]+</title>") { $seoIssues += "[$rel] missing <title>" }
  if ($content -notmatch '<meta\s+name="description"\s+content="[^"]+"') { $seoIssues += "[$rel] missing meta description" }
  if ($content -notmatch '<link\s+rel="canonical"') { $seoIssues += "[$rel] missing canonical" }
  if ($content -notmatch '<meta\s+property="og:title"') { $seoIssues += "[$rel] missing og:title" }
  if ($content -notmatch '<meta\s+property="og:image"') { $seoIssues += "[$rel] missing og:image" }
  $ldCount = ([regex]::Matches($content, 'application/ld\+json')).Count
  if ($ldCount -eq 0) { $seoIssues += "[$rel] no JSON-LD" }
}

if ($seoIssues.Count -eq 0) {
  Write-Host "  [OK] All pages have required SEO elements`n" -ForegroundColor Green
} else {
  Write-Host "  Found $($seoIssues.Count) issues:" -ForegroundColor Red
  $seoIssues | ForEach-Object { Write-Host "    - $_" -ForegroundColor Red }
  Write-Host ""
}

# ============================================================
# CHECK 2+3: internal links, image paths, 404 broken links
# ============================================================
Write-Host "===== Check 2+3: Links, Images, Broken 404 =====" -ForegroundColor Yellow

$broken = @()
$checked = 0

foreach ($f in $htmlFiles) {
  $rel = $f.FullName.Replace($root, "").TrimStart("\")
  $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
  $baseDir = $f.DirectoryName

  $links = [regex]::Matches($content, '(?:href|src)="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

  foreach ($link in $links) {
    if ($link -match "^(https?://|mailto:|tel:|#|javascript:|data:)" -or [string]::IsNullOrEmpty($link)) { continue }

    $pathOnly = ($link -split "#")[0]
    if ([string]::IsNullOrEmpty($pathOnly)) { continue }

    $checked++

    $target = Join-Path $baseDir $pathOnly
    if (-not (Test-Path $target)) {
      $broken += "[$rel] NOT FOUND: $link"
    }
  }
}

Write-Host "  Checked $checked internal links/resources`n" -ForegroundColor Gray
if ($broken.Count -eq 0) {
  Write-Host "  [OK] No broken links`n" -ForegroundColor Green
} else {
  Write-Host "  Found $($broken.Count) broken links:" -ForegroundColor Red
  $broken | ForEach-Object { Write-Host "    - $_" -ForegroundColor Red }
  Write-Host ""
}

# ============================================================
# Summary
# ============================================================
Write-Host "===== Summary =====" -ForegroundColor Cyan
Write-Host "  HTML pages      : $($htmlFiles.Count)"
Write-Host "  SEO issues      : $($seoIssues.Count)"
Write-Host "  Links checked   : $checked"
Write-Host "  Broken links    : $($broken.Count)"
$totalIssues = $seoIssues.Count + $broken.Count
if ($totalIssues -eq 0) {
  Write-Host "`n  [ALL PASSED] Site check complete, no issues found." -ForegroundColor Green
} else {
  Write-Host "`n  [NEEDS FIX] $totalIssues issue(s) found." -ForegroundColor Red
}
