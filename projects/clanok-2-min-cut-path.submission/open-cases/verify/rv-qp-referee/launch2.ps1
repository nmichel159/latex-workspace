# Referee qp-referee: adversarial runs (QPR_ADV) of run_sf.py; PIDs appended to runs/pids.txt
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$env:QPR_ADV = "1"
$env:QPR_ALLCOV = ""
$jobs = @(
  @("deep", "41", "60", "3", "7"),
  @("deep", "42", "16", "4", "8"),
  @("deep", "43", "6", "5", "9"),
  @("rigid", "44", "2000", "6", "18")
)
foreach ($j in $jobs) {
  $tag = ($j -join "-") + "-adv"
  $p = Start-Process -FilePath "python" -ArgumentList (@("run_sf.py") + $j) -NoNewWindow -PassThru `
       -RedirectStandardOutput "runs\$tag.out" -RedirectStandardError "runs\$tag.err"
  "$($p.Id) $tag" | Out-File -Append -Encoding utf8 "runs\pids.txt"
}
Get-Content "runs\pids.txt"
