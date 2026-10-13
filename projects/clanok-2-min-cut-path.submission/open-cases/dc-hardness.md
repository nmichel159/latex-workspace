# Open case of DC: hardness attempts (agent "DC-hardness", 2026-10-12/13)

Status: working file, version 2 (resumed run; version 1 consisted of Sections 1 and 2, kept unchanged in substance).
Scripts: `dc-hardness/`. Every claim is labeled **proved**, **checked** (exact computation on the instances named),
**sketch** or **conjecture**. Notation as in `theory-dc.md`: ZZ, P2, SW, `Q`, `cl`, down-set `D`.
2CH = the contracted switch model (`dc-hardness/twoch.py`): nodes, terminals `s`, `t`, switches `w` with two node
sets (*sides*) `E_w`, `F_w`; a mode vector picks one side per switch; question: are `s`, `t` connected in the
hypergraph of picked sides. P2: `E_w ∩ E_v != ∅` or `F_w ∩ F_v != ∅` for `w != v`. SW + P2 and 2CH + P2 are the same
problem (Section 2), and SW + P2 is a special case of ZZ + P2, i.e. of the open case of DC (theory-dc.md, Theorem 13).

## 0. Results at a glance

| # | Statement | Status |
|---|---|---|
| T1 | The class "`d <= 2` or `c <= 3`" (pairs with `d = 2`, `c >= 4`) is polynomially equivalent to ZZ + P2, hence to the open case of DC | proved (re-read in this run: no error) |
| R | Rigid family `R_L` in SW + P2: unique solution, alternating modes | proved; checked `L <= 16` |
| PC1 | AC and PC on broken rigid families (`R_L` with one backbone node removed, or `t` moved into a flip side), `L <= 8`, 56 no-instances: AC answers wrongly on 30 of them, **PC is right on all**; on TIC no-instances AC is wrong on most, PC again on none (Section 5) | checked |
| D | The dead-end mechanism of `R_L` protects a connector only when the partner of one of its sides is a separator (a forced side). Connectors between two switches whose sides both lie on choice routes are shortcuts; for the SW encoding of the unsatisfiable formula `(x∨y)(x∨¬y)(¬x∨y)(¬x∨¬y)` three switch pairs admit **no** connector at all (every single added node creates a solution), so no P2 completion of that encoding exists | Lemma D proved; the completion obstruction checked exactly |
| L | **Locality dichotomy.** (a) 2CH + P2 with a linear layout of width `k` (nodes per position) and reach `l` (positional diameter of a side) is decidable in `N^{O(kl)}` time. (b) Without P2, 2CH is NP-complete already for width 1 and reach 2 (two-choice interval cover). | proved; (b) checked on 2334 formulas, (a) on 3000 instances |
| T | **TIC is polynomial**: two-choice interval cover with P2 (sides are intervals of a line, any lengths), a special case of 2CH + P2 that contains the rigid family, is solved in `O(K^4 n^{11})` time | proved; algorithm checked against brute force on 2400 + 1456 instances |
| H | **Helly version.** 2CH + P2 is decidable in polynomial time when pairwise intersecting sides of the same type always share a node; in general in `N^{O(t)}` time when such families can be pierced by `t` nodes. Ties (equivalent elements of ZZ) are not covered. | proved |
| C | Consequence for hardness proofs: an NP-hardness proof for the open case of DC through SW + P2 must produce, for every solution of its yes-instances, families of unused sides that pairwise intersect but have unbounded piercing number; through general ZZ it may instead use ties (equivalence classes with many members), where the Helly argument does not apply | proved (from L, T, H) |

Summary: no NP-hardness proof was found. The dead-end mechanism of `R_L` does not extend to a 3-SAT reduction,
and the reason is now precise in two forms: (1) dead ends need forced separators (Lemma D); (2) every "geometric"
encoding (bounded reach, or intervals, or Helly sides) of SW + P2 is polynomial (Theorems L, T, H), although the
same geometric encodings without P2 are NP-complete. The remaining room for a hardness proof is non-Helly side
families or ties.

