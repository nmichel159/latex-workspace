<#
.SYNOPSIS
    Builds a LaTeX project from projects/<Project> into outputs/<Project>.

.DESCRIPTION
    The single supported build entry point. Source files stay in projects/,
    the PDF and auxiliary files go to outputs/. Prints the path to the PDF at the end.
    The tree of project subfolders is mirrored into outputs/<Project> before the build,
    so that \include{chapters/...} has a place to write its .aux.

.PARAMETER Project
    Name of a folder in projects/ (e.g. cv, clanok-1-min-cut-path).

.PARAMETER MainFile
    Main .tex file. If omitted, main.tex is used, otherwise the only .tex with \documentclass.

.PARAMETER InstallMissing
    Lets MiKTeX download missing packages during the build. Without the switch,
    the build fails immediately on a missing package (no hidden dialogs).

.PARAMETER NoPackageCheck
    Skips the package check after the build. By default the static part of package-project.ps1
    (template conformance, self-containedness) runs after a successful build and its verdict is
    printed before the PDF path. The check is informative: it never changes the result of the build.

.EXAMPLE
    .\scripts\build-project.ps1 -Project cv
    .\scripts\build-project.ps1 -Project clanok-1-min-cut-path -MainFile main.tex
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Project,

    [Parameter(Position = 1)]
    [string]$MainFile,

    [switch]$InstallMissing,

    [switch]$NoPackageCheck
)

$workspace = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $workspace "projects"
$sourceDirectory = Join-Path $projectsRoot $Project
$outputDirectory = Join-Path $workspace "outputs\$Project"

if (-not (Test-Path -LiteralPath $sourceDirectory -PathType Container)) {
    $available = (Get-ChildItem -LiteralPath $projectsRoot -Directory | ForEach-Object { $_.Name }) -join ", "
    throw "Project does not exist: $sourceDirectory. Available projects: $available"
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
            throw "Cannot determine the main file automatically (candidates: $names). Pass -MainFile."
        }
        $MainFile = $candidates[0].Name
    }
}

$mainPath = Join-Path $sourceDirectory $MainFile
if (-not (Test-Path -LiteralPath $mainPath)) {
    throw "Main LaTeX file does not exist: $mainPath"
}

$installer = if ($InstallMissing) { "-enable-installer" } else { "-disable-installer" }
# After a failed build latexmk does nothing until the sources change; -g forces a fresh run
# so that the build really repeats once the packages have been installed.
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

# \include{chapters/01-intro} writes chapters/01-intro.aux into the output folder.
# MiKTeX creates a missing subfolder by itself, TeX Live fails with "I can't write on file".
# To make the build independent of the distribution, the tree of project subfolders (folders only,
# recursively) is mirrored into outputs/<Project>. Folders whose name starts with a dot
# are skipped together with their contents.
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
        throw "LaTeX build failed. See the log: $(Join-Path $outputDirectory ([IO.Path]::ChangeExtension($MainFile, '.log')))"
    }
}
finally {
    Pop-Location
}

$pdfPath = Join-Path $outputDirectory ([IO.Path]::ChangeExtension($MainFile, ".pdf"))
if (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "The build finished without error, but the PDF does not exist: $pdfPath"
}

# Package check: the static part of package-project.ps1 (does the project follow its template, is the
# folder self-contained). Informative only. Skipped for the revision files, which are not packaged.
$packager = Join-Path $PSScriptRoot "package-project.ps1"
$notPackaged = @("response-to-reviewers.tex", "main-marked.tex")
if (-not $NoPackageCheck -and (Test-Path -LiteralPath $packager) -and ($notPackaged -notcontains $MainFile)) {
    Write-Output ""
    try {
        $check = @(& $packager -Project $Project -MainFile $MainFile -CheckOnly 2>&1 | ForEach-Object { "$_" })
        $verdict = @($check | Where-Object { $_ -like "Verdict:*" }) | Select-Object -Last 1
        $findings = @($check | Where-Object { $_ -match '^[^ ]+:[0-9]+: [[]' })
        $failed = @($findings | Where-Object { $_ -like "*] FAIL:*" })
        $failed | ForEach-Object { Write-Output $_ }
        if ($verdict) {
            Write-Output "Package check (static): $verdict; $($findings.Count) finding(s). Details: .\scripts\package-project.ps1 -Project $Project -CheckOnly"
        }
        else {
            Write-Output "Package check (static): no verdict. Run .\scripts\package-project.ps1 -Project $Project -CheckOnly"
        }
    }
    catch {
        Write-Output "Package check (static): not run ($($_.Exception.Message))"
    }
    $global:LASTEXITCODE = 0
}

$pdf = Get-Item -LiteralPath $pdfPath
$relative = "outputs/$Project/$($pdf.Name)" -replace '\\', '/'
Write-Output ""
Write-Output "PDF:  $($pdf.FullName)"
Write-Output "Link: $relative"
Write-Output "Size: $([math]::Round($pdf.Length / 1KB)) kB, modified $($pdf.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
