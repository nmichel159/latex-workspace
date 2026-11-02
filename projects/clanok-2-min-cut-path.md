# Article 2 - Min Cut-Path: NP-Complete on Diameter Three, Polynomial for Distance or Cut-Value Two

There are two articles on Min Cut-Path: article 1, and this one. On 2026-11-02 the author decided that the former projects `clanok-2` and `clanok-3` are one article, and they were merged here.
Status: **37 pages, 13,200 words, 12 figures, 1 table.** Reviewed by AI agents, not read by the author. `main.tex` is the source.
The manuscript of 2026-10-12 with its notes and change history is in `archives/removed-from-projects/clanok-2-min-cut-path/2026-11-02-before-merge/`.
Only there, and left out on the author's request of 2026-10-31: Theorem 17 `thm:hardness` (NP-completeness for pairs with cut-value two), Proposition 12 `prop:lengths`.

Sections: 1 Introduction (with `thm:main`), 2 Preliminaries, 3 NP-completeness on diameter three (`thm:dt-hardness`), 4 Pairs with cut-value at most two (squares, `thm:linear-time`), 5 Zigzag problem (`thm:zz-reduction`, `lem:zz-valid`), 6 Polynomial algorithm (`thm:pa-formulas`, `thm:pa-open-case`: `O(n^30)`), 7 Conclusion.
Results of article 1 are only cited, on the author's request. Sections 5 and 6 are written directly on the preorder (no bridge-free graph, no multigraph with ears, no switch form).

