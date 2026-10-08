# Patches a copy of settings.tex to the author-date citation mode (test harness, item 3).
param([string]$Dir)
$f = Join-Path $Dir 'settings.tex'
$s = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$s = $s.Replace('{\ThesisBibStyle}{unsrtnat}', '{\ThesisBibStyle}{plainnat}')
$s = $s.Replace('{\ThesisNatbibOptions}{numbers,sort&compress}', '{\ThesisNatbibOptions}{authoryear,round}')
[System.IO.File]::WriteAllText($f, $s, (New-Object System.Text.UTF8Encoding($false)))
Select-String -Path $f -Pattern 'ThesisBibStyle\}\{|ThesisNatbibOptions\}\{' | ForEach-Object { $_.Line }
