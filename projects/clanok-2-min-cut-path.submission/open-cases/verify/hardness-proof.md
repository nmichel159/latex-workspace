# Adversarial verification of Theorem 2.5, Corollary 2.6 and Section 5 of `theory-hardness.md`

Agent "verify-hardness-proof", 2026-10-12. Target: `open-cases/theory-hardness.md` (version of 2026-10-12 10:21).
Scripts and raw results: `open-cases/verify/hardness-proof-scripts/` (own code; the construction is re-implemented from
the text of Section 2.1 without importing `hardness/`; the max flow, the enumeration of minimum cuts and the exact `cp`
are own routines, validated first).

## 0. Verdict

| Claim | Verdict | Basis |
|---|---|---|
| Lemma 2.2 (forcing), Lemma 2.3 (all minimum cuts are the `A_tau`), Lemma 2.4 (cut graphs) | **hold** | every step re-derived (Section 1); checked on 4537 formulas |
| Theorem 2.5: PATH-IN-MIN-CUT NP-complete, also with `d(u,v) = 2` on graphs of diameter exactly 3 | **holds** | Section 1; no counterexample in 4537 formulas, exact `cp` by enumeration of all vertex sets on 148 of them |
| Corollary 2.6 (a), (b): `cp = c` NP-complete; decision Min Cut-Path NP-complete on diameter 3 with `b = c`; computing `cp` NP-hard for `d = 2`; hence also for the class "`d <= 3` or `c <= 2`" | **hold** | Section 1.5 |
| Corollary 2.6 (c): deciding `cp = c + d - 1` is coNP-complete (also `d = 2`, diameter 3) | **holds**; the gloss "i.e. whether the union of a minimum cut and a shortest path is a minimum cut-path" is exact only for `d = 2` (E2) | Section 1.5 |
| Corollary 2.6 (d): every path inside a minimum cut has length `>= 2m+1` | **holds**; the written proof is terse, a two-line completion is given in 1.5 | all simple paths enumerated in 1290 graphs |
| Section 5: for "`c(x,y) <= 3` for all pairs", deciding `cp = c` is polynomial | **holds** (it needs only `c(u,v) <= 3`) | Section 1.6; compared with exact `cp` on 57096 pairs |

No gap was found in the proofs. Three slips that do not affect any result:

- **E1 (Remark (2) after Theorem 2.5).** "fillers of `K_A` and `K_B` are at distance 3 with `c = M - 1`" is wrong:
  `delta(K_A)` separates them with `c0 = M - 2` edges, and the argument of Lemmas 2.2-2.3 gives `c(f_A, f_B) = M - 2`.
  Computed: `c(fA0, fB0) = M - 2` for all 4537 formulas. The point of the remark (the pair is at distance 3 with
  `c >= 3`, so the graph is not in DC) stands.
- **E2 (Corollary 2.6 (c)).** "`cp = c + d - 1`, i.e. whether the union of a minimum cut and a shortest path is a
  minimum cut-path (Remark 5.6)": Remark 5.6 of article 1 gives only one direction (`cp = c + d - 1` implies that
  every such union is minimum). Read as "some union is minimum", the converse is false for `d >= 3`. Example
  (8 vertices, 11 edges; none exists on `<= 7` vertices, exhaustive over the networkx atlas):
  edges `u-p p-y u-q q-y x-r r-v x-s s-v u-x x-y y-v`; `c = 3`, `d = 3`, `cp = 3`
  (brute force), `c + d - 1 = 5`; the minimum cut `delta({u,p,q,y}) = {ux, xy, yv}` contains the shortest path
  `u x y v`, so its union with that path is a minimum cut-path although `cp != c + d - 1`
  (`results-probe-misc.txt`). For `d = 2` a minimum cut meets a path of length 2 in exactly one edge (its middle
  vertex cannot lie on both sides), every union has `c + 1` edges, and the two questions coincide; the coNP claim is
  stated for `cp = c + d - 1`, so it is unaffected. Suggested wording: "Deciding `cp = c + d - 1` (in which case, by
  article 1, Remark 5.6, the union of any minimum cut and any shortest path is a minimum cut-path; for `d = 2` the two
  questions coincide) is coNP-complete".
- **E3 (Corollary 2.6 (d)).** "no constant bound on the length of the paths that have to be tested exists unless
  P = NP": the forced length `>= 2m+1` is unconditional, so "unless P = NP" is superfluous there (it belongs to the
  different statement that no polynomial algorithm tests only paths of bounded length). "Smallest instances
  (one-literal clauses)" means the smallest with `m = 2`; with `m = 1`, `phi = (x_1)` gives 13 vertices, `c = 4`
  and a path of length 3.

