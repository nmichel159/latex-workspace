# Porting a manuscript to a journal or conference template

Procedure for moving a project built from `templates/article-modular` (or article 1) into a venue's class.
Operational checklist for Claude: skill `port-latex-template`. House rules: [latex-conventions.md](latex-conventions.md);
package craft: [latex-guide.md](latex-guide.md); venue facts (page limits, anonymity, AI policy):
[../venues/README.md](../venues/README.md); submission package: [submission.md](submission.md).

Only `main.tex` and the class files depend on the venue. `sections/`, `img/` and `references.bib` move unchanged
(exceptions: citation commands under an author-year style, §4; layout-only edits that a narrower text block forces,
§5); `preamble/` loses the lines the class provides and regains the ones the old class provided (§3).

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
   `archives/removed-from-projects/<project>/main-before-port-<YYYY-MM-DD>.tex`.
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
6. **Adapt `preamble/`** (§3): remove what the class loads or defines, rename what clashes, keep the load order.
   List what the *old* class loaded (`Select-String -Pattern RequirePackage <old>.cls`) and keep what the sections use
   of it (new-aiaa: `enumitem`, `microtype`); a missing one shows no warning, only option text or overfull lines in
   the output (§3).
7. **Bibliography**: copy the venue's style, switch `\bibliographystyle` to a style the template ships (or the
   biblatex options). A numeric venue: the source keeps plain `\cite`, nothing else changes. An author-year venue:
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
| title, short title | `\title{\PaperTitle}` | `\title[short]{long}`: acmart, amsart, sn-jnl; llncs `\titlerunning{short}`; LIPIcs `\titlerunning{short}` (only when the title exceeds one line); SIAM `\headers{short title}{authors}` |
| authors, affiliations | `\author{...}` with `\\` lines | llncs `\author{A\inst{1} \and B\inst{2}}` + `\institute{I$_1$ \and I$_2$}`, `\authorrunning`; LIPIcs `\author{name}{affiliation}{email}{ORCID URL}{funding}` once per author, `\authorrunning`, `\Copyright`; elsarticle `\author[l1]{}` + `\affiliation[l1]{organization=,addressline=,city=,postcode=,country=}` inside `frontmatter`; sn-jnl `\author*[1,2]{\fnm{} \sur{}}\email{}` + `\affil*[1]{\orgdiv{}\orgname{}\orgaddress{}}`; acmart per author `\author{}`, `\orcid{}`, `\affiliation{\institution{}\city{}\country{}}`, `\email{}` (institution, city, country mandatory); IEEEtran `\author{Name,~\IEEEmembership{...}}` with `\thanks{affiliation}`; SIAM `\author{...\thanks{}}` joined by `\and`, `\email{}`; amsart `\author{}` + `\address{}`, `\email{}`, `\urladdr{}` (printed at the end of the article) |
| full affiliation | Institute of Computer Science, Faculty of Science, Pavol Jozef Šafárik University in Košice ([../author.md](../author.md)) | as above |
| ORCID | none | llncs `\orcidID{...}` after the name; LIPIcs fourth `\author` argument; acmart `\orcid{...}`; SIAM `\orcid{}` is accepted and prints nothing; sn-jnl `\orcid{URL}` (needs `Orcidlogo.eps`, §6.3); elsarticle, IEEEtran, amsart: no command in the class source or sample; use `\orcidlink` (package `orcidlink`, installed) after the name or the submission form |
| abstract | `sections/00-abstract.tex` inside `abstract` | `abstract` environment in all classes; sn-jnl `\abstract{...}` as a command; amsart: before `\maketitle`; elsarticle: inside `frontmatter` |
| keywords | manual `\noindent\textbf{Keywords:}` line | llncs `\keywords{A \and B}` inside the `abstract` environment, after the `\input`; LIPIcs, acmart, sn-jnl, amsart `\keywords{...}`; elsarticle `keyword` environment with `\sep`; IEEEtran `IEEEkeywords` environment; SIAM `keywords` environment |
| MSC 2020 | none | amsart `\subjclass[2020]{05C40, 68Q17}`; elsarticle `\MSC[2020] code \sep code` (default is 2000); SIAM `MSCcodes` environment; sn-jnl `\pacs[MSC Classification]{...}`; the example codes exist (05C40 Connectivity, 05C38 Paths and cycles, 68Q17 Computational difficulty of problems; MSC 2020 list, §8); pick the article's codes from that list, never from memory |
| ACM CCS | none | acmart and LIPIcs `\ccsdesc[weight]{Area~Subarea}` (acmart: required for articles over two pages); concepts from the ACM CCS tool, never invented |
| funding | none (or acknowledgments) | LIPIcs per-author fifth `\author` argument and `\funding{...}`; SIAM `\funding{...}`; acmart `\grantsponsor{id}{name}{url}` + `\grantnum{id}{number}` inside `acks` (all financial support must use them); sn-jnl "Funding" item of the Declarations section; others: acknowledgments |
| acknowledgments | `sections/90-acknowledgments.tex`, heading in the wrapper | llncs `credits` environment with `\subsubsection*{\ackname}` and the mandatory `\discintname` paragraph; LIPIcs `\acknowledgements{...}`; acmart `acks` environment (omitted in anonymous mode); IEEEtran `\section*{Acknowledgment}`; others unnumbered section; keep the text file, change the wrapper |
| statements (data, code, conflicts, AI use) | none | sn-jnl `\section*{Declarations}` with fixed items; other venues in the submission system; policy content: [submission.md](submission.md) |

