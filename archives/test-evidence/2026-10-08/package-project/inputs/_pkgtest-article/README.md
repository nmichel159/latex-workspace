# Template `article-modular`

Venue-neutral article (class `article`, 11pt, A4, pdfLaTeX, Latin Modern, natbib + `plainnat`). Default for every
new article.

## Layout

```
main.tex                        wrapper, the ONLY template-dependent file: \documentclass, fonts, page layout,
                                title and author, natbib, hyperref, cleveref, abstract/keywords wrapper,
                                \input of the parts, bibliography commands
preamble/packages.tex           portable packages: amsmath, amssymb, amsthm, thmtools, mathtools, graphicx,
                                booktabs, tcolorbox, algorithm, algpseudocode, csquotes
preamble/environments.tex       definition, theorem, lemma, claim, corollary, proposition, remark, example
                                (one shared counter per section, \declaretheorem), problem box, equation numbering,
                                algorithm headers (\Require prints "Input:", \Ensure prints "Output:")
preamble/macros.tex             \N \Z \R \E, \OPT, \diam, \poly, \abs \ceil \floor \set, \textproblem
sections/00-abstract.tex        abstract text only (no \begin{abstract})
sections/01-introduction.tex    each section file starts with \section{...} and \label{sec:...}
sections/02-preliminaries.tex   commented examples (remove): definition, figure, booktabs table
sections/03-results.tex         theorem referenced with \cref; commented example (remove): algorithm with a referenced line
sections/04-conclusion.tex
sections/90-acknowledgments.tex acknowledgment text only; the wrapper supplies the heading
references.bib                  cited entries, copied from knowledge/bibliography/references.bib
img/                            figures (vector PDF preferred)
```

Load order in `main.tex`: `\DoNotLoadEpstopdf` -> class -> fonts and layout -> `preamble/packages` -> natbib ->
hyperref -> cleveref -> `preamble/environments` -> `preamble/macros`. Reasons: `knowledge/writing/latex-guide.md`,
section 3.

## What is template-dependent

`main.tex` and the class files (`.cls`, `.bst`). A journal class gets a new wrapper written from its sample file;
`preamble/` loses the lines the class already provides (amsthm, hyperref, cleveref, natbib, theorem environments);
`sections/`, `img/` and `references.bib` stay unchanged. Procedure and class quirks:
`knowledge/writing/template-porting.md`.

The venue's files enter the project unmodified, its layout is not overridden, and the folder stays self-contained;
`scripts/package-project.ps1` checks this and makes the zip that is sent
(`knowledge/writing/latex-conventions.md`, section 1.1).

## Start a project

```powershell
Copy-Item -Recurse templates\article-modular projects\clanok-<n>-<topic>
.\scripts\build-project.ps1 -Project clanok-<n>-<topic>
```

Then in the project:

1. Replace this file with the project `README.md` (headings: Intent, Status, Article contents, Files, Build,
   Known problems, Content changes to review, Change history).
2. Set `\PaperTitle`, author block and keywords in `main.tex`. Before anything is sent, replace `\date{\today}` by a
   fixed date: a rebuild on another day (journal system, arXiv) changes the text of the PDF.
3. Delete the blocks marked `Example (remove)` and the packages the manuscript does not use.
4. Add project notation to `preamble/macros.tex`; rename and add `sections/NN-name.tex` and their `\input` lines.
5. Add the project to the project tables in `CLAUDE.md` and the root `README.md`.
6. After each structural change (new file, new package): `.\scripts\package-project.ps1 -Project <project> -CheckOnly`.

House rules: `knowledge/writing/latex-conventions.md`.

## Status (2026-10-08)

- Builds with exit code 0, no LaTeX warnings, no undefined references, all fonts Type 1 (2 pages with the examples
  enabled and a dummy citation, `latexmk` with the build script's flags, tested in `archives/test-evidence/2026-10-08/latex-article-test4/`). Without
  any `\cite` (`archives/test-evidence/2026-10-08/latex-article-test4-plain/`), natbib warns "Empty `thebibliography' environment" and BibTeX
  reports "I found no \citation commands"; both disappear with the first citation.
- With the commented algorithm example enabled, `\Require` and `\Ensure` print "Input:" and "Output:" (`pdftotext` of
  the 2-page test PDF, 2026-10-08).
- Preamble compatibility with `llncs`, `IEEEtran`, `elsarticle`, `amsart` and `new-aiaa` was built and tested on
  2026-10-08; results and the changes each class needs: `knowledge/writing/template-porting.md`, section 6.
- Reasons for the template's workarounds, all in `knowledge/writing/latex-guide.md`: `\DoNotLoadEpstopdf` before
  `\documentclass` (section 3), `\declaretheorem[sibling=definition]` instead of `\newtheorem` (section 6),
  `line~\ref{...}` for algorithm lines (section 4), the `T1/lmr/bx/sc` font mapping in `main.tex` (section 2).
