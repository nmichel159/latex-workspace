# Article 2 - Min Cut-Path (template ready, no text yet)

**Layout since 2026-10-09: the folder is what is sent.** `projects/clanok-2-min-cut-path/` holds four files and no
sub-folders: `main.tex` (the template's sample `sn-article.tex` with the content places filled in, one file, no
`\input`), `sn-jnl.cls`, `sn-mathphys-num.bst` (byte-identical to `templates/sn-jnl/`) and `references.bib` (empty).
To send: zip the content of the folder and submit it, after `package-project.ps1 -Template sn-jnl -Flat
-KeepComments` ends with `Verdict: PASS` (2026-10-09: PASS, 2 pages).
To fill in, all in `main.tex`: the title, the abstract (150-250 words), 4 to 6 keywords, the eight declarations and
the acknowledgements, and the text from the master's thesis in the four sections; figures go beside `main.tex`.
Not taken over from the modular skeleton, because the sample's preamble is kept as it is: cleveref, the PDF title
and author (`\hypersetup`), `\RequirePackage{float}` before the class, the environments lemma, claim and corollary,
the problem box and the notation macros. What the text needs goes to the sample's place for additional packages; the
old files are in `archives/removed-from-projects/clanok-2-min-cut-path/2026-10-09-before-flat/`.
Differences from the sample outside the content places: `\usepackage[T1]{fontenc}`, and line 28, where the two
typographic quotes of the publisher's comment are re-encoded from Windows-1252 to UTF-8 (the packager reads only
UTF-8). "Change history" below names `preamble/` and `sections/` files of the former layout.

## Intent

