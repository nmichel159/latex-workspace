# Adversarial verification, round 3 (agent verify-round3)

Status: complete, 2026-10-13 (all background runs finished; every result file ends with its violation count). Scripts and result files: `verify/round3/` (own code written from the definitions in
`theory-dc.md` and `dc-algorithm.md`; other agents' code is imported only in the cross-checks named as such).
Targets: (1) the unfinished Sections 8 and 9 of `verify/lth.md`; (2) `dc-algorithm.md` Proposition 6.1, the hub
counterexample `H(2,2)` to path consistency, Lemma G, Theorem F; (3) if time remains, Theorem A.
Verdict labels as in `verify/equivalence.md`: **holds**, **holds, repair given**, **gap**, **false**.

## 0. Verdicts

| Claim (dc-algorithm.md unless stated) | Verdict | Notes |
|---|---|---|
| Prop. 6.1, classes version (P2, no consistent zigzag) | holds | §2.1; own rebuild of `H(2,2)`: 625 down-sets, none connects `u`, `v` |
| Prop. 6.1, partial-order version | holds, repair given | one sentence of the proof is false ("`G_D` has no edge at a middle element"); conclusion right; repair in §2.1 |
| §6.3: PC leaves every relation of `H(2,2)` non-empty at `L = 19, 21`, refutes `L <= 17`; AC refutes `L <= 13` | holds | own PC; the PC network at `L = 19, 21` re-verified as a certificate (§2.2) |
| §6.4: graph form of `H(2,2)` (po): 417 vertices, 833 edges, simple, `d = 2`, `c = 160`, in DC, no `u`-`v` path in a minimum cut | holds | own realisation and graph-only checks (max flow, 3-edge-connected components, Gomory-Hu tree, prefix search with flows) (§2.3); the classes version realises too (430 vertices, `c = 152`) |
| §6.3 side claims: PC refutes `H(1,1)`, `H(1,2)`, `H(2,1)`, `H(1,3)`, `H(3,1)` and passes `H(2,3)`; Theorem F answers "no" on `H(2,2)`, `H(2,3)`, `H(3,3)` | holds | §2.4; also `H(3,2)`; the "two-sided order" variant was not rebuilt |
| Lemma G (PC non-empty at `L` ⇒ at `L + 2`) | holds | every step re-derived (needs strong PC, which is what is computed); the network `N'` of the proof certified on 1440 random PC closures; monotonicity on 3600 instances (§3) |
| §4: CSP(`L`) solvable iff a consistent zigzag of length `<= L` exists | holds | backtracking vs exact shortest zigzag, all odd `L <= 9`, 3600 instances (§3) |
| Theorem F (i), (ii), (iii), dual | holds | proof re-derived line by line (§4); own algorithm = two exact solvers on 35,400 instances with the hypothesis; claim (ii) on 1.65 million shortest paths |
| Theorem F, Remarks (1)-(3) | holds | the bound "two" needs the hypothesis: on `R_L` (P2, no witnesses) the smallest working bound is `floor(L/2)` (§4) |
| §6.5 minimality of `H(2,2)` | holds | only the deletion of `u b_β` keeps a PC false positive (§2.5) |
| Theorem A (FPT in `c`), Lemmas A1-A4 | holds | proof re-derived (§7); own implementation = brute force / exact references on 3000 graphs, every lemma checked on 1500 (§7) |
| Theorem A' (any chain decomposition) | holds | proof steps re-derived for general chains (§7); not implemented |
| lth.md §8 (other statements of dc-hardness.md) | completed here, §5 | Theorem 1 Remark (2), `R_L` and its forms, the `all4` completion obstruction, PC1 on broken rigid families (own code): all hold |
| lth.md §9 (computations) | completed here, §6 | all lth scripts run with new seeds: 0 violations; the `t = 2` test of Theorem H is vacuous on random instances |
| §4 D1 (9-element AC counterexample); §6.6 singleton PC refutes `H(2,2)` | holds | own code (§2.6) |
| Cross-check of own AC, PC, exact solver with `dc-algorithm/zz.py` | agree | 2000 instances, 0 mismatches (§2.6) |
| New: the mixed case of Theorem F (bottom or top witnesses per pair) contains 2CH + P2 | proved | §4; so this case is at least as hard as SW + P2, whose complexity is open |

No claim of `dc-algorithm.md` checked here is false. One proof sentence (Prop. 6.1, partial-order version) is false and
is repaired; the conclusion and the counterexample `H(2,2)` stand. What `verify/lth.md` left open (§8, §9) is done in
§5, §6: nothing new is false.

## 2. The hub counterexample `H(2,2)` (dc-algorithm.md §6)

Own code: `r3core.py` (ZZ axioms, P2, enumeration of down-sets, DFS over consistent zigzags, AC, strong PC,
Theorem F algorithm), `hub3.py` (`H(m, m')` rebuilt from the text of §6.1 only), `hub_check.py`, `pc_cert.py`,
`realise3.py`, `test_realise3.py`, `hub_more.py`.

### 2.1 Proposition 6.1

*Classes version — holds.* Every step re-derived: the only `R`-edges at `v = t_t` and at `b_t` are those listed; a middle
element outside `D` has cut edges to `b_β` and to `b_a` (entries) or `b_t` (exits) only; the top chain
`t_{n_0} .. t_{n_K}` is linked to the hub side only by `b_a t_a`; `u = b_s` has the single neighbour `t_{n_0}`. Hence
`u`, `v` are connected in `G_D` iff some `ξ_j ∉ D`, some `ε_i ∉ D`, and every gadget has a route in `D`, and the down-set
property blocks gadget `(i, j)`.

*Partial-order version — holds, repair given.* The first case of the proof says: "if some bottom `b != u` is outside `D`,
every middle element and every top is outside `D`, so `G_D` has no edge at a middle element". The second half is false:
`D = {u, b_β}` is a down-set (the bottoms other than `u` are pairwise incomparable), and the twelve edges `b_β x`
(`x` middle) cross it (checked). Replacement: in this case the component of `u` in `G_D` is
`{u, t_{n_0}} ∪ {bottoms outside D}`. Indeed `u` is joined in `G_D` to `t_{n_0}` and to the bottoms outside `D`;
`t_{n_0}` has no other cut edge (its other neighbours, routes of `g_1` and `v`, lie outside `D` with it); a bottom
`b ∉ D` has no other cut edge (all its neighbours other than `u` are middle elements or tops, outside `D`). So `v` is not
reached. The second case (some top `t != v` in `D`) and the third case are right as written.

*Checks* (`hub_check.py`, `hub22.txt`): both versions of `H(2,2)` satisfy the ZZ axioms, `q = 22`, `|R| = 35` and `43`,
P2; the number of down-sets with `u ∈ D ∌ v` is 625 and 663 (as stated); none connects `u` and `v`; the independent DFS
over consistent zigzags finds none.

### 2.2 PC on `H(2,2)` (§6.3) — holds

Own strong PC (relations for all ordered pairs of positions including the diagonal, greatest fixpoint of
`T_ij ← T_ij ∩ (T_ik ∘ T_kj)` over all `k`). Results, both versions (`hub22.txt`):

| `L` | 11 | 13 | 15 | 17 | 19 | 21 | 23 |
|---|---|---|---|---|---|---|---|
| AC | no | no | yes | yes | yes | yes | yes |
| PC | no | no | no | no | yes | yes | yes |

(An earlier version of my own PC took the union over `k` instead of the intersection and accepted everything; caught by
the comparison with AC at `L = 11` and fixed before any result was recorded.)
*Certificate* (`pc_cert.py`, `pc-cert-22.txt`): the PC closure is the largest path-consistent network inside the base
constraints, so a network that (1) lies inside the base constraints, (2) is path consistent, (3) has no empty relation,
proves "PC does not refute". The network returned at `L = 19` and `L = 21` was checked for (1) with explicit loops from
the definitions and for (2) by integer matrix products for every triple of positions: 0 violations, 0 empty relations,
both versions (7613 and 19629 kept pairs). Hence for the decision procedure of §4 (`L = 21` for `q = 22`) `H(2,2)` is a
PC false positive. Claim E stands.

### 2.3 Graph form (§6.4) — holds

`realise3.py` (`realise-22-po.txt`, `realise-22-po-gh.txt`): own construction of `G(Π)` (Theorem 13(b), `M = 1`) for the
partial-order version: 417 vertices, 833 edges, simple, `N = 160` strict pairs; on the graph alone: `d(u,v) = 2` (BFS),
`c(u,v) = 160` (Dinic max flow), DC holds (every pair inside a 3-edge-connected component of `networkx.k_edge_components`
has distance at most 2; 396 components; a Gomory-Hu tree gives the same pairs with `c >= 3`, 0 mismatches), and a
depth-first search over simple paths from `u`, which keeps a prefix only if its even-indexed vertices (with `u`) and its
odd-indexed vertices (with `v`) are separated by a cut of value `c` (max flow with super terminals), finds no `u`-`v`
path inside a minimum cut (4780 flow tests). So `cp(u,v) = c + 1 = 161`. This search uses no ZZ theory. The classes
version (`realise-22-classes.txt`, `M = 1` ears inside the two classes) gives 430 vertices, 851 edges, `d = 2`,
`c = N = 152`, DC, no path. Validation (`test_realise3.py 1 400`, `results-test-realise3.txt`): on 387 random P2
instances (124 yes) the graph checks give `c = N`, `d = 2`, DC, and the search answer equals the ZZ answer in all;
0 violations.

### 2.4 Other members of the family (`hub_more.py`, `hub-more.txt`)

All with P2 and no consistent zigzag (down-set enumeration: up to 532,471 down-sets for `H(3,3)`); PC at
`L` = largest odd `<= q`:

| Instance | `q` | PC (both versions) | Theorem F, classes version |
|---|---|---|---|
| `H(1,1)` | 11 | refutes | no |
| `H(1,2)`, `H(2,1)` | 15 | refutes | no |
| `H(1,3)`, `H(3,1)` | 19 | refutes | no |
| `H(2,2)` | 22 | passes (`L = 21`) | no |
| `H(2,3)`, `H(3,2)` | 29 | passes (`L = 29`) | no |
| `H(3,3)` | 39 | not run | no |

The classes versions satisfy the bottom-witness hypothesis of Theorem F (lower hub `b_β`), the partial-order versions do
not (Remark (1) of §7). AC passes every instance of the table at that `L`.

## 3. Lemma G and the CSP of §4 — holds

*Proof re-derived.* Positions `L+1`, `L+2` are copies of `L`. Base constraints of the `(L+2)`-CSP: position `L` (odd) and
`L+1` must share the head, `L+1` (even) and `L+2` the tail: the identity satisfies both and compatibility (`h <= t` is
impossible for an edge `t < h`); `L+2` inherits "head `= v`" from `L`; the constraint "head `= v`" at `L` is dropped,
so `N` on positions `1..L` stays inside the base constraints; pairs `(j, L+1)`, `(j, L+2)` with `j < L` need only
compatibility, which `R_{j,L}` has. Path consistency: a triple of positions maps to a triple of `N` with copies replaced
by `L`; the triples with two copies of `L` need a support of `a ∈ D_L` in `R_{L,k}`, which strong PC (diagonal relations
included) provides. The PC closure is the largest path-consistent network inside the base constraints (the propagation
never deletes a pair of a path-consistent subnetwork), so it contains `N'`.
The proof uses PC in the strong form (domains as diagonal relations, so that PC implies arc consistency); this is the
form computed by `dc-algorithm.md` and by my code. With PC on the binary relations only, the step "a value of `D_L` has a
support" is not available. No change of the statement is needed if "PC" is read as strong PC, which §4 does implicitly.

*Checks* (`testG.py main 4000 150 24 6`, `results-G-main.txt`): 3600 random instances (2733 with P2; `q <= 10`, ties
included), every odd `L <= q + 4`: (a) CSP(`L`) solvable (backtracking) iff the exact shortest consistent zigzag has
length `<= L`, all `L <= 9`: 0 mismatches; (b) PC ⇒ AC, and a solvable CSP is never refuted by AC or PC: 0 violations;
(c) PC non-empty at `L` ⇒ non-empty at `L + 2`: 0 violations; the network `N'` built from the PC closure at `L` was
checked with `pc_cert.certify` at `L + 2` (inside the base constraints, path consistent, no empty relation) in 1440 cases:
0 failures. On these instances PC was never a false positive; AC was, 12 times (pairs instance, `L`).

## 4. Theorem F (§7) — holds

*(i)* Elements equivalent to `u` or `v` are comparable with all elements; a bottom witness `w ~ u` of two middle elements
is below both, strictly (otherwise the middle element would be equivalent to `u`).
*(ii)* A peak of `Z'` lies outside `D`, an element `w ~ u` inside (`w <= u ∈ D`); for incomparable peaks `x_i`, `x_j`
with `j >= i + 4` the walk `x_0 .. x_i w x_j .. x_L` lies in `G_D` and has length `<= L - 2`. Peaks have odd positions,
so two distinct ones differ by at least 2, and three pairwise incomparable peaks would need pairwise differences exactly
2. The representatives of distinct minimal classes of the middle peaks are pairwise incomparable (if `a <= b`, both
minimal, then `a ~ b`).
*(iii)* `D` generated by the valleys of `Z` misses `v` and the peaks (consistency); every peak of `Z'` is `~ v` or a middle
peak (an element `~ u` lies in `D`), hence lies in `↑(A ∪ {v})`; `D ∩ ↑(A ∪ {v}) = ∅` because `D` is a down-set without
peaks and without `v`; so `Z' ⊆ G_{D_A}`. Soundness: `D_A` is a down-set not containing `v`; if `u ∉ D_A` then `D_A = ∅`
(every non-empty down-set contains the least element) and `G_∅` has no edge, so the search never returns a false "yes",
also for the sets `A` containing elements `~ u`, which the algorithm tries. A `u`-`v` path of `G_D` is a consistent zigzag.
*Dual.* Reversing the order and exchanging `u`, `v` maps zigzags to reversed zigzags (valleys and peaks exchange) and
keeps consistency; the down-set `Q - ↑'(A ∪ {u})` of the reversed order is the up-set `Q - ↓(A ∪ {u})`, whose complement
`↓(A ∪ {u})` is the down-set of the statement.
Nothing is missing; the running time `O(q^2 (q + |R|))` is right.

*Checks* (`testF.py`, own implementation `r3core.Inst.thmF`; `results-F-main.txt`, `results-F-big.txt`): families
`bottom`, `top` (1-3 elements `~ u`, 2-9 middle, 1-3 `~ v`), `bottie` (ties between middle elements, denser order),
`bottombig`, `topbig` (8-12 middle elements, sparse, some ties): 35,400 instances with the hypothesis (bottom resp. top
witnesses) and P2, 14,228 yes. In all: Theorem F algorithm = down-set enumeration = DFS over consistent zigzags (each DFS
witness re-checked); claim (ii) and `|A| <= 2` on every shortest `u`-`v` path of every connecting `G_D` (at most 200 per
`D`): 1,646,592 paths, 0 violations, `|A| = 2` attained. AC/PC (`L` = largest odd `<= q`) on 1920 no-instances with
`q <= 12`: AC wrong 6 times, PC never. A `mixed` family (witness kind chosen per pair, then P2 repair) had one of the two
hypotheses in 1071 of 1800 instances; on all 1800 the search with `|A| <= 2` (bottom or dual) happened to be right, so
random instances do not exercise the open mixed case.

*The bound "two" needs the hypothesis* (`rl_thmF.py`, `rl-thmF.txt`): on the rigid family `R_L` of dc-hardness.md
(2CH + P2 in ZZ form, own construction; neither bottom nor top witnesses for `L >= 3`) the smallest `k` for which the
search over sets of `k` peaks or of `k` valleys finds the (unique) solution is `floor(L/2)`, `L = 2..9`. So no bounded
version of Theorem F (iii) holds for general ZZ + P2; the mixed case of Remark (3) is genuinely different.

*Remarks (1)-(3)* — hold. (1) checked: the classes versions of `H(m, m')` have bottom witnesses, the partial-order
versions do not. (3): in the 2CH form, bottoms are equivalent to `u`, so bottom witnesses are exactly "every two
`E`-sides meet", and the middle peaks of a shortest zigzag are the switches used with their `E`-side; all switches are
incomparable, so at most two `E`-sides occur in a shortest sequence of picked sides. (Wording: "a shortest solution
uses at most two switches in `E`-mode" refers to the sequence of picked sides, not to the mode vector.)

*Observation on the mixed case (new, proved).* In the ZZ form of 2CH every P2 witness is a bottom `b_x ~ u` or a top
`t_x ~ v`, so every 2CH + P2 instance (= SW + P2) has, for every incomparable pair, a bottom witness or a top witness.
Hence the mixed case of Remark (3) is open already without middle witnesses: "every incomparable pair has a bottom or a
top witness" contains 2CH + P2. Checked on `R_L`, `L = 2..7`: every pair has a witness of one of the two kinds, both
kinds occur (`L = 7`: 9 pairs with only bottom, 12 with only top witnesses).

### 2.6 Cross-checks with the agent's code and further claims of §4, §6.6

Done after the own checks were finished (`crosscheck_dcalg.py 2 2000`, `results-crosscheck-dcalg.txt`; imports
`dc-algorithm/zz.py` read-only): on 2000 random instances (1544 with P2, ties included, 624 yes) at `L` = largest odd
`<= q`, own AC = `zz.ac_answer`, own PC = `zz.pc_answer` = `zz.pc_numpy`, own down-set enumeration = `zz.exact_dfs`:
0 mismatches.
*§4, D1 (AC does not decide ZZ + P2) — holds.* The 9-element switch instance rebuilt from the text (own code): P2, no
consistent zigzag, AC at `L = 9` passes, PC refutes.
*§6.6, singleton PC — holds for `H(2,2)`* (`spc.py`, `spc-22-*.txt`): starting from the PC closure at `L = 21`, the
first round of singleton PC empties the domain of position 4 in both versions (refuted in 2-3 s). With slack, classes
version, `L = 25` and `L = 31`: refuted in the first round (positions `1..7`, resp. `1..13`, forced to a single value,
the next domain empty); `H(2,3)` classes version at `L = 29`: refuted in the first round (`spc-22-classes-25.txt`,
`spc-22-classes-31.txt`, `spc-23-classes.txt`). The partial-order version of `H(2,3)` and `L = 41` were not run.
The simple-path CSP and the long-route variant of §6.6 were not rebuilt.

### 2.5 Minimality of `H(2,2)` (§6.5) — holds

`hub_minimal.py` (`hub-minimal.txt`): of the 20 element deletions and 43 (35) edge deletions of the partial-order (classes)
version, 33 in total destroy P2; none creates a zigzag; PC (`L` = largest odd `<= q`) still passes after exactly one
deletion, the edge `u b_β` of the partial-order version, as stated.

## 5. verify/lth.md §8 completed: other statements of dc-hardness.md

Sections 1-7 of `verify/lth.md` stand as written; this section and §6 below replace its unfinished §8 and §9.

**8.1 Theorem 1, Remark (2) (`deg(z) >= 4`) — holds.** With `z ∈ C = A ∩ B`, `z != u`: `C` is a minimum cut
(intersection of minimum cuts), so `c <= |δ(C - z)| = |δ(C)| - e(z, V - C) + e(z, C - z)` gives
`e(z, C - z) >= e(z, V - C) >= 2` (the edges `zx`, `zy`, as `x, y ∉ C`), hence `deg(z) >= 4`; the case `z ∉ A ∪ B` is
symmetric. Remark (1) is labeled sketch and was not checked.

**8.2 Family `R_L`, its interval form and the form with `t` in every flip side — holds, one wording point.** P2 (same
parity: `w_pq ∈ Fl_p ∩ Fl_q`; opposite parity: `z_pq ∈ Fl_p ∩ h_q`, same type) and uniqueness re-derived: if `r` is the
first flipped switch, the sides reachable from `s` are `h_1 .. h_{r-1}`, because `h_k` (`k < r`) meets only
`h_{k-1}`, `h_{k+1}` and the flip sides `Fl_p` with `p < k`, which are not picked; `t` lies in `h_L` only. Interval form:
edge `(r-1, r)` is covered only by `h_r` and the `Fl_p`, `p < r`. With `t` added to every flip side the same argument
holds (the flip sides reachable are still those with `p < r`, unpicked). Checked by the lth scripts run here
(`lth-runs/smoke.txt`, `lth-runs/rigidH.txt`): unique alternating solution and P2 for `L <= 8` (2CH and interval form)
and `L <= 6` (form with `t`); the Helly property holds for the interval form (`L <= 6`), fails for the 2CH form from
`L = 4` and for the form with `t` from `L = 5` (as `verify/lth.md` §6 says against Theorem H, Remark (2); §2 of
dc-hardness.md claims the Helly property only for the interval form, correctly).

**8.3 Section 3, the exact completion obstruction for `all4` — holds.** `lth/check_p2options.py` (own contraction to
2CH and own brute force; the SW encoding of the formula is taken read-only from `dc-algorithm/sw_sat.py`), run here
(`lth-runs/p2options.txt`): `all4` has 8 switches, answer "no", no P2; 6 switch pairs have neither a common bottom nor a
common top; exactly three of them admit no single addition that keeps the answer "no": `(x in C1, ¬y in C4)`,
`(y in C1, ¬x in C3)`, `(x in C2, ¬y in C4)` — the three pairs named in dc-hardness.md. The inference "hence no P2
completion" is right: every completion gives each of these pairs a shared node, i.e. contains one of the tried single
additions (an existing node added to the side where it is missing, or a new node shared by at least these two sides),
and adding nodes to sides can only connect more. `x-notx` has P2 already.

**8.4 Row PC1, AC and PC on broken rigid families — holds (for `L <= 6`), independent code.** `broken_rigid.py`
(`broken-rigid-2-5.txt`, `broken-rigid-6.txt`): `cut(L, k)` (node `y_k` deleted) and `tflip(L, k)` (`t` moved from `h_L`
into `Fl_k`), `k = 1..L-1`, converted to ZZ by my own conversion (two elements per node, one per switch; larger than the
conversion of dc-hardness.md, up to 50 elements for `L = 6`): all 30 instances with `L = 2..6` keep P2, all are
no-instances (2CH brute force over mode vectors = DFS over consistent zigzags), AC passes 24 of them, and my PC refutes
every one at `L_CSP` = largest odd `<= q`; by Lemma G this
implies refutation at every smaller odd `L_CSP`, in particular at the length used by dc-hardness.md. AC accepts those
whose relaxation (both sides of every switch) is "yes". (dc-hardness.md counts AC false positives with its own, smaller
conversion; AC depends on the conversion, PC refutes in both.) `L = 7, 8` were not run (my conversion gives 65 and 82
elements).

## 6. verify/lth.md §9 completed: computations

The scripts of `verify/lth/` were run unchanged from `verify/round3/lth-runs/` (so their output files land there), with
seeds different from any earlier run. All end with 0 violations.

| Script, arguments | Result file | What is compared | Instances | Violations |
|---|---|---|---|---|
| `smoke.py 8` | `lth-runs/smoke.txt` | `R_L`, 2CH and interval form: P2, unique alternating solution; Theorem T solves | `L = 2..8` | 0 |
| `test_zz.py 2 5000 400` | `lth-runs/zz.txt` | §1: 2CH → ZZ: preorder valid, ZZ answer = 2CH brute force, ZZ-P2 = 2CH-P2; graph of Theorem 13(b): `c = N`, `d = 2`, DC, path test = answer | 5000 (4131 P2, 3611 yes); 400 graphs (259 yes, up to 76 vertices) | 0 |
| `test_D.py 2 5000` | `lth-runs/D.txt` | §2: Lemma D with guarded connectors, all mode vectors; dead sides given `t`; control with unguarded connectors breaks the equivalence in 1420 of 4414 instances (hypothesis not vacuous) | 4256 (14,888 guarded connectors, 9296 dead sides) | 0 |
| `test_La.py 2 3000` | `lth-runs/La.txt` | §3: concentration lemma, count of concentrated sides on shortest sequences, window search = brute force | 2999 (1725 yes; 664 with a non-trivial window) | 0 |
| `test_Lb.py 2 4000` | `lth-runs/Lb.txt` | §4: the 3-SAT variant is equisatisfiable with the stated occurrence pattern; the TIC encoding has reach `<= 2` and is coverable iff satisfiable | 2131 formulas (1529 sat) | 0 |
| `test_T.py`, `test_T_exh.py` (run by verify-LTH) | `lth/results-T-main.txt`, `lth/results-T-exh-*.txt` | §5: Theorem T and the `t = 1` search vs brute force; exhaustive TIC + P2 for small `K`, `n` | 28,800 random; 450,081 exhaustive | 0 |
| `test_H.py main 9100 300 30 1 5` | `lth-runs/results-H-main.txt` | §6: Theorem H, `t = 1`: soundness (also without P2), certificates, completeness when the need is `<= 1` | 9000 (families rand, tree (Helly), sparse, hardrand, nop2) | 0 |
| `test_H2.py main 9500 100 10 5` | `lth-runs/results-H2-main.txt` | §6: Theorem H with `t = 2` on yes-instances missed by `t = 1` | 1000 (964 yes) | 0, but vacuous: the `t = 1` search missed no yes-instance, so `t = 2` was never needed |
| `rigid_H.py 6 6 10` | `lth-runs/rigidH.txt` | §6, Remark (2): Helly property of the three forms of `R_L`; `t = 1` search on `R_L` | `L <= 10` | — (see 8.2) |
| `check_p2options.py all4 x-notx` | `lth-runs/p2options.txt` | §8.3 above | 2 formulas | — |
| `crosscheck.py 2 2000 400` | `lth-runs/crosscheck.txt` | own Theorem T and `t = 1` search vs the scripts of agent DC-hardness (`tic_poly.poly_solve`, `helly2ch.helly_solve`) and brute force | 1671 TIC + P2, 339 2CH | 0 |

Remarks on the computations. (1) `rigid_H.py` part (b): the full `t = 1` search solves `R_L` for `L <= 6`; the search
restricted to guesses among the flip nodes solves `L <= 7` and fails for `L = 8, 9, 10`. A failure of the restricted
search does not imply a failure of the full one, so the computation illustrates, but does not check, the proved statement
"the `t`-search fails for `L > 8t`" (`verify/lth.md` §6); the form with `t` in every flip side is solved by the full
`t = 1` search for `L <= 8`. (2) In the random `test_H.py` families the `t = 1` search never missed a yes-instance
(column `miss_need_gt_t` = 0), so the regime "piercing number `> t`" is reached only by the structured `R_L`.

## 7. Theorem A (dc-algorithm.md §1) — holds

*Lemma A1 — holds.* Flow value `c = f(A → V-A) - f(V-A → A) <= |δ(A)| = c` forces one unit outwards on every cut edge
and nothing inwards; a chain cannot re-enter `A`. In a flow without cycles every flow-carrying edge lies on exactly one
chain, which the correctness step uses ("every edge of `δ(A)` lies on exactly one chain").
*Lemma A2 — holds.* The Helly characterisation (D1): if `h_e ∉ C(t_{e'})` and `h_{e'} ∉ C(t_e)`, the minimum side
`C(t_e) ∪ C(t_{e'})` cuts both edges (`h_e ∉ C(t_e)` by cuttability); conversely tails lie in `A` and heads outside
(Lemma A1). Monotonicity of `Bad1`, `Bad2` uses that `C(·)` is a down-set and that minimum sides meet chains in
prefixes; the case analysis for the componentwise maximum is complete.
*Lemma A3 — holds.* Re-derived; injectivity from simplicity of the chains.
*Lemma A4 — holds* (standard).
*Theorem A — holds.* Soundness: pairwise compatible cuttable edges lie in the cut of `⋃ C(t_e)` (Helly), and the
shared ends give a `u`-`v` walk of distinct edges inside it. Completeness: a path inside `δ(A)` alternates sides, its
edges lie on distinct chains at cuttable positions, consecutive edges share the head (odd `j`) or the tail (even `j`),
and every two of them lie in `δ(A)`, so `Good` holds. "`cp = c` iff PIMC" holds in every graph (a cut-path of size `c`
consists of a minimum cut containing the path). Counting: `Σ_{L odd} c!/(c-L)! <= e·c!`; AC-3 on `L <= c` variables
with domains `<= n` is `O(c^2 n^3)`. Nothing is missing.
*Theorem A' — holds (proof only).* For a chain `f_1 < f_2 < ...` of the order `e < e'` iff `h(e) <= t(e')`: `t(e) <= h(e)`
for every edge of a minimum cut (a minimum side containing `h` but not `t` would receive flow), so
`h(f_{s''}) <= t(f_s) <= h(f_s)` for `s'' < s`, which is what A2 needs; in A3, two edges of one chain with a common head
or tail would be comparable with `h(f) <= t(f)`, contradicting cuttability. Irreflexivity and transitivity of `<`
follow in the same way, and antichain = "in one minimum cut" is D1. Not implemented here.

*Checks* (`thmA.py`, `thmA_test.py main 7100 250 12 5`, `results-A-main.txt`), own implementation from the text: own
unit-capacity max flow, decomposition into chains with flow cycles cancelled (the flow is rebuilt from the chains),
closures `C(x)` from the residual digraph, depth-first search over chain sequences with arc consistency on every prefix,
largest values as the solution.
- `rand`: 1500 connected random graphs, 4-12 vertices, 30% with parallel edges, `u`, `v` at distance `>= 2` in 1362;
  reference: brute force over all vertex sets with `u ∈ A ∌ v` and `|δ(A)| = c`. Answers agree (142 yes). On every
  instance, checked against the list of all minimum cuts: Lemma A1 (prefix, one cut edge per chain, cut edges = chain
  edges), `C(x)` = the smallest minimum side containing `x` (and undefined exactly when no minimum side contains `x`),
  the characterisation of `Good` by "in a common minimum cut", closure of `Good` under max and min, strict monotonicity
  of the same-head and same-tail relations: 0 violations.
- `gpi`: 1500 graphs `G(Π)` of Theorem 13(b) (`M = 1`) of random P2 instances (`d = 2`, `c = N` up to 33, up to about
  100 vertices); references: down-set enumeration of the ZZ instance and the flow-pruned path search of `realise3.py`
  (which agree on all). Answers agree (588 yes; witness lengths 3: 515, 5: 68, 7: 4, 9: 1).
- Every "yes" witness: its edges lie in the cut of the union of the closures of their tails, of value `c`, and form a
  `u`-`v` walk; Lemma A4 (largest remaining values form a solution) held on every solved CSP. Largest search tree:
  23,753 prefixes (`c = 33`, a no-instance), far below `c!`.
0 violations in total.

## 8. Not checked, and pointers

- `dc-algorithm.md` Theorems B, C, H (the `K_4` control), the adversarial accounting of §5, the two-sided order and the
  long-route variant of §6.3/§6.6, the simple-path CSP, and the sketch "why the hub construction needs order relations"
  (labeled sketch there) were not re-checked.
- Singleton PC was run only on the hub family (§2.6); like the other stronger relaxations of §6.6 it has not been
  tested adversarially, so it is a candidate algorithm, not a verified one.
- For the author's main question (complexity of ZZ + P2): this round confirms the two structural facts the next step
  can rely on: PC is not an algorithm for ZZ + P2, not even on the polynomial class of Theorem F (the classes version of
  `H(2,2)` has a lower hub); and Theorem F's bound needs its hypothesis, while the mixed bottom/top-witness case already
  contains SW + P2.

## 9. Scripts and result files (`verify/round3/`)

| Script | What | Output |
|---|---|---|
| `r3core.py` | ZZ instances, P2, witnesses, down-sets, DFS, Theorem F algorithm, CSP, AC, strong PC, random generator | library |
| `hub3.py`, `hub_check.py`, `hub_more.py`, `hub_minimal.py` | hub family rebuilt; Prop. 6.1, §6.3, §6.5 | `hub22.txt`, `hub-more.txt`, `hub-minimal.txt` |
| `pc_cert.py` | certificate check of a PC closure | `pc-cert-22.txt` |
| `realise3.py`, `test_realise3.py` | graph `G(Π)`, `d`, `c`, DC, flow-pruned path search | `realise-22-po.txt`, `realise-22-po-gh.txt`, `realise-22-classes.txt`, `results-test-realise3.txt` |
| `testF.py` | Theorem F | `results-F-main.txt`, `results-F-big.txt` (logs `log-F-*.txt`) |
| `rl_thmF.py` | `R_L` in ZZ form; bounded-peak search | `rl-thmF.txt` |
| `testG.py` | Lemma G, CSP exactness | `results-G-main.txt` |
| `broken_rigid.py` | dc-hardness PC1 with own code | `broken-rigid-2-5.txt`, `broken-rigid-6.txt` |
| `thmA.py`, `thmA_test.py` | Theorem A | `results-A-main.txt` |
| `crosscheck_dcalg.py` | cross-check with `dc-algorithm/zz.py`; D1 instance | `results-crosscheck-dcalg.txt` |
| `spc.py` | singleton PC on the hub family | `spc-22-classes.txt`, `spc-22-po.txt`, `spc-22-classes-25.txt`, `spc-22-classes-31.txt`, `spc-23-classes.txt` |
| `lth-runs/` | output of the `verify/lth/` scripts run here | see §6 |

Live findings log: three bullets posted on 2026-10-13 (`H(2,2)` confirmed with the repair; Theorem F and Lemma G;
Theorem A and the mixed case containing SW + P2).
