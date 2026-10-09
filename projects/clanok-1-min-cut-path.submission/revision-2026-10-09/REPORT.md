# Preserving revision of article 1, 2026-10-09: report for the author

Manuscript: `projects/clanok-1-min-cut-path/main.tex`. Original kept at
`archives/removed-from-projects/clanok-1-min-cut-path/main-before-preserving-revision-2026-10-09.tex`
(and its `.bib` beside it). Line-level diff: `git diff 0cc6ff9 -- projects/clanok-1-min-cut-path/main.tex`.

## Result

- Build: 19 pages (before 15), no undefined references or citations; the only overfull box is the class's own at
  `\maketitle`. Static package check `Verdict: PASS`. `check-text.ps1`: 9 hits, all judged false positives
  (problem name "Most Vital Edges", authors named before `\cite`, "exhaustive" cases, the one logged novelty
  sentence). `check-bib.ps1`: 2 recommendations (no issue number in Crossref for two journal entries).
- Words: 5622 -> about 7800. Nothing mathematical was removed (preservation audit in `review-math.md`, section 1:
  every definition, lemma, theorem, remark, proof step, Algorithm 1 line, procedure, figure and citation is present).

## What changed

| Place | Change |
|---|---|
| Abstract | `c(u,v)` and `d(u,v)` explained before the formula; secured edges named. |
| Introduction | Related work rewritten from verified reading notes: non-disconnecting paths (Mao; Abhinav et al.), Shortest Path Most Vital Edges (Bazgan et al.), Network Diversion (Bentert et al.), Matching Cut (Le and Le; Komusiewicz et al., DAM 2020); comparison on diameter two. Contributions carry theorem numbers; the random-graph range is stated exactly; a paragraph gives the idea of the reduction. |
| Section 2 | Renamed "Preliminaries" (label kept). One sentence defines a u-v cut in Definition 2.1's own words; existence of the minimum in Definition 2.3 made explicit; the proof of Lemma 2.4 spells out both cases. All definitions kept. |
| Section 3 | Reorganized for navigation, nothing removed: 3.1.1 Gadgets (Figures 3, 4, 6 now cited; Figures 7-9 after the list), 3.1.2 The Construction (procedures, notation, Algorithm 1 moved out of the proof, "In words", lengths after calibration), 3.1.3 Correctness: Lemma 3.5 (shortest paths = chain paths), 3.6 (synchronization), 3.7 (clause threads), 3.8 (separation), then Theorem 3.9 with (a)/(b), running time, NP. Lemma 3.8's proof rewritten on the author's request in four parts: the graph G \ P (unused paths, open and closed crossing edges; a u-v path uses only usable connecting paths), open crossing edges (sign in a block; literal of a clause), usable connecting paths (Table 1: only the first/last paths of synchronization threads and the clause-thread paths between false literals), and the conclusion (following Q from u: back to u from I_i, or through L_{1,k}, L_{2,k}, L_{3,k} with all three literals false). Section 3.2: uniform headings, "breadth-first search", the NP-hard sentence after the proof. |
| Section 4 | Lemma 4.3 has a proof (from the sentence that stood before it). Theorem 4.5: cases as paragraphs; made explicit why a minimum cut is an edge boundary, the two renamings behind "by symmetry", why `deg(u,I) = 0`. Figure 10 redrawn as vector PDF (source in `../figures/diameter-two-structure.tex`; the PNG is in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-png-figures/`). |
| Section 5 | Cactus argument: the two vertices named and the path between them constructed; Theorem 5.1: cycles renamed `Z_i` inside the proof (clash with cut `C` and clauses `C_k`), the concatenation of arcs justified. |
| Section 6 | "With high probability" defined once; `\mathbb{P}(\cdot)`; inline solidus fractions and `\exp` (DAM style); steps of Lemmas 6.4, 6.5 and Theorem 6.6 made explicit; Theorem 6.2 now also cites Chung and Lu (2001). |
| Section 7 | Open problems as parallel questions; one new question: NP-hardness on graphs of diameter three (the boundary for Most Vital Edges and Matching Cut). |
| Acknowledgments | Name without academic titles. |
| Bibliography | Seven verified entries added (Abhinav et al. 2022, Bazgan et al. 2019, Bentert et al. 2025, Chung and Lu 2001, Komusiewicz et al. 2020 (DAM), Le and Le 2019, Mao 2021); 18 in total. |

Two wording corrections touch the meaning of an existing sentence and need your confirmation:
1. Proof of Theorem 6.6: "the bounds of Theorem 6.2 and Lemma 6.5 remain valid for every p >= alpha log n / n" was
   false for the upper bound `c(u,v) <= beta_2 log n` (adding edges can increase `c`). It now says "the diameter
   bound ... and the lower bound `c(u,v) >= beta_1 log n`"; only these two are used.
2. Section 3.1: the sentence after the SSP box now says that a solution is a *separating* shortest path, i.e., a
   cut-path of size `d(u,v)`.

## Decisions for the author (not applied)

Full lists with exact proposed LaTeX: `issues-A.md` (front matter, Sections 1-2), `issues-B.md` (Section 3),
`issues-C.md` (Sections 4-5), `issues-D.md` (Sections 6-7), `review-math.md`, `review-style.md`. The important ones:

**Possible mathematical errors or gaps**
- "Simple" graphs are never assumed, but Theorem 4.5 (`deg(u,K) <= |K|-1`, `deg(u) >= c(u,v)`) and the cactus
  argument need them (A4, C3). Proposal: "All graphs are finite, simple and undirected."
- "Cut" has two meanings: any separating edge set (Definition 2.1) and the edge boundary of a vertex set
  (Lemmas 4.2-4.4); Lemma 4.4 is false for the first (A2, C2). "Cut-value" is never defined (A3).
- Definition 2.5 measures "almost all inputs" uniformly, Theorem 6.6 is about `G(n,p)` (A5, D7); "scheme" is a
  misnomer (A6). Proposal: state Theorem 6.6 as "w.h.p., for all u, v, `|C u P| <= (1 + 1/(beta_1 log log n)) cp(u,v)`" (D8).
- Section 5: the cactus argument shows only that two cycles share no edge, not that they share at most one
  vertex (C7); the proof of Theorem 5.1 assumes that `P` meets each cycle in one arc (C8). Both claims are true;
  proofs proposed.
- Definitions 3.1-3.4: item 2 of Definition 3.1 is vacuous; Definition 3.3 is circular ("every other thread") and
  disagrees with 3.4 on whether a thread is finished (B7, B10, B11); `Calibrate` says "at least Lambda" while the
  running-time paragraph says "has Lambda edges" (B13).
- Theorem 6.3 ("k-edge-connected with k = delta(G)", a random `k`) and its source are not verified first-hand (D4).

**New claims you may want (proposals only)**
- `|C u P| < 2 cp(u,v)`: the union of a minimum cut and a shortest path is a 2-approximation in every graph (A8).
- SSP asks whether `cp(u,v) = d(u,v)`, so deciding whether the lower bound of Lemma 2.4 is attained is
  NP-complete (B16); every vertex other than u, v of the reduction graph has degree at most three (B15).
- Dense case as a corollary (D9); the failing class "diam or cut 2" with the parked counterexamples (C11, D11).

**Proposed deletions or restructuring** (redundant original text): Lemma 4.2 as a definition (C1); unused
`beta_2` and the upper Chernoff tail (D2); `G' := G` and the repeated assumption in Theorem 3.10 (B17, B18);
Section 3.2 as a corollary (B25).

**Other**: the novelty sentence vs. your master's thesis (A1); title and keywords (A10, A11); the student-number
e-mail (A12); the redrawn Figure 10 reads the end of `P` as a vertex `k` (review-math N5): check it.