| | |
|---|---|
| Type | journal article; skeleton with placeholder text |
| Language | English (American spelling) |
| Content source | **master's thesis *Min Cut-Path* (2025)**, the author's decision of 2026-10-07 |
| Main file | `main.tex` (the template's sample `sn-article.tex` filled in; the whole manuscript in one file) |
| Target journal | Algorithmica (Springer), the author's request of 2026-10-08; venue card [knowledge/venues/algorithmica.md](../knowledge/venues/algorithmica.md) |
| Class | `sn-jnl.cls` (Springer Nature journal article template 3.1, December 2024; `\ProvidesClass`: `sn-jnl 2019/11/18 v0.1`), options `pdflatex,sn-mathphys-num` (the reference style is inferred from Algorithmica's numbered citations, TODO(verify) on the venue card); bibliography `sn-mathphys-num.bst`, which the class selects itself (natbib `numbers,sort&compress`) |
| Template folder | `templates/sn-jnl/` (the template the Algorithmica submission guidelines recommend; download URL and SHA-256 in `templates/SOURCES.tsv`); `sn-jnl.cls` and `sn-mathphys-num.bst` here are byte-identical to it (packager, 2026-10-08) and are never edited in the project; `main.tex` is `sn-article.tex` with the content places filled in |
| Bibliography | `references.bib` (empty: nothing is cited yet) |
| Origin | empty folder `clanok_2 min cut-path`, renamed by the convention on 2026-10-07; skeleton from `templates/article-modular` and the Springer Nature template, 2026-10-08 |
| Knowledge base | [knowledge/research/min-cut-path.md](../knowledge/research/min-cut-path.md) |

## Status

Template prepared on 2026-10-08, replaced by the filled-in sample on 2026-10-09; the text is placeholder only.
Builds with exit code 0: 2 pages A4, no undefined references, all fonts Type 1. The static check and the full
package check pass (`Verdict: PASS`, see "Build").

### Needed before writing

1. **LaTeX source of the master's thesis.** The repository has only the PDF and the extracted text
   (`knowledge/sources/diplomova-praca-2025-min-cut-path.*`). If the source exists (Overleaf, disk), put the zip into `inbox/`:
   formulas, algorithms and figures can then be taken over exactly. Without it the text is transcribed from the PDF.
2. **Scope and title.** Article 1 already used from the thesis: diameter 2, cut at most 2, random graphs (approximation scheme).
   Left unused (see [knowledge/research/min-cut-path.md](../knowledge/research/min-cut-path.md), Section 4):
   - ch. 2: tree-cut, 2-approximation, global minimum, partial path / partial cut property;
   - ch. 3.3: class *diam or cut 2*, general square graph decomposition, polynomial and linear algorithm;
   - ch. 4.5: almost polynomial average-case algorithm (Path-Cut);
   - ch. 5: symmetric case `c = d = cp`, Filter-BFS, Local-Cut, nearly k-regular graphs.

   The CV lists two working titles: *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem* and
   *Random Graph Models for the Min Cut-Path Problem*. The title goes into `\title{...}` in `main.tex`.
3. **Intent** (`knowledge/writing/paper-structure.md` section 1): the four answers, written here before any text.

### Open items for the author (before submission)

1. **Title, abstract (150-250 words), 4 to 6 keywords**: placeholders in `main.tex`.
2. **Declarations** (`\section*{Declarations}` in `main.tex`): every item is a placeholder ("Statement."); the
   second item keeps the sample's double heading "Conflict of interest/Competing interests", choose one. Algorithmica returns a submission
   without the relevant declarations as incomplete; a data availability statement is mandatory; an item that does not
   apply reads "Not applicable". Funding, competing interests and author contribution are also entered in the
   submission system; for the last two only the system's entries are used in the published version.
3. **AI declaration**: if AI tools were used beyond copy editing, the use is described in the manuscript
   (`knowledge/writing/submission.md` §1.3); the packager reminds of it on every run.
4. **One `.tex` file.** Settled 2026-10-09: `main.tex` is one file without `\input`, as the template's sample asks
   ("Submit your LaTeX manuscript as one .tex document").
5. **`[referee]` option.** The template's user manual asks for double line spacing (`\documentclass[referee,...]`) "for
   the peer review and editorial stages"; the sample's active line and Algorithmica's guidelines do not use it. Decide
   at submission.

## Article contents

| Section | Label | Contents |
|---|---|---|
| 1 Introduction | `sec:introduction` | placeholder |
| 2 Preliminaries | `sec:preliminaries` | placeholder |
| 3 Results | `sec:results` | placeholder |
| 4 Conclusion | `sec:conclusion` | placeholder |

## Files

```
projects/clanok-2-min-cut-path/     (everything in it is sent; no sub-folders)
main.tex                    sn-article.tex (template 3.1) with the content places filled in: \title, \author*, \email,
                            \affil (one author, no numbers), \abstract, \keywords, the sections Introduction,
                            Preliminaries, Results, Conclusion (placeholders), \backmatter, \bmhead{Acknowledgements},
                            \section*{Declarations} with the sample's eight items, \bibliography{references};
                            added: \usepackage[T1]{fontenc}. The sample's \documentclass[pdflatex,sn-mathphys-num]{sn-jnl},
                            package block, \theoremstyle/\newtheorem lines (theorem, proposition, example, remark,
                            definition), \raggedbottom and the publisher's comments are unchanged
references.bib              cited entries only (empty: nothing is cited yet)
sn-jnl.cls, sn-mathphys-num.bst   venue files, byte-identical to templates/sn-jnl/ (the .bst from its bst/ folder)

beside the folder (never sent)
projects/clanok-2-min-cut-path.md   these notes
```

## Build

```powershell
.\scripts\build-project.ps1 -Project clanok-2-min-cut-path
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments -CheckOnly    # after a structural change
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments               # before the folder is sent
```

`-Flat`: Springer Nature asks for all files in one directory. `-KeepComments`: the folder is sent with its comments.
No `-MaxPages`: Algorithmica states no page limit.
Last run 2026-10-09 after the move to the flat folder (`-Template sn-jnl -Flat -KeepComments`): `Verdict: PASS`,
2 pages, `Trace scan: 5 files, 0 hits (0 allowed); 2 files identical to the template not scanned`, 82 comment lines
kept, one finding `[ai-declaration]` (the reminder). `check-text.ps1`: one finding, the sample's heading
"Acknowledgements" (see "Known problems"). Built by hand in a copy of the folder (pdflatex, bibtex, pdflatex,
pdflatex): 2 pages; bibtex ends with its one error "I found no \citation commands" until something is cited.
Run of the modular layout earlier that day (after the review fixes): `-Flat` PASS, 15 files in the zip, 2 pages, `Trace scan: 15 files, 0
hits`, venue files identical to the template; findings only `[comment]` (end-of-line comments such as `% border
color`) and the `[ai-declaration]` reminder. `check-text.ps1`: 0 findings; `check-bib.ps1`: 0 findings.

## Known problems

- **PDF title and author are empty** (`pdfinfo`): the class sets no PDF metadata and the `\hypersetup` line of the
  former wrapper was not taken over (2026-10-09).
- **T1 font encoding added to `main.tex`.** The class leaves `\RequirePackage[T1]{fontenc}` commented out; with its
  default OT1 the surname printed as "l" with a caron above instead of "ľ" and the PDF text lost every accent
  (`pdftotext`: "Michel", "Saf´arik"). The added line changes the encoding only (Computer Modern stays, Type 1 from
  `cm-super`); remove it if the journal objects.
- **Diacritics as TeX code.** Springer Nature's LaTeX page asks to write special characters as TeX code
  (`Miche\v{l}`, `Ko\v{s}ice`); the front matter does, and new text should do the same.
- **Figures.** Springer Nature wants every file in one directory (the folder has no sub-folders) and Algorithmica prefers EPS for
  vector figures; the template's user manual still says the compiler "accepts only .eps", although the class's default
  option is `pdflatex`. An EPS figure (the template's `fig.eps`, tested in the modular layout) builds here: pdfLaTeX
  converts it with `epstopdf` (test: `archives/test-evidence/2026-10-09/sn-jnl-float/`). Whether submission.nature.com accepts
  PDF figures: TODO(verify) when the first figure is added. Captions print "Fig. 1" (class).
  Algorithmica's guide also asks for figure files named "Fig" plus the number (`Fig1.eps`), while the house rule
  names files by content; whether this applies to LaTeX source uploads: TODO(verify). Settle before the first figure
  (renaming changes every `\includegraphics` path).
- **Labelled lists.** In `sn-jnl` the optional argument of `enumerate` sets only the label width; the labels are fixed
  (`1.`, `(a)`, `(i)` by depth), so `\begin{enumerate}[(a)]` (article 1, thesis) silently prints `1.`. Loading
  `enumerate` or `enumitem` would replace the class's list layout. Before the first labelled list, test an
  adaptation in the preamble that keeps `[(a)]` in the text and record it here.
- **No `\DoNotLoadEpstopdf`.** The house template sets it when cleveref gets options; here it is left out on
  purpose, because it switches off `epstopdf` and EPS figures would stop building (`grfext`, the reason for it, is
  installed since 2026-10-08).
- **Reference order.** `sn-mathphys-num.bst` numbers references in citation order (its default); Algorithmica's
  guide says "numbered consecutively", while published Algorithmica lists are alphabetical. The `.bst` has an `alpha`
  option (an `@settings` entry with `options = "alpha"`, untested). TODO(verify) which order the journal wants.
- **Acknowledgments placement.** Algorithmica's guide puts acknowledgments on the title page; the template sets them
  with `\bmhead{...}` in the back matter. `main.tex` follows the template; since 2026-10-09 the heading is the
  sample's "Acknowledgements" (article 1 has "Acknowledgments", American English; `check-text.ps1` reports the
  British form). Decide before submission.
- **Build messages while the text is a placeholder:** natbib "Empty `thebibliography' environment" and BibTeX "I found
  no \citation commands" (both disappear with the first citation); an empty "References" heading prints.
- **Class messages** (the pristine sample shows them too): `U/rsfs/m/n` size substitutions (from `mathrsfs` of the
  sample's package block), hyperref "Difference (4) between bookmark levels", one "Underfull \vbox (badness 10000) has
  occurred while \output is active" per page.
- **`\RequirePackage{float}` before `\documentclass`: not in `main.tex` since 2026-10-09** (the sample's preamble is
  kept as it is); it comes back with the first figure, table or algorithm if the duplicate anchors are to be avoided.
  The sample's block loads `float` (through `algorithm.sty`) after
  the class has loaded `hyperref`, so every figure and table anchor is written twice (pdfTeX "destination with the same
  identifier (name{figure.1})"; the pristine sample shows it for each float). Loading `float` first removes it (tested
  2026-10-09 with a figure, a table and an algorithm; `\cref` then reads "Figure 1, Table 1, and Algorithm 1"). Same
  fix as article 1 under `cas-sc`; not a layout change.

## Content changes to review

None (no text yet).

## Change history

**2026-10-08 - template for Algorithmica (sn-jnl, Springer Nature template 3.1)**
- Template: `templates/sn-jnl/` from the zip linked by https://www.springernature.com/gp/authors/campaigns/latex-author-support
  (recommended by the Algorithmica submission guidelines), `\ProvidesClass` line: `sn-jnl 2019/11/18 v0.1`.
- Skeleton: `preamble/`, `sections/`, `img/`, `references.bib` copied from `templates/article-modular`; `sn-jnl.cls` and
  `bst/sn-mathphys-num.bst` copied from the template unchanged.
- Wrapper: new `main.tex` from `sn-article.tex`: class options of the sample's active line, its standard package block,
  front matter for one author (`\author*`, `\affil*` without numbers; `\affil` since 2026-10-09), back matter
  (`\backmatter`, `\bmhead{Acknowledgments}`, `\section*{Declarations}`); added `\usepackage[T1]{fontenc}`, cleveref,
  `\hypersetup` with title and author.
- preamble/: removed amsmath, amssymb, amsthm, graphicx, booktabs, algorithm, algpseudocode from `packages.tex`
  (loaded by the sample's block in `main.tex` or by the class; restored 2026-10-09); theorem styles switched to the class's `thmstyleone`,
  `thmstyletwo`, `thmstylethree` as the sample assigns them; Min Cut-Path macro block added.
- sections/: new `92-declarations.tex`; the abstract's comment states Algorithmica's 150-250 words.
- Bibliography: `sn-mathphys-num` (numbered, square brackets, as Algorithmica asks); no BibTeX warnings beyond the empty list.
- Build: 2 pages, undefined references 0, overfull 0; fonts Type 1 only.
- Package: `package-project.ps1 -Template sn-jnl -Flat`: Verdict PASS; `[layout]`: none.
- MiKTeX packages installed with the author's consent: `threeparttable`, `jknappen`, `ncctools`.

**2026-10-09 - float anchors, review fixes**
- `main.tex`: `\RequirePackage{float}` before `\documentclass` (duplicate float destinations otherwise, see "Known
  problems"); heading `\bmhead{Acknowledgments}` in American spelling (`check-text.ps1` finding); `\affil` instead of
  `\affil*` (with one author the starred form printed an asterisk that pointed to nothing); comments on what is
  class-dependent and on the absent `\DoNotLoadEpstopdf`.
- `preamble/packages.tex`: amsmath, amssymb, amsthm, graphicx, booktabs, algorithm, algpseudocode back in (no-ops after
  the sample's block); `preamble/environments.tex`: comment that the style names belong to `sn-jnl`.
- `sections/92-declarations.tex`, `sections/02-preliminaries.tex`: comments only (submission-system items; figure
  names point to "Figures" under "Known problems").
- Known problems added: figure file names, labelled lists, `\DoNotLoadEpstopdf`, the per-page underfull message.
- Build: 2 pages, no undefined references, no overfull lines. Package: `-Template sn-jnl -Flat` Verdict PASS.
