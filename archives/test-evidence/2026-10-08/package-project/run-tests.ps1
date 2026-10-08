# Test driver for scripts/package-project.ps1 (2026-10-08). Run from the workspace root:
#   .\archives\test-evidence\2026-10-08\package-project\run-tests.ps1 [-Only <name-prefix>]
# Creates the test projects projects/_pkgtest-* (from templates/ and from inputs/), runs every case, writes one log per
# case to logs/ and the table to results.txt, and moves projects/_pkgtest-* and outputs/_pkgtest-* to tmp/pkgtest/.
# ASCII only. Does not touch any other project.
param([string]$Only = "")

$workspace = (Get-Location).Path
$evidence = Join-Path $workspace "archives\test-evidence\2026-10-08\package-project"
$logs = Join-Path $evidence "logs"
$inputs = Join-Path $evidence "inputs"
$pkgtmp = Join-Path $workspace "tmp\pkgtest"
$utf8 = New-Object System.Text.UTF8Encoding $false
$stamp = Get-Date -Format "yyyyMMdd"
New-Item -ItemType Directory -Force -Path $logs, $pkgtmp | Out-Null
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$script:rows = New-Object System.Collections.Generic.List[string]
$script:bad = 0

function Move-TestProjects {
    foreach ($root in "projects", "outputs") {
        foreach ($d in @(Get-ChildItem -LiteralPath (Join-Path $workspace $root) -Directory -Filter "_pkgtest-*")) {
            $target = Join-Path $pkgtmp ($root + "-" + $d.Name)
            if (Test-Path -LiteralPath $target) { [IO.Directory]::Delete($target, $true) }
            Move-Item -LiteralPath $d.FullName -Destination $target
        }
    }
}
function Remove-TestProject([string]$Name) {
    if ($Name -notlike "_pkgtest-*") { throw "refusing to delete $Name" }
    $p = Join-Path $workspace "projects\$Name"
    if (Test-Path -LiteralPath $p) { [IO.Directory]::Delete($p, $true) }
}
function New-ArticleProject([string]$Name = "_pkgtest-article") {
    Remove-TestProject $Name
    Copy-Item -LiteralPath (Join-Path $inputs "_pkgtest-article") -Destination (Join-Path $workspace "projects\$Name") -Recurse
}
function New-TemplateProject([string]$Template, [string]$Name) {
    Remove-TestProject $Name
    Copy-Item -LiteralPath (Join-Path $workspace "templates\$Template") -Destination (Join-Path $workspace "projects\$Name") -Recurse
}
function Append-Text([string]$Project, [string]$Rel, [string]$Text) {
    [IO.File]::AppendAllText((Join-Path $workspace "projects\$Project\$Rel"), $Text, $utf8)
}
function Write-Text([string]$Project, [string]$Rel, [string]$Text) {
    $p = Join-Path $workspace "projects\$Project\$Rel"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $p) | Out-Null
    [IO.File]::WriteAllText($p, $Text, $utf8)
}
function Get-ZipNames([string]$Zip) {
    $s = [IO.File]::OpenRead($Zip); $z = New-Object System.IO.Compression.ZipArchive($s, 'Read')
    $n = @($z.Entries | ForEach-Object { $_.FullName }); $z.Dispose(); $s.Dispose(); return $n
}
function Get-ZipText([string]$Zip, [string]$Name) {
    $s = [IO.File]::OpenRead($Zip); $z = New-Object System.IO.Compression.ZipArchive($s, 'Read')
    $r = New-Object IO.StreamReader($z.GetEntry($Name).Open(), $utf8); $t = $r.ReadToEnd(); $r.Dispose(); $z.Dispose(); $s.Dispose(); return $t
}

