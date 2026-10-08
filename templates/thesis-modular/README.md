# Template `thesis-modular`

UPJŠ dissertation (English, class `report`, pdfLaTeX, Times-like font, natbib) and, from the same sources, the written
work for the dissertation exam. Requirements: `knowledge/writing/thesis.md`, section 7 (cited below as "req. N").
The author-specific values live in `settings.tex`; `main.tex` and `preamble/` need no editing for a normal thesis.

## Layout

```
settings.tex               fields (title page, cover, keywords) and switches (parts, layout); definitions only,
                           read BEFORE \documentclass, so it can steer the class options
main.tex                   wrapper: load order, order of the parts, \include of chapters, bibliography, appendices
exam.tex                   written work for the dissertation exam: defines \ThesisExamVariant, then reads main.tex
references.bib             cited entries (3 samples copied from knowledge/bibliography/references.bib)
preamble/packages.tex      portable packages: amsmath, amssymb, amsthm, thmtools, mathtools, etoolbox, graphicx,
                           booktabs, longtable, tcolorbox, algorithm, algpseudocode
preamble/layout.tex        UPJŠ-dependent: T1 + newtxtext/newtxmath, microtype, babel [slovak,english], csquotes,
                           geometry, setspace, page style (number in the footer), text extraction (glyphtounicode)
preamble/environments.tex  definition, theorem, lemma, claim, corollary, proposition, remark, example (one counter
                           per chapter, \declaretheorem), problem box, equation numbering, algorithm headers
                           (\Require prints "Input:", \Ensure prints "Output:")
preamble/macros.tex        \N \Z \R \E, \OPT, \diam, \poly, \abs \ceil \floor \set, \textproblem, \chapterbasedon
preamble/thesis.tex        unnumbered chapters, front-matter parts, contents and lists, assignment page,
                           symbol list, abstract and keyword checks, index heading
frontmatter/               cover, titlepage, acknowledgments, assignment, ai-statement, declaration, abstract-sk,
                           abstract-en, abbreviations, glossary (text only; main.tex supplies headings)
chapters/01..07            Introduction (unnumbered), Preliminaries, First Result, Second Result, Discussion,
                           Conclusion (unnumbered), Resumé (Slovak, unnumbered)
appendices/01..02          Omitted Proofs (A), Additional Material (B)
backmatter/cv.tex          curriculum vitae (switch)
exam/00..07                chapters of the exam work (thesis.md section 3): Theses of the Project (unnumbered),
                           Introduction, Preliminaries, State of the Art, Results So Far, Methodology and Planned
                           Research, Publication Plan, Timeline
img/                       figures (vector PDF preferred)
```

Load order in `main.tex`: `settings` -> `\DoNotLoadEpstopdf` -> class -> `preamble/packages` -> `preamble/layout` ->
natbib -> hyperref -> cleveref -> `preamble/environments` -> `preamble/macros` -> `preamble/thesis`.
Reasons: `knowledge/writing/latex-guide.md`, section 3. Only `main.tex` and `settings.tex` know the class.

Order of the parts (req. 4): cover, title page, acknowledgments, assignment, AI-use statement, declaration, Slovak
abstract, English abstract, contents, list of figures, list of tables, abbreviations and symbols, glossary,
Introduction, chapters, Conclusion, Resumé, References, appendices, curriculum vitae, index. Every part starts on a new page.

## What to edit: `settings.tex`

