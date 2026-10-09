# Porting a manuscript to a journal or conference template

Procedure for moving a project built from `templates/article-modular` (or article 1) into a venue's class.
Operational checklist for Claude: skill `port-latex-template`. House rules: [latex-conventions.md](latex-conventions.md);
package craft: [latex-guide.md](latex-guide.md); venue facts (page limits, anonymity, AI policy):
[../venues/README.md](../venues/README.md); submission package: [submission.md](submission.md).

Only `main.tex` and the class files depend on the venue. `sections/`, `img/` and `references.bib` move unchanged
(exceptions: citation commands under an author-year style, §4; layout-only edits that a narrower text block forces,
§5); `preamble/` loses only what clashes with the class and gains what the new class lacks (§3). `sections/` use
standard LaTeX markup (`[H]`, `[tb]`, list labels `[(a)]`); when a class reads standard markup differently, the
wrapper adapts the class (cas-sc: a key `H` for `[H]`, §6.3), so the next port finds `sections/` unchanged
(article 1, review 2026-10-08).

## 1. Procedure

**Conformance** is the result the procedure must reach (invariant: [latex-conventions.md](latex-conventions.md) §1.1):

- the venue's files in the project are byte-identical to `templates/<venue>/`;
- the wrapper `main.tex` is the venue's sample file with the manuscript's `\input` lines, not the old wrapper with a
  new class name;
- nothing overrides the venue's layout (page size, margins, fonts, line spacing, headings, running heads); a text
  that does not fit is shortened or moved to an appendix (§5);
- the venue's own checklist (sample file comments, author guide, venue card) has no open item;
- `package-project.ps1` proves the first point and fails on a page count over `-MaxPages` (`[pages]`). For the third
  it flags the overrides on its fixed list (`[layout]`: geometry, setspace, titlesec, fancyhdr, spacing commands,
  length settings and assignments, `\pagestyle`, `\enlargethispage`, `\vspace{-...}`, `\fontsize`, `\titleformat`,
  `\setlist`, redefined `\section` ... `\maketitle`; tested 2026-10-08). It does not see font packages or an
  override written another way: read the wrapper for those. The second and the fourth point are checked by reading.

1. **Unpack pristine.** The owner drops the template (zip or folder) into `inbox/`. Unpack it to
   `templates/<venue>/` (skill `process-inbox`), archive the zip, never edit `templates/<venue>/` afterwards.
   Record its origin URL and version (the `\ProvidesClass` line) in `templates/README.md`. `<venue>` is the name of
   the template, lowercase with hyphens: the class name when one template serves several journals (`elsarticle`,
   `sn-jnl`, `llncs`, `lipics-v2021`); the venue cards that use it name the folder in their *LaTeX* field. It is the
   value of the packager's `-Template`.
2. **Snapshot the project.** Build it, note page count and warnings; copy `main.tex` to
   `archives/removed-from-projects/<project>/main-before-port-<YYYY-MM-DD>.tex`. A project ported before: read its
   porting log (§7, line "Venue-only markup") and undo what it lists in `sections/` and `preamble/` (for example
   `[pos=H]` back to `[H]`, a package re-added that the old class loaded); the old wrapper's class adaptations (cas-sc:
   the `H` key alias, `nologo`, the font-shape lines) leave with the old wrapper and are not copied to the new one.
3. **Copy class files into the project**, unmodified: `.cls`, `.bst` (or `.bbx`/`.cbx`), logos and support files
   the sample file needs. Move the files of the old class (`.cls`, `.bst`) to
   `archives/removed-from-projects/<project>/`. Check that every package the class requires exists:
   `Select-String -Pattern "RequirePackage|LoadClass" <class>.cls` (PowerShell has no `grep`; lines inside
   `\IfFileExists` are optional), then `kpsewhich --miktex-disable-installer <pkg>.sty` for each.
   Missing ones: ask the owner before any install (CLAUDE.md rule 6); §6.1 lists what is missing for the classes
   below.
4. **Write the new wrapper `main.tex` from the template's sample file**, not from the old wrapper: keep the sample's
   class options, front-matter commands and bibliography commands; replace its body by the `\input` lines of
   `sections/`. Keep `\newcommand*{\DoNotLoadEpstopdf}{}` before `\documentclass` when cleveref gets options
   ([latex-guide.md](latex-guide.md) §3).
5. **Map the front matter** (§2). Data come from [../author.md](../author.md); never invent an ORCID, funding number
   or classification code.
6. **Adapt `preamble/`** (§3): remove what clashes with the class (theorem environments it defines, packages it
   forbids or loads with other options), rename what clashes, keep the load order; a package the class loads too
   stays (a repeated `\usepackage` without options does nothing, and `preamble/` stays portable). List what the *old*
   class loaded (`Select-String -Pattern RequirePackage <old>.cls`) and keep what the sections use of it
   (new-aiaa: `microtype`; for list labels see §6.3, Lists); a missing one shows no warning, only option text or
   overfull lines in the output (§3). Do not change `sections/` markup for the class: adapt the class in the wrapper
   (§6.3), and if a layout-only edit there cannot be avoided, list it in the porting log with the markup to restore
   at the next port.
7. **Bibliography**: copy the venue's style, switch `\bibliographystyle` to a style the template ships (or the
   biblatex options; sn-jnl: the class option sets the style and the wrapper has no `\bibliographystyle`, §6.2). A numeric venue: the source keeps plain `\cite`, nothing else changes. An author-year venue:
   plain `\cite` alone prints the textual form, so add `\let\cite\citep` to the wrapper and replace each
   *Names*`~\cite{key}` in `sections/` by `\citet{key}` (§4); list these replacements in the porting log.
8. **Layout consequences** (§5): two columns, page size, fonts.
9. **Build** with `.\scripts\build-project.ps1 -Project <project>`; fix errors; then compare with the snapshot:
   page count, undefined references/citations, overfull lines, font substitutions (`pdffonts`), the class's own
   warnings, and `pdftotext -layout` of both PDFs: only front matter, numbering, list labels, the reference list
   and line breaks may differ (leaked option text such as `label=(a)` or a doubled period `..` is a defect, §6.3).
   Run the template's checklist (sample file comments, author guide, venue card). Then the static checks:
   `.\scripts\package-project.ps1 -Project <project> -Template <venue> -CheckOnly`; no `[template-file]`,
   `[template-bst]`, `[outside]` or `[missing]` may remain; every `[layout]` line is removed from the source, or kept
   with its reason under "Known problems".
10. **Record** the porting log (§7) in the project README; list leftovers under "Known problems".
11. **Package**, the proof that the port conforms ([latex-conventions.md](latex-conventions.md) §1.1):

    ```powershell
    .\scripts\package-project.ps1 -Project <project> -Template <venue> [-MaxPages <n>] [-Flat]
    ```

    `-MaxPages`: the page limit on the venue card; leave it out when the card states none (a type's limit, such as
    the Note of Discrete Applied Mathematics, does not bind a Contribution). `-Flat`: the venue builds from one
    directory (Elsevier Editorial Manager, Springer). The port is done on `Verdict: PASS` (a page count over
    `-MaxPages` fails it); the verdict goes into the porting log. The
    script does not inline `\input`: the one-file request of the Springer Nature sample is in §6.3. What a
    submission adds: [submission.md](submission.md) §3.2.

