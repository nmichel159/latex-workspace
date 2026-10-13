# Article 2 - shared specification (2026-10-12)

Read `CLAUDE.md` in the workspace root first; its rules bind every agent (files in English, sources only in
`projects/<project>/`, never delete files, cite only verified sources, no commits, no package installs without
the author's consent, builds from PowerShell with the MiKTeX installer disabled).

## 1. Goal

Write article 2 from Section 3.3 of the master's thesis (*Diam or Cut 2 Graph*): the Min Cut-Path problem on
graphs in which every pair of vertices is at distance at most two or has cut-value at most two.
The author allowed a full restructuring: new wording, better figures, complete proofs.
Target: Algorithmica, class `sn-jnl` (project `projects/clanok-2-min-cut-path/`, one `main.tex`).
The thesis text is loose (definitions by algorithm, proof sketches); the article states canonical definitions and
proves every statement. A later phase (not now) looks for new results: the open case `d(u,v) = 2`, diameter three.

## 2. Sources

| What | Where |
|---|---|
| Thesis, Section 3.3 (pages 33-51 of the thesis) | `knowledge/sources/diplomova-praca-2025-min-cut-path.txt` lines 1467-2397 (formulas scrambled), exact wording and figures in the PDF beside it |
| Article 1 (definitions, notation, style to follow; results to cite) | `projects/clanok-1-min-cut-path/main.tex`, notes `projects/clanok-1-min-cut-path.md` |
| Research map, errata of the thesis, related work already verified | `knowledge/research/min-cut-path.md` (Sections 3, 5a, 5b, 6) |
| Writing rules | `knowledge/writing/academic-style.md`, `math-writing.md`, `paper-structure.md`, `latex-conventions.md`, `checklist.md` |
| Citations | `knowledge/bibliography/README.md`, `knowledge/bibliography/references.bib`, `knowledge/literature/` |
| Venue | `knowledge/venues/algorithmica.md`, project notes `projects/clanok-2-min-cut-path.md` ("Known problems") |
| Counterexample drawings (TikZ) | `projects/clanok-1-min-cut-path.submission/figures/counterexample-*.tex` |
| Checks of article 1 (brute-force `cp`, graph enumeration) | `projects/clanok-1-min-cut-path.submission/checks/` |

## 3. File ownership (an agent writes only its own files)

All working files live in `projects/clanok-2-min-cut-path.submission/` (never sent).

| Agent | Owns |
|---|---|
| math core | `drafts/core.tex`, `drafts/core-notes.md` |
| checks | `checks/*` |
| literature | `drafts/related-work.md`, `knowledge/bibliography/references.bib`, new notes in `knowledge/literature/`, `knowledge/literature/searches.md` (append), `projects/clanok-2-min-cut-path/references.bib` |
| figures | `figures/*`, figure PDFs in `projects/clanok-2-min-cut-path/` |
| integration (later) | `projects/clanok-2-min-cut-path/main.tex`, `projects/clanok-2-min-cut-path.md` |

Save as you go. Scratch builds go to `tmp/clanok-2-<agent>/`.

## 4. Terminology and notation (fixed for all agents)

Notation of article 1 is kept: `G = (V, E)` finite, simple, undirected, connected; `u != v`; `d(u,v)`, `c(u,v)`,
`\cp(u,v)`, `\CP(u,v)`; a cut is `\delta(A)`; a cut-path is `S`; `G \setminus P` removes the edges of `P`;
problem names in small caps (`\MinCutPath`, `\SSP`).

| Term | Meaning | Thesis |
|---|---|---|
| class `\DC` (prints `\mathcal{DC}_2`) | graphs in which every two distinct vertices `x, y` satisfy `d(x,y) <= 2` or `c(x,y) <= 2` | "diam or cut 2 graph", Def. 37 |
| `F = F(u,v)` | union of all minimum `u`-`v` cuts, for a pair with `c(u,v) = 2` | - |
| tail, head of `e in F` | every edge of `F` is oriented from the `u`-side to the `v`-side | - |
| piece | component of `G - F` | - |
| entering / leaving edge of a piece | edge of `F` with its head / tail in the piece | - |
| square | the piece of `u`, the piece of `v`, and every piece with two entering edges; `S_1, ..., S_k`, `k >= 2`, in the order from `u` to `v` | square graph, Def. 39 |
| terminals of `S_i` | `a_i, b_i`: heads of the entering edges (`a_1 = b_1 = u`); `c_i, d_i`: tails of the leaving edges (`c_k = d_k = v`) | designated / critical vertices |
| link | a piece that is not a square (one entering, one leaving edge) | - |
| general path `P_{i,1}, P_{i,2}` | the two sequences `e_0, L_1, e_1, ..., L_r, e_r` (`r >= 0`, `e_j in F`, `L_j` links) that lead from `S_i` to `S_{i+1}` | general path, Def. 38 |
| square decomposition of `(G, u, v)` | `S_1, P_{1,1}, P_{1,2}, S_2, ..., S_k` | general square graph, Def. 40 |

Macros to assume in drafts: `\cp`, `\CP`, `\DC`, `\MinCutPath`, `\SSP`. Labels with prefixes `sec:`, `def:`,
`thm:`, `lem:`, `cor:`, `prop:`, `rem:`, `ex:`, `fig:`, `alg:`, `eq:`; references with `\cref`.
Environments available: `theorem`, `lemma`, `corollary`, `proposition` (one shared counter, continuous numbers),
`definition`, `remark`, `example` (own counters), `proof`, `algorithm` + `algorithmic` (algpseudocode).
Lists: plain `enumerate` / `itemize` only (the class fixes the labels: `1.`, then `(a)`); conditions referred to in
the text are written inline as (i), (ii). One sentence per source line. American spelling.

## 5. Mathematical blueprint

Derived on 2026-10-12 from the thesis; every statement must be proved in `drafts/core.tex` and tested in `checks/`.
If a statement turns out false or needs another hypothesis, correct it and record the change in `core-notes.md`;
the checks agent reports a minimal counterexample instead of adapting the test.

Setting for S1-S11: `c(u,v) = 2`; `p_1, p_2` are two edge-disjoint `u`-`v` paths (Menger).

- **S0 (easy pairs).** `c(u,v) = 1` or `d(u,v) = 1` implies `cp = c + d - 1` (article 1, Lemma 2.3).
  In `\DC` a pair with `d(u,v) >= 3` has `c(u,v) <= 2`. Open pairs: `d(u,v) = 2` and `c(u,v) >= 3`.
  Bridges: `cp(u,v)`, distances and cut-values between vertices of the 2-edge-connected component `K` of `u`
  (which contains `v`, `p_1`, `p_2`) are the same in `K` and in `G`.
- **S1.** `F` is a subset of `E(p_1) ∪ E(p_2)`; every minimum cut has one edge on `p_1` and one on `p_2`.
- **S2 (orientation).** Orient `e in F ∩ E(p_i)` in the direction of `p_i`. For every minimum cut `\delta(A)`
  with `u in A` that contains `e`, the tail is in `A` and the head is not. Every `u`-`v` path contains exactly
  one edge of every minimum cut and traverses each of its edges of `F` from tail to head.
- **S3 (pieces).** Every edge of `F` joins two different pieces. The vertices of a piece that lie on a `u`-`v`
  path `R` are consecutive on `R` (a path visits a piece at most once).
- **S4 (degrees of pieces).** Every piece has at most two entering and at most two leaving edges. The piece of
  `u` has none entering and two leaving, the piece of `v` two entering and none leaving, and they differ. Every
  other piece has as many entering as leaving edges, one or two.
- **S5 (chain).** The two entering edges of a square other than `S_1` form a minimum `u`-`v` cut, and so do the
  two leaving edges of a square other than `S_k`. Every `u`-`v` path visits all squares, in the same order
  `S_1, ..., S_k`. Between `S_i` and `S_{i+1}` the remaining pieces and edges of `F` form the two general paths;
  a `u`-`v` path contains all `F`-edges of exactly one of them, visits all its links and no link of the other.
- **S6 (terminals).** Two distinct terminals `s, t` of one square satisfy `c_G(s,t) >= 3`.
  (Proof idea: a cut `\delta(B)` with at most two edges that separates `s` from `t` and not `u` from `v` is
  uncrossed with the entering or the leaving cut of the square; submodularity gives a minimum `u`-`v` cut that
  separates two vertices of one piece.)
- **S7 (separation criterion).** Let `R` be a `u`-`v` path. In `S_i` let `x_i` be the head of the entering edge
  used by `R` (`x_1 = u`), `y_i` the tail of the leaving edge used by `R` (`y_k = v`), `\alpha_i` the head of the
  other entering edge (`\alpha_1 = u`) and `\beta_i` the tail of the other leaving edge (`\beta_k = v`).
  Then `u` and `v` lie in different components of `G \setminus R` if and only if for some `i` the vertices
  `\alpha_i` and `\beta_i` lie in different components of `S_i \setminus R`.
- **S8 (lengths).** Let `\vec G` be `G` with the edges of `F` usable only from tail to head. The `u`-`v` paths
  of `G` are exactly the directed `u`-`v` paths of `\vec G`. For an edge `e in F` with tail `s` and head `t` put
  `\lambda^-(e) = d_{\vec G}(u, s)` and `\lambda^+(e) = d_{\vec G}(t, v)`. For an entering edge `g` and a leaving
  edge `h` of `S_i` and every path `p` in `S_i` from the head of `g` to the tail of `h`, the shortest `u`-`v` path
  that contains `g`, `p`, `h` has `\lambda^-(g) + 1 + |p| + 1 + \lambda^+(h)` edges and meets `S_i` exactly in `p`
  (for `S_1`: `|p| + 1 + \lambda^+(h)`; for `S_k`: `\lambda^-(g) + 1 + |p|`).
- **S9 (characterization; any graph with `c(u,v) = 2`).** `cp(u,v) = d(u,v)` if and only if some square `S_i`
  contains a path `p` from an entering terminal `x` to a leaving terminal `y` such that the count of S8 equals
  `d(u,v)` and `p` separates the other two terminals `\alpha`, `\beta` in `S_i`. Otherwise `cp(u,v) = d(u,v) + 1`.
- **S10 (role of the class).** If `G in \DC`, such a path `p` has `|p| = d_G(x,y) <= 2` (S6 and the class).
- **S11 (algorithm, linear time).** Compute `p_1, p_2` (two augmentations), `F` (edges of `p_1 ∪ p_2` whose ends
  lie in different strongly connected components of the residual digraph; minimum cuts = closed sets), the
  pieces, `\lambda^-`, `\lambda^+` (two breadth-first searches in `\vec G`). For every square and every pair
  (entering, leaving): `\ell = d(u,v) - (count without |p|)`; if `\ell = 1` test the edge `xy`; if `\ell = 2`
  take one `\alpha`-`\beta` path `q` in `S_i`: a separating `x`-`w`-`y` path shares an edge with `q`, so `w` is one
  of the at most four neighbors of `x` or `y` on `q`; test each by one search. Total `O(|V| + |E|)`.
  Output also a minimum cut-path: the path found, or a shortest path plus the second edge of a minimum cut.
- **S12 (hardness without the class).** For general graphs, deciding `cp(u,v) = d(u,v)` is NP-complete even for
  pairs with `c(u,v) = 2`: add a new vertex `u'` joined to `u` by two internally disjoint paths of length two;
  a shortest `u'`-`v` path separates `u'` from `v` iff its `u`-`v` part separates `u` from `v`
  (article 1, NP-completeness of Separating Shortest Path). In the decomposition the whole of `G` is one square.
- **S13 (the class).** `G in \DC` iff every class of the relation `c(x,y) >= 3` has pairwise distances at most
  two in `G`. Graphs of diameter two and cactus graphs lie in `\DC`; the formula `cp = c + d - 1` holds in both
  (article 1) and fails in `\DC` (two six-vertex counterexamples, research map Section 3).
- **S14 (coarser decompositions).** The thesis stops splitting a square as soon as its terminals are pairwise at
  distance at most two; the criterion S7 and the algorithm work for every such coarser decomposition. Remark only.
- **S15 (open pairs, `d(u,v) = 2`, `c(u,v) >= 3`).** `cp in {c, c+1}`; `cp = c` iff some minimum `u`-`v` cut
  contains a `u`-`v` path, and such a path has odd length at least three. Stated as what is known, not solved.

## 6. Planned sections of the article

1. Introduction (problem, results of article 1, the class, contributions, related work)
2. Preliminaries (cut-path, bounds, easy pairs, the class `\DC`, counterexamples)
3. Structure of the minimum cuts of a pair with `c(u,v) = 2` (S1-S6: square decomposition)
4. Separating shortest paths (S7-S9)
5. A linear-time algorithm in `\DC` (S10, S11)
6. Hardness outside the class (S12)
7. Pairs at distance two (S15) and open questions
8. Conclusion
