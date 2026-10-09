# Packager: trace scan, template origin, AI declaration (2026-10-08)

Tests of `scripts/package-project-next.ps1`, the successor of `scripts/package-project.ps1` that adds the
`[trace]`, `[template-origin]` and `[ai-declaration]` findings, `.bib` comment stripping and the exclusion of every
`*.md` file ([knowledge/writing/latex-conventions.md](../../../../knowledge/writing/latex-conventions.md) §1.1, point 4).
Environment: Windows PowerShell 5.1, MiKTeX 25.12, poppler `pdfinfo` 24.04.0, Python 3.13 (fixtures only).

Repeat from PowerShell in the workspace root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-trace\run-tests.ps1
```

`run-tests.ps1` creates the test projects `projects/zz-packager-test-*` from `templates/` and `inputs/`, generates the
fixtures, runs every case, writes `outputs/*.txt` and `results.txt`, and moves the test projects and their outputs to
`tmp/packager-trace/`. `-Old` names the packager before the change (default `scripts/package-project.ps1`; once the
successor has replaced it, copy `inputs/package-project-before.ps1` into `scripts/` under another name and pass it).

## Files

| Path | Content |
|---|---|
| `run-tests.ps1` | the driver |
| `make-trace-fixtures.py` | PNG with `tEXt`, `zTXt`, compressed `iTXt`; JPEG with a COM segment, an XMP APP1 segment and a UTF-16 EXIF string (from `templates/els-cas/thumbnails/cas-email.jpeg`); EPS with `%%Creator` and `%%For`; SVG with a generator comment and a base64 image |
| `inputs/fixtures/*.tex` | PDF figures: `/Creator (Claude)`; a term hidden in a compressed object stream and in a Flate XMP stream; `/Creator (Claude Berge diagram)` |
| `inputs/trace/` | files laid over a copy of `templates/article-modular`: every planted trace and the negative controls (`sections/01-introduction.tex`, `references.bib`, `main.tex`), a declaration file, an allowlist with an invalid line, `notes/todo.md` |
| `inputs/stage/`, `inputs/pdfmeta/`, `inputs/pass/` | a term that exists only in the generated `.bbl` (BibTeX `@string` concatenation); only in the staged PDF's metadata (`pdfcreator` built from two macros); a project with allowed hits only (declaration, Claude Berge in text, `.bib`, PNG and PDF figure metadata) |
| `inputs/package-project-before.ps1` | `scripts/package-project.ps1` as it was before the change (regression baseline) |
| `test-template-origin.ps1` | eleven `templates/SOURCES.tsv` variants and a class file that only the project has (O12), in a sandbox copy of the workspace (`tmp/packager-sandbox/`) |
| `outputs/r-*-before.txt`, `outputs/r-*-after.txt`, `outputs/diff-*.txt` | regression: the CV, copies of `article-modular`, `thesis-modular` (also `-MainFile exam.tex`) and the CAS template, before and after |
| `outputs/t*.txt`, `outputs/o-template-origin.txt` | the new checks |
| `results.txt` | exit code, verdict and trace line of every run |

## Results

| Case | Expected | Observed |
|---|---|---|
| R: CV, article, thesis, thesis `exam.tex`, CAS | same verdict and findings as before; new lines only; zip without `*.md`; `.bib` without comment lines; text-diff proof passes | as expected: PASS before and after; differences are the new lines, `LICENSE.md` of the CV moved from the zip (and its `[unused]` note) to the excluded list, `publications.bib` and `references.bib` shorter by their comment lines |
| T0: `thesis-modular` as shipped (`-CheckOnly`) | true positives only | FAIL: four `TODO(verify)` end-of-line comments in `settings.tex` (lines 16, 68, 79, 92), which the package would carry |
| T1: planted traces (`-CheckOnly`) | every plant reported; no hit on the negative controls (`$f:\R\to\R$`, `$F:\Omega\to\Omega$`, "generated with networkx", "knowledge/data", `scripts/run.py`, `outputs/run-1/`, `/tmp/x`, a URL with `a:/b/`, Claudel, `todonotes`, the math title in `.bib`, a base64 run with TODO in the SVG, the stripped `.bib` header and `@comment`, a full-line comment) | as expected: 47 FAIL hits plus the invalid allowlist line (48 FAIL findings), 5 allowed notes (declaration file twice, `Claude Berge` in text, PNG and PDF figure metadata), `notes/todo.md` excluded |
| T2: as T1 with `-KeepComments` | additionally the comment lines | 16 more FAIL hits: the full-line `TODO`, the `.bib` header path and `@comment`, the template's `knowledge/` guidance comments, `.\scripts\build-project.ps1` |
| T3: term only in the `.bbl` | FAIL in the staged files, no zip | as expected |
| T4: term only in the staged PDF metadata | FAIL in the verification, no zip | as expected |
| T5: allowed hits only, with and without `-Flat` | PASS; each allowed hit reported once; the figure's Creator found again in the staged PDF (pdfTeX copies a figure's info dictionary) | as expected |
| O1-O12: `SOURCES.tsv` variants; a project-only class | FAIL for no row, no file, missing column, http URL, missing archive, archive outside the workspace, wrong SHA-256, unknown kind, a class that no template folder ships; note for `other`; nothing for `house` and for a correct `venue` row | as expected |
| B: the static check as `build-project.ps1` parses it | verdict and finding lines recognised | as expected |

Decisions taken while testing (also in the script header): "Claude Code" counts as an AI tool name, not a workspace
trace, because the CV lists it as a skill and a declaration names it; "Generated with" counts only in the commit
trailer form, because "generated with networkx" is prose; the backslash form of a Windows path is not searched in
TeX code; a file identical to a template file is skipped only for templates of kind `venue` or `other`; a class
file that only the project has fails as `[template-origin]`; `*ai-statement*.tex` (the thesis) is exempt like
`*ai-declaration*.tex`. The CV passes because `projects/cv/submission/package-allow.txt` allows its two skill tags
(Claude Code, OpenAI API).

## Note (appended 2026-10-08, after integration)

The tested `scripts/package-project-next.ps1` was integrated as `scripts/package-project.ps1` on 2026-10-08 (the
draft moved to `tmp/packager-integration/`). The integrated script also decodes the draw.io copy of a diagram in PNG
text chunks and SVG files; tests and the rerun of this suite with the extended script (same `results.txt` and hit
lists): [../packager-drawio/](../packager-drawio/README.md). The description above refers to the `-next` script.

## Note (appended 2026-10-09, after the review fixes)

The suite was re-run on 2026-10-09 with the packager as changed after the reviews of 2026-10-08, from a copy of this
folder in `tmp/` so that `outputs/` and `results.txt` here stay as recorded. Same verdicts; the intended differences
(T1/T2: the planted declaration file is not read by `main.tex` and now fails; O8: a house folder with a class now
fails; new allowed notes for printed text) are listed in [../packager-review/](../packager-review/README.md).
