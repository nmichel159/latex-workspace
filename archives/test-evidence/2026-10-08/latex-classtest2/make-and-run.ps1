# Disposable harness: builds class-compatibility variants of the article-modular preamble (2026-10-08).
param([string[]]$Only)
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$body = @'
\section{Introduction}\label{sec:intro}
\begin{definition}\label{def:a}A definition.\end{definition}
\begin{lemma}\label{lem:a}A lemma.\end{lemma}
\begin{theorem}\label{thm:a}A theorem.\end{theorem}
\begin{proof}Trivial.\end{proof}
\noindent REFS: \Cref{sec:intro}; \cref{def:a}; \cref{lem:a}; \cref{thm:a}; \cref{lem:a,thm:a}. Cite~\cite{Dummy2001}.
'@

# name -> pre (before documentclass), documentclass line, middle (packages/hyperref/cleveref/environments/macros), front
$houseMid = @'
\input{preamble/packages}
\usepackage[numbers,sort&compress]{natbib}
\usepackage[hidelinks]{hyperref}
\usepackage[capitalise,noabbrev]{cleveref}
\input{preamble/environments}
\input{preamble/macros}
'@
$noNatMid = @'
\input{preamble/packages}
\usepackage[hidelinks]{hyperref}
\usepackage[capitalise,noabbrev]{cleveref}
\input{preamble/environments}
\input{preamble/macros}
'@
$classEnvMid = @'
\usepackage{amsmath,amssymb,mathtools,graphicx,booktabs}
\usepackage[hidelinks]{hyperref}
\usepackage[capitalise,noabbrev]{cleveref}
\input{preamble/macros}
'@
$front = @'
\title{Test}
\author{A. Author}
\begin{document}
\maketitle
\input{body}
\bibliographystyle{plain}
\bibliography{references}
\end{document}
'@

$variants = [ordered]@{
  'llncs-house'     = "\documentclass{llncs}`n$houseMid"
  'llncs-class'     = "\documentclass{llncs}`n$classEnvMid"
  'llncs-same'      = "\documentclass[envcountsame]{llncs}`n$classEnvMid"
  'llncs-natbib'    = "\documentclass{llncs}`n\usepackage[numbers,sort&compress]{natbib}`n$classEnvMid"
  'llncs-thmtools'  = "\documentclass{llncs}`n\usepackage{thmtools}`n$classEnvMid"
  'ieee-house'      = "\documentclass[journal]{IEEEtran}`n$houseMid"
  'els-house'       = "\documentclass[preprint,12pt]{elsarticle}`n$houseMid"
  'els-nonat'       = "\documentclass[preprint,12pt]{elsarticle}`n$noNatMid"
  'amsart-house'    = "\documentclass{amsart}`n$houseMid"
  'aiaa-house'      = "\documentclass[journal]{new-aiaa}`n$houseMid"
  'aiaa-nohyper'    = "\documentclass[journal]{new-aiaa}`n\let\openbox\relax`n\let\Bbbk\relax`n\input{preamble/packages}`n\usepackage[capitalise,noabbrev]{cleveref}`n\input{preamble/environments}`n\input{preamble/macros}"
}

Copy-Item ..\latex-classtest\new-aiaa.cls . -Force
Copy-Item ..\latex-classtest\new-aiaa.bst . -Force
Set-Content -Path body.tex -Value $body -Encoding UTF8

foreach ($name in $variants.Keys) {
  if ($Only -and ($Only -notcontains $name)) { continue }
  $dir = Join-Path $root $name
  New-Item -ItemType Directory -Force $dir | Out-Null
  $pre = "\newcommand*{\DoNotLoadEpstopdf}{}`n"
  Set-Content -Path (Join-Path $dir 'main.tex') -Value ($pre + $variants[$name] + "`n" + $front) -Encoding UTF8
  foreach ($f in 'body.tex','references.bib','llncs.cls','IEEEtran.cls','elsarticle.cls','new-aiaa.cls','new-aiaa.bst') { Copy-Item (Join-Path $root $f) $dir -Force }
  Copy-Item (Join-Path $root 'preamble') $dir -Recurse -Force
  Push-Location $dir
  $out = & latexmk -pdf -f -interaction=nonstopmode -file-line-error "-pdflatex=pdflatex -disable-installer %O %S" -outdir=out main.tex 2>&1
  Pop-Location
  $log = Join-Path $dir 'out\main.log'
  Write-Host "=== $name  (latexmk exit $LASTEXITCODE)"
  if (Test-Path $log) {
    Select-String -Path $log -Pattern '^\./main\.tex:\d+:|^! |^\S+\.(tex|sty|cls):\d+:' | Select-Object -First 6 | ForEach-Object { '  ERR  ' + $_.Line }
    Select-String -Path $log -Pattern 'Warning' | Where-Object { $_.Line -notmatch 'infwarerr' } | Select-Object -First 8 | ForEach-Object { '  WARN ' + $_.Line }
    $pdf = Join-Path $dir 'out\main.pdf'
    if (Test-Path $pdf) { '  TEXT ' + ((& pdftotext -enc UTF-8 $pdf - | Select-String 'REFS' ) -join ' ') }
  } else { '  no log' }
}
