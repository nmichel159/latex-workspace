# Open case of DC: computational experiments (agent "experiments", 2026-10-12)

Setting: `G in DC`, `d(u,v) = 2`, `c(u,v) >= 3`; then `cp(u,v) = c(u,v)` iff some minimum `u`-`v` cut contains a
`u`-`v` path ("cut path" below). Scripts and raw results are in `open-cases/experiments/`; the library
`experiments/cutpaths.py` imports `checks/mcp.py` read-only. Every number below is copied from a `results-*.txt`
file named in the section.

## 0. Summary

1. **O4 is false, in the weak and the strong form.** The 10-vertex DC graph `E10` (Section 2) has `d(u,v) = 2`,
   `c(u,v) = cp(u,v) = 5`, and its only cut path has length 5. The test O3 (paths of length 3) answers
   `cp = c + 1` there, so the candidate algorithm of task 5 is wrong on DC.
2. **The length is unbounded in DC.** The family `F(k)` (Section 3) has `4k + 2` vertices, lies in DC, has
   `d(u,v) = 2`, `c(u,v) = cp(u,v) = 2k + 1`, and its only cut path has length `2k + 1`. Proof below (it uses the
   residual-closure description O6); brute-force check for `k <= 5`.
3. **`E10` is vertex-minimal**, also among graphs outside DC: no pair of any connected graph with at most 9
   vertices has a cut path of length `>= 5` (exhaustive, Section 4). Local search on 10 vertices finds 17 edges as
   the minimum, every 17-edge example it lists is isomorphic to `E10`; outside DC the fewest edges found on 10
   vertices is 18 (`E10` plus one edge).
4. **O1 and O5 pass every test** (Section 5): O1 on all pairs with a cut path and `c >= 3` of all connected graphs
   with `<= 8` vertices and on all random instances; O5 on all ordered pairs of all graphs with `<= 7` vertices.
   O1 also has a short proof (Section 5).
5. **Random instances with 9-16 vertices** (Section 6): 147,502 DC graphs, 1,890,041 pairs with `d = 2`,
   `c >= 3`, of them 18,323 with `cp = c`; the length-3 test misses 1,144 of these (6.2 %). It never errs on
   9 vertices (exhaustive there, Section 4).
6. **Bounded numbers of generators do not help either** (Section 7, exploratory): the DC graphs `G(k)`
   (`k = 2..7`) have a unique cut path, and every minimum cut containing it needs `k` vertices besides `u` to
   generate its `u`-side by residual closure, and `k` besides `v` for its `v`-side.
7. Open for the theory agents: whether "cp = c?" is NP-hard on DC. The constructions above show where a
   reduction could get its long forced alternating paths: one-vertex ears supply the doubled capacity, and edges
   inside the sides of the planted cut are free (Lemma M, Section 3).

## 1. Routines and their validation (task 1)

`cutpaths.py`:

- `PairInfo(g, u, v)`: one maximum flow (`mcp.maxflow`), the residual digraph (an edge with flow `a -> b` gives only
  the arc `b -> a`, an edge without flow gives both arcs), reach masks of all vertices.
- `cut_paths()`: depth-first search over paths `x_0 = u, x_1, ..., x_k = v` whose edges carry flow
  `x_{2i} -> x_{2i+1}` and `x_{2i+2} -> x_{2i+1}`, pruned as soon as the residual closure of the even vertices
  contains an odd vertex or `v`. By O6 (Picard-Queyranne, report Theorem 1, p. 4, as recorded in the workspace note
  `knowledge/literature/PicardQueyranne1980.md`) a path lies in some minimum cut iff it passes both tests, and both
  tests are inherited by prefixes, so the search returns exactly the cut paths.
- `shortest_cut_path()`: iterative deepening over lengths 1, 3, 5, ...
- `o3_paths()`, `candidate_dc()`: the lead's O3 test, implemented independently by a set-to-set maximum flow
  between `{u, b}` and `{a, v}` on a capacity matrix.
- `dc_violations()`, `class3()`: pairs with `d >= 3` and `c >= 3`; the class `Q` of `u` (`c(u,x) >= 3`).

Validation `validate.py` -> `results-validate.txt` (all connected graphs with 2-8 vertices; ordered pairs for
`n <= 7`, unordered for `n = 8`: 351,148 pairs). Compared with brute force over all vertex sets
(`mcp.min_cuts_by_sets` and plain path enumeration inside every minimum cut) and with `mcp.cp_brute`:
`c(u,v)`, the full set of cut paths, the shortest length, `cp = c` iff a cut path exists, and the length-3 paths of
the O3 test. **0 failures.** (The table "by (d, lengths)" at the end of that file is cumulative over all `n`.)

