# Round 5, agent r5-verify: adversarial review of the unreviewed round-4 statements

Status: complete for priorities 1-3, priority 4 partly (2026-10-19). Reviewer: agent r5-verify. Scripts and logs:
`verify/r5-review/` and `verify/r5-review/runs/`. All code was written from the definitions in the reports; no code of
other agents is imported (no cross-check script was needed). Labels: **holds**, **holds with repair**, **gap**,
**false**, **not checked**; computations with script, seed, sizes, counts, outcome.

**Overall verdict.** No statement under review is false and none has a gap. T3 (the hardness theorem the article may
cite) holds as written, including NP membership and the graph form; ten realised graphs (367 to 3,295 vertices) were
checked with own max-flow code. Theorem R, Corollary R', Theorem 5', the soundness of forced-exit propagation and of
HYB, Lemma Sub, Lemma Mon and Example MW2 hold. Two wording repairs (propagation: stop when the component of one
terminal contains the other; Theorem R: a fixing is a partial mode vector), and one strengthening (Theorem R (b): the
exception for free middle witnesses is vacuous, `I*` always satisfies P2). No counterexample to any statement was found
in about 33,000 random general instances (24,000 ZZ + P2, 9,000 abstract switch forms), all 16,384 tiny
abstract switch forms, 3,300 T3 formulas and ten realised T3 graphs.

## 1. Verdicts

| # | Statement | Verdict | Notes |
|---|---|---|---|
| 1a | r4-hard T3 (a): ZZ restricted to P3 is NP-complete (P3, pendant reduction, NP membership) | holds | §2 |
| 1b | r4-hard T3 (b): graph form, every pair `d <= 3` or `c <= 2`, `d(u,v) = 2`, `c(u,v) >= 3` | holds | §2; ten graphs, own flow |
| 2a | r4-general Theorem R (a) | holds with repair (wording) | §3.4: the fixing must be a partial mode vector |
| 2b | Theorem R (b) | holds | §3.4: the stated exception is vacuous; `I*` always has P2 |
| 2c | Theorem R (c) | holds | relies on r4-switch Theorem 10 (reviewed) |
| 2d | Corollary R' | holds | its second hypothesis is implied by the first |
| 2e | §9.1 ties version (2CH with classes + P2) | holds | §3.4 |
| 2f | §7.3 forced-exit propagation: every fixed mode is a mode of every solution | holds with repair (wording) | §3.3: stop when the other terminal is reached (the code does) |
| 2g | §7.3 pruning and Proposition HYB (never accepts a no-instance; polynomial for fixed parameters) | holds | §3.3 |
| 2h | §5.1 Theorem 5' (soundness with conflict families and declarations) | holds | §3.2; also for walks with repeated sides |
| 2i | §5.1 conversion to the general switch form; valid walks exist iff yes | holds | §3.1 |
| 3a | Lemma Sub | holds | §4; "every middle edge a witness edge" needs one-at-a-time subdivision |
| 3b | Lemma Mon | holds | §4 |
| 3c | Example MW2 | holds | §4 |
| 4a | Proposition X (i), (ii) | holds | §5.1; checked `L <= 8` |
| 4b | Proposition X (iii) | holds | §5.1; no smaller triple for `L <= 6` |
| 4c | Proposition X (iv) (GC certificate number) | not checked | |
| 4d | Theorem Y (i) | holds | §5.2; checked `k <= 5` |
| 4e | Theorem Y (ii) | holds | §5.2; partial computation `k = 3, 4, 5` |
| 4f | Theorem Y (iii) | holds | §5.2; bound attained, `k <= 5` |
| 4g | Theorem Y (iv) (GC) | not checked | |
| 4h | Proposition Y' | holds | §5.2; the proof gives the stronger condition `kd + ks + s < k` and `B < k`; rejection not re-computed |
| 4i | r4-hard Lemma 1.1 | holds | §6; wording: add the unit clauses `λ(u) = λ(v) = 1` |
| 4j | r4-hard Lemmas 2.1, 2.2, 2.3 | holds | §6 |
| 4k | r4-hard Proposition 2.4 | holds | §6 |
| 4l | r4-hard Lemma 4.1, Corollary 4.2 | holds | §6; 500 random completions of `φ_32` |
| 4m | r4-hard Lemma 4.3 (hub lemma) | holds | §6 |

## 2. r4-hard.md §6, Theorem T3

### 2.1 Line-by-line reading