| Setting | Default | Effect |
|---|---|---|
| `\ThesisTitle`, `\ThesisSubtitle`, `\ThesisAuthor`, `\ThesisAuthorDegrees` | placeholders | cover, title page, PDF metadata (`\ThesisAuthor` without degrees) |
| `\ThesisUniversity` ... `\ThesisPlace`, `\ThesisRegNo`, `\ThesisConsultant` | UPJŠ values; last two empty | title page and cover; an empty value omits its line |
| `\ThesisKeywords`, `\ThesisKeywordsSK` | placeholders | keywords under the abstracts (3-5 entries, checked) and PDF metadata |
| `\ThesisYear`, `\ThesisType` | 2029 `Dizertačná práca`; exam: 2027 `Písomná práca k dizertačnej skúške` | set by the variant |
| `\thesislabelsenglishtrue` | off (Slovak labels as in the official models) | English labels and type on cover and title page (acceptance TODO(verify), thesis.md section 9) |
| `\thesisacktrue`, `\thesisassignmenttrue`, `\thesisaistatementtrue`, `\thesisabbrtrue`, `\thesisresumetrue`, `\thesisloftrue`, `\thesislottrue` | on | the part is printed; the exam variant switches the assignment and the Resumé off |
| `\thesisdeclarationtrue`, `\thesisglossarytrue`, `\thesisbackmattertrue`, `\thesisindextrue` | off | declaration of originality (not in Dod. 4), glossary, curriculum vitae, index |
| `\ThesisSides` | `oneside` | `twoside` also mirrors the margins (inner 35 mm, outer 20 mm) |
| `\ThesisMarginInner/Outer/Top/Bottom`, `\ThesisSpacing` | 35, 20, 25, 25 mm; `\onehalfspacing` | Smernica recommendations |
| `\ThesisFooter` | page number centered | right: `\fancyfoot[R]{\thepage}`; twoside: `\fancyfoot[RO,LE]{\thepage}` |
| `\thesiscovercountstrue` | off | the cover is page 1 and the title page page 2 |
| `\ThesisAssignmentPages` | `1` | pages of `assignment.pdf` to insert (`1,2`); without the file a placeholder page appears |
| `\ThesisBibStyle` | `unsrtnat` | numeric in citation order; `plainnat` = alphabetical |
| `\ThesisNatbibOptions` | `numbers,sort&compress` | options of natbib; the two settings change together: numeric = `unsrtnat` (or `plainnat`) + `numbers,sort&compress`; author-date (the examples of Príloha 6A) = `plainnat` + `authoryear,round`, `\cite` then prints "(Author, 2022)" (`main.tex` maps it to `\citep`) |

Other edits: delete the blocks marked `Example (remove)` and the packages the thesis does not use; add notation to
`preamble/macros.tex`; rename or add `chapters/NN-name.tex` and the matching `\include` lines in `main.tex`;
`\chapterbasedon{<bibkey>}` below `\chapter{...}` prints the source paper as an unnumbered footnote; give each
abbreviation or symbol a `\label{abbr:...}` where it is defined and list it in `frontmatter/abbreviations.tex`;
`\includeonly{chapters/NN-name}` (line in `main.tex`) builds one chapter during drafting.

## Start a project

```powershell
Copy-Item -Recurse templates\thesis-modular projects\praca-dizertacna-<topic>
.\scripts\build-project.ps1 -Project praca-dizertacna-<topic>                       # dissertation: main.pdf
.\scripts\build-project.ps1 -Project praca-dizertacna-<topic> -MainFile exam.tex    # exam work: exam.pdf
```

Then: replace this file with the project `README.md`; set the fields in `settings.tex`; put the AiS2 assignment next
to `main.tex` as `assignment.pdf` (without signatures); add the project to `CLAUDE.md` and the root `README.md`.

Run the build from PowerShell. From Git Bash, `latexmk` hands BibTeX `/c/...` search paths; BibTeX then silently reads
an unrelated `references.bib` from the MiKTeX tree and reports "I didn't find a database entry" for every key.

Character count (req. 26, target 144 000 to 270 000 including spaces), after a build, from the workspace root:

```bash
pdftotext -enc UTF-8 outputs/<project>/main.pdf - | wc -m
```

The count includes front matter, formulas (as private-use characters) and the bibliography; subtract them for the thesis proper.

Sending the sources (supervisor, co-author, Overleaf): `.\scripts\package-project.ps1 -Project <project>`, the exam work
with `-MainFile exam.tex`; not `-Flat`, because `chapters/` and `exam/` hold files of the same name. Rule and findings:
`knowledge/writing/latex-conventions.md` section 1.1 (tested 2026-10-08: both variants `Verdict: PASS`).

## Requirement coverage (thesis.md section 7)

