<#
.SYNOPSIS
    Supplement to run-review-tests-2.ps1 (2026-10-09): cases whose setup was wrong in that run.

.DESCRIPTION
    Run from PowerShell (never Git Bash) in the workspace root:
        powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-review\run-review-tests-2b.ps1
    - B2: PDF strings that only the build writes, outside the page text and the info dictionary: a bookmark title
      assembled from two macros (OpenAI) and a catalog entry written as a hex string (Anthropic). Under cas-sc (B1)
      the bookmark plant never reached the PDF (the class's PDF has no outlines), so B2 uses templates\article-modular,
      whose hyperref writes bookmarks.
    - H1b-H3b: the hand-made class of H1-H3 (run-review-tests.ps1 and -2.ps1 replaced "\documentclass{article}",
      which the wrapper does not contain, so those runs tested the standard class article).
    - E2: elsarticle (class generated from the archive, SHA-256 in the SOURCES.tsv note) with a substitute for
      example-image-a (package mwe is not installed), so that only [template-origin] is under test.
    Writes outputs-2026-10-09\<case>.txt and results-2026-10-09-part2.txt here; moves the test projects, their
    outputs and the copy of the old packager to tmp\packager-review-2b\.
#>
param(
    [string]$New = "scripts\package-project.ps1",
    [string]$OldSource = "archives\test-evidence\2026-10-08\packager-review\inputs\package-project-before-review.ps1"
)

$ErrorActionPreference = 'Continue'
$here = $PSScriptRoot
$workspace = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$inputs = Join-Path $here "inputs"
$outDir = Join-Path $here "outputs-2026-10-09"
$resultsFile = Join-Path $here "results-2026-10-09-part2.txt"
$scratch = Join-Path $workspace "tmp\packager-review-2b"
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = $utf8
New-Item -ItemType Directory -Force -Path $outDir, $scratch | Out-Null
$results = New-Object System.Collections.Generic.List[string]
$Old = "scripts\zz-package-project-before-review.ps1"
Copy-Item -LiteralPath (Join-Path $workspace $OldSource) -Destination (Join-Path $workspace $Old) -Force

function New-TemplateCopy([string]$Name, [string]$Template) {
    $target = Join-Path $workspace "projects\$Name"
    if (Test-Path -LiteralPath $target) { throw "Test project exists already: $target" }
    Copy-Item -Recurse -LiteralPath (Join-Path $workspace "templates\$Template") -Destination $target
    return $target
}

function Invoke-Packager([string]$Script, [string]$Label, [string[]]$Arguments) {
    $lines = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Script @Arguments 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    [IO.File]::WriteAllLines((Join-Path $outDir "$Label.txt"), [string[]]$lines, $utf8)
    $verdict = @($lines | Where-Object { $_ -like 'Verdict:*' }) | Select-Object -Last 1
    $trace = @($lines | Where-Object { $_ -like 'Trace scan:*' }) | Select-Object -Last 1
    $results.Add(("{0,-40} exit {1}  {2}  {3}" -f $Label, $code, $verdict, $trace))
    foreach ($hit in @($lines | Where-Object { $_ -like '*] FAIL:*' -or $_ -like '*[[]template-origin[]]*' -or $_ -like 'Template*' })) {
        $results.Add("    " + $hit.Substring(0, [Math]::Min(200, $hit.Length)))
    }
    return , $lines
}

function Invoke-Both([string]$Label, [string[]]$Arguments) {
    [void](Invoke-Packager (Join-Path $workspace $Old) "$Label-before" $Arguments)
    [void](Invoke-Packager (Join-Path $workspace $New) "$Label-after" $Arguments)
}

# --- B2: bookmark title and catalog hex string that only the build writes -------------------------------------------
$p = New-TemplateCopy "zz-review-build-b" "article-modular"
$wrapper = Join-Path $p "main.tex"
$text = [IO.File]::ReadAllText($wrapper, $utf8)
$plants = "\def\plantC{Open}\def\plantD{AI}`n\pdfbookmark[1]{\plantC\plantD}{plant-bookmark}`n\pdfcatalog{/PlantNote <416E7468726F706963>}`n`n\end{document}"
if ($text.IndexOf("\end{document}") -lt 0) { throw "no \end{document} in $wrapper" }
[IO.File]::WriteAllText($wrapper, $text.Replace("\end{document}", $plants), $utf8)
Invoke-Both "b2-bookmark-and-catalog-strings" @("-Project", "zz-review-build-b")

# --- H1b-H3b: a hand-made class in the project ----------------------------------------------------------------------
$p = New-TemplateCopy "zz-review-handmade" "article-modular"
Copy-Item -LiteralPath (Join-Path $inputs "handmade\journalx.cls") -Destination $p
$wrapper = Join-Path $p "main.tex"
$text = [IO.File]::ReadAllText($wrapper, $utf8)
$changed = [regex]::Replace($text, '\\documentclass(\[[^\]]*\])?\{article\}', '\documentclass$1{journalx}')
if ($changed -eq $text) { throw "no \documentclass{article} in $wrapper" }
[IO.File]::WriteAllText($wrapper, $changed, $utf8)
Invoke-Both "h1b-handmade-auto" @("-Project", "zz-review-handmade", "-CheckOnly")
Invoke-Both "h2b-handmade-template-article-modular" @("-Project", "zz-review-handmade", "-Template", "article-modular", "-CheckOnly")
Invoke-Both "h3b-handmade-template-els-cas" @("-Project", "zz-review-handmade", "-Template", "els-cas", "-CheckOnly")

# --- E2: elsarticle with a substitute image -------------------------------------------------------------------------
$p = Join-Path $workspace "projects\zz-review-elsarticle"
if (Test-Path -LiteralPath $p) { throw "Test project exists already: $p" }
New-Item -ItemType Directory -Force -Path $p | Out-Null
foreach ($f in @("elsarticle.cls", "elsarticle-num.bst")) { Copy-Item (Join-Path $workspace "templates\elsarticle\$f") $p }
Copy-Item (Join-Path $workspace "templates\elsarticle\elsarticle-template-num.tex") (Join-Path $p "main.tex")
Copy-Item (Join-Path $workspace "templates\els-cas\thumbnails\cas-email.jpeg") (Join-Path $p "example-image-a.jpg")
Invoke-Both "e2-elsarticle-generated-class" @("-Project", "zz-review-elsarticle", "-Template", "elsarticle", "-Flat")

[IO.File]::WriteAllLines($resultsFile, [string[]]$results, $utf8)
$results

# --- Clean-up -------------------------------------------------------------------------------------------------------
foreach ($kind in @("projects", "outputs")) {
    $destination = Join-Path $scratch $kind
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    foreach ($folder in @(Get-ChildItem -LiteralPath (Join-Path $workspace $kind) -Directory -Filter "zz-review-*")) {
        $target = Join-Path $destination $folder.Name
        if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
        Move-Item -LiteralPath $folder.FullName -Destination $target
    }
}
Move-Item -LiteralPath (Join-Path $workspace $Old) -Destination (Join-Path $scratch "zz-package-project-before-review.ps1") -Force
