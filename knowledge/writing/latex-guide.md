# LaTeX guide

Craft reference for the articles and the dissertation: each rule with its reason. House rules of this workspace
(layout, labels, build command): [latex-conventions.md](latex-conventions.md). Class swaps:
[template-porting.md](template-porting.md). Exposition of definitions and proofs: [math-writing.md](math-writing.md).

Environment of the claims below: MiKTeX 25.12, LaTeX 2025-11-01, pdfTeX 1.40.28; "tested" means a test build in
`archives/test-evidence/2026-10-08/latex-tests/` on 2026-10-08. Sources: last section.

## 1. Engine and encoding

- **pdfLaTeX** is the default: the build script runs it, journal classes are written for it, and arXiv "fully supports
  and automatically recognizes PDFLaTeX" [arxiv-tex].
- **LuaLaTeX** only when the document needs OpenType fonts (`fontspec`, installed) or tagged PDF with MathML
  (§16), and the venue accepts it. Never switch engines during a port without checking the venue.
- Source files are UTF-8. UTF-8 is the default input encoding since LaTeX 2018-04-01 [ltnews28], so
  `\usepackage[utf8]{inputenc}` is redundant (harmless).
- `\usepackage[T1]{fontenc}`: hyphenation of accented words and searchable text. Combine it with an outline font
  (`lmodern`, `newtx`): T1 with Computer Modern needs `cm-super` (installed 2026-10-08) and without it falls back to
  blurry Type 3 bitmap fonts (seen with `elsarticle` 2026-10-07 and `cas-sc` 2026-10-08).

## 2. Fonts and microtype

- The class decides the fonts. Neutral template: `lmodern`. Never override a venue's font (LIPIcs forbids it,
  [template-porting.md](template-porting.md) §6.3).
- `\usepackage{microtype}` after the fonts: character protrusion and font expansion (pdfTeX, LuaTeX; XeTeX has
  protrusion only) give fewer overfull lines and a smoother right margin [microtype].
- Latin Modern has no bold small caps (`t1lmr.fd` declares no `bx/sc`). Bold contexts with `\textsc` (problem-box
  title, headings) then warn "Font shape `T1/lmr/bx/sc' undefined". Silent, deliberate substitution:

  ```latex
  \AtBeginDocument{\DeclareFontShape{T1}{lmr}{bx}{sc}{<->ssub*lmr/m/sc}{}}
  ```

- Math alphabets: `\mathbb` from `amssymb`; `\bm` (package `bm`) for bold symbols, not `\mathbf` (upright).

## 3. Preamble load order and known conflicts

```latex
\newcommand*{\DoNotLoadEpstopdf}{}  % 1
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage[margin=2.5cm]{geometry}
\input{preamble/packages}           % amsmath, amssymb, amsthm, thmtools, mathtools, graphicx, booktabs, ...
\usepackage[numbers,sort&compress]{natbib}
\usepackage[hidelinks]{hyperref}    % 2
\usepackage[capitalise,noabbrev]{cleveref}  % 3
\input{preamble/environments}       % 4
\input{preamble/macros}
```

1. cleveref with options leaves them in `\@curroptions`; `epstopdf-base` (loaded by `pdftex.def` at
   `\begin{document}`) then requires `grfext.sty`, which this MiKTeX lacked until 2026-10-08: "File `grfext.sty' not
   found" (tested). `\DoNotLoadEpstopdf` before `\documentclass` disables the EPS converter. Since `grfext` was
   installed (2026-10-08) the line is optional; never set it for a venue that wants EPS figures (Algorithmica), or
   EPS figures stop building. Article 2 leaves it out and converts EPS with `epstopdf` (tested 2026-10-09).
2. hyperref redefines many commands: load it after other packages [hyperref, §3].
3. cleveref after every package that does not support it, including hyperref [cleveref, §2, §13].
4. Theorem definitions after cleveref (cleveref requires `\newaliascnt` after itself [cleveref, §6]); use
   `\declaretheorem` (§6).