Checks: build clean, no undefined reference, no overfull line. Package check `-Template sn-jnl -Flat -KeepComments -CheckOnly`: `Verdict: PASS`, 1 finding (`[ai-declaration]`). `check-text.ps1`: 3 findings kept (the logged "to the best of our knowledge"; "Vital" in a problem name; the sample's "Acknowledgements"). `check-bib.ps1`: 1 recommended (no issue number for `LeLe2019MatchingCut`).

## Files

`projects/clanok-2-min-cut-path/` is what is sent: `main.tex`, `references.bib`, `sn-jnl.cls`, `sn-mathphys-num.bst`, 12 figure PDFs. Beside it, in `projects/clanok-2-min-cut-path.submission/`, never sent:

| Path | Contents |
|---|---|
| `review/` | `referee-article.md` (Sections 1 to 4), `referee-direct.md` (Sections 5 and 6), `referee-math.md` (the manuscript of 2026-10-12) |
| `checks/` | `README.md` and `check_*.py`: squares; `zz_*.py`, `run_*.py`, `runs/`: the proof of Sections 5 and 6; `example_zz.py`: the example and `rem:zz-no-p2` |
| `figures/` | TikZ sources and `README.md` |
| `drafts/`, `SPEC.md`, `SPEC-merged.md`, `integration-notes.md`, `ai-declaration.tex` | history of the text; the AI-declaration draft still says seven figures |
| `open-cases/` | research on the open case, `status.md` |
| `elegant/` | search for more elegant proofs: `brief.md` and unfinished reports of the solvers |

## Reviews

- Sections 1 to 4: `review/referee-article.md`: no gap, 3 easily repaired errors and 8 minor points, all applied.
- Sections 5 and 6: `review/referee-direct.md` with programs in `checks/`: **holds, no gap and no error, 5 minor remarks, applied** (M3 needed nothing). Limits are in its Section 5: the enumeration itself is not run, and Stage 1 was reached only from planted layouts, so the verdict rests on the hand check.
- After the verdict, two changes to what the referee read: Shape B now uses five classes (the referee's own suggestion, so 28 elements instead of 31), and the time is stated as `O(n^30)` with `O(n^5)` for the reduction, counted by hand. `checks/run_final.py` runs exactly these constants: 600 runs, Shape A 300, Shape B 150, `FAILURES: none`. A second referee has not read these two changes.

## Next steps

1. The author reads the article.
2. The search for more elegant proofs and a smaller exponent is stopped on the author's request and resumes when the author says so: `elegant/brief.md`, reports `walk-dp.md`, `min-formula.md`, `frames.md`, programs beside them, nothing yet from `squares`. Nothing in them is reviewed, and they do not change the article.
3. Optional, from `referee-direct.md` Section 6: margin 4 instead of 6 would give 26 elements with one more case in `(star)`; one flow gives the whole preorder. Not applied, because neither makes the proof simpler.

## Intent

| | |
|---|---|
| Type | journal article, theory (graph algorithms) |
| Language | English (American spelling) |
| Author's plan (2026-10-31) | NP-completeness only for diameter three; then "diam or cut 2" is in P by two proofs, the squares for `c <= 2` and ZZ + P2 for `d = 2`, `c >= 3`; then improvement and simpler proofs. What is in article 1 is at most cited, never restated with its proof |
| Class | `sn-jnl` (template 3.1), options `pdflatex,sn-mathphys-num`; `sn-jnl.cls`, `sn-mathphys-num.bst` byte-identical to `templates/sn-jnl/` |
| Target journal | Algorithmica (Springer), the author's request of 2026-10-08, made for the former article 2; venue card `knowledge/venues/algorithmica.md`; to be confirmed for the merged text |
| Sources | Section 3.3 of the master's thesis; `open-cases/` (`theory-hardness.md`, `r7-desc.md`, reviews in `verify/`) |

The four answers of `knowledge/writing/paper-structure.md` §1:

| Question | Answer |
|---|---|
| **Main claim** | Min Cut-Path is NP-complete on graphs of diameter three, and solvable in polynomial time on graphs in which every pair has distance or cut-value at most two |
| **Contributions** | (1) NP-completeness on diameter three, already for `d(u,v) = 2`. (2) Linear time for pairs with `c <= 2` (squares). (3) Reduction of pairs with `d = 2`, `c >= 3` to the zigzag problem ZZ + P2. (4) Polynomial algorithm for ZZ + P2 |
| **Closest work** | article 1, the master's thesis; minimum cuts: Picard and Queyranne; searches in `knowledge/literature/searches.md`, rows "article 2" |
| **Reader and venue** | researchers in graph algorithms and connectivity |

## Open points for the author

1. **Read the manuscript.** Everything is AI-written and AI-reviewed so far.
2. **Title.** The title also stands in `\hypersetup{pdftitle=...}`: change both. The CV lists the working title *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem*; reconcile it once the title is final.
3. **Declarations.** Placeholders for Funding, Competing interests and Author contribution.
4. **AI-use statement.** Required; draft `ai-declaration.tex`, to be updated. The sentence "the author reviewed ..." can be signed only after item 1. All figures are TikZ written by the assistant.
5. **Article 1 must be public before submission** (`Michel2026MinCutPath`, "Manuscript"), because `lem:basic-bounds`, half of `lem:minimum-cuts` and five further results are only cited from it. Recheck the numbers against the public version: Lemma 2.3, Theorems 3.10, 3.11, 5.5, 6.2, 8.4, Lemmas 5.4, 6.1. `lem:basic-bounds` cites proofs of article 1, because two of its clauses are not stated there; stating them in Lemma 2.3 of article 1 would shift no number and allow a plain citation.
6. **Reference order, figure file names and format, `[referee]` option, placement of the acknowledgements:** see "Known problems".

## Preamble additions


Everything is in `main.tex` at the places the sample provides; no layout override.

| Addition | Where | Why |
|---|---|---|
| `\RequirePackage{float}` | before the active `\documentclass` line | the class loads hyperref; `float`, loaded later by `algorithm`, would write every float anchor twice (pdfTeX "destination with the same identifier"). With the line: no such message for 7 figures and 1 algorithm |
| `\usepackage[T1]{fontenc}` | first line of the package block (since 2026-10-08) | "Known problems" |
| `\usepackage{thmtools}`, `\usepackage[capitalise,noabbrev]{cleveref}` | after the sample's package block | references by `\cref` |
| sample's `\newtheorem{proposition}[theorem]{Proposition}` commented out; `\declaretheorem[name=..., style=thmstyleone, sibling=theorem]` for `proposition`, `lemma`, `corollary` | the sample's theorem block; `theorem`, `example`, `remark`, `definition` keep the sample's `\newtheorem` lines and its numbering scheme | **route chosen after a test.** Plain route (cleveref, `\newtheorem{lemma}[theorem]{Lemma}`): builds, but `\cref` prints "Theorem 6(iii)" for Lemma 6 and "Theorem 5(ii)" for Proposition 5, because the class loads hyperref before amsthm and cleveref then cannot tell environments on a shared counter apart. With `thmtools`: "Lemma 6(iii)", "Proposition 5", "Corollary 13", "Lemmas 6 to 8" (checked in the PDF text). `thmtools` was installed already |
| `\algrenewcommand\algorithmicrequire{\textbf{Input:}}`, `\algrenewcommand\algorithmicensure{\textbf{Output:}}` | after the theorem block | the algorithm states input and output |
| `\cp`, `\DC`, `\MinCutPath`, `\SSP` | after them | notation (`\CP` is not used and not defined) |
| `\hypersetup{pdftitle=..., pdfauthor=...}` | after them | the class leaves both empty; `pdfinfo`: title and "Norbert Micheľ" |

Also `\newcommand` lines for `\PathInMinCut`, `\dn`, `\upp`, `\pos`, `\MB`, `\MA`, `\Pos`, `\win`, `\FR`, `\ER`, `\EP`.

## Build and checks


```powershell
.\scripts\build-project.ps1 -Project clanok-2-min-cut-path
.\scripts\check-text.ps1 -Project clanok-2-min-cut-path
.\scripts\check-bib.ps1 -Project clanok-2-min-cut-path
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments -CheckOnly    # after a structural change
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments               # before the folder is sent
```

`-Flat`: Springer Nature asks for all files in one directory. `-KeepComments`: the folder is sent with its comments.
No `-MaxPages`: Algorithmica states no page limit.

## Known problems

Carried over from the notes of 2026-10-12. Page and reference numbers in this section refer to that build.


- **Loose pages.** The sample sets `\raggedbottom`, and a page break before a theorem-like environment is
  preferred, so some pages end early (pages 7 and 13 of the build of 2026-10-12, both under two figures). No
  layout override was added. In the same build the statement of Theorem 15 starts at the foot of page 17 and ends
  under Algorithm 1 at the top of page 18.
- **"Figure 3" in the text, "Fig. 3" in the caption.** The class abbreviates in captions; `\cref` with the house
  options `capitalise,noabbrev` does not. Dropping `noabbrev` gives "Fig. 3" in the text and "Eq." for equations;
  not done, the author decides.
- **Algorithm 1.** Lines that do not fit (the output line, 6 and 20) continue at the left margin (`algpseudocode`
  default).
- **Abstract.** The class prints the math of the abstract in bold. It has 239 words of the 250 allowed.
- **Reference list as printed by `sn-mathphys-num.bst`:** [2] "Manuscript (2026)" (open item 5); [8] "arXiv
  preprint (2021)" without the number; [9] "pp. 6-1615" for `6:1--6:15`; [14] is a self-published book with a URL;
  the thesis entry has no handle.
- **AI declaration draft and the packager.** The packager looks for a draft in `projects/<project>/submission/`;
  the draft lies beside the folder, so the reminder says "no draft". Infrastructure, not changed.
- **T1 font encoding added to `main.tex`.** The class leaves `\RequirePackage[T1]{fontenc}` commented out; with its
  default OT1 the surname printed as "l" with a caron above instead of "ľ" and the PDF text lost every accent
  (`pdftotext`: "Michel", "Saf´arik"). The added line changes the encoding only (Computer Modern stays, Type 1 from
  `cm-super`); remove it if the journal objects.
- **Diacritics as TeX code.** Springer Nature's LaTeX page asks to write special characters as TeX code
  (`Miche\v{l}`, `Ko\v{s}ice`); the front matter and the `\hypersetup` line do, and new text should do the same.
- **Figures.** Springer Nature wants every file in one directory (the folder has no sub-folders) and Algorithmica prefers EPS for
  vector figures; the template's user manual still says the compiler "accepts only .eps", although the class's default
  option is `pdflatex`. An EPS figure (the template's `fig.eps`, tested in the modular layout) builds here: pdfLaTeX
  converts it with `epstopdf` (test: `archives/test-evidence/2026-10-09/sn-jnl-float/`). Whether submission.nature.com accepts
  PDF figures: TODO(verify); the figures are PDF. Captions print "Fig. 1" (class).
  Algorithmica's guide also asks for figure files named "Fig" plus the number (`Fig1.eps`), while the house rule
  names files by content; whether this applies to LaTeX source uploads: TODO(verify). Renaming changes every
  `\includegraphics` path.
- **Labelled lists.** In `sn-jnl` the optional argument of `enumerate` sets only the label width; the labels are fixed
  (`1.`, `(a)`, `(i)` by depth), so `\begin{enumerate}[(a)]` (article 1, thesis) silently prints `1.`. Loading
  `enumerate` or `enumitem` would replace the class's list layout. The manuscript uses plain `enumerate` only (results,
  open questions) and types the parts of statements inline as (i), (ii).
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
- **Class messages** (the pristine sample shows them too): `U/rsfs/m/n` size substitutions (from `mathrsfs` of the
  sample's package block), hyperref "Difference (4) between bookmark levels", one "Underfull \vbox (badness 10000) has
  occurred while \output is active" per page (24).
- **`\RequirePackage{float}` before `\documentclass`: in `main.tex` again since 2026-10-12** (it was left out on
  2026-10-09, when the sample's preamble was kept as it is, and came back with the first figure). The sample's block
  loads `float` (through `algorithm.sty`) after the class has loaded `hyperref`, so every figure and table anchor
  would be written twice (pdfTeX "destination with the same identifier (name{figure.1})"; the pristine sample shows
  it for each float). Loading `float` first removes it. Same fix as article 1 under `cas-sc`; not a layout change.