## 2. The counterexample `E10` to O4 (tasks 2 and 5)

`n = 10`, `m = 17`, `u = 0`, `v = 5`:

    0-1 1-2 2-3 3-4 4-5   0-2 0-6 2-6 0-4 0-7 4-7   1-5 1-8 5-8 3-5 3-9 5-9

- In DC (`mcp.in_dc` and `cutpaths.in_dc`); diameter 3; the six pairs at distance 3 (`0-9, 5-6, 6-8, 6-9, 7-8,
  7-9`) all have `c = 2`.
- `d(u,v) = 2` (common neighbors 1 and 4), `c(u,v) = 5`, `cp(u,v) = 5 = c` by `mcp.cp_brute`, `mcp.cp_subsets` and
  `mcp.cp_definition` (three independent computations).
- All 21 minimum `u`-`v` cuts enumerated by vertex sets: the only `u`-`v` path inside any of them is
  `0-1-2-3-4-5`, inside `delta({0,2,4,6,7})`. No minimum cut contains a path of length 3.
- Structure: the path alternates between `{0,2,4}` and `{1,3,5}`; on the side of `u` the vertex `u` has two
  edge-disjoint routes to `x2` (edge `0-2`, ear `0-6-2`) and to `x4` (`0-4`, `0-7-4`); on the side of `v` the
  same for `x1`, `x3` (`1-5`, `1-8-5`, `3-5`, `3-9-5`). Flow: `0-1-5`, `0-2-1-8-5`, `0-6-2-3-5`, `0-4-3-9-5`,
  `0-7-4-5`. The four ears are one-vertex ears of O2; all path vertices lie in `Q` (O1).
- Re-checked with `mcp.py` only: `verify_examples.py` -> `results-verify-examples.txt`.

## 3. The family `F(k)`: unbounded length in DC

`family.py` -> `results-family.txt`. Vertices `x_0, ..., x_{2k+1}` (`u = x_0`, `v = x_{2k+1}`), `y_1..y_k`,
`z_0..z_{k-1}`; edges:

- the path `x_0 x_1 ... x_{2k+1}`;
- `u x_{2i}`, `u y_i`, `y_i x_{2i}` for `1 <= i <= k`; `x_{2j+1} v`, `x_{2j+1} z_j`, `z_j v` for `0 <= j <= k-1`;
- all edges among the even `x`'s and among the odd `x`'s ("cliques").

`n = 4k + 2`, `m = 6k + 1 + 2 binom(k+1, 2)`. `F(1)` is the known 6-vertex example; `F(2)` without the cliques
is `E10` (with the cliques, 19 edges, also a counterexample).

**Claim F.** For every `k >= 1`: `F(k) in DC`, `d(u,v) = 2`, `c(u,v) = cp(u,v) = 2k + 1`, and the only `u`-`v`
path contained in a minimum `u`-`v` cut is `x_0 x_1 ... x_{2k+1}`. Status: proved below (using O6); computed for
`k <= 5` by brute force over all vertex sets (number of minimum cuts 5, 9, 17, 33, 65 for `k = 1..5`).

*Proof.* `deg u = 2k + 1`. The flow: one unit on each of `u x_{2i}` and `u y_i x_{2i}` (so `x_{2i}` receives 2 for
`i >= 1`), one unit on `u x_1`; every even `x_{2i}` (`i >= 1`) sends one unit to each path neighbor; every odd
`x_{2j+1}` (`j < k`) receives two units and sends them on `x_{2j+1} v` and `x_{2j+1} z_j v`; `x_{2k}` sends one
unit to `v` on the path edge. These are `2k + 1` edge-disjoint paths, so `c = 2k + 1`. For
`A = {x_0, x_2, ..., x_{2k}} + {y_i}` the cut `delta(A)` consists of the `2k + 1` path edges, so it is minimum and
contains the path; `cp = c`. `d(u,v) = 2` by `u x_1 v`. DC: two even (two odd) `x`'s are adjacent; an even
`x_{2i}` and an odd `x` are at distance `<= 2` through the odd neighbor `x_{2i+1}` of `x_{2i}`; every `y_i`, `z_j`
has degree 2. Uniqueness: in the residual digraph of this flow, `u` has no out-arc, `y_i` has only `y_i -> u`, and
`x_{2i}` (`i >= 1`) has out-arcs only to `u`, `y_i` and the other even `x`'s; so the closure of the even `x`'s is
`A` and contains no odd vertex. A cut path must leave `u` on a flow edge: to `x_{2i}` or `y_i` it continues
backwards on a flow edge into that vertex, whose only other tail is `y_i` resp. nothing, and `y_i` has no unused
outgoing flow edge, a dead end; so it starts `u x_1`. From an odd `x_{2j+1}` the only unused flow edge into it
comes from `x_{2j+2}`; from an even `x_{2i}` the only unused flow edge out of it goes to `x_{2i+1}`. Hence the path
is forced. (The cliques carry no flow.) []