*Base instance.* `I0` is the instance of `theory-dc.md` Theorem 13(c) (reviewed earlier: `verify/equivalence.md` §4,
holds). Its generating relations form an acyclic digraph (`c_j -> P_{j,k} -> T_i/F_i -> a_i`, `e_0 -> d, a_1`,
`c_1 -> a_{n+1}`, plus `u`, `v`), so the order has no ties. The `R`-graph is a series of parallel blocks
(`u d e_0 a_1 {T_1,F_1} a_2 .. a_{n+1} c_1 {P_{1,k}} c_2 .. c_{m+1} v`), every simple `u`-`v` path in it is a zigzag
of the stated form, and the only valley-above-peak pairs are the conflict relations `X_i >= P_{j,k}`. So `I0` has a
consistent zigzag iff the formula is satisfiable; re-checked by own code (§2.2).

*Pendants.* The new relations are `u < b_x < y` (`y ∈ Q0 - {u}`). Transitivity: a chain `z <= b_x <= y` has `z = u`
or `z = b_x`, and `u <= y`; a chain `b_x <= y <= z` has `z` old and `≠ u`, so `b_x <= z`. Antisymmetry: only `u` lies
below `b_x`, and `b_x <= u` fails. So the order is a partial order, `u` least, `v` greatest, and the order on `Q0` is
unchanged (a new relation between old elements would pass through a pendant, and `x <= b_x` forces `x = u`). The
edge `b_x x` joins `b_x < x` (`x ≠ u`); `{u, v}` is still not an `R`-edge.

*Same answer.* For a down-set `D` of `I` (`u ∈ D ∌ v`), `D ∩ Q0` is a down-set of `I0`. `G_D` is `G_{D ∩ Q0}` plus
the edges `b_x x` with `b_x ∈ D ∌ x`; a pendant has degree one in `R` and is not a terminal, so it is never an inner
vertex of a path and connectivity of `u`, `v` is unchanged. Conversely `D0 ∪ {all pendants}` is a down-set of `I`
for every admissible `D0` (pendants have only `u` below them). **Holds.**

*P3.* Incomparable old elements are neither `u` nor `v`, so both have pendants, and `b_x < y`. Two pendants:
`b_y < x`, and `x` is the `R`-neighbour of `b_x`. A pendant is comparable with every old element. **Holds.**
Remark: P3 gives distance `<= 3` in the realisation of *every* P3 instance (an `R`-neighbour `z` of `x` comparable
with `y` gives the edge `x z` and the edge or ear of the comparable pair `z, y`).

*NP membership.* A certificate is a `u`-`v` path `P`; Lemma 6 of `theory-dc.md` tests "some minimum cut contains `P`"
by one max-flow between the even and odd vertices of `P`; for ZZ a zigzag is tested directly. **Holds.**

*Graph form.* The cut formula of Theorem 13(b) needs no P2: per strictly comparable pair `a < b` (edge or ear `ab`,
ear `u a` if `a ≠ u`, ear `b v` if `b ≠ v`) the contribution is 1, 1, 1, 3 in the cases `a, b ∈ A`; `a ∈ A ∌ b`;
`a, b ∉ A`; `b ∈ A ∌ a`, with ear vertices on their optimal sides. So the minimum cuts restrict to the down-sets and
`c = N`. A `u`-`v` path inside a minimum cut has no inner vertex of degree 2 (theory-dc Lemma 2 with `X = {w}`), so it
consists of real edges between elements and is a path of `G_D` for `D = A ∩ Q`; conversely a path of `G_D` lies in the
minimum cut of `D`. No ties occur, so no `M`-ears are needed. Distances: comparable elements `<= 2`; incomparable old
`x, y` via `x b_x` and the edge or ear of `b_x < y` (`<= 3`); two pendants `b_x, b_y` via the edge or ear of `b_x < y`
and the edge `y b_y` (`<= 3`); a pair containing an ear vertex has `c <= 2` (degree 2). `d(u,v) = 2` (ear `uv`, no
edge). The reduction is polynomial (`N = O(|Q|^2)`, at most three ears per pair). **Holds.**

No step needs repair. The graph form is about the class "`d <= 3` or `c <= 2` for every pair", not about DC; the
realised graphs are outside DC (§2.2, item 7), as they must be (P2 fails, `verify/equivalence.md` Fact 1).

### 2.2 Computations (own code: `zzlib.py`, `t3lib.py`, `graphlib.py`)