## 1. The shifted class "d <= 2 or c <= 3" is not easier (fallback closed)

**Theorem 1 (proved).** Let `DC'` be the class of graphs in which every pair `x, y` has `d(x,y) <= 2` or
`c(x,y) <= 3`. Deciding `cp(u,v) = c(u,v)` for pairs with `d(u,v) = 2`, `c(u,v) >= 4` in `DC'` is polynomially
equivalent to ZZ restricted to P2, hence (theory-dc.md, Theorem 13) to the open case of DC.

*Proof.* (ZZ+P2 to `DC'`.) Theorem 13(b) of theory-dc.md produces a graph in DC, and DC is contained in `DC'`;
instances with fewer than four comparable pairs are decided by inspection, so `c = N >= 4` may be assumed.

(`DC'` to ZZ+P2.) Let `G` be in `DC'`, `d(u,v) = 2`, `c(u,v) >= 4`, and `Q4 = {x : c(x,u) >= 4}` (it contains `u`
and `v`). By Corollary 4.2(b) of theory-hardness.md (with `t = 3`) every vertex of a `u`-`v` path inside a minimum
cut lies in `Q4`. Let `x <= y` mean that every minimum `u`-`v` cut containing `y` contains `x`; by
Picard-Queyranne the minimum cuts are exactly the down-sets of this preorder on `V` that contain `u` and not `v`.
Restrict the preorder to `Q4` and let `R` be the edges of `G[Q4]` joining non-equivalent vertices.
A down-set `D` of the restricted preorder is the trace `A ∩ Q4` of the minimum cut `A = {x : x <= d for some d in D}`,
and every trace is such a down-set. Hence a `u`-`v` path inside a minimum cut is a consistent zigzag of
`(Q4, <=, R, u, v)`, and a consistent zigzag with valley set `V` lies inside the minimum cut generated by `V`.
So the answers agree. It remains to show P2.

Let `x, y in Q4` be incomparable. Then minimum cuts `A` with `x in A`, `y notin A` and `B` with `y in B`,
`x notin B` exist. `c(x,y) >= min(c(x,u), c(u,y)) >= 4`, so `d(x,y) <= 2`; `x` and `y` are not adjacent
(theory-hardness.md, Lemma 4.3(i): no edge joins `A - B` and `B - A`). Let `z` be a common neighbour.
If `z = u` or `z = v` it is a common `R`-neighbour below (above) both. Otherwise, by Lemma 4.3(ii),
`z in C = A ∩ B` or `z notin C' = A ∪ B`. Suppose `z notin Q4`: some `Y` with `z in Y`, `u notin Y`,
`|δ(Y)| <= 3` exists; `v notin Y` (else `δ(Y)` would be a `u`-`v` cut with fewer than `c(u,v)` edges) and
`x, y notin Y` (they lie in `Q4`). In the case `z in C` put `W = C ∩ Y`; moving `W` out of `C` gives
`|δ(C - Y)| = |δ(C)| - e(W, V - C) + e(W, C - Y)`. The edges `zx`, `zy` lie in `e(W, V - C)` and in `δ(Y)`, and the
edges counted by `e(W, C - Y)` lie in `δ(Y)` as well, so `e(W, C - Y) <= |δ(Y)| - 2 <= 1` and
`|δ(C - Y)| <= c - 1`; `C - Y` contains `u` and not `v`, a contradiction. The case `z notin C'` is symmetric
(`W = Y - C'`, add `W` to `C'`). Hence `z in Q4`. An edge joins only comparable vertices (Lemma 4.3(i) again), so
`z` is comparable with `x` and with `y`, not equivalent to either, and, `x` and `y` being incomparable, `z` lies
above both or below both: P2 holds. ∎

Re-check in this run (task item 3): every step was re-derived (the trace argument, the identity
`|δ(C - W)| = |δ(C)| - e(W, V - C) + e(W, C - W)`, the side of `z` relative to `x`, `y`); no error found, no change.

