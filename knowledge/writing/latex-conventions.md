# LaTeX conventions

House rules for every project in this workspace. Craft and reasons: [latex-guide.md](latex-guide.md).
Moving a manuscript to a journal class: [template-porting.md](template-porting.md).
The column "Article 1" marks rules that `projects/clanok-1-min-cut-path` does not follow yet; do not change article 1
for them unless the owner asks.

## 1. Project layout

```
projects/<project>/
  main.tex                 wrapper: \documentclass, fonts, title page, \input of the parts, bibliography commands
  preamble/packages.tex    portable packages (math, graphics, tables, algorithms)
  preamble/environments.tex  theorem environments, problem box, numbering
  preamble/macros.tex      notation macros
  sections/NN-name.tex     article text; the thesis uses chapters/NN-name.tex
  img/                     figures
  references.bib           cited entries only
  <class>.cls, <style>.bst class and bibliography style of the venue: unmodified copies from templates/<venue>/ (§1.1)
  data/                    optional: experiment results (CSV) that the plots in img/ read (latex-guide.md §8)
  experiments/             optional: code, configurations, instance lists, prompts and logs (experiments-reporting.md §7)
  submission/              optional: metadata.txt, cover letter, reviews, rebuttal drafts, AI-use log (submission.md §3.1, §4, §5.5)
  response-to-reviewers.tex, main-marked.tex   optional: revision files (submission.md §5.3, §5.6)
  README.md                Intent, Status, Article contents, Files, Build, Known problems, Content changes to review, Change history
```

The last four lines are workspace-only material: it lives in the folder and never reaches the package (§1.1).

| Rule | Value | Article 1 |
|---|---|---|
| Place | one document = one folder `projects/<project>/` | ok |
| Project name | lowercase, hyphens, ASCII: `clanok-<n>-<topic>`, `praca-<type>-<topic>`, `prezentacia-<topic>`, `cv` | ok |
| Main file | `main.tex`; the CV keeps `norbert-michel-cv.tex` because the PDF name is sent out | ok |
| Template-dependent files | only `main.tex`, `.cls`, `.bst`; `sections/`, `img/` and `references.bib` survive a class swap unchanged, `preamble/` loses the lines the class provides ([template-porting.md](template-porting.md) §3) | ok |
| Part files | `NN-name.tex`: `00-abstract`, `01`-`89` sections in reading order, `90-acknowledgments`, `95`-`99` appendices; each section file starts with `\section{...}` and `\label{sec:...}` | `90-acknowledgment.tex` |
| Abstract and acknowledgments files | text only; the wrapper supplies `\begin{abstract}` and the heading, because both depend on the class | ok |
| Bibliography | `references.bib`; the CV keeps `publications.bib` (own publications only) | ok |
| Images | `img/`, lowercase with hyphens, named by content (`chain-link-types.pdf`, not `fig3.pdf`); vector PDF for drawings and plots, PNG only for raster content | PNG drawings |
| Long document | `chapters/NN-name.tex` via `\include` | - |
| Optional parts | `data/` (experiment results, plots are generated from it into `img/`); `experiments/` (what produced `data/`: [experiments-reporting.md](experiments-reporting.md) §7); `experiments/`, `submission/`, `response-to-reviewers.tex`, `main-marked.tex` are not part of the paper and are left out of the package (§1.1) | - |
| Self-contained | class, `.bst`, images and every input live in the folder and nothing refers outside it (§1.1) | ok |
| Venue files | `.cls`, `.bst` and style files byte-identical to `templates/<venue>/`; never edited in the project (§1.1) | ok: `new-aiaa.cls`, `new-aiaa.bst` have the SHA-256 of `templates/new-aiaa/` (2026-10-08) |
| Encoding | UTF-8 | ok |
| Generated files | only in `outputs/<project>/`; exception: `pdfa.xmpi`, which `pdfx` writes next to the source | ok |
| Packages | load only what the document uses | ok |
| Source lines | one sentence per line in new text (a change touches one line; readable diffs) | not yet |

