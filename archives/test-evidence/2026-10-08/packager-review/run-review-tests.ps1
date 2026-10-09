<#
.SYNOPSIS
    Repeats the tests of the packager changes made after the review of 2026-10-08 (trace scan, template origin,
    AI declaration) against the packager before the change.

.DESCRIPTION
    Run from PowerShell (never Git Bash) in the workspace root:
        powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-review\run-review-tests.ps1
    Copies inputs\package-project-before-review.ps1 to scripts\zz-package-project-before-review.ps1 (a packager
    finds the workspace from its own folder), builds the test projects projects\zz-review-* from
    projects\clanok-1-min-cut-path, templates\article-modular and templates\elsarticle with the overlays in inputs\,
    runs every case with the packager before (-Old) and after (-New) the change, writes outputs\*.txt and
    results.txt here, and finally moves the test projects, their outputs, the sandbox and the old packager copy to
    tmp\packager-review\.
#>
param(
    [string]$New = "scripts\package-project.ps1",
    [string]$OldSource = "archives\test-evidence\2026-10-08\packager-review\inputs\package-project-before-review.ps1"
)

$ErrorActionPreference = 'Continue'      # native tools write notices to stderr (MiKTeX update reminder)
$here = $PSScriptRoot
$workspace = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$inputs = Join-Path $here "inputs"
$outDir = Join-Path $here "outputs"
$scratch = Join-Path $workspace "tmp\packager-review"
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = $utf8
New-Item -ItemType Directory -Force -Path $outDir, $scratch | Out-Null
$results = New-Object System.Collections.Generic.List[string]
$Old = "scripts\zz-package-project-before-review.ps1"
Copy-Item -LiteralPath (Join-Path $workspace $OldSource) -Destination (Join-Path $workspace $Old) -Force

function Copy-Overlay([string]$From, [string]$To) {
    foreach ($file in @(Get-ChildItem -LiteralPath $From -Recurse -File)) {
        $target = Join-Path $To $file.FullName.Substring($From.Length + 1)
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    }
}

# A copy of article 1 without its README (the workspace-only file is excluded anyway).
function New-ArticleCopy([string]$Name) {
    $target = Join-Path $workspace "projects\$Name"
    if (Test-Path -LiteralPath $target) { throw "Test project exists already: $target" }
    Copy-Item -Recurse -LiteralPath (Join-Path $workspace "projects\clanok-1-min-cut-path") -Destination $target
    Remove-Item -LiteralPath (Join-Path $target "README.md") -Force
    return $target
}

# Inserts lines after (or before) the first line whose trimmed text equals $Anchor.
function Edit-Lines([string]$File, [string]$Anchor, [string[]]$Lines, [switch]$Before) {
    $text = [IO.File]::ReadAllText($File, $utf8)
    $list = New-Object System.Collections.Generic.List[string]
    $list.AddRange([string[]]($text -split "`n"))
    $index = -1
    for ($i = 0; $i -lt $list.Count; $i++) { if ($list[$i].TrimEnd("`r").Trim() -eq $Anchor) { $index = $i; break } }
    if ($index -lt 0) { throw "Anchor not found in ${File}: $Anchor" }
    $at = $(if ($Before) { $index } else { $index + 1 })
    $list.InsertRange($at, $Lines)
    [IO.File]::WriteAllText($File, ($list -join "`n"), $utf8)
}

function Invoke-Packager([string]$Script, [string]$Label, [string[]]$Arguments) {
    $lines = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Script @Arguments 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    [IO.File]::WriteAllLines((Join-Path $outDir "$Label.txt"), [string[]]$lines, $utf8)
    $verdict = @($lines | Where-Object { $_ -like 'Verdict:*' }) | Select-Object -Last 1
    $trace = @($lines | Where-Object { $_ -like 'Trace scan:*' }) | Select-Object -Last 1
    $results.Add(("{0,-36} exit {1}  {2}  {3}" -f $Label, $code, $verdict, $trace))
    return , $lines
}

function Invoke-Both([string]$Label, [string[]]$Arguments) {
    [void](Invoke-Packager (Join-Path $workspace $Old) "$Label-before" $Arguments)
    [void](Invoke-Packager (Join-Path $workspace $New) "$Label-after" $Arguments)
}

$main = "main.tex"
$authorLine = "\hypersetup{pdfauthor={Norbert Miche" + [char]0x013E + "}}"

