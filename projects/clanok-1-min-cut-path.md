# Article 1 - Min Cut-Path Problem

**Layout since 2026-10-09: the folder is what is sent.** `projects/clanok-1-min-cut-path/` holds only what the build
needs, with no sub-folders: `main.tex` (one file written from `cas-sc-template.tex`; packages, environments, macros
and the whole text are in it), `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` (byte-identical to
`templates/els-cas/`), `references.bib` and the ten figure files (seven PNG, three vector PDF; four figures were
added from the author's talk on 2026-10-09, see "Change history").
To send: zip the content of the folder and submit it, after `package-project.ps1 -Template els-cas -Flat
-KeepComments` ends with `Verdict: PASS` (2026-10-09, after the new figures: PASS, 17 pages).
Beside the folder: these notes and `projects/clanok-1-min-cut-path.submission/` (draft AI declaration).
Still open: "Open items for the author" below (AI declaration, funding, highlights, figures, abstract) and "Content
changes to review". "Change history" names `preamble/` and `sections/` files; their content is now in `main.tex`, the
files are in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-before-flat/`.

## Intent

| | |
|---|---|
| Type | journal article (manuscript) |
| Language | English (American spelling) |
| Main file | `main.tex` (the whole manuscript in one file, written from `cas-sc-template.tex`) |
| Target journal | Discrete Applied Mathematics (Elsevier), article type *Contribution* (more than 10 pages); venue card [knowledge/venues/discrete-applied-mathematics.md](../knowledge/venues/discrete-applied-mathematics.md) |
| Class | `cas-sc.cls` (Elsevier CAS bundle 2.4, single column; `\ProvidesClass`: `cas-sc 2024/05/04, 2.4`) with `cas-common.sty`; bibliography `cas-model2-names.bst` via `\usepackage[numbers,sort&compress]{natbib}` |
| Template folder | `templates/els-cas/` (the official template the DAM guide for authors links; download URL and SHA-256 in `templates/SOURCES.tsv`); `cas-sc.cls`, `cas-common.sty` and `cas-model2-names.bst` here are byte-identical to it (SHA-256 compared 2026-10-08) and are never edited in the project; `main.tex` is written from `cas-sc-template.tex` |
| Bibliography | `references.bib` (12 entries, all cited and verified) |
| Origin | Overleaf export `archives/clanok_1_min_cut_path.zip` (2026-10-07); class `new-aiaa` until 2026-10-08 |
| Knowledge base | [knowledge/research/min-cut-path.md](../knowledge/research/min-cut-path.md) |

## Status

Ported to the DAM template on 2026-10-08 and adjusted after the review of 2026-10-08 on 2026-10-09 (porting log and
review fixes in "Change history"). Four figures (three from the author's talk, one new) were added on 2026-10-09 (10 figures in
total). Builds with exit code 0: 17 pages (paper 192 x 262 mm, the class's own page
size), no undefined references or citations, no multiply defined labels, BibTeX without warnings, all fonts Type 1
and embedded (`cm-super` installed 2026-10-08). Remaining build messages are the class's own (see "Known
problems"). The flat package and the package with folders pass the packager, the no-trace check included
(`Verdict: PASS`; see "Build").
The text went through a full revision (formal errors, consistency, language, sources) - see "Change history".

**Before submission the author must check the content changes** listed in "Content changes to review" and settle
the open items below.

### Open items for the author (before submission)

1. **Keywords** (DAM: 1-7, required): proposed in `main.tex`, confirm or change (see "Content changes to review",
   item 13).
2. **AI declaration** (Elsevier requires it in the manuscript when AI tools were used beyond grammar, spelling and
   reference checks): drafted in `projects/clanok-1-min-cut-path.submission/ai-declaration.tex`, not in the
   manuscript. Fill in the model and version, check the purposes, then insert it as the comment block of that file
   describes: the heading and the paragraph directly in `main.tex` before
   `\section*{Acknowledgments}` (DAM wants the acknowledgments directly before the reference list and the declaration
   before the reference list). The packager fails while `[MODEL AND VERSION]` is in the manuscript.
3. **Funding:** list the funders in the form the guide gives ("Funding: This work was supported by ... [grant
   number ...]"), or use the recommended sentence "This research did not receive any specific grant from funding
   agencies in the public, commercial, or not-for-profit sectors." Nothing is in the manuscript yet.
4. **Competing interests:** the declarations tool (form) in Editorial Manager, "I have nothing to declare" if none.
5. **Research data** (Option C): the article has no data set; a statement in the submission form saying so.
6. **Highlights** (encouraged): a separate editable file with "highlights" in its name, 3-5 bullets of at most 85
   characters each; not written.
7. **Figures:** DAM asks for vector drawings (EPS/PDF) or bitmapped line drawings of at least 1000 dpi; the seven
   PNG drawings have 146-226 dpi at their printed width (see "Known problems"). Redraw them as vector graphics, or
   supply the originals at 1000 dpi or more; export without the embedded draw.io copy of the diagram, which six of
   the files carry (see "Known problems", figure metadata). The three figures added as PDF on 2026-10-09 are vector
   drawings and meet the requirement; the same TikZ route (sources in
   `projects/clanok-1-min-cut-path.submission/figures/`) would do for the seven PNG drawings.
8. **Figure citations and captions** (DAM guide, "Figures, images and other artwork" and "Captions": cite all images
   in the text; a caption is a brief title and a description of the image): Figures 3, 4 and 6 (`fig:chain-link`,
   `fig:chain`, `fig:threading` in Section 3 of `main.tex`) are never cited in the text, only shown, and their
   captions are a bare title ("A chain link", "A chain", "The threading operation"). Wording is the author's
   decision: for example "(Figure~\ref{fig:chain-link})" at the definitions of chain link, chain and threading.
   (Found in the review of 2026-10-08; not changed. The author wants one-line captions, stated 2026-10-09: a
   bare title is fine with him; the figures added on that day are all cited and have one-line captions.)
9. **Abstract** (DAM guide, "Abstract": state the purpose, the basic procedures, the main findings and the principal
   conclusions): the abstract gives only the motivation; NP-completeness, `cp = c + d − 1` for diameter two and
   cut-value at most two, and the random-graph results are missing (also "Known problems", Assessment item 3).
   Rewriting it is the author's decision.
10. **Math notation** (DAM guide, "Math formulae": the solidus for small fractional terms, powers of e written with
    exp): inline `\frac` in Section 6 of `main.tex` (`$p = \frac{1}{\alpha}$`, `$p = \frac{\alpha \log n}{n}$`
    and the same fraction in running text) and `e^{-\mu h(a)}` in two displays of the same section. Possible forms:
    `1/\alpha`, `\alpha\log n/n`, `\exp(-\mu h(a))`; notation changes are the author's decision. Elsevier typesets
    accepted articles itself, so this is a style point, not a blocker.
11. **Year of Frieze–Karoński** (bibliography): the publisher's page (`citation_publication_date` 2015/10) and
    Crossref (print 2015-10-26) date *Introduction to Random Graphs* 2015; the entry keeps 2016 (note in the
    canonical `.bib`). Confirm the year from the book's imprint page.
12. **AI use in the figures** (since 2026-10-09): Figures 7, 8 and 9 (`fig:two-synchronization`,
    `fig:three-synchronization`, `fig:clause-thread`) are TikZ drawings written by the AI assistant; 7 and 8
    follow the author's drawings in the talk, 9 is new (asked for by the author, drawn like 8). The talk's own versions of these images were made with an image generator (their files say so:
    `knowledge/sources/README.md`, "AI-generated images") and are not in the manuscript.
    Elsevier allows AI-created explanatory images only with a disclosure in the caption
    (`knowledge/writing/submission.md` §1.1): decide whether the three captions need the sentence and name the
    figures in the AI declaration (open item 2; the draft lists them). Check the drawings against the construction
    before submission.
13. **Parked: class diagram and counterexamples for the class "diam or cut 2"** (author's decision 2026-10-09: not
    in the article for now). They were in the conclusion for one build and were taken out again; the conclusion has
    its text of before. Files: `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-conclusion-figures/`
    (`graph-classes.png`, `counterexample-cut-two.pdf`, `counterexample-distance-two.pdf`); TikZ sources of the two
    counterexamples: `projects/clanok-1-min-cut-path.submission/figures/`; the two graphs and their values:
    `knowledge/research/min-cut-path.md`, below the results map. If they return: the counterexamples fit the end of
    Section 5 (they bound Theorems 4.5 and 5.1) better than the conclusion, and the class would then be defined
    there. In the class diagram the label "NP" names a complexity class while the regions are graph classes, and
    "diameter 2" and "cut 2" are drawn disjoint although the classes overlap (the cycle on four vertices is in
    both): redraw it or explain both points in the caption.

Settled, no action: the postal address of the affiliation is verified (institute's contact page, 2026-10-08); the
author has no ORCID (stated 2026-10-08), so the title page carries no `orcid` key (the empty "ORCID(s):" line: see
"Known problems"); the fonts are Type 1 since `cm-super` was installed (2026-10-08).

## Article contents

| Section | Label | Contents |
|---|---|---|
| 1 Introduction | `sec:introduction` | motivation, related problems, contributions, relation to the master's thesis |
| 2 Fundamentals | `sec:fundamentals` | cut-path, `CP(u,v)`, `cp(u,v)`, optimization version, Lemma *Basic Bounds*, average (1+ε)-approximation scheme |
| 3 NP-completeness | `sec:np-completeness` | 3-SAT → Separating Shortest Path (`sec:ssp`: chain, threads, calibration) → Min Cut-Path (`sec:ssp-to-mcp`) |
| 4 Graphs of Diameter Two | `sec:diameter-two` | decomposition `I, J, K, L`, odd intersection of path and cut, `cp = c + d − 1` |
| 5 Graphs with Cut-Value at Most Two | `sec:cut-two` | cactus structure, `cp = c + d − 1` |
| 6 Erdős–Rényi Graphs | `sec:random-graphs` | diameter 2 in dense graphs, properties of sparse ones, approximation scheme |
| 7 Conclusion | `sec:conclusion` | summary, further directions |

Section numbers are arabic since the port (the class `new-aiaa` printed I-VII): Section III is now Section 3,
Theorem III.5 is Theorem 3.5, Lemma II.4 is Lemma 2.4, and so on; the order is unchanged. The Roman numbers in
"Known problems" and "Content changes to review" below refer to the PDF before the port, and so do their citation
numbers: the reference list is now alphabetical, so the old [9] (Bollobás) is [1], [10] (Frieze–Karoński) is [5],
[3] (Mehlhorn et al.) is [10] and [5] (master's thesis) is [11].

Figures (number on 2026-10-09, label, file, section): 1 `fig:cut-path` `cut-path.png` (2); 2 `fig:chain-threads`
`chain-threads.png`, 3 `fig:chain-link` `chain-link.png`, 4 `fig:chain` `chain.png`, 5 `fig:chain-link-types`
`chain-link-types.png`, 6 `fig:threading` `threading.png`, 7 `fig:two-synchronization`
`two-synchronization-threads.pdf`, 8 `fig:three-synchronization` `three-synchronization-threads.pdf`,
9 `fig:clause-thread` `clause-thread.pdf` (all 3; Figures 7-9 stand inside the numbered list of thread types);
10 `fig:diameter-two-structure` `diameter-two-structure.png` (4).

Labels of statements: `lem:basic-bounds`, `thm:ssp-np-complete`, `alg:reduction`, `thm:mcp-np-complete`, `lem:cut-decomposition`,
`lem:empty-i-or-l`, `lem:odd-intersection`, `thm:diameter-two`, `rem:algorithm`, `thm:cut-two`, `thm:random-diameter-two`, `thm:random-diameter`,
`thm:random-connectivity`, `lem:degree-bounds`, `lem:connectivity-bounds`, `thm:approximation-scheme`.

## Files

```
projects/clanok-1-min-cut-path/     (everything in it is sent; no sub-folders)
main.tex                    the whole manuscript, written from cas-sc-template.tex: \RequirePackage{float},
                            \documentclass[a4paper,fleqn]{cas-sc}, natbib; packages float, tcolorbox, amsthm, algorithm,
                            algpseudocode (the class loads graphicx, amsmath, amssymb, etoolbox and hyperref); equation
                            numbering, theorem environments (\newtheorem, shared counter), problem box, algorithm
                            headers Input/Output; notation macros \cp, \CP, \diam, \OPT, \MinCutPath, \SSP, \ThreeSAT;
                            small-caps font shapes, key nologo, key alias H for figures; front matter (\shorttitle,
                            \shortauthors, \title, \author, \cormark, \ead, \affiliation, \cortext, abstract, keywords),
                            \maketitle, \hypersetup{pdfauthor}; Sections 1-7; Acknowledgments;
                            \bibliographystyle{cas-model2-names}, \bibliography
references.bib              bibliography
cas-sc.cls                  document class (Elsevier CAS bundle 2.4), pristine copy of templates/els-cas/
cas-common.sty              macros of the CAS classes, pristine copy
cas-model2-names.bst        bibliography style of the CAS bundle, pristine copy
chain.png, chain-link.png, chain-link-types.png, chain-threads.png, threading.png, diameter-two-structure.png   figures
cut-path.png                figure from the author's talk (bitmap, unchanged copy; since 2026-10-09)
two-synchronization-threads.pdf, three-synchronization-threads.pdf, clause-thread.pdf
                            vector figures (since 2026-10-09)

beside the folder (never sent)
projects/clanok-1-min-cut-path.md                              these notes
projects/clanok-1-min-cut-path.submission/ai-declaration.tex   draft AI declaration for the author
projects/clanok-1-min-cut-path.submission/figures/*.tex        TikZ sources of the three vector figures and of the
                                                               two parked counterexample drawings (class
                                                               standalone, STIX fonts as in the article); build
                                                               each with pdflatex --miktex-disable-installer
                                                               into tmp/ and copy the PDF into the project folder
```

No `thumbnails/` folder: `main.tex` sets the class key `nologo` (see "Build").

Version before the revision: `archives/removed-from-projects/clanok-1-min-cut-path/main-before-revision-2026-10-07.tex`
(compare with the single-file version `main-before-split-2026-10-07.tex` in the same folder).
Wrapper before the port: `main-before-port-2026-10-08.tex` in the same folder, together with `new-aiaa.cls` and
`new-aiaa.bst`. Modular version of 2026-10-08 (wrapper `main.tex`, `preamble/`, `sections/`): sub-folder
`2026-10-09-before-flat/` of the same folder.

## Build

```powershell
.\scripts\build-project.ps1 -Project clanok-1-min-cut-path
```

PDF: [outputs/clanok-1-min-cut-path/main.pdf](../outputs/clanok-1-min-cut-path/main.pdf)

Package check (what is sent is the project folder itself, zipped; the packager is the check that must end with
`Verdict: PASS` before sending). Editorial Manager cannot process sub-folders, hence the flat folder and `-Flat`;
DAM states no page limit for a Contribution, hence no `-MaxPages`; `-KeepComments` because the folder is sent with
its comments:

```powershell
.\scripts\package-project.ps1 -Project clanok-1-min-cut-path -Template els-cas -Flat -KeepComments -CheckOnly   # after a new file, a new package, a touched class file
.\scripts\package-project.ps1 -Project clanok-1-min-cut-path -Template els-cas -Flat -KeepComments              # before sending
```

Send only on `Verdict: PASS`. Last run 2026-10-09, 09:34, with the four new figures (`-Template els-cas -Flat
-KeepComments`): `Verdict: PASS`, 17 pages, `Trace scan: 15 files, 0 hits (0 allowed); 3 files identical to the
template not scanned`, 22 comment lines kept, one finding `[ai-declaration]` (advisory). The run before it, after
the move to the flat folder: `Verdict: PASS`, 16 pages, `Trace scan: 11 files, 0 hits (0 allowed); 3 files identical to the
template not scanned`, 22 comment lines kept, one finding `[ai-declaration]` (the packager looks for the draft in
`projects/clanok-1-min-cut-path/submission/`; it is now in `projects/clanok-1-min-cut-path.submission/`).
Runs of the modular layout earlier that day, 08:05-08:08, with the packager as changed after the review:
`-Template els-cas -CheckOnly`: `Verdict: PASS` (`Trace scan: 20 files, 0 hits (0 allowed); 3 files identical to
the template not scanned`); `-Template els-cas -Flat`: `Verdict: PASS`, 24 files in
`outputs/clanok-1-min-cut-path/package/clanok-1-min-cut-path-20261009-flat.zip`, PDF beside it
`clanok-1-min-cut-path-20261009.pdf`, 16 pages; the same without `-Flat`: `Verdict: PASS`,
`clanok-1-min-cut-path-20261009.zip` with folders, for Overleaf or a co-author. Report lines of both full runs:
`Template origin: els-cas (venue, CAS bundle 2.4; cas-sc 2024/05/04, 2.4, <download URL>)` (the folder matches the
archive file by file); `Trace scan: 23 files, 0 hits (0 allowed); 3 files identical to the template not scanned`
(the page text of the staged PDF included); `AI declaration: none in the manuscript; a draft exists at
projects/clanok-1-min-cut-path/submission/ai-declaration.tex and was not packaged`. Findings, none failing:
`[comment]` 8 (end-of-line comments in `preamble/`: tcolorbox options, meaning of two macros, purpose of two
packages; harmless, kept), `[ai-declaration]` 1 (the advisory note, open item 2); no `[fonts]` finding (the packaged
PDF has Type 1 fonts only, all embedded). The packages of 2026-10-08 (17 pages, no book DOIs) were moved out of
`outputs/clanok-1-min-cut-path/package/` to `tmp/review-fix/superseded-packages/`. The staged `references.bib` has no header comment (the packager
strips `.bib` comment lines); the draw.io copies inside the six PNG files are decoded and scanned as well (no hit).
Upload to Editorial Manager: the files of the folder, the
`.tex`, `.bst`, `.sty`, `.cls` and `.bib` files as Manuscript items, the six PNG files as Figure items
(Elsevier LaTeX instructions). The folder holds no `main.bbl` (a build product; the packager's zip adds one):
TODO(verify) whether Editorial Manager needs the `.bbl` beside the `.bib`.

Lines of `main.tex` that the template's sample does not have, each needed by the class (details:
[template-porting.md](../knowledge/writing/template-porting.md) §6.3):

- `\RequirePackage{float}` before `\documentclass`: the class loads hyperref, which writes every figure anchor twice
  when float comes later.
- `\keys_set:nn { stm / mktitle } { nologo }`: the class's own key; `\ead` then prints "Email address:" instead of the
  icon `thumbnails/cas-email.jpeg`, which needs a sub-folder that Editorial Manager cannot process.
- `\keys_define:nn { cas / fig } { H .meta:n = { pos = H } }` (since 2026-10-09): the class's `figure` takes
  key-value options and drops a plain `[H]`; `H` is declared as a short form of the class's own key `pos=H`, so
  the figures keep the standard `\begin{figure}[H]`.
- `\begin{abstract}[\abstractname]`: the class writes the abstract verbatim; without the optional argument it lost
  the `\input` line of the modular layout. Kept since the abstract text is in `main.tex`.
- `\DeclareFontShape` for `T1/stix/m/scit` and `b/scit`: STIX has no italic small caps; the substitution the font
  system makes anyway, declared without a warning.
- `\hypersetup{pdfauthor={Norbert Micheľ}}` after `\maketitle`: the class's own value ends with a stray character.
- `\usepackage[numbers,sort&compress]{natbib}`: the template's commented alternative to its author-year line, because
  DAM numbers the references; `sort&compress` added.

## Known problems

### Assessment (2026-10-07)

The article as a whole makes sense: definitions → NP-completeness → two polynomial classes → random graphs follow
from each other, and I found no error in the proofs in their current wording (I went through the reduction from
3-SAT, the theorem on diameter 2 and the theorem on cut ≤ 2 step by step and checked the formula on `K_n`, `C_4`, `C_5`,
`K_{2,3}` and the Petersen graph). Weak points, ordered by importance:

1. **Related work.** A comparison with close problems is missing. The closest one is the *non-separating st-path*
   (a path whose edge removal leaves the graph connected) - the mirror notion to Separating Shortest Path; its existence
   is NP-hard on general graphs (X. Mao, arXiv:2101.03519). Further, shortest-path interdiction / "most vital edges"
   and the Force Path Cut problem. A reviewer will almost certainly ask; the claim "not studied elsewhere" needs a
   paragraph on these works to back it.
2. **Definition II.5 vs. Theorem VI.6** - see below; moreover, "approximation scheme" usually means a family of
   algorithms parametrized by `ε`. Here it is one algorithm whose ratio tends to 1 - the result could be stated more
   simply and more strongly ("asymptotically optimal with high probability").
3. **Abstract and title** - the abstract does not state the results, the title is generic.
4. **Theorem VI.2** - the statement for `α > 1` holds, but the exact source is Chung, Lu: *The Diameter of Sparse
   Random Graphs* (2001): the diameter is `(1 + o(1)) log n / log(np)`; I recommend citing this work alongside [9].
5. **Motivation** - the introduction now says in one sentence what the cut guarantees in the model; the article does
   not return to the application later (fine for a theoretical article).

### Open points (unchanged)

- **Definition II.5** measures "almost all inputs" by the ratio `|I_opt(n)| / |I(n)|`, i.e. uniformly over all graphs
  (this corresponds to `p = 1/2`), while Theorem VI.6 speaks about `G(n, p)`. Proposal: add to item 3 a sentence that
  for inputs drawn from a probability distribution the ratio is replaced by a probability.
- **Abstract** does not state the results (NP-completeness, the formula `cp = c + d − 1`, the approximation scheme) -
  only the motivation.
- **Theorems VI.2 and VI.3** are cited after [9] and [10]; the exact wording and the theorem numbers in the books need
  checking (`TODO(verify)`); I did not have the books.
- Citation [3] for the cactus structure is given as "cf." - the work concerns the cactus representation of 2-cuts;
  the statement itself is justified directly in the article.
- The "Intent" section does not yet answer the four questions of
  [paper-structure.md](../knowledge/writing/paper-structure.md) §1 (main claim, contributions, closest work, reader
  and venue): for the author to fill in.

### Build and template (2026-10-08, class `cas-sc` 2.4)

- **Fonts (resolved 2026-10-08):** the four Type 3 bitmap fonts (T1 Computer Modern sans, sans bold extended,
  typewriter: captions, running head, footer, e-mail, DOIs) are Type 1 since `cm-super` was installed; `pdffonts`
  lists 17 entries, all Type 1 and embedded, and `pdftotext` reads the footer as "N. Micheľ" (before: `©`). The rebuild
  needed no `initexmf` refresh.
- **Figure resolution:** the drawings are PNG at 146-226 dpi at their printed width (DAM: vector, or at least
  1000 dpi for bitmapped line drawings): `chain-threads.png` 1293 x 219 px at 145 mm (226 dpi), `chain.png`
  1293 x 155 px at 145 mm (226 dpi), `chain-link-types.png` 1219 x 155 px at 145 mm (214 dpi), `threading.png`
  835 x 200 px at 145 mm (146 dpi), `chain-link.png` 290 x 156 px at 50 mm (147 dpi),
  `diameter-two-structure.png` 351 x 429 px at 60 mm (149 dpi). The images are the author's and were not changed
  (open item 7). Added 2026-10-09: `cut-path.png`, 555 x 366 px at 80 mm (176 dpi), a freehand bitmap from the
  author's talk, unchanged copy. The three PDF figures are vector drawings.
- **Figure metadata of the files added 2026-10-09:** `cut-path.png` carries only an XMP packet
  with `tiff:Orientation`; the three PDF figures have Creator "TeX" and Producer "MiKTeX pdfTeX-1.40.28", no date and
  no other key (`pdfinfo -custom`); fonts STIXMath, Type 1, embedded.
- **Figure metadata:** each of the six older PNG files carries the draw.io source of the drawing in a `tEXt` chunk
  `mxfile` (decoded 2026-10-08: the diagram, the editor host `app.diagrams.net`, the browser's user agent string,
  the page name "Stránka-1" and browser-translated Slovak style names). It names no AI tool and no workspace path,
  so the packager's trace scan, which decodes it, passes; but it travels with the zip. A redraw or re-export without "Include a copy of
  my diagram" (open item 7) removes it.
- **Class messages that also appear in the build of the pristine `cas-sc-template.tex`:** `Overfull \hbox
  (117.0831pt too wide)` and three hyperref "Ignoring empty anchor" at `\maketitle` (the front-matter box; nothing
  visible on page 1); an empty "ORCID(s):" footnote line.
- **ORCID line (decision 2026-10-08: left):** the author has no ORCID, but the title-page footnotes still end with
  "ORCID(s):". `\printorcid` (`cas-common.sty` l.425-435) prints it unconditionally; the class has no key to omit it,
  and its blind mode, the only switch that drops it, also hides the author, address and e-mail, which DAM's
  single-anonymized review needs. The pristine `cas-sc-template.tex` prints the same line (built in
  `tmp/orcid-check-2026-10-08/`, title page checked). `main.tex` is unchanged: redefining `\printorcid` would patch a
  class internal. DAM asks for no ORCID, and it typesets accepted articles itself from the editable files (guide for
  authors: "required to typeset your article for final publication").
- One `Underfull \hbox (badness 1292)` in the reference list (the Mehlhorn et al. entry, line broken inside the DOI);
  cosmetic.
- PDF subject "Complex STM Content" is set by the class; title and author are set (`pdfinfo`).
- `check-text.ps1` (run on the modular layout): 77 findings, all in the wording of the sections, which the port did
  not change (rule: content and wording are the author's); the wrapper lines 0 findings.
  `projects/clanok-1-min-cut-path.submission/ai-declaration.tex`: one long sentence and "in order
  to", both from Elsevier's prescribed statement, kept on purpose.

### Deviations from the rules in `knowledge/writing/`

- References with `Theorem~\ref{...}`; no `cleveref` (not requested; the class loads `hyperref`, `natbib` is loaded
  in `main.tex`).
- Theorem environments with `\newtheorem[definition]` (correct only while cleveref is not loaded).
- Figures placed with `[H]` (through the key alias `H` in `main.tex`; from 2026-10-08 to 2026-10-09 the sections
  carried the class's `[pos=H]`), the algorithm with `[H]`; house rule: `[tb]`.
- Figures are PNG drawings, not vector PDF (see above).
- Lists use the class's own `enumerate` and `itemize` (since 2026-10-09; `enumitem`, which replaced them with
  `article`'s spacing, was removed). The labelled list in Section 3 (proof of Theorem 3.5) is written
  `\begin{enumerate}[(a)]`, the class's label syntax (before: `[label=(\alph*)]` with `enumitem`); under a class
  without that syntax the preamble needs `\usepackage{enumerate}`. The plain `enumerate` nested in item
  (b) of the two-way correspondence (proof of Theorem 3.5) is labelled (a)-(c), the same style as the outer
  list (a)-(b); `new-aiaa` printed 1)-3). If the author wants other labels there, `\begin{enumerate}[1.]` on that line
  would do it (markup only; not changed, because it was not requested).

## Content changes to review

These edits change the mathematical content or claims about the literature. They were made on the basis of findings
from the revision, but the author is responsible for them.

1. **The proof of NP-completeness of Separating Shortest Path (Theorem III.5) is rewritten.**
   - The procedure `Calibrate` was added (equalizing the lengths of both paths of each link of the chain; extending
     the connecting paths of the threads to at least `Λ` edges) and is called in the algorithm.
   - The correctness proof now has the steps: shortest paths are exactly the paths of the chain → the path must "hit"
     every thread → synchronization threads force consistent signs → clause threads correspond to satisfying the
     clauses → analysis of `G ∖ P` through "unused paths" and dead ends.
   - The algorithm uses the occurrence sets `O_i` and the indices `L_{j,k,i}` (position `j`, clause `k`, variable `i`)
     instead of `ℓ[0], ℓ[1]`; brackets fixed.
   - The definition of a thread now states that a thread contains no simple edges of the chain; the chain has `r`
     links (instead of `m`).
2. **Lemma II.4 (Basic Bounds) is new** - `max{c, d} ≤ cp ≤ c + d − 1` with a proof (in the master's thesis Claim 6
   and 7). The proofs of Theorems IV.5 and V.1 refer to it.
3. **Theorem V.1 (cut at most 2) has a proper proof** - taken from the master's thesis (Theorem 18) and completed with
   the argument about the bridge and the arcs of the cycles.
4. **Vertex degrees in `G(n, α log n / n)`**: the original "Degree Concentration" (all degrees in `(1 ± ε) α log n` for
   every fixed `ε`) does not hold for fixed `α` - the minimum and maximum degree are a constant factor away from
   `α log n`. Replaced by Lemma VI.4 (*Degree Bounds*): there are constants `0 < β₁ < β₂` depending only on `α` such that
   all degrees lie in `[β₁ log n, β₂ log n]`, with a proof via Chernoff bounds. Lemma VI.5 (bounds for `c(u,v)`) and the
   proof of Theorem VI.6 were adjusted accordingly. The resulting theorem on the approximation scheme does not change.
   **The same error is in the master's thesis (Theorem 28, Claim 29).**
5. **Theorem VI.6** (approximation scheme): the assumption `p ≥ α log n / n` is kept; the proof gained the monotonicity
   argument (adding edges does not increase distances and does not decrease `c(u,v)`).
6. **Theorem VI.1** (diameter 2 for constant `p`): `α > 1` instead of `α > 0`, and a citation [Bollobás] was added.
7. **Definition of cut-path in the problem boxes**: "contains subsets `P, C ⊆ S`" instead of "can be partitioned into
   `S = P ∪ C`" (consistent with Definition II.1).
8. **The optimization version is NP-hard** (originally "NP-complete").
9. **Introduction**: the problem is presented as introduced in the master's thesis [5]; a sentence was added that the
   NP-completeness is new and that the results on graph classes and random graphs come from the master's thesis.
   The conclusion refers to partial results for the class "diam or cut 2".
10. **Introduction, related work**: the wording at citations [1]–[3] is adjusted to match the content of the cited works
    (multi-terminal minimum cuts; representations of all minimum cuts; small cuts and edge connectivity).
11. Minor refinements: `u, v` lie in the same component; the odd-intersection lemma is stated for a cut `C` with two
    sides (originally the cut was called `c(u,v)`, which clashed with the value of the minimum cut); definition of the
    diameter ("at most `k`"); bound variables in the lemmas are `x, y`, so they do not clash with `u, v`.

12. **Added in the stylistic revision** (2026-10-07, second round): Remark IV.6 (if `cp = c + d − 1` holds, the union of
    any minimum cut and any shortest path is a minimum cut-path - this backs the sentence about the "simple
    algorithm"); item 4 in the definition of the chain (parts of the chain share a vertex only when they are adjacent);
    a one-sentence definition of `G(n, p)`; a sentence that for dense random graphs the problem can be solved exactly
    in polynomial time on almost all inputs.

13. **Keywords (new, port to DAM, 2026-10-08)** - author metadata, proposed from the article's own terms and
    avoiding the title words (min, cut-path, problem): *NP-completeness*, *edge connectivity*, *graph diameter*,
    *Erdős–Rényi graphs*, *average-case approximation* (`keywords` environment in `main.tex`). DAM asks for 1-7
    keywords in English and advises against multi-word keywords joined by "and" or "of". Confirm or replace them.
14. **Title page (port to DAM, 2026-10-08)**: the affiliation now carries the full postal address that DAM requires,
    "Jesenná 5, 040 01 Košice, Slovakia", taken from the institute's contact page
    (<https://ics.science.upjs.sk/en/contact/>, read 2026-10-08; recorded in `knowledge/author.md`); the e-mail
    address is marked as the corresponding author's.
15. **Algorithm 1 headers (port to DAM, 2026-10-08)**: "Require:" and "Ensure:" are printed as "Input:" and
    "Output:" (two `\algrenewcommand` lines in `preamble/environments.tex`; house rule of
    `knowledge/writing/math-writing.md`, not a DAM requirement; `sections/03-np-completeness.tex` still writes
    `\Require`/`\Ensure`). Confirm, or delete the two lines to get the old headers back.
16. **Figures added on 2026-10-09 and the text that cites them.** Captions are one line and the text is the
    minimum, on the author's instruction of that day (longer captions and lead-in sentences were cut).
    - Section 2, after Definition 2.1: one new sentence, "Figure 1 shows a cut-path schematically."
    - Section 3, list of thread types: Figures 7, 8 and 9 stand inside the three items; each item cites its
      figure in brackets. The proof of Theorem 3.5 ("Synchronization of variable gadgets") cites Figures 7 and 8.
    - Figure 9 shows the clause thread for the example clause `C_k = (x_1 ∨ ¬x_2 ∨ x_3)`, i.e., signs `+, -, +`
      in `L_{1,k}, L_{2,k}, L_{3,k}`; the example clause appears only in the caption.
    - Section 7 (conclusion): unchanged (open item 13).
    - Drawings: Figures 7-9 are TikZ drawings: the threads run through crossing edges on the upper or lower
      path of a link (the talk's images end at the corners of the links), with dashed ends towards `u` and `v`
      and the signs `+`, `-` inside the links. Confirm that they show the construction as intended.

## Change history

**2026-10-09 - figures from the author's talk (09:10-09:35)**
- Source: the beamer talk *Min Cut-Path Problem* in `knowledge/sources/Overleaf Projects (1 items) (11).zip`
  (table of its images: `knowledge/sources/README.md`, "Other material"). Five of its images are the figures the
  article already had (same SHA-256).
- Added as an unchanged copy: `cut-path.png` (talk: `figures/obrazok_cut-path.png`) as Figure 1 in Section 2.
- Redrawn in TikZ as vector PDF, on the author's decision (2026-10-09), because the talk's files `2-sych.png` and
  `3-sych.png` are marked by their own metadata as made by an image generator: `two-synchronization-threads.pdf`
  (Figure 7), `three-synchronization-threads.pdf` (Figure 8), both in Section 3. Sources:
  `projects/clanok-1-min-cut-path.submission/figures/`; included at their natural size (137 mm).
- Added and removed again on the same day, on the author's decision ("not in the article for now"): the class
  diagram `graph-classes.png` (talk: `figures/triedy_zlozitosti_diam_or_cut-2.png`) and the two counterexamples
  `counterexample-cut-two.pdf`, `counterexample-distance-two.pdf` (TikZ redraws of the talk's `example_cut2c.png`
  and `example_diam2c.png`, which are also image-generator files), with a paragraph in the conclusion stating that
  `cp = c + d - 1` fails in the class "diam or cut 2". The three files are in
  `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-conclusion-figures/`; the conclusion is
  identical to the committed text again (open item 13).
- Not added: `figures/triedy_zlozitosti.png` (the class diagram without the class "diam or cut 2");
  `general_square_graph.png` and `Transformation_A/B/C.png` (general square graphs are not defined in this
  article; material for article 2).
- New drawing, asked for by the author: `clause-thread.pdf` (Figure 9), the clause thread of an example clause.
- Placement and length, on the author's instruction: Figures 7-9 stand inside the numbered list of thread types;
  all new captions are one line; the explanatory sentences first written around the figures were cut.
- Text: "Content changes to review", item 16. The old figures are now Figures 2-6 and 10.
- Build: 17 pages (16 before), no undefined references, the class's overfull 117 pt box and the underfull line in
  the reference list as before, all fonts Type 1 and embedded. `check-text.ps1`: 77 findings, the number before
  the change. Packager, full run `-Template els-cas -Flat -KeepComments`: `Verdict: PASS`, 17 pages,
  `Trace scan: 15 files, 0 hits`.
- Draft AI declaration (`projects/clanok-1-min-cut-path.submission/ai-declaration.tex`): the three drawings added
  to the purposes and to the list of points to complete. Open items 12 and 13 are new; items 7 and 8 updated.

**2026-10-09 - fixes after the review of 2026-10-08 (DAM conformance, packager, regression)**
- `references.bib` (canonical file first, with new status lines): DOIs added to the four books that have one,
  each checked on the publisher's book page and in its Crossref record (both list the entry's ISBN):
  Bollobás 2001 `10.1017/CBO9780511814068`, Frieze–Karoński `10.1017/CBO9781316339831` (cambridge.org), Diestel 2025
  `10.1007/978-3-662-70107-2`, Godsil–Royle 2001 `10.1007/978-1-4613-0163-9` (link.springer.com). Cormen et al.
  (MIT Press): no DOI. The year of Frieze–Karoński is open item 11. `check-bib.ps1 -Project clanok-1-min-cut-path`:
  0 findings.
- Lists: `enumitem` removed from `preamble/packages.tex`; `sections/03-np-completeness.tex` line 341
  `\begin{enumerate}[label=(\alph*)]` → `\begin{enumerate}[(a)]`, the class's label syntax; labels (a)/(b) print as
  before, the lists take the class's spacing: 17 → 16 pages.
- Figures: `sections/03-np-completeness.tex` (lines 74, 102, 133, 165, 207) and `04-diameter-two.tex` (line 124) back
  to `\begin{figure}[H]`; `main.tex` declares `H` as a short form of the class's key `pos=H`. Every figure stays where
  it is written (pages 5, 5, 6, 6, 7, 12).
- `preamble/packages.tex`: `graphicx`, `amsmath`, `amssymb` loaded again (the class loads them too), so `preamble/`
  and `sections/` also build under `article` (tested with `\usepackage{enumerate}`, 29 pages); `etoolbox` not
  re-added (nothing in the article uses it; `tcolorbox` loads it). Comments of `main.tex` and `packages.tex` say so.
- Text comparison with the packaged PDF of 2026-10-08, 22:18 (word diff of `pdftotext` output, running heads and
  footers removed; `tmp/review-fix/compare2/`): the four DOIs and the positions of the running title at page breaks;
  nothing else.
- Build: 16 pages, no undefined references, the class's overfull 117 pt box and three empty-anchor warnings at
  `\maketitle`, one underfull line in the reference list; 17 fonts, all Type 1 and embedded.
- Packager (`scripts/package-project.ps1`, changed after the review; tests:
  `archives/test-evidence/2026-10-08/packager-review/`): names that only the build assembles are found in the staged
  PDF; the template folder is compared with its archive file by file. Runs on article 1: see "Build".
- `submission/ai-declaration.tex`: insertion steps aligned with `knowledge/writing/submission.md` §1.3 (text in
  `sections/91-ai-declaration.tex`, heading and `\input` in `main.tex` before the acknowledgments).
- README: open items 8-11 (figure citations and captions, abstract, math notation, a book's year), "Content changes
  to review" item 15 (algorithm headers), the porting log's "done" claim corrected.
- Final check, 08:31-08:40, no source change: rebuild (16 pages, 0 errors); `-Template els-cas -Flat` full run
  repeated, `Verdict: PASS`, the flat zip and the PDF beside it rewritten (same 24 files, same report lines). The
  unpacked flat zip checked by hand: no AI tool name, user name or workspace path in the `.tex`, `.bib` and `.bbl`
  files, in the PDF's metadata, page text and inflated streams, or in the PNG text chunks (draw.io data only);
  `cas-sc.cls`, `cas-common.sty` and `cas-model2-names.bst` have the SHA-256 of the files inside
  `archives/els-cas-templates.zip`, whose own SHA-256 is the one in `templates/SOURCES.tsv`. Negative test on a
  throwaway copy (`tmp/dam-final-check/zz-trace-probe`): a tool name in the text, a tool name in a `.bib` note and a
  user-profile path in a macro give `Verdict: FAIL (trace)`; one line appended to `cas-sc.cls` gives
  `Verdict: FAIL (template-file)`.

**2026-10-08 - fonts and ORCID line after the port (22:16-22:19)**
- Fonts: `cm-super` installed with the owner's consent; rebuild with no source change and no `initexmf` refresh:
  17 pages, `pdffonts` 17 entries, all Type 1 and embedded (cm-super `SFSS0900`, `SFSS1000`, `SFSX0900`, `SFTT0800` in
  place of the four Type 3 fonts); `pdftotext` reads the footer as "N. Micheľ". Log otherwise unchanged (the class's
  overfull 117 pt box and three empty-anchor warnings at `\maketitle`, one underfull line in the reference list).
- ORCID: the author has none. The class prints "ORCID(s):" unconditionally and offers no key to omit it; the pristine
  `cas-sc-template.tex` prints the same line (`tmp/orcid-check-2026-10-08/`). Left as is, `main.tex` unchanged
  ("Known problems").
- Package: `-Template els-cas -CheckOnly` `Verdict: PASS`; `-Template els-cas -Flat` `Verdict: PASS` (24 files,
  17 pages, no `[fonts]`, `Trace scan: 23 files, 0 hits (0 allowed)`); without `-Flat` `Verdict: PASS`. Both zips
  have the size of the 18:26 zips (sources unchanged); the packaged PDF is new.

**2026-10-08 - ported to Discrete Applied Mathematics (cas-sc 2.4)**
- Template: `templates/els-cas/` from
  https://assets.ctfassets.net/o78em1y1w4i4/5uFmLZJTPDMAUjFnHRpjj8/6f19a979146eb93263763d87a894ab0d/els-cas-templates.zip
  (linked as "LaTeX template" from the DAM guide for authors; SHA-256 in `templates/SOURCES.tsv`), `\ProvidesClass`
  line: `cas-sc 2024/05/04, 2.4: Formatting class for CAS single column articles`. Copied unmodified into the project:
  `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` (SHA-256 equal to the template). Retired to
  `archives/removed-from-projects/clanok-1-min-cut-path/`: `new-aiaa.cls`, `new-aiaa.bst`.
- Wrapper: new `main.tex` from `cas-sc-template.tex` (class options `a4paper,fleqn`; `\WriteBookmarks`,
  `\floatpagepagefraction`, `\textpagefraction` lines; front-matter commands; `\bibliographystyle{cas-model2-names}`);
  old wrapper archived at `archives/removed-from-projects/clanok-1-min-cut-path/main-before-port-2026-10-08.tex`.
  Template elements left out because they would print empty or do not apply: `\tnotemark`/`\tnotetext`,
  `\fnmark`/`\fntext`, `\ead[url]`, `\credit`/`\printcredits` (single author), `highlights` and `graphicalabstract`
  environments, `\bio`, the sample section, figure, table and `\clearpage`, the `\tsc` macros, `\nocite{*}`. Lines
  added for the class: listed under "Build".
- Front matter: title, short title, short author "N. Micheľ", author with affiliation mark *a*, full postal address
  (verified, see "Content changes to review" item 14), corresponding author with e-mail; abstract unchanged
  (141 words, DAM limit 250); keywords proposed (item 13); no ORCID (none recorded); no MSC codes (DAM asks for
  none); funding, competing interests, data statement: open items; acknowledgments as `\section*{Acknowledgments}`
  directly before the reference list (DAM).
- preamble/: removed `graphicx`, `amsmath`, `amssymb`, `etoolbox` (the class loads them); added `enumitem` (the text
  uses `[label=(\alph*)]`, which the class's `enumerate` prints as text) and the algorithm headers
  `\algrenewcommand\algorithmicrequire{\textbf{Input:}}`, `\algrenewcommand\algorithmicensure{\textbf{Output:}}`
  (house rule, scheduled for the port). Removed from the wrapper: `inputenc` (UTF-8 is the default), `\let\openbox\relax`,
  `\let\Bbbk\relax` (only needed with newtxmath), `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (the class is
  single-spaced and loads no setspace). Comments that named workspace files were removed from `preamble/macros.tex`
  and from the header of `references.bib` (entries unchanged).
- Bibliography: `new-aiaa.bst` (order of citation) → `cas-model2-names.bst` with natbib `numbers,sort&compress`:
  labels [1]-[12] in alphabetical order of the first author (Bollobás ... Nagamochi), DOIs printed as `doi:...`,
  the Frieze–Karoński URL printed; BibTeX warnings: none. `check-bib.ps1`: 0 findings.
- Layout: text block 164.6 mm (paper 192 x 262 mm), the old one 6.5 in; all figure widths (at most 145 mm) fit,
  no display or table needed a change.
- Build: 23 → 17 pages; undefined references 0; multiply defined labels 0; overfull 1 (the class's front-matter box,
  117 pt, also in the pristine template's build, not visible); remaining warnings: three hyperref "Ignoring empty
  anchor" (class), one underfull line in the reference list; fonts: four Type 3 (no `cm-super`). Fixed during the
  port: all figures moved to the end of the document (`[H]` dropped by the class), duplicate figure anchors
  (float loaded after hyperref), the abstract printed as "sections/00-abstract" (verbatim abstract), small-caps
  shape warnings, a stray character in the PDF author field.
- Text comparison (`pdftotext -layout`, old and new PDF, word diff after Unicode normalization; files in
  `tmp/port-dam-2026-10-08/`): differences only in the front matter (address, keywords, footnotes), section and
  statement numbers (Roman → arabic), citation numbers (alphabetical list), list labels (`1)` → `1.`; the
  `[label=(\alph*)]` list unchanged; its nested list now `(a)`-`(c)` instead of `1)`-`3)`, see "Known problems"), caption labels ("Fig. 1" → "Figure 1:"), the reference list style, running heads and page footers,
  line breaks, "Acknowledgment" → "Acknowledgments", "Require:"/"Ensure:" → "Input:"/"Output:". Small caps are
  extracted as capitals, and `pdftotext` does not extract some STIX math symbols (`\mathsf{true}`, `\mathcal{C}`,
  `\ell`); the rendered pages show them correctly (pages 4, 8 and 9 checked visually).
- Template checklist: sample comments (`longmktitle` not needed, the front matter fits page 1; `\nocite{*}` and
  `\clearpage` removed): done. Guide for authors: title page, abstract, keywords, acknowledgments position, numbered
  alphabetical references with DOIs, figures as separate files in the zip: done; open: funding, competing interests,
  data statement, highlights, AI declaration, figure resolution, fonts (see "Open items"). Corrected 2026-10-09
  after the review: the abstract was checked only for its length, not for the content the guide asks for (open item
  9); the figures were not checked for being cited in the text or for captions with a description (open item 8);
  the books had no DOIs (added 2026-10-09); the math rules of the guide were not checked (open item 10).
- Package: `package-project.ps1 -Project clanok-1-min-cut-path -Template els-cas -Flat`: `Verdict: PASS`; `[layout]`:
  none; `[fonts]` 4 (Type 3); `[comment]` 9 (harmless); `[unused]` none. The zip and the packaged PDF contain no
  mention of AI tools, of this workspace or of local paths (checked).
- Package with the no-trace packager (2026-10-08, 18:26; `scripts/package-project.ps1` now scans everything sent,
  the decoded draw.io copies in the PNG files included, and checks `templates/SOURCES.tsv`): `-Template els-cas
  -CheckOnly` `Verdict: PASS`; full run `-Template els-cas -Flat` `Verdict: PASS`, `clanok-1-min-cut-path-20261008-flat.zip` (24 files) with
  `clanok-1-min-cut-path-20261008.pdf` (17 pages); `Template origin: els-cas (venue, ...)`; `Trace scan: 23 files,
  0 hits (0 allowed)`; findings `[fonts]` 4, `[comment]` 9, `[ai-declaration]` 1 (advisory). No project file needed
  a change. Run without `-Flat`: `Verdict: PASS`, `clanok-1-min-cut-path-20261008.zip`. Independent check of the
  unpacked flat zip and the PDF (`grep`, `pdfinfo`, `pdfinfo -meta`, `pdftotext`, decoded PNG text chunks): no AI
  tool name, no workspace path, no user name. `build-project.ps1`: `Package check (static): Verdict: PASS; 1
  finding(s)`.
- Text in sections/: changed only layout markup: `\begin{figure}[H]` → `\begin{figure}[pos=H]` in
  `sections/03-np-completeness.tex` lines 74, 102, 133, 165, 207 and `sections/04-diameter-two.tex` line 124;
  `sections/90-acknowledgment.tex` renamed to `90-acknowledgments.tex` (content unchanged). Line endings of the two
  edited files are now LF like the rest of the project.
- New: `submission/ai-declaration.tex` (draft of Elsevier's AI declaration for the author; not in the manuscript,
  not packaged).

**2026-10-08 - bibliography synchronized with the canonical file**
- `references.bib`: the 12 entries are now identical to `knowledge/bibliography/references.bib`; header in English;
  author names with diacritics written as LaTeX escapes (Bollobás, Frieze–Karoński), printed output unchanged.
- One visible change in the PDF: the Nagamochi–Kameda reference now ends with its DOI
  `10.15807/jorsj.39.135` (Crossref record, resolves to J-STAGE). The extracted text of the paper before and after
  differs in that line only; still 23 pages.
- `.\scripts\check-bib.ps1 -Project clanok-1-min-cut-path`: 0 findings.

**2026-10-07 - split into files**
- The single `main.tex` became the wrapper `main.tex` plus `preamble/` and `sections/`:
  - `preamble/packages.tex`: the `\usepackage` lines (graphicx, float, amsmath, tcolorbox, etoolbox, amsthm, amssymb,
    algorithm, algpseudocode);
  - `preamble/environments.tex`: `\numberwithin`, the `\newtheorem` block and the `problem` tcolorbox;
  - `preamble/macros.tex`: the notation block (`\cp`, `\CP`, `\diam`, `\OPT`, `\MinCutPath`, `\SSP`, `\ThreeSAT`);
  - `sections/00-abstract.tex` … `07-conclusion.tex` and `90-acknowledgment.tex`: the text, verbatim;
  - `main.tex` keeps the class-dependent lines: `\documentclass`, `inputenc`, `\let\openbox\relax`, `\let\Bbbk\relax`,
    `\AtBeginEnvironment{algorithmic}{\setstretch{1}}`, title, author, the abstract and acknowledgment wrappers,
    `\bibliography`.
- The PDF is unchanged: the 23 page renders have identical SHA-256 hashes (`archives/test-evidence/2026-10-08/split-before-hashes.txt` vs
  `split-after-hashes.txt`) and the extracted text is identical (`split-before.txt` vs `split-after.txt`, same folder);
  re-checked 2026-10-08.
- The single-file version is archived at `archives/removed-from-projects/clanok-1-min-cut-path/main-before-split-2026-10-07.tex`.

**2026-10-07 - stylistic revision (second round)**
- Repetitions removed: the definition of cut-path no longer appears three times (the problem boxes refer to
  Definition II.1), doubled introductory sentences before definitions and theorems, the free-standing sentence
  "Without loss of generality… `L = ∅`".
- Shortened wordy phrasings (*It is a well-established result…*, *Building on the structural insights…*, *For a better
  understanding…*), statements of theorems and lemmas without "Formally:" where the formula only repeated the text.
- Uniform: *graphs of diameter two* (in words), *minimum cut-value*, `G(n, p)` (without `p(n)`), heading *Erdős–Rényi*
  with a dash, subheadings in proofs (`\paragraph{…}` with a period, the same names of steps in both NP-completeness
  proofs), figure captions.
- Parameters of the procedure `Thread` renamed to `(K_1, σ_1), …, (K_t, σ_t)`, so that they do not clash with the links
  `L_i`, the literal links `L_{j,k}` and the clause index `k`.
- Section VI: first the theorem on diameter 2, only then its consequence for Min Cut-Path (originally the other way round).
- Acknowledgment without bold type.
- The article has 23 pages.

**2026-10-07 - revision**
- Formal: removed a paragraph from the master's thesis referring to a nonexistent figure; caption for the figure of
  link types of the chain + a reference to it in the text; figures taken out of definitions; `\deg`, `\[ … \]`,
  removed `\Bigr.`; `c(v,v)` → `c(u,v)`; "Chapter/This chapter" → sections; QED marks at the ends of proofs
  (`\qedhere`); an opening sentence of the proof, so that "Proof." does not jump into the algorithm.
- Consistency: notation via macros (`\cp`, `\CP`), `CP(u,v)` everywhere; "Lemma~\ref"; labels according to the
  convention (`sec:`, `def:`, `lem:`, `thm:`, `fig:`); heading of section IV; uniform `$…$`.
- Language: typos and grammar in the whole text (e.g. *egde*, *prove show*, *a Average*, *for large random.*, *More
  Formally*, *Firstly/Secondly* → *First/Second*, missing dashes and articles), removed doubled sentences.
- Preamble: removed unused packages of the template (`textcomp`, `mhchem`, `siunitx`, `longtable`, `tabularx`,
  `fancyvrb`, `listings`, `subcaption`).
- Figures renamed: `chain_threads` → `chain-threads`, `chain_link` → `chain-link`, `Chain_link_example` →
  `chain-link-types`, `Threading` → `threading`, `2_diam_2` → `diameter-two-structure`.
- Bibliography (everything verified against the DOI / publisher page):
  | Entry | Correction |
  |---|---|
  | Mehlhorn, Neumann, Schmidt | journal *Algorithmica* 77(2), 309–335, 2017 (originally ACM TALG 12(1), 2016); key `Mehlhorn2017Certifying` |
  | Gomory, Hu | DOI `10.1137/0109047` (originally `…045`) |
  | Cormen et al. | ISBN 978-0-262-04630-5 (the original had an invalid check digit) |
  | Diestel | the 6th edition appeared in 2025, ISBN 978-3-662-70106-5 (originally 2023 and an invalid ISBN); key `Diestel2025` |
  | Frieze, Karoński | ISBN 978-1-107-11850-8 |
  | Godsil, Royle | ISBN 978-0-387-95220-8 |
  | Bollobás | added the series Cambridge Studies in Advanced Mathematics 73 |
  | Cook | type `@inproceedings`, key in `\cite` identical to the `.bib` |
  | Micheľ 2025 | new entry - master's thesis |
  | Itai–Shiloach, Henzinger et al., Nagamochi–Kameda | verified, data unchanged (Nagamochi–Kameda: DOI added 2026-10-08, see above) |

**2026-10-07 - import from Overleaf**
- `sample.bib` → `references.bib` (sample AIAA entries removed); `graph.jpg` (sample figure of the template) to the archive.
- Added to the preamble: `\let\openbox\relax` and `\let\Bbbk\relax` (conflict of `newtxmath` with `amsthm`/`amssymb`,
  which Overleaf skips).
- 25 MiKTeX packages installed: `newtx`, `xpatch`, `xstring`, `carlisle`, `binhex`, `footmisc`, `setspace`, `abstract`, `preprint`,
  `titlesec`, `lettrine`, `caption`, `quoting`, `natbib`, `mhchem`, `chemgreek`, `siunitx`, `translations`, `amscls`, `algorithmicx`,
  `algorithms`, `float`, `fancyvrb`, `txfonts`, `tex-gyre`. On another computer they have to be installed again (`-InstallMissing`).
