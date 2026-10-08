# Test evidence, 2026-10-08

Sources of the test builds that the workspace documents cite. The originals lived in `tmp/` (disposable, ignored by
git); this folder keeps what is needed to repeat each test: `.tex`, `.bib`, `.ps1`, `.sh`, `.py`, `.xmpdata`, the
classes that MiKTeX does not ship (`llncs.cls`, `IEEEtran.cls`, `elsarticle.cls`, `new-aiaa.cls`, `new-aiaa.bst`)
and small result `.txt` files. Not kept: PDFs, `.aux`, `.log`, `.png` and other build products; the template copies
under `thesis-build/a`, `b`, `c`, `f` (`sync.sh <variant>` recreates them from `templates/thesis-modular/`).
Repeat a test by copying the folder to `tmp/` and building from PowerShell with
`latexmk -pdf "-pdflatex=pdflatex -disable-installer %O %S" -interaction=nonstopmode -file-line-error -halt-on-error -outdir=out <main>.tex`.
Environment: MiKTeX 25.12, LaTeX 2025-11-01, pdfTeX 1.40.28. The paths in the scripts (`C:\Users\norom\Documents\latex\tmp\...`)
point to the former location.

| Folder | What was tested | Cited by |
|---|---|---|
| `latex-tests/` | one small document per claim about packages and counters: cleveref with `\newtheorem` and `\declaretheorem` (shared and separate counters, `sibling=`), `epstopdf` and cleveref options, algorithm line references, `\tag`, `\label`, `\include`, babel, `restatable` | `knowledge/writing/latex-guide.md` |
| `latex-classtest2/` | the `article-modular` preamble under `llncs`, `IEEEtran`, `elsarticle`, `amsart` and `new-aiaa` (harness `make-and-run.ps1`, one folder per variant; the class files sit once in the top folder and `make-and-run.ps1` copies them into each variant); `t-amsthm/`: amsthm with `llncs` | `knowledge/writing/template-porting.md` (sections 6 and 8) |
| `latex-article-test4/` | `templates/article-modular` with the commented examples enabled and a dummy citation: exit code 0, no warnings, fonts Type 1 (`build-run.txt`) | `templates/README.md`, `templates/article-modular/README.md` |
| `latex-article-test4-plain/` | the same template without any `\cite`: the natbib and BibTeX messages that disappear with the first citation (`build-run.txt`) | `templates/article-modular/README.md` |
| `thesis-build/` | `templates/thesis-modular` variants: harness `build.ps1`, `sync.sh`, `check.sh`; patches `patch-c.*` (every switch on, `twoside`) and `patch-f.*` (negative tests for keywords and abstracts); `dummy/` (two-page `assignment.pdf` source); `fonttest/` (font and PDF/A experiments, `pa.xmpdata`) | `templates/thesis-modular/README.md` |
| `template-final/` | final check of both templates after the fixes of 2026-10-08: `article-modular` copy with the examples enabled (algorithm prints "Input:" and "Output:"), `thesis-modular` `main.tex` and `exam.tex` in numeric and author-date citation mode; scripts and the result list `final-tests.txt` | `templates/README.md`, `templates/article-modular/README.md`, `templates/thesis-modular/README.md` |
| `check-text/` | `scripts/check-text.ps1` before and after the spelling, quote and `robust` changes on article 1 (`check-text-before.txt`, `check-text-after.txt`: 77 findings each, only the rule count differs) and two test inputs (`spell.tex`: 31 spelling findings and 1 quote finding; `robust.tex`: 4 findings) | `scripts/check-text.ps1`, `knowledge/writing/phrase-list.tsv` |
| `split-before-hashes.txt`, `split-after-hashes.txt`, `split-before.txt`, `split-after.txt` | article 1 before and after the split into `preamble/` and `sections/`: SHA-256 of the 23 page renders (`pdftoppm`) and the text extracted with `pdftotext`; the two pairs are identical | `projects/clanok-1-min-cut-path/README.md` (change history) |
| `rehearsal-elsarticle/` | dress rehearsal of the port of article 1 to `elsarticle` in a sandbox copy of the workspace (`tmp/rehearsal/ws/`): ported wrapper `main.tex`, adapted `preamble/`, the layout-only diff of `sections/` (`sections.diff`) and the step-by-step notes (`notes.md`); result: 30 pages, packager PASS in both layouts, flat zip builds with pdflatex alone | `knowledge/writing/template-porting.md` |