# --- S1: static plants of the trace review, run 1 ----------------------------------------------------------------
$p = New-ArticleCopy "zz-review-static"
Copy-Overlay (Join-Path $inputs "static") $p
Edit-Lines (Join-Path $p $main) $authorLine @("\hypersetup{pdfsubject={Sonnet 4.5 draft}}")
Edit-Lines (Join-Path $p $main) "\input{sections/07-conclusion}" @("\input{sections/95-plants}")
$bib = Join-Path $p "references.bib"
[IO.File]::WriteAllText($bib, [IO.File]::ReadAllText($bib, $utf8).Replace("  isbn      = {978-0-521-79722-1},", "  isbn      = {978-0-521-79722-1},`n  annote    = {Sonnet 4.5 check},"), $utf8)
Invoke-Both "s1-static-plants" @("-Project", "zz-review-static", "-Template", "els-cas", "-Flat", "-CheckOnly")

# --- S2: static plants, run 2 (\iffalse, .inc, no extension, UTF-16, sub-folder, XMP, unread declaration name) --
$p = New-ArticleCopy "zz-review-static-b"
Copy-Overlay (Join-Path $inputs "static-b") $p
Edit-Lines (Join-Path $p $main) $authorLine @("\hypersetup{pdfkeywords={Claude}}")
Edit-Lines (Join-Path $p $main) "\input{sections/07-conclusion}" @("\input{sections/95-plants}", "\input{sections/96-plant.inc}", "\input{sections/97-plant}")
Invoke-Both "s2-static-plants-b" @("-Project", "zz-review-static-b", "-Template", "els-cas", "-CheckOnly")

# --- B1: names that only the build produces (macros, hex and octal info strings), with a correct declaration ------
$p = New-ArticleCopy "zz-review-build"
Copy-Overlay (Join-Path $inputs "build") $p
Copy-Overlay (Join-Path $inputs "declaration") $p
Edit-Lines (Join-Path $p $main) $authorLine @("\pdfinfo{/Generator <436C61756465>}", "\pdfinfo{/Tool (\103laude)}")
Edit-Lines (Join-Path $p $main) "\input{sections/07-conclusion}" @("\input{sections/95-build-plants}", "\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}", "\input{sections/91-ai-declaration}")
Invoke-Both "b1-build-time-plants" @("-Project", "zz-review-build", "-Template", "els-cas", "-Flat")

# --- U1: a file named like the declaration that nothing reads -------------------------------------------------------
$p = New-ArticleCopy "zz-review-unread"
Copy-Overlay (Join-Path $inputs "unread-declaration") $p
Invoke-Both "u1-unread-declaration" @("-Project", "zz-review-unread", "-Template", "els-cas", "-Flat")

# --- D1: the declaration inserted as the draft says (heading in main.tex before the acknowledgments) --------------
$p = New-ArticleCopy "zz-review-declaration"
Copy-Overlay (Join-Path $inputs "declaration") $p
Edit-Lines (Join-Path $p $main) "\section*{Acknowledgments}" -Before @("\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}", "\input{sections/91-ai-declaration}", "")
Invoke-Both "d1-declaration-complete" @("-Project", "zz-review-declaration", "-Template", "els-cas", "-Flat")

# --- D2: the declaration with placeholders and a comment that names the tool --------------------------------------
$p = New-ArticleCopy "zz-review-declaration-draft"
Copy-Overlay (Join-Path $inputs "declaration-unfinished") $p
Edit-Lines (Join-Path $p $main) "\section*{Acknowledgments}" -Before @("\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}", "\input{sections/91-ai-declaration}", "")
Invoke-Both "d2-declaration-unfinished" @("-Project", "zz-review-declaration-draft", "-Template", "els-cas", "-CheckOnly")

# --- H: a hand-made class in the project ---------------------------------------------------------------------------
$p = Join-Path $workspace "projects\zz-review-handmade"
Copy-Item -Recurse -LiteralPath (Join-Path $workspace "templates\article-modular") -Destination $p
Copy-Item -LiteralPath (Join-Path $inputs "handmade\journalx.cls") -Destination $p
$wrapper = Join-Path $p $main
[IO.File]::WriteAllText($wrapper, [IO.File]::ReadAllText($wrapper, $utf8).Replace("\documentclass{article}", "\documentclass{journalx}"), $utf8)
Invoke-Both "h1-handmade-auto" @("-Project", "zz-review-handmade", "-CheckOnly")
Invoke-Both "h2-handmade-template-article-modular" @("-Project", "zz-review-handmade", "-Template", "article-modular", "-CheckOnly")
Invoke-Both "h3-handmade-template-els-cas" @("-Project", "zz-review-handmade", "-Template", "els-cas", "-CheckOnly")

# --- E1: elsarticle, whose class is generated from the archive (SHA-256 recorded in the SOURCES.tsv note) ----------
$p = Join-Path $workspace "projects\zz-review-elsarticle"
New-Item -ItemType Directory -Force -Path $p | Out-Null
foreach ($f in @("elsarticle.cls", "elsarticle-num.bst")) { Copy-Item (Join-Path $workspace "templates\elsarticle\$f") $p }
Copy-Item (Join-Path $workspace "templates\elsarticle\elsarticle-template-num.tex") (Join-Path $p $main)
Invoke-Both "e1-elsarticle-generated-class" @("-Project", "zz-review-elsarticle", "-CheckOnly")

