# Sandbox test of the [template-origin] check. A copy of the packager in tmp\packager-sandbox\scripts\ treats
# tmp\packager-sandbox\ as its workspace, so templates\SOURCES.tsv can be varied without touching the real one.
# Needs projects\zz-packager-test-cas (created by run-tests.ps1). Static checks only (-CheckOnly).
param(
    [string]$Workspace = "C:\Users\norom\Documents\latex",
    [string]$Script = "scripts\package-project-next.ps1",
    [string]$Out
)

$sandbox = Join-Path $Workspace "tmp\packager-sandbox"
if (Test-Path -LiteralPath $sandbox) { Remove-Item -LiteralPath $sandbox -Recurse -Force }
foreach ($d in @("scripts", "templates\els-cas", "archives", "projects")) { New-Item -ItemType Directory -Force -Path (Join-Path $sandbox $d) | Out-Null }
Copy-Item (Join-Path $Workspace $Script) (Join-Path $sandbox "scripts\packager.ps1")
foreach ($f in @("cas-sc.cls", "cas-common.sty", "cas-model2-names.bst")) { Copy-Item (Join-Path $Workspace "templates\els-cas\$f") (Join-Path $sandbox "templates\els-cas") }
Copy-Item -Recurse (Join-Path $Workspace "templates\els-cas\thumbnails") (Join-Path $sandbox "templates\els-cas")
Copy-Item (Join-Path $Workspace "archives\els-cas-templates.zip") (Join-Path $sandbox "archives")
Copy-Item -Recurse (Join-Path $Workspace "projects\zz-packager-test-cas") (Join-Path $sandbox "projects\zz-cas")
[IO.File]::WriteAllText((Join-Path $sandbox "archives\other.zip"), "not the download")

$real = [IO.File]::ReadAllLines((Join-Path $Workspace "templates\SOURCES.tsv"))
$header = $real[0]
$row = @($real | Where-Object { $_ -like "els-cas`t*" })[0]
$cells = $row.Split("`t")
function New-Row([hashtable]$Change) {
    $c = $cells.Clone()
    $names = $header.Split("`t")
    foreach ($k in $Change.Keys) { $c[[Array]::IndexOf($names, $k)] = $Change[$k] }
    return ($c -join "`t")
}
$cases = [ordered]@{
    "O1 venue row, archive and hash correct" = @($header, $row)
    "O2 no row for the folder"               = @($header, (New-Row @{ folder = "some-other-folder" }))
    "O3 official_url is not https"           = @($header, (New-Row @{ official_url = "http://example.org/els-cas-templates.zip" }))
    "O4 archive file missing"                = @($header, (New-Row @{ archive = "archives/missing.zip" }))
    "O5 archive with another SHA-256"        = @($header, (New-Row @{ archive = "archives/other.zip" }))
    "O6 archive outside the workspace"       = @($header, (New-Row @{ archive = "../els-cas-templates.zip" }))
    "O7 kind other"                          = @($header, (New-Row @{ kind = "other"; note = "test row of kind other" }))
    "O8 kind house"                          = @($header, (New-Row @{ kind = "house" }))
    "O9 unknown kind"                        = @($header, (New-Row @{ kind = "vendor" }))
    "O10 header lacks sha256"                = @(($header -replace "`tsha256", "`thash"), $row)
    "O11 SOURCES.tsv missing"                = $null
}
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = $utf8
$report = New-Object System.Collections.Generic.List[string]
foreach ($name in $cases.Keys) {
    $tsv = Join-Path $sandbox "templates\SOURCES.tsv"
    if ($null -eq $cases[$name]) { if (Test-Path $tsv) { Remove-Item $tsv } }
    else { [IO.File]::WriteAllText($tsv, (($cases[$name] -join "`n") + "`n"), $utf8) }
    $output = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $sandbox "scripts\packager.ps1") -Project zz-cas -CheckOnly 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    $report.Add("== $name (exit $code)")
    foreach ($line in $output) { if ($line -match '\[template-origin\]|^Template origin:|^Verdict:') { $report.Add($line) } }
}
# O12: a class that only the project has (no folder of templates/ ships it)
$local = Join-Path $sandbox "projects\zz-local"
New-Item -ItemType Directory -Force -Path $local | Out-Null
[IO.File]::WriteAllText((Join-Path $local "localclass.cls"), "\NeedsTeXFormat{LaTeX2e}`n\ProvidesClass{localclass}`n\LoadClass{article}`n", $utf8)
[IO.File]::WriteAllText((Join-Path $local "main.tex"), "\documentclass{localclass}`n\begin{document}`nx`n\end{document}`n", $utf8)
[IO.File]::WriteAllText((Join-Path $sandbox "templates\SOURCES.tsv"), (($header, $row) -join "`n") + "`n", $utf8)
$output = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $sandbox "scripts\packager.ps1") -Project zz-local -CheckOnly 2>&1 | ForEach-Object { "$_" })
$report.Add("== O12 class file only in the project (exit $LASTEXITCODE)")
foreach ($line in $output) { if ($line -match '\[template-origin\]|^Template|^Verdict:') { $report.Add($line) } }

[IO.File]::WriteAllLines($Out, [string[]]$report, $utf8)
Remove-Item -LiteralPath $sandbox -Recurse -Force
$report