Remarks. (1) The argument needs `|δ(Y)| - 2 < 2`, i.e. it works for "d <= 2 or c <= k" with `k <= 3` only. For
`k = 4` a vertex of degree 4 outside the core can join two incomparable core vertices; but such a vertex behaves in
the cut lattice exactly like a lower or upper connector of ZZ (its cost is modular in the sides of `x` and `y`, as
uncrossing forces), so the merging obstruction below is the same (sketch). (2) The bound "deg(z) >= 3" in Lemma
4.3(ii) of theory-hardness.md is not sharp: the same counting with `Y = {z}` shows that `z` has at least as many
neighbours on its own side as on the other, so `deg(z) >= 4`.

## 2. A rigid family in the switch model

Contracted form of SW (`twoch.py`): nodes, terminals `s`, `t`; switch `i` has two node sets `E_i`, `F_i`; a mode
vector picks one of them per switch; question: are `s` and `t` connected in the picked hypergraph. P2: every two
switches have intersecting `E`-sets or intersecting `F`-sets. (Contract the components of the fixed bottom-top
edges into nodes; conversely give each node a bottom vertex, a top vertex and the edge between them. The conversion
used by the scripts is `swlib.to_zz`.)

**Family R_L (proved; checked L = 2..16, `rigid.py`, `results-rigid.txt`).** Switches `x_1..x_L`; the
"path" set `h_k` is `E` for odd `k`, `F` for even `k`, `Fl_k` is the other set. Nodes: `s in h_1`, `t in h_L`,
`y_k in h_k ∩ h_{k+1}`; for `p < q`: `z_pq in Fl_p ∩ h_q` if `q - p` is odd, `w_pq in Fl_p ∩ Fl_q` if `q - p` is
even. P2 holds, and the only connecting mode vector is the alternating one.
*Proof.* P2: same parity gives two `Fl` sets of the same type sharing `w_pq`; opposite parity gives `Fl_p` and
`h_q` of the same type sharing `z_pq`. Uniqueness: let some switch be flipped and let `r` be the first one. The
component of `s` contains no flipped set: a flipped `Fl_p` is reached from a path set only through some `z_pq`,
which lies in `h_q` with `q > p`, and the path sets reachable from `s` without flipped sets are `h_1..h_{r-1}`, all
with index below `r <= p`. So `s` reaches only `h_1..h_{r-1}` and not `t`. ∎
Consequences: every solution has about `L/2` switches in each mode, so no algorithm that tries "all switches in one
mode except boundedly many" decides SW+P2; realised as DC graphs (theory-dc.md, Theorem 13(b)) the witness cut
needs about `L/2` generators on each side (compare `G(k)` of experiments.md).

**Interval form (proved; checked L <= 12, `check_tic.py`).** `R_L` is also an instance of TIC (Section 5): line
`0..L`, switch `k` has the span `h_k = [k-1, k]` (type `E` for odd `k`) and the span `Fl_k = [k, L]`. The same
first-flip argument applies (the edge `(r-1, r)` is covered only by `h_r` and by `Fl_p`, `p < r`), so the alternating
vector is the only solution. Here all flip spans of one type contain the junction `L`: the family is Helly, which is
why Theorem T covers it. Likewise adding `t` to every `Fl_k` of the 2CH form keeps P2 and the unique solution
(a flipped `Fl_p` is still entered only from `h_q`, `q > p`).

**PC on broken rigid families (checked; `rigid_pc.py`, `rigid_pc_big.py`, `results-rigid-pc-{6,7,8}.txt`).**
`cut(L, k)`: `R_L` without `y_k` (no solution: the first-flip argument stops at `h_k`); `tflip(L, k)`: `t` moved
from `h_L` into `Fl_k` (no solution). All keep P2. On all 56 instances with `2 <= L <= 8` (ZZ conversions up to 53
elements and 80 real edges; `results-rigid-pc-small.txt` for `L <= 5`) the exact answer is "no", the relaxation
(both sides of every switch) is "yes" on 48, AC answers "yes" on 30, and PC answers "no" on every one. These are no-instances whose refutation is the unbounded
first-flip induction, yet PC catches them.