# --- X: sandbox copy of the workspace with varied templates\SOURCES.tsv and an edited template folder ----------------
$sandbox = Join-Path $scratch "sandbox"
if (Test-Path -LiteralPath $sandbox) { Remove-Item -LiteralPath $sandbox -Recurse -Force }
foreach ($d in @("scripts", "templates\els-cas", "archives", "projects\zz-cas")) { New-Item -ItemType Directory -Force -Path (Join-Path $sandbox $d) | Out-Null }
Copy-Item (Join-Path $workspace $New) (Join-Path $sandbox "scripts\new.ps1")
Copy-Item (Join-Path $workspace $Old) (Join-Path $sandbox "scripts\old.ps1")
foreach ($f in @("cas-sc.cls", "cas-common.sty", "cas-model2-names.bst")) {
    Copy-Item (Join-Path $workspace "templates\els-cas\$f") (Join-Path $sandbox "templates\els-cas")
    Copy-Item (Join-Path $workspace "templates\els-cas\$f") (Join-Path $sandbox "projects\zz-cas")
}
Copy-Item (Join-Path $workspace "templates\els-cas\cas-sc-template.tex") (Join-Path $sandbox "templates\els-cas")
Copy-Item (Join-Path $workspace "templates\els-cas\cas-sc-template.tex") (Join-Path $sandbox "projects\zz-cas\main.tex")
Copy-Item -Recurse (Join-Path $workspace "templates\els-cas\thumbnails") (Join-Path $sandbox "templates\els-cas")
Copy-Item -Recurse (Join-Path $workspace "templates\els-cas\thumbnails") (Join-Path $sandbox "projects\zz-cas")
Copy-Item (Join-Path $workspace "templates\els-cas\cas-refs.bib") (Join-Path $sandbox "projects\zz-cas")
Copy-Item (Join-Path $workspace "archives\els-cas-templates.zip") (Join-Path $sandbox "archives")
$realTsv = [IO.File]::ReadAllLines((Join-Path $workspace "templates\SOURCES.tsv"), $utf8)
$tsvHeader = $realTsv[0]
$tsvRow = @($realTsv | Where-Object { $_ -like "els-cas`t*" })[0]
$sandboxTsv = Join-Path $sandbox "templates\SOURCES.tsv"
function Set-SandboxTsv([string]$Row) { [IO.File]::WriteAllText($sandboxTsv, (($tsvHeader, $Row) -join "`n") + "`n", $utf8) }
function Invoke-SandboxBoth([string]$Label) {
    [void](Invoke-Packager (Join-Path $sandbox "scripts\old.ps1") "$Label-before" @("-Project", "zz-cas", "-CheckOnly"))
    [void](Invoke-Packager (Join-Path $sandbox "scripts\new.ps1") "$Label-after" @("-Project", "zz-cas", "-CheckOnly"))
}
Set-SandboxTsv $tsvRow
Invoke-SandboxBoth "x1-sandbox-baseline"
Set-SandboxTsv ($tsvRow.Replace("els-cas`tvenue`t", "els-cas`thouse`t"))
Invoke-SandboxBoth "x2-sandbox-kind-house"
Set-SandboxTsv $tsvRow
$plant = "`n% Patched with Claude Code, see " + (Join-Path $workspace "CLAUDE.md") + "`n"
foreach ($copy in @("templates\els-cas\cas-common.sty", "projects\zz-cas\cas-common.sty")) { [IO.File]::AppendAllText((Join-Path $sandbox $copy), $plant, $utf8) }
Invoke-SandboxBoth "x3-sandbox-edited-template-sty"
foreach ($f in @("cas-common.sty")) {
    Copy-Item (Join-Path $workspace "templates\els-cas\$f") (Join-Path $sandbox "templates\els-cas") -Force
    Copy-Item (Join-Path $workspace "templates\els-cas\$f") (Join-Path $sandbox "projects\zz-cas") -Force
}
foreach ($copy in @("templates\els-cas\cas-sc.cls", "projects\zz-cas\cas-sc.cls")) { [IO.File]::AppendAllText((Join-Path $sandbox $copy), "`n\def\baselinestretch{0.9}`n", $utf8) }
Invoke-SandboxBoth "x4-sandbox-edited-template-cls"

[IO.File]::WriteAllLines((Join-Path $here "results.txt"), [string[]]$results, $utf8)
$results

# --- Clean-up: test projects, their outputs, the sandbox and the old packager to tmp\packager-review\ --------------
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