*ZZ level* (`t3_zz.py SEED COUNT MAXVARS MAXCLAUSES`; random CNF, 1-3 literals per clause): for every formula the
axioms of `I0` and `I` (preorder, `u` least, `v` greatest, strict real edges, `uv ∉ R`), no ties, the order on `Q0`
unchanged, every pendant comparable with every old element and with only `u` below it, P3 by brute force; answer by
truth tables, by the exact closure search `zz_search` (states: current element, down-closure of the valleys, up-closure
of the peaks) on `I` and on `I0`, and by enumeration of all down-sets of `I0` when `|Q0| <= 26`; every zigzag found in
`I` avoids the pendants.

| seed | formulas | vars / clauses | sat / unsat | with down-set enumeration | P3 failures | mismatches |
|---|---|---|---|---|---|---|
| 2 | 2000 | `<= 3` / `<= 6` | 1428 / 572 | 1447 | 0 | 0 |
| 3 | 1000 | `<= 4` / `<= 10` | 574 / 426 | 398 | 0 | 0 |
| 4 | 300 | `<= 6` / `<= 20` | 100 / 200 | 48 | 0 | 0 |

P2 fails on all 3,300 instances (expected). Logs `runs/t3zz-{2,3,4}.txt`.

*Graph level* (`t3_graph.py 1`, log `runs/t3graph-1.txt`): ten formulas (the four of r4-hard and six new ones, four
unsatisfiable), `I` realised by own code. Checks: (1) every non-element vertex has degree 2; (2) all element pairs at
distance `<= 3` (BFS), `d(u,v) = 2`; (3) `c(u,v) = N` (own Dinic); (4) minimum cuts = down-sets: for every element `y`
the residual closure of `{u, y}` meets the elements exactly in `{u} ∪ ↓y` and misses `v`; (5) the cut formula on 300
random element sets per graph, counted directly from the edge list; (6) the answer by an exact order-free search for a
walk inside one minimum cut (state: residual closure of the even vertices and co-closure of the odd vertices of one
maximum flow, with dominance pruning; exact because the closed sets containing `u` and missing `v` are exactly the
minimum cuts), compared with satisfiability, and every found walk re-checked by a fresh max-flow between its even and
odd vertices; (7) some element pair at distance 3 with `c >= 3` (the graph is not in DC).

| formula | vertices | `N = c(u,v)` | max element distance | `d(u,v)` | (4) | (5) | PIMC | SAT |
|---|---|---|---|---|---|---|---|---|
| `(x1)` | 367 | 135 | 3 | 2 | yes | yes | yes | yes |
| `(x1)(¬x1)` | 530 | 192 | 3 | 2 | yes | yes | no | no |
| `(x1 ∨ x2)` | 700 | 252 | 3 | 2 | yes | yes | yes | yes |
| `(x1)(¬x1 ∨ x2)` | 914 | 326 | 3 | 2 | yes | yes | yes | yes |
| `(x1 ∨ x2)(¬x1)(¬x2)` | 1149 | 407 | 3 | 2 | yes | yes | no | no |
| `(x1 ∨ ¬x2)(¬x1 ∨ x2)(x1 ∨ x2)` | 1421 | 501 | 3 | 2 | yes | yes | yes | yes |
| all four 2-clauses on `x1, x2` | 1861 | 652 | 3 | 2 | yes | yes | no | no |
| `(x1 ∨ x2 ∨ x3)(¬x1 ∨ ¬x2)(¬x3)` | 1834 | 643 | 3 | 2 | yes | yes | yes | yes |
| `(x1 ∨ ¬x2)(x2 ∨ ¬x3)(x3 ∨ ¬x1)(x1 ∨ x2 ∨ x3)` | 2518 | 877 | 3 | 2 | yes | yes | yes | yes |
| the same plus `(¬x1 ∨ ¬x2 ∨ ¬x3)` | 3295 | 1142 | 3 | 2 | yes | yes | no | no |

Every found walk uses element vertices only and has max-flow `c` between its even and odd vertices; the vertex counts
of the four formulas of r4-hard agree with its §6; in every graph some element pair at distance 3 has `c >= 3` (e.g.
`b_c1, b_P1_1` with `c = 22` for `(x1)`).

**Verdict T3: holds**, both parts.

## 3. r4-general.md §8, §7.3, §5.1 (priority 2)