## 1. Line-by-line check

Notation as in `theory-hardness.md`: `m` clauses, `L` literal occurrences, `c0 = (m+1) + 2L`, `M = c0 + 2`.

### 1.1 Construction (Section 2.1)

- Names: `K_A` holds `h_0 = u, ..., h_m, a_1, a_2` and `M - m - 3 = 2L >= 2` fillers; `K_B` symmetric with
  `beta_m = v`. All named vertices are distinct, so the graph is simple: an occurrence vertex of `C_k` has the four
  distinct neighbours `beta_{k-1}, beta_k, a_1, a_2` (positive) or `h_{k-1}, h_k, b_1, b_2` (negative), and sync edges
  join distinct occurrence vertices once each.
- Counts `2M + L` vertices and `M(M-1) + (m+1) + 4L + sum_i (abs(O_i) - 1)` edges: correct (asserted in
  `construct.py` for every formula). Size `O((m + L)^2)`: polynomial.
- Clauses with repeated literals, with both `x_i` and `not x_i`, variables occurring once, and gaps in the variable
  indices are all admissible; all occur in the tested families.
- The code `hardness/reduction.py` (read after `construct.py` was written) builds the same graph (sync path in the
  order of occurrence; the order is irrelevant to every proof).

### 1.2 Lemma 2.2 (forcing)

- `delta(K_A)` = the `m + 1` edges of `F` and the two `K_A`-edges of each of the `L` occurrence vertices: `c0` edges,
  so `c(u,v) <= c0`. Correct.
- If `a in K_A - A`: the edge `ua` and the paths `u w a` (`w in K_A - {u,a}`) are `M - 1` edge-disjoint `u`-`a` paths,
  each with an edge in `delta(A)`, so `abs(delta(A)) >= M - 1 = c0 + 1 > c`. Same for `K_B` and `v`. Correct.
- Margin: the proof needs only `M - 1 > c0`. Removing one filler from each clique (`M = c0 + 1`) still gave the same
  minimum cuts and answers on three unsatisfiable formulas (`probe_misc.py`), so `M = c0 + 2` is not tight; nothing
  depends on this.

### 1.3 Lemma 2.3 (all minimum cuts)

For `K_A subset A subset V - K_B`: no clique edge is cut, all of `F` is cut, an occurrence vertex contributes exactly
its two edges to the opposite clique, and the only edges between occurrence vertices are sync edges. Hence
`abs(delta(A)) = c0 + s(A)`. With Lemma 2.2, `c = c0` (attained by `A = K_A`) and the minimum cuts are the `A` with
`s(A) = 0`; since each `O_i` induces a connected sync path, these are exactly the `A_tau`, distinct for distinct
assignments of the occurring variables. Correct. In particular every `A_tau` is minimum, and no other set is: a set
splitting a clique costs `>= c0 + 1`, a set splitting some `O_i` costs `c0 + s(A) >= c0 + 1`; `F` edges and
occurrence vertices on "unexpected sides" are covered by the formula `c0 + s(A)`.
The sync edges are essential: without them the minimum cuts are all `2^L` sets `K_A + S` and the unsatisfiable
formulas `(x_1)(not x_1)`, the four 2-clauses on `x_1, x_2`, and `(x_1 x_1 x_1)(not x_1 not x_1 not x_1)` become
yes-instances (`results-probe-misc.txt`).

### 1.4 Lemma 2.4 (cut graphs)

Edges of `H_tau = (V, delta(A_tau))`: `F`; a true positive occurrence of `C_k` (in `A_tau`) contributes
`o beta_{k-1}`, `o beta_k`; a true negative one (outside `A_tau`) `o h_{k-1}`, `o h_k`; a false positive one (outside)
`o a_1`, `o a_2`; a false negative one (inside) `o b_1`, `o b_2`. Nothing else (no clique edge, no sync edge).
So `H_tau` has the components: the levels `L_k = {h_k, beta_k}` linked through true occurrence vertices;
`{a_1, a_2}` with the false positive occurrence vertices; `{b_1, b_2}` with the false negative ones; isolated
fillers. The direction (⇐) is immediate; in (⇒) the set `W` is closed in `H_tau` because `h_j`, `beta_j` (`j <= k-1`)
have `H_tau`-neighbours only in `L_j` and among the true occurrence vertices of `C_j`, `C_{j+1}`, and a true
occurrence vertex of `C_j` has `H_tau`-neighbours only in `L_{j-1} + L_j`. Correct, including the boundary cases
`k = 1` (`W = L_0`) and `k = m`.
Probe (`probe_paths.py`): in 1290 reduction graphs (all formulas with `m <= 2` over `x_1, x_2` with clauses of
size 1-3, and 100 random 3-CNF with `m <= 5`), all 12956 simple `u`-`v` paths of all cut graphs `H_A` of all
minimum cuts were enumerated: each uses only `h_k`, `beta_k` and true occurrence vertices, no sync edge, and has odd
length `>= 2m + 1`. So no path uses `a_1, a_2, b_1, b_2`, fillers or sync edges.