## 3. Why the dead-end mechanism of R_L does not give a 3-SAT reduction

Setting: a 2CH instance `I0` (the *backbone*: variable routes and clause options in series) and *connectors*: new
nodes `z` added to one side `X` of a switch `σ` and one side `Y` of a switch `τ` (same type, so that P2 holds for
`σ, τ`). Write `X'`, `Y'` for the partner sides.

**Lemma D (proved).** Let `I` be `I0` plus connector nodes, each added to exactly two sides `X`, `Y` of different
switches. Call an `s`-`X` path of `I0` a sequence of sides of `I0` (connector nodes removed) from a side containing
`s` to `X`, consecutive ones sharing a node. Suppose every connector `z in X ∩ Y` satisfies: every `s`-`X` path of
`I0` uses `Y'`, and every `s`-`Y` path of `I0` uses `X'` (vacuous when there is no such path). Then a mode vector
connects `s`, `t` in `I` iff it does in `I0`.
*Proof.* Let a mode vector connect `s`, `t` in `I`; take a sequence of picked sides from `s` to `t`, consecutive
sides sharing a node. If consecutive sides always share a node of `I0`, it is a sequence of `I0`. Otherwise take the
first consecutive pair that shares only connector nodes; it is `{X, Y}` for a connector `z`, say in the order
`X, Y`. The prefix up to `X` is an `s`-`X` path of `I0`, so it uses `Y'`; the sequence also uses `Y`, and `Y`, `Y'`
are never picked together. Contradiction. ∎
In `R_L`: `I0` keeps only the nodes `s`, `t`, `y_k`; the connectors are the `z_pq` and `w_pq`. For `z_pq` (`X = h_q`,
`Y = Fl_p`, `p < q`) the only `s`-`h_q` path of `I0` is `h_1 ... h_q`, which uses `h_p = Y'`, and there is no
`s`-`Fl_p` path (in `I0` the flip sides are empty); for `w_pq` both conditions are vacuous. So Lemma D gives the
uniqueness statement of Section 2 again.

**Why it fails for 3-SAT (sketch, with an exact check).** In a backbone that encodes a formula with series of
choices (variable routes `T_i`/`F_i`, clause options), the only sides that lie on every `s`-`X` path are forced ones
(junctions). A switch whose two sides are both used in some intended solution (a literal occurrence: route side and
clause side) has no side that is a separator, so a connector between two such switches never satisfies Lemma D in
either direction, and it creates a shortcut between the positions of `X` and `Y` whenever both are picked. Counting
as in theory-hardness.md 6.2 then shows that a P2 completion must contain harmful shortcuts once the formula has
literal occurrences of different variables in three pairwise non-consecutive clauses of each sign.
Exact check (`p2_options.py`, run in this session on the SW encoding `dc-algorithm/sw_sat.encode`, imported
read-only, of the unsatisfiable formula `all4 = (x∨y)(x∨¬y)(¬x∨y)(¬x∨¬y)`, 8 switches): adding a single node is
monotone (it can only connect more), and for the switch pairs `(x in C1, ¬y in C4)`, `(y in C1, ¬x in C3)`,
`(x in C2, ¬y in C4)` every one of the possible additions (a shared existing bottom or top, a new private bottom or
top) turns the answer into "yes". Hence this encoding has no P2 completion at all, regardless of the other pairs.
(`x-notx = (x)(¬x)` is completable: its two switches already share a node.)

The analysis does not exclude all reductions; Sections 4 and 5 make the obstruction precise for whole classes of
encodings.

## 4. Locality dichotomy

A *layout* of a 2CH instance is a map `pos` from nodes to integers; its *width* `k` is the largest number of nodes at
one position, its *reach* `l` the largest difference `max pos(X) - min pos(X)` over sides `X`.