Without the cliques `F(k)` is not in DC for `k >= 3` (for `k = 3` the pair `x_2, x_5` has `d = 3`, `c = 4`), but the claim
on the paths still holds (computed for `k <= 5`). Adding edges inside the sides is harmless by:

**Lemma M (monotonicity).** If `delta(A)` is a minimum `u`-`v` cut of `G` and the edge `e` has both ends in `A` or
both in `V - A`, then `c_{G+e}(u,v) = c_G(u,v)`, `delta(A)` is a minimum cut of `G + e`, and every minimum cut of
`G + e` is a minimum cut of `G` (same edge set). Hence the cut paths of `G + e` form a subset of those of `G` and
include those inside `delta(A)`. *Proof.* `c` does not decrease when an edge is added and `delta_{G+e}(A) =
delta_G(A)`. If `delta_{G+e}(B)` is minimum, `|delta_G(B)| <= c`, so `delta_G(B)` is minimum, and `e` cannot cross
`B` (else `|delta_G(B)| = c - 1`). []

Local search for shorter instances with a forced length-7 path (`climb.py`, 64 seeds x 40,000 steps each): none
found on 11, 12 or 13 vertices (in DC or not), found on 14 vertices (62 of 64 seeds) with at least 26 edges, e.g.
`F(3)` without cliques plus the edge `x_1 x_5`. Results: `results-climb-n1{1,2,3,4}-L7-*.txt`. This is evidence
only; it suggests that a forced length `2k + 1` needs `4k + 2` vertices.

## 4. Smallest instances, inside and outside DC (task 4)

`extend9.py` -> `results-extend9.txt`. Every connected 9-vertex graph is a connected 8-vertex graph plus a vertex
(delete a non-cut vertex); the 11,117 connected 8-vertex graphs (cached list of the checks agent, count verified)
times 255 neighborhoods give 2,834,835 labelled candidates covering all isomorphism classes. A cut path of length
`L` needs `c(u,v) >= L`, so length `>= 5` needs degrees `>= 5`; on 9 vertices this forces `d(u,v) <= 2`.

- 29,381,216 pairs (with repetitions) with `d = 2`, `c >= 3`; 102,793 have a cut path; 2,941,169 have `c >= 5`.
- **0 pairs with a cut path of length `>= 5`**, in DC or not. With the data for `n <= 8`
  (`checks/results-open-cases.txt`, and `results-validate.txt`), every cut path of a pair with `d(u,v) = 2` on at
  most 9 vertices has length 3, and O3 is exact there.
- Hence the smallest graphs with a cut path of length `>= 5` have 10 vertices; `E10` is one of them and lies in DC.
- Local search on 10 vertices (`climb.py 10 5 ...`, 64 seeds x 30,000 steps): fewest edges 17 for "any graph" and
  for DC (all 17-edge results are isomorphic to `E10` with `u, v` marked, `results-verify-examples.txt`); fewest
  edges outside DC 18, e.g. `E10 + 6-7` (the two ears on the side of `u` joined; the pair `5, 6` then has
  `d = 3`, `c = 3`). These minima are evidence, not exhaustive.

Outside DC the same mechanism works: the class hypothesis does not prevent long forced paths, it only constrains
how the core is joined (all path vertices are pairwise at distance `<= 2`).

## 5. O1 and O5 (task 3)