# Runs one case. $Expect = sorted list of finding categories other than [comment]; $Extra returns "" or a failure text.
function Test-Case([string]$Name, [hashtable]$Arguments, [int]$ExitCode, [string[]]$Expect, [scriptblock]$Extra = $null) {
    if ($Only -and -not $Name.StartsWith($Only)) { return }
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $out = & (Join-Path $workspace "scripts\package-project.ps1") @Arguments *>&1 | Out-String
    $code = $LASTEXITCODE
    $out | Out-File -LiteralPath (Join-Path $logs "$Name.txt") -Encoding utf8
    $lines = $out -split "`r?`n"
    $cats = @($lines | ForEach-Object { if ($_ -match '^.+?:\d+: \[([a-z-]+)\]') { $Matches[1] } } | Where-Object { $_ -ne "comment" } | Sort-Object -Unique)
    $verdict = ($lines | Where-Object { $_ -like "Verdict:*" } | Select-Object -Last 1)
    if (-not $verdict) { $verdict = "(no verdict line)" }
    $pages = ""
    $pl = $lines | Where-Object { $_ -like "Pages:*" } | Select-Object -First 1
    if ($pl) { $pages = ($pl -replace '^Pages:\s*', '') }
    $zipInfo = ""
    $zl = $lines | Where-Object { $_ -like "Zip:*" } | Select-Object -First 1
    if ($zl) {
        $zp = ($zl -replace '^Zip:\s*', '').Trim()
        $n = ($lines | Where-Object { $_ -like "Files in the zip (*" } | Select-Object -First 1)
        $count = ""
        if ($n -match '\((\d+),') { $count = $Matches[1] }
        $zipInfo = "{0} bytes, {1} entries" -f (Get-Item -LiteralPath $zp).Length, $count
    }
    $problem = ""
    if ($code -ne $ExitCode) { $problem += " exit code $code, expected $ExitCode;" }
    if (($cats -join ",") -ne ((@($Expect) | Sort-Object) -join ",")) { $problem += " categories [$($cats -join ',')], expected [$((@($Expect) | Sort-Object) -join ',')];" }
    if ($Extra) { $e = & $Extra; if ($e) { $problem += " $e" } }
    $ok = $(if ($problem) { "MISMATCH:$problem" } else { "ok" })
    if ($problem) { $script:bad++ }
    $row = "{0,-34} exit {1}  {2,-34} cats [{3}]  pages {4}  {5}  {6:N0} s  {7}" -f $Name, $code, $verdict, ($cats -join ","), $pages, $zipInfo, $sw.Elapsed.TotalSeconds, $ok
    $script:rows.Add($row)
    Write-Host $row
}

Move-TestProjects