Cells name commands from the class sources and sample files in §8; check the venue's current sample anyway,
classes change.

## 3. Adapting `preamble/`

| Class does | Do in the project | Detect |
|---|---|---|
| loads or embeds `amsmath`, `amsthm`, `amsfonts` (amsart, acmart via amsart, LIPIcs, sn-jnl) | keep the house lines (tested with amsart) unless options clash | "Option clash" error |
| defines theorem environments | delete the theorem block of `preamble/environments.tex`; use the class's names and counters (§6.1); define only the missing ones with the class's mechanism | "Command \theorem already defined" |
| defines `proof` itself (llncs) | `\let\proof\relax \let\endproof\relax` before `\usepackage{amsthm}` (tested), or do not load amsthm | "Command \proof already defined" at `amsthm.sty` |
| defines `problem` (llncs) | `\let\problem\relax \let\endproblem\relax` before `\newtcolorbox{problem}` (tested), or name the box `problembox` | "Command \problem already defined" |
| loads `hyperref` (new-aiaa, LIPIcs, acmart, SIAM, sn-jnl) | delete the `hyperref` line; move options to `\hypersetup` | "Option clash for package hyperref" |
| loads `cleveref` or has an option for it (SIAM, LIPIcs) | delete the `cleveref` line; use the class option; keep `\crefname` lines | class warning |
| loads `natbib` (elsarticle, acmart, new-aiaa, sn-jnl) | delete the `natbib` line; options: `\PassOptionsToPackage{sort&compress}{natbib}` before `\documentclass` (tested with elsarticle; its `\biboptions` is read from `main.spl` on the next run) | "Option clash for package natbib" (tested with elsarticle) |
| does not load `hyperref` (elsarticle, amsart, IEEEtran) | `\usepackage[hidelinks]{hyperref}` in the wrapper after `preamble/packages`, as in `templates/article-modular`; elsarticle then fills the PDF title and author from `\title` and `\author` (tested) | `pdfinfo`: empty Title |
| the old class loaded packages that the text uses (new-aiaa: `enumitem`, `microtype`, `setspace`) | `\usepackage{enumitem}` in `preamble/packages.tex` when the text uses `[label=...]` (elsarticle redefines `enumerate` and prints the option as text, §6.3); `microtype` in the wrapper after the fonts; delete `\setstretch` lines under a single-spaced class | `pdftotext`: option text; overfull lines |
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
| `sn-jnl` | template 3.1 (2024-12); class header `\ProvidesClass{sn-jnl}[2019/11/18 v0.1]` | `article[twoside,fleqn]`; setspace, geometry, cuted, rotating, threeparttable, appendix, hyperref, wrapfig, amsthm, fix-cm; natbib with the options of the chosen reference style (`apacite` for `sn-apa`); `vruler` with option `lineno`; global `\sloppy` and `\frenchspacing` | the class defines the theorem *styles* `thmstyleone` ... `thmstylefour`; the sample defines theorem, proposition (`thmstyleone`), example, remark (`thmstyletwo`), definition (`thmstylethree`) with `\newtheorem` | no: `wrapfig`, `cuted`, `threeparttable` (class), `manyfoot`, `mathrsfs` (sample) missing |
| `acmart` | 2.20 (2026-08-16) | `amsart[reqno]`; microtype, booktabs, natbib (default), hyperref[bookmarksnumbered,unicode], hyperxmp, graphicx, xcolor, geometry, caption, float, comment, fancyhdr, totpages, framed, pifont, Libertine fonts | theorem, conjecture, proposition, lemma, corollary (style `acmplain`); example, definition (`acmdefinition`); one `theorem` counter; no `remark`; `acmthm=false` suppresses all | no: `hyperxmp`, `totpages`, `comment`, `libertine`, `framed`, `pifont`, `ACM-Reference-Format.bst` missing |
| `IEEEtran` | 1.8b (2015-08-26) | `article`; no package (option `compsoc` loads newtxmath); default fonts Times via `ptm`, `phv`, `pcr` | none predefined (class restyles theorem output); `IEEEproof`; amsthm `proof` works (tested) | yes, with `IEEEtran.cls` copied; psnfss Times fonts missing (§6.3) |
| `amsart` | 2.20.6 (2020-05-29) | amsmath, amsfonts; amsthm code built in, `\usepackage{amsthm}` is harmless | none predefined; `proof`, `\theoremstyle`, `\newtheorem` | yes, installed |
| `siamart251216` | 1.4.8 (2025-12-16) | own layout, no `\LoadClass`; amsmath[leqno], ntheorem, hyperref, xr-hyper, ifpdf, breakurl, xcolor, hypcap, algorithm, cleveref[capitalize,nameinlink]; `lineno` with option `review` | ntheorem: theorem, lemma, corollary, proposition, definition on one `theorem` counter (within sections); `proof`; `\newsiamthm{claim}{Claim}`, `\newsiamremark{remark}{Remark}` for the rest | no: `ntheorem`, `hypcap`, `breakurl`, `lineno`, `siamplain.bst` missing |
| `new-aiaa` | 1.2 (2018-01-10) | `article[10pt]`; T1, inputenc, microtype, newtxtext, newtxmath, geometry, enumitem, footmisc, setspace, abstract, authblk, titlesec, lettrine, caption, quoting, natbib[sort&compress,numbers], url, hyperref | none | yes (article 1) |

