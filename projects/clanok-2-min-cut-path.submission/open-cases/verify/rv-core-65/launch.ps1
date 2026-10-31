# Launch background runs of the reviewer rv-core-65 and record their PIDs (one line per run: PID, log, arguments).
# usage: powershell -File launch.ps1 TAG "script args" [TAG "script args" ...]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$pairs)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$runs = Join-Path $here "runs"
for ($i = 0; $i -lt $pairs.Count; $i += 2) {
    $tag = $pairs[$i]
    $argline = $pairs[$i + 1]
    $out = Join-Path $runs ($tag + ".txt")
    $err = Join-Path $runs ($tag + ".err")
    $p = Start-Process -FilePath python -ArgumentList $argline -WorkingDirectory $here -NoNewWindow `
        -RedirectStandardOutput $out -RedirectStandardError $err -PassThru
    $line = "{0}`t{1}`tpython {2}`t{3}" -f $p.Id, ($tag + ".txt"), $argline, (Get-Date -Format "yyyy-MM-dd HH:mm")
    Add-Content -Path (Join-Path $runs "pids.tsv") -Value $line
    Write-Output $line
}