### 1.5 Theorem 2.5 and Corollary 2.6

- **NP membership.** Certificate a `u`-`v` path `P`; Lemma 1.3 (c) (`c_{G-P}(u,v) = c(u,v) - abs(P)`) is tested by
  two max-flows. The proof of (c)⇒(a) is correct (`P` plus a minimum cut of `G - P` is a `u`-`v` cut of size `c`
  containing `P`; it equals `delta` of the component of `u`). Alternatively the set `A` is a certificate. Correct.
- **Hardness.** `phi` satisfiable ⇔ some `H_tau` connects `u`, `v` (Lemma 2.4) ⇔ some minimum cut contains a
  `u`-`v` path (Lemma 2.3: the minimum cuts are exactly the `A_tau`; a `u`-`v` walk in `H_A` contains a path).
  The map `phi -> (G, u, v)` is polynomial. Correct (CNF-SAT, hence 3-SAT with repeated literals allowed).
- **`d(u,v) = 2`.** `u = h_0` and `v = beta_m` are not adjacent (`F` joins `h_0` only to `beta_0`, `m >= 1`; no other
  edge joins the cliques); `h_m` is a common neighbour. Correct.
- **Diameter exactly 3.** Clique pairs: 1; `x in K_A`, `y in K_B`: `x h_m beta_m y`; occurrence vertex to clique
  vertex: `<= 2` (it has neighbours in both cliques); two occurrence vertices: through their `K_A`-neighbours,
  `<= 3`. A filler of `K_A` and one of `K_B` (they exist, `2L >= 2`) have neighbourhoods `K_A - f_A` and `K_B - f_B`,
  disjoint and non-adjacent to the other filler: distance 3. Correct.
- **2.6 (a).** Lemma 1.1 (`cp = c` iff some minimum cut contains a `u`-`v` path) is correct; NP membership:
  certificate a cut-path with `c` edges. Correct.
- **2.6 (b).** `cp >= c` always (article 1, Lemma 2.3), so `cp <= b := c(u,v)` iff `cp = c`; `b` is computed in
  polynomial time (or directly as `c0`). NP membership as in article 1, `thm:mcp-np-complete` (a cut-path with `<= b` edges is checked by two searches).
  Every graph of diameter `<= 3` lies in "`d <= 3` or `c <= 2`", so the class result follows. Correct.
- **2.6 (c).** `cp <= c + d - 1` always (article 1, Lemma 2.3), so the complement of "`cp = c + d - 1`" is
  "some cut-path has `<= c + d - 2` edges", in NP: coNP membership. For `d = 2`, `cp in {c, c+1}`, so
  `cp = c + 1 = c + d - 1` iff not `cp = c`; UNSAT reduces to it by the same map. Correct (wording E2).
- **2.6 (d).** Completion of the terse proof: for a satisfying `tau` and `k = 1..m` put
  `W_k = L_0 + ... + L_{k-1} + {true occurrence vertices of C_1..C_{k-1}}`. By 1.4 the only `H_tau`-edges leaving
  `W_k` join `L_{k-1}` to a true occurrence vertex `o` of `C_k`, whose only `H_tau`-neighbours are its two vertices
  in `L_{k-1} + L_k` (one in each). A `u`-`v` path leaves `W_k` (`u in W_k`, `v notin W_k`), so it contains such an
  `o` and both its edges; for different `k` these edge pairs are disjoint. Hence at least `2m` edges, and the length
  is odd (Lemma 1.2 (i)): `>= 2m + 1`. Correct. The example `(x_1)(x_1)`: 20 vertices, 84 edges, `c = cp = 7`,
  `d = 2`, diameter 3, two minimum cuts, exactly one `u`-`v` path in a minimum cut, of length 5 (confirmed).

### 1.6 Section 5: "`c(x,y) <= 3` for all pairs" gives a polynomial test of `cp = c`