Test bed (`test_general.py MODE SEED COUNT`, own generators in `gswlib.py`): mode `zz`, seeds 1-6, and mode `zzs`
(sparse orders, many ties), seeds 7-8, 3,000 instances each (24,000; 15,128 yes, 8,872 no): random ZZ + P2 instances
with 4-11 middle elements, random preorders with ties and one-way relations, random real edges (middle-middle
included), P2 repaired by existing or new bottom/top witnesses or by middle witnesses; mode `abs`, seeds 1-3, 3,000 each (9,000; 7,235 yes, 1,765 no): abstract switch forms with 3-9
switches, any hypergraph, any preorder on the switches, no P2. Exact answers by brute force over all order-consistent
mode vectors. Logs `runs/general-*.txt`; totals by `aggregate.py`. Exhaustive tiny instances: `exhaustive_small.py`
(all 16,384 abstract forms with 3 nodes, 2 switches and every preorder; 4,000 sampled with 3 nodes / 3 switches and
4,000 with 4 nodes / 3 switches; logs `runs/exh-*.txt`).

### 3.1 The general switch form and valid walks (§5.1)

*Reading.* Nodes are the components of the `B`-`T` edges plus one private node per edge between middle elements. For
`w ∈ D` (middle) the edges of `G_D` at `w` go to tops and to middle `x > w` with `x ∉ D` (lower neighbours lie in
`D`); the private node of `w x` lies in `F_w ∩ E_x` and is picked by both exactly when `w ∈ D ∌ x`. Dually for
`w ∉ D`. `B`-`T` edges are in every `G_D`, `B`-`B` and `T`-`T` edges in none, ties carry no edge. So `u`, `v` are
connected in `G_D` iff `s`, `t` are connected in the hypergraph of the sides picked by `D`. A walk without a conflict
pair certifies the vector "F exactly on the down-closure of its F-members" (its E-members lie outside that set, else a
conflict pair); conversely a shortest sequence of picked sides of a solution has no conflict pair. **Holds.**
*Checked:* switch-form answer = brute force over all down-sets of the ZZ instance = `zz_search`, on all 24,000 ZZ
instances; "valid walk exists iff yes" (exhaustive search with `K` = all sides, no declarations) on all 33,000
instances; every found walk certifies an order-consistent connecting vector. 0 mismatches.

### 3.2 Theorem 5'

*Re-derivation.* `Π` is symmetric on conflict pairs. Let `X` be first used at time `i` and `Y ∈ Π(X)` first used at
`j > i`. At time `i`, `Y ∈ K`, or `Y ∈ Dc`, or `X` declares `Y`; `Dc` only grows and appending `Y` needs `Y ∉ Dc`, so
`Y ∈ K`. Hence (*) every conflict partner of `X` first used after `X` lies in `K`, and members of `K` never declare.
At time `j`: if `X ∈ K`, `X ∈ St` and `Y` is refused; if `X ∉ K ∪ Dc`, `Y` would have to declare `X`, which a member
of `K` cannot; if `X ∉ K` but `X ∈ Dc`, then `X` was declared after time `i` (it was appended at `i`) by some `Z` with
`X ∈ Π(Z)`; `Z` was first used after `i` (a first use before `i` would have put `X` into `K ∪ Dc` before time `i`), so
`Z ∈ K` by (*) and cannot declare: contradiction. Sides may repeat in a walk; only first uses and the monotonicity of
`St`, `Dc` enter. **Holds.** The completeness remark also holds (a member of a valid path is never in `Dc` and never in
conflict with `St`).
*Checked* (own `SW.search5`, transitions to meeting sides): 144,000 runs with random `K`, `B ∈ 0..6`, `s ∈ 0..3` on the
ZZ instances and 54,000 on the abstract ones (70,797 + 34,650 acceptances): every accepted walk valid, every
acceptance on a yes-instance. All walks of length `<= 7` allowed step by step by the rules, without state merging, on
every instance with at most 10 sides: 157.1 million rule walks reaching `t`, all valid. Exhaustive: every `K`, `B ∈ 0..3`,
`s ∈ 0..2` on the 16,384 tiny instances (2,430,000 searches, 1,223,456 accepting) and on the 8,000 sampled 3-switch
instances (4,636,584 searches): 0 unsound.

### 3.3 §7.3: forced-exit propagation, pruning, HYB