### 1.1 Invariant: the project follows its template and can be sent

The owner's requirement. It is stated here only; every other file links to this section.

1. **Template.** A project that has a venue template uses the venue's files (`.cls`, `.bst`, style files)
   byte-identical to the pristine copy in `templates/<venue>/`, a wrapper `main.tex` written from the venue's sample
   file, and no override of the venue's layout: no `geometry`, `setspace`, `titlesec`, `fancyhdr`, `\linespread`,
   `\setlength` of page dimensions, negative `\vspace`, `\enlargethispage`, `\pagestyle`. What the class lacks is
   added in the wrapper or in `preamble/`, never in the venue file. Procedure: [template-porting.md](template-porting.md) §1.
2. **Self-contained.** Everything the paper needs is inside `projects/<project>/` at all times. No path leaves the
   folder (`../`, absolute paths, files of another project); file names are ASCII without spaces and are written in
   the source in their exact letter case (the recipient's system is case-sensitive).
3. **One command makes and proves the package.** What goes to a journal, a reviewer, a co-author or Overleaf is the
   zip written by the packager with `Verdict: PASS`, never an archive made by hand and never an edited copy of it.

```powershell
.\scripts\package-project.ps1 -Project <project> [-MainFile <file.tex>] [-Template <name>] [-Flat] [-KeepComments] [-CheckOnly] [-MaxPages <n>]
```

| When | Run |
|---|---|
| after any structural change: new file, new package, class files touched, file renamed or moved | `-CheckOnly` (static checks, no build) |
| after every build | nothing: `build-project.ps1` runs the static checks itself and prints the verdict before the PDF path |
| before anything is sent | the full run; send only on `Verdict: PASS` |

| Switch | Use |
|---|---|
| `-Template <name>` | folder under `templates/`; without it the script takes the folder that ships the project's class |
| `-MaxPages <n>` | page limit from the venue card ([../venues/README.md](../venues/README.md), rule 6) |
| `-Flat` | all files in one directory, paths rewritten: systems that build from one directory (Elsevier Editorial Manager, Springer; [submission.md](submission.md) §3.1); not for arXiv or Overleaf |
| `-KeepComments` | keep comment lines (co-author, Overleaf); default: comment lines are stripped |
| `-MainFile <file.tex>` | a project with several main files |

Left out of the package (the only material in a project folder that is not part of the paper): in the project root
`README.md`, `submission/`, `experiments/`, `response-to-reviewers.tex`, `main-marked.tex`; anywhere zip files,
dot-files, `pdfa.xmpi`, editor backups and build products.
Everything else in the folder counts as part of the paper and is staged, so notes, old versions and drafts go to
`submission/` or to `archives/removed-from-projects/<project>/`, never next to `main.tex`.

| Finding | Meaning | Do |
|---|---|---|
| `[template-file]` (fails) | a venue file differs from `templates/<venue>/` | copy the pristine file again; move the change into the wrapper or `preamble/` |
| `[template-bst]` | `\bibliographystyle` names a style the template does not ship | use the template's style |
| `[layout]` | a layout override under a venue class (list in point 1) | remove it; a deliberate one is justified under "Known problems" in the project README |
| `[outside]`, `[missing]` (fail) | a path leaves the folder; an input does not exist | copy the file into the project; fix the path |
| `[case]` (fails) | letter case of a path differs from the file: builds on Windows, breaks on the recipient's case-sensitive system | correct the path or rename the file |
| `[filename]` | space or non-ASCII character in a file name | rename the file |
| `[flat]` (fails, `-Flat` only) | two files in different folders have the same name | rename one; a thesis with `chapters/` and `exam/` is packaged without `-Flat` |
| `[comment]` | end-of-line comments that remain in the staged copy | read them; delete in the project what a reviewer must not see |
| `[undefined]`, `[pages]` (fail), `[fonts]` | staged build: undefined references or citations, more pages than `-MaxPages`, font problems | fix in the project (§2), run again; over the limit: shorten or move to an appendix ([template-porting.md](template-porting.md) §5) |
| `[text-diff]` (fails) | the staged PDF differs in text from a reference build of the untouched project made in the same run | comment stripping, flattening or an excluded file changed the paper: find which (run with `-KeepComments`, then without `-Flat`) |
| `[unused]` | files the staged build never read | retire them to `archives/removed-from-projects/<project>/`; figure sources and `data/` may stay |
| round trip (fails) | the zip, unpacked elsewhere, does not build to the same text | the folder was not complete: fix the project |

- Stage: `tmp/package-<project>/`. Output: `outputs/<project>/package/<project>-<yyyyMMdd>.zip` (`-flat.zip` with
  `-Flat`), `.bbl` included, the PDF beside it; a second main file beside `main.tex` adds its name
  (`<project>-exam-<yyyyMMdd>.zip`). Exit code 0 = PASS, 1 = FAIL, 2 = bad parameters; last line
  `Verdict: PASS|FAIL`. Parameters and findings in full: the script's comment header.
- A finding is fixed in `projects/<project>/` and the script is run again; the stage and the zip are never edited.
- Scope: every project that is sent. A project on a class of the TeX distribution (`article` from
  `templates/article-modular`, `report` from `templates/thesis-modular`) has no venue files, so points 2 and 3 apply.
  Tested 2026-10-08: thesis template with `main.tex` and with `-MainFile exam.tex`, and the CV (biber): PASS.
- Limits: the round trip builds with this machine's MiKTeX, so a package the recipient lacks is not detected: load
  only packages the venue's class and sample use or a current TeX Live ships. Text is compared, figures and layout
  are not: look at the packaged PDF before sending.
- Submission adds what the script does not do (venue card, statements, anonymization, metadata, frozen copy):
  [submission.md](submission.md) §3.2.

## 2. Build

```powershell
.\scripts\build-project.ps1 -Project <project> [-MainFile <file.tex>] [-InstallMissing]
```

- `latexmk` drives pdfLaTeX and picks BibTeX or biber itself; `-halt-on-error` stops at the first error.
- A missing package fails fast with `File 'x.sty' not found`. `-InstallMissing` downloads from the MiKTeX repository:
  only with the owner's consent.
- Overleaf skips errors and still produces a PDF, so a project that "worked on Overleaf" can fail here: fix the source.
- Output: `outputs/<project>/<main>.pdf`; the script prints the path and the relative link.
- Read PDF text with `pdftotext -enc UTF-8 -layout <pdf> -`; without `-enc UTF-8` the output drops `ľ`, `š`, although
  the PDF contains them.

**Clean build** (required before reporting a document as done):

| Check | Command (workspace root, Git Bash) |
|---|---|
| exit code 0 | the build script throws otherwise |
| no undefined references or citations | `grep -E "undefined|Rerun to get" outputs/<p>/main.log` is empty; no `??` or `[?]` in `pdftotext` output |
| no multiply defined labels | `grep "multiply defined" outputs/<p>/main.log` is empty |
| no visible overfull lines | `grep -A2 "^Overfull" outputs/<p>/main.log`; fix every one wider than 1pt |
| bibliography tool clean | `grep -E "^Warning|error message" outputs/<p>/main.blg` is empty (BibTeX); biber: `grep -E "WARN|ERROR" outputs/<p>/main.blg` |
| fonts embedded | `pdffonts outputs/<p>/main.pdf`: every row `emb yes`, no `Type 3` |

Remaining warnings go to the project README under "Known problems". A clean build is not yet a sendable project:
§1.1.

## 3. Preamble load order

```
\newcommand*{\DoNotLoadEpstopdf}{}   % before \documentclass; see latex-guide.md 3
\documentclass[...]{...}
fonts, page layout                   % main.tex, template-dependent
\input{preamble/packages}
natbib (or the class's citation package)
hyperref                             % late
cleveref                             % after hyperref
\input{preamble/environments}        % theorem definitions after cleveref
\input{preamble/macros}
```

- A class that loads `amsthm`, `hyperref`, `cleveref` or `natbib` itself: delete the duplicate line, keep the order of
  the rest ([template-porting.md](template-porting.md) §3).
- `newtxmath` (loaded by `new-aiaa` and some journal classes) defines `\openbox` and `\Bbbk`. Put
  `\let\openbox\relax` and `\let\Bbbk\relax` before `amsthm`/`amssymb`, otherwise they stop with "Command already defined".
- Article 1: no `cleveref`; `hyperref` and `natbib` come from the class `new-aiaa`; order is class, `packages`,
  `environments`, `macros`.

## 4. Theorem environments

One shared counter within the section: Definition 2.1, Theorem 2.2, Lemma 2.3.
Define them with `thmtools`, not `\newtheorem`:

```latex
\numberwithin{equation}{section}
\declaretheorem[name=Definition,  style=definition, numberwithin=section]{definition}
\declaretheorem[name=Theorem,     style=plain,      sibling=definition]{theorem}
\declaretheorem[name=Lemma,       style=plain,      sibling=definition]{lemma}
\declaretheorem[name=Claim,       style=plain,      sibling=definition]{claim}
\declaretheorem[name=Corollary,   style=plain,      sibling=definition]{corollary}
\declaretheorem[name=Proposition, style=plain,      sibling=definition]{proposition}
\declaretheorem[name=Remark,      style=remark,     sibling=definition]{remark}
\declaretheorem[name=Example,     style=remark,     sibling=definition]{example}
```

Reason (`\cref` names a `\newtheorem` lemma on the shared counter "Definition"): [latex-guide.md](latex-guide.md) §6.

| Rule | Article 1 |
|---|---|
| Environments: `definition`, `theorem`, `lemma`, `claim`, `corollary`, `proposition`, `remark`, `example` | ok |
| Shared counter via `\declaretheorem[sibling=definition]` | `\newtheorem[definition]`; correct while it has no cleveref |
| Proof ending in a list or display: `\qedhere` on its last line, otherwise the QED mark lands alone on a new line or page | ok |
| No blank line before `\end{proof}` | ok |
| Start a proof with a sentence, never with `\paragraph`, an algorithm or a figure: "Proof." would attach to the next paragraph, even inside the algorithm | ok |
| No figure or algorithm inside a `definition` (or any theorem-like environment) | ok |

## 5. Problem box

Every computational problem is stated in the `problem` box, with an **Input / Question** table (decision version) or
**Input / Output** table (optimization version).

```latex
\newtcolorbox{problem}[1][]{enhanced, colback=white, colframe=black, boxrule=0.8pt, arc=2pt,
  left=6pt, right=6pt, top=6pt, bottom=6pt, title=\textbf{Problem: #1}}
```

`llncs` and other classes define a `problem` theorem environment; there release the class's environment or rename
the box ([template-porting.md](template-porting.md) §3).

## 6. Notation macros

Min Cut-Path block (article 1 uses it):

```latex
\newcommand{\cp}{\operatorname{cp}}                 % cp(u,v): value of a minimum cut-path
\newcommand{\CP}{\operatorname{CP}}                 % CP(u,v): set of cut-paths
\newcommand{\diam}{\operatorname{diam}}
\newcommand{\OPT}{\mathrm{OPT}}
\newcommand{\MinCutPath}{\textsc{Min Cut-Path}}
\newcommand{\SSP}{\textsc{Separating Shortest Path}}
\newcommand{\ThreeSAT}{\textsc{3-SAT}}
```

- In a project built from `templates/article-modular`, `macros.tex` already defines `\diam` and `\OPT`: copy only the
  other five lines.
- `\deg` is a standard operator: always with the backslash (`\deg(u, J)`, not `deg(u, J)`).
- Problem names in small caps through a macro: `\textproblem{Name}` (defined in the template's `preamble/macros.tex`)
  or a per-problem macro (`\MinCutPath`, as in article 1); never `\problemname`, which `llncs` defines.
- Meaning of the symbols: [../research/min-cut-path.md](../research/min-cut-path.md), section 2.

## 7. Labels and references

| Object | Prefix | Example |
|---|---|---|
| section, subsection, appendix | `sec:` | `sec:np-completeness` |
| definition | `def:` | `def:cut-path` |
| theorem | `thm:` | `thm:diameter-two` |
| lemma | `lem:` | `lem:odd-intersection` |
| claim | `clm:` | `clm:basic-bounds` |
| corollary, proposition | `cor:`, `prop:` | |
| remark, example | `rem:`, `ex:` | `rem:algorithm` |
| figure, table | `fig:`, `tab:` | `fig:chain-link` |
| algorithm, algorithm line | `alg:`, `line:` | `alg:reduction`, `line:calibrate` |
| equation | `eq:` | |
| problem statement | none (the box has no counter) | referred to by its name macro (`\MinCutPath`, §6) |

- Label: prefix + lowercase words with hyphens; the prefix matches the environment.
- `\label` directly after `\caption` (figure, table, algorithm) or after `\begin{<theorem-like>}`; a float without a
  caption has no label.
- References with cleveref (`capitalise,noabbrev`): `\cref{thm:main}`, `\Cref` at the start of a sentence,
  `\eqref{eq:x}` for equations, `line~\ref{line:x}` for algorithm lines; output of each command and reasons:
  [latex-guide.md](latex-guide.md) §4.
- Without cleveref (article 1, or a class that breaks it): `Theorem~\ref{thm:main}`, `Section~\ref{sec:x}`, capitalized,
  with `~`.
- Article 1: `\ref` style, label list in its README; switching to `\cref` is part of the port to the target journal.

## 8. Math, figures, text

- Inline math `$...$`, display `\[...\]` or `equation`/`align`; never `$$...$$` or `eqnarray`. One inline style per document.
- Figure: `figure` with `\centering`, `\includegraphics[width=<fraction>\linewidth]{img/...}`, `\caption`, `\label`.
- Dashes: ranges and pairs with `--` (`$u$--$v$ path`, `151--158`); parenthetical dash `---` without spaces (American).
- Placement `[tb]`; `[H]` (package `float`) only when the float must stay at that exact spot. Article 1 uses `[H]`.

## 9. Citations

Citation rules live in [../bibliography/README.md](../bibliography/README.md); the section numbers below are its sections.

- In the text (`~\cite{key}`, plain `\cite`, `\citet`/`\citep` only for author-year venues, locators): §8.
- Entries (canonical file first, project copy second, never from memory): §1–§2; keys, fields, status lines: §3–§6.
- Bibliography system per document type: [../bibliography/README.md](../bibliography/README.md) §11; package mechanics: [latex-guide.md](latex-guide.md) §10.

## 10. Templates

| Template | Use | Status |
|---|---|---|
| `templates/article-modular/` | default for every new article; class `article`, venue-neutral | cleveref, mathtools, booktabs, csquotes enabled |
| `templates/thesis-modular/` | dissertation and the written part of the dissertation exam | see its README; UPJŠ rules: [thesis.md](thesis.md) |
| `templates/new-aiaa/` | pristine copy of the class used by article 1 (temporary venue) | never edit |
| `templates/altacv/` | CV (AltaCV 1.7.x) | never edit |

- A new project is a copy of a template in `projects/<project>/`; templates are never edited in place by a project.
- A journal template dropped into `inbox/` is unpacked pristine to `templates/<venue>/`, then ported
  ([template-porting.md](template-porting.md)). The packager compares a project's venue files with that folder
  (§1.1), which is why it is never edited.
