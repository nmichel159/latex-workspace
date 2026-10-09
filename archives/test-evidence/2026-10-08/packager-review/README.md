# Packager: changes after the reviews of 2026-10-08 (tested 2026-10-09)

Three read-only reviews of 2026-10-08 (DAM conformance of article 1, an attack on the no-trace check, a regression
and documentation review) found that `scripts/package-project.ps1` passed packages that carried AI-tool names or
an unrecorded template. The script was changed on 2026-10-08 (evening) and 2026-10-09; this folder tests the change
against the script before it. Rule and findings: [latex-conventions.md](../../../../knowledge/writing/latex-conventions.md)
§1.1, point 4.

| Script | SHA-256 |
|---|---|
| before: `inputs/package-project-before-review.ps1` (= `scripts/package-project.ps1` of 2026-10-08, 18:18) | `DFFF8444DD82900203C7E671609DA26BB1782ED4B6B1C91B73CEE560AB135FF6` |
| after: `scripts/package-project.ps1` as tested on 2026-10-09 | `9ECB3EA54042C80A65959D0824486FEC1542B6D7369C648A769DE25F8E319397` |

Environment: Windows PowerShell 5.1, MiKTeX 25.12 (`cm-super` installed), poppler 24.04.0 (`pdfinfo -custom`,
`pdftotext`).

