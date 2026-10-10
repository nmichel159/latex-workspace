# Min Cut-Path – research overview

Sources: the master's thesis *Min Cut-Path* (Charles University, Prague, 2025; **MT**) and the manuscript of article 1
(`projects/clanok-1-min-cut-path/main.tex`, the whole text in one file; **A1**). Definition and theorem numbers of MT can be located in
`knowledge/sources/diplomova-praca-2025-min-cut-path.txt`.

## 1. Problem

The graph `G = (V, E)` is undirected and finite; `u, v ∈ V` are two distinct vertices.

- **Cut-path** between `u` and `v`: a set of edges `S ⊆ E` that contains subsets `P, C ⊆ S` such that `P` is a `u`–`v` path and `C` is a cut separating `u` and `v`.
- **Min Cut-Path (optimization):** find a cut-path with the fewest edges; its value is `cp(u, v)`.
- **Min Cut-Path (decision):** input `G, u, v, k`; is there a cut-path `F` with `|F| ≤ k`?
- Motivation (A1): communication between trusted servers (the path) while cutting off an adversary (the cut) – "communication and control".
- Idea due to: prof. Martin Loebl.

## 2. Notation

| Symbol | Meaning | Note |
|---|---|---|
| `n = \|V\|`, `m = \|E\|` | number of vertices, edges | in the NP-completeness section `n`, `m` are the numbers of variables and clauses; the chain has `r` links |
| `d(u, v)` | distance (length of a shortest path) | "min path" in MT, "shortest path" in A1 |
| `c(u, v)` | size of a minimum `u`–`v` cut | |
| `cp(u, v)` | value of a minimum cut-path | macro `\cp` in A1 |
| `CP(u, v)` | set of all cut-paths | `cut-path(u, v)` in MT; macro `\CP` in A1 |
| `tc(u, v)`, `t(G)` | minimum tree-cut, size of a spanning tree | MT only |
| `deg(v)`, `deg(v, S)` | degree, number of neighbors in the set `S` | |
| `δ(S)`, `δ(G)` | cut determined by the set `S`; minimum degree | |
| `G ∖ P` | graph after removing the edges of the path `P` | |
| `G(n, p)` | Erdős–Rényi random graph | |
| `I, J, K, L` | partition of the vertices by a cut: `I ∪ J = A₁`, `K ∪ L = A₂`; `J, K` have an edge in the cut, `I, L` do not | |
| `G_P` | max independent path graph | MT only, ch. 5 |
| `OPT(x)`, `I(n)`, `I_A^opt(n)` | optimum, set of inputs of size `n`, inputs with a guarantee | definition of an approximation scheme |

Typeset problem names in small caps: `\textsc{Min Cut-Path}`, `\textsc{Separating Shortest Path}`, `\textsc{3-SAT}`.

## 3. Results map

