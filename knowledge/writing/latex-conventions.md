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
  submission/              optional: metadata.txt, cover letter, reviews, rebuttal drafts, AI-use log, ai-declaration.tex draft, package-allow.txt (submission.md §1.3, §3.1, §4, §5.5; §1.1 here)
  response-to-reviewers.tex, main-marked.tex   optional: revision files (submission.md §5.3, §5.6)
  README.md                Intent, Status, Article contents, Files, Build, Known problems, Content changes to review, Change history
```

The last four lines are workspace-only material: it lives in the folder and never reaches the package (§1.1).

| Rule | Value | Article 1 |
|---|---|---|
| Place | one document = one folder `projects/<project>/` | ok |
| Project name | lowercase, hyphens, ASCII: `clanok-<n>-<topic>`, `praca-<type>-<topic>`, `prezentacia-<topic>`, `cv` | ok |
| Main file | `main.tex`; the CV keeps `norbert-michel-cv.tex` because the PDF name is sent out | ok |
| Template-dependent files | only `main.tex`, `.cls`, `.bst`; `sections/`, `img/` and `references.bib` survive a class swap unchanged, `preamble/` loses only lines that clash with the class and keeps those the class loads too; a class that reads standard markup differently is adapted in the wrapper ([template-porting.md](template-porting.md) §1, §3) | ok since 2026-10-09 (cas-sc key alias `H` in `main.tex`; `preamble/` and `sections/` build under `article` with `\usepackage{enumerate}`) |
| Part files | `NN-name.tex`: `00-abstract`, `01`-`89` sections in reading order, `90-acknowledgments`, `91-ai-declaration` (only when AI tools were used; text only, the wrapper gives the venue's heading: [submission.md](submission.md) §1.3), `92-declarations` (only for venues that want declarations in the manuscript; text only, the wrapper gives the venue's heading, e.g., Springer Nature's `\section*{Declarations}`: [template-porting.md](template-porting.md) §2), `95`-`99` appendices; each section file starts with `\section{...}` and `\label{sec:...}` | ok |
| Abstract and acknowledgments files | text only; the wrapper supplies `\begin{abstract}` (sn-jnl: `\abstract{...}`) and the heading, because both depend on the class | ok |
| Bibliography | `references.bib`; the CV keeps `publications.bib` (own publications only) | ok |
| Images | `img/`, lowercase with hyphens, named by content (`chain-link-types.pdf`, not `fig3.pdf`); vector PDF for drawings and plots, PNG only for raster content | PNG drawings |
| Long document | `chapters/NN-name.tex` via `\include` | - |
| Optional parts | `data/` (experiment results, plots are generated from it into `img/`); `experiments/` (what produced `data/`: [experiments-reporting.md](experiments-reporting.md) §7); `experiments/`, `submission/`, `response-to-reviewers.tex`, `main-marked.tex` are not part of the paper and are left out of the package (§1.1) | - |
| Self-contained | class, `.bst`, images and every input live in the folder and nothing refers outside it (§1.1) | ok |
| Venue files | `.cls`, `.bst` and style files byte-identical to `templates/<venue>/`; never edited in the project (§1.1); a `.bst` that the template keeps in a sub-folder (sn-jnl: `bst/`) is copied next to `main.tex` | ok: `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` are identical to `templates/els-cas/` (packager, 2026-10-08) |
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
4. **No traces.** Nothing that is sent names this workspace, its tools or an AI tool, except the AI declaration the
   venue requires. The packager scans every file it would package (as staged: stripped comment lines are skipped)
   and every path; before the zip is written, the staged files with the `.bbl`; the zip entry names. Text lines are
   also read with TeX's invisible separators removed (`{}`, `\-`, `\/`, soft hyphen, zero-width characters) and
   `^^xx` decoded, so `Cl{}aude` counts. Images: PNG text chunks, every other ancillary chunk and any bytes after
   the image data; JPEG EXIF/XMP/comment and bytes after the image; EPS header; SVG; PNG text and SVG also
   URL-decoded with the draw.io copy of the diagram inflated. PDF figures and the staged PDF: every info key
   (`pdfinfo -custom`), XMP, the page text (`pdftotext`, so a name that TeX assembles from macros or `\char` and
   prints is found), and the objects and object streams with hex, octal and UTF-16 strings decoded. Other binary
   files: printable runs in ASCII, UTF-16 and UTF-32. Not read: PDF content streams beyond what `pdftotext`
   extracts (text drawn outside the page). Two pattern groups, case-insensitive, whole words:
   - workspace traces, never allowed: `TODO`, `FIXME`, the placeholders of a statement template
     (`[MODEL AND VERSION]`, `[NAME OF TOOL / SERVICE]`, `[REASON]`, `[TOOL, VERSION]`, `[PROVIDER]`), `claude.ai`,
     `claude.com`, `anthropic.com`, `Co-Authored-By`, the commit trailer "Generated with [", `noreply@`,
     `CLAUDE.md`, `.claude/`, the name of any Markdown file (`README.md`, `latex-conventions.md`: never packaged, so
     naming one is workspace information), the Windows user name and profile path, absolute Windows paths (in TeX
     files only in comments and verbatim, because `f:\R\to\R` is math), paths into this workspace (`knowledge/`,
     `archives/`, `outputs/`, `inbox/`, `scripts/`, `tmp/`, `projects/` followed by a name that exists there);
   - AI tool names: Claude, "Claude Code", Anthropic, ChatGPT, OpenAI, Copilot, Gemini, GPT-*n*, the model names
     Opus, Sonnet and Haiku with a version number, glued and camelCase forms (`ClaudeCode`, `\claudeNote`), "Claudes",
     "AI-generated", "generated by AI"; allowed only in the text (not the comments) of a `.tex` file named
     `*ai-declaration*.tex` or `*ai-statement*.tex` that the main file reads (articles:
     `sections/91-ai-declaration.tex`, [submission.md](submission.md) §1.3; thesis: `frontmatter/ai-statement.tex`),
     in the stretch of the staged PDF's page text that this declaration prints, or where a regular expression in
     `projects/<p>/submission/package-allow.txt` matches the same line (one regex per line, ` # reason` after it;
     for research on LLMs, or names such as Claude Berge).

   Allowed hits stay in the report as notes. The template folder must also be a recorded download: a row in
   `templates/SOURCES.tsv`, and for a venue template an https URL and the archive in `archives/` with the recorded
   SHA-256, and the folder still byte-identical to that archive, file by file
   ([../../templates/README.md](../../templates/README.md), Provenance). Files identical to the archive are the
   publisher's and are not scanned; a file that is only identical to the folder is.

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
| `-KeepComments` | keep comment lines (co-author, Overleaf); default: comment lines are stripped; kept comments are scanned for traces like the text |
| `-MainFile <file.tex>` | a project with several main files |