**O1** (if `c(u,v) >= 3` and a minimum cut `delta(A)` contains the `u`-`v` path `P`, every vertex `x` of `P` has
`c(u,x) >= 3`). Tests: every pair with `c >= 3` and a cut path of every connected graph with `<= 8` vertices
(140,392 pairs, ordered for `n <= 7`), all random instances of Section 6, all examples above: **0 failures**.
Proof (repairs nothing in the lead's sketch, fills the case analysis): suppose `x in P`, `c(u,x) <= 2`, and let
`delta(X)`, `|delta(X)| <= 2`, separate `x` from `u`, with `x in X`, `u notin X`. If `v in X`, `delta(X)` is a
`u`-`v` cut of size `<= 2 < c`; so `v notin X`. `P` enters and leaves `X`, so `delta(X) = {e_1, e_2}` are the edges
where `P` enters and leaves, `e_1 = y s_1`, `e_2 = s_2 z` with `s_1, s_2 in X`, `y, z notin X`, and the subpath
`P[s_1, s_2]` lies in `X` with `t >= 0` edges, all in `delta(A)`. If `y, z` are on the same side of `A`, move `X`
to that side: `e_1, e_2` and the `t` inner edges leave the cut, other edges are unaffected; the cut drops by
`>= 2`. If `y, z` are on different sides, `s_1, s_2` are on different sides, so `t >= 1`; move `X` to the side
of `y`: `e_1` and the `t` edges leave, `e_2` stays; the cut drops by `>= 1 + t >= 2`. Both contradict minimality
(the new side still contains `u` and not `v`). []

**O5** (adding `w` adjacent to `u`, `v`): for all 39,692 ordered pairs of all connected graphs with `<= 7`
vertices, `c` grows by 1, `d` becomes `min(d, 2)` and the set of cut paths is unchanged (`results-validate.txt`):
**0 failures**.

## 6. Random instances with 9-16 vertices (tasks 2 and 5)

`search.py 240 32 gnp,ears,planted,family search` -> `results-search.txt` (32 workers x 240 s, seeds 1000-1031).
Generators: `gnp` (G(n,p)), `ears` (random core plus 1- or 2-vertex ears), `planted` (a planted alternating path of
length 3, 5 or 7 with dense sides and sparse crossing edges), `family` (random relatives of `F(k)`: planted path,
`u` joined to some even path vertices, `v` to some odd ones, the other vertices ears on random vertices, random
edges inside the parity classes). For every pair with `d = 2`, `c >= 3`: exact answer (closure search), candidate
(O3 by set-to-set flow), O1.

Totals over the four generators (graphs | pairs with `d = 2`, `c >= 3` | pairs with `cp = c` | pairs whose shortest
cut path has length `>= 5` (= pairs where the candidate O3 is wrong) | pairs with some cut path of length `>= 5`;
the per-generator table is in `results-search.txt`):

| n | DC graphs | DC pairs | cp = c | O3 wrong | some >= 5 | non-DC graphs | non-DC pairs | cp = c | O3 wrong |
|---|---|---|---|---|---|---|---|---|---|
| 9 | 35,423 | 205,572 | 3,240 | 0 | 0 | 5,930 | 59,923 | 1,272 | 0 |
| 10 | 29,233 | 246,477 | 2,567 | 24 | 29 | 12,358 | 162,180 | 2,121 | 37 |
| 11 | 23,545 | 251,168 | 2,429 | 78 | 88 | 17,930 | 290,989 | 3,200 | 115 |
| 12 | 18,733 | 263,540 | 2,211 | 124 | 141 | 23,294 | 463,887 | 3,654 | 251 |
| 13 | 14,272 | 241,649 | 2,120 | 160 | 199 | 27,715 | 652,636 | 4,563 | 355 |
| 14 | 10,928 | 225,926 | 2,080 | 238 | 278 | 31,062 | 853,742 | 5,276 | 486 |
| 15 | 8,503 | 224,224 | 1,971 | 262 | 312 | 33,533 | 1,073,869 | 6,440 | 750 |
| 16 | 6,865 | 231,485 | 1,705 | 258 | 347 | 35,676 | 1,310,728 | 7,449 | 982 |
| all | 147,502 | 1,890,041 | 18,323 | 1,144 | 1,394 | 187,498 | 4,867,954 | 33,975 | 2,976 |

- The candidate (O3) never answers `cp = c` wrongly (it only finds real paths); it misses the answer `cp = c` in
  1,144 of the 18,323 positive DC pairs (6.2 %), almost all from the generators `family` and `planted`. Plain
  `G(n,p)` and random core-plus-ears graphs in DC gave 1 miss in 2,333 positive pairs (`ears`, n = 11).
- Pairs with both a length-3 and a longer cut path exist in DC (the strong form fails while the weak form holds),
  e.g. `n = 10`, `m = 19`, `u = 0`, `v = 5`:
  `0-1 0-2 0-4 0-7 0-8 1-2 1-3 1-5 2-3 2-4 3-4 3-5 3-6 3-9 4-5 4-7 4-8 5-6 5-9`: cut paths `0-2-4-5` and
  `0-1-2-3-4-5` (re-checked with `mcp.py` only, `results-verify-examples.txt`).
- O1: 0 failures on all these pairs, DC or not.
- An extra hypothesis "the even path vertices lie in `N[u]` and the odd ones in `N[v]`" fails already for
  length-3 paths in DC (examples at the end of `results-search.txt`); recorded only so that nobody retries it.

## 7. Minimum cuts generated by few vertices (exploratory)

Motivation: a polynomial algorithm could try only the minimum cuts spanned by the residual closure of `u` and a
few vertices. For a pair let `gen_A` be the least `j` such that the closure of `u` and `j` vertices spans a minimum
cut containing a `u`-`v` path, and `gen_B` the same for the complement of the co-closure (vertices that reach
`v` or one of `j` vertices). After one maximum flow, `gen_A <= 1` is decided with `n` closures and a search in
each cut, `gen_A <= 2` with `n^2`.

- `test_generated_cuts.py 150 32` -> `results-generated-cuts.txt`: on all positive pairs (`d = 2`, `c >= 3`)
  of all graphs with `<= 8` vertices (400) and of 157,593 random positive pairs (9-16 vertices, 4,363 + 19 of
  them in DC with shortest length 5 or 7), `gen_A <= 2 or gen_B <= 1` held every time (the script tests the
  closures of two vertices only when both one-vertex tests fail); `gen_A <= 1 or gen_B <= 1` failed on 5 DC pairs (the smallest listed is isomorphic to `E10` with `u`, `v` marked).
- `generators.py` -> `results-generators.txt`: `E10` has `gen_A = gen_B = 2`. In `F(k)` with both cliques
  `gen_A = gen_B = 1`; with only the odd clique (still DC) `gen_A = k`, `gen_B = 1`; symmetric with only the even
  clique.
- `repaired_family.py` -> `results-repaired-family.txt`: **`G(k)`**, `F(k)` without cliques, repaired into DC by
  adding, for each violating pair `(a, b)` of path vertices (`a` even, `b` odd), three degree-2 vertices (ears
  `a-w-b`, `u-y-a`, `b-z-v`). For `k = 2..7` (`n = 10, 17, 30, 49, 74, 105`): in DC (`mcp.in_dc`), `d(u,v) = 2`,
  the planted path is the only cut path (length `2k + 1`), and **`gen_A = gen_B = k`**. `G(3)` (`n = 17`,
  `m = 31`, `c = 8`, `cp_brute = 8`), `u = 0`, `v = 7`, edges in `results-repaired-family.txt`; re-checked with
  `mcp.py` only (`results-verify-examples.txt`: 162 minimum cuts, the planted path is the only path inside them).
  `gen_A`, `gen_B` were computed through the cut paths (`generators.gen_numbers_fast`) and checked against the
  subset search for `G(2)`, `G(3)` and all 20 variants of `F(k)`, `k <= 5`, in `results-generators.txt`.
- Consequence (evidence, with the exact numbers above): no test that inspects the minimum cuts generated by a
  bounded number of vertices on one side decides `cp = c` in DC. Together with Section 3 this rules out the two
  natural bounded searches (bounded path length, bounded number of generators).

## 8. Files

`experiments/`: `cutpaths.py` (library), `validate.py`, `extend9.py`, `family.py`, `climb.py`, `search.py`,
`verify_examples.py`, `test_generated_cuts.py`, `generators.py`, `repaired_family.py`; results
`results-validate.txt`, `results-extend9.txt`, `results-family.txt`, `results-climb-*.txt`, `results-search.txt`,
`results-verify-examples.txt`, `results-generated-cuts.txt`, `results-generators.txt`,
`results-repaired-family.txt`; logs `*.log`. Run from `experiments/` with Python 3.13 (networkx only for the
graph lists and the isomorphism test); every script uses fixed seeds. Three test-run outputs of `search.py`
(`results-searchtest*.txt`, written while debugging the script) were removed again by this agent.