### 6.2 Citations, cleveref, and what to change

| Class | Citations and `.bst` | cleveref | Change in the project |
|---|---|---|---|
| `llncs` | own numeric `\cite`; `splncs04.bst` ships with the class; option `citeauthoryear` for author-year; natbib after the class loads (tested) | tested with class environments: "Lemma 2; Theorem 3" under `envcountsame`, "Lemma 1" otherwise | delete the theorem block and the `amsthm` line, or `\let\proof\relax` first; thmtools alone loads and warns "LLNCS support disables automatic casing of theorem names" (tested); box `problem`: §3; add class option `orivec`, else amsmath warns "Unable to redefine math accent \vec" (tested) |
| `lipics-v2021` | plain BibTeX, `\bibliographystyle{plainurl}` mandatory; natbib "not supported", no author-year (sample comments) | class option `cleveref` loads it with `capitalise,noabbrev`; loading it directly gives a class warning | delete amsthm, hyperref, cleveref, natbib, subcaption, enumitem lines and the theorem block; class options `cleveref`, `thm-restate`; `\subjclass` and `\affil` are errors; add `\pdfoutput=1` and `\hideLIPIcs` for arXiv (sample comments) |
| `elsarticle` | natbib loaded by the class: numeric by default, `authoryear` option for round brackets; sample uses `\bibliographystyle{elsarticle-num}` (`elsarticle-num.bst` not installed) | tested: correct names | delete the `natbib` line (else "Option clash for package natbib", tested); keep `lmodern` and declare the small-caps shapes, add `hyperref` (§3); `graphicx` twice is harmless; house theorem block works with amsthm (tested); `\MSC[2020]`; traps: §6.3 |
| `sn-jnl` | natbib loaded by the class; the class option (`sn-mathphys-num`, `sn-mathphys-ay`, `sn-basic`, ...) selects natbib options and `\bibliographystyle{sn-...}`; the `.bst` files are in the zip folder `bst/` | not loaded by the class or sample; TODO(verify) with a build | delete the natbib, hyperref and amsthm lines (the class loads them); copy the sample's theorem lines (or define the house environments with the class's styles); one `.tex` file only (§6.3) |
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
    prints `label=(a)` with no warning. Load `enumitem` (§3); the lists then follow `article`, and an old `\setlist`
    (new-aiaa: labels `1)`) is gone, so list labels differ from the old PDF.
  - Paper is Letter: `\ExecuteOptions{a4paper,...}` runs before the class's `\DeclareOption*`, so `a4paper` is dropped
    (`\paperwidth` 614 pt; A4: 597 pt). The sample does not pass it; pass `a4paper` on `\documentclass` only when the
    owner or the venue asks for A4.
  - `\affiliation` takes `organization`, `addressline`, `city`, `postcode`, `country`; [../author.md](../author.md) has
    no street or postcode: leave those keys out and list them as open items, never invent them. `\ead{}` after
    `\author` prints the address in a footnote; the PDF author field ends with `; `.
  - Without the venue's `.bst`, `\bibliographystyle{plainnat}` (installed) under the class's `numbers` prints `[n]`
    labels sorted alphabetically, with DOIs; with the venue's `.bst` in `templates/<venue>/` the packager flags
    `plainnat` as `[template-bst]` (verdict stays PASS; step 9 allows none): switch to the shipped style (§4).
  - A document with nothing loaded after the class fails with `grfext.sty` not found in this MiKTeX
    ([latex-guide.md](latex-guide.md) §3, note 1): add `\DoNotLoadEpstopdf` before `\documentclass` in test files.