| Conflict | Symptom | Fix |
|---|---|---|
| `newtxmath` before `amsthm` | "Command \openbox already defined" (tested) | load `amsthm` first, or `\usepackage[amsthm]{newtxmath}` [newtx]; if the class loads newtxmath: `\let\openbox\relax` before `amsthm` |
| `newtxmath` before `amssymb` | "Command `\Bbbk' already defined" (tested) | drop `amssymb` (newtxmath has the AMS symbols) or `\let\Bbbk\relax` |
| `natbib` with `biblatex` | biblatex lists natbib as incompatible (`biblatex.sty`) | one system per document (§10) |
| package already loaded by the class with other options | "Option clash for package x" | `\PassOptionsToPackage{opt}{x}` before `\documentclass`, or drop the line |
| `.bst` defines a macro in the `.bbl` (`new-aiaa.bst` defines `\enquote`) | "Command \enquote already defined" with csquotes | `\let\enquote\undefined` before `\bibliography` (tested 2026-10-07) |
| shared theorem counter + cleveref | `\cref` prints "Definition" for a lemma (tested) | `\declaretheorem[sibling=...]` (§6) |

Find what a class loads: `grep -E "RequirePackage|LoadClass" <class>.cls`, or after a build
`grep -o "[a-z0-9-]*\.sty" outputs/<p>/main.log | sort -u`.

## 4. Cross-references and hyperref

```latex
\newcommand{\PaperTitle}{Min Cut-Path Problem}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={\PaperTitle}, pdfauthor={Norbert Micheľ}, pdfkeywords={cut, shortest path}}
```

- Metadata: `\hypersetup{pdftitle=..., pdfauthor=...}`, or option `pdfusetitle`, which derives both from `\title` and
  `\author` [hyperref, §7.21]. Use explicit `\hypersetup` when `\author` holds affiliations and line breaks.
- `hidelinks` removes boxes and color [hyperref]; use it for print-like output. Colored links (`colorlinks`) only
  if the venue asks; classes that load hyperref themselves (LIPIcs) set their own link style.
- Math or commands in headings: `\section{\texorpdfstring{$G(n,p)$}{G(n,p)}}` gives a clean bookmark [hyperref].
- Reference commands (cleveref with `capitalise,noabbrev`):

  | Command | Output |
  |---|---|
  | `\cref{thm:main}` | Theorem 3.1 |
  | `\cref{lem:a,lem:b}` | Lemmas 2.3 and 2.4; three consecutive labels give "Lemmas 2.3 to 2.5" (sorted and compressed [cleveref, §5]; tested) |
  | `\crefrange{lem:a}{lem:d}` | Lemmas 2.3 to 2.6 (tested) |
  | `\Cref{...}` | capitalized form for sentence starts; identical with `capitalise`, robust if the option goes |
  | `\eqref{eq:x}` | (2.1) |
  | `\nameref{sec:x}` | the section title (hyperref/nameref) |

- Custom counter: `\crefname{<counter>}{Name}{Names}` (singular, plural) [cleveref, §8].
- `\label` after `\caption`: `\caption` sets the counter `\label` records; before it the label takes the section
  number (tested: "2" instead of "1").
- Algorithm lines: `line~\ref{line:x}`; `\cref` prints "Algorithm 1" for a line label (tested).
- Never type numbers by hand ("Theorem 3"); a renumbering breaks them silently.

## 5. Math

```latex
\DeclareMathOperator{\diam}{diam}                 % upright name, operator spacing
\DeclarePairedDelimiter{\abs}{\lvert}{\rvert}     % \abs{x}, \abs*{\frac{a}{b}}, \abs[\big]{x}
S \coloneqq \set{v \in V : \deg(v) \geq 2}        % := with centered colon (mathtools)
```

- Load `mathtools` (it loads and fixes `amsmath`) [mathtools]; `amsmath` provides `\DeclareMathOperator`, `\text`,
  the display environments and `\dots` variants [amsldoc].
- `\abs*` scales with `\left...\right`, `\abs[\big]` sets the size by hand [mathtools]. Never `|x|` for
  absolute values in new text: spacing and sizing.
- Display environments [amsldoc]:

  | Environment | Use |
  |---|---|
  | `\[ ... \]` | one unnumbered equation |
  | `equation` | one numbered equation |
  | `align` | several equations aligned at `&` |
  | `gather` | several equations, centered, no alignment |
  | `multline` | one long equation over several lines, one number |
  | `split` (inside `equation`) | one long equation aligned, one number |

- Number only equations that are referenced; use starred forms or `\[ \]` for the rest (or `mathtools`
  `\mathtoolsset{showonlyrefs}`, which numbers only equations cited with `\eqref` [mathtools]).