*Re-derivation.* Let `σ` be a solution extending the partial assignment `α` (then `σ` extends the order closure of
`α`). Let `C` be the component of `s` in the hypergraph of the sides fixed by `α`, `t ∉ C`. The `σ`-picked sides join
`s` to `t`, so one of them meets `C` and has a node outside `C`; it is not a fixed side (a fixed side meeting `C` lies
in `C`), so it is a side of an unfixed switch that meets `C` and leaves it. So "no exit" refutes correctly and a unique
exit is picked by every such `σ`; fixing it (and closing) keeps all solutions extending `α`. A closure contradiction
is a correct refutation. **Repair (wording):** the text says "grow the component of `s`; if no side of an unfixed
switch meets `C` and leaves it, refute", which read literally also refutes when `t ∈ C` and no exit remains (for
example when every switch is fixed and the fixed sides connect); the rule must stop without refuting as soon as the
component contains the other terminal. The code (`gsw.refutes`: `if (C >> goal) & 1: break`) and the own code do so.
Pruning: if `α ∪ {w: m}` is refuted, every solution extending `α` has the other mode; by induction every fixed mode is
a mode of every solution, so no removed side is used by a solution; if both modes of a switch are refuted there is no
solution (the code returns "no solution at all").
HYB: a walk accepted on the pruned instance is valid there (Theorem 5') and hence valid in the original (same order,
fewer sides), so HYB never accepts a no-instance, for every parameter and every pruning. Time: for fixed
`(kd, ks, s, B)` there are `D^{O(kd + ks)}` sets `K`; a state is (side, `St`, `Dc`, count) with `|St| <= B` and
`Dc = (∪ Π(Y_i)) - K` determined by the at most `s` declaring sides, so `O(D^{1 + B + s})` states; pruning is at most
`m` rounds of `2m` propagations. **Proposition HYB holds.**
*Checked* (own `SW.refutes`, `SW.prune`): on all 33,000 instances every fixed mode agrees with every solution; the
pruned instance (dead sides deleted) has the original answer; searches of Theorem 5' on the pruned instances (random
`K`) accepted 42,088 + 19,547 times, always on yes-instances and with walks valid in the original; exhaustively sound
on the tiny instances. Observations (not claims of r4-general): pruning refuted 8,821 of the 8,872 ZZ no-instances (it
is not a complete refutation procedure) and all 1,765 abstract no-instances; it reached exactly the maximal sound
fixing (the modes common to all solutions) on 1,212 of 1,213 abstract and 706 of 718 ZZ yes-instances
(`prune_vs_max.py 5 1500`, `runs/prune-vs-max-5.txt`); 557 of the 15,128 ZZ yes-instances and 200 of the 7,235
abstract ones are rigid.

### 3.4 Theorem R (a)-(c), Corollary R', §9.1

*Re-derivation.* (a) Let the fixing be closed under the order and give at most one mode per switch. A relation between
a free `x` and a fixed `y` forbids only (`x <= y`) `y` F with `x` E, or (`y <= x`) `x` F with `y` E; in the forbidden
cases closure would have fixed `x`; a tie between free and fixed is excluded likewise. Free switches are pairwise
incomparable, so every vector of the free switches extends the fixing to an order-consistent vector, whose picked
hypergraph is (fixed picked sides) ∪ (free picked sides); contracting each fixed picked side (overlaps merge
transitively) preserves `s`-`t` connectivity for every free vector. Hence `I*` yes ⇒ `I` yes needs **no** soundness,
and `I` yes ⇒ `I*` yes because every solution satisfies the sound fixing. **Holds with a wording repair:** "a set of
pairs (switch, mode) that every solution satisfies" is vacuous on a no-instance and may then contain both modes of a
switch, for which the contraction is undefined; the fixing must be a partial mode vector (automatic on yes-instances;
pruning that refutes both modes answers "no", as the code does).
(b) A bottom (top) witness of two free switches is a common node of their E-sides (F-sides). A middle witness `w` of
free `x, y` is strictly comparable with both, so **under the hypothesis of the theorem it is never free**; it is not
fixed E (closure would fix `x`, `y`), so it is fixed F, and `F_w`, which contains the private nodes of `w x` and `w y`,
is contracted into one node of `E*_x ∩ E*_y`; dually above. **Holds; the exception "unless some pair of free switches
has only free middle witnesses" is vacuous: under the hypothesis `I*` always satisfies P2.** Sides of `I*` may be
empty or meet their partner, and `s = t` may occur; r4-switch §1 admits all of this (empty sets are not sides,
`s = t` is a yes-instance; `verify/r4-switch-review.md` §2.1).
(c) Theorem 10 of r4-switch (reviewed: holds) decides `I*`; contraction and pruning are polynomial. **Holds.**
*Corollary R'* **holds**; its second hypothesis ("every pair of free elements with a common node or a fixed witness")
follows from the first. *§9.1 (ties only among the free switches):* the same proof gives an instance of 2CH with
classes (the classes stay classes); a middle witness of free switches of different classes is strictly comparable with
them, hence fixed F as above, so P2 holds between different classes. **Holds.**
*Checked* (own `SW.contract`; `I` and `I*` by brute force):