| Req. | Where | Note |
|---|---|---|
| 1-3 | `preamble/layout.tex`, `settings.tex` | A4, 12 pt, margins, 1.5 spacing, one family; all options. Font TeX Gyre Termes (Times clone), not Times New Roman |
| 4, 5 | `main.tex` | order above; `\chapter*` puts every part on its own page. The AI-use statement page is a recommendation (switch `\thesisaistatementtrue`, default on): the act and the regulation require a truthful statement and the marking of every use, not a page |
| 6-9 | `frontmatter/cover.tex`, `titlepage.tex`, `settings.tex` | text inside `otherlanguage{slovak}` unless English labels; "v~Košiciach" keeps the preposition off the line end |
| 10-12 | `cover.tex`, `titlepage.tex`, `layout.tex`, `main.tex` | cover roman and unprinted, title page = 1 without number, then Arabic to the end; hyperref `plainpages=false`: PDF page labels `i, 1, 2, ...` equal the printed numbers, no duplicate-destination warnings |
| 13 | `layout.tex` | numbering and contents to three levels; STN ISO 2145 not opened |
| 14-16 | `thesis.tex`, `main.tex` | `\chapter` on a new page (`report`, `openany`: no blank pages with `twoside`); `\unnumberedchapter` for Introduction, Conclusion, Resumé, References; `\appendix` gives A, B, ... listed in the contents (package `appendix` not needed) |
| 17 | `\thesisabstractpage` | warns for keywords outside 3-5, abstract outside 100-500 words or in several paragraphs |
| 18 | `symbollist`, `frontmatter/glossary.tex` | `longtable` with `\pageref` to the definition; no nomencl/glossaries |
| 19 | `settings.tex`, `main.tex`, `references.bib` | one technique throughout, chosen by the field: numeric by default (natbib `numbers,sort&compress`, `unsrtnat`), author-date by changing `\ThesisBibStyle` and `\ThesisNatbibOptions` (both modes built, exit 0, 21 pages); the annex Príloha 6A shows author-date, so numeric is a choice, not a copy of the annex; ISO 690 conformity of the `.bst` TODO(verify), `biblatex-iso690` not installed |
| 20, 21 | `layout.tex` | `T1`, `babel [slovak,english]`, `glyphtounicode`; `pdftotext -enc UTF-8` returns the Slovak words and the `ffi` ligature |
| 22 | `main.tex` | title, author, keywords (recommended), language in the PDF. PDF/A is not required and its optional `pdfx` switch is **not provided**: `pdfx` a-2b compiles, but with the 2025-11 kernel it gave "destination with the same identifier" for floats, needs a `.xmpdata` file and cannot be validated (veraPDF missing); neither Smernica nor decree 205/2026 requires it |
| 23 | `frontmatter/assignment.tex`, `thesis.tex` | `\includegraphics[page=...]{assignment.pdf}` on numbered pages; tested with a 2-page file |
| 24, 25 | `chapters/`, `macros.tex` | `\chapterbasedon`; section "Publications and Author's Contribution" in the Introduction |
| 26 | above | |
| 27 | `exam.tex`, `exam/`, `settings.tex` | no assignment page, no Resumé (TODO(verify)), numbered Introduction as in thesis.md section 3, no Conclusion, no appendices |
| 28 | **not provided** | the autoreferát is a separate A5 document in Slovak whose pages 1-2 follow a UPJŠ model that was not found (thesis.md section 8); build it as its own project when the model is known |
| 29 | outside the template | binding and copies are print matters; the PDF equals the print except the unsigned assignment; `twoside` is available |

With `twoside` the cover (not counted) and the title page (page 1) share the parity of page 1; print the cover separately.
`makeindex` runs through `latexmk` when `\thesisindextrue` is set and the text contains `\index` entries.

Open questions for the doctoral office: `knowledge/writing/thesis.md`, section 9 (labels, cover counting, Resumé extent,
declaration page, exam work extent).

## Status (2026-10-08)

Tested in copies of the template (harness and variant patches: `archives/test-evidence/2026-10-08/thesis-build/`), `latexmk` with the flags of `scripts/build-project.ps1`, run from PowerShell:

| Variant | Result |
|---|---|
| default `main.tex` | exit 0, 21 pages, PDF labels `i, 1, ..., 20`, all fonts Type 1 |
| `exam.tex` | exit 0, 19 pages |
| author-date mode (`\ThesisBibStyle` = `plainnat`, `\ThesisNatbibOptions` = `authoryear,round`), `main.tex` and `exam.tex` | exit 0, 21 and 19 pages, the same two placeholder warnings; `\cite` prints "(Cormen et al., 2022)", numeric mode "[1]" |
| `twoside`, every switch on, English labels, cover counted, 2-page `assignment.pdf`, examples enabled | exit 0, 27 pages, footers outside, index and glossary printed |
| negative test: 2 and 6 keywords, 520-word and 2-paragraph abstracts, `\chapterbasedon` | warnings fire; no other warnings |
| through `scripts/build-project.ps1` (`main.tex` and `-MainFile exam.tex`) | exit 0 |

No undefined references or citations, no overfull or underfull boxes, no `??` in the text. Text extraction returns
"Školiteľ", "Prírodovedecká fakulta", "Kľúčové slová" and "efficient". Formulas extract as private-use characters
(`newtxmath` has no Unicode map); ANTIPLAG ignores formulas.

Known warnings (placeholder text, expected): `Package thesis Warning: Abstrakt: about 13 words ...` and the same for
`Abstract`; both disappear with real abstracts. The lists of figures and tables are empty until the first `\caption`
(drop them with `\thesisloffalse` and `\thesislotfalse`). A document without any `\cite` gets natbib's
"Empty `thebibliography'" and BibTeX's "no \citation commands".