- Never `$$...$$` (bypasses LaTeX's display code: spacing, `fleqn`, QED [texfaq-dolldoll]) and never `eqnarray`
  (not supported with amsmath; use `align` [l2tabu]).
- Words in math: `\text{if } x > 0`; names of functions: operators, not italics (`\deg`, `\diam`, `\cp`).
- A display is part of the sentence: end it with the punctuation the sentence needs (`, ` or `.` inside the display).
- Dots: `\dots` chooses by context; explicit `\dotsc` (commas), `\dotsb` (binary operators) [amsldoc].
- Inline math stays short; break long formulas into displays instead of letting them overflow (§12).

## 6. Theorem environments and proofs

- `amsthm` defines styles and `proof`; `thmtools` (`\declaretheorem`) adds key-value definitions, names for cleveref
  and restatable theorems [thmtools].
- Shared counter: `\declaretheorem[name=Lemma, style=plain, sibling=definition]{lemma}`; `sibling` equals
  `numberlike`/`sharenumber` [thmtools]. With `\newtheorem{lemma}[definition]{Lemma}`, cleveref 0.21.4 prints
  "Definition 1.2" for the lemma in this LaTeX (tested), although its manual documents amsthm support [cleveref, §8].
  The LaTeX tagging project lists the `sibling` key as wrongly numbered under tagging [tagging]; irrelevant while
  documents are untagged.
- Restate a theorem (introduction and later, or proof in the appendix):

  ```latex
  \begin{restatable}{theorem}{mainthm}
  \label{thm:main}
  Every graph of diameter two satisfies $\cp(u,v) = c + d - 1$.
  \end{restatable}
  ...
  \mainthm*          % same number, links to the original
  ```

  `restatable` comes from `thm-restate` (part of thmtools); `\usepackage{thmtools}` alone suffices here (tested)
  [thmtools, §1.4].
- Proofs [amsthdoc]: a proof ending with a display or a list gets `\qedhere` at the end of the display or before
  `\end{itemize}`; `\qedhere` fails in `eqnarray` and `$$`. Name the proved statement when the proof is separated:
  `\begin{proof}[Proof of \cref{thm:main}]`.
- House rules on proof layout: [latex-conventions.md](latex-conventions.md) §4.

## 7. Algorithms

```latex
\begin{algorithm}[tb]
  \caption{Reduction from \textproblem{3-SAT}.}
  \label{alg:reduction}
  \begin{algorithmic}[1]                        % [1]: number every line
    \Require formula $\varphi$ with clauses $C_1, \dots, C_m$
    \Ensure graph $G$ and vertices $u, v$
    \Procedure{Reduce}{$\varphi$}
      \State $G \gets \emptyset$
      \For{$k \gets 1$ \textbf{to} $m$} \Comment{one gadget per clause}
        \State \Call{AddGadget}{$G, C_k$} \label{line:gadget}
      \EndFor
      \State \Return $(G, u, v)$
    \EndProcedure
  \end{algorithmic}
\end{algorithm}
```

- `algorithm` (float, from the `algorithms` bundle) + `algpseudocode` (algorithmicx): `\Require`, `\Ensure`,
  `\Comment`, `\Procedure`/`\Function`, `\Call`, `\Return` [algorithmicx]. `algorithm2e` is not installed.
- Caption and label at the top of the float; reference lines with `line~\ref{line:gadget}` (§4).
- Single line spacing inside `algorithmic` when the class sets double spacing:
  `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (article 1 under its former class `new-aiaa`).
- What the pseudocode contains: [math-writing.md](math-writing.md) §6.

## 8. Figures

- Formats: vector PDF for drawings and plots, PNG for screenshots and raster images, JPG for photographs only.
  EPS needs conversion: `epstopdf` does it during the pdfLaTeX build unless `\DoNotLoadEpstopdf` is set (§3); keep
  EPS where the venue asks for it (Algorithmica).
- Draw with TikZ in a standalone source next to the figure, compiled to PDF:

  ```latex
  % img/chain-link.tex  ->  img/chain-link.pdf
  \documentclass[tikz,border=2pt]{standalone}   % output cropped to the drawing [standalone]
  \usepackage[T1]{fontenc}
  \usepackage{lmodern}                            % same fonts as the paper
  \begin{document}
  \begin{tikzpicture} ... \end{tikzpicture}
  \end{document}
  ```

  Without the font lines the figure uses Computer Modern (CMR10 appeared in the template test next to Latin Modern).
- Width relative to the text block: `\includegraphics[width=0.8\linewidth]{img/x}`. Inside a float `\linewidth`
  equals the column width, so the figure survives a switch to two columns; `figure*` spans both columns.
- Text in figures at least the size of the caption text; never scale a figure so that its labels shrink below it.
- Subfigures (`subcaption`, installed; LIPIcs loads it itself):

  ```latex
  \begin{figure}[tb]
    \centering
    \begin{subfigure}{0.48\linewidth}\centering
      \includegraphics[width=\linewidth]{img/a}\caption{Before.}\label{fig:a}
    \end{subfigure}\hfill
    \begin{subfigure}{0.48\linewidth}\centering
      \includegraphics[width=\linewidth]{img/b}\caption{After.}\label{fig:b}
    \end{subfigure}
    \caption{Both states of the chain.}\label{fig:ab}
  \end{figure}
  ```

- Placement `[tb]`: floats belong at the top or bottom of a page. `[H]` (package `float`) forces "put it here"
  [float] and leaves gaps when the float does not fit; use it only when the float must follow a specific line.
  Floats drifting too far: move the float's source earlier in the text, not `[H]`.
- Color: readable in gray print and for color-blind readers; vary marker shape and line style as well as hue.
  Paul Tol's "bright" scheme is color-blind safe [tol]:

  ```latex
  \definecolor{tolblue}{HTML}{4477AA}  \definecolor{tolcyan}{HTML}{66CCEE}
  \definecolor{tolgreen}{HTML}{228833} \definecolor{tolyellow}{HTML}{CCBB44}
  \definecolor{tolred}{HTML}{EE6677}   \definecolor{tolpurple}{HTML}{AA3377}
  \definecolor{tolgray}{HTML}{BBBBBB}
  ```

  The CTAN package `colorblind` packages Tol's and Okabe-Ito's schemes; not installed.
- Experiment plots are generated from the data file, so a rerun of the experiment regenerates the figure:

  ```latex
  % img/runtime.tex (standalone) reads data/runtime.csv: n,exact,heuristic
  \usepackage{pgfplots}\pgfplotsset{compat=1.18}
  \begin{tikzpicture}
    \begin{axis}[xlabel={$n$}, ylabel={time (s)}, ymode=log, legend pos=north west]
      \addplot+[tolblue, mark=o] table[col sep=comma, x=n, y=exact]{data/runtime.csv};
      \addplot+[tolred, mark=square] table[col sep=comma, x=n, y=heuristic]{data/runtime.csv};
      \legend{exact, heuristic}
    \end{axis}
  \end{tikzpicture}
  ```

  `col sep=comma` applies to `\addplot table` [pgfplotstable]. Keep the CSV in the project (`data/`), never
  numbers typed into the plot. Reporting rules for tables and figures: [experiments-reporting.md](experiments-reporting.md) §6.

## 9. Tables

```latex
\begin{table}[tb]
  \centering
  \caption{Running time in seconds, mean of 10 runs.}   % caption above the table
  \label{tab:runtime}
  \begin{tabular}{@{}l S[table-format=4.0] S[table-format=2.2]@{}}
    \toprule
    Instance & {$\abs{V}$} & {Time (s)} \\                % braces: header is not a number
    \midrule
    \texttt{grid-10} &  100 &  0.12 \\
    \texttt{grid-50} & 2500 & 12.85 \\
    \bottomrule
  \end{tabular}
\end{table}
```

- `booktabs` rules (`\toprule`, `\midrule`, `\cmidrule`, `\bottomrule`); no vertical rules, no double rules
  [booktabs, §2]. Separate groups with `\cmidrule` or space, not lines.
- Numbers aligned on the decimal point with `siunitx` `S` columns (`table-format=<int>.<dec>`); non-numeric cells in
  braces [siunitx]. Same number of decimals within a column.
- Caption above tables (reader meets the caption before the data), below figures.
- Text columns that must fill the width: `tabularx` with `X` columns [tabularx]. Tables longer than a page: `longtable`
  (installed); `xltabular`, `ltablex` are not installed.
- Table notes: put notes in a `\footnotesize` paragraph directly under the `tabular`, inside the float.
  `threeparttable` is installed since 2026-10-08 (the class `sn-jnl` loads it); its notes are untested here.
- Units in the header (`Time (s)`), not in every cell.

## 10. Bibliography mechanics

| | BibTeX + natbib (default) | biblatex + biber |
|---|---|---|
| style | `.bst` file from the template | `.bbx`/`.cbx` options |
| journals | BibTeX is the default of every class in the quirks table of [template-porting.md](template-porting.md) §6.2; natbib only where the class loads it (elsarticle, acmart, sn-jnl, new-aiaa); LIPIcs, SIAM, IEEEtran, llncs use plain BibTeX | only where the class allows it (acmart: experimental variants) |
| arXiv | upload the `.bbl` | upload the `.bbl`; its format must match arXiv's biblatex: TeX Live 2025 accepts only bbl format 3.3 [arxiv-tex]; local biblatex 3.21 writes 3.3 |
| this workspace | articles | CV (`biblatex-ieee`) |

- Load one system: biblatex declares natbib incompatible (`biblatex.sty`).
- Keep `\cite{key}` in the source; it works under natbib, biblatex and plain BibTeX classes. `\citet`/`\citep`
  only when the venue uses author-year natbib [natbib]. Locator: `\cite[Theorem~7.3]{Bollobas2001}`.
- natbib options in the neutral wrapper: `numbers,sort&compress` ([1-3] instead of [1, 2, 3]).
- The `.bst` decides what is printed: `plainnat` prints `doi`, `isbn` and `url` fields (fields present in
  `plainnat.bst`); a journal `.bst` may ignore them. Never edit `.bib` data to fix the look; switch or patch the style.
- The `.bbl` is generated (`outputs/`); a venue or arXiv that does not run BibTeX gets the `.bbl` with the sources,
  renamed to the main file's name [arxiv-tex]. The packager puts it into the zip
  ([latex-conventions.md](latex-conventions.md) §1.1).
- Entry rules (fields, keys, verification): [../bibliography/README.md](../bibliography/README.md).

## 11. Text typography

| Need | Write | Reason |
|---|---|---|
| reference with name | `Theorem~\ref{thm:a}`, `\cref{thm:a}` | `~` keeps name and number on one line (cleveref inserts it) |
| citation | `graph theory~\cite{Diestel2025}` | no line break before the bracket |
| number range, pair | `151--158`, `$u$--$v$ path` | en dash |
| parenthetical dash | `text---text` | em dash, no spaces (American) |
| hyphen in a compound | `cut-path`, `NP-hard` | plain hyphen |
| quotation | `\enquote{text}` (csquotes) | correct and nested quotes; `autostyle` follows babel [csquotes] |
| sentence ends after a capital | `solvable in P\@.` | otherwise LaTeX reads an abbreviation and sets a short space [latexref-at] |
| abbreviation inside a sentence | `et al.\ proved`, `cf.~\cite{key}` | otherwise LaTeX sets a sentence space [latexref-at]; `e.g.,` and `i.e.,` take a comma ([academic-style.md](academic-style.md) §2) and need no `\ ` |
| ellipsis | `\dots` (text), `\dotsc`/`\dotsb` (math) | spacing [amsldoc] |
| number with unit | `\qty{2.5}{\second}`, `\num{12345}` | consistent spacing and grouping (siunitx) [siunitx] |
| list spacing | `\begin{itemize}[nosep]` (enumitem) | compact lists [enumitem]; LIPIcs forbids enumitem ([template-porting.md](template-porting.md) §3) |
| emphasis | `\emph{...}` | never bold or underline in running text |

- Math in text is math: `$n$ vertices`, not `n vertices`; numbers alone stay text (`3 graphs`).
- Slovak text (abstract in Slovak, thesis declarations): `\usepackage[slovak,american]{babel}` and
  `\begin{otherlanguage}{slovak}...\end{otherlanguage}`; Slovak hyphenation patterns are installed (tested:
  "naj-nep-rav-de-po-dob-nej-šieho"). The last language option is the main language.

## 12. Hyphenation and overfull boxes

- Diagnose: `grep -A3 "^Overfull" outputs/<p>/main.log` gives the width, the source lines and the text of the line.
  The class option `draft` marks every overfull line with a black bar (`\overfullrule` 5pt, tested).
- Fix in this order:
  1. reword the sentence (move a long formula or URL, split an inline formula into a display);
  2. teach hyphenation: `\hyphenation{cut-path NP-com-plete-ness}` in the preamble, or `\-` once in the word;
  3. break long URLs with `xurl` (installed).
- Never a global `\sloppy`: it spreads bad spacing over the whole document [l2tabu, §1.8]; a single paragraph may
  use `sloppypar` as a last resort.
- `microtype` (§2) removes most overfull lines before any manual fix.
- Underfull boxes ("badness 10000") from forced `\\` or `\newline` in text: remove the manual break.

## 13. Drafts

- Notes: `todonotes` (installed): `\todo{check bound}`, `\todo[inline]{...}`, `\missingfigure{sketch of the chain}`,
  `\listoftodos`; option `disable` removes all notes without editing the text [todonotes].
- Draft/final switch in `main.tex`:

  ```latex
  \newif\ifdraft \drafttrue          % \draftfalse for the submitted version
  \ifdraft
    \setlength{\marginparwidth}{2cm} % article's default is narrower; todonotes warns [todonotes, §1.6]
    \usepackage[colorinlistoftodos]{todonotes}
  \else
    \usepackage[disable]{todonotes}
  \fi
  ```

- Before any upload of sources (journal, arXiv, Overleaf share): no comments, `\iffalse` blocks or unused files;
  arXiv sources are downloadable and comments in them are visible [arxiv-cleaner]. The packager strips comment lines
  and lists the remaining end-of-line comments and the unused files ([latex-conventions.md](latex-conventions.md)
  §1.1); `\iffalse` blocks are deleted in the project by hand. `arxiv_latex_cleaner` (Python) is not installed and
  not needed.
- `todonotes` breaks tagged PDF (tagging status "currently-incompatible" [tagging]): always `disable` for the final build.

## 14. Long documents

- `\input{file}` inserts text verbatim (sections of an article). `\include{file}` starts a new page and writes its own
  `.aux`; `\includeonly{chapters/03-results}` in the preamble builds only that chapter while keeping numbers and
  references of the others (tested).
- Thesis: `chapters/NN-name.tex` via `\include`; the build script mirrors subfolders into `outputs/<p>/` so the
  per-chapter `.aux` files can be written (comment in `scripts/build-project.ps1`).
- One preamble for the whole document; chapter files contain no `\usepackage`.
- Front matter, main matter and appendices: `\appendix` before the first appendix chapter; `appendix` package
  (installed) for appendix headings in the table of contents.

## 15. Version control and revisions

- One sentence per line: a change touches one line, diffs and review comments point to sentences.
- Revisions for reviewers: marked PDF through the `\rev{}` wrapper, not `latexdiff`
  ([submission.md](submission.md) §5.3 gives the stub status and the procedure; do not run `latexdiff`).
  `latexpand`, `texcount` and `latexindent` are likewise on `PATH` only as MiKTeX stubs (checked 2026-10-08); their
  scripts are not in `texmfs/install/scripts`, so running them may start the MiKTeX package installer: ask the owner
  before the first run. `chktex` (1.7.9) and `lacheck` are native and run (`chktex -q -v0 <file>.tex`).
- Freeze the submitted state in `archives/submissions/<project>/<YYYY-MM-DD>-<venue>-<stage>/`
  ([submission.md](submission.md) §3.2 step 6); a git tag only when the owner asks.
- The workspace is its own git repository (branch `main`): no commit or stage without the owner (CLAUDE.md).

## 16. PDF quality and accessibility

| Check | Command | Expected |
|---|---|---|
| metadata | `pdfinfo main.pdf` | Title and Author set (template: `\hypersetup`) |
| fonts | `pdffonts main.pdf` | every font `emb yes`, Type 1 or TrueType/CID, no Type 3 (bitmap) |
| page size | `pdfinfo main.pdf \| grep "Page size"` | A4 or the venue's size |
| text extractable | `pdftotext -enc UTF-8 main.pdf -` | readable words, ligatures and diacritics intact |

- Bookmarks come from hyperref; `\texorpdfstring` keeps them readable (§4).
- PDF/A (a repository or the university requires it): `pdfx` with option `a-1b`, `a-2b`, `a-2u` or `a-3u`, loaded
  directly after `\documentclass`; metadata in `\jobname.xmpdata` (`\Title`, `\Author` with `\sep`, `\Language`,
  `\Keywords`); hyperref options then go into `\hypersetup` [pdfx]. hyperref's own `pdfa` option alone does not
  produce PDF/A [hyperref, §7.13]. Validation needs veraPDF, not installed. In the thesis template `pdfx` (`a-2b`) compiled but gave
  duplicate-destination warnings on floats (2026-10-08), so the template does not offer it ([thesis.md](thesis.md) §7). University requirements:
  [thesis.md](thesis.md).
- Tagged PDF (structure for screen readers): enabled with `\DocumentMetadata{tagging=on}` before `\documentclass`
  [tagging]. **Not available here**: this MiKTeX stops with "No support files for \DocumentMetadata found" under
  pdfLaTeX and LuaLaTeX (tested). Status of packages in the tagging project's list (checked 2026-10-08) [tagging]:

  | Status | Packages and classes used here |
  |---|---|
  | compatible | article, xcolor, algorithmicx/algpseudocode, natbib, booktabs, microtype |
  | partially compatible | amsmath, amsthm, mathtools, hyperref, cleveref, tcolorbox, siunitx, csquotes, enumitem, newtx, tikz, biblatex; classes amsart, acmart |
  | currently incompatible | caption, subcaption, float, algorithm, pgfplots, thmtools, todonotes; classes llncs, IEEEtran |

- Alternative text: `\includegraphics[alt={Chain of four links ...}]{img/chain}`; graphicx accepts the `alt` key
  but ignores it unless tagging is active (`graphicx.sty`). Write it anyway for figures that carry content.
  Venues that ask for it (checked 2026-10-08): acmart wants `\Description{...}` inside every `figure` environment
  [acmart]; Springer proceedings (LNCS) require textual substitutes for all figures and tables in image formats,
  written by the authors on request or by the typesetter (instructions PDF, section 3, linked from
  https://link.springer.com/series/558/information-for-authors-and-editors). Other target venues: TODO(verify)
  per venue card.
- Accessible content regardless of tagging: real text (no text as images), vector figures, color-blind-safe
  palettes (§8), captions that state what the figure shows.

## 17. Build hygiene

- Build only with `.\scripts\build-project.ps1 -Project <p>`: latexmk reruns LaTeX and BibTeX/biber until
  references settle [latexmk]; `-halt-on-error` and `-file-line-error` make the first error final and locatable;
  `-disable-installer` keeps MiKTeX from downloading packages silently.
- Warnings that matter (fix or record in the project README):

  | Log text | Meaning |
  |---|---|
  | `Reference ... undefined`, `Citation ... undefined`, `??`, `[?]` in the PDF | missing label or `.bib` key |
  | `There were multiply-defined labels` | two `\label` with one name |
  | `Label(s) may have changed. Rerun` (at the end) | latexmk stopped early |
  | `Overfull \hbox` | text in the margin (§12) |
  | `Font shape ... undefined`, `Some font shapes were not available` | substituted font (§2) |
  | `Empty 'thebibliography' environment` (natbib) | no `\cite` yet |
  | BibTeX `Warning--empty ...`, `I didn't find a database entry` | incomplete or missing entry |

- Harmless here: `major issue: So far, you have not checked for MiKTeX updates` (MiKTeX notice in every tool's
  output).
- Log commands (Git Bash, workspace root):

  ```bash
  L=outputs/<p>/main.log
  grep -n -E "^!|Error" $L                               # errors
  grep -n -E "Warning" $L | grep -v infwarerr             # all warnings
  grep -n -A3 "^Overfull" $L                              # overfull lines with context
  grep -E "^Warning|error message" outputs/<p>/main.blg   # BibTeX
  pdftotext -enc UTF-8 outputs/<p>/main.pdf - | grep -n -E "\?\?|\[\?\]"   # unresolved references in the PDF
  ```

- Run `build-project.ps1` and `latexmk` from PowerShell, not from Git Bash: there BibTeX receives `/c/...` paths, fails
  to find the project's `.bst`/`.bib` and can silently read a stray `references.bib` from the MiKTeX tree (observed
  2026-10-08 by two independent builds).