**Theorem L(a) (proved).** A 2CH + P2 instance with a layout of width `k` and reach `l` is decided in
`O(n^{(5l+1)k + 1} · N)` time (`n` switches, `N` nodes).
*Proof.* Switches with an empty side are fixed to the other side. Put `x_w = min pos(E_w)`, `y_w = min pos(F_w)`. If
`E_w ∩ E_v != ∅` then `|x_w - x_v| <= l`; likewise for `F`. *Concentration:* if some `w, v` have `|x_w - x_v| > 2l`,
their `E`-sides are disjoint, so their `F`-sides meet and `|y_w - y_v| <= l`; every other `r` has `|x_r - x_w| > l`
or `|x_r - x_v| > l`, hence `F_r` meets `F_w` or `F_v`, and `|y_r - y_w| <= 2l`. So all `F`-sides lie within the
`5l + 1` positions `[y_w - 2l, y_w + 3l]`. Otherwise all `x_w` lie within `2l`, and all `E`-sides within `3l + 1`
positions. Call the concentrated type `F` and `W` the set of nodes at those positions, `|W| <= (5l + 1)k`.
*Search:* for every set `S` of at most `|W| + 1` switches, put `S` in `F`-mode and the rest in `E`-mode and test
connectivity. If some mode vector connects `s, t`, take a shortest sequence of picked sides `X_1..X_r` from `s` to `t`
and nodes `z_a in X_a ∩ X_{a+1}`; the `z_a` are distinct (a repeated node would shorten the sequence), an `F`-side
`X_a` contains `z_{a-1}` or `z_a` in `W`, so at most `|W| + 1` `F`-sides occur; with `S` their switches, all sides of
the sequence are picked in the test. ∎

**Theorem L(b) (proved).** Without P2, 2CH is NP-complete for layouts of width 1 and reach 2, namely for
*two-choice interval cover*: nodes `0..K` on a line, every side a set of consecutive nodes (a span), `s = 0`, `t = K`
(the picked spans must cover every edge `(j-1, j)`).
*Proof.* In NP: guess the modes. Hardness from 3-SAT in which every variable occurs at most twice positively and at
most once negatively or vice versa (NP-complete: replace a variable with `q` occurrences by copies `x^1..x^q`, one per
occurrence, and add the clauses `(¬x^a ∨ x^{a+1})`, indices mod `q`; each copy then occurs three times, twice with
one sign). Lay out one *clause edge* per clause and, for each variable with a single occurrence `c` of one sign and
occurrences `a` (and `b`) of the other, the *conflict edges* `d_ac` (and `d_bc`) next to each other. Switch = literal
occurrence `w`: its `F`-span is its clause edge, its `E`-span is its conflict edges (`E_c` spans `d_ac` and `d_bc`).
Spans have at most 2 edges. A satisfying assignment gives a cover (`F`-mode iff the literal is true: each clause edge
has a true literal, each conflict edge has a false occurrence). A cover gives an assignment: two occurrences of
opposite signs of one variable cannot both be in `F`-mode (their conflict edge would be uncovered), so the literals
in `F`-mode are consistent, and every clause edge is covered by one of them. ∎
Checked (`check_tic.py`, seed 1): 2334 random formulas of this shape, coverable iff satisfiable in all (1805 yes,
529 no). Theorem L(a) checked on 3000 random TIC + P2 instances (the concentration lemma held in all, and the window
search agreed with brute force).

Reading: P2 is exactly what turns a local NP-complete problem into a polynomial one. Any reduction to SW + P2 must
use sides of unbounded reach in every layout of bounded width: long-range sides such as the `Fl` sides of `R_L`.

## 5. TIC: interval sides of any length

**TIC.** Two-choice interval cover with P2: line `0..K`, every switch `w` has spans `E_w`, `F_w` (or empty), P2 =
"the `E`-spans or the `F`-spans of any two switches share a node". TIC is a special case of 2CH + P2 (nodes = the
junctions `0..K`), hence of the open case of DC, and it contains `R_L` (Section 2). Script: `tic.py`.