# ---------------------------------------------------------------------------- Test 1: article 1 (class new-aiaa, BibTeX)
$a1 = @{ Project = "clanok-1-min-cut-path" }
Test-Case "t1-default" $a1 0 @("layout") {
    $zip = Join-Path $workspace "outputs\clanok-1-min-cut-path\package\clanok-1-min-cut-path-$stamp.zip"
    $names = Get-ZipNames $zip
    if (@($names | Where-Object { $_.Contains('\') -or $_.StartsWith('/') }).Count -gt 0) { return "zip entries with backslash or leading slash" }
    if ($names -notcontains "main.tex" -or $names -notcontains "main.bbl" -or $names -contains "README.md") { return "unexpected zip content" }
}
Test-Case "t1-flat" ($a1 + @{ Flat = $true }) 0 @("layout") {
    $zip = Join-Path $workspace "outputs\clanok-1-min-cut-path\package\clanok-1-min-cut-path-$stamp-flat.zip"
    $names = Get-ZipNames $zip
    $fresh = Join-Path $pkgtmp "flat-extract-$(Get-Date -Format HHmmss)"
    [IO.Compression.ZipFile]::ExtractToDirectory($zip, $fresh)
    $sub = @(Get-ChildItem -LiteralPath $fresh -Recurse -Directory).Count
    $back = @($names | Where-Object { $_.Contains('\') }).Count
    if ($sub -ne 0 -or $back -ne 0 -or @($names | Where-Object { $_.Contains('/') }).Count -ne 0) { return "flat zip has $sub subfolders, $back backslash entries" }
}
Test-Case "t1-checkonly" ($a1 + @{ CheckOnly = $true }) 0 @("layout")
Test-Case "t1-keepcomments" ($a1 + @{ KeepComments = $true }) 0 @("layout")
Test-Case "t1-maxpages20" ($a1 + @{ MaxPages = 20 }) 0 @("layout", "pages")

# ---------------------------------------------------------------------------- Test 2: article-modular copy (standard class)
$ta = @{ Project = "_pkgtest-article" }
New-ArticleProject
Test-Case "t2-article-checkonly" ($ta + @{ CheckOnly = $true }) 0 @()
Test-Case "t2-article-default" $ta 0 @()
Test-Case "t2-article-flat" ($ta + @{ Flat = $true }) 0 @()

New-ArticleProject; Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`n\input{../other}`n"
Test-Case "t2-var-a-outside" $ta 1 @("outside")
New-ArticleProject
$p = Join-Path $workspace "projects\_pkgtest-article\sections\02-preliminaries.tex"
[IO.File]::WriteAllText($p, ([IO.File]::ReadAllText($p, $utf8)).Replace("img/example}", "img/Example}"), $utf8)
Test-Case "t2-var-b-case" $ta 0 @("case")
New-ArticleProject; Write-Text "_pkgtest-article" "my notes.tex" "Notes of the author.`n"
Test-Case "t2-var-c-filename" $ta 0 @("filename", "unused")
New-ArticleProject; Write-Text "_pkgtest-article" "sections\unused-section.tex" "\section{Unused}`nNot included anywhere.`n"
Test-Case "t2-var-d-unused" $ta 0 @("unused")
New-TemplateProject "new-aiaa" "_pkgtest-aiaa"
Test-Case "t2-var-e0-aiaa-unmodified" @{ Project = "_pkgtest-aiaa" } 0 @()
Append-Text "_pkgtest-aiaa" "new-aiaa.cls" "% edited by the author`n"
Test-Case "t2-var-e-aiaa-modified-cls" @{ Project = "_pkgtest-aiaa" } 1 @("template-file")
New-ArticleProject; Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`n\begin{verbatim}`n% this comment-only line must survive`nx = 1`n\end{verbatim}`n% this full-line comment is removed`n"
Test-Case "t2-var-f-verbatim" $ta 0 @() {
    $zip = Join-Path $workspace "outputs\_pkgtest-article\package\_pkgtest-article-$stamp.zip"
    $t = Get-ZipText $zip "sections/04-conclusion.tex"
    if ($t -notmatch '% this comment-only line must survive') { return "verbatim comment line was removed" }
    if ($t -match 'is removed') { return "full-line comment outside verbatim survived" }
}
New-ArticleProject
Write-Text "_pkgtest-article" "submission\reviews-r1.txt" "Reviewer 1: ...`n"
Write-Text "_pkgtest-article" "experiments\run.py" "print('experiment')`n"
Test-Case "t2-var-g-workspace-only" $ta 0 @() {
    $zip = Join-Path $workspace "outputs\_pkgtest-article\package\_pkgtest-article-$stamp.zip"
    $bad = @(Get-ZipNames $zip | Where-Object { $_ -match 'README|submission|experiments|reviews|run\.py' })
    if ($bad.Count -gt 0) { return "workspace-only files in the zip: $($bad -join ', ')" }
}
New-ArticleProject
Append-Text "_pkgtest-article" "preamble\packages.tex" "`n\usepackage{nonexistentpkgxyz}`n"
Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`n\input{no-such-file}`n\input{glyphtounicode}`n\includegraphics{img/nope}`n\input{C:/Users/someone/other}`n"
Test-Case "t2-var-h-missing-static" ($ta + @{ CheckOnly = $true }) 1 @("missing", "outside")
New-ArticleProject; Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`n\thisdoesnotexist`n"
Test-Case "t2-var-i-build-error" $ta 1 @("build")
New-ArticleProject; Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`nSee \cref{thm:nonexistent}.`n"
Test-Case "t2-var-j-undefined-ref" $ta 1 @("undefined")
New-ArticleProject; Append-Text "_pkgtest-article" "sections\04-conclusion.tex" "`n\newenvironment{myverb}{\verbatim}{\endverbatim}`n\begin{myverb}`n% a line that stripping would delete`nx = 1`n\end{myverb}`n"
Test-Case "t2-var-k-text-diff" $ta 1 @("text-diff")

# ---------------------------------------------------------------------------- Test 3: thesis-modular copy (class report)
New-TemplateProject "thesis-modular" "_pkgtest-thesis"
$tt = @{ Project = "_pkgtest-thesis" }
Test-Case "t3-thesis-checkonly" ($tt + @{ CheckOnly = $true }) 0 @()
Test-Case "t3-thesis-default" $tt 0 @("unused")
Test-Case "t3-thesis-exam" ($tt + @{ MainFile = "exam.tex" }) 0 @("unused")
Test-Case "t3-thesis-flat" ($tt + @{ Flat = $true }) 1 @("flat")
# thesis without the exam variant (its chapter names clash with chapters/ in the flat layout)
Remove-TestProject "_pkgtest-thesis-noexam"
Copy-Item -LiteralPath (Join-Path $workspace "projects\_pkgtest-thesis") -Destination (Join-Path $workspace "projects\_pkgtest-thesis-noexam") -Recurse
[IO.Directory]::Delete((Join-Path $workspace "projects\_pkgtest-thesis-noexam\exam"), $true)
[IO.File]::Delete((Join-Path $workspace "projects\_pkgtest-thesis-noexam\exam.tex"))
$p = Join-Path $workspace "projects\_pkgtest-thesis-noexam\main.tex"
$t = [IO.File]::ReadAllText($p, $utf8)
$start = [regex]::Match($t, '\\ifthesisexam\r?\n  % Written work').Index
$elseAt = $t.IndexOf("\else", $start)
$t2 = $t.Substring(0, $start) + $t.Substring($t.IndexOf("`n", $elseAt) + 1)
$fi = $t2.IndexOf("\fi", $start)
$t2 = $t2.Substring(0, $fi) + $t2.Substring($t2.IndexOf("`n", $fi) + 1)
[IO.File]::WriteAllText($p, $t2, $utf8)
Test-Case "t3-thesis-noexam-default" @{ Project = "_pkgtest-thesis-noexam" } 0 @("unused")
Test-Case "t3-thesis-noexam-flat" @{ Project = "_pkgtest-thesis-noexam"; Flat = $true } 0 @("unused")

# ---------------------------------------------------------------------------- Test 4: CV (biblatex + biber, own latexmkrc)
Test-Case "t4-cv-default" @{ Project = "cv"; MainFile = "norbert-michel-cv.tex" } 0 @("layout", "unused")
Test-Case "t4-cv-flat" @{ Project = "cv"; MainFile = "norbert-michel-cv.tex"; Flat = $true } 0 @("layout", "unused")

# ---------------------------------------------------------------------------- Parameters (exit code 2) and edge cases
Test-Case "p-no-project" @{} 2 @()
Test-Case "p-bad-project" @{ Project = "does-not-exist" } 2 @()
Test-Case "p-bad-template" @{ Project = "clanok-1-min-cut-path"; Template = "nope"; CheckOnly = $true } 2 @()
Test-Case "p-bad-mainfile" @{ Project = "clanok-1-min-cut-path"; MainFile = "nope.tex"; CheckOnly = $true } 2 @()
Test-Case "p-bad-maxpages" @{ Project = "clanok-1-min-cut-path"; MaxPages = 0; CheckOnly = $true } 2 @()
Test-Case "p-excluded-main" @{ Project = "clanok-1-min-cut-path"; MainFile = "README.md"; CheckOnly = $true } 2 @()
Test-Case "p-explicit-template" @{ Project = "clanok-1-min-cut-path"; Template = "new-aiaa"; CheckOnly = $true } 0 @("layout")

Move-TestProjects

$header = @(
    "package-project.ps1 test results, $(Get-Date -Format 'yyyy-MM-dd HH:mm'), PowerShell $($PSVersionTable.PSVersion)",
    "Driver: archives/test-evidence/2026-10-08/package-project/run-tests.ps1; per-case output: logs/<case>.txt",
    "cats = finding categories other than [comment]; ok = exit code and categories as expected",
    ""
)
($header + $script:rows + @("", "Cases that differ from the expectation: $($script:bad)")) | Out-File -LiteralPath (Join-Path $evidence "results-table.txt") -Encoding utf8
Write-Host "Cases that differ from the expectation: $($script:bad)"
