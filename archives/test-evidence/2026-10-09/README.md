# Test evidence, 2026-10-09

Results of the test builds behind the Springer Nature template (`templates/sn-jnl/`) and article 2. The builds ran
in `tmp/` (disposable); this folder keeps the inputs that are not elsewhere in the workspace and the result lists.
Environment: MiKTeX 25.12, LaTeX 2025-11-01, pdfTeX 1.40.28.

| Folder | What was tested | Cited by |
|---|---|---|
| `sn-jnl-sample/` | the pristine sample `sn-article.tex` of `templates/sn-jnl/` with `bst/sn-mathphys-num.bst` copied next to it (built 2026-10-08): exit code 0, 12 pages A4, 32 Type 1 fonts, the sample's own warnings (including one duplicate destination per float), the MiKTeX packages installed for it, and the first text difference from the publisher's `sn-article.pdf` (author-year there, numbered here); `results.txt` | `templates/README.md` (Status), `knowledge/writing/template-porting.md` (§6.3) |
| `sn-jnl-float/` | copies of `projects/clanok-2-min-cut-path` with one figure (the template's `fig.eps`), one table and one algorithm (`04-conclusion-floats.tex`): without `\RequirePackage{float}` before `\documentclass` pdfTeX writes `figure.1` and `table.1` twice, with it none; `\Cref` prints "Figure 1, Table 1, and Algorithm 1"; the EPS figure is converted by `epstopdf`; `main-a-vs-b.diff`, `results.txt` | `projects/clanok-2-min-cut-path/README.md`, `knowledge/writing/template-porting.md` (§6.3) |

Repeat: copy `templates/sn-jnl/` (or the project) to `tmp/`, apply the inputs kept here and build from PowerShell with
`latexmk -pdf "-pdflatex=pdflatex -disable-installer %O %S" -interaction=nonstopmode -file-line-error -halt-on-error <main>.tex`.