Only `c(u,v) <= 3` is used: a path inside a minimum cut has odd length `<= c(u,v)` (Lemma 1.2 (i), (iii): its edges
lie in `delta(A)`, `abs(delta(A)) = c`), so it has length 1 (then `uv in E`, `d = 1`, answer yes) or 3; the `O(n^2)`
paths `u x y v` are each tested by one max-flow (Lemma 1.3 (c)). Correct. Compared with the exact `cp`
(`probe_c3.py`): (i) all connected graphs with `<= 7` vertices, all 32518 ordered pairs with `c <= 3` (15128 with
`cp = c`, 24 of them with `d >= 2`); (ii) 600 random connected graphs with 9-15 vertices in the class
"`c(x,y) <= 3` for all pairs" (checked by a Gomory-Hu tree), all 24578 non-adjacent pairs (20 with `cp = c`, all with
`c = 3`): 0 disagreements. (The table's "Min Cut-Path: open" for this class is not a claim and was not examined.)

## 2. Attacks that failed

1. Minimum cuts other than the `A_tau` (split cliques, `F` edges, sync paths, occurrence vertices on the wrong side):
   excluded by Lemmas 2.2-2.3; brute force over **all** `2^(n-2)` vertex sets on 148 instances (13 unsatisfiable,
   13-25 vertices) found exactly the `A_tau`; random sets splitting a clique always cost `>= c0 + 1` (V7).
2. Paths through `a_1, a_2, b_1, b_2`, fillers, sync edges or clique edges (shortcuts between non-consecutive
   levels): impossible by the component structure of `H_tau` (1.4); none among 12956 enumerated paths.
3. Distances: every reduction graph has `d(u,v) = 2` and diameter exactly 3 (4537 of 4537).
4. Degenerate formulas (clauses of length 1-4, repeated and complementary literals, single occurrences, `m = 1`):
   no failure.
5. Exact `cp` without any lemma: `cp = min over A of abs(delta(A)) + dist(u,v)` with the edges of `delta(A)` of
   length 0 and the others of length 1; on 148 instances `cp = c` iff `phi` is satisfiable and `cp in {c, c+1}`.

## 3. Computations

| Script | What | Result file | Outcome |
|---|---|---|---|
| `construct.py` | the construction of Section 2.1 from the text; `A_tau`; assignments | – | library |
| `vexact.py` | own unit-capacity max flow, Picard-Queyranne enumeration of minimum cuts, cut sizes of all vertex sets (numpy, chunked), exact `cp` by enumeration of all vertex sets | – | library |
| `test_vexact.py` | `vexact` vs networkx connectivity, brute-force minimum cuts, and (`n <= 6`) `cp = min over paths P of abs(P) + c_{G-P}`, on all 39692 ordered pairs of the 995 connected graphs with 2-7 vertices | `results-test-vexact.txt` | 0 failures, 16 s |
| `verify_reduction.py` | V1-V8 (docstring) on 4537 formulas: all with `m <= 2` over `x_1, x_2` with clause multisets of size 1-3 (1190), all with `m = 3` and clauses of size 1-2 (2744), 400 random 3-CNF (`n <= 7`, `m <= 14`), 200 random mixed lengths 1-4, 3 unsatisfiable cores; 13-244 vertices, 36-10323 edges, `c` 4-99; 3694 satisfiable, 843 not | `results-verify-reduction.txt` | 0 failures, 285 s on 30 processes |
| `probe_paths.py` | all simple `u`-`v` paths in all `H_A`, 1290 formulas | `results-probe-paths.txt` | 12956 paths, 0 violations |
| `probe_c3.py` | Section 5, `c(u,v) <= 3` | `results-probe-c3.txt` | 57096 pairs, 0 disagreements |
| `probe_misc.py` | E2 example; sensitivity (`M = c0 + 1`; no sync edges) | `results-probe-misc.txt` | as stated in 0 and 1.2-1.3 |
| `probe_e2_min.py` | E2-type pairs on all connected graphs with `<= 7` vertices | `results-probe-e2-min.txt` | 13 pairs with `d >= 3`, `cp < c + d - 1`; none of E2 type |

## 4. Scope

Checked: Sections 1 (Lemmas 1.1-1.3 and Corollary 1.4 as far as Theorem 2.5 uses them), 2, and the table and claim of
Section 5. Not checked: Lemma 3.1 (O5), Section 4 (Lemmas 4.1-4.3), Sections 6-7 (DC obstruction, polynomial cases
other than `c <= 3`), except where quoted above. Article 1 was opened at Lemma 2.3 (`lem:basic-bounds`), Theorem 5.5
(`thm:diameter-two`), Remark 5.6 (`rem:algorithm`), the decision version and `thm:mcp-np-complete`, and the open
questions of its conclusion; the statements of `theory-hardness.md` about those places are accurate (questions 1 and
3 answered, question 2 answered for bounded `d`).