**Theorem T (proved).** TIC is decidable in `O(K^4 n^{11})` time.
*Proof.* *Chains.* A minimal set of picked spans covering `[0, K]`, sorted by left end, `I_1, ..., I_r`, has strictly
increasing left and right ends, `0 in I_1`, `K in I_r`, consecutive spans sharing a junction, and
`right(I_a) < left(I_{a+2})` (otherwise `I_{a+1}` is redundant). So `I_a ∩ I_b = ∅` for `|a - b| >= 2`, and every
junction lies in at most two of the spans. *Groups.* Give `I_a` the group `(type of I_a, a mod 2)`. Two spans
`I_a, I_b` of one group satisfy `|a - b| >= 2`, so they are disjoint spans of the same type; by P2 the *partner*
spans (the other spans of their switches) meet. Pairwise meeting intervals share a point (Helly), so for each group
`g` with a member with non-empty partner there is a junction `φ_g` lying in all partner spans of the group (a group
with two members has non-empty partners by P2). *Certificate.* For a guess `φ = (φ_g)` (one junction or none per
group) call a chain admissible if (i) the partner of every member is empty or contains `φ_g` of its group, and
(ii) no two members that contain some `φ_g` belong to the same switch. A minimal cover of a solution is admissible
for its `φ` (its members come from distinct switches). Conversely, in an admissible chain two members `X`, `X'` of
one switch would both contain a `φ` junction (`X'` contains `φ_{g(X)}` by (i), and vice versa), contradicting (ii);
so the members come from distinct switches and picking them is a solution. *Search.* For each of the `(K + 2)^4`
guesses run a breadth-first search over states (previous span, current span, parity, members so far that contain a
`φ` junction); the last component has at most 8 spans because each junction lies in at most two chain members. The
state space is `O(n^{10})` per guess, `O(n)` transitions each. ∎
Checked: `tic_poly.py` (seed 1: 1456 random instances, plus `R_1..R_7`) and `tic_poly_check2.py` (seeds 11-16:
2400 instances, random and P2-repaired local-SAT instances, including 214 no-instances whose relaxation is yes):
algorithm = brute force on all.

**Theorem H (proved; the general form of the argument).** Let `I` be a 2CH + P2 instance in which every family of
pairwise intersecting `E`-sides has a common node, and likewise for `F`-sides (Helly property, e.g. intervals of a
line or subtrees of a tree). Then `I` is decidable in polynomial time. More generally, if every such family can be
pierced by `t` nodes, `I` is decidable in `N^{O(t)} n^{O(t)}` time.
*Proof.* Replace the chain by a shortest sequence `X_1..X_r` of picked sides from `s` to `t`: then `X_a ∩ X_b = ∅`
for `|a - b| >= 2` and every node lies in at most two members. Groups, partners and P2 give, as above, pairwise
meeting partner families, pierced by sets `Φ_g` of at most `t` nodes. Guess `Φ_g` (`N^{4t}` choices) and search over
walks of sides with states (current side, parity, members so far that meet `Φ = ∪Φ_g`), allowing at most two members
through each node of `Φ` (so at most `8t` stored sides), requiring (i) every member's partner is empty or meets
`Φ_g` of its group and (ii) no two stored members belong to one switch. Soundness and completeness are as in
Theorem T. ∎
Remarks. (1) Soundness does not use minimality, so the search may run over arbitrary walks of sides, including
repetitions of a side (a side meets itself), which shift parities; the implementation `helly2ch.py` does so.
(2) The parameter is not bounded on easy instances: in the 2CH form of `R_L` every valid walk uses all of
`h_1, ..., h_L` (unique solution), the partner `Fl_k` of `h_k` meets another flip side only in the private node
`w_jk`, so a node pierces at most two partners of a group, at most `2t` members fit in each of the four groups, and
the `t`-search fails for `L > 8t` (proved). The equivalent forms of Section 2 (interval form, or `t` added to every
flip side) are Helly and are solved with `t = 1`. In general, in the setting of Lemma D, a side all of whose nodes are
connector nodes can be given the node `t` without creating solutions (take a shortest sequence from `s` to a side
containing `t`; it cannot enter such a side through `t` before its end, and entering it through a connector is
excluded as in Lemma D), so guarded dead sides never force a large `t`.
Checked (`helly2ch.py`, seed 1, `results-helly2ch.txt`): on 185 random 2CH + P2 instances (at most 8 nodes) the
`t = 1` search was never wrong on a no-instance (92) and found a solution on every yes-instance (93); it also solves
`R_2..R_5` and the Helly forms of `R_2..R_5` (unique solution and P2 confirmed).