| Result | MT 2025 | A1 | Note |
|---|---|---|---|
| Base case: if `c = 1` or `d = 1`, then `cp = c + d − 1` | Claim 6 | Lemma `lem:basic-bounds` (2.3), second part | |
| Bounds `max(c, d) ≤ cp ≤ c + d − 1` | Claim 7 | Lemma `lem:basic-bounds` (2.3) | added to A1 on 2026-10-07 |
| The union of a minimum cut and a shortest path is a 2-approximation | Claim 8 | Corollary `cor:two-approximation` (2.4): `\|C ∪ P\| ≤ 2cp − 1` | added to A1 on 2026-10-10 |
| `min cp(u,v) = min c(u,v)` over the edges `{u,v} ∈ E` | Theorem 9 | – | |
| Partial Path / Partial Cut Property (a known path or cut of an optimum ⇒ polynomial solution) | Theorem 10, 11 | Lemma `lem:contraction` (7.5): `cp = min (|C| + d_C)` over the inclusion-minimal cuts `C`, the formula behind Theorem 11 | basis of the Path-Cut algorithm; trying all cuts with at most `b` edges takes `|E|^O(b)` time (XP, not FPT) |
| No PTAS (hence no FPTAS) unless P = NP; FPT with respect to the threshold `b` (treewidth reduction of `Marx2013Separators` and Courcelle's theorem) | – | Section 7 (in `main.tex` since 2026-10-10): Theorem `thm:no-ptas` (7.3, with Lemmas `lem:missed-threads` 7.1 and `lem:unsatisfied-clauses` 7.2), Corollary `cor:no-fptas` (7.4), Theorem `thm:fpt` (7.8), Lemmas `lem:treewidth-reduction` (7.6), `lem:good-set` (7.7) | important cuts do not suffice: in the left graph of Example 5.3 the only important cut gives 4, `cp = 3`; lemmas checked on small graphs (`checks/check_fpt_lemmas.py`, `checks/check_good_set_literal.py`) |
| Tree-cut: `tc(u,v) = t(G)` in an unweighted graph; fails in a weighted one | Theorem 4, 5 | – | |
| Decomposition `I, J, K, L` by a cut | Claim 12 (+ Algorithm 1) | Definition `def:cut-decomposition` (4.2; a lemma until 2026-10-10) | |
| Diameter 2 ⇒ `I = ∅` or `L = ∅` | Claim 13 | Lemma `lem:empty-i-or-l` (4.3) | |
| Every `u`–`v` path intersects every `u`–`v` cut in an odd number of edges | Claim 14 | Lemma `lem:odd-intersection` (4.4) | holds for a cut of the form `δ(A₁)` |
| **Diameter 2 ⇒ `cp = c + d − 1`** | Theorem 15 | Theorem `thm:diameter-two` (4.5) | |
| Diameter 2 ⇒ `c(u,v) = min(deg u, deg v)` | Theorem 16 | Corollary `cor:diameter-two-degrees` (4.7), with `cp = min(deg u, deg v) + d − 1` and a linear-time algorithm | added to A1 on 2026-10-10 |
| `c(x,y) ≤ 2` for all pairs ⇒ cactus structure | Claim 17 | Lemma `lem:cactus` (5.1): `c(x,y) ≤ 2` for all pairs iff two distinct cycles share at most one vertex (both directions proved); Section 5 is titled "Cactus Graphs" | a lemma with proof since 2026-10-10 |
| **`c(x,y) ≤ 2` for all pairs ⇒ `cp = c + d − 1`** | Theorem 18 | Theorem `thm:cut-two` (5.2) | proof added 2026-10-07 |
| Class *diam or cut 2*; the formula `cp = c + d − 1` does not hold in it (counterexamples) | Def. 37, Fig. 3.3 | Example `ex:strict` (5.3) with Figure 11 shows the two counterexamples; the conclusion names the class and says that the formula fails in it | the two counterexamples are described below the table; the author decided on 2026-10-09 not to put them or the class diagram into A1 for now |
| General path, square graph, general square graph, pseudo-square graph | Def. 38–41 | – | |
| Decomposition into a general square graph for `c(u,v) = 2` | Theorem 20 (Alg. 2–5) | – | |
| Polynomial computation of `cp` in *diam or cut 2* for `c(u,v) = 2` | Theorem 22 (Alg. 6) | – | the case `d(u,v) = 2` remains open |
| Linear `O(\|E\|)` computation given the decomposition | Theorem 23 (Alg. 7) | – | |
| `G(n, 1/α)`, `α > 1`, has diameter 2 almost surely | Theorem 24 (with proof; `α > 0` in MT) | Theorem `thm:random-diameter-two` (6.1), constant `p`, with a proof since 2026-10-10 (known fact: Frieze-Karoński, Exercise 1.4.8) | |
| Properties of `G(n, α log n / n)`, `α > 1`: connectivity, diameter | Theorem 25, 26 | `thm:random-diameter` (6.2, Chung-Lu), `thm:random-connectivity` (6.3, Bollobás p. 169) | Theorem 27 (largest component) is only in MT |
| Vertex degrees | Theorem 28: all in `(1 ± ε) α log n` – **false** for fixed `α` | Lemma `lem:degree-bounds` (6.4): all at least `β₁ log n` (the upper bound `β₂` was removed on 2026-10-09) | see Section 5a |
| Bounds for `c(u,v)` | Claim 29 (with `(1 ± ε) α log n`) | Lemma `lem:connectivity-bounds` (6.5): `c(u,v) ≥ β₁ log n` | |
| **Average (1+ε)-Approximation Scheme** for `p ≥ α log n / n` | Theorem 30 | Theorem `thm:approximation-scheme` (6.6): with high probability `\|C ∪ P\| ≤ (1 + 1/(β₁ log log n)) cp` for all pairs; the scheme is its consequence (2026-10-10) | monotonicity argument added in A1 |
| Almost polynomial average-case algorithm (Path-Cut) | Theorem 31 (Alg. 8) | – | |
| For `α < 1`, `cp(u,v)` is defined with probability → 0 | Claim 32 | – | |
| Symmetric case `c = d = cp`: symmetric cut-path graph, max independent path graph | Def. 47, 48; Claim 33–36 | – | up to `2^{O(√n)}` distinct optima (Claim 35) |
| Filter-BFS, Local-Cut; polynomial for nearly 5-regular graphs | Alg. 9–12; Theorem 37, 38 | – | |
| **NP-completeness of \textsc{Separating Shortest Path}** (reduction from 3-SAT, chain and threads) | – | Theorem `thm:ssp-np-complete` (3.10), Lemmas 3.6-3.9, `alg:reduction` | new relative to MT; proof rewritten 2026-10-07 |
| **NP-completeness of the decision version of \textsc{Min Cut-Path}** | – (an open problem in MT) | Theorem `thm:mcp-np-complete` (3.11), Corollary `cor:lower-bound-attained` (3.12: deciding `cp = d` is NP-complete) | threshold `b = d(u,v)`; the optimization version is NP-hard |

**Counterexamples in the class *diam or cut 2*** (MT Fig. 3.3; not in A1; checked by hand 2026-10-09; vector
drawings with the path in red: TikZ sources in `projects/clanok-1-min-cut-path.submission/figures/`, PDFs in
`archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-conclusion-figures/`).
Both graphs have the six vertices `t, a, v, u, b, s` and the edges `ta, tv, au, ab, vb, us, sb`; graph (b) also has
`av` and `ub`. The path `u–a–b–v` has three edges and its removal separates `{a, t, v}` from `{u, b, s}`.
- (a): `c(u,v) = 2`, `d(u,v) = 3`, `cp(u,v) = 3 ≠ 4`; the path is a shortest path that is also a cut. The graph has
  `d(u,v) = 3` and `c(a,b) = 3`, so it lies in neither of the two smaller classes.
- (b): `d(u,v) = 2`, `c(u,v) = 3`, `cp(u,v) = 3 ≠ 4`; the path is a minimum cut that is also a path. The graph has
  `d(t,s) = 3` and `c(u,v) = 3`, so it lies in neither of the two smaller classes.
- In both, a minimum cut and a shortest path share exactly one edge (odd intersection, at most two), so no union of
  a minimum cut and a shortest path is a minimum cut-path.

**Computational verification (2026-10-10).** Scripts and logs: `projects/clanok-1-min-cut-path.submission/checks/`.
- Reduction: an executable model of Algorithm 1 (`reduction.py`); Lemmas 3.6-3.9, Table 1 and Theorem 3.10 hold on
  5639 formulas (59 unsatisfiable; clauses with repeated variables included). Exact sizes: `2n + 7m` threads,
  `4n + 21m` crossing edges, `6n + 28m` connecting paths, `Λ = 10n + 33m + 1`, chain `18n + 63m + 1` edges,
  `|E| = 18n + 63m + 1 + (6n + 28m)Λ`; every vertex other than `u`, `v` has degree at most three.
- Small graphs: Lemma 2.3, Corollaries 2.4 and 3.12 (`cp = d` iff a separating shortest path exists), Lemmas 4.3, 4.4,
  Theorem 4.5, Remark 4.6, Lemma 5.1 and Theorem 5.2 hold on all 1251 graphs with 2 to 7 vertices; every minimum
  `u`-`v` cut is an edge boundary; `c(x,y) ≤ 2` for all pairs iff every block is an edge or a cycle.
- Class *diam or cut 2*: the two counterexamples above are the only graphs with at most six vertices in which
  `cp = c + d − 1` fails; 22 further graphs with seven vertices fail (24 of the 995 connected graphs with 2 to 7
  vertices; every connected graph with at most seven vertices lies in the class).

## 4. What each text contains beyond the other

**Only in MT** (material for further articles):
- chapter 2: tree-cut, 2-approximation, global minimum, partial path/cut property;
- chapter 3.3: the whole theory of *diam or cut 2* and of the decomposition into a general square graph;
- chapter 4.5: almost polynomial average-case algorithm for sparse random graphs;
- chapter 5: symmetric case `c = d = cp`, algorithms Filter-BFS and Local-Cut.

**Only in A1:**
- NP-completeness via the intermediate problem \textsc{Separating Shortest Path};
- gadgets: chain link (a cycle with two equally long `p`–`q` paths, positive and negative), chain with `r` links, thread, threading, crossing edge;
- chain link types: initialization `I_i`, terminal `T_i`, literal `L_{j,k}` (`j` = literal position, `k` = clause; `2n + 3m` links in total);
- thread types: 2-synchronization, 3-synchronization, clause thread;
- auxiliary procedures `BuildChain(u, v, r)`, `Thread(u, v, [(L, σ), …])` (also creates *connecting paths*) and `Calibrate(G)`;
- proof concepts: *chain path*, a chain path *hits* a thread, *consistent* chain path, *unused path* of a link, *dead end*;
- outline of the correctness proof: (1) after calibration the shortest `u`–`v` paths are exactly the chain paths, (2) a separating path must hit every thread, (3) synchronization threads ⇒ consistent signs ⇒ truth assignment, (4) a clause thread is hit ⇔ the clause is satisfied, (5) for a satisfying assignment the component of vertex `u` in `G ∖ P` does not contain `v`.

## 5. Differences between MT and A1 (watch out when reusing text)

| Topic | MT | A1 |
|---|---|---|
| Complexity of the general case | NP-hardness is an open problem | NP-completeness proved |
| Set of cut-paths | `cut-path(u, v)` | `CP(u, v)` |
| Auxiliary statements | `Claim` | `Lemma` (labels `lem:…`) |
| Subsets in the definition of a cut-path | `A` (cut), `B` (path) | `C` (cut), `P` (path); problem boxes worded the same as the definition |
| Division | chapters (`Chapter`) | sections |
| Bibliography | ISO 690, 8 entries (several with errors, see `knowledge/sources/README.md`) | natbib numeric, 11 verified entries (MT itself is not cited since 2026-10-09, author's decision); before: 12 verified entries including MT |
| Degrees in `G(n, α log n / n)` | concentration `(1 ± ε) α log n` | constant bounds `β₁ log n`, `β₂ log n` |

## 5a. Errors found in MT (important for article 2)

Article 2 will be prepared from the master's thesis. Do not reuse these places without correction:

1. **Theorem 28 (Degree Concentration) and Claim 29**: the claim that for `p = α log n / n` with fixed `α > 1` and any fixed `ε > 0` all degrees lie in `(1 ± ε) α log n` is false. A degree is binomial with mean `μ ≈ α log n`; `P[deg ≤ aμ] ≈ n^{−α h(a)}`, `h(a) = a ln a − a + 1`, so after a union bound over the `n` vertices the probability tends to zero only for `α h(a) > 1`. The minimum and maximum degrees are therefore `≈ a₁ α log n` and `≈ a₂ α log n` with constants `a₁ < 1 < a₂` depending on `α`. The correct formulation is in A1 (`lem:degree-bounds`). Theorem 30 (approximation scheme) remains valid because it needs only `c(u,v) ≥ β₁ log n`.
2. **Theorem 24**: `p = 1/α` requires `α > 1` (not `α > 0`).
3. **Theorem 27 (Largest Component)** is stated for `α > 1` but is used in Claim 32 for `α < 1` – `TODO(verify)` both the wording and the source.
4. **Introduction and conclusion of MT** state NP-hardness as an open problem – no longer true after A1.
5. **MT bibliography**: wrong ISBNs (Diestel, Cormen, Godsil–Royle, Frieze–Karoński, Roughgarden), Diestel 6th edition is from 2025, OpenIntro Statistics 4th edition is from 2019, entry 7 has authors Blanc, Lange, Qiao, Tan. Corrected entries: `knowledge/bibliography/references.bib`.
6. **Definitions 44–46** (average-case) measure inputs uniformly (`|I_opt| / |I|`), whereas the theorems concern `G(n, p)` – formulate via probability.
7. Language and formal errors of the same kinds as in the original A1 (checklist: `knowledge/writing/academic-style.md`, `knowledge/writing/checklist.md`).

## 5b. Related problems in the literature

Cited in A1 since the preserving revision of 2026-10-09 (introduction; Chung-Lu at Theorem 6.2; diameter three as an open question in the conclusion); not in MT; cite them in article 2 too (entries are in `knowledge/bibliography/references.bib`, reading notes in `knowledge/literature/`). Searched again 2026-10-09 (`knowledge/literature/searches.md`): the problem itself was not found elsewhere; no Discrete Applied Mathematics paper on a close problem was found.

| Problem | Relation to Min Cut-Path | Source |
|---|---|---|
| *Non-disconnecting* (Mao: non-separating, edge version) s-t path: `G - E(P)` connected; existence NP-hard; shortest one FPT in its length; polynomial on chordal graphs | opposite requirement to Separating Shortest Path; same "private channel" motivation | `Mao2021NonSeparating` (preprint), `Abhinav2022NonSeparating` (MFCS 2022) |
| Shortest Path Most Vital Edges (= length-bounded edge cut, unit lengths): delete `k` edges so that `d(s,t) >= l` | cuts that destroy short paths; NP-hard; for unit lengths NP-hard on diameter three and linear time on diameter two; for arbitrary lengths NP-hard on complete graphs (Theorem 5) | `Bazgan2019MostVital` (Theorem 4, Proposition 1 of arXiv v1); Baier et al. 2010 read, not added |
| Network Diversion: minimal s-t cut containing a prescribed edge | a cut with prescribed content; open on undirected graphs, polynomial on planar graphs | `Bentert2025NetworkDiversion` |
| Matching Cut: an edge cut that is a matching | a cut with prescribed structure; polynomial on diameter two, NP-complete on every fixed diameter `>= 3` | `LeLe2019MatchingCut`, `Komusiewicz2020MatchingCut` (DAM) |
| Diameter of `G(n, p)` for `p >= c log n / n`, `c` constant | exact source for Theorem 6.2 of A1: with `c = alpha > 1`, `diam <= log n / log log n` w.h.p. | `ChungLu2001`, Theorem 4 (authors' PDF; journal numbering not compared) |
| Edge connectivity = minimum degree w.h.p. in `G(n, p)` | Theorem 6.3 of A1 | not verified first-hand: Bollobas, Thomason 1985 and Section 7.2 of `Bollobas2001` according to secondary sources |
| Chernoff tails `P(X <= a mu) <= exp(-mu h(a))`, `h(a) = a log a - a + 1`, and the upper tail with the same `h` | Lemma 6.4 of A1 | Frieze-Karonski, free PDF 2026: (34.19) and (34.17), Section 34.4, p. 707 (`phi(a - 1) = h(a)`); printed numbering (Ch. 21) not verified |

Diameter two is the boundary of tractability for Most Vital Edges with unit edge lengths and for Matching Cut. Whether Min Cut-Path is NP-hard on graphs of diameter three is open (the reduction of A1 produces graphs of large diameter).

Note for texts: if `cp = c + d − 1` holds, the union of any minimum cut and any shortest path is a minimum cut-path (A1, Remark IV.6).

## 6. Open problems and directions

From MT and the conclusion of A1:
1. Class *diam or cut 2*: the case `d(u, v) = 2` (MT solves only `c(u, v) = 2`); in A1 phrased as merging two polynomial "islands".
2. Planar graphs (cut ↔ cycle duality), graphs of bounded treewidth.
3. Approximation algorithms with a guarantee for general graphs (only the trivial 2-approximation is known).
   No PTAS unless P = NP (A1, Theorem 7.3, 2026-10-10; no FPTAS is Corollary 7.4): in the graph of the reduction every cut-path has at least
   `Lambda + eta*` edges, `eta*` = the least number of threads a chain path misses (Lemma 7.1), and `eta*` is at
   least a fifth of the least number of unsatisfied clauses when every variable occurs five times (Lemma 7.2);
   with the gap problem of `Feige1998Threshold`. Open: the best factor between `1 + eps_0` and two; whether
   `cp = Lambda + eta*` always holds in these graphs (it does on the 38 formulas of `checks/check_gap_lemmas.py`).
4. Weighted and directed variants.
5. Experimental evaluation on real and random networks.
6. Structure of graphs with a fixed value `cp(u, v)`.
7. Further "islands of polynomial-time solvability".

## 7. Planned manuscripts

Author's decision (2026-10-07): **article 2 will be produced from the master's thesis** (project `projects/clanok-2-min-cut-path/`; target Algorithmica, Springer Nature template `sn-jnl` prepared 2026-10-08, placeholder text only). The LaTeX source of MT is not in the repository – supply it in `inbox/`, otherwise the text is transcribed from the PDF. Article 1 targets Discrete Applied Mathematics and was ported to its template on 2026-10-08 (class `cas-sc`).

| Title in the CV | Likely source in MT (guess, to be confirmed) |
|---|---|
| *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem* | chapter 3 (possibly also 5) |
| *Random Graph Models for the Min Cut-Path Problem* | chapter 4 |

## 8. Glossary

English terms come from MT and A1, Czech ones from the Czech abstract of MT. The Slovak equivalents are proposals – no established Slovak terminology exists for this problem.

| EN | CZ (abstract of MT) | SK (proposal) |
|---|---|---|
| cut-path | řezo-cesta | rez-cesta |
| Min Cut-Path | minimální řez-cesta | minimálna rez-cesta |
| edge cut | hranový řez | hranový rez |
| shortest path / min path | nejkratší cesta | najkratšia cesta |
| general path | obecná cesta | všeobecná cesta |
| square graph | čtvercový graf | štvorcový graf |
| general square graph | obecný čtvercový graf | všeobecný štvorcový graf |
| diam or cut 2 graph | graf s průměrem nebo řezem nejvýše dva | graf s priemerom alebo rezom najviac dva |
| nearly k-regular graph | téměř k-regulární graf | takmer k-regulárny graf |
| symmetric cut-path | symetrická řezo-cesta | symetrická rez-cesta |
| tree-cut | – | strom-rez |
| separating shortest path | – | oddeľujúca najkratšia cesta |
| chain, chain link, thread, threading | – | reťaz, článok reťaze, vlákno, navliekanie |
| average (1+ε)-approximation scheme | aproximační schéma s průměrnou zárukou | aproximačná schéma v priemernom prípade |
| almost polynomial algorithm | téměř polynomiální algoritmus | takmer polynomiálny algoritmus |
