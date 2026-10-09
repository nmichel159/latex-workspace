<#
.SYNOPSIS
    Repeats the tests of the packager's trace scan, .bib comment stripping, *.md exclusion, [template-origin] and
    [ai-declaration] (2026-10-08).

.DESCRIPTION
    Run from PowerShell (never Git Bash) in the workspace root:
        powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-trace\run-tests.ps1
    Creates the test projects projects\zz-packager-test-* from templates\ and inputs\, generates the image and PDF
    fixtures (python -I make-trace-fixtures.py, pdflatex -disable-installer), runs the packager under test (-New)
    and, for the regression comparison, the packager before the change (-Old), writes outputs\*.txt and
    results.txt in this folder, and finally moves the test projects and their outputs to tmp\packager-trace\.
    Both packagers must live in scripts\ (they find the workspace from their own folder). After the -next script
    has replaced scripts\package-project.ps1, copy inputs\package-project-before.ps1 to scripts\ under another
    name and pass it as -Old.
#>
param(
    [string]$New = "scripts\package-project-next.ps1",
    [string]$Old = "scripts\package-project.ps1"
)

$ErrorActionPreference = 'Continue'      # native tools write notices to stderr (MiKTeX update reminder)
$here = $PSScriptRoot
$workspace = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$outDir = Join-Path $here "outputs"
$scratch = Join-Path $workspace "tmp\packager-trace"
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = $utf8
New-Item -ItemType Directory -Force -Path $outDir, $scratch | Out-Null
$results = New-Object System.Collections.Generic.List[string]

function Copy-Overlay([string]$From, [string]$To) {
    foreach ($file in @(Get-ChildItem -LiteralPath $From -Recurse -File)) {
        $target = Join-Path $To $file.FullName.Substring($From.Length + 1)
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    }
}

function New-TestProject([string]$Name, [string]$Template) {
    $target = Join-Path $workspace "projects\$Name"
    if (Test-Path -LiteralPath $target) { throw "Test project exists already: $target" }
    Copy-Item -Recurse -LiteralPath (Join-Path $workspace "templates\$Template") -Destination $target
    return $target
}

function Invoke-Packager([string]$Script, [string]$Label, [string[]]$Arguments) {
    $lines = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $workspace $Script) @Arguments 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    [IO.File]::WriteAllLines((Join-Path $outDir "$Label.txt"), [string[]]$lines, $utf8)
    $verdict = @($lines | Where-Object { $_ -like 'Verdict:*' }) | Select-Object -Last 1
    $trace = @($lines | Where-Object { $_ -like 'Trace scan:*' }) | Select-Object -Last 1
    $results.Add(("{0,-34} exit {1}  {2}  {3}" -f $Label, $code, $verdict, $trace))
    return , $lines
}

function Compare-Runs([string]$Label, [string[]]$Before, [string[]]$After) {
    $diff = @(Compare-Object $Before $After | ForEach-Object { "$($_.SideIndicator) $($_.InputObject)" })
    [IO.File]::WriteAllLines((Join-Path $outDir "diff-$Label.txt"), [string[]]$diff, $utf8)
    $results.Add(("{0,-34} {1} differing lines ({0}.txt)" -f "diff-$Label", $diff.Count))
}

# --- Fixtures ------------------------------------------------------------------------------------------------
$fixtures = Join-Path $scratch "fixtures"
if (Test-Path -LiteralPath $fixtures) { Remove-Item -LiteralPath $fixtures -Recurse -Force }
New-Item -ItemType Directory -Force -Path (Join-Path $fixtures "pdf") | Out-Null
& python -I (Join-Path $here "make-trace-fixtures.py") (Join-Path $workspace "templates\els-cas\thumbnails\cas-email.jpeg") (Join-Path $fixtures "img")
foreach ($tex in @(Get-ChildItem -LiteralPath (Join-Path $here "inputs\fixtures") -Filter *.tex)) {
    Copy-Item -LiteralPath $tex.FullName -Destination (Join-Path $fixtures "pdf")
    Push-Location (Join-Path $fixtures "pdf")
    & pdflatex -disable-installer -interaction=nonstopmode $tex.Name | Out-Null
    Pop-Location
}
$img = Join-Path $fixtures "img"
$pdf = Join-Path $fixtures "pdf"

# --- Test projects -------------------------------------------------------------------------------------------
$p = New-TestProject "zz-packager-test-article" "article-modular"
$p = New-TestProject "zz-packager-test-thesis-orig" "thesis-modular"
$p = New-TestProject "zz-packager-test-thesis" "thesis-modular"
$settings = Join-Path $p "settings.tex"
[IO.File]::WriteAllText($settings, [IO.File]::ReadAllText($settings).Replace("TODO(verify)", "to be verified"), $utf8)