## 2. Front-matter map

| Item | Neutral template (`article`) | In the venue classes |
|---|---|---|
| title, short title | `\title{\PaperTitle}` | `\title[short]{long}`: acmart, amsart, sn-jnl; llncs `\titlerunning{short}`; LIPIcs `\titlerunning{short}` (only when the title exceeds one line); SIAM `\headers{short title}{authors}`; cas-sc `\title[mode = title]{long}` plus `\shorttitle{}` and `\shortauthors{}` for the running head and footer, all after `\begin{document}` and before `\maketitle` |
| authors, affiliations | `\author{...}` with `\\` lines | llncs `\author{A\inst{1} \and B\inst{2}}` + `\institute{I$_1$ \and I$_2$}`, `\authorrunning`; LIPIcs `\author{name}{affiliation}{email}{ORCID URL}{funding}` once per author, `\authorrunning`, `\Copyright`; elsarticle `\author[l1]{}` + `\affiliation[l1]{organization=,addressline=,city=,postcode=,country=}` inside `frontmatter`; cas-sc `\author[1]{Name}`, `\cormark[1]`, `\ead{e-mail}`, `\affiliation[1]{organization=,addressline=,postcode=,postcodesep={},city=,country=}` (keys are printed in the order given; `postcode` then `postcodesep={}` then `city` prints "040 01 Košice", as the sample does for Amsterdam), `\cortext[1]{Corresponding author}`; sn-jnl `\author*[1,2]{\fnm{} \sur{}}\email{}` (`*` marks the corresponding author) + `\affil*[1]{\orgdiv{}, \orgname{}, \orgaddress{\street{}, \city{}, \postcode{}, \state{}, \country{}}}` (commas as in the sample), a single author and address without the numbers (user manual; tested: prints "*" before the affiliation and "Corresponding author(s). E-mail(s): ...;"); acmart per author `\author{}`, `\orcid{}`, `\affiliation{\institution{}\city{}\country{}}`, `\email{}` (institution, city, country mandatory); IEEEtran `\author{Name,~\IEEEmembership{...}}` with `\thanks{affiliation}`; SIAM `\author{...\thanks{}}` joined by `\and`, `\email{}`; amsart `\author{}` + `\address{}`, `\email{}`, `\urladdr{}` (printed at the end of the article) |
| full affiliation | Institute of Computer Science, Faculty of Science, Pavol Jozef Šafárik University in Košice, Jesenná 5, 040 01 Košice, Slovakia ([../author.md](../author.md), from the institute's contact page) | as above |
| ORCID | none | llncs `\orcidID{...}` after the name; LIPIcs fourth `\author` argument; acmart `\orcid{...}`; SIAM `\orcid{}` is accepted and prints nothing; sn-jnl `\orcid{URL}` (a link around `\includegraphics{Orcidlogo.eps}`, class source; the zip has no `Orcidlogo.eps`, §6.3); cas-sc option `orcid=` of `\author[1]{Name}[orcid=...]` (sample; the class prints an "ORCID(s):" footnote line even when no author has one, §6.3); elsarticle, IEEEtran, amsart: no command in the class source or sample; use `\orcidlink` (package `orcidlink`, installed) after the name or the submission form |
| abstract | `sections/00-abstract.tex` inside `abstract` | `abstract` environment in all classes; sn-jnl `\abstract{...}` as a command, before `\maketitle` (the class stores the text and prints it in `\maketitle`, so `\abstract{\input{sections/00-abstract}}` works, tested); amsart: before `\maketitle`; elsarticle: inside `frontmatter`; cas-sc: before `\maketitle`, written as `\begin{abstract}[\abstractname]` when the body is an `\input` line (§6.3) |
| keywords | manual `\noindent\textbf{Keywords:}` line | llncs `\keywords{A \and B}` inside the `abstract` environment, after the `\input`; LIPIcs, acmart, sn-jnl, amsart `\keywords{...}`; elsarticle `keyword` environment with `\sep`; cas-sc `keywords` environment with `\sep`, before `\maketitle`; IEEEtran `IEEEkeywords` environment; SIAM `keywords` environment |
| MSC 2020 | none | amsart `\subjclass[2020]{05C40, 68Q17}`; elsarticle `\MSC[2020] code \sep code` (default is 2000); cas-sc `\MSC` (defined in `cas-common.sty`; Discrete Applied Mathematics asks for no MSC codes); SIAM `MSCcodes` environment; sn-jnl `\pacs[MSC Classification]{...}` (commented out in the sample; Algorithmica's guide does not mention MSC); the example codes exist (05C40 Connectivity, 05C38 Paths and cycles, 68Q17 Computational difficulty of problems; MSC 2020 list, §8); pick the article's codes from that list, never from memory |
| ACM CCS | none | acmart and LIPIcs `\ccsdesc[weight]{Area~Subarea}` (acmart: required for articles over two pages); concepts from the ACM CCS tool, never invented |
| funding | none (or acknowledgments) | LIPIcs per-author fifth `\author` argument and `\funding{...}`; SIAM `\funding{...}`; acmart `\grantsponsor{id}{name}{url}` + `\grantnum{id}{number}` inside `acks` (all financial support must use them); sn-jnl "Funding" item of the Declarations section; Elsevier journals (DAM card): funders listed in the standard "Funding: ..." form or the recommended no-funding sentence, never invented; others: acknowledgments |
| acknowledgments | `sections/90-acknowledgments.tex`, heading in the wrapper | llncs `credits` environment with `\subsubsection*{\ackname}` and the mandatory `\discintname` paragraph; LIPIcs `\acknowledgements{...}`; acmart `acks` environment (omitted in anonymous mode); IEEEtran `\section*{Acknowledgment}`; cas-sc (Elsevier) `\section*{Acknowledgments}` directly before `\bibliographystyle`; sn-jnl `\backmatter` after the last section, then `\bmhead{Acknowledgements}` (sample spelling; Algorithmica's guide wants them on the title page instead, §6.3); others unnumbered section; keep the text file, change the wrapper |
| statements (data, code, conflicts, AI use) | none | sn-jnl `\section*{Declarations}` after the acknowledgments with the sample's 8 items (Funding; Conflict of interest/Competing interests; Ethics approval and consent to participate; Consent for publication; Data availability; Materials availability; Code availability; Author contribution), an item that does not apply keeps its heading and reads "Not applicable"; the items are text in `sections/92-declarations.tex`, the heading is in the wrapper ([latex-conventions.md](latex-conventions.md) §1); Elsevier: AI declaration as `\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}` before the references ([submission.md](submission.md) §1.3), competing interests and data in the submission system; other venues in the submission system; policy content: [submission.md](submission.md) |

Cells name commands from the class sources and sample files in §8; check the venue's current sample anyway,
classes change.

## 3. Adapting `preamble/`

| Class does | Do in the project | Detect |
|---|---|---|
| loads or embeds `amsmath`, `amsthm`, `amsfonts` (amsart, acmart via amsart, LIPIcs; sn-jnl loads only `amsthm`) | keep the house lines (tested with amsart) unless options clash; sn-jnl: the sample's package block in the wrapper loads them, so `preamble/packages.tex` drops them (§6.2) | "Option clash" error |
| defines theorem environments | delete the theorem block of `preamble/environments.tex`; use the class's names and counters (§6.1); define only the missing ones with the class's mechanism | "Command \theorem already defined" |
| defines `proof` itself (llncs) | `\let\proof\relax \let\endproof\relax` before `\usepackage{amsthm}` (tested), or do not load amsthm | "Command \proof already defined" at `amsthm.sty` |
| defines `problem` (llncs) | `\let\problem\relax \let\endproblem\relax` before `\newtcolorbox{problem}` (tested), or name the box `problembox` | "Command \problem already defined" |
| loads `hyperref` (new-aiaa, LIPIcs, acmart, SIAM, sn-jnl, cas-sc) | delete the `hyperref` line; move options to `\hypersetup`; a package that hyperref adapts to only when it is loaded first (`float`) goes before `\documentclass` as `\RequirePackage{float}` (cas-sc, tested) | "Option clash for package hyperref"; pdfTeX "destination with the same identifier (name{figure.1})" |
| loads `graphicx`, `amsmath`, `amssymb`, `etoolbox` (cas-sc, elsarticle: `graphicx`) | keep the lines in `preamble/packages.tex`: a repeated `\usepackage` without options does nothing, and the preamble then builds under the next class too (article 1 keeps `graphicx`, `amsmath`, `amssymb` since the review of 2026-10-08; deleting them made `\nexists` undefined under `article`); delete a line only when it passes options that clash | "Option clash" error |
| loads `cleveref` or has an option for it (SIAM, LIPIcs) | delete the `cleveref` line; use the class option; keep `\crefname` lines | class warning |
| loads `natbib` (elsarticle, acmart, new-aiaa, sn-jnl) | delete the `natbib` line; options: `\PassOptionsToPackage{sort&compress}{natbib}` before `\documentclass` (tested with elsarticle; its `\biboptions` is read from `main.spl` on the next run) | "Option clash for package natbib" (tested with elsarticle) |
| does not load `hyperref` (elsarticle, amsart, IEEEtran) | `\usepackage[hidelinks]{hyperref}` in the wrapper after `preamble/packages`, as in `templates/article-modular`; elsarticle then fills the PDF title and author from `\title` and `\author` (tested) | `pdfinfo`: empty Title |
| the old class loaded packages that the text uses (new-aiaa: `enumitem`, `microtype`, `setspace`) | list labels: write them as `[(a)]`, which elsarticle and cas-sc read natively and the package `enumerate` gives every other class (`\usepackage{enumerate}` in `preamble/packages.tex` under a class without the syntax); not `enumitem` under elsarticle or cas-sc, whose lists it replaces with `article`'s spacing (a layout override; article 1: 17 pages with enumitem, 16 without) (§6.3); `microtype` in the wrapper after the fonts; delete `\setstretch` lines under a single-spaced class | `pdftotext`: option text such as `label=(a)`; overfull lines |
| forbids packages (LIPIcs: enumitem, paralist, subfig, natbib) | remove them; rewrite list options without enumitem | warning or error in the log |
| sets fonts (new-aiaa, acmart, IEEEtran: Times) | delete `fontenc`/`lmodern` lines from the wrapper; check `\textsc` in bold (problem title) for font warnings | `pdffonts`; "Font shape ... undefined" |
| loads only `fontenc` T1 (elsarticle) | keep `\usepackage{lmodern}`; without it T1 with Computer Modern falls back to Type 3 bitmaps (tested). Latin Modern has no bold and no italic small caps: `\textsc` in the problem-box title and in theorem statements warns `T1/lmr/bx/sc` and `T1/lmr/m/scit` undefined; declare both silently, `\AtBeginDocument{\DeclareFontShape{T1}{lmr}{bx}{sc}{<->ssub*lmr/m/sc}{}\DeclareFontShape{T1}{lmr}{m}{scit}{<->ssub*lmr/m/scsl}{}}` (tested) | `pdffonts`: `Type 3`; "Font shape ... undefined" |
| Roman section numbers (IEEEtran, new-aiaa) | nothing; `\cref` follows ("Theorem I.3", tested) | |

Theorem environments with the house names (`definition`, `theorem`, `lemma`, `claim`, `corollary`, `proposition`,
`remark`, `example`): when the class lacks one, define only the missing ones with the class's mechanism
(`\declaretheorem` if thmtools loads, `\newtheorem` with the class's counter otherwise). Shared counter + cleveref:
[latex-guide.md](latex-guide.md) §6.

## 4. Bibliography style switch

- Copy the venue's `.bst` into the project; set `\bibliographystyle{<venue>}` in the wrapper; delete `natbib`
  options the class sets itself.
- Numeric → author-year: natbib's plain `\cite` then prints the textual form (*Author (2022)*). Map it in the
  wrapper after natbib, `\let\cite\citep` (as `templates/thesis-modular/main.tex` does), so parenthetical citations
  stay parenthetical; then replace each *Names*`~\cite{key}` by `\citet{key}`
  (`grep -nE '[A-Z][a-z]+~\\cite' sections/*.tex`). Nothing else changes: sentences do not use citations as nouns
  ([../bibliography/README.md](../bibliography/README.md) §8). Tested 2026-10-08 in the thesis template.
- biblatex venues (acmart has experimental variants): replace `\bibliographystyle`/`\bibliography` by
  `\usepackage[...]{biblatex}`, `\addbibresource{references.bib}`, `\printbibliography`; delete natbib.
- After the switch: `grep -E "^Warning" outputs/<p>/main.blg` (missing fields the new style needs, e.g., `address`,
  `publisher`), and read the reference list once in the PDF.

## 5. Layout consequences

| Change | Check | Fix |
|---|---|---|
| one column → two columns | figures, tables, algorithms wider than a column; long displays | widths in `\linewidth` survive; wide floats → `figure*`/`table*` (top of page only); split displays with `multline`/`split`; shorten algorithm lines |
| page size / margins | overfull lines, float placement | reword; never shrink fonts or margins (venues forbid it, e.g., LIPIcs) |
| narrower text block (elsarticle `preprint,12pt`: 390 pt against 6.5 in; article 1: 23 → 30 pages) | overfull lines: label columns `p{0.12\linewidth}` of the problem box, `width=145mm` figures, long displays | layout-only edits in `sections/`, no word changes: `p{0.18\linewidth}p{0.75\linewidth}`, `width=\linewidth`, `multline*` or `gather*` for a display (tested); `microtype` for a line over by 1-2 pt; list each edit under "Text in sections/" in the porting log (§7) |
| font change (Times, Libertine) | `pdffonts`, bold small caps, math symbols | remove own font packages; check `\Bbbk`/`\openbox` conflicts ([latex-guide.md](latex-guide.md) §3) |
| displays flush left (LIPIcs `fleqn`) | alignment inside theorems | nothing; do not center displays by hand |
| page limit | `pdfinfo` page count; `-MaxPages` of the packager (§1 step 11) | move proofs to an appendix with restated theorems (`restatable`), if the venue allows appendices |
| Roman section numbers | references read "Section III", "Theorem III.5" | nothing; text never contains hand-typed numbers |

## 6. Class quirks

Sources and dates: §8. "Tested" = build of the article-modular preamble with the class in
`archives/test-evidence/2026-10-08/latex-classtest2/` on 2026-10-08 (pdfLaTeX, MiKTeX 25.12, LaTeX 2025-11-01). Version = `\ProvidesClass`
line of the file read. Cells that were not read or built: TODO(verify).

### 6.1 What the class loads and defines

| Class | Version | Base and packages loaded | Theorem-like environments (counters) | Builds here |
|---|---|---|---|---|
| `llncs` | 2.26 (2025-02-25) | `article[twoside]`; `multicol`, `aliascnt`; nothing else (no hyperref, natbib, amsthm) | `\spnewtheorem`: theorem, claim\*, proof\*, case, conjecture, corollary, definition, example, exercise, lemma, note, problem, property, proposition, question, solution, remark; each its own counter, option `envcountsame`: all on the theorem counter | yes, with `llncs.cls` copied into the project; `splncs04.bst` not installed |
| `lipics-v2021` | 3.1.3 (2023-05-12) | `article[twoside,notitlepage,fleqn]`; T1, microtype, babel, amsmath[tbtags,fleqn], amsthm, hyperref[unicode], caption, subcaption, enumerate, graphicx, tabularx, multirow, rotating, listings, lineno, comment, soul, threeparttable, xstring | theorem, lemma, corollary, proposition, exercise, definition, conjecture, observation, example, note, remark, claim (+ starred note, remark, claim); `proof` redefined, `claimproof`; one `theorem` counter, within sections only with `numberwithinsect` | no: `lineno`, `comment`, `soul`, `threeparttable`, `plainurl.bst` missing |
| `elsarticle` | 3.5 (2026-01-09) | `article`; T1, graphicx, natbib (unless `nonatbib`), geometry (`1p`, `3p`, `5p`); option `times` loads txfonts | none predefined; class adds `\newdefinition`, `\newproof`, `\qed`; the house `\declaretheorem` block works with amsthm (tested) | yes, class generated from `elsarticle.dtx` |
| `cas-sc` (Elsevier CAS bundle; `cas-dc` is the two-column twin) | 2.4 (2024/05/04) | `article` (executes `a4paper,10pt,oneside,fleqn`); graphicx, amsmath, amsfonts, amssymb, expl3, xparse, etoolbox, booktabs, makecell, multirow, array, colortbl, dcolumn, stfloats, xspace, xstring, footmisc, xcolor[svgnames,dvipsnames], hyperref[colorlinks], `cas-common.sty` (moreverb, wrapfig), fontenc T1, stix (text and math; `charis` for text only when `charis.sty` exists), geometry (paper 192 x 262 mm); setspace only with option `review`; no natbib | none predefined; `cas-common.sty` adds `\newdefinition`, `\newproof`, `\qed` and redefines the kernel's `\@begintheorem`; the house `\newtheorem` block with amsthm loaded after the class works (article 1, tested) | yes, with `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` copied from `templates/els-cas/`; MiKTeX packages `makecell`, `sttools`, `moreverb`, `wrapfig`, `colortbl`, `stix`, `grfext`, `cm-super` installed 2026-10-08; Type 1 fonts only (§6.3) |
| `sn-jnl` | template 3.1 (December 2024, zip entries dated 2024-12-13); class header `\ProvidesClass{sn-jnl}[2019/11/18 v0.1]`, not updated for 3.1 | `article[twoside,fleqn]`; geometry (A4, one column, text 31pc x 194.25 mm; option `iicol`: two columns, 160 x 216 mm), cuted, rotating[figuresright], threeparttable, appendix[title], hyperref (`colorlinks`, blue links, citations and URLs), wrapfig, amsthm, fix-cm; breakurl only without option `pdflatex`; natbib with the options of the reference-style option (`sn-mathphys-num`: `numbers,sort&compress`; `apacite` for `sn-apa`); setspace with `\doublespacing` under option `referee`; `vruler` with option `lineno`; `\RequirePackage[T1]{fontenc}` commented out, so OT1 (§6.3); global `\sloppy`, `\frenchspacing`, `\flushbottom`, `\pagestyle{headings}`; no PDF title or author | none predefined; the class defines the theorem *styles* `thmstyleone` (bold head, italic body), `thmstyletwo` (italic head, roman body in the class source; the user manual's "theorem head in Roman font and theorem text in italic style" is wrong), `thmstylethree` (bold head, roman body), `thmstylefour` (proof-like), all with a `\small` body and 18pt above and below; it redefines `\@begintheorem` and, at `\begin{document}`, `proof` (italic "Proof", open square); the sample defines theorem, proposition (`thmstyleone`, proposition on the theorem counter), example, remark (`thmstyletwo`), definition (`thmstylethree`) with `\newtheorem`; the house `\declaretheorem` block with these styles works (article 2, tested) | yes: MiKTeX packages `threeparttable` (class), `jknappen` (`mathrsfs.sty`) and `ncctools` (`manyfoot.sty`) of the sample's package block installed 2026-10-08; `vruler` (option `lineno` only) not installed, untested; the pristine sample builds to 12 pages with Type 1 fonts only (§6.3) |
| `acmart` | 2.20 (2026-08-16) | `amsart[reqno]`; microtype, booktabs, natbib (default), hyperref[bookmarksnumbered,unicode], hyperxmp, graphicx, xcolor, geometry, caption, float, comment, fancyhdr, totpages, framed, pifont, Libertine fonts | theorem, conjecture, proposition, lemma, corollary (style `acmplain`); example, definition (`acmdefinition`); one `theorem` counter; no `remark`; `acmthm=false` suppresses all | no: `hyperxmp`, `totpages`, `comment`, `libertine`, `framed`, `pifont`, `ACM-Reference-Format.bst` missing |
| `IEEEtran` | 1.8b (2015-08-26) | `article`; no package (option `compsoc` loads newtxmath); default fonts Times via `ptm`, `phv`, `pcr` | none predefined (class restyles theorem output); `IEEEproof`; amsthm `proof` works (tested) | yes, with `IEEEtran.cls` copied; psnfss Times fonts missing (§6.3) |
| `amsart` | 2.20.6 (2020-05-29) | amsmath, amsfonts; amsthm code built in, `\usepackage{amsthm}` is harmless | none predefined; `proof`, `\theoremstyle`, `\newtheorem` | yes, installed |
| `siamart251216` | 1.4.8 (2025-12-16) | own layout, no `\LoadClass`; amsmath[leqno], ntheorem, hyperref, xr-hyper, ifpdf, breakurl, xcolor, hypcap, algorithm, cleveref[capitalize,nameinlink]; `lineno` with option `review` | ntheorem: theorem, lemma, corollary, proposition, definition on one `theorem` counter (within sections); `proof`; `\newsiamthm{claim}{Claim}`, `\newsiamremark{remark}{Remark}` for the rest | no: `ntheorem`, `hypcap`, `breakurl`, `lineno`, `siamplain.bst` missing |
| `new-aiaa` | 1.2 (2018-01-10) | `article[10pt]`; T1, inputenc, microtype, newtxtext, newtxmath, geometry, enumitem, footmisc, setspace, abstract, authblk, titlesec, lettrine, caption, quoting, natbib[sort&compress,numbers], url, hyperref | none | yes (article 1 until 2026-10-08) |

### 6.2 Citations, cleveref, and what to change

| Class | Citations and `.bst` | cleveref | Change in the project |
|---|---|---|---|
| `llncs` | own numeric `\cite`; `splncs04.bst` ships with the class; option `citeauthoryear` for author-year; natbib after the class loads (tested) | tested with class environments: "Lemma 2; Theorem 3" under `envcountsame`, "Lemma 1" otherwise | delete the theorem block and the `amsthm` line, or `\let\proof\relax` first; thmtools alone loads and warns "LLNCS support disables automatic casing of theorem names" (tested); box `problem`: §3; add class option `orivec`, else amsmath warns "Unable to redefine math accent \vec" (tested) |
| `lipics-v2021` | plain BibTeX, `\bibliographystyle{plainurl}` mandatory; natbib "not supported", no author-year (sample comments) | class option `cleveref` loads it with `capitalise,noabbrev`; loading it directly gives a class warning | delete amsthm, hyperref, cleveref, natbib, subcaption, enumitem lines and the theorem block; class options `cleveref`, `thm-restate`; `\subjclass` and `\affil` are errors; add `\pdfoutput=1` and `\hideLIPIcs` for arXiv (sample comments) |
| `elsarticle` | natbib loaded by the class: numeric by default, `authoryear` option for round brackets; sample uses `\bibliographystyle{elsarticle-num}` (`elsarticle-num.bst` not installed) | tested: correct names | delete the `natbib` line (else "Option clash for package natbib", tested); keep `lmodern` and declare the small-caps shapes, add `hyperref` (§3); `graphicx` twice is harmless; house theorem block works with amsthm (tested); `\MSC[2020]`; traps: §6.3 |
| `cas-sc` | natbib not loaded by the class; the template's line is `\usepackage[authoryear,longnamesfirst]{natbib}`, its commented alternative `\usepackage[numbers]{natbib}`; `cas-model2-names.bst` (shipped) sorts by author and prints DOIs as `doi:...`; with `numbers` the labels are [1]..[n] in alphabetical order (article 1, tested) | not loaded by the class or the template; untested with cas-sc | wrapper from `cas-sc-template.tex`; numeric venue (DAM): `\usepackage[numbers,sort&compress]{natbib}`; delete the hyperref line; keep graphicx, amsmath, amssymb (the class loads them too; the preamble stays portable, §3), amsthm and the theorem block; list labels as `[(a)]`, no `enumitem` (§6.3, Lists); class-specific lines in the wrapper (§6.3): `\RequirePackage{float}` before `\documentclass`, key `nologo`, the key alias `H` so that figures keep `[H]`, `\begin{abstract}[\abstractname]`, small-caps shapes, `\hypersetup{pdfauthor=...}` after `\maketitle` (article 1 until 2026-10-08: figures `[pos=H]` in `sections/`, `enumitem`, the four packages deleted; changed after the review of 2026-10-08) |
| `sn-jnl` | natbib loaded by the class; the class option (`sn-mathphys-num`, `sn-mathphys-ay`, `sn-basic`, ...) selects natbib's options and sets `\bibliographystyle{sn-...}` itself (`sn-mathphys-num`: `numbers,sort&compress`, `\bibliographystyle{sn-mathphys-num}`), so the wrapper has no `\bibliographystyle`; option `Numbered` switches `sn-basic` and `sn-chicago` to numbers; the `.bst` files are in the template's folder `bst/`: copy the chosen one next to `main.tex` (user manual §8.3; the packager matches it by file name anywhere in the template folder); `sn-mathphys-num.bst` numbers in citation order by default; option `sn-aps` is broken (§6.3) | not loaded by the class or the sample; tested 2026-10-08 (article 2): cleveref `[capitalise,noabbrev]` after the class's hyperref with `\declaretheorem[style=thmstyleone]` (also `thmstyletwo`, `thmstylethree`) prints "Theorem 3.1", "Section 3" | wrapper from `sn-article.tex` with the class options of its active line; keep the sample's standard package block in the wrapper (the user manual says the class depends on these packages; the class's `\email` uses `\textcolor`, the block loads `xcolor`); `preamble/packages.tex` then drops what the block and the class load (amsmath, amssymb, amsthm, graphicx, booktabs, algorithm, algpseudocode); delete the natbib and hyperref lines; theorem block with the class's styles (definition `thmstylethree`; theorem, lemma, claim, corollary, proposition `thmstyleone`; remark, example `thmstyletwo`); `\hypersetup{pdftitle=..., pdfauthor=...}` (the class sets none); T1 encoding and the one-`.tex`-file request: §6.3 |
| `acmart` | natbib with `\citestyle{acmnumeric}` default, `\citestyle{acmauthoryear}`; `ACM-Reference-Format.bst`; biblatex variants experimental | not loaded by the class; with shared counters the class manual says to label with the kind: `\label[lemma]{...}`; TODO(verify) with a build | delete natbib, hyperref and the theorem block; define `remark` after the preamble with `\AtEndPreamble{\theoremstyle{acmdefinition}\newtheorem{remark}[theorem]{Remark}}`; `\ccsdesc` required over two pages |
| `IEEEtran` | own numeric `\cite` ("[1], [2]"); `\bibliographystyle{IEEEtran}` (`IEEEtran.bst` not installed); package `cite` optional | tested: "Section I; Definition I.1; Lemma I.2; Theorem I.3" | the house preamble builds unchanged (tested); fonts: §6.3 |
| `amsart` | numeric via natbib; `amsplain.bst`, `amsalpha.bst` installed | tested: "Definition 1.1; Lemma 1.2; Theorem 1.3" | none: house preamble builds unchanged (tested); `\subjclass[2020]`, abstract before `\maketitle` |
| `siamart251216` | numeric `thebibliography`; `\bibliographystyle{siamplain}`; no natbib | loaded by the class; `\cref` prints "section" in lowercase, `\Cref` "Section", equations as "(1)" without the word (class source) | delete amsthm, thmtools, hyperref, cleveref, natbib lines and the theorem block; define the rest with `\newsiamthm`, `\newsiamremark`; the class comment says `\newtheorem` calls follow cleveref |
| `new-aiaa` | natbib `[sort&compress,numbers]` loaded by the class; `new-aiaa.bst` | tested: "Definition I.1; Lemma I.2; Theorem I.3" | `\let\openbox\relax`, `\let\Bbbk\relax` before the packages; delete hyperref and natbib lines; `\let\enquote\undefined` before `\bibliography` (the `.bst` defines `\enquote`); without these four errors (tested) |

### 6.3 Traps

- **llncs.** `\problem` and `\problemname` exist (house box: §3). Credits go into the `credits` environment, and the
  "Disclosure of Interests" paragraph is mandatory (llncsdoc). `\keywords{a \and b}`, `\orcidID`, `\email`,
  `\institute` are class commands.
- **LIPIcs.** Do not change fonts, margins or the bibliography style; displays are flush left (`fleqn`); packages
  the class loads are not installed here (§6.1), so a build needs the owner's consent for an install (CLAUDE.md rule 6).
- **elsarticle.** `\MSC` defaults to the 2000 scheme. The class source carries a cleveref guard around
  `\fntext`, `\cortext`, `\tnotetext`; tested: cleveref after the class works. Tested 2026-10-08 on article 1 (class
  3.5, `preprint,12pt` as in the sample `elsarticle-template-num.tex`):
  - `\paragraph{Title.}` prints "Title..": the class appends the period (source l.1068-1070). Wrapper patch, keeps
    `sections/` unchanged: `\makeatletter\def\els@aparagraph[#1]#2{\elsparagraph[#1]{#2}}\def\els@bparagraph#1{\elsparagraph*{#1}}\makeatother`
    (the packager does not flag it).
  - The class redefines `enumerate` and `itemize` and reads the optional argument as a label pattern: `[label=(\alph*)]`
    prints `label=(a)` with no warning. Write the label as the pattern `[(a)]` (§3; class source l.1109-1125); `enumitem`
    would replace the class's lists with `article`'s. An old `\setlist` (new-aiaa: labels `1)`) is gone either way, so
    list labels differ from the old PDF.
  - Paper is Letter: `\ExecuteOptions{a4paper,...}` runs before the class's `\DeclareOption*`, so `a4paper` is dropped
    (`\paperwidth` 614 pt; A4: 597 pt). The sample does not pass it; pass `a4paper` on `\documentclass` only when the
    owner or the venue asks for A4.
  - `\affiliation` takes `organization`, `addressline`, `city`, `postcode`, `country`; street and postcode come from
    [../author.md](../author.md) (verified on the institute's contact page 2026-10-08), never from memory. `\ead{}` after
    `\author` prints the address in a footnote; the PDF author field ends with `; `.
  - Without the venue's `.bst`, `\bibliographystyle{plainnat}` (installed) under the class's `numbers` prints `[n]`
    labels sorted alphabetically, with DOIs; with the venue's `.bst` in `templates/<venue>/` the packager flags
    `plainnat` as `[template-bst]` (verdict stays PASS; step 9 allows none): switch to the shipped style (§4).
  - A document with nothing loaded after the class fails with `grfext.sty` not found in this MiKTeX
    ([latex-guide.md](latex-guide.md) §3, note 1): add `\DoNotLoadEpstopdf` before `\documentclass` in test files.
- **cas-sc (Elsevier CAS bundle 2.4).** Tested 2026-10-08 on article 1 (Discrete Applied Mathematics) and on minimal
  documents; every fix below lives in the wrapper or in `sections/` markup, the class files stay byte-identical:
  - **Icons need a sub-folder.** `\ead` prints `thumbnails/cas-email.jpeg`, `\ead[url]` `thumbnails/cas-url.jpeg`
    (and the social-network options their own icons) by a relative path (`cas-common.sty` l.386, l.404); without the
    folder the build stops with `File 'thumbnails/cas-email.jpeg' not found`, also when the icons lie beside the
    main file. Editorial Manager cannot process sub-folders (Elsevier LaTeX instructions, FAQ), and `-Flat` cannot
    rewrite the path inside the pristine `.sty`. The class's own key `nologo` (key set `stm / mktitle`, l.1732)
    replaces the icons by the labels "Email address:" and "URL:"; `cas-sc`'s `\maketitle` takes no option, so the
    wrapper sets the key in the preamble: `\ExplSyntaxOn \keys_set:nn { stm / mktitle } { nologo } \ExplSyntaxOff`.
    No `thumbnails/` folder is then needed. The class documentation (`doc/elsdoc-cas.tex`) does not mention the key.
  - **Abstract is written verbatim.** `abstract` writes its body to `\jobname.abs` with `moreverb`'s
    `\verbatimwrite` and reads it back in `\maketitle`; its optional argument (heading; stored in `\abstracttitle`,
    which nothing prints) is looked for first, which tokenizes the first item of the body: a command there
    (`\input{sections/00-abstract}`) is lost and the abstract prints "sections/00-abstract". A blank first line is
    an error ("Paragraph ended before \verbatim@start"). Fix: `\begin{abstract}[\abstractname]` (the class's own
    heading as the documented optional argument, `doc/elsdoc-cas.tex` l.211).
  - **Float options are key-value.** `figure` and `table` take `[pos=..., width=..., ...]`; a plain `[H]` or `[t]` is
    an unknown key (tested with `[H]`; `[t]` takes the same code path, key set `cas / fig`, `cas-common.sty` l.2193-2213), the class stores
    an empty placement (log: "No positions in optional float specifier. Default
    added", followed by an empty specifier) and every such float waits until the end of the document. Keep the
    standard `[H]` in `sections/` and declare `H` in the wrapper as a short form of the class's own key:
    `\ExplSyntaxOn \keys_define:nn { cas / fig } { H .meta:n = { pos = H } } \ExplSyntaxOff` (with `float`; article 1
    since 2026-10-09: the figures stay where they are written and the PDF text keeps the order it had with `[pos=H]`
    in `sections/`, which the port of 2026-10-08 used). Other placements and tables (key set `cas / tbl`) presumably
    work the same way (untested), or use `[pos=tb]` in `sections/` as a layout-only edit listed in the porting log
    (line "Venue-only markup"). Algorithms (`algorithm` of `float`) keep `[H]`.
  - **float after hyperref.** The class loads `hyperref`, which adapts to `float` only when `float` is loaded before
    it; loaded later, every figure anchor is written twice ("destination with the same identifier (name{figure.1})").
    Put `\RequirePackage{float}` before `\documentclass`; a later `\usepackage{float}` is then a no-op.
  - **Lists.** `enumerate` and `itemize` are redefined (`cas-common.sty` l.2491-2535): an optional argument is read as
    a label pattern (`[(a)]`), so `[label=(\alph*)]` prints garbage without a warning. Write the label as `[(a)]`
    (the class's documented syntax, `cas-sc-template.tex`; §3), not `enumitem`, whose lists replace the class's spacing
    (a layout override: article 1 had 17 pages with enumitem, 16 with the class's lists, 2026-10-09).
  - **Fonts.** `charis.sty` exists in no MiKTeX package (`charissil` ships `CharisSIL.sty`), so the class takes its
    `stix` branch: STIX text and math, as in the publisher's `cas-sc-sample.pdf`. STIX has no italic small caps:
    `\textsc` in theorem statements and in italic headings warns `T1/stix/m/scit` and `T1/stix/b/scit` undefined;
    declare the substitution the font system makes anyway:
    `\AtBeginDocument{\DeclareFontShape{T1}{stix}{m}{scit}{<->ssub*stix/m/sc}{}\DeclareFontShape{T1}{stix}{b}{scit}{<->ssub*stix/b/sc}{}}`
    (tested; the `.fd` is loaded by then). Captions, the running head and the author name in the footer are set in
    `\sffamily` (T1 Computer Modern sans) and `\ead`, DOIs and URLs in `cmtt` (the class's `inconsolata` test has no file extension and
    never succeeds): these need the MiKTeX package `cm-super` (installed 2026-10-08; article 1 and the pristine
    template then have Type 1 fonts only). Without it they are Type 3 bitmaps (packager `[fonts]`) and `pdftotext`
    turns `ľ` in the footer into `©`.
  - **PDF metadata.** `\title` sets the PDF title; `\maketitle` sets the author to the author list followed by `, `,
    which shows as a stray character, and the subject to "Complex STM Content". Set
    `\hypersetup{pdfauthor={...}}` after `\maketitle` (before it, the class overwrites it).
  - **Class artefacts, also in the build of the pristine `cas-sc-template.tex`:** `Overfull \hbox (117.0831pt too
    wide)` and three `hyperref` "Ignoring empty anchor" at `\maketitle` (the front-matter box; nothing visible); an
    "ORCID(s):" footnote line printed even when no author has an ORCID (`\printorcid`, `cas-common.sty` l.425-435,
    has no condition and no key; the only switch that drops it, blind mode, also hides the authors and e-mails, so
    leave the line: rechecked 2026-10-08); the keyword box does not reserve height, so
    keywords taller than the abstract overlap the first heading.
  - **Layout.** Paper 192 x 262 mm from the class's `geometry` call (the `a4paper` option of the sample changes
    nothing); arabic section numbers ("Theorem 3.5"); `\paragraph` is an italic run-in heading without an added
    period (unlike elsarticle); captions "Figure 1:" in small sans-serif; footer "Preprint submitted to Elsevier"
    and "Page n of N". Option `longmktitle` when the front matter runs over one page.
- **sn-jnl (Springer Nature journal template 3.1).** Tested 2026-10-08 on the pristine sample (copy with
  `sn-mathphys-num.bst` beside `sn-article.tex`) and on article 2 (Algorithmica, [../venues/algorithmica.md](../venues/algorithmica.md));
  the class files stay byte-identical, every fix lives in the wrapper:
  - **One `.tex` file.** The sample's header says "Submit your LaTeX manuscript as one .tex document" and asks not to
    use `\input`; the user manual and Algorithmica's guide do not state the rule. The packager's `-Flat` gives one
    directory, not one file, and nothing here inlines the `\input` lines (`latexpand` is a stub:
    [latex-guide.md](latex-guide.md) §15). Open: ask the owner before the first submission; the packaged copy is never
    edited by hand ([latex-conventions.md](latex-conventions.md) §1.1).
  - **Font encoding.** The class leaves `\RequirePackage[T1]{fontenc}` commented out, so the encoding is OT1:
    `Miche\v{l}` prints an "l" with a caron above instead of "ľ", and `pdftotext` loses every accent ("Michel",
    "Saf´arik"). Article 2 adds `\usepackage[T1]{fontenc}` after the sample's package block: the typeface stays
    Computer Modern (Type 1 from `cm-super`), "Micheľ" prints and the PDF text keeps the accents (tested). The user
    manual asks for no custom fonts; T1 changes the encoding only. Diacritics go into the source as TeX code
    (`Miche\v{l}`, `Ko\v{s}ice`), as Springer Nature's LaTeX author-support page asks.
  - **Double spacing for review.** The user manual asks for double line spacing, option `[referee]`, "for the peer
    review and editorial stages". The sample's active class line does not use it and Algorithmica's guide does not
    mention it: the owner decides at submission. `referee` loads `setspace` with `\doublespacing`; `lineno` loads
    `vruler` (not installed).
  - **Spacing.** The class sets `\sloppy`, `\frenchspacing` and `\flushbottom` globally (class source l.1487-1489);
    the sample adds `\raggedbottom` after its theorem lines. Leave them, and check interword spacing in the PDF.
  - **Option `sn-aps` is broken.** It sets `\bibliographystyle{sn-APS}`, but the file is `sn-aps.bst`: BibTeX
    fails on a case-sensitive system.
  - **Line endings.** `sn-jnl.cls` has CR-only line endings, so `grep` reads it as one line: search a converted copy
    (`tr '\r' '\n' < sn-jnl.cls`); the class line numbers cited here count lines of that copy. `sn-article.tex`,
    `sn-bibliography.bib`, `sn-apacite.bst` and `sn-nature.bst` have CRLF, the other `.bst` and the `.eps` files LF.
    The workspace `.gitattributes` (`* text=auto`) with `core.autocrlf=true` may rewrite LF and CRLF on commit and
    checkout (a lone CR stays), as for `templates/els-cas/`; the template is not committed yet, so whether the
    packager's byte comparison still passes after a checkout: TODO(verify).
  - **Bibliography.** The publisher's `sn-article.pdf` prints author-year citations ("Campbell and Gear (1995)"), so it
    was not made with the sample's active `sn-mathphys-num` line: compare with a local build of the sample, not with
    that PDF. While nothing is cited, natbib warns "Empty `thebibliography' environment" and BibTeX reports one error
    (no `\citation` commands); both disappear with the first citation. `sn-mathphys-num.bst` numbers in citation
    order; its header names an `alpha` option for alphabetical order, set without editing the file by an `@settings`
    entry with `options = "alpha"` (needs `\nocite` of that entry; untested). Which order Algorithmica wants:
    TODO(verify) on the venue card.
  - **Figures.** The user manual asks for image files "on the same level as your LaTeX document" and no subfigures,
    and says the compiler "accepts only .eps": old wording, since `pdflatex` is the default option from 3.1 on and the
    sample's `fig.eps` is converted to PDF during the pdfLaTeX build (`epstopdf`, sample build log). `img/` stays in
    the project; `-Flat` puts every file into one directory and rewrites the paths. Which figure formats Algorithmica
    accepts from a pdfLaTeX source: TODO(verify) on the venue card. `\orcid{URL}` (class source l.1796-1800) is a link
    around `\includegraphics{Orcidlogo.eps}`, a file the zip does not contain (`templates/sn-jnl/` holds its 16
    files).
  - **float after hyperref.** The pristine sample shows pdfTeX "destination with the same identifier" once per float
    (`table.1` to `table.3`, `figure.1`): the sample's `algorithm` loads `float` after the class's `hyperref`, the
    cas-sc case above. `\RequirePackage{float}` before `\documentclass` removes it (tested 2026-10-09 on a copy of
    article 2 with a figure, a table and an algorithm: without the line `figure.1` and `table.1` are written twice,
    with it no such warning; `\cref` reads "Figure 1, Table 1, and Algorithm 1"); article 2's wrapper has the line.
    Captions print "Fig. 1" (class), `\cref` "Figure 1".
  - **Class artefacts, also in the build of the pristine sample** (12 pages, A4, Type 1 fonts only): `U/rsfs/m/n`
    size substitutions (from `mathrsfs` of the sample's package block), "Font shape `OMS/cmss/m/n' undefined",
    "`h' float specifier changed to `ht'", "No positions in optional float specifier", `Overfull \hbox` of 7.56pt
    (sample lines 395-407), hyperref "Difference (4) between bookmark levels". Article 2 shows the `rsfs` and
    bookmark warnings.
  - **Front and back matter.** The class sets no PDF title or author: `\hypersetup{pdftitle=..., pdfauthor=...}` in
    the wrapper. The template puts the acknowledgments into the back matter (`\bmhead`); Algorithmica's guide wants
    them "in a separate section on the title page": a conflict whose editorial preference is unknown; article 2
    follows the template.
  - **Author-support page.** No custom fonts; diacritics as TeX code; "All files should be included in a single
    directory"; `\includegraphics` with the local path only; `graphicx` without the `dvips` option. Its sentence
    on pdfLaTeX and a `.zip` upload names "Snapp", a system the page does not identify; Algorithmica submits through
    the Springer Nature Article Processing Platform (https://submission.nature.com/), which "Compiles files to PDF
    via TexLive 2021". Its `.bbl` rules are stated for Editorial Manager and eJP only ([submission.md](submission.md) §3.1).
- **acmart.** In anonymous mode `acks` must be omitted; funding goes through `\grantsponsor`/`\grantnum`; a build
  needs many packages that are not installed here.
- **IEEEtran.** The class sets Times through psnfss (`\rmdefault{ptm}`, class source l.495), and this MiKTeX has no
  `times.sty`, `ot1ptm.fd`, `t1ptm.fd`: the build warns "Font shape OT1/ptm/m/n undefined" and falls back to Computer
  Modern; with T1 the output is Type 3 bitmaps (tested). `\usepackage{newtxtext,newtxmath}` after the house packages
  gives Type 1 Times-like fonts (TeX Gyre Termes, tested) with five remaining warnings from the class's own font
  selection; whether IEEE accepts newtx in a submission: TODO(verify). Alternative: ask the owner to install `psnfss`.
- **new-aiaa.** Roman section numbers; class option `journal` sets double spacing, so algorithms need
  `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (article 1 until 2026-10-08).
- **siamart.** The class builds theorems with `ntheorem`, not `amsthm`, so the house `\declaretheorem` block
  cannot stay; whether thmtools or amsthm can be loaded next to `ntheorem`: TODO(verify) (no build possible here).
  Option `review` needs `lineno`; `\orcid` is accepted but prints nothing.

## 7. Porting log (copy into the project README, Change history)

```markdown
**YYYY-MM-DD - ported to <venue> (<class> <version>)**
- Template: `templates/<venue>/` from <URL or inbox file>, `\ProvidesClass` line: <...>.
- Wrapper: new `main.tex` from `<sample file>`; old wrapper archived at
  `archives/removed-from-projects/<project>/main-before-port-YYYY-MM-DD.tex`.
- Front matter: title, authors, affiliation, ORCID, abstract, keywords, <MSC/CCS>, funding, acknowledgments mapped.
- preamble/: removed <packages/environments> (class provides them); renamed <...>; added <...>.
- Bibliography: <old style> → <new style>; BibTeX/biber warnings: <none | list>.
- Layout: <two-column fixes, figure*/table*, split displays>.
- Build: <pages before> → <pages after> pages; undefined refs 0; overfull <n>; remaining warnings: <list>.
- Template checklist: <items done / open>.
- Package: `package-project.ps1 -Template <venue> <other switches>`: Verdict <PASS | FAIL>; `[layout]`: <none | kept, with reason>.
- Text in sections/: unchanged | changed only <\ref→\cref on the owner's request; Names~\cite→\citet for the author-year style; layout-only edits, one per file and line: column fractions, figure widths, split displays>.
- Venue-only markup (undo at the next port, §1 step 2): <none | file, line, markup and its standard form, e.g. `[pos=tb]` → `[tb]`; packages dropped from preamble/ because the class loads them>.
```

## 8. Sources

Opened 2026-10-08. `CTAN:` = mirror `https://ctan.gust.org.pl/tex-archive/`.

| Class | Source read |
|---|---|
| llncs 2.26 | `CTAN:macros/latex/contrib/llncs/llncs.cls`, `llncsdoc.tex` |
| lipics-v2021 3.1.3 | https://raw.githubusercontent.com/dagstuhl-publishing/styles/master/LIPIcs/authors/lipics-v2021.cls and `lipics-v2021-sample-article.tex` (same folder; read through a page-summary tool, so cell wording is a summary), `lipics-v2021-authors-guidelines.pdf` |
| elsarticle 3.5 | `CTAN:macros/latex/contrib/elsarticle/elsarticle.dtx`, `elsarticle-template-num.tex`; class generated from the `.dtx` for the tests (the publisher's download in `templates/elsarticle/` is version 3.4, 2024/04/04: `templates/SOURCES.tsv`) |
| cas-sc 2.4 | `templates/els-cas/` (Elsevier CAS bundle 2.4 from `els-cas-templates.zip`, linked as "LaTeX template" from the Discrete Applied Mathematics guide for authors; URLs and SHA-256 in `templates/SOURCES.tsv`): `cas-sc.cls`, `cas-common.sty`, `cas-sc-template.tex`, `cas-sc-sample.tex`, `doc/elsdoc-cas.tex`; Elsevier [LaTeX instructions](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions) (FAQ on sub-folders, item types); tests: port of article 1 (porting log in `projects/clanok-1-min-cut-path/README.md`) and minimal documents, 2026-10-08 |
| sn-jnl (template 3.1) | `templates/sn-jnl/` (Springer Nature journal article template package, December 2024 version, linked from https://www.springernature.com/gp/authors/campaigns/latex-author-support, the page the Algorithmica submission guidelines link; zip URL and SHA-256 in `templates/SOURCES.tsv`): `sn-jnl.cls` (searched in a copy with converted line endings, §6.3), `sn-article.tex`, `user-manual.pdf` (Straive TeX Support, read in full), `bst/sn-mathphys-num.bst`; tests: build of the pristine sample and the port of article 2 (porting log in `projects/clanok-2-min-cut-path/README.md`), 2026-10-08 |
| acmart 2.20 | `CTAN:macros/latex/contrib/acmart/acmart.dtx` (user guide and implementation) |
| IEEEtran 1.8b | `CTAN:macros/latex/contrib/IEEEtran/IEEEtran.cls`, `bare_jrnl.tex` |
| amsart 2.20.6 | local `tex/latex/amscls/amsart.cls` (MiKTeX); `CTAN:macros/latex/required/amscls/doc/amsclass.pdf` |
| siamart251216 1.4.8 | https://epubs.siam.org/journal-authors (section SIAM LaTeX Macros/Templates): `siamart251216.cls`, `ex_article.tex` under https://epubs.siam.org/pb-assets/macros/standard/ |
| new-aiaa 1.2 | `templates/new-aiaa/new-aiaa.cls` |
| MSC 2020 codes | https://msc2020.org/MSC_2020.csv (full list, tab-separated) |
| availability of packages and `.bst` files | `kpsewhich --miktex-disable-installer`, 2026-10-08 |
| tests | `archives/test-evidence/2026-10-08/latex-classtest2/` (harness `make-and-run.ps1`, one folder per variant) |
