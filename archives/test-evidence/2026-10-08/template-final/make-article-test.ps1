# Fresh copy of templates/article-modular with the commented examples enabled and a dummy citation (item 7).
$root = 'C:\Users\norom\Documents\latex'
$dst = Join-Path $root 'tmp\fixup\article-modular-test'
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
Copy-Item -Recurse (Join-Path $root 'templates\article-modular') $dst

function Enable-Examples([string]$Path) {
    $lines = [System.IO.File]::ReadAllLines($Path, [System.Text.Encoding]::UTF8)
    $header = -1
    for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -like '% --- Example (remove)*') { $header = $i; break } }
    if ($header -lt 0) { throw "no example header in $Path" }
    $blank = -1
    for ($i = $header + 1; $i -lt $lines.Count; $i++) { if ($lines[$i] -eq '%') { $blank = $i; break } }
    for ($i = $blank; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -eq '%') { $lines[$i] = '' }
        elseif ($lines[$i].StartsWith('% ')) { $lines[$i] = $lines[$i].Substring(2) }
        elseif ($lines[$i].StartsWith('%')) { $lines[$i] = $lines[$i].Substring(1) }
    }
    [System.IO.File]::WriteAllLines($Path, $lines, (New-Object System.Text.UTF8Encoding($false)))
}
Enable-Examples (Join-Path $dst 'sections\02-preliminaries.tex')
Enable-Examples (Join-Path $dst 'sections\03-results.tex')

# dummy citation
Add-Content -Path (Join-Path $dst 'references.bib') -Encoding UTF8 -Value "`n@misc{Dummy2026,`n  author = {Doe, Jane},`n  title  = {A Dummy Entry for the Template Test},`n  year   = {2026},`n  doi    = {10.0000/dummy}`n}"
Add-Content -Path (Join-Path $dst 'sections\01-introduction.tex') -Encoding UTF8 -Value "A dummy citation~\cite{Dummy2026}."

# figure for the example: standalone PDF from the saved test source
Copy-Item (Join-Path $root 'archives\test-evidence\2026-10-08\latex-article-test4\img\example.tex') (Join-Path $dst 'img\example.tex')
Push-Location (Join-Path $dst 'img')
pdflatex -disable-installer -interaction=nonstopmode example.tex | Out-Null
"standalone figure exit: $LASTEXITCODE"
Pop-Location
