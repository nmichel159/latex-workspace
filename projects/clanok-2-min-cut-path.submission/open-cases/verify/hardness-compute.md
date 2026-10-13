# Independent computational check of the NP-hardness reduction (agent "verify-hardness-compute", 2026-10-12)

Object of the check: `open-cases/theory-hardness.md`, Section 2 (construction 2.1, Lemmas 2.2-2.4, Theorem 2.5,
Corollary 2.6, Remarks), the numbers of Sections 2.3 and 6.4 that concern the reduction graphs, and the row
"`c(x,y) <= 3` for all pairs: `cp = c` polynomial" of the table in Section 5 (with Corollary 1.4 and Lemma 1.3).
Scripts and logs: `open-cases/verify/hardness-compute/` (file list in Section 7).

## 0. Verdict

| Claim (theory-hardness.md) | Result here |
|---|---|
| Construction 2.1: sizes `2M + L` vertices, `M(M-1) + (m+1) + 4L + sum_i (abs(O_i) - 1)` edges, simple graph, two neighbours of each occurrence vertex in each clique | holds on every formula tested |
| Lemma 2.2 / 2.3: `c(u,v) = c0`; the minimum cuts are exactly the `A_tau` (`2^(number of occurring variables)` of them); `abs(delta(A)) = c0 + s(A)` between `K_A` and `V - K_B` | holds on every formula tested, by three independent methods |
| Lemma 2.4: `u`, `v` connected in `H_tau` iff `tau` satisfies `phi` | holds for every assignment of every formula tested |
| Theorem 2.5: `d(u,v) = 2`, diameter exactly 3 (hence the class "`d <= 3` or `c <= 2`"); PATH-IN-MIN-CUT iff satisfiable | holds on every formula tested |
| Corollary 2.6 (a)-(c): `cp(u,v) = c` iff satisfiable, `cp = c + 1 = c + d - 1` iff unsatisfiable | holds wherever the definition-based `cp` search finished (all formulas except those listed in Section 3.3) |
| Corollary 2.6 (d): every path inside a minimum cut has odd length `>= 2m + 1`; example `(x1)(x1)` | holds; example reproduced exactly |
| Section 2.3: not in DC, not in "`d <= 2` or `c <= 3`" | holds (filler pairs: `d = 3`, `c = c0 >= 4`) |
| Section 6.4 numbers for `(x1)(x2)(not x3)(not x4)` and the 6-variable formula | reproduced (16 cuts, one with a path, `A_tau = down(o1) u down(o2)`, `k* = 2`; `k* = 3`) |
| **Remark (2) after Theorem 2.5: fillers of `K_A`, `K_B` at distance 3 "with `c = M - 1`"** | **false as stated: `c = c0 = M - 2`** (Section 4.1); harmless for every result |
| Section 5: `c(x,y) <= 3` for all pairs gives a polynomial decision of `cp = c` (paths of length 1 and 3, one max flow each) | see Section 5 |

## 1. Method and independence

- The construction was re-implemented from the text of Section 2.1 only (`vred.py`); the `hardness/` scripts were
  opened only after all my code was written and the main runs had started (Section 6 compares them).
- The text leaves the order of the vertices on a sync path open ("joined into a path"). My runs use the order of
  occurrence (`natural`), the reverse order, and seeded random orders.
