# Min Cut-Path – research overview

Sources: the master's thesis *Min Cut-Path* (Charles University, Prague, 2025; **MT**), the manuscript of article 1
(`projects/clanok-1-min-cut-path/main.tex`, the whole text in one file; **A1**) and the manuscript of article 2
(`projects/clanok-2-min-cut-path/main.tex`, first written 2026-10-12 from Section 3.3 of MT, merged 2026-11-02 with the former project `clanok-3`; **A2**, Section 3a below).
Definition and theorem numbers of MT can be located in `knowledge/sources/diplomova-praca-2025-min-cut-path.txt`.

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
| Partial Path / Partial Cut Property (a known path or cut of an optimum ⇒ polynomial solution) | Theorem 10, 11 | Lemma `lem:contraction` (8.1): `cp = min (|C| + d_C)` over the inclusion-minimal cuts `C`, the formula behind Theorem 11 | basis of the Path-Cut algorithm; trying all cuts with at most `b` edges takes `|E|^O(b)` time (XP, not FPT) |
| No PTAS (hence no FPTAS) unless P = NP; FPT with respect to the threshold `b` (treewidth reduction of `Marx2013Separators` and Courcelle's theorem) | – | Section 4 "Approximation Hardness": Theorem `thm:no-ptas` (4.3, with Lemmas `lem:missed-threads` 4.1 and `lem:unsatisfied-clauses` 4.2), Corollary `cor:no-fptas` (4.4); Section 8 "Fixed-Parameter Tractability": Theorem `thm:fpt` (8.4), Lemmas `lem:treewidth-reduction` (8.2), `lem:good-set` (8.3); one Section 7 until the reorder of 2026-10-10 | important cuts do not suffice: in the left graph of Example 6.3 the only important cut gives 4, `cp = 3`; lemmas checked on small graphs (`checks/check_fpt_lemmas.py`, `checks/check_good_set_literal.py`) |
| Tree-cut: `tc(u,v) = t(G)` in an unweighted graph; fails in a weighted one | Theorem 4, 5 | – | |
| Decomposition `I, J, K, L` by a cut | Claim 12 (+ Algorithm 1) | Definition `def:cut-decomposition` (5.2; a lemma until 2026-10-10) | |
| Diameter 2 ⇒ `I = ∅` or `L = ∅` | Claim 13 | Lemma `lem:empty-i-or-l` (5.3) | |
| Every `u`–`v` path intersects every `u`–`v` cut in an odd number of edges | Claim 14 | Lemma `lem:odd-intersection` (5.4) | holds for a cut of the form `δ(A₁)` |
| **Diameter 2 ⇒ `cp = c + d − 1`** | Theorem 15 | Theorem `thm:diameter-two` (5.5) | |
| Diameter 2 ⇒ `c(u,v) = min(deg u, deg v)` | Theorem 16 | Corollary `cor:diameter-two-degrees` (5.7), with `cp = min(deg u, deg v) + d − 1` and a linear-time algorithm | added to A1 on 2026-10-10; **the first equality is a known theorem** (Fricke, Oellermann, Swart; `Stuart2009Eavesdropping`, Theorem 11), see Section 5b |
| `c(x,y) ≤ 2` for all pairs ⇒ cactus structure | Claim 17 | Lemma `lem:cactus` (6.1): `c(x,y) ≤ 2` for all pairs iff two distinct cycles share at most one vertex (both directions proved); Section 6 is titled "Cactus Graphs" | a lemma with proof since 2026-10-10 |
| **`c(x,y) ≤ 2` for all pairs ⇒ `cp = c + d − 1`** | Theorem 18 | Theorem `thm:cut-two` (6.2) | proof added 2026-10-07 |
| Class *diam or cut 2*; the formula `cp = c + d − 1` does not hold in it (counterexamples) | Def. 37, Fig. 3.3 | Example `ex:strict` (6.3) with Figure 12 shows the two counterexamples; the conclusion names the class and says that the formula fails in it | the two counterexamples are described below the table; the author decided on 2026-10-09 not to put them or the class diagram into A1 for now |
| General path, square graph, general square graph, pseudo-square graph | Def. 38–41 | – | |
| Decomposition into a general square graph for `c(u,v) = 2` | Theorem 20 (Alg. 2–5) | – | |
| Polynomial computation of `cp` in *diam or cut 2* for `c(u,v) = 2` | Theorem 22 (Alg. 6) | – | the case `d(u,v) = 2` remains open |
| Linear `O(\|E\|)` computation given the decomposition | Theorem 23 (Alg. 7) | – | |
| `G(n, 1/α)`, `α > 1`, has diameter 2 almost surely | Theorem 24 (with proof; `α > 0` in MT) | Theorem `thm:random-diameter-two` (7.1), constant `p`, with a proof since 2026-10-10 (known fact: Frieze-Karoński, Exercise 1.4.8) | |
| Properties of `G(n, α log n / n)`, `α > 1`: connectivity, diameter | Theorem 25, 26 | `thm:random-diameter` (7.2, Chung-Lu), `thm:random-connectivity` (7.3, Bollobás p. 169) | Theorem 27 (largest component) is only in MT |
| Vertex degrees | Theorem 28: all in `(1 ± ε) α log n` – **false** for fixed `α` | Lemma `lem:degree-bounds` (7.4): all at least `β₁ log n` (the upper bound `β₂` was removed on 2026-10-09) | see Section 5a |
| Bounds for `c(u,v)` | Claim 29 (with `(1 ± ε) α log n`) | Lemma `lem:connectivity-bounds` (7.5): `c(u,v) ≥ β₁ log n` | |
| **Average (1+ε)-Approximation Scheme** for `p ≥ α log n / n` | Theorem 30 | Theorem `thm:approximation-scheme` (7.6): with high probability `\|C ∪ P\| ≤ (1 + 1/(β₁ log log n)) cp` for all pairs; the scheme is its consequence (2026-10-10) | monotonicity argument added in A1 |
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
- Small graphs: Lemma 2.3, Corollaries 2.4 and 3.12 (`cp = d` iff a separating shortest path exists), Lemmas 5.3, 5.4,
  Theorem 5.5, Remark 5.6, Lemma 6.1 and Theorem 6.2 hold on all 1251 graphs with 2 to 7 vertices; every minimum
  `u`-`v` cut is an edge boundary; `c(x,y) ≤ 2` for all pairs iff every block is an edge or a cycle.
- Class *diam or cut 2*: the two counterexamples above are the only graphs with at most six vertices in which
  `cp = c + d − 1` fails; 22 further graphs with seven vertices fail (24 of the 995 connected graphs with 2 to 7
  vertices; every connected graph with at most seven vertices lies in the class).

## 3a. Article 2: the class `DC_2` (written 2026-10-12)

The statement numbers of this section are those of the manuscript of 2026-10-12, archived in `archives/removed-from-projects/clanok-2-min-cut-path/2026-11-02-before-merge/`. The current text keeps the labels, except that Theorem 17 `thm:hardness` and Proposition 12 `prop:lengths` are left out, and it adds NP-completeness on diameter three (`thm:dt-hardness`) and the polynomial algorithm for the open pairs (`thm:pa-open-case`).

Subject: Section 3.3 of MT with canonical definitions and complete proofs. Class `DC_2` (macro `\DC`): connected
graphs in which every two distinct vertices satisfy `d(x,y) ≤ 2` or `c(x,y) ≤ 2` (MT: *diam or cut 2*, Def. 37).
Statements are numbered on one counter (theorem, lemma, proposition, corollary); numbers as compiled 2026-10-12.

**Terms (A2, Definitions 3 and 4), for a pair with `c(u,v) = 2`:** `F` = union of all minimum `u`-`v` cuts; every
edge of `F` has a *tail* (on the `u`-side of every minimum cut containing it) and a *head*; a *piece* is a
component of `G − F`; an edge of `F` *enters* the piece of its head and *leaves* the piece of its tail; a *square*
is the piece of `u`, the piece of `v` or a piece entered by two edges, `S_1, …, S_k` in the order from `u` to `v`;
a *link* is any other piece (one entering, one leaving edge); *terminals* of `S_i`: `a_i, b_i` heads of the entering
edges (`a_1 = b_1 = u`), `c_i, d_i` tails of the leaving edges (`c_k = d_k = v`); a *general path* is a sequence
`e_0, L_1, e_1, …, L_r, e_r` of edges of `F` and links from one square to the next; the *square decomposition* is
`S_1, P_{1,1}, P_{1,2}, S_2, …, S_k`; the *trace* of a path in a piece is its part inside the piece.

| A2 | Label | Result | MT | Note |
|---|---|---|---|---|
| Lemma 1 | `lem:basic-bounds` | `max{c,d} ≤ cp ≤ c+d−1`; `cp = d` iff a separating shortest path exists | Claims 6, 7 | proved in A2 |
| Prop. 4 | `prop:class` | `c(x,y) ≥ 3` is an equivalence relation (3-edge-connected components); `G ∈ DC_2` iff every class has pairwise distances ≤ 2; diameter two and cactus graphs lie in the class | – | |
| Ex. 1 | `ex:counterexamples` | `G_a`, `G_b`: `cp = 3 < c + d − 1` | Fig. 3.3 | the two counterexamples of Section 3 above |
| Prop. 5 | `prop:easy-pairs` | `d = 1 ⇒ cp = c`; `c = 1 ⇒ cp = d`; `c = 2 ⇒ cp ∈ {d, d+1}`; `d = 2 ⇒ cp ∈ {c, c+1}` | Claims 6, 7 | in the class every pair is of one of the four kinds |
| Lemmas 6-8 | `lem:orientation`, `lem:pieces`, `lem:degrees` | `F ⊆ p_1 ∪ p_2`; orientation; a `u`-`v` path visits a piece once; numbers of entering and leaving edges | Claim 19 | |
| **Thm 9** | `thm:structure` | square decomposition: entering/leaving edges of a square form minimum cuts; all `u`-`v` paths pass the squares in one order and follow one of the two general paths; **distinct terminals of a square have `c ≥ 3`** | Theorem 20 (Def. 38-40) | parts (i)-(iv) are the known structure of all minimum cuts for value two (Section 5b) |
| Lemma 10 | `lem:criterion` | a `u`-`v` path `R` separates iff in some square the other entering and the other leaving terminal are separated in `S_i ∖ R` | inside the proof of Theorem 22 | |
| **Thm 11** | `thm:characterization` | any graph, `c(u,v) = 2`: `cp = d` iff some square has an `x`-`y` path `p` with `d(u,x) + |p| + d(y,v) = d(u,v)` that separates the other two terminals in the square; else `cp = d + 1` | Theorem 22 | |
| Cor. 13 | `cor:two-edges` | in the class such a `p` has at most two edges | Claim 21 | |
| Lemma 14 | `lem:residual` | `F` = edges of `p_1 ∪ p_2` whose ends lie in different strong components of the residual digraph | – | Picard-Queyranne for value two |
| **Thm 15** | `thm:linear-time` (Alg. 1 `alg:cut-two`) | `O(|V|+|E|)`: decide `c(u,v) ≤ 2` and compute `cp` and a minimum cut-path, for every connected graph, or return a pair with `c ≥ 3`, `d ≥ 3` that certifies `G ∉ DC_2` (never for `G ∈ DC_2`) | Theorems 22, 23 (Alg. 6, 7) | MT: linear only when the decomposition is given; the certificate form was added after the referee pass |
| Cor. 16 | `cor:class-pairs` | in the class all pairs with `c ≤ 2` (hence all with `d ≥ 3`) in linear time; `d = 1` by one minimum cut | – | |
| Rem. 2 | `rem:coarser` | unions of some minimum cuts give coarser decompositions with the same criterion; the construction of MT (Transformations A, B, C) is of this kind | Alg. 2-5, Def. 41 | not proved that every run of Alg. 5 of MT gives such a union |
| **Thm 17** | `thm:hardness` | deciding `cp = d` is NP-complete for pairs with `c(u,v) = 2` in general graphs (add `u'` joined to `u` by two paths of length two; A1, Theorem 3.10) | – | new; answers, for the cut-value, question 2 of the conclusion of A1 (bounded `c(u,v)`) |
| Prop. 18 | `prop:open-pairs` | `cp = c` iff some minimum cut contains a `u`-`v` path; odd length, at least three if `d = 2` | proof of Theorem 15 | the pairs `d = 2`, `c ≥ 3` of the class stay open in A2 |

**Verification (2026-10-12).** `projects/clanok-2-min-cut-path.submission/checks/` (README with counts): every
statement on all 12112 connected graphs with at most 8 vertices and on 2953 random chains in the class (up to 40
vertices); the algorithm against brute force; 18 mutation tests. Independent referee pass with its own scripts:
`projects/clanok-2-min-cut-path.submission/review/referee-math.md` (no error; 11895 instances, 81 example values).
Every connected graph with at most 7 vertices lies in `DC_2`; 537 connected graphs with 8 vertices do not.
Outside the class the algorithm without the certificate returns `d + 1` where `cp = d` on 111 of 4789 random
instances, so the hypothesis on the class (or the certificate) is needed.

**Errors and gaps of MT Section 3.3** (details: `projects/clanok-2-min-cut-path.submission/drafts/core-notes.md` §3):
Definitions 38-40 do not fix which decomposition is meant and the proofs use unproved facts about it; condition 2
of Definition 39 is a consequence, not a definition; Transformations A, B, C and Algorithm 5 are not specified
precisely and Theorem 20 has only an "intuition of correctness"; the proof of Claim 21 is not an argument (case 2);
the key equivalence of Theorem 22 is asserted; Algorithm 7 starts with `P ← ∅` and intersects, removes vertices
where edges are meant, and Theorem 23 assumes the decomposition as given.

**Work on the open pairs** (`d(u,v) = 2`, `c(u,v) ≥ 3`): `projects/clanok-2-min-cut-path.submission/open-cases/`
holds the working files of AI agents (rounds 1-5, 2026-10-12 to 2026-10-22); current state and the list of what is
reviewed: `open-cases/status.md`. Not read by the author. In short: the open case is equivalent to the
zigzag problem ZZ + P2 (reviewed, `verify/rv-r6-chain.md`), and ZZ + P2 is in P, time `m^71 · poly` with `m <= n − 2`
switches (`open-cases/r7-desc.md` Theorem B, reviewed `verify/rv-r7-desc.md`). A2 rewrites this proof directly on the preorder, time `O(n^30)`, reviewed (`projects/clanok-2-min-cut-path.submission/review/referee-direct.md`). So every pair of `DC_2` is solved in
polynomial time, as reviewed by AI agents. Deciding `cp = c` is NP-complete on graphs of diameter three with
`d(u,v) = 2` (reviewed, `open-cases/theory-hardness.md` Thm 2.5) and FPT in `c`.

## 4. What each text contains beyond the other

**Only in MT** (material for further articles):
- chapter 2: tree-cut, 2-approximation, global minimum, partial path/cut property;
- chapter 3.3: Transformations A, B, C and the incremental construction (A2 replaces them by the canonical decomposition, Section 3a);
- chapter 4.5: almost polynomial average-case algorithm for sparse random graphs;
- chapter 5: symmetric case `c = d = cp`, algorithms Filter-BFS and Local-Cut.

**Only in A2:** the canonical square decomposition from the minimum cuts, the 3-edge-connectivity of the terminals,
the separation criterion and the characterization for every graph with `c(u,v) = 2`, linear time including the
decomposition, the certificate for graphs outside the class, NP-completeness for `c(u,v) = 2`.

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

Cited in A1 since the preserving revision of 2026-10-09 (introduction; Chung-Lu at Theorem 7.2; diameter three as an open question in the conclusion); not in MT; cite them in article 2 too (entries are in `knowledge/bibliography/references.bib`, reading notes in `knowledge/literature/`). Searched again 2026-10-09 (`knowledge/literature/searches.md`): the problem itself was not found elsewhere; no Discrete Applied Mathematics paper on a close problem was found.

| Problem | Relation to Min Cut-Path | Source |
|---|---|---|
| *Non-disconnecting* (Mao: non-separating, edge version) s-t path: `G - E(P)` connected; existence NP-hard; shortest one FPT in its length; polynomial on chordal graphs | opposite requirement to Separating Shortest Path; same "private channel" motivation | `Mao2021NonSeparating` (preprint), `Abhinav2022NonSeparating` (MFCS 2022) |
| Shortest Path Most Vital Edges (= length-bounded edge cut, unit lengths): delete `k` edges so that `d(s,t) >= l` | cuts that destroy short paths; NP-hard; for unit lengths NP-hard on diameter three and linear time on diameter two; for arbitrary lengths NP-hard on complete graphs (Theorem 5) | `Bazgan2019MostVital` (Theorem 4, Proposition 1 of arXiv v1); Baier et al. 2010 read, not added |
| Two disjoint paths, one of them shortest (2D1SP, two terminal pairs): NP-complete on undirected graphs with unit lengths; one-pair form = Min-Min disjoint paths ("shortest path with a disjoint counterpart") | mirror of Separating Shortest Path: the removal of a shortest path must leave a pair connected; neither the same problem nor its complement | `EilamTzoreff1998Disjoint` (DAM, Claim 1; cited in A1 since 2026-10-10); Xu et al. 2006, Guo and Shen 2013 read as abstracts only, not added |
| Length-bounded edge cut: no `s`-`t` path with at most `L` edges remains; NP-hard to approximate within 1.1377 for `L >= 4` | source of the term used for Most Vital Edges with unit lengths; companion of "no PTAS" | `Baier2010LengthBounded` (cited in A1 since 2026-10-10) |
| Maximally local-edge-connected graphs: diameter at most two implies `c(u,v) = min{deg u, deg v}` for all pairs (Fricke, Oellermann, Swart 2000, unpublished; Hellwig, Volkmann 2004 for digraphs; global form Plesník 1975) | **known theorem equal to the first half of Corollary 5.7 of A1**; Lemma 5.3 is the case distinction of the known proof; `cp = c + d - 1` is not in this literature | `Stuart2009Eavesdropping`, Theorem 11 (attributed in the Introduction of A1 since 2026-10-10; a sentence for Section 5 is proposed, not applied) |
| Cactus graphs = connected graphs with `c(x,y) <= 2` for all pairs | Lemma 6.1 of A1 is folklore; no source states exactly this sentence (nearest: Marx, Végh, ACM TALG 2015, Proposition 3.7 of arXiv 1304.6593v2) | not cited; the Introduction of A1 calls it a folklore fact |
| Treewidth reduction, connected `s`-`t` separators | tool and model of the FPT proof (Section 8 of A1); no theorem of the paper contains Min Cut-Path | `Marx2013Separators`, Section 3.3 |
| Network Diversion: minimal s-t cut containing a prescribed edge | a cut with prescribed content; open on undirected graphs (still on 2026-10-10), polynomial on planar graphs | `Bentert2025NetworkDiversion` |
| Matching Cut: an edge cut that is a matching | a cut with prescribed structure; polynomial on diameter two, NP-complete on every fixed diameter `>= 3` | `LeLe2019MatchingCut`, `Komusiewicz2020MatchingCut` (DAM) |
| Diameter of `G(n, p)` for `p >= c log n / n`, `c` constant | exact source for Theorem 7.2 of A1: with `c = alpha > 1`, `diam <= log n / log log n` w.h.p. | `ChungLu2001`, Theorem 4 (authors' PDF; journal numbering not compared) |
| Edge connectivity = minimum degree w.h.p. in `G(n, p)` | Theorem 7.3 of A1 | not verified first-hand: Bollobas, Thomason 1985 and Section 7.2 of `Bollobas2001` according to secondary sources |
| Chernoff tails `P(X <= a mu) <= exp(-mu h(a))`, `h(a) = a log a - a + 1`, and the upper tail with the same `h` | Lemma 7.4 of A1 | Frieze-Karonski, free PDF 2026: (34.19) and (34.17), Section 34.4, p. 707 (`phi(a - 1) = h(a)`); printed numbering (Ch. 21) not verified |

Added for A2 on 2026-10-12 (verdicts and exact locations: `projects/clanok-2-min-cut-path.submission/drafts/related-work.md`; searches logged in `knowledge/literature/searches.md`):

| Topic | Relation to A2 | Source |
|---|---|---|
| All minimum `s`-`t` cuts are the closed sets of the residual graph of one maximum flow; contracting its strong components gives an acyclic graph (the "strip" of Dinitz and Vainshtein, balanced for undirected graphs) | **the square decomposition is this structure for value two**: Theorem 9(i)-(iv) and Lemma 14 of A2 must be attributed; new in A2 are its explicit form with terminals and what is done with it | `PicardQueyranne1980` (Theorem 1, Corollary 6 of the authors' report), `BaswanaPandey2025Carcass` (Section 1); `DinitzVainshtein2000Carcass` only PARTIAL |
| 3-edge-connected components are vertex classes; cactus of the 2-edge cuts of a 2-edge-connected graph | the classes of `c(x,y) ≥ 3` in Proposition 4 of A2; "the square decomposition is the part of the cactus between `u` and `v`" is in no source (our derivation, not proved in A2) | `Mehlhorn2017Certifying` (Section 1, Lemma 11 of arXiv v3), `NagamochiKameda1996` |
| Classes defined by bounded local edge-connectivity | nearest named classes; the class `DC_2` ("small distance or small local connectivity") was not found under any name | `Aboulker2017Coloring` |
| Standard algorithms (breadth-first search, strong components, augmenting paths, flow decomposition), bridges | Section 5 of A2 | `Erickson2019Algorithms`, `Tarjan1972DFS` (abstract only), `Schmidt2013TwoConnectivity` |

Not found anywhere: the separation criterion, the characterization of `cp = d` for `c(u,v) = 2`, the algorithm, the
hardness for `c(u,v) = 2` (DBLP, Google Scholar and MathSciNet were not searched).

Diameter two is the boundary of tractability for Most Vital Edges with unit edge lengths and for Matching Cut. Whether Min Cut-Path is NP-hard on graphs of diameter three is open (the reduction of A1 produces graphs of large diameter).

Note for texts: if `cp = c + d − 1` holds, the union of any minimum cut and any shortest path is a minimum cut-path (A1, Remark 5.6).

## 6. Open problems and directions

From MT and the conclusion of A1:
1. Class *diam or cut 2* (`DC_2`): the pairs with `d(u, v) = 2` and `c(u, v) ≥ 3` (MT and A2 solve the pairs with `c(u, v) ≤ 2`, A2 in linear time); in A1 phrased as merging two polynomial "islands". There `cp ∈ {c, c+1}` and `cp = c` iff some minimum cut contains a `u`-`v` path (A2, Proposition 18). On graphs with at most 8 vertices: `cp = c` for 400 pairs, `cp = c + 1` for 65193.
   Partial results (AI agents, 2026-10-12 to 2026-10-22, not in any manuscript): `open-cases/status.md` (Section 3a).
   Question 2 of the conclusion of A1 (bounded `c(u,v)` or `d(u,v)`): answered for the cut-value by A2, Theorem 17 (NP-complete already for `c(u,v) = 2`); A1's text still lists it as open.
2. Planar graphs (cut ↔ cycle duality), graphs of bounded treewidth.
3. Approximation algorithms with a guarantee for general graphs (only the trivial 2-approximation is known).
   No PTAS unless P = NP (A1, Theorem 4.3, 2026-10-10; no FPTAS is Corollary 4.4): in the graph of the reduction every cut-path has at least
   `Lambda + eta*` edges, `eta*` = the least number of threads a chain path misses (Lemma 4.1), and `eta*` is at
   least a fifth of the least number of unsatisfied clauses when every variable occurs five times (Lemma 4.2);
   with the gap problem of `Feige1998Threshold`. Open: the best factor between `1 + eps_0` and two; whether
   `cp = Lambda + eta*` always holds in these graphs (it does on the 38 formulas of `checks/check_gap_lemmas.py`).
4. Weighted and directed variants.
5. Experimental evaluation on real and random networks.
6. Structure of graphs with a fixed value `cp(u, v)`.
7. Further "islands of polynomial-time solvability".

## 7. Planned manuscripts

Author's decision (2026-10-07): **article 2 will be produced from the master's thesis** (project `projects/clanok-2-min-cut-path/`; target Algorithmica, Springer Nature template `sn-jnl` prepared 2026-10-08). Written 2026-10-12 from Section 3.3 of MT (the class `DC_2`; Section 3a above), working title *Min Cut-Path on Graphs with Distance or Cut-Value at Most Two*; the author has not yet read it. The LaTeX source of MT is not in the repository; the text was written from the PDF. Article 1 targets Discrete Applied Mathematics and was ported to its template on 2026-10-08 (class `cas-sc`).

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
| square, link, piece, terminal (A2) | – | štvorec, článok, kus, terminál |
| square decomposition (A2; "general square graph" in MT) | – | dekompozícia na štvorce |
| entering / leaving edge, tail, head (A2) | – | vstupná / výstupná hrana, chvost, hlava |
| trace of a path in a square (A2) | – | stopa cesty vo štvorci |
| nearly k-regular graph | téměř k-regulární graf | takmer k-regulárny graf |
| symmetric cut-path | symetrická řezo-cesta | symetrická rez-cesta |
| tree-cut | – | strom-rez |
| separating shortest path | – | oddeľujúca najkratšia cesta |
| chain, chain link, thread, threading | – | reťaz, článok reťaze, vlákno, navliekanie |
| average (1+ε)-approximation scheme | aproximační schéma s průměrnou zárukou | aproximačná schéma v priemernom prípade |
| almost polynomial algorithm | téměř polynomiální algoritmus | takmer polynomiálny algoritmus |