Repeat from PowerShell in the workspace root (each driver copies the old script into `scripts/` and moves it, the
test projects and their outputs to `tmp/` at the end):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-review\run-review-tests-2.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-review\run-review-tests-2b.ps1
```

## What changed in the script

- Trace scan: text lines also read with `{}`, `\-`, `\/`, soft hyphen and zero-width characters removed and `^^xx`
  decoded; the page text of every PDF figure and of the staged PDF (`pdftotext`), so a name that TeX assembles and
  prints is found; every info key (`pdfinfo -custom`); hex, octal and UTF-16 strings in the PDF objects and object
  streams decoded; PNG: every other ancillary chunk and bytes after `IEND`; JPEG: bytes after the image; other
  binary files in UTF-32 too.
- New patterns: Claude model names with a version (Opus, Sonnet, Haiku), glued and camelCase forms, `\claude...`
  macros, "Claudes"; the name of any Markdown file (workspace trace); placeholders of a statement template
  (`[MODEL AND VERSION]`, `[NAME OF TOOL / SERVICE]`, `[REASON]`, `[TOOL, VERSION]`, `[PROVIDER]`).
- AI declaration: exempt only in the text (not the comments) of an `*ai-declaration*` / `*ai-statement*` file that
  the main file reads, and in the stretch of the staged PDF's page text that it prints; an allowed occurrence no
  longer hides a failing one on the same line.
- `[template-origin]`: a project class that no folder ships fails whether or not `-Template` is given; a project
  class that the `-Template` folder does not ship fails; a class or style file in a folder of kind `house` fails;
  the template folder is compared with its recorded archive file by file (kind `venue`: all files; kind `other`:
  `.cls`, `.bst`, `.sty` ...; generated files by the SHA-256 in the row's note), and only files identical to the
  archive are skipped by the trace scan; "Template: none (class X is a file of the project; ...)".

## Files

| Path | Content |
|---|---|
| `run-review-tests.ps1`, `outputs/` | first driver and its run of 2026-10-08, 23:13: stopped after case B1 (usage limit). Its B1 never built (`\pdfinfo{/Tool (\103laude)}`: `\1` is an undefined control sequence, `[build] FAIL` before and after), and its H cases replaced `\documentclass{article}`, which the wrapper does not contain (it reads `\documentclass[11pt,a4paper]{article}`), so they tested the standard class. Kept as the record of that run |
| `run-review-tests-2.ps1`, `outputs-2026-10-09/`, `results-2026-10-09.txt` | complete run with the final script: S, B1 (overlay `inputs/build-2/`), U, D, H1-H4, E1, T1-T4, X1-X8 |
| `run-review-tests-2b.ps1`, `results-2026-10-09-part2.txt` | B2, H1b-H3b and E2, the cases whose setup was wrong in the first two drivers (outputs in `outputs-2026-10-09/` as well) |
| `inputs/` | the script before the change; overlays laid over a copy of article 1: `static/` (S1), `static-b/` (S2), `build/` (first B1), `build-2/` (B1), `unread-declaration/` (U1), `declaration/` (B1, D1), `declaration-unfinished/` (D2), `handmade/journalx.cls` (H) |
| `outputs-2026-10-09/trace-suite/`, `outputs-2026-10-09/drawio-suite/` | the re-run of [../packager-trace/](../packager-trace/README.md) and [../packager-drawio/](../packager-drawio/README.md) with the final script, made from copies of those folders in `tmp/` (their own `outputs/` and `results.txt` stay as recorded) |

## Results (final script)

| Case | Plant or setup | Before | After |
|---|---|---|---|
| S1 static plants (`-CheckOnly`, copy of article 1) | `Cl{}aude`, `^^43laude`, `Cla­ude` (soft hyphen), `\claudeNote`, `% ClaudeCode`, `% Sonnet 4.5 ... Opus 4`, `% ... latex-conventions.md ... README.md`, a PNG with a private chunk, a PNG with text after `IEND`, a PDF figure whose page says "Figure drawn by Claude", a UTF-32 text file, `pdfsubject={Sonnet 4.5 draft}`, `annote = {Sonnet 4.5 check}` | PASS, 0 hits | FAIL (trace), 16 hits: every plant |
| S2 static plants b | `\iffalse Claude \fi`, `.inc`, a file without extension, UTF-16, a sub-folder file, XMP in PNG, `pdfkeywords={Claude}`, `sections/notes-ai-declaration.tex` that nothing reads | FAIL, 9 hits (2 allowed: the unread declaration-named file) | FAIL, 9 hits (0 allowed) |
| B1 build-time names (full run, `-Flat`, with a correct declaration) | `ChatGPT` from two macros, `\char67 laude`, `\pdfinfo{/Generator <436F70696C6F74>}` (Copilot), `\pdfinfo{/Tool (\string\107emini)}` (Gemini), a bookmark from two macros (Anthropic; cas-sc writes no outlines, so it never reaches the PDF) | PASS, zip written | FAIL (trace) in the staged PDF, no zip: ChatGPT and Claude in the page text, Copilot and Gemini in PDF info; the printed declaration allowed (3 notes) |
| B2 PDF strings (full run, copy of `article-modular`) | bookmark title from two macros (OpenAI), `\pdfcatalog{/PlantNote <416E7468726F706963>}` (Anthropic) | PASS | FAIL (trace): both, "PDF objects, strings decoded" |
| U1 unread declaration name | `sections/notes-ai-declaration.tex`, not `\input` | PASS, 3 allowed | FAIL (trace), 3 hits with the hint that the file is not read |
| D1 declaration inserted as the draft says (full run, `-Flat`) | heading and `\input` before the acknowledgments | PASS, 2 allowed | PASS, 6 allowed (file text and printed text) |
| D2 unfinished declaration (`-CheckOnly`) | `[MODEL AND VERSION]`, `[REASON]`, `% wording suggested by Claude` | PASS | FAIL (trace): both placeholders and the comment; the text stays allowed |
| H1b-H3b hand-made class `journalx.cls` | auto; `-Template article-modular`; `-Template els-cas` | FAIL; PASS; PASS | FAIL in all three ("no folder of templates/ ships it"); auto: "Template: none (class journalx is a file of the project; ...)" |
| H4 article 1 with `-Template elsarticle` | the class `cas-sc.cls` ships in `els-cas`, not in the named folder | PASS | FAIL (template-origin): "templates/elsarticle (-Template) does not ship it (templates/els-cas does)" |
| E2 elsarticle, generated class (full run, `-Flat`) | `elsarticle.cls` is not in the archive; its SHA-256 is in the row's note | PASS | PASS (E1 in run 2 fails `[missing]` on `example-image-a`, mwe not installed, before and after; E2 uses a substitute image) |
| T1, T2 thesis template as shipped (`main.tex`, `-MainFile exam.tex`, `-CheckOnly`) | four `TODO(verify)` comments in `settings.tex` | - | FAIL (trace), 4 hits each |
| T3, T4 the same with the markers resolved (full runs) | | - | PASS, 40 files, 0 hits, both main files |
| X1 sandbox baseline (pristine CAS template, correct row) | | PASS | PASS |
| X2 row of kind `house` for `els-cas` | | PASS | FAIL: the project class from a house folder, and each `.cls`/`.sty`/`.bst` of the folder |
| X3 `cas-common.sty` edited in the folder and the project (a trace line appended) | | PASS, the edited file skipped as "identical to the template" | FAIL: the folder file differs from the archive entry, the project file matches no archive file, and the file is now scanned (3 trace hits) |
| X4 `cas-sc.cls` edited in both (`\def\baselinestretch{0.9}`) | | PASS | FAIL (template-origin) |
| X5 `cas-sc-template.tex` edited in the folder only | | PASS | FAIL (template-origin) |
| X6 `extra-notes.sty` added to the folder | | PASS | FAIL: not in the archive and not recorded |
| X7 house folder with a style, project on `article`, `-Template house-x` | | PASS | FAIL (template-origin) |
| X8 hand-made class filed in a house folder | | PASS | FAIL (template-origin) |

Not covered: text that a PDF draws outside the page area (`pdftotext` drops it) and PDF content streams beyond what
`pdftotext` extracts; a package the recipient's TeX lacks (the round trip builds with this machine's MiKTeX).

## Regression of the earlier suites

Both suites were run from copies of their folders in `tmp/review-fix/suites/` (their drivers write next to
themselves), with the final script as `-New` and their own "before" scripts as `-Old`; outputs and `results.txt`
are in `outputs-2026-10-09/trace-suite/` and `outputs-2026-10-09/drawio-suite/`.

- `packager-drawio`: `results.txt` identical to [../packager-drawio/results.txt](../packager-drawio/results.txt).
- `packager-trace`: same verdicts as [../packager-trace/results.txt](../packager-trace/results.txt) for every case
  (R: CV, article, thesis, thesis `exam.tex`, CAS; T0-T5; B). Differences, all intended:
  - T1, T2: `sections/91-ai-declaration.tex` of the planted project is not read by its `main.tex`, so its two AI
    names now fail instead of being allowed (52 and 68 hits as before; 3 allowed instead of 5);
  - R CV, T5: new allowed notes for the printed text of the staged PDF (CV skill tags "Claude Code" and "OpenAI API"
    by `package-allow.txt`; "Claude Berge" and the printed declaration in T5); in T5 the figure's `/Creator (Claude
    Berge diagram)` copied into the staged PDF is now covered by the same allowed note (one note per term and
    decision per file);
  - T3: the term that only the `.bbl` holds is printed in the reference list, so it is now found in the staged PDF's
    page text, before the staged files are scanned (same FAIL, one file fewer counted);
  - O8 (row of kind `house` for a folder with a class): FAIL instead of nothing; O12: "Template: none (class
    localclass is a file of the project; ...)" instead of "standard class";
  - wording of the AI-name message ("in the text of the AI declaration"), dates in file names, and the `[fonts]`
    notes of the CAS copy, gone since `cm-super` was installed (2026-10-08).

Article 1 with the final script (2026-10-09): `-Template els-cas -CheckOnly`, `-Template els-cas -Flat` and the run
without `-Flat` give `Verdict: PASS`, `Trace scan: 23 files, 0 hits (0 allowed)` for the full runs (project
README, "Build"); the CV gives `Verdict: PASS` with four allowed notes; article 2 (`-CheckOnly`) gives
`Verdict: PASS`, its `templates/sn-jnl/` folder identical to its archive file by file.