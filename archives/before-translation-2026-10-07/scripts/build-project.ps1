<#
.SYNOPSIS
    Skompiluje LaTeX projekt z projects/<Project> do outputs/<Project>.

.DESCRIPTION
    Jediny podporovany vstupny bod kompilacie. Zdrojove subory ostavaju v projects/,
    PDF a pomocne subory idu do outputs/. Na konci vypise cestu k PDF.
    Strom podpriecinkov projektu sa pred kompilaciou zrkadli do outputs/<Project>,
    aby \include{chapters/...} mal kam zapisat svoj .aux.

.PARAMETER Project
    Nazov priecinka v projects/ (napr. cv, clanok-1-min-cut-path).

.PARAMETER MainFile
    Hlavny .tex subor. Ak chyba, pouzije sa main.tex, inak jediny .tex s \documentclass.

.PARAMETER InstallMissing
    Dovoli MiKTeX-u stiahnut chybajuce balicky pocas kompilacie. Bez prepinaca
    kompilacia pri chybajucom balicku hned skonci chybou (ziadne skryte dialogy).

.EXAMPLE
    .\scripts\build-project.ps1 -Project cv
    .\scripts\build-project.ps1 -Project clanok-1-min-cut-path -MainFile main.tex
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Project,

    [Parameter(Position = 1)]
    [string]$MainFile,

    [switch]$InstallMissing
)

$workspace = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $workspace "projects"
$sourceDirectory = Join-Path $projectsRoot $Project
$outputDirectory = Join-Path $workspace "outputs\$Project"

if (-not (Test-Path -LiteralPath $sourceDirectory -PathType Container)) {
    $available = (Get-ChildItem -LiteralPath $projectsRoot -Directory | ForEach-Object { $_.Name }) -join ", "
    throw "Projekt neexistuje: $sourceDirectory. Dostupne projekty: $available"
}

if (-not $MainFile) {
    if (Test-Path -LiteralPath (Join-Path $sourceDirectory "main.tex")) {
        $MainFile = "main.tex"
    }
    else {
        $candidates = @(Get-ChildItem -LiteralPath $sourceDirectory -Filter *.tex -File |
            Where-Object { Select-String -LiteralPath $_.FullName -Pattern '^\s*\\documentclass' -Quiet })
        if ($candidates.Count -ne 1) {
            $names = ($candidates | ForEach-Object { $_.Name }) -join ", "
            throw "Hlavny subor sa neda urcit automaticky (kandidati: $names). Zadaj -MainFile."
        }
        $MainFile = $candidates[0].Name
    }
}

$mainPath = Join-Path $sourceDirectory $MainFile
if (-not (Test-Path -LiteralPath $mainPath)) {
    throw "Hlavny LaTeX subor neexistuje: $mainPath"
}

$installer = if ($InstallMissing) { "-enable-installer" } else { "-disable-installer" }
# Po neuspesnej kompilacii latexmk bez zmeny zdrojov nic nespusti; -g vynuti novy beh,
# aby sa po doinstalovani balickov kompilacia naozaj zopakovala.
$latexmkArgs = @("-pdf")
if ($InstallMissing) { $latexmkArgs += "-g" }
$latexmkArgs += @(
    "-pdflatex=pdflatex $installer %O %S",
    "-interaction=nonstopmode",
    "-file-line-error",
    "-halt-on-error",
    "-outdir=$outputDirectory",
    $MainFile
)

New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

# \include{chapters/01-intro} zapisuje chapters/01-intro.aux do vystupneho priecinka.
# MiKTeX si chybajuci podpriecinok vytvori sam, TeX Live skonci chybou "I can't write on file".
# Aby kompilacia nezavisela od distribucie, strom podpriecinkov projektu (len priecinky,
# rekurzivne) sa zrkadli do outputs/<Project>. Priecinky s bodkou na zaciatku nazvu
# sa preskakuju aj s celym obsahom.
function Copy-DirectoryTree([string]$Source, [string]$Target) {
    foreach ($directory in @(Get-ChildItem -LiteralPath $Source -Directory | Where-Object { $_.Name -notlike '.*' })) {
        $mirror = Join-Path $Target $directory.Name
        New-Item -ItemType Directory -Force -Path $mirror | Out-Null
        Copy-DirectoryTree -Source $directory.FullName -Target $mirror
    }
}
Copy-DirectoryTree -Source $sourceDirectory -Target $outputDirectory

Push-Location $sourceDirectory
try {
    & latexmk @latexmkArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Kompilacia LaTeX zlyhala. Pozri log: $(Join-Path $outputDirectory ([IO.Path]::ChangeExtension($MainFile, '.log')))"
    }
}
finally {
    Pop-Location
}

$pdfPath = Join-Path $outputDirectory ([IO.Path]::ChangeExtension($MainFile, ".pdf"))
if (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "Kompilacia skoncila bez chyby, ale PDF neexistuje: $pdfPath"
}

$pdf = Get-Item -LiteralPath $pdfPath
$relative = "outputs/$Project/$($pdf.Name)" -replace '\\', '/'
Write-Output ""
Write-Output "PDF:  $($pdf.FullName)"
Write-Output "Link: $relative"
Write-Output "Size: $([math]::Round($pdf.Length / 1KB)) kB, zmenene $($pdf.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