**Consequences for a hardness proof (proved, from L, T, H).**
1. Through SW + P2 (= 2CH + P2): the yes-instances produced must have the property that for every solution and every
   shortest sequence of picked sides, the unused partner sides of some group form a pairwise intersecting family
   with large piercing number (otherwise the `t`-algorithm finds a solution, and it is always right on
   no-instances). Encodings in which sides are intervals, subtrees, or of bounded reach cannot work.
2. Through general ZZ: Theorem H does not cover ties (equivalent elements, i.e. classes of switches forced into
   the same mode, as in the 3-SAT reduction of theory-hardness.md, where a variable is a class and its occurrences
   are the members). There a conflict is any two members of one class used with different sides, and P2 relates
   only members of different classes, so the partner certificate (i) does not control conflicts. This is the
   remaining gap on the side of the switch model.

## 6. Scripts and logs (`dc-hardness/`)

| Script | What | Output |
|---|---|---|
| `twoch.py` | 2CH routines (brute force, P2, random P2 instances) | library |
| `swlib.py` | 2CH to ZZ conversion, AC/PC wrappers around `dc-algorithm/zz.py` (read-only import) | library |
| `rigid.py` | family `R_L` | `results-rigid.txt` |
| `rigid_pc.py`, `rigid_pc_big.py` | AC/PC on broken rigid families | `results-rigid-pc-small.txt` (`L <= 5`), `results-rigid-pc-{6,7,8}.txt` |
| `helly2ch.py` | Theorem H search with `t = 1` on 2CH + P2; `R_L` and its Helly form | `results-helly2ch.txt` |
| `tic_pc_hunt.py` | AC/PC on TIC no-instances, random and hill climbing | `results-tic-pc-{21..26}.txt` |
| `tic.py` | TIC instances, rigid TIC, local SAT family, window algorithm | library |
| `check_tic.py` | Theorem L(b), rigid TIC, Theorem L(a) | console, seed 1 |
| `tic_poly.py`, `tic_poly_check2.py` | Theorem T algorithm vs brute force | console; `results-tic-poly-{11..16}.txt` |
| `p2_options.py` | single-node P2 options of the SW encoding of `all4` | `results-p2-options.txt` |
| `greedy_safety.py`, `exp_exceptional.py`, `branch.py`, `path2.py` | earlier experiments (version 1) | console |

## 7. Next steps

**Conjecture (evidence only).** SW + P2 (= 2CH + P2) is polynomial. Evidence: Theorems L, T, H; Lemma D and the
exact completion obstruction of Section 3; PC never wrong on any instance tried here (rigid variants, TIC).

1. Ties: is 2CH + P2 *with classes* (several switches forced into one mode, P2 only between switches of different
   classes; = ZZ + P2 whose middle classes form an antichain) NP-hard? This is the form in which 3-SAT enters most
   naturally (theory-hardness.md), and Theorem H does not apply. Sketch of why ties do not help in one dimension:
   if the spans of the members of a class used in one mode are confined to the region that this mode covers anyway,
   they can be merged into one span per mode, which gives a TIC instance; the open case is a class whose
   inactive-mode spans must reach far (as P2 demands) without covering anything.
2. Non-Helly 2CH + P2: find a yes-instance family in which every solution needs a large piercing number in
   Theorem H and the unused sides cannot be given a common node, or show that this never happens.
3. Theorem T only proves membership in P (exponent 11); a faster algorithm (for instance with lazily fixed `φ_g`)
   would be needed before stating a running time in a paper.
