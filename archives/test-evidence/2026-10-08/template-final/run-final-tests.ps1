# Final tests of item 7: article-modular copy (examples enabled) and thesis-modular copies (numeric, author-date, exam).
$root = 'C:\Users\norom\Documents\latex'
Set-Location $root
$mirrors = @('sections', 'chapters', 'exam', 'appendices', 'backmatter', 'frontmatter')

function Invoke-Build([string]$Dir, [string]$Main) {
    Push-Location $Dir
    New-Item -ItemType Directory -Force out | Out-Null
    foreach ($m in $mirrors) { if (Test-Path $m) { New-Item -ItemType Directory -Force "out\$m" | Out-Null } }
    latexmk -pdf "-pdflatex=pdflatex -disable-installer %O %S" -interaction=nonstopmode -file-line-error -halt-on-error -outdir=out $Main > "build-$Main.txt" 2>&1
    $code = $LASTEXITCODE
    Pop-Location
    $base = [System.IO.Path]::GetFileNameWithoutExtension($Main)
    $log = Join-Path $Dir "out\$base.log"
    $pdf = Join-Path $Dir "out\$base.pdf"
    $pages = if (Test-Path $pdf) { ((pdfinfo $pdf | Select-String '^Pages:').Line -replace '\D', '') } else { 'no pdf' }
    "=== $Dir $Main : exit $code, pages $pages"
    if (Test-Path $log) {
        $w = Select-String -Path $log -Pattern 'Warning|Overfull|Underfull|undefined|^!' | Where-Object { $_.Line -notmatch 'infwarerr' }
        "warnings/errors: " + @($w).Count
        $w | ForEach-Object { '   ' + $_.Line }
        $blg = Join-Path $Dir "out\$base.blg"
        if (Test-Path $blg) { $b = Select-String -Path $blg -Pattern 'Warning|error' ; "bibtex warnings: " + @($b).Count; $b | ForEach-Object { '   ' + $_.Line } }
        $fonts = pdffonts $pdf | Select-Object -Skip 2 | ForEach-Object { ($_ -split '\s+')[ -5..-5 ] } | Sort-Object -Unique
        "font types (column): " + (($fonts | Where-Object { $_ }) -join ',')
    }
}

# article
Invoke-Build 'tmp\fixup\article-modular-test' 'main.tex'
$txt = pdftotext -layout 'tmp\fixup\article-modular-test\out\main.pdf' -
"article: 'Input:' found = " + [bool]($txt | Select-String 'Input:') + "; 'Output:' found = " + [bool]($txt | Select-String 'Output:') + "; 'Require' found = " + [bool]($txt | Select-String 'Require:')
$txt | Select-String -Pattern 'Input:|Output:|Algorithm 1' | ForEach-Object { '   ' + $_.Line.Trim() }
"undefined '??' in text: " + [bool]($txt | Select-String '\?\?')

# thesis: fresh copies
foreach ($mode in 'numeric', 'authordate') {
    $dst = "tmp\fixup\thesis-$mode"
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    Copy-Item -Recurse 'templates\thesis-modular' $dst
    if ($mode -eq 'authordate') { & .\tmp\fixup\patch-authordate.ps1 -Dir $dst | Out-Null }
    Invoke-Build $dst 'main.tex'
    $t = pdftotext -enc UTF-8 "$dst\out\main.pdf" -
    $t | Select-String -Pattern 'is standard' | ForEach-Object { '   citation: ' + $_.Line.Trim() }
    "undefined '??' in text: " + [bool]($t | Select-String '\?\?')
}
Invoke-Build 'tmp\fixup\thesis-numeric' 'exam.tex'
Invoke-Build 'tmp\fixup\thesis-authordate' 'exam.tex'