- Exact routines (`vlib.py`, own code): unit-capacity max flow (pure-Python augmenting paths returning the flow, and
  scipy's Dinic for values); all minimum `u`-`v` cuts by three methods:
  (M1) closed sets of the residual digraph of one maximum flow (strong components, ideal enumeration);
  (M2) brute force over all vertex sets (numpy, `n <= 25`);
  (M3) naive branching vertex by vertex, keeping a node `(S, T)` iff `lambda(S, T) = c` (no residual graph used).
  For the reduction graphs also a certificate (R5 below) that needs no enumeration at all.
- `cp` computed from its definition, independently of every lemma of theory-hardness.md:
  `cp(u,v) = min over simple u-v paths P of (abs(P) + c_{G-P}(u,v))` (a cut-path is a path plus a cut of `G - P`).
  `f(P') = abs(P') + c_{G-P'}` never decreases when a prefix `P'` is extended and is always `>= c`, so `cp = c` iff a
  depth-first search that extends only prefixes with `f = c` reaches `v` (`cp_eq_c_bb`). The faster variant
  `cp_eq_c_bb2` additionally skips an edge that carries no flow in one maximum flow of `G - P'` (such an edge cannot
  lower `c_{G-P'}`); both variants return the same set of paths on all 39692 ordered pairs of the connected graphs
  with `<= 7` vertices. A third computation is an integer program (`vilp.py`, CBC): variables for a side
  assignment, a unit `u`-`v` flow and the chosen edge set; its optimum is `cp` (proof in the docstring).
- Satisfiability by brute force over all assignments.

## 2. Validation of the exact routines (`check_vlib.py`, `results-vlib.txt`)

All 995 connected graphs with 2-7 vertices (networkx atlas) and 300 random connected graphs with 8-9 vertices,
every ordered pair, 58876 pairs (30266 yes-pairs). Compared: `c` by four methods (Python flow, scipy, brute force,
networkx); the minimum cuts by M1, M2, M3; the answer "some minimum cut contains a `u`-`v` path" (M1 cuts and cut
graphs) against `cp_eq_c_bb`, `cp_paths == c` (all simple paths of length `<= c + d`), `cp_definition == c` (all edge
sets by size, graphs with `<= 12` edges) and `checks/mcp.py: cp_brute` (imported read-only). **0 failures.**

## 3. The reduction (`check_reduction.py`, `redcheck.py`)

### 3.1 Checks per formula

R0 sizes and structure; R1 `c(u,v) = c0` (two flow codes); R2 `d(u,v) = 2`; R3 diameter exactly 3;
R4 minimum cuts by M1 `==` `{A_tau}`; R5 certificate: `lambda({u},{v,x}) > c0` for every `x in K_A - u`,
`lambda({u,x},{v}) > c0` for every `x in K_B - v`, `lambda({u,o},{v,o'}) > c0` and `lambda({u,o'},{v,o}) > c0` for every
sync edge `oo'`, and `abs(delta(A_tau)) = c0` for every `tau` (together these prove that the minimum cuts are exactly
the `A_tau`); R6 M2 (`n <= 25`) or M3 (`n <= 70`) `==` `{A_tau}`; R7 answer (cut graphs of the M1 cuts) `==`
satisfiable; R7b for every `tau`: `H_tau` connects `u`, `v` iff `tau` satisfies `phi`; R8 `cp_eq_c_bb2` answer `==`
satisfiable, the found path is odd, of length `>= 2m + 1` and lies in some `delta(A_tau)`, and the explicit cut-path
`u h_m v` plus a minimum cut of the rest has size exactly `c0 + 1`; R9 shortest path inside a path-containing
minimum cut odd and `>= 2m + 1`; R10 `abs(delta(A)) = c0 + s(A)` for all `2^L` sets `K_A <= A <= V - K_B` (`L <= 12`);
R11 a filler pair has `d = 3` and `c >= 4` (not DC, not "`d <= 2` or `c <= 3`"), and its `c` equals `c0`.

### 3.2 Formula families and results

Families (`check_reduction.py`; one line per formula in `info-<F>.jsonl`; summary `results-reduction-<F>.txt`,
table below from `summarize.py` → `results-summary.txt`):

- F1: all 3-CNF formulas over `x1, x2, x3` (three literals per clause, repetitions allowed), `m = 1, 2, 3`, one per
  class under renaming of the variables; natural sync order.
- F1s: F1 with `m <= 2` in reverse and in seeded random sync order, and a seeded sample of 2000 formulas with `m = 3`
  in random order.
- F2: all CNF formulas with clauses of 1-3 literals over `x1, x2`, `m = 1, 2, 3`, at least one clause shorter than 3.
- F3: 400 seeded random 3-CNF formulas, 3-7 variables, `m = 4..30`, natural or random order. The first run stopped
  after 283 formulas (`info-F3.jsonl`); `resume_family.py` ran the other 117 with the same jobs and checks
  (`info-F3-rest.jsonl`, `run-F3-resume.log`).
- F4: 17 hand-picked formulas in all three orders: the full unsatisfiable 3-CNF on 3 variables (two clause orders),
  7 of its clauses, the examples of the text, variables with gaps in their indices, clauses with 5 and 7 literals,
  one-literal contradictions.

| Family | formulas | sat / unsat | sync orders | `n` | `abs(E)` | `c` | minimum cuts | R6 (brute / branch) | R8 finished | R10 (all `2^L` sets) | failing formulas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 30098 | 29838 / 260 | natural | 23-57 | 104-600 | 8-22 | 2-8 | 14 / 30084 | 30098 | 30098 | 0 |
| F1s | 3140 | 3115 / 25 | random, reverse | 23-57 | 104-600 | 8-22 | 2-8 | 28 / 3112 | 3140 | 3140 | 0 |
| F2 | 16044 | 13892 / 2152 | natural | 13-52 | 36-505 | 4-20 | 2-4 | 56 / 15988 | 16044 | 16044 | 0 |
| F3 | 400 | 360 / 40 | natural, random | 74-516 | 988-45631 | 29-211 | 8-128 | 0 / 0 | 351 | 21 | 0 |
| F4 | 51 | 30 / 21 | natural, random, reverse | 20-142 | 84-3548 | 7-57 | 2-128 | 9 / 30 | 51 | 39 | 0 |
| **total** | **49733** | 47235 / 2498 | | 13-516 | up to 45631 | 4-211 | | | 49684 | | **0** |

Every formula passed R0-R5, R7, R7b, R9, R11 and R8-f0 (the explicit cut-path of size `c0 + 1`); R6 and R10 ran where
the size allowed (columns), R8 wherever the search finished (Section 3.3). All of R0-R11 together: 0 failures on
49733 formulas. Cumulative CPU time: F1 431 s, F1s 51 s, F2 196 s, F4 12 s (wall clock, 30 processes), F3 72311 s
(sum of per-formula times).

Path lengths (R9, all satisfiable formulas): the shortest path inside a path-containing minimum cut has odd length
`>= 2m + 1` in all 47235 cases (for example `(m, length)`: `(1,3)` 59, `(2,5)` 1950, `(2,7)` 79, `(3,7)` 40179,
`(3,9)` 4596, up to `(30,71)`; full list in `results-summary.txt`). `results-examples.txt` (E4) checks every path
length, not only the shortest, on 2218 formulas: 0 violations of Corollary 2.6 (d).

### 3.3 Where the definition-based `cp` search did not finish

`cp_eq_c_bb2` ran with a budget of 20000 search nodes. It finished on 49684 of the 49733 formulas (all of F1, F1s,
F2, F4 and 351 of F3; the largest finished graph has 482 vertices, the largest finished unsatisfiable one 380 vertices
with `m = 22`; the most nodes used were 19524) and agreed with satisfiability every time. It did not finish on 49 F3
formulas, all with `m >= 12` (210-516 vertices, `c = 85..211`): 31 satisfiable, 18 unsatisfiable. Seeds (order `n` =
natural, `r` = random), from `results-summary.txt`:

- satisfiable (31): 376r, 370r, 174r, 38r, 172r, 392n, 336r, 167n, 54n, 79r, 173r, 201n, 235n, 319r, 331r, 39r, 96r,
  208r, 256n, 234n, 351n, 205n, 209r, 286r, 356n, 143n, 165n, 198r, 239r, 11n, 322n;
- unsatisfiable (18): 7r, 241n, 56r, 124n, 357r, 359n, 320n, 230n, 37n, 290n, 136n, 187n, 67r, 9n, 13r, 61n, 342r,
  284r.

What still holds for these 49 without the search:

- satisfiable: `cp = c0` is shown by an explicit object. R7b found a cut graph `H_tau` connecting `u` and `v`, R5
  verified `abs(delta(A_tau)) = c0`, and R1 verified `c = c0` by two flow codes; so `delta(A_tau)` is a cut-path of
  size `c`, and `cp >= c` holds in every graph (article 1, Lemma 2.3).
- unsatisfiable: `cp <= c0 + 1` by the explicit cut-path of R8-f0. The lower bound `cp >= c0 + 1` uses Lemma 1.1
  (a cut-path of size `c` is a minimum cut `delta(A)` containing a path, a three-line argument) together with R4/R5
  (the minimum cuts are exactly the `A_tau`, proved by the certificate) and R7 (no cut graph of a minimum cut connects
  `u` and `v`). Only this direction depends on a lemma of theory-hardness.md here; on the 22 unsatisfiable F3
  formulas and the 2458 unsatisfiable formulas of the other families, where the search finished, it was confirmed from the definition.

The ILP (Section 3.4) is a third computation of `cp` on the small graphs.

## 4. Mismatches

### 4.1 Remark (2) of Section 2.2 (minor, wording)

The remark says fillers of `K_A` and `K_B` "are at distance 3 with `c = M - 1`". The cut `delta(K_A)` separates them
and has `c0 = M - 2` edges, so `c <= M - 2`; computed: `c = c0 = M - 2` on every formula tested (R11). Smallest
instance: `phi = (x1) and (x1)`: `M = 9`, the fillers `8` (in `K_A`) and `17` (in `K_B`) have `d = 3` and `c = 7`, not
8. Nothing depends on it: `c0 >= 4` still puts the pair outside DC and outside "`d <= 2` or `c <= 3`".

### 4.2 Edge-count formula (nit)

`sum_i (abs(O_i) - 1)` must run over the variables that occur (a declared but absent variable would contribute `-1`).
Checked with that reading (`F4` contains formulas with gaps in the variable indices).

No other mismatch was found.

## 5. The class "`c(x,y) <= 3` for all pairs" (`check_c3.py`, `results-c3.txt`)

Claim: if `c(u,v) <= 3`, `cp(u,v) = c(u,v)` is decided by testing the `u`-`v` paths of length 1 and 3 with one max
flow each (`P` qualifies iff `lambda(even(P), odd(P)) = c`). This follows from Lemma 1.2 (iii) (a path inside a
minimum cut has odd length `<= c`) and Lemma 1.3 ((a) iff (b)); there are at most `deg(u) deg(v) <= n^2` paths of
length 3. The argument uses `c(u,v) <= 3` only for the pair `(u,v)` itself, so the restriction to the class is not
needed (as the row "`d <= 2` or `c <= 3`" of the same table already says for pairs with `c(u,v) <= 3`).

Run (`check_c3.py` → `results-c3.txt`, 238 s). Per pair three answers were compared: the truth (all minimum cuts by
residual closure, also by all vertex sets for `n <= 16`, and a search in each cut graph), the definition-based search
`cp_eq_c_bb2`, and the procedure of the claim (Corollary 1.4 with `k = c`). In addition Lemma 1.3, (a) iff (b) iff (c),
was tested on every `u`-`v` path of odd length `<= c`.

| Graphs | Pairs | Yes-pairs | Pairs with `d = 2` (yes) | Odd paths tested for Lemma 1.3 | Failures |
|---|---|---|---|---|---|
| class `c(x,y) <= 3` for all pairs: 390 atlas graphs (all connected graphs with `<= 7` vertices in the class, all ordered pairs), 300 random subcubic graphs with 8-22 vertices, 150 random graphs with 8-16 vertices grown edge by edge to maximality inside the class, 55 wheels, fans and wheels with chords (4-14 rim vertices); at most 60-80 sampled pairs per graph outside the atlas | 47738 | 14735 | 17285 (93) | 47808 | 0 |
| unrestricted `G(n,p)`, `n = 8..11`, `p = 0.25..0.5`, 200 graphs, 30 sampled pairs each (procedure with all odd lengths `<= c`; no pair exceeded the cap of 4000 paths) | 6000 | 2434 | 2629 (4) | 47830 | 0 |

The 93 yes-pairs with `d = 2` in the class are the only ones that need a path of length 3. The row is confirmed:
the decision of `cp = c` is polynomial for pairs with `c(u,v) <= 3`. (Not tested: the entry "Min Cut-Path: open" of
that row.) An earlier plan with denser unrestricted graphs (`n` up to 12, `p` up to 0.7) was dropped before the run
because one graph took more than 10 minutes.

## 6. Comparison with `hardness/` (after my implementation)

`compare_hardness.py` → `results-compare.txt` (the `hardness/` modules imported read-only, no bytecode written into
that folder).

| Check | Result |
|---|---|
| H1 the graphs: my `vred.build` (natural sync order) vs `hardness/reduction.build`: vertex count, `u`, `v`, edge set | identical on all 46159 formulas of F1, F2, F4 (natural) and all 399 formulas of `hardness/check_reduction.py` |
| H2 shortest path inside a minimum cut: my BFS value in `H_tau` vs `hardness/reduction.shortest_route` (a dynamic program over the formula) | equal on all 49733 records of my five families (47235 satisfiable; `None` for the unsatisfiable ones on both sides) |
| H3 my checks R0-R11 on the 399 formulas of `hardness/check_reduction.py` | 352 satisfiable, 47 unsatisfiable, up to 176 vertices; the definition-based search finished on all 399; 0 failing formulas |
| H4 the two libraries on 600 random connected `G(n,p)` (`n = 6..14`, `p = 0.2..0.5`), 7200 ordered pairs: `c`, the set of minimum cuts (`exact.min_cuts_pq` vs `vlib.min_cuts_residual`), the answer `cp = c` (`exact.cp_equals_c_paths` vs `vlib.cp_eq_c_bb2`) | 0 mismatches |

Differences of method and coverage:

- `hardness/check_reduction.py` covers 399 formulas over at most 6 variables, the natural sync order only, graphs up
  to 176 vertices; mine covers 3 to 7 variables, three sync orders and graphs up to 482 vertices, and adds the
  enumeration-free certificate R5, Lemma 2.3 on all `2^L` sets (R10), the explicit cut-path of size `c0 + 1` (R8-f0)
  and the fillers' `c` (R11).
- Its "definition-based" test (`exact.cp_equals_c_paths`) prunes with Lemma 1.2 (the path alternates and its edges
  carry flow in alternating directions), so it is not independent of the theory it checks. `vlib.cp_eq_c_bb2` uses
  only the definition, the monotonicity of `abs(P') + c_{G-P'}` along prefixes, and the fact that an edge without
  flow in a maximum flow of `G - P'` cannot lower `c_{G-P'}`.
- It tests membership in DC and in "`d <= 2` or `c <= 3`" by counting violating pairs and never computes `c` of the
  two fillers, which is why Remark (2) passed unnoticed there.
- The proof verifier (`verify/hardness-proof.md`, its E1) reports the same Remark (2) slip by hand (`c = M - 2`);
  the two reports agree on it.
- The numbers of `hardness/results-examples.txt` (E1: 20 vertices, 84 edges, `c = 7`, two minimum cuts, only length
  5; E2: 16 minimum cuts, one with a path, not single-generated) equal mine (`results-examples.txt`).

## 7. Files

All in `open-cases/verify/hardness-compute/`.

| File | Content |
|---|---|
| `vlib.py` | exact routines (flows, three minimum-cut enumerations, cut graphs, definition-based `cp`) |
| `vred.py` | the construction of Section 2.1 from the text; `A_tau`; satisfiability |
| `vilp.py` | `cp` as an integer program (CBC) |
| `check_vlib.py` → `results-vlib.txt`, `check_vlib.log` | validation of `vlib.py` (Section 2) |
| `redcheck.py`, `check_reduction.py` → `results-reduction-<F>.txt`, `info-<F>.jsonl`, `run-families.log` | checks R0-R11 per family (Section 3); `-run1` files: first run of F4 with the unfiltered search |
| `check_examples.py` → `results-examples.txt` | numbers stated in the text (Section 4.1, Section 6.4 examples, path lengths) |
| `check_ilp.py` → `results-ilp.txt` | third `cp` computation on reduction graphs |
| `check_c3.py` → `results-c3.txt` | Section 5 |
| `gurobi.log` | written by pulp when it probed the installed Gurobi (licence expired, not used); it holds the local licence id, so the author may want to remove it |
