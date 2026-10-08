# usage: build.ps1 <variant> [mainfile]  -- builds tmp/thesis-build/<variant>/src into .../out with the flags of scripts/build-project.ps1
param([string]$Variant, [string]$MainFile = "main.tex")
$base = "C:\Users\norom\Documents\latex\tmp\thesis-build\$Variant"
$src = Join-Path $base "src"; $out = Join-Path $base "out"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Copy-DirectoryTree([string]$Source, [string]$Target) {
    foreach ($d in @(Get-ChildItem -LiteralPath $Source -Directory | Where-Object { $_.Name -notlike '.*' })) {
        $m = Join-Path $Target $d.Name; New-Item -ItemType Directory -Force -Path $m | Out-Null
        Copy-DirectoryTree -Source $d.FullName -Target $m
    }
}
Copy-DirectoryTree -Source $src -Target $out
Push-Location $src
$args2 = @("-pdf", "-pdflatex=pdflatex -disable-installer %O %S", "-interaction=nonstopmode", "-file-line-error", "-halt-on-error", "-outdir=$out", $MainFile)
& latexmk @args2 2>&1 | Out-File -Encoding utf8 (Join-Path $base "build.log")
$code = $LASTEXITCODE
Pop-Location
"exit=$code"
