# Article 1 - Min Cut-Path Problem

**Layout since 2026-10-09: the folder is what is sent.** `projects/clanok-1-min-cut-path/` holds only what the build
needs, with no sub-folders: `main.tex` (one file written from `cas-sc-template.tex`; packages, environments, macros
and the whole text are in it), `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` (byte-identical to
`templates/els-cas/`), `references.bib` and the ten figure files (one PNG, nine vector PDF; Figure 1 redrawn 2026-10-09; four figures were
added from the author's talk on 2026-10-09 and Figures 2-6 were redrawn as vector PDF the same day, see "Change history").
To send: zip the content of the folder and submit it, after `package-project.ps1 -Template els-cas -Flat
-KeepComments` ends with `Verdict: PASS` (2026-10-09, after the plain-style revision: PASS, 15 pages).
Beside the folder: these notes and `projects/clanok-1-min-cut-path.submission/` (draft AI declaration; plan for the next session: `NEXT-TASK.md`).
Still open: "Open items for the author" below (AI declaration, funding, highlights, figures, abstract) and "Content
changes to review". "Change history" names `preamble/` and `sections/` files; their content is now in `main.tex`, the
files are in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-before-flat/`.

**Session of 2026-10-10 (plan `NEXT-TASK.md`):** the statements of Sections 2-5 were checked by computation (no
failure; `projects/clanok-1-min-cut-path.submission/checks/`), the sources of Section 6 and the related work were
re-checked, Sections 3-5 were tidied (Lemma 5.1 is new as an environment, Theorem 5.1 became 5.2; the count in
Theorem 4.5 is one display; Figures 5, 8 and 10 updated). The author approved the recommended decisions the same day
("súhlasím") and they were applied: symbols (`b`, `S`, `W`, `ALG`, index `h`), Corollaries 2.4 and 3.12, Definition 3.5,
Definition 4.2 (was Lemma 4.2), proof of Theorem 6.1, Theorem 6.6 as a bound with high probability, the 3-SAT
citation, the last question of the conclusion. 18 pages; full packager run `Verdict: PASS`. Report, what was applied
and what is still open: `projects/clanok-1-min-cut-path.submission/session-2026-10-10/REPORT.md`.
After the referee review (same day) the reasons asked for by the reviewer were added and, with the author's approval,
its proposals 1-8: Corollary 4.7, Lemma 5.1 as an equivalence, Section 5 "Cactus Graphs", Example 5.3 with Figure 11,
new abstract sentences and open questions. 20 pages; packager `Verdict: PASS`.
**Proof of Lemma 3.9 (Separation) rewritten 2026-10-10 (afternoon, author's request):** the paragraphs "Open
crossing edges", "Usable connecting paths", Table 1 (`tab:usable`, removed) and the case analysis are replaced by the
transition graph `\Gamma` (vertices `u`, `v` and the two paths `K^+`, `K^-` of every chain link; edges = connecting
paths, types (a)-(d)) and the new Figure 10 (`fig:transition-graph`, `transition-graph.pdf`, TikZ source in
`.submission/figures/transition-graph.tex`; drawn by the AI assistant, see open item 12). Edges of types (b), (c)
join opposite signs in one block and never remain in `G \setminus P`; the only `u`-`v` path left is a whole clause
thread, which contradicts Lemma 3.8. The former Figures 10, 11 are now 11, 12; the folder has eleven figure files.
The author must check the new argument ("Content changes to review"). 20 pages; `-CheckOnly` packager run `Verdict: PASS`.
**Draft section "Approximation and Parameterized Complexity" (2026-10-10, evening; not in `main.tex`):**
`projects/clanok-1-min-cut-path.submission/draft-approximation-parameterized.tex`. Contents: no FPTAS unless P = NP
(`thm:no-fptas`); contraction lemma `cp = min (|C| + d_C)` (`lem:contraction`, the formula of Theorem 11 of the
master's thesis); FPT with respect to `b` (`thm:fpt`) through the treewidth reduction of Marx, O'Sullivan and Razgon
and Courcelle's theorem (`lem:treewidth-reduction`, `lem:good-set`). The proof by enumeration of important cuts that
the author asked for is not valid (the left graph of Example 5.3: the only important cut gives 4, `cp = 3`), and
trying all cuts with at most `b` edges takes `|E|^{O(b)}` time, which is not FPT. The two lemmas were checked on all
connected graphs with at most six vertices (`checks/check_fpt_lemmas.py`). A preview build with the section before the
conclusion has 22 pages (`tmp/fpt-section-preview/`). **The author must check the proof of `thm:fpt` before it enters
the manuscript.** When it is inserted: add `\tw`, `\torso` to the macros and `Marx2013Separators`,
`GareyJohnson1978Strong` to `references.bib`; `GareyJohnson1978Strong` is `PARTIAL` (content not read) and its
sentence carries a `TODO(verify)`; theorem numbers of Marx et al. are those of arXiv v1; the conclusion's questions on
approximation and on FPT with respect to `b`, the abstract and the contributions then need an update.
**Independent check of the draft (2026-10-10, second pass, author's request):** every step of `thm:no-fptas`,
`lem:contraction`, `lem:good-set` and `thm:fpt` was derived again; no error found. The statements cited from Marx et
al. (Theorems 2.1, 2.2 with the paragraph on labeled graphs, Definitions 2.3, 2.5, Proposition 2.7, Corollary 2.10,
Lemma 2.11, Remarks 2.13, 2.14, the definition of FPT) were compared with the text of arXiv:1110.4765v1 and match.
Two edits in the draft, both on how the source is cited: the bounds of their Lemma 2.11 depend on `l` and `k - l`
(hence on `k`); labeled graphs are the extension stated after Theorem 2.2, not the theorem itself. `lem:good-set`
was checked once more with the literal definition of a good set (`checks/check_good_set_literal.py`, 59112
constructions, no failure). Still open: `GareyJohnson1978Strong` is unread (`TODO(verify)` stays; `thm:no-fptas`
does not depend on it); the definition of FPT asks for a computable `f` and the proof of `thm:fpt` does not say why
`f` is computable (Lemma 2.11 gives explicit recursions; TODO(verify) a source that states Courcelle's theorem with
a computable bound).
**Section 7 "Approximation and Parameterized Complexity" is in `main.tex` since 2026-10-10 (author's request).**
It is the draft without one paragraph: the two sentences on strong NP-completeness with the citation
`GareyJohnson1978Strong` stayed out, because the paper is still unread and the packager fails on a `TODO` in the
manuscript; Theorem 7.1 has its own proof. The draft with that paragraph is in
`archives/removed-from-projects/clanok-1-min-cut-path/2026-10-10-draft-section-7/`. Added with the section: macros `\tw`,
`\torso`; `Marx2013Separators` in `references.bib` (19 entries); one sentence in the abstract; "Fourth, ..." in the
contributions; one sentence in the roadmap; in the conclusion (now Section 8) the third question also asks for a
PTAS and the last one asks for time `2^{O(b)}` instead of asking whether the problem is FPT in `b`. 22 pages;
`check-text.ps1` 8 findings (the known false positives), `check-bib.ps1` 2 recommendations, packager `-CheckOnly`
`Verdict: PASS`. The section was written and checked by the AI assistant: the author must read it ("Content
changes to review", item 18) and the AI declaration must name it (open item 2).

Current numbering: Definitions 2.1, 2.2, Lemma 2.3, Corollary 2.4, Definition 2.5; Definitions 3.1-3.5, Lemmas 3.6-3.9,
Theorems 3.10 (`thm:ssp-np-complete`), 3.11 (`thm:mcp-np-complete`), Corollary 3.12; Definitions 4.1, 4.2, Lemmas 4.3,
4.4, Theorem 4.5, Remark 4.6, Corollary 4.7; Lemma 5.1, Theorem 5.2, Example 5.3; Theorems 6.1-6.3, Lemmas 6.4, 6.5,
Theorem 6.6; Theorem 7.1 (`thm:no-fptas`), Lemmas 7.2 (`lem:contraction`), 7.3 (`lem:treewidth-reduction`), 7.4
(`lem:good-set`), Theorem 7.5 (`thm:fpt`), equation (7.1) (`eq:cut-separator`). Older notes
below, the session report and the files in `checks/` use the numbers of their day (before the approval: Lemmas
3.5-3.8, Theorems 3.9, 3.10, Lemma 4.2, Definition 2.4).

**Preserving revision of 2026-10-09 (evening):** the whole text was tidied without removing content; Section 3
is reorganized into construction (Algorithm 1 outside the proof) and Lemmas 3.5-3.8 before Theorem 3.9; seven
verified references added (18 entries); Figure 10 is vector (all figures are vector now). 19 pages. Report, change
logs and the open mathematical issues for the author:
`projects/clanok-1-min-cut-path.submission/revision-2026-10-09/REPORT.md`. Original:
`archives/removed-from-projects/clanok-1-min-cut-path/main-before-preserving-revision-2026-10-09.tex`.
Label and numbering notes below that predate this revision (Theorem 3.5 = SSP, figure list, `.png`) are outdated:
Theorem 3.9 is `thm:ssp-np-complete`, Theorem 3.10 `thm:mcp-np-complete`; Figure 10 is `diameter-two-structure.pdf`.

## Intent

| | |
|---|---|
| Type | journal article (manuscript) |
| Language | English (American spelling) |
| Main file | `main.tex` (the whole manuscript in one file, written from `cas-sc-template.tex`) |
| Target journal | Discrete Applied Mathematics (Elsevier), article type *Contribution* (more than 10 pages); venue card [knowledge/venues/discrete-applied-mathematics.md](../knowledge/venues/discrete-applied-mathematics.md) |
| Class | `cas-sc.cls` (Elsevier CAS bundle 2.4, single column; `\ProvidesClass`: `cas-sc 2024/05/04, 2.4`) with `cas-common.sty`; bibliography `cas-model2-names.bst` via `\usepackage[numbers,sort&compress]{natbib}` |
| Template folder | `templates/els-cas/` (the official template the DAM guide for authors links; download URL and SHA-256 in `templates/SOURCES.tsv`); `cas-sc.cls`, `cas-common.sty` and `cas-model2-names.bst` here are byte-identical to it (SHA-256 compared 2026-10-08) and are never edited in the project; `main.tex` is written from `cas-sc-template.tex` |
| Bibliography | `references.bib` (19 entries, all cited and verified; the master's thesis is not cited since 2026-10-09, author's decision) |
| Origin | Overleaf export `archives/clanok_1_min_cut_path.zip` (2026-10-07); class `new-aiaa` until 2026-10-08 |
| Knowledge base | [knowledge/research/min-cut-path.md](../knowledge/research/min-cut-path.md) |

## Status

Ported to the DAM template on 2026-10-08 and adjusted after the review of 2026-10-08 on 2026-10-09 (porting log and
review fixes in "Change history"). Four figures (three from the author's talk, one new) were added on 2026-10-09 (10 figures in
total). Builds with exit code 0: 15 pages (paper 192 x 262 mm, the class's own page
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
   characters each; drafted 2026-10-10 in `projects/clanok-1-min-cut-path.submission/highlights.txt` (five lines, at
   most 78 characters), to be confirmed.
7. **Figures (Figures 2-6 redrawn as vector PDF on 2026-10-09; open only for
   `diameter-two-structure.png`; Figure 1 `cut-path` was redrawn too):** DAM asks for vector drawings (EPS/PDF) or bitmapped line drawings of at least 1000 dpi; the seven
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
9. **Abstract: rewritten 2026-10-09** (it now states the three results; check it, "Content changes to review"
   item 17). Before that: (DAM guide, "Abstract": state the purpose, the basic procedures, the main findings and the principal
   conclusions): the abstract gives only the motivation; NP-completeness, `cp = c + d − 1` for diameter two and
   cut-value at most two, and the random-graph results are missing (also "Known problems", Assessment item 3).
   Rewriting it is the author's decision.
10. **Math notation** (DAM guide, "Math formulae": the solidus for small fractional terms, powers of e written with
    exp): inline `\frac` in Section 6 of `main.tex` (`$p = \frac{1}{\alpha}$`, `$p = \frac{\alpha \log n}{n}$`
    and the same fraction in running text) and `e^{-\mu h(a)}` in two displays of the same section. Possible forms:
    `1/\alpha`, `\alpha\log n/n`, `\exp(-\mu h(a))`; notation changes are the author's decision. Elsevier typesets
    accepted articles itself, so this is a style point, not a blocker.
11. **Year of Frieze–Karoński** (bibliography): settled 2026-10-10. The imprint page of the printed book reads
    "First published 2016" (Google Books preview; note in the canonical `.bib`); the entry keeps 2016. Open instead:
    the entry's `url` points to the authors' PDF of 2026, whose numbering differs from the printed book
    (`session-2026-10-10/REPORT.md`, decision 12).
12. **AI use in the figures** (since 2026-10-09; Figures 2-6 (`chain-threads`, `chain-link`, `chain`,
    `chain-link-types`, `threading`) are since that day also TikZ drawings written by the AI assistant, redrawn
    from the author's PNG drawings, and are not yet named in the draft declaration): Figures 7, 8 and 9 (`fig:two-synchronization`,
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
| 7 Approximation and Parameterized Complexity | `sec:approx-param` | no FPTAS unless P = NP (`sec:approximation`); `cp = min (\|C\| + d_C)`, treewidth reduction, FPT in the threshold `b` (`sec:fpt`) |
| 8 Conclusion | `sec:conclusion` | summary, further directions |

Section numbers are arabic since the port (the class `new-aiaa` printed I-VII): Section III is now Section 3,
Theorem III.5 is Theorem 3.5, Lemma II.4 is Lemma 2.4, and so on; the order is unchanged. The Roman numbers in
"Known problems" and "Content changes to review" below refer to the PDF before the port, and so do their citation
numbers: the reference list is now alphabetical, so the old [9] (Bollobás) is [1], [10] (Frieze–Karoński) is [5],
[3] (Mehlhorn et al.) is [10] and [5] (master's thesis) is [11].

Figures (number on 2026-10-09, label, file, section): 1 `fig:cut-path` `cut-path.pdf` (2); 2 `fig:chain-threads`
`chain-threads.pdf`, 3 `fig:chain-link` `chain-link.pdf`, 4 `fig:chain` `chain.pdf`, 5 `fig:chain-link-types`
`chain-link-types.pdf`, 6 `fig:threading` `threading.pdf`, 7 `fig:two-synchronization`
`two-synchronization-threads.pdf`, 8 `fig:three-synchronization` `three-synchronization-threads.pdf`,
9 `fig:clause-thread` `clause-thread.pdf` (all 3; Figures 7-9 stand inside the numbered list of thread types);
10 `fig:diameter-two-structure` `diameter-two-structure.png` (4).

Labels of statements: `def:cut-path`, `def:cp-value`, `lem:basic-bounds`, `cor:two-approximation`,
`def:approximation-scheme`, `def:chain-link`, `def:chain`, `def:thread`, `def:threading`, `alg:reduction`,
`def:chain-path`, `lem:chain-paths`, `lem:synchronization`, `lem:clause-threads`, `lem:separating`, `tab:usable`,
`thm:ssp-np-complete`, `thm:mcp-np-complete`, `cor:lower-bound-attained`, `def:diameter`,
`def:cut-decomposition` (was `lem:cut-decomposition`), `lem:empty-i-or-l`, `lem:odd-intersection`, `thm:diameter-two`, `rem:algorithm`, `lem:cactus`
(new 2026-10-10), `thm:cut-two`, `thm:random-diameter-two`, `thm:random-diameter`, `thm:random-connectivity`,
`lem:degree-bounds`, `lem:connectivity-bounds`, `thm:approximation-scheme`, `thm:no-fptas`, `lem:contraction`,
`lem:treewidth-reduction`, `eq:cut-separator`, `lem:good-set`, `thm:fpt`.

### Notation table (2026-10-10)

Occurrences are counted in the math of `main.tex` by section (rough; script of the session, not kept). "Clash" names
another meaning of the same letter; the decisions are in `session-2026-10-10/REPORT.md`, decision 1.
The table shows the state before the approval. Applied since: the threshold is `b`; a cut-path is always `S` (`F` is
gone; the set `C \cap P` of Lemma 4.4 has no name; `\deg(x, W)`); the algorithm is `\ALG` and the instance sets are
`\mathcal{I}(n)`, `\mathcal{I}_{\ALG}^{\mathrm{opt}}(n)`; the index of `Thread` is `h`. Kept by decision: clauses
`C_k`, parts `I, J, K, L`, `n`, `p`, `q`.

| Symbol | Meaning | Defined | Uses (section: count) | Clash |
|---|---|---|---|---|
| `G = (V, E)`, `u`, `v` | graph, the two distinguished vertices | Section 2 | everywhere | - |
| `d(u,v)`, `c(u,v)`, `\cp(u,v)` | distance, cut-value, size of a minimum cut-path | Section 2, Definition 2.2 | everywhere | - |
| `P`, `Q` | `u`-`v` path; a second `u`-`v` path | Section 2; Lemmas 3.5, 3.8 | `Q` 3: 14 | - |
| `C` | `u`-`v` cut | Section 2 | 2: 10, 4: 33 | clauses `C_k` (3: 20), `\mathcal{C}` (3: 5) |
| `S` | cut-path | Definition 2.1 | 2: 6, 4: 12, 5: 2, 6: 3 | `S = C \cap P` (proof of Lemma 4.4), vertex set in `\deg(x, S)` (proof of Theorem 4.5) |
| `F` | cut-path in the decision version | Section 3.2 | 3: 11 | same object as `S` |
| `k` | clause index | Section 3 | 3: 62 | threshold of the decision version (Section 3.2), bound in Definition 4.1 (4: 3), budget of other problems (1: 2) |
| `n`, `m` | numbers of variables and clauses | Section 3 (declared) | 3: 17, 14 | `n` = number of vertices in Sections 1, 2, 6 (67) |
| `i`, `j` | variable index, position of a literal | Section 3 | - | `i` also indexes `H_i`, `L_i` (Definition 3.2) and `Z_i` (Section 5) |
| `r` | number of chain links | Definition 3.2 | 3: 12 (both meanings) | index of `Thread` (`K_r`, `\sigma_r`) |
| `t` | number of links of a thread | `Thread` | 3: 7 | number of cycles `Z_1, \dots, Z_t` (5: 3) |
| `p`, `q`; `p_i`, `q_i` | ends of a chain link | Definitions 3.1, 3.2 | 3: 9 | `p` = edge probability (6: 17) |
| `L`; `L_i` | a chain link; the `i`-th link | Definitions 3.1-3.4 | 3: 13 | part `L` of Section 4 (4: 13) |
| `I_i`, `T_i`, `L_{j,k}` | initialization, terminal, literal chain link | Section 3.1.1 | 3: 28, 26, about 45 | parts `I`, `L` of Section 4; `I(n)` |
| `K_1, \dots, K_t`, `\sigma_r` | links and signs passed to `Thread` | Section 3.1.2 | 3: 8 | part `K` of Section 4 (4: 28) |
| `H_i` | single edges of a chain | Definition 3.2 | 3: 4 | `h(a)` (Lemma 6.4) |
| `z_1, z_2`, `e = \{x, y\}` | new vertices and the subdivided edge | Definition 3.4 | 3 | - |
| `\mathcal{M}`, `\mathit{Lits}`, `\ell[0]`, `\ell[1]`, `s(\ell)` | map of literals, list, position of a literal, sign | Section 3.1.2 | 3 | author's notation, kept |
| `\Lambda` | number of edges of a chain path | `Calibrate` | 3: 10 | - |
| `\tau` | truth assignment | 3-SAT | 3: 24 | - |
| `A`; `A_1`, `A_2` | vertex set of a side; the two sides of a cut | Section 2; Lemma 4.2 | 2: 2, 4: 7; 4: 46 | algorithm `A` of Definition 2.4 (2: 7) |
| `I, J, K, L` | parts of the sides (incident to the cut or not) | Lemma 4.2 | 4: 19, 18, 28, 13 | see `I_i`, `K_r`, `L` |
| `\deg(x, S)` | number of neighbors of `x` in `S` | proof of Theorem 4.5 | 4: 8 | `S` |
| `Z_1, \dots, Z_t` | cycles met by `P` | proof of Theorem 5.2 | 5: 16 | - |
| `I(n)`, `I_A^{\mathrm{opt}}(n)`, `X`, `\OPT(X)` | instances of size `n`, good instances, an instance, its optimum | Section 2, Definition 2.4 | 2: 7, 8, 3; 6: 3, 2 | `I` |
| `G(n,p)`, `\alpha`, `\beta_1`, `\mu`, `a`, `a_1`, `h(a)` | random graph, constants of Section 6 | Section 6 | 6 | `a`, `b` are vertices in the proof of Lemma 4.3 |
| `V(G)`, `\delta(G)` | vertex set and minimum degree of the random graph | Section 6 | 6: 2, 3 | `V(G)` only twice |
| `\epsilon` | accuracy of the approximation | Definition 2.4 | 0: 2, 1: 1, 2: 5, 6: 5 | house rule prefers `\varepsilon` |

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
chain.pdf, chain-link.pdf, chain-link-types.pdf, chain-threads.pdf, threading.pdf   vector figures (since 2026-10-09)
diameter-two-structure.png  figure (bitmap)
cut-path.pdf                vector figure, redrawn from the talk's bitmap (since 2026-10-09)
two-synchronization-threads.pdf, three-synchronization-threads.pdf, clause-thread.pdf
                            vector figures (since 2026-10-09)

beside the folder (never sent)
projects/clanok-1-min-cut-path.md                              these notes
projects/clanok-1-min-cut-path.submission/ai-declaration.tex   draft AI declaration for the author
projects/clanok-1-min-cut-path.submission/figures/*.tex        TikZ sources of the eight vector figures and of the
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

Send only on `Verdict: PASS`. Last run 2026-10-10, 11:35, after the approved decisions (`-Template els-cas -Flat
-KeepComments`): `Verdict: PASS`, 18 pages, 16 files in the zip, `Trace scan: 15 files, 0 hits (0 allowed)`. Run of
10:05 the same day: `Verdict: PASS`, 17 pages, 16 files in the zip, `Trace scan: 15 files, 0 hits (0 allowed)`, 22 comment lines kept, one advisory finding
`[ai-declaration]`. Run of 2026-10-09, 09:47, after the plain-style revision: `Verdict: PASS`, 15 pages, `Trace scan: 15 files, 0 hits (0 allowed); 3 files identical to the
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

### Review of 2026-10-09 (read-through of `main.tex`, nothing changed)

Build clean (15 pages), `check-text.ps1` 2 findings, `check-bib.ps1` 0. New findings, line numbers of `main.tex`:

- **Proofs missing:** Lemma 4.2 (l.728) and Lemma 4.3 (l.744) have no `proof`; the argument for 4.3 is the
  sentence before it (l.741).
- **Proof of Theorem 4.5 (l.825-844):** the estimate carries `\deg(u, I)` and the first bullet calls it edges to
  the opposite side, but `u \in K` has no neighbor in `I` (said only at l.844); drop the term from the start.
  "connected graph of diameter two" (l.777) is redundant.
- **"Cut" has two meanings:** any separating edge set (Definition 2.1, l.180) and the edge boundary of a vertex
  partition (Lemmas 4.2-4.4). Lemma 4.4 needs the second. "Cut-value" (title of Section 5, l.147, l.858) is never
  defined; Section 2 says "minimum size of a cut".
- **Theorem 6.2 (l.931):** the exact bound `\diam \leq \log n / \log\log n` needs checking against the source
  (the known asymptotics is `(1+o(1)) \log n / \log(np)`); the proof of Theorem 6.6 only needs
  `O(\log n / \log\log n)`. **Theorem 6.3 (l.940):** "k-edge-connected where k = δ(G)" is better stated as
  edge connectivity equal to minimum degree. Theorems 6.1-6.3 and the Chernoff bound cite whole books; add
  theorem or page numbers (`\cite[Theorem~x]{...}`).
- **Sources:** `Cook1971Complexity` for the NP-completeness of 3-SAT (l.297): TODO(verify) that the paper
  states it for 3-SAT in this form (commonly cited: Karp 1972 or Garey-Johnson). `GodsilRoyle2001` for
  "diameter two" (l.713) and "cf." `Mehlhorn2017Certifying` for the cactus structure (l.860) are loose. "These
  papers" (l.137) includes a textbook. `Frieze2016` prints a DOI and a URL to the author's PDF.
- **Symbol clashes:** `n, m` (graph, l.162; formula, l.298), `C` / `C_k` / `C_i` (cut, clause, cycle l.890),
  `I, K, L` (sets of Section 4; links `I_i`, `K_i`, `L_i`; instances `I(n)`), `P` (path; polynomial l.257), `k`
  (threshold l.670, clause index, diameter l.717, connectivity l.942).
- **Language and consistency:** "the value of the minimum cut-path" (l.778, l.866) -> "a minimum cut-path";
  "at least 3" (l.808) vs "at least three" (l.831); "converges to 1" (l.913) vs "tending to one"; "Then:" before
  a display (l.929, l.938); `\textbf{Reduction.}` etc. in the proof of Theorem 3.6 (l.684-703) vs `\paragraph` in
  Theorem 3.5; "BFS or DFS" (l.700) vs "breadth-first search" (l.657); "unless otherwise stated" (l.161) with no
  exception later; `G' := G` (l.687) is not needed; l.686 repeats the assumption of l.167; l.1006 states
  Theorem 6.6 before the theorem; "Third, this work is purely theoretical" (l.1055) is not a question;
  Definition 3.1 (l.361) speaks of a chain before Definition 3.2; Definition 3.3 item 2 (l.442) defines a thread
  through "every other thread".
- **Front and back matter:** academic titles in the acknowledgments (l.1063; English journals print the name
  only); the e-mail is a student-number address (l.94); unused environments `claim`, `corollary`, `proposition`,
  `example` (l.29-35).

Full review with all findings by section and an order of work:
`projects/clanok-1-min-cut-path.submission/review-2026-10-09.md`.

Rewrite proposals of the same day (second pass, nothing changed; the author decides):

- **Section 3.1, construction and proof of Theorem 3.5.** The construction is spread over five places (thread
  types l.470-505, which already assert what the threads force; procedures l.510-519; Algorithm 1 inside the
  `proof`, l.548; "In words", l.579; `Calibrate`). Proposal: one static "Construction" of the graph before the
  theorem, then four lemmas (shortest paths are exactly the chain paths; hits all synchronization threads iff
  consistent; hits all clause threads iff the assignment satisfies; consistent and satisfying implies separating),
  and a proof of the theorem of a few lines. Algorithm 1 either goes or stays outside the proof as a summary.
  The "separating" step (l.627-645) follows a walk from `u` case by case; a set argument is tighter: name the
  set `X` of vertices (first connecting paths, unused paths of the `I_i`, unused paths of the literal links before
  the first satisfied literal of each clause, the dead ends attached to them), show that no edge of `G \setminus P`
  leaves `X` and that `v \notin X`.
- **Section 3.2.** \textsc{Separating Shortest Path} is the question `cp(u,v) = d(u,v)`; saying so makes
  Theorem 3.6 a corollary of a few lines and gives the sharper statement that deciding whether the lower bound of
  Lemma 2.4 is attained is NP-complete.
- **Section 2.** `CP(u,v)` is used only at l.197-212 (Definitions 2.2, 2.3 can be one sentence);
  `\deg(x,S)` is used only in Section 4 and Definition 2.5 only in Section 6; no example shows a cut-path smaller
  than a minimum cut plus a shortest path (the parked counterexamples would do). Lemma 2.4 gives
  `|C \cup P| < 2\,cp(u,v)`, a 2-approximation, which the article never states.
- **Section 4.** Lemma 4.2 is a definition; Lemma 4.3 can read "for every cut, all vertices of one side are
  incident to a cut edge", which removes `I, J, K, L`; the count in Theorem 4.5 then is
  `|C| \geq \deg(u, A_1) + 2 + (|A_2| - 2) \geq \deg(u) + 1`. Remark 4.6 is used as a result in Sections 5 and 6:
  a corollary.
- **Section 6.** The upper bound `\beta_2` (Lemma 6.4, Lemma 6.5, the upper Chernoff tail) is never used;
  Theorem 6.6 needs only `c(u,v) \geq \beta_1 \log n`. Stating Theorem 6.6 as "with high probability, for all
  `u, v`, `|C \cup P| \leq (1 + 1/(\beta_1 \log\log n))\,cp(u,v)`" removes Definition 2.5 and its mismatch with
  `G(n,p)`. The setting "Let `G(n,p)` be ... `\alpha > 1`" is repeated five times; `\mathbb{P}[\,]` (l.915, l.931)
  and `\mathbb{P}(\,)` (l.952, l.978) are mixed.
- **Introduction.** It does not say what selecting an edge means in the model (protected, monitored); the
  contributions carry no theorem numbers; the roadmap repeats them; no paragraph gives the idea of the reduction.

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
17. **Plain-style revision and the thesis citation (2026-10-09, on the author's instruction).**
    - Wording: formulaic passages were replaced by plain sentences in the whole text: abstract, introduction,
      the sentences that lead into definitions, lemmas and theorems, conclusion, acknowledgments
      (7128 -> 5625 words; `check-text.ps1` 77 -> 2 findings). Statements, proofs and algorithms are unchanged,
      except the wording of Definition 4.1 (diameter), now one sentence without the displayed formula.
    - Abstract: now states the results (NP-completeness, `cp = c + d - 1` in both classes, the random-graph
      result); before, it gave only the motivation.
    - Introduction: contributions and roadmap state the results; the conclusion lists four open questions.
    - Thesis: the master's thesis is no longer cited (entry removed from `references.bib`). Gone with it: the
      sentences that the problem was introduced there, that the results on graph classes and random graphs
      first appeared there, and that partial results for the class "diam or cut 2" were obtained there. The
      introduction now reads "To the best of our knowledge, the problem has not been studied before."
      **Check this sentence against the thesis** and against the journal's question on prior publication.
18. **Section 7 (new, 2026-10-10): no FPTAS, FPT in the threshold `b`.** Statements and proofs were written by the
    AI assistant and checked twice (by hand, against the preprint of Marx et al., and by brute force on small
    graphs; `checks/README.md`). The proof of Theorem 7.5 rests on Lemma 2.11 of Marx, O'Sullivan and Razgon and
    on Courcelle's theorem, cited by the numbers of arXiv:1110.4765v1: compare with the journal version before
    submission. The sentences added to the abstract, the contributions, the roadmap and the conclusion are listed
    at the top of these notes.

## Change history

**2026-10-10 - Section 7 inserted (author's request)**
- `main.tex`: Section 7 from the draft (without the paragraph that cites `GareyJohnson1978Strong`), macros `\tw`,
  `\torso`, abstract, contributions, roadmap, conclusion; `references.bib`: `Marx2013Separators`. Draft retired to
  `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-10-draft-section-7/`.
- Build: 22 pages, no undefined references, BibTeX without warnings; packager `-Template els-cas -Flat
  -KeepComments -CheckOnly`: `Verdict: PASS`.

**2026-10-10 - session along `NEXT-TASK.md` (Windows, 08:35-10:30)**
- Phase B: computational checks, `projects/clanok-1-min-cut-path.submission/checks/` (`README.md` there): Algorithm 1
  as an executable model, Lemmas 3.5-3.8 and Theorem 3.9 on 5639 formulas; Lemma 2.3, Theorem 3.10, Lemmas 4.3, 4.4,
  Theorem 4.5, Lemma 5.1 and Theorem 5.2 on all graphs with at most seven vertices. No failure.
- `main.tex`: Section 1 (Most Vital Edges "with unit edge lengths"; no symbol `d` in the Matching Cut sentence);
  Section 2 (`G = (V, E)` introduced); Section 3 (plan sentence in the proofs of Lemma 3.5 and Theorem 3.9; "exactly
  `Λ` edges"); Section 4 (count of Theorem 4.5 as one display with groups (i)-(iii), `deg(u, I)` gone from the
  estimate); Section 5 (Lemma 5.1 `lem:cactus` with proof; Theorem 5.2 cites it); Section 6 (verified locations:
  `ChungLu2001` alone for Theorem 6.2, `\cite[p.~169]{Bollobas2001}` for Theorem 6.3, `\cite[Eq.~(21.19)]{Frieze2016}`,
  `\cite[Section~1.1]{Frieze2016}`; bound variable `x` in Lemma 6.4); Section 7 (diameter-three question).
- Figures: `chain-link-types.pdf` and `three-synchronization-threads.pdf` with labels `L_{j,k}` (were `L_{j,k,i}`);
  `diameter-two-structure.pdf` with the marks (i), (ii), (iii). Sources in
  `projects/clanok-1-min-cut-path.submission/figures/`; old PDFs in
  `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-10-figure-10/` and `2026-10-10-figure-labels/`.
- Sources and literature (two agents): `session-2026-10-10/sources-section-6.md`, `related-work-check.md`; canonical
  `.bib` comments, `searches.md` (14 rows), `Bazgan2019MostVital.md`, `knowledge/research/min-cut-path.md` updated.
  The same problem was not found under any name; no close paper in Discrete Applied Mathematics.
- Build: 17 pages, no undefined references; `check-text.ps1` 7 findings (known false positives); `check-bib.ps1` 2
  recommendations; packager, full run `-Template els-cas -Flat -KeepComments`: `Verdict: PASS`, 16 files,
  `Trace scan: 15 files, 0 hits`, one advisory finding `[ai-declaration]`.
- Committed on the author's request (three commits). Decisions for the author: `session-2026-10-10/REPORT.md`.

**2026-10-10 - approved decisions applied (11:00-11:40)**
- The author approved the recommendations of `session-2026-10-10/REPORT.md` in chat. Applied in `main.tex`:
  decision 1 (threshold `b`; cut-path `S` in the decision version and Theorem 3.11; `C \cap P` unnamed in Lemma 4.4;
  `\deg(x, W)`; `\ALG`, `\mathcal{I}(n)`; index `h` in `Thread`); 2 (Corollary 2.4 `cor:two-approximation` with one
  sentence on the factor two; Corollary 3.12 `cor:lower-bound-attained`); 3 (Theorem 6.6 states the bound
  `1 + 1/(\beta_1 \log\log n)` with high probability, the scheme is its "in particular"; Definition 2.5, item 3, with a
  probability; "with high probability" / "with probability tending to one" instead of "on almost all inputs"); 4
  (Definition 3.3 with two items about the path itself, the disjointness of threads as a sentence about the
  construction; Definition 3.4 "thread under construction"); 5 (Definition 4.2 instead of Lemma 4.2, items in words);
  6 (Definition 3.5: chain path, hits, consistent); 7 (Theorem 6.1 with a proof; Frieze-Karonski, Exercise 1.4.8, as
  the reference); 8 (sentence after Theorem 6.2 with the bound of Chung and Lu, cited without a theorem number); 9
  (3-SAT: Cook and Karp, padding by repeating a literal; `Karp1972Reducibility` copied into `references.bib`, 18
  entries); 10 (last question of the conclusion: fixed-parameter tractability in the threshold).
- Not applied, still the author's: title, keywords, novelty sentence, AI declaration, funding (decision 11); the `url`
  of `Frieze2016` (decision 12); the theorem number of Chung and Lu in the journal version.
- Build: 18 pages, no undefined references, BibTeX without warnings; `check-text.ps1` 8 findings (the seven known
  false positives and "Chung and Lu~\cite{...} proved", authors named); `check-bib.ps1` 2 recommendations; packager,
  full run `-Template els-cas -Flat -KeepComments`: `Verdict: PASS`, 18 pages, `Trace scan: 15 files, 0 hits`.

**2026-10-10 - referee proposals approved and applied (14:00-14:30)**
- The author approved items 1-8 of "Referee review" in `session-2026-10-10/REPORT.md`. Applied in `main.tex`:
  abstract (the intermediate question; "cactus graphs"; the bound is the size of the union of a minimum cut and a
  shortest path; "edge probability at least `α log n / n`" instead of "above the connectivity threshold");
  introduction (what is proved, in place of "settle its complexity"; both classes attain the upper bound of Lemma
  2.3); Section 2 (`cp` as the minimum over paths `P` of `|P|` plus the cut-value in `G \ P`); Section 3 (paragraph
  after Theorem 3.10: degree at most three outside `u, v`, `c(u,v) >= 2n + 7m`, `d(u,v) = Λ`); Section 4 ("diameter
  at most two" in Lemma 4.3 and Theorem 4.5; Corollary 4.7 `cor:diameter-two-degrees`: `c(u,v) = min(deg u, deg v)`,
  linear time); Section 5 (title "Cactus Graphs"; Lemma 5.1 is an equivalence with the converse proved directly;
  Theorem 5.2 stated for cactus graphs; Example 5.3 `ex:strict` with Figure 11 `fig:counterexamples`); Section 7
  (the formula fails in the candidate class; approximation below factor two instead of the question about
  experiments; bounded `c` or `d`, deciding `cp = c`).
- New files in the project folder: `counterexample-cut-two.pdf`, `counterexample-distance-two.pdf` (copies of the
  figures parked on 2026-10-09 in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-conclusion-figures/`;
  TikZ sources in `projects/clanok-1-min-cut-path.submission/figures/`). Open item 13 (parked counterexamples) is
  settled by this; the class diagram stays out.
- Corollary 4.7 checked by computation on all graphs of diameter at most two with at most seven vertices (8941 pairs).
- Not applied: the classical theorem on diameter two (attribution to Plesnik 1975 not verified, so not cited); M3,
  M4, M11; notation `l[0]`, `l[1]` and Algorithm 1 (the author's); the empty "ORCID(s):" line (class); colour-only
  cues in Figures 7, 8, 10; keywords.
- Build: 20 pages, 11 figures, no undefined references; `check-text.ps1` 8 findings (false positives); packager, full
  run: `Verdict: PASS`, 18 files, `Trace scan: 17 files, 0 hits`. Committed and pushed on the author's request.

**2026-10-10 - referee review and its justifications (13:00-13:40)**
- Independent review as a DAM referee: session-2026-10-10/referee-report.md. Verdict: major revision, borderline
  minor; no error in the mathematics. Applied in main.tex: the findings that make reasons explicit or fix wording
  (M1, M2, M5-M9, M12-M15, P3, P7; table in session-2026-10-10/REPORT.md, section Referee review). New paragraph
  The construction is well defined in Section 3.1.2; two reason sentences in the proof of Lemma 3.9; the symmetry
  behind the second renaming in the proof of Theorem 4.5; the cycles of the proof of Theorem 5.2 defined before use;
  the convention of Chung and Lu for disconnected graphs after Theorem 6.2.
- Not applied, for the author: an example with cp < c + d - 1 (the parked counterexamples), the corollary
  c(u,v) = min(deg u, deg v) for diameter two, the name cactus graphs, abstract and introduction, open questions
  (REPORT.md, same section, items 1-9).
- Build: 18 pages, no undefined references; check-text.ps1 8 findings (false positives); packager, full run:
  Verdict: PASS. Committed and pushed after the author's approval.

**2026-10-09 - preserving revision (cloud session, 16:50-17:20)**
- Four editors (front matter and Sections 1-2; Section 3; Sections 4-5 and Figure 10; Sections 6-7 and sources) and
  two reviewers (mathematics and preservation; style). Working files, inventories, change logs and issue lists:
  `projects/clanok-1-min-cut-path.submission/revision-2026-10-09/`; summary in `REPORT.md` there.
- `references.bib`: Abhinav2022NonSeparating, Bazgan2019MostVital, Bentert2025NetworkDiversion, ChungLu2001,
  Komusiewicz2020MatchingCut, LeLe2019MatchingCut, Mao2021NonSeparating copied from the canonical file.
- `diameter-two-structure.png` replaced by `diameter-two-structure.pdf` (TikZ source in
  `projects/clanok-1-min-cut-path.submission/figures/`); PNG in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-png-figures/`.
- Build (TeX Live 2023 in the cloud container): 19 pages, no undefined references; static package check PASS.
  The full packager run with `-KeepComments` was not repeated on Windows.


**2026-10-09 - Figures 2-6 redrawn as vector graphics (10:55-11:00)**
- On the author's request, `chain-threads`, `chain-link`, `chain`, `chain-link-types` and `threading` were redrawn
  in TikZ in the style of Figures 7-9 (same line widths, link size, thread color, thick crossing edge, STIX
  fonts) and are included as PDF at their natural size. Sources:
  `projects/clanok-1-min-cut-path.submission/figures/`. The five PNG files are in
  `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-png-figures/`.
- Differences from the PNG drawings: the links of Figures 3, 5 and 6 carry the signs `+`, `-` inside (as in
  Figures 7-9); in Figure 6 the links are larger than in the other figures (half-width 1.5 cm instead of 1.1 cm), the vertices `x`, `y`, `z_1`, `z_2` (inner vertices of the positive path) are labelled and the thread ends are dashed. Captions and text
  unchanged. `main.tex`: the five `\includegraphics` lines only.
- Build: 15 pages, no undefined references; packager `-CheckOnly`: `Verdict: PASS`. Still bitmap:
  `diameter-two-structure.png` (Figure 10). Figure 1 (`cut-path`) was redrawn in TikZ later that day (11:10), PNG in the same archive folder.

**2026-10-09 - plain-style revision; thesis citation removed (09:40-09:50)**
- `main.tex`: "Content changes to review", item 17. `references.bib`: entry `Michel2025MinCutPath` removed
  (it stays in the canonical file); 11 entries, `check-bib.ps1` 0 findings.
- Build: 15 pages, no undefined references; packager, full run: `Verdict: PASS`. `check-text.ps1`: 2 findings
  (one "To the best of our knowledge", backed by the search of 2026-10-07; one long sentence in the proof of
  Theorem 4.5, a proof step, left).

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