| fixing | ZZ + P2 (seeds 1-8): hypothesis holds | abstract (seeds 1-3) | answer mismatches | P2 failures in `I*` |
|---|---|---|---|---|
| own pruning | 3,630 | 1,596 | 0 | 0 |
| maximal sound fixing | 3,634 | 1,596 | 0 | 0 |
| random closed sub-fixings of the maximal one | 9,329 | 4,089 | 0 | 0 |
| no-instances, random closed partial vectors | 13,858 | 3,210 | 0 | 0 |
| §9.1, ties only among free switches, all fixings (ZZ seeds 5-8, abstract seed 3) | 4,393 | 597 | 0 | 0 (different classes) |

and on the tiny instances 18,516 + 5,220 contractions, 0 mismatches. P2 of `I*` is tested on the ZZ + P2 runs only.

## 4. r4-general.md §3 (priority 3)

**Lemma Sub — holds.** `b_e ~ u` lies in every admissible down-set and `t_e ~ v` in none, so `D ↦ D ∪ {b_e}` is a
bijection; `b_e t_e` is always present, `y t_e` iff `y ∈ D`, `b_e x` iff `x ∉ D`; if `y ∈ D ∌ x` the path
`y t_e b_e x` replaces `e`; otherwise (`y ∉ D`, hence `x ∉ D`; or `x ∈ D`, hence `y ∈ D`) the new elements form a
pendant path at `x` or at `y`. The new elements are comparable with everything and each has one old neighbour, so they
witness no pair; old witnesses survive unless they use `e`. The consequence "every middle edge may be assumed to be a
witness edge" holds when edges are subdivided one at a time and neededness is re-evaluated after each step (two edges
can each be dispensable while not both are). *Checked* (`test_small.py 1 300`, `runs/small-1.txt`): 300 random
ZZ + P2 instances, each of their 4,320 edges (643 between middle elements) subdivided: the down-sets of `I'` are exactly
the images, connectivity agrees for every single down-set, and "P2 in `I'`" agrees with the witness criterion in all
4,320 cases (P2 kept in 2,309). 0 failures.

**Lemma Mon — holds.** With the order on the old elements unchanged, `↓_{I'} D` meets them in `D`, misses `v` and
keeps every edge of `G_D`. The consequence presupposes that `I` is a no-instance and that the relaxed relation is a
preorder. *Checked:* 300 random instances, 1-3 new elements between `↓a` and `↑b` (`a <= b`; the old order re-verified
unchanged) and random new edges: all 2,204 solutions map to solutions.

**Example MW2 — holds.** Own brute force: 9 elements, axioms and P2 hold (incomparable pairs `{x, y}` with witness `w`
and `{y, a}` with witness `v`), no solution (re-done by hand by cases on `a ∈ D`, `x ∈ D`, `p ∈ D`); a new bottom
witness of `x, y` gives exactly one solution, `D = {u, z, z', b}` (path `u p z x b y z' v`); a new top witness exactly
one, `D = {u, z, z', p, w, x, y}` (path `u a x τ y v`). Without `a` (8 elements): no solution; bottom witness: one
solution; top witness: none, as stated.

## 5. r4-general.md §4, §6 (priority 4)

Own builders `families.py` (from the text of §4 and §6, in the general switch form; each node is a bottom-top pair in
the ZZ form of `ng_check.py`).

### 5.1 Proposition X