- Clean build criteria for this workspace: [latex-conventions.md](latex-conventions.md) §2. Template conformance,
  self-containedness and the package that is sent (`scripts/package-project.ps1`): §1.1 there.
- Static check of the source: `chktex -q -v0 sections/*.tex`; prose checks: `scripts/check-text.ps1`.

## Sources

Opened 2026-10-08 unless noted. CTAN files were read from the mirror `https://ctan.gust.org.pl/tex-archive/`
(abbreviated `CTAN:`) or from the local MiKTeX documentation tree.

| Key | Source |
|---|---|
| acmart | acmart 2.20 (2026-08-16) user guide inside `acmart.dtx`, CTAN: macros/latex/contrib/acmart/acmart.dtx |
| amsldoc | User's Guide for the amsmath Package v2.1, CTAN: macros/latex/required/amsmath/amsldoc.pdf |
| amsthdoc | Using the amsthm package, CTAN: macros/latex/required/amscls/doc/amsthdoc.pdf |
| arxiv-cleaner | arxiv-latex-cleaner 1.0.11, https://pypi.org/project/arxiv-latex-cleaner/ |
| arxiv-tex | arXiv, Submitting TeX/LaTeX, https://info.arxiv.org/help/submit_tex.html |
| booktabs | booktabs documentation, local `doc/latex/booktabs` (MiKTeX) |
| cleveref | cleveref 0.21.4 manual, local `doc/latex/cleveref/cleveref.pdf` |
| csquotes | csquotes v5.2p (2026-05-19), CTAN: macros/latex/contrib/csquotes/csquotes.pdf |
| enumitem | enumitem 3.11 (2025-02-06), CTAN: macros/latex/contrib/enumitem/enumitem.pdf |
| float | float documentation, local `doc/latex/float` |
| hyperref | hyperref manual v7.01r (2026-06-17), CTAN: macros/latex/contrib/hyperref/doc/hyperref-doc.pdf |
| l2tabu | l2tabu v1.8 (English), CTAN: info/l2tabu/english/l2tabuen.pdf |
| latexmk | latexmk manual, CTAN: support/latexmk/latexmk.pdf |
| latexref-at | LaTeX2e unofficial reference manual, `\@`, https://latexref.xyz/_005c_0040.html |
| ltnews28 | LaTeX News 28 (2018-04-01), https://www.latex-project.org/news/latex2e-news/ltnews28.pdf |
| mathtools | mathtools manual (2024-10-04), CTAN: macros/latex/contrib/mathtools/mathtools.pdf |
| microtype | microtype v3.2d (2026-03-01), CTAN: macros/latex/contrib/microtype/microtype.pdf |
| natbib | natbib 8.31b documentation, local `doc/latex/natbib` |
| newtx | newtx documentation (2024-06-22), CTAN: fonts/newtx/doc/newtxdoc.pdf |
| pdfx | pdfx (2024-07-01), CTAN: macros/latex/contrib/pdfx/pdfx.pdf |
| pgfplotstable | pgfplotstable 1.18.3 (2026-08-26), CTAN: graphics/pgf/contrib/pgfplots/doc/pgfplotstable.pdf |
| siunitx | siunitx (2026-09-28), CTAN: macros/latex/contrib/siunitx/siunitx.pdf |
| standalone | standalone v1.5a (2025-02-22), CTAN: macros/latex/contrib/standalone/standalone.pdf |
| tabularx | tabularx v2.12a, CTAN: macros/latex/required/tools/tabularx.pdf |
| tagging | LaTeX Tagging Project, tagging status, https://latex3.github.io/tagging-project/tagging-status/ |
| texfaq-dolldoll | TeX FAQ, "Why use \[ ... \] in place of $$ ... $$?", https://texfaq.org/FAQ-dolldoll |
| thmtools | thmtools v0.76 (2023-05-04), CTAN: macros/latex/contrib/thmtools/doc/thmtools-manual.pdf |
| todonotes | todonotes (2024-01-05), CTAN: macros/latex/contrib/todonotes/todonotes.pdf |
| tol | Paul Tol, color schemes, https://sronpersonalpages.nl/~pault/ |
| local files | `kpsewhich --miktex-disable-installer` lookups and class/package sources in the MiKTeX tree (2026-10-08) |