- **sn-jnl.** The sample states: "Submit your LaTeX manuscript as one .tex document" and "do not use `\input`". The
  packager's `-Flat` gives one directory, not one file, and nothing here inlines the `\input` lines (`latexpand` is a
  stub: [latex-guide.md](latex-guide.md) §15). Whether the journal's system enforces the sentence: TODO(verify) on the
  venue card. If it does, ask the owner before the first such submission; the packaged copy is never edited by hand
  ([latex-conventions.md](latex-conventions.md) §1.1). The class sets `\sloppy` and `\frenchspacing` globally (class source l.1487-1488): leave them, and
  check spacing. `\orcid{URL}` is defined but needs `Orcidlogo.eps`, which the zip does not contain. The authors page
  asks for pdfLaTeX, no custom fonts, `graphicx` without the `dvips` option, and a `.zip` upload.
- **acmart.** In anonymous mode `acks` must be omitted; funding goes through `\grantsponsor`/`\grantnum`; a build
  needs many packages that are not installed here.
- **IEEEtran.** The class sets Times through psnfss (`\rmdefault{ptm}`, class source l.495), and this MiKTeX has no
  `times.sty`, `ot1ptm.fd`, `t1ptm.fd`: the build warns "Font shape OT1/ptm/m/n undefined" and falls back to Computer
  Modern; with T1 the output is Type 3 bitmaps (tested). `\usepackage{newtxtext,newtxmath}` after the house packages
  gives Type 1 Times-like fonts (TeX Gyre Termes, tested) with five remaining warnings from the class's own font
  selection; whether IEEE accepts newtx in a submission: TODO(verify). Alternative: ask the owner to install `psnfss`.
- **new-aiaa.** Roman section numbers; class option `journal` sets double spacing, so algorithms need
  `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (article 1).
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
```

## 8. Sources

Opened 2026-10-08. `CTAN:` = mirror `https://ctan.gust.org.pl/tex-archive/`.

| Class | Source read |
|---|---|
| llncs 2.26 | `CTAN:macros/latex/contrib/llncs/llncs.cls`, `llncsdoc.tex` |
| lipics-v2021 3.1.3 | https://raw.githubusercontent.com/dagstuhl-publishing/styles/master/LIPIcs/authors/lipics-v2021.cls and `lipics-v2021-sample-article.tex` (same folder; read through a page-summary tool, so cell wording is a summary), `lipics-v2021-authors-guidelines.pdf` |
| elsarticle 3.5 | `CTAN:macros/latex/contrib/elsarticle/elsarticle.dtx`, `elsarticle-template-num.tex`; class generated from the `.dtx` for the tests |
| sn-jnl | Springer Nature journal template ZIP (v3.1, December 2024; link "Journal template ZIP" on https://www.springernature.com/gp/authors/campaigns/latex-author-support): `sn-jnl.cls`, `sn-article.tex` read in memory; Overleaf copy of the sample, https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq |
| acmart 2.20 | `CTAN:macros/latex/contrib/acmart/acmart.dtx` (user guide and implementation) |
| IEEEtran 1.8b | `CTAN:macros/latex/contrib/IEEEtran/IEEEtran.cls`, `bare_jrnl.tex` |
| amsart 2.20.6 | local `tex/latex/amscls/amsart.cls` (MiKTeX); `CTAN:macros/latex/required/amscls/doc/amsclass.pdf` |
| siamart251216 1.4.8 | https://epubs.siam.org/journal-authors (section SIAM LaTeX Macros/Templates): `siamart251216.cls`, `ex_article.tex` under https://epubs.siam.org/pb-assets/macros/standard/ |
| new-aiaa 1.2 | `templates/new-aiaa/new-aiaa.cls` |
| MSC 2020 codes | https://msc2020.org/MSC_2020.csv (full list, tab-separated) |
| availability of packages and `.bst` files | `kpsewhich --miktex-disable-installer`, 2026-10-08 |
| tests | `archives/test-evidence/2026-10-08/latex-classtest2/` (harness `make-and-run.ps1`, one folder per variant) |
