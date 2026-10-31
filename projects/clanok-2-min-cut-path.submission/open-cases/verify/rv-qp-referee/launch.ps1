# Referee qp-referee: background runs of run_sf.py (at most 8 processes); PIDs go to runs/pids.txt
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$env:QPR_ALLCOV = "1"
$jobs = @(
  @("zz", "4", "0", "4"),
  @("zz", "4", "1", "4"),
  @("zz", "4", "2", "4"),
  @("zz", "4", "3", "4"),
  @("rsw", "11", "2500", "6", "10"),
  @("rigid", "12", "300", "6", "16"),
  @("deep", "13", "16", "3", "7"),
  @("deep", "14", "4", "4", "8")
)
foreach ($j in $jobs) {
  $tag = ($j -join "-")
  $p = Start-Process -FilePath "python" -ArgumentList (@("run_sf.py") + $j) -NoNewWindow -PassThru `
       -RedirectStandardOutput "runs\$tag.out" -RedirectStandardError "runs\$tag.err"
  "$($p.Id) $tag" | Out-File -Append -Encoding utf8 "runs\pids.txt"
}
Get-Content "runs\pids.txt"
