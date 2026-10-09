<#
.SYNOPSIS
    Repeats the test of the packager's decoding of URL-encoded PNG text chunks and draw.io diagram pages
    (2026-10-08).

.DESCRIPTION
    Run from PowerShell (never Git Bash) in the workspace root:
        powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-drawio\run-drawio-test.ps1 -Old scripts\<packager before the fix>.ps1
    Copies projects\<Source> to projects\zz-packager-drawio-test, plants three hidden terms with
    make-drawio-fixtures.ps1 (a URL-encoded PNG mxfile chunk, a compressed draw.io page in a PNG, a compressed page in
    a draw.io SVG), runs -CheckOnly with the packager before the fix (-Old, optional) and after it (-New), writes
    outputs\*.txt and results.txt here and moves the test project to tmp\packager-drawio-test\.
    Both packagers must live in scripts\ (they find the workspace from their own folder).
#>
param(
    [string]$New = "scripts\package-project.ps1",
    [string]$Old = "",
    [string]$Source = "clanok-1-min-cut-path",
    [string]$Template = "els-cas"
)

$ErrorActionPreference = 'Continue'
$here = $PSScriptRoot
$workspace = (Resolve-Path (Join-Path $here "..\..\..\..")).Path
$utf8 = New-Object System.Text.UTF8Encoding $false
$outDir = Join-Path $here "outputs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$name = "zz-packager-drawio-test"
$project = Join-Path $workspace "projects\$name"
if (Test-Path -LiteralPath $project) { throw "Test project exists already: $project" }
Copy-Item -Recurse -LiteralPath (Join-Path $workspace "projects\$Source") -Destination $project
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here "make-drawio-fixtures.ps1") -ProjectDir $project | Out-Null

$results = New-Object System.Collections.Generic.List[string]
$runs = New-Object System.Collections.Generic.List[object]
if ($Old -ne "") { $runs.Add([pscustomobject]@{ Label = "before"; Script = $Old }) }
$runs.Add([pscustomobject]@{ Label = "after"; Script = $New })
foreach ($run in $runs) {
    $lines = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $workspace $run.Script) -Project $name -Template $Template -CheckOnly 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    [IO.File]::WriteAllLines((Join-Path $outDir "drawio-$($run.Label).txt"), [string[]]$lines, $utf8)
    $verdict = @($lines | Where-Object { $_ -like 'Verdict:*' }) | Select-Object -Last 1
    $trace = @($lines | Where-Object { $_ -like 'Trace scan:*' }) | Select-Object -Last 1
    $results.Add(("{0,-14} exit {1}  {2}  {3}" -f "drawio-$($run.Label)", $code, $verdict, $trace))
    foreach ($hit in @($lines | Where-Object { $_ -like '*] FAIL:*' })) { $results.Add("    " + $hit.Substring(0, [Math]::Min(160, $hit.Length))) }
}
[IO.File]::WriteAllLines((Join-Path $here "results.txt"), [string[]]$results, $utf8)

$scratch = Join-Path $workspace "tmp\packager-drawio-test"
if (Test-Path -LiteralPath $scratch) { Remove-Item -LiteralPath $scratch -Recurse -Force }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $scratch) | Out-Null
Move-Item -LiteralPath $project -Destination $scratch
$results
