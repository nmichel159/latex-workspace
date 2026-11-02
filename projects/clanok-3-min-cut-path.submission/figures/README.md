# Figures of article 3

TikZ sources of the figures new in `projects/clanok-3-min-cut-path/main.tex` (not sent). Each `<name>.tex` is a standalone document that builds `<name>.pdf`;
the PDF lies directly in `projects/clanok-3-min-cut-path/` and is included at its natural size, never with `width=`. The other seven figures come from
`projects/clanok-2-min-cut-path.submission/figures/`, whose conventions these follow, with one addition: larger elements of a preorder are drawn higher.

**AI declaration.** The drawings were written as TikZ code by an AI assistant. The author must declare this at submission (`knowledge/writing/submission.md`, §1.3).

| File | Label | Shows |
|---|---|---|
| `zz-walk` | `fig:zz-walk` | the ZZ instance of `G_b` with its walk; a general valid walk with `D` between `L_P` and `Q \ U_P` |
| `p2-outside` | `fig:p2-outside` | why a common neighbor of two incomparable elements lies in `Q` |
| `one-detour` | `fig:one-detour` | the walks of `lem:pa-one`(a) and (b) |
| `two-detours` | `fig:two-detours` | the walk of `lem:pa-two`, both orders of `p_2`, `p_3` |
| `positions` | `fig:positions` | the ranges and thresholds in the remaining case of `thm:pa-formulas` |

## Rebuild

From PowerShell in the workspace root (never run `pdflatex` without `--miktex-disable-installer`):

```powershell
New-Item -ItemType Directory -Force tmp\clanok-3-figures | Out-Null
Set-Location tmp\clanok-3-figures
foreach ($n in 'zz-walk','p2-outside','one-detour','two-detours','positions') {
  Copy-Item "..\..\projects\clanok-3-min-cut-path.submission\figures\$n.tex" .
  pdflatex -interaction=nonstopmode -halt-on-error --miktex-disable-installer "$n.tex"
  Copy-Item "$n.pdf" ..\..\projects\clanok-3-min-cut-path\ -Force
}
```