(i), (ii) **hold**: re-derived as written (first-flip argument: the component of `s` is `h_1 ∪ .. ∪ h_{r-1}`, which
misses `t`). *Checked* (`families.py 8 5`, `runs/families-8-5.txt`): `X_2 .. X_8`: P2 for every incomparable pair, exactly
one order-consistent connecting mode vector, equal to the stated one; the own propagation fixes every switch (rigid),
in agreement with the caveat of §7.3.
(iii) **holds**: every odd `x_k` lies outside `D*` and only bottoms lie below it, so `x_k ∈ Γ ∪ N^-(Π)`; upper
neighbours of odd `x_k` other than `v` (tops of `z_kq`, `n'_jk`) serve one odd switch each; with `v ∈ Π` every even
mate lies in `N^-(Π) ∩ D*` and must be below `Y ∪ {u}`, which needs an element of `{m_k, x_k}` per even `k` (a top in
`Y` empties `G`). *Checked* (`ng_check.py 6 5`, `runs/ng-6-5.txt`): exhaustive over all triples of total size `<=
⌊L/2⌋ - 1`, peak and valley side, `L = 2..6` (up to 110 elements): none succeeds.
(iv) **not checked** (the GC certificate definitions of `dc-general.md` were not re-implemented).

### 5.2 Theorem Y, Proposition Y'

(i) **holds**: P2 by the listed nodes; uniqueness by the first-flip argument. *Checked:* `Y_2 .. Y_5`, `Y'_2 .. Y'_5`:
P2, exactly one solution, equal to the stated one; rigid under the own propagation.
(ii) **holds**: under the unique solution the picked path sides form an induced path and the picked mate E-sides meet no
path side, so an accepted walk passes every `h_c`; `F(m_c)` can be declared only by `E(x_c) = h_c` or `E(m_c)`
(`Π(E_w) ∋ F(m_c)` iff `w <= m_c`, i.e. `w ∈ {x_c, m_c}`); a set `N_F[Z]` contains `F(m_c)` only for `Z = F(m_c)` or
`Z = Fl_b`; `N_F[Fl_b]` contains all `k` F-members (through `z_bq`), forcing `B >= k`. *Checked* (`y_search_check.py`,
own `search5`; `runs/ysearch-*.txt`): `K_E` = (at most one `N_F[Z]`) ∪ (at most one single F-side), `K_F` ∈ {∅, one or
two sets `N_E[Z]`} (`k = 3`) or {∅, one `N_E[Z]`} (`k = 4, 5`), `kd + ks + s = k - 1`, `B = k - 1`: 750, 798 and 1,288
certificate sets, none accepted; with `B = k` and one dominator some are accepted (4, 9, 11), as the sharpness remark
says. This covers a sub-family of "any `K_F`" only; the proof covers all.
(iii) **holds**: below an E-member lie only bottoms; its upper neighbours (tops of `z_cq`, `w_cb`, `f_bc`) are adjacent
to at most two E-members. *Checked* (`ng_check.py`): with the best possible `Y` (`Y = D*` on the peak side, the
complement of `D*` on the valley side; any other `Y` only removes useful generators), the least `|Γ| + |Π|` of a
successful triple is exactly `⌈k/2⌉` for `Y_2 .. Y_5` and `Y'_2 .. Y'_5`.
(iv) **not checked**.
Proposition Y' **holds**: as in (ii), with `F(m_c)` reachable from `h_{k+c}` unless deleted; a set `N_F[Z]` containing
`F(m_c)` has `Z ∈ {F(m_c), h_{k+c}} ∪ {Fl_b}`, the first two serve one `c` each, `N_F[Fl_b]` puts all `k` F-members
into `K`, hence into `S`. The proof shows rejection whenever `kd + ks + s < k` and `B < k`, which is weaker than the
stated hypothesis `kd + ks + s + B < k` (so the statement is true and can be strengthened). P2 and uniqueness of
`Y'_k` checked for `k <= 5`; the refined search itself was not re-implemented.

## 6. r4-hard.md Lemmas 1.1, 2.1-2.3, Proposition 2.4, Lemmas 4.1, 4.3, Corollary 4.2 (priority 4)

All re-derived line by line; all **hold**.
- Lemma 1.1: (a) `x < y` and the edge is in `G_D` iff `x ∈ D ∌ y`; (b) substitution of `λ` into "`b ∈ D ⇒ a ∈ D`";
  (c) main edges go up from `Vt`. Wording: "the order is exactly a set of 2-clauses" holds on the non-witness elements
  once the unit clauses `λ(u) = λ(v) = 1` (the terminal conditions) are added; witness elements are fixed.
- Lemma 2.1 (bottom `b ∈ D` always), the table (four combinations), Lemma 2.2 (main neighbours of a dead `Vt` element
  lie above it, outside `D`), Lemma 2.3 (bottoms and dead `Vt` elements form a set closed under adjacency in `G_D`;
  `u`, `v` are live), Proposition 2.4 (delete the witnesses by Lemma 2.3; down-sets of the reduced instance extend by
  the bottoms; then Proposition 14 of theory-dc).
