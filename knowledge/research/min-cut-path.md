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
| Base case: if `c = 1` or `d = 1`, then `cp = c + d − 1` | Claim 6 | Lemma `lem:basic-bounds` (II.4), second part | |
| Bounds `max(c, d) ≤ cp ≤ c + d − 1` | Claim 7 | Lemma `lem:basic-bounds` (II.4) | added to A1 on 2026-10-07 |
| The union of a minimum cut and a shortest path is a 2-approximation | Claim 8 | – | |
| `min cp(u,v) = min c(u,v)` over the edges `{u,v} ∈ E` | Theorem 9 | – | |
| Partial Path / Partial Cut Property (a known path or cut of an optimum ⇒ polynomial solution) | Theorem 10, 11 | – | basis of the Path-Cut algorithm |
| Tree-cut: `tc(u,v) = t(G)` in an unweighted graph; fails in a weighted one | Theorem 4, 5 | – | |
| Decomposition `I, J, K, L` by a cut | Claim 12 (+ Algorithm 1) | Lemma `lem:cut-decomposition` | |
| Diameter 2 ⇒ `I = ∅` or `L = ∅` | Claim 13 | Lemma `lem:empty-i-or-l` | |
| Every `u`–`v` path intersects every `u`–`v` cut in an odd number of edges | Claim 14 | Lemma `lem:odd-intersection` | holds for a cut of the form `δ(A₁)` |
| **Diameter 2 ⇒ `cp = c + d − 1`** | Theorem 15 | Theorem `thm:diameter-two` (IV.5) | |
| Diameter 2 ⇒ `c(u,v) = min(deg u, deg v)` | Theorem 16 | – | |
| `c(x,y) ≤ 2` for all pairs ⇒ cactus structure | Claim 17 | paragraph before Theorem V.1 | |
| **`c(x,y) ≤ 2` for all pairs ⇒ `cp = c + d − 1`** | Theorem 18 | Theorem `thm:cut-two` (V.1) | proof added 2026-10-07 |
| Class *diam or cut 2*; the formula `cp = c + d − 1` does not hold in it (counterexamples) | Def. 37, Fig. 3.3 | only in the conclusion as a further direction, without the counterexamples | the two counterexamples are described below the table; the author decided on 2026-10-09 not to put them or the class diagram into A1 for now |
| General path, square graph, general square graph, pseudo-square graph | Def. 38–41 | – | |
| Decomposition into a general square graph for `c(u,v) = 2` | Theorem 20 (Alg. 2–5) | – | |
| Polynomial computation of `cp` in *diam or cut 2* for `c(u,v) = 2` | Theorem 22 (Alg. 6) | – | the case `d(u,v) = 2` remains open |
| Linear `O(\|E\|)` computation given the decomposition | Theorem 23 (Alg. 7) | – | |
| `G(n, 1/α)`, `α > 1`, has diameter 2 almost surely | Theorem 24 (with proof; `α > 0` in MT) | Theorem `thm:random-diameter-two` (VI.1), citing Bollobás | |
| Properties of `G(n, α log n / n)`, `α > 1`: connectivity, diameter | Theorem 25, 26 | `thm:random-connectivity`, `thm:random-diameter` | Theorem 27 (largest component) is only in MT |
| Vertex degrees | Theorem 28: all in `(1 ± ε) α log n` – **false** for fixed `α` | Lemma `lem:degree-bounds` (VI.4): all in `[β₁ log n, β₂ log n]` | see Section 5a |
| Bounds for `c(u,v)` | Claim 29 (with `(1 ± ε) α log n`) | Lemma `lem:connectivity-bounds` (VI.5) with `β₁, β₂` | |
| **Average (1+ε)-Approximation Scheme** for `p ≥ α log n / n` | Theorem 30 | Theorem `thm:approximation-scheme` (VI.6) | monotonicity argument added in A1 |
| Almost polynomial average-case algorithm (Path-Cut) | Theorem 31 (Alg. 8) | – | |
| For `α < 1`, `cp(u,v)` is defined with probability → 0 | Claim 32 | – | |
| Symmetric case `c = d = cp`: symmetric cut-path graph, max independent path graph | Def. 47, 48; Claim 33–36 | – | up to `2^{O(√n)}` distinct optima (Claim 35) |
| Filter-BFS, Local-Cut; polynomial for nearly 5-regular graphs | Alg. 9–12; Theorem 37, 38 | – | |
| **NP-completeness of \textsc{Separating Shortest Path}** (reduction from 3-SAT, chain and threads) | – | Theorem `thm:ssp-np-complete` (III.5), `alg:reduction` | new relative to MT; proof rewritten 2026-10-07 |
| **NP-completeness of the decision version of \textsc{Min Cut-Path}** | – (an open problem in MT) | Theorem `thm:mcp-np-complete` (III.6) | reduction `G' = G`, `k = d_G(u,v)`; the optimization version is NP-hard |

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

## 4. What each text contains beyond the other

**Only in MT** (material for further articles):
- chapter 2: tree-cut, 2-approximation, global minimum, partial path/cut property;
- chapter 3.3: the whole theory of *diam or cut 2* and of the decomposition into a general square graph;
- chapter 4.5: almost polynomial average-case algorithm for sparse random graphs;
- chapter 5: symmetric case `c = d = cp`, algorithms Filter-BFS and Local-Cut.

**Only in A1:**
- NP-completeness via the intermediate problem \textsc{Separating Shortest Path};
- gadgets: chain link (a cycle with two equally long `p`–`q` paths, positive and negative), chain with `r` links, thread, threading, crossing edge;
- chain link types: initialization `I_i`, terminal `T_i`, literal `L_{j,k,i}` (`j` = literal position, `k` = clause, `i` = variable; `3m + 2n` in total);
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

Mentioned neither in A1 nor in MT; cite them in the next revision of A1 and in article 2 (entries are in `knowledge/bibliography/references.bib`).

| Problem | Relation to Min Cut-Path | Source |
|---|---|---|
| *Non-separating st-path*: an `s`–`t` path whose edge removal leaves the graph connected; existence is NP-hard on general graphs, polynomial on chordal graphs | mirror notion to Separating Shortest Path (there removing the path must separate `u` and `v`) | Mao, arXiv:2101.03519 (verified) |
| Diameter of sparse random graphs: `(1 + o(1)) log n / log(np)` | exact source for Theorem VI.2 in A1 (Theorem 26 in MT) | Chung, Lu 2001 (partially verified) |
| Shortest-path interdiction, "most vital edges", Force Path Cut (removing edges so that the shortest path changes) | a different combination of cuts and shortest paths; find and verify specific papers | `TODO(verify)` – so far only from search results |

Note for texts: if `cp = c + d − 1` holds, the union of any minimum cut and any shortest path is a minimum cut-path (A1, Remark IV.6).

## 6. Open problems and directions

From MT and the conclusion of A1:
1. Class *diam or cut 2*: the case `d(u, v) = 2` (MT solves only `c(u, v) = 2`); in A1 phrased as merging two polynomial "islands".
2. Planar graphs (cut ↔ cycle duality), graphs of bounded treewidth.
3. Approximation algorithms with a guarantee for general graphs (only the trivial 2-approximation is known).
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