$p = Join-Path $workspace "projects\zz-packager-test-cas"
New-Item -ItemType Directory -Force -Path $p | Out-Null
foreach ($f in @("cas-sc.cls", "cas-common.sty", "cas-model2-names.bst", "cas-refs.bib")) { Copy-Item (Join-Path $workspace "templates\els-cas\$f") $p }
Copy-Item -Recurse (Join-Path $workspace "templates\els-cas\thumbnails") $p
Copy-Item (Join-Path $workspace "templates\els-cas\cas-sc-template.tex") (Join-Path $p "main.tex")

$p = New-TestProject "zz-packager-test-trace" "article-modular"
Copy-Overlay (Join-Path $here "inputs\trace") $p
Copy-Item (Join-Path $img "plain.png") (Join-Path $p "img\claude-sketch.png")
foreach ($f in @("plain.png", "text-software.png", "ztext-author.png", "itext-comment.png", "berge-software.png", "com-chatgpt.jpg",
        "xmp-gemini.jpg", "exif-utf16.jpg", "creator-claude.eps", "generator.svg")) { Copy-Item (Join-Path $img $f) (Join-Path $p "img") }
foreach ($f in @("creator-claude.pdf", "objstm-copilot.pdf", "creator-berge.pdf")) { Copy-Item (Join-Path $pdf $f) (Join-Path $p "img") }

$p = New-TestProject "zz-packager-test-stage" "article-modular"
Copy-Overlay (Join-Path $here "inputs\stage") $p
$p = New-TestProject "zz-packager-test-pdfmeta" "article-modular"
Copy-Overlay (Join-Path $here "inputs\pdfmeta") $p
$p = New-TestProject "zz-packager-test-pass" "article-modular"
Copy-Overlay (Join-Path $here "inputs\pass") $p
Copy-Item (Join-Path $pdf "creator-berge.pdf") (Join-Path $p "img\berge-diagram.pdf")
Copy-Item (Join-Path $img "berge-software.png") (Join-Path $p "img\berge-sketch.png")

# --- R: regression, before and after the change ---------------------------------------------------------------
foreach ($case in @(
        @("cv", "cv", @("-Project", "cv")),
        @("article", "article", @("-Project", "zz-packager-test-article")),
        @("thesis", "thesis", @("-Project", "zz-packager-test-thesis")),
        @("thesis-exam-static", "thesis-exam-static", @("-Project", "zz-packager-test-thesis", "-MainFile", "exam.tex", "-CheckOnly")),
        @("cas", "cas", @("-Project", "zz-packager-test-cas")))) {
    $before = Invoke-Packager $Old "r-$($case[0])-before" $case[2]
    $after = Invoke-Packager $New "r-$($case[0])-after" $case[2]
    Compare-Runs $case[1] $before $after
}

# --- T: trace scan ----------------------------------------------------------------------------------------------
[void](Invoke-Packager $New "t0-thesis-template-static" @("-Project", "zz-packager-test-thesis-orig", "-CheckOnly"))
[void](Invoke-Packager $New "t1-planted-static" @("-Project", "zz-packager-test-trace", "-CheckOnly"))
[void](Invoke-Packager $New "t2-planted-static-keepcomments" @("-Project", "zz-packager-test-trace", "-CheckOnly", "-KeepComments"))
[void](Invoke-Packager $New "t3-term-only-in-bbl" @("-Project", "zz-packager-test-stage"))
[void](Invoke-Packager $New "t4-term-only-in-pdf-metadata" @("-Project", "zz-packager-test-pdfmeta"))
[void](Invoke-Packager $New "t5-allowed-only" @("-Project", "zz-packager-test-pass"))
[void](Invoke-Packager $New "t5-allowed-only-flat" @("-Project", "zz-packager-test-pass", "-Flat"))

# --- O: template origin (sandbox copy of the workspace) ---------------------------------------------------------
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here "test-template-origin.ps1") -Workspace $workspace -Script $New -Out (Join-Path $outDir "o-template-origin.txt") | Out-Null
$results.Add("o-template-origin                  see outputs\o-template-origin.txt")

# --- B: the static check as build-project.ps1 reads it --------------------------------------------------------
$check = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $workspace $New) -Project cv -CheckOnly 2>&1 | ForEach-Object { "$_" })
$verdict = @($check | Where-Object { $_ -like "Verdict:*" }) | Select-Object -Last 1
$findings = @($check | Where-Object { $_ -match '^[^ ]+:[0-9]+: [[]' })
$failed = @($findings | Where-Object { $_ -like "*] FAIL:*" })
$results.Add("b-build-project-parse (cv)         Package check (static): $verdict; $($findings.Count) finding(s), $($failed.Count) FAIL line(s)")

[IO.File]::WriteAllLines((Join-Path $here "results.txt"), [string[]]$results, $utf8)
$results

# --- Clean-up: test projects and their outputs to tmp\packager-trace\ ------------------------------------------
foreach ($kind in @("projects", "outputs")) {
    $destination = Join-Path $scratch $kind
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    foreach ($folder in @(Get-ChildItem -LiteralPath (Join-Path $workspace $kind) -Directory -Filter "zz-packager-test-*")) {
        $target = Join-Path $destination $folder.Name
        if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
        Move-Item -LiteralPath $folder.FullName -Destination $target
    }
}