- Lemma 4.1: if (E) fails, each `q_b` has at least two `p` with `E ∩ E = ∅`, hence `F ∩ F ≠ ∅`: at least 6 such pairs;
  if (F) fails, at most 3. Corollary 4.2: positions 1st, 15th, 29th of the sorted E-occurrence positions are pairwise
  `>= 14` apart (`k >= 29`), the F-occurrences of three further variables likewise (`k - 3 >= 29`); at most 12 special
  clauses, at least 13 clauses strictly between `π_a` and `π_c`; every fresh variable occurs once, so the assignment
  is well defined and falsifies exactly `K`.
- Lemma 4.3: if every `b` has at most `⌈n/2⌉ - 1` L-pairs, some `a` has at least `⌊n/2⌋ + 1 >= ⌈n/2⌉` U-pairs.
*Checked* (`r4hard_lemmas.py 1 400`, `runs/r4hard-lemmas-1.txt`): 400 random typed instances (70% with harmless
witnesses), all 8,311 down-sets: Lemma 1.1 (a), (b), Lemma 2.1, Lemma 2.2, Lemma 2.3 (no live element in a witness
component; `u`-`v` connectivity equals connectivity by live main edges), 0 failures; Proposition 2.4 (Proposition 14
algorithm against brute force) on the 85 instances with all `Vt`-`Pt` pairs comparable, 0 mismatches; Lemma 4.3 on
6,311 random incomparable blocks (`n = 1..3`) of random ZZ + P2 instances, 0 failures. Corollary 4.2
(`o1_check.py`, own setting-S instances for `φ_32`, random clause order, random E-literals, random P2 completions with
random reuse of witness nodes and E/F bias 0.05, 0.5 or 0.95; P2 and "dead sides hold witness nodes only" asserted):
seed 1, 200 instances (194 case (E), 6 case (F)); seed 2, 300 instances (199 (E), 101 (F)); the proof's construction
succeeded in all 500: the assignment falsifies exactly the clause `K` and connects `s`, `t`.

## 7. Not checked

- Proposition X (iv) and Theorem Y (iv) (certificate number of Theorem GC).
- The rejection claims of Proposition Y' by computation (the proof was re-derived).
- Theorem Y (ii) for all `K_F` by computation (only a sub-family; the proof was re-derived).
- The family claims of Corollary R' for `T_L^tie`, `T_L^one`, the ladders, `R_L` with mates and the 133 `r4-search`
  instances (only `X_L`, `Y_k`, `Y'_k` were rebuilt; they are rigid under the own propagation).
- r4-hard §3 (C1), §4.4, §5, §7 (sketches or not in the list).

## 8. Files (`verify/r5-review/`)

| Script | What | Logs |
|---|---|---|
| `zzlib.py` | ZZ instances, axioms, P2, P3, exact closure search, down-set enumeration | |
| `t3lib.py`, `t3_zz.py`, `t3_graph.py` | T3: construction, ZZ-level checks, graph realisation and flow checks | `runs/t3zz-*.txt`, `runs/t3graph-1.txt` |
| `graphlib.py` | realisation (Theorem 13(b)), BFS, Dinic, residual closures, order-free PIMC search | |
| `gswlib.py` | general switch form, propagation, pruning, contraction, search of Theorem 5', generators | |
| `test_general.py`, `aggregate.py`, `prune_vs_max.py` | §5.1, §7.3, §8, §9.1 on random instances | `runs/general-*.txt`, `runs/prune-vs-max-5.txt` |
| `exhaustive_small.py` | the same on all tiny instances | `runs/exh-*.txt` |
| `test_small.py` | Lemma Sub, Lemma Mon, MW2 | `runs/small-1.txt` |
| `families.py`, `ng_check.py`, `y_search_check.py` | `X_L`, `Y_k`, `Y'_k`; NG bounds; Theorem Y (ii) | `runs/families-8-5.txt`, `runs/ng-6-5.txt`, `runs/ysearch-*.txt` |
| `r4hard_lemmas.py`, `o1_check.py` | r4-hard Lemmas 1.1-2.3, Proposition 2.4, Lemma 4.3; Corollary 4.2 | `runs/r4hard-lemmas-1.txt`, `runs/o1-*.txt` |