Left out of the package (the only material in a project folder that is not part of the paper): in the project root
`submission/`, `experiments/`, `response-to-reviewers.tex`, `main-marked.tex`; anywhere `*.md` files (`README.md`,
notes), zip files, dot-files, `pdfa.xmpi`, editor backups and build products.
Everything else in the folder counts as part of the paper and is staged, so notes, old versions and drafts go to
`submission/` or to `archives/removed-from-projects/<project>/`, never next to `main.tex`.
Staging removes comment lines: full-line `%` comments of `.tex` files, and in `.bib` files the `%` lines outside
entries and `@comment{...}` blocks (the header naming the canonical `.bib`, status lines); `-KeepComments` keeps both.

| Finding | Meaning | Do |
|---|---|---|
| `[template-file]` (fails) | a venue file differs from `templates/<venue>/` | copy the pristine file again; move the change into the wrapper or `preamble/` |
| `[template-origin]` (fails; note for kind `other`) | the template folder that ships the class has no row in `templates/SOURCES.tsv`, or its `venue` row lacks an https URL, the archive or the matching SHA-256; a file of the folder differs from the archive or is not in it (kind `venue`: every file; kind `other`: `.cls`, `.bst`, `.sty` ...; a generated file counts when the row's note records its SHA-256); the project has a class file that no folder of `templates/` ships, or that the `-Template` folder does not ship; a folder of kind `house` holds a class or style file; the report prints `Template origin: <folder> (<kind>, <version>, <url>)`, and for a class that only the project has `Template: none (class X is a file of the project; ...)` | download the template from the publisher's page with the owner's consent and file it with its row (skill `process-inbox`); restore an edited folder from its archive; never hand-make a venue template |
| `[template-bst]` | `\bibliographystyle` names a style the template does not ship | use the template's style |
| `[layout]` | a layout override under a venue class (list in point 1) | remove it; a deliberate one is justified under "Known problems" in the project README |
| `[outside]`, `[missing]` (fail) | a path leaves the folder; an input does not exist | copy the file into the project; fix the path |
| `[case]` (fails) | letter case of a path differs from the file: builds on Windows, breaks on the recipient's case-sensitive system | correct the path or rename the file |
| `[filename]` | space or non-ASCII character in a file name | rename the file |
| `[flat]` (fails, `-Flat` only) | two files in different folders have the same name | rename one; a thesis with `chapters/` and `exam/` is packaged without `-Flat` |
| `[trace]` (fails; note when allowed) | a workspace trace or an AI tool name in a packaged file, a path, image or PDF metadata, the page text of a PDF figure or of the staged PDF, the `.bbl` or a zip entry name (point 4); an invalid regex in `package-allow.txt`; a file that cannot be scanned (nothing proves it clean) | delete it in the project (a figure: export it again without metadata); a tool name belongs in the text of `sections/91-ai-declaration.tex`; an AI name that is research content goes into `submission/package-allow.txt` with a reason |
| `[comment]` | end-of-line comments that remain in the staged copy | read them; delete in the project what a reviewer must not see |
| `[ai-declaration]` (never fails) | no heading "Declaration of generative AI ...", "Use of AI tools" or "... AI-assisted technologies ..." in the package; says whether `submission/*ai-declaration*.tex` holds a draft; repeated in the line `AI declaration:` before the verdict on every run | if AI tools were used beyond grammar checking, insert the declaration ([submission.md](submission.md) §1.3) |
| `[encoding]` | a `.tex` or `.bib` file that is not valid UTF-8: copied unchanged (its comments stay; a `.tex` is not parsed and its paths are not rewritten) | save it as UTF-8 |
| `[build]` (fails) | the staged package does not build (latexmk, installer disabled); the first error lines follow | fix the project; a package missing from MiKTeX needs the owner's consent to install (CLAUDE.md rule 6) |
| `[undefined]`, `[pages]` (fail), `[fonts]` | staged build: undefined references or citations, more pages than `-MaxPages`, font problems | fix in the project (§2), run again; over the limit: shorten or move to an appendix ([template-porting.md](template-porting.md) §5) |
| `[text-diff]` (fails) | the staged PDF differs in text from a reference build of the untouched project made in the same run | comment stripping, flattening or an excluded file changed the paper: find which (run with `-KeepComments`, then without `-Flat`) |
| `[unused]` | files the staged build never read | retire them to `archives/removed-from-projects/<project>/`; figure sources and `data/` may stay |
| `[roundtrip]` (fails) | the zip, unpacked elsewhere, does not build to the same text | the folder was not complete: fix the project |
| `[internal]` (fails) | an unexpected error stopped the script (message and script line in the finding) | read the message, fix the cause and run again; never send a package from such a run |

- Stage: `tmp/package-<project>/`. Output: `outputs/<project>/package/<project>-<yyyyMMdd>.zip` (`-flat.zip` with
  `-Flat`), `.bbl` included, the PDF beside it; a second main file beside `main.tex` adds its name
  (`<project>-exam-<yyyyMMdd>.zip`). Exit code 0 = PASS, 1 = FAIL, 2 = bad parameters; last line
  `Verdict: PASS|FAIL`; just before it `Trace scan: <n> files, <m> hits (<k> allowed)` and `AI declaration: ...`.
  Parameters and findings in full: the script's comment header.
- A finding is fixed in `projects/<project>/` and the script is run again; the stage and the zip are never edited.
- Scope: every project that is sent. A project on a class of the TeX distribution (`article` from
  `templates/article-modular`, `report` from `templates/thesis-modular`) has no venue files, so points 2 to 4 apply.
  The CV (biber) passes (2026-10-08). The thesis template as shipped fails, with `main.tex` and with
  `-MainFile exam.tex`: four `TODO(verify)` end-of-line comments in `settings.tex` would reach the package; with them
  resolved, the full run passes for both main files (2026-10-09, cases T1-T4 of
  [packager-review/](../../archives/test-evidence/2026-10-08/packager-review/README.md)).
  Trace scan, `.bib` stripping, `*.md` exclusion, `[template-origin]` and `[ai-declaration]` tested 2026-10-08 on the
  CV, copies of both house templates and of the CAS template, planted traces of every kind, eleven
  `SOURCES.tsv` variants and a project-only class: [archives/test-evidence/2026-10-08/packager-trace/](../../archives/test-evidence/2026-10-08/packager-trace/README.md).
  The changes after the review of 2026-10-08 (build-time names in the page text, PDF strings, model names, Markdown
  file names, declaration exemption, template folder against its archive, house folders, `-Template` naming another
  folder) were tested on 2026-10-09 against the script before the change:
  [archives/test-evidence/2026-10-08/packager-review/](../../archives/test-evidence/2026-10-08/packager-review/README.md).
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
- Article 1 (class `cas-sc`): no `cleveref`; the class loads `hyperref`, the wrapper loads `natbib`; order is
  `\RequirePackage{float}`, class, `natbib`, `packages`, `environments`, `macros`.

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
- Article 1: `\ref` style, label list in its README; the port to `cas-sc` (2026-10-08) kept it, because the owner did
  not ask for `\cref`.

## 8. Math, figures, text

- Inline math `$...$`, display `\[...\]` or `equation`/`align`; never `$$...$$` or `eqnarray`. One inline style per document.
- Figure: `figure` with `\centering`, `\includegraphics[width=<fraction>\linewidth]{img/...}`, `\caption`, `\label`.
- Dashes: ranges and pairs with `--` (`$u$--$v$ path`, `151--158`); parenthetical dash `---` without spaces (American).
- Placement `[tb]`; `[H]` (package `float`) only when the float must stay at that exact spot. Article 1 uses `[H]` for its figures and
  its algorithm; `cas-sc` drops a plain `[H]`, so the wrapper declares `H` as a short form of the class's key `pos=H`
  (since 2026-10-09; [template-porting.md](template-porting.md) §6.3).

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
| `templates/els-cas/` | Elsevier CAS bundle 2.4, publisher download: class `cas-sc` of article 1 (Discrete Applied Mathematics) | never edit |
| `templates/elsarticle/` | Elsevier's general class `elsarticle` 3.4, publisher download | never edit |
| `templates/sn-jnl/` | Springer Nature journal article template 3.1, publisher download: class `sn-jnl` of article 2 (Algorithmica); `.bst` files in `bst/` | never edit |
| `templates/new-aiaa/` | former class of article 1 (until 2026-10-08) | never edit |
| `templates/altacv/` | CV (AltaCV 1.7.x) | never edit |

- A new project is a copy of a template in `projects/<project>/`; templates are never edited in place by a project.
- A journal template dropped into `inbox/` is unpacked pristine to `templates/<venue>/`, then ported
  ([template-porting.md](template-porting.md)). The packager compares a project's venue files with that folder
  (§1.1), which is why it is never edited.
