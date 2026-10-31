# Round 4, agent r4-hard: towards NP-completeness of ZZ + P2

Status: final for this round (2026-10-18; started 2026-10-16, resumed twice after rate-limit stops). Scripts:
`r4-hard/`. Labels: **proved**, **checked**, **sketch**, **conjecture**, **refuted**. Notation of `r4-brief.md`: ZZ
instance `(Q, <=, R, u, v)`, down-set `D` (`u ∈ D ∌ v`), `G_D` = the `R`-edges with exactly one end in `D`; *bottom* =
element `~ u`, *top* = element `~ v`, *middle* = neither. An `R`-edge `ab` with `a < b` lies in `G_D` iff `a ∈ D ∌ b`.

## 0. Results at a glance (updated as the work goes)

| # | Statement | Status |
|---|---|---|
| L1 | Liveness form: in a *typed* instance the main edges of `G_D` form the subgraph induced by the *live* elements, and the order is exactly a set of 2-clauses on liveness literals; a consistent zigzag of main edges is a path avoiding the forbidden pairs `p <= q` (`p` peak-type, `q` valley-type) | proved (§1) |
| L2 | Link lemma: a private bottom (top) witness joins its pair in exactly one of the four mode combinations, (out, out) (resp. (in, in)); for typed elements VV-lower and PP-upper links only join dead elements and are harmless; a PV link always joins a live element to a dead one, and the dead one is a hub for all its partners of that kind | proved (§2) |
| L3 | If in a typed instance with harmless VV/PP witnesses every valley-type element is comparable with every peak-type element, the instance is polynomial (Prop. 14 of `theory-dc.md` after deleting the witness components) | proved (§2) |
| C1 | With ties, 3-SAT reduces to ZZ without P2 in the switch model with classes (one class per variable, one member per occurrence); the mode of a class is the truth value | proved (§3) |
| O1 | **Counting obstruction for class encodings with clauses in series** (any witness nodes, shared or private, any clause order): if the formula has occurrences of the E-literals of three distinct variables in clauses at pairwise distance `>= 2` and of the F-literals of three further variables in clauses at pairwise distance `>= 2`, some three of these members merge two junctions at distance `>= 2` under a condition on three literals (Lemma 4.1); hence no such encoding is assignment-faithful on the family `φ_k` (`k >= 32`) (Corollary 4.2) | proved (§4); checked on 500 random completions |
| L4 | **Hub lemma** (any ZZ + P2 instance): in every `n × n` block of incomparable pairs some element of the block shares witnesses of one direction with `⌈n/2⌉` elements of the other side; with bottom/top witnesses these form a star of `G_D` in every down-set that puts the star on one side | proved (§4.3) |
| O1' | Unfaithful reductions with merges of bounded span fail the same way when the F-occurrences are spread | sketch (§4.4) |
| G | Guard/bypass mechanism: a middle (conditional) witness can be made harmless for one pair by a guard on the main line and bypass members, but the bypass members are new elements of the critical kind (live in one mode, needing PV witnesses with every independent element), so the construction regresses | sketch (§5) |
| T3 | **Tightness**: if P2 is weakened to "every incomparable pair `x, y` has an `R`-neighbour of `x` comparable with `y` (or vice versa)", which is distance `<= 3` in the realised graph, ZZ is NP-complete; graph form: deciding `cp(u,v) = c(u,v)` is NP-complete on graphs in which every pair has `d <= 3` or `c <= 2`, even with `d(u,v) = 2`, `c(u,v) >= 3` | proved (§6); checked (§6) |

## 1. Liveness form of typed instances (L1, proved)

**Definition.** A ZZ instance is *typed* if its elements are partitioned into `Vt ∋ u` (valley type), `Pt ∋ v` (peak
type) and a set `W` of *witness elements*, each a bottom or a top, such that every `R`-edge with no end in `W` (a *main
edge*) joins an element of `Vt` (lower end) to an element of `Pt` (upper end), and every `R`-edge at a witness joins it
to a non-witness element. For a down-set `D` the *liveness* of `x ∈ Vt` is `λ(x) = [x ∈ D]`, of `y ∈ Pt` it is
`λ(y) = [y ∉ D]`; an element is *live* or *dead* accordingly.

**Lemma 1.1 (proved).** (a) A main edge `xy` (`x ∈ Vt`, `y ∈ Pt`) lies in `G_D` iff `x` and `y` are both live.
(b) The order relations translate as: `a <= b` with `a, b ∈ Vt` gives `λ(b) ⇒ λ(a)`; with `a, b ∈ Pt` gives
`λ(a) ⇒ λ(b)`; `a <= b` with `a ∈ Vt`, `b ∈ Pt` gives `λ(a) ∨ λ(b)`; `a <= b` with `a ∈ Pt`, `b ∈ Vt` gives
`¬λ(a) ∨ ¬λ(b)` (a *conflict*). (c) A `u`-`v` path of main edges is a zigzag whose valleys are its `Vt`-vertices
and whose peaks are its `Pt`-vertices; it is consistent iff it contains no conflict pair.

*Proof.* (a) `x < y` (a real edge joins strictly comparable elements, lower end `x`), so the edge is in `G_D` iff
`x ∈ D ∌ y`. (b) `a <= b` means `b ∈ D ⇒ a ∈ D`; substitute the definitions of `λ`. (c) Main edges go up from `Vt` to
`Pt`, so a path of main edges alternates and goes up at every `Vt`-vertex: it is a zigzag with valleys in `Vt` and
peaks in `Pt`. A valley `>=` a peak is a pair `p <= q` with `p ∈ Pt`, `q ∈ Vt`. ∎

So, witnesses aside, typed ZZ is "a path avoiding forbidden pairs" in the bipartite main graph, with the forbidden
pairs closed under the composition `p <= q <= p' <= q'` (`p <= q'`) that transitivity imposes. The 3-SAT reduction of
`theory-dc.md` Theorem 13(c) is typed (`Vt = {e_0, T_i, F_i, c_j}`, `Pt = {d, a_i, P_{j,k}}`), and so are the class
encodings of §3.

## 2. The link lemma (L2, L3; proved)

**Lemma 2.1 (proved).** Let `x, y` be incomparable middle elements and `b` a bottom whose only `R`-edges are `bx`,
`by` (a *private lower witness*). In `G_D`, `b` is adjacent to `x` iff `x ∉ D`; so `b` joins `x` and `y` iff
`x, y ∉ D`, and otherwise is a leaf or isolated. Dually a private top `t` joins `x, y` iff `x, y ∈ D`.

*Proof.* `b ∈ D` for every `D` (`b <= u`), `b < x`, so `bx ∈ G_D` iff `x ∉ D`. ∎

For a shared witness the same holds for each of its edges, so a bottom `b` joins all its neighbours outside `D`.
For typed elements write the four combinations as live/dead: a `Vt`-element outside `D` and a `Pt`-element inside `D`
are dead. Lemma 2.1 gives:

| pair | lower witness (both out of `D`) | upper witness (both in `D`) |
|---|---|---|
| `Vt`-`Vt` | dead, dead | live, live |
| `Pt`-`Pt` | live, live | dead, dead |
| `Vt`-`Pt` | dead `Vt`, live `Pt` | live `Vt`, dead `Pt` |

**Lemma 2.2 (dead elements are hubs; proved).** In a typed instance a dead `Vt`-element `x` has no main edge in `G_D`
(its main neighbours lie above it, outside `D` with it); its edges in `G_D` go to its lower witnesses. Hence `x`
joins every element outside `D` that shares a lower witness with `x` (N1 of the brief). Dually for a dead
`Pt`-element and upper witnesses.

*Proof.* `x ∉ D` and `x < y` for every main neighbour `y`, so `y ∉ D` and `xy ∉ G_D`. Its other `R`-neighbours are
witnesses; a lower witness `b ∈ D` is adjacent to `x` in `G_D`, an upper witness (outside `D`) is not. ∎

**Lemma 2.3 (harmless witnesses; proved).** Suppose every bottom witness has all its `R`-neighbours in `Vt` and every
top witness all its `R`-neighbours in `Pt`. Then for every `D` the component of `G_D` containing a witness contains no
live element and neither `u` nor `v`. So `u` and `v` are connected in `G_D` iff they are connected by main edges
between live elements.

*Proof.* A bottom `b ∈ D` is adjacent in `G_D` exactly to its neighbours outside `D`, which are dead `Vt`-elements;
a dead `Vt`-element is adjacent only to bottoms (Lemma 2.2). The set of these bottoms and dead `Vt`-elements is closed
under adjacency in `G_D`; it contains no live element; `u` is not in it (`u` is not adjacent to an element `~ u`, and
`u` is live). Dually for tops. ∎

So `Vt`-`Vt` pairs can always be witnessed harmlessly by a *bottom hub* adjacent to all of `Vt - {u}`, and
`Pt`-`Pt` pairs by a top hub adjacent to all of `Pt - {v}`. The `Vt`-`Pt` pairs are the whole difficulty:

**Proposition 2.4 (L3; proved).** If an instance satisfies the hypothesis of Lemma 2.3 and every element of `Vt` is
comparable with every element of `Pt`, ZZ is decided in `O(|Q| |R|)` time.

*Proof.* By Lemma 2.3 the witnesses can be deleted without changing any answer. What remains has `R` bipartite between
`Vt ∋ u` and `Pt ∋ v` with every cross pair comparable; this is Proposition 14 of `theory-dc.md`. ∎

Reading: every typed hardness construction must contain incomparable `Vt`-`Pt` pairs, and each of them (with a
bottom or top witness) is a live-dead link, i.e. it puts a live element into the hub of a dead one (Lemma 2.2). This
is the precise form of the "shortcut" of `theory-dc.md` §5 and `theory-hardness.md` §6.2.

## 3. Ties encode 3-SAT without P2 (C1, proved)

*Construction.* CNF `φ` with clauses `C_1, ..., C_m`. Switch model with classes (2CH with classes, `r4-brief.md` §1):
junction nodes `n_0 = s, n_1, ..., n_m = t`; one class `X_i` per variable; for each variable choose its *E-literal*
(`x_i` or `¬x_i`); for an occurrence of a literal `ℓ` of `x_i` in `C_j` one member of `X_i` with *main side*
`{n_{j-1}, n_j}`, of type E if `ℓ` is the E-literal and of type F otherwise, and empty other side. The mode E of `X_i`
means "the E-literal is true".
*Claim.* `s, t` are connected under a mode vector iff the corresponding assignment satisfies `φ`.
*Proof.* The picked sides are the main sides of the members whose literal is true; the pair `{n_{j-1}, n_j}` is
contained only in sides of members of `C_j`, so the picked hypergraph is the path `n_0 ... n_m` with the link
`n_{j-1} n_j` present iff `C_j` has a true literal. ∎
In ZZ form (nodes = bottom-top pairs with a fixed edge, members = middle elements, classes = ties) this is typed with
`Vt` = members of type F (live in `D`) and `Pt` = members of type E (live outside `D`). P2 fails
for almost all pairs of members of different classes; §4 shows that no completion by witness nodes is faithful once
the occurrences are spread out (Corollary 4.2).

## 4. Counting obstruction for series class encodings (O1, proved)

**Setting S.** The instance of §3 plus arbitrary *witness nodes* (nodes other than `n_0, ..., n_m`), each added to any
sides of any members, such that P2 holds: members `a, b` of different classes have `E_a ∩ E_b ≠ ∅` or
`F_a ∩ F_b ≠ ∅`. So a member's main side is `{n_{j-1}, n_j}` plus witness nodes, its other side (*dead side*)
consists of witness nodes only. Witness nodes may be shared by any number of sides. The clause order is arbitrary.

Call a member an *E-member* if its main side has type E (its literal is the E-literal of its variable), an
*F-member* otherwise. An E-member is live (main side picked) iff its literal is true; an F-member likewise.

**Lemma 4.1 (proved).** Let `p_1, p_2, p_3` be E-members of three distinct variables in clauses `π_1, π_2, π_3` with
`|π_a - π_c| >= 2` for `a ≠ c`, and `q_1, q_2, q_3` F-members of three further distinct variables in clauses
`κ_1, κ_2, κ_3` with `|κ_b - κ_d| >= 2`. In every instance of setting S one of the following holds:
(E) some `q_b` and two `p_a, p_c` (`π_a < π_c`) satisfy `E_{p_a} ∩ E_{q_b} ≠ ∅ ≠ E_{p_c} ∩ E_{q_b}`; then under every
mode vector in which the classes of `p_a`, `p_c`, `q_b` are in mode E, the junctions `n_{π_a}` and `n_{π_c - 1}` are
connected by the three sides `E_{p_a}`, `E_{q_b}`, `E_{p_c}`;
(F) some `p_a` and two `q_b, q_d` (`κ_b < κ_d`) satisfy `F_{q_b} ∩ F_{p_a} ≠ ∅ ≠ F_{q_d} ∩ F_{p_a}`; then under every
mode vector with these three classes in mode F, `n_{κ_b}` and `n_{κ_d - 1}` are connected.

*Proof.* For each of the nine pairs `(p_a, q_b)` P2 gives a common node of `E_{p_a}` and `E_{q_b}` or of `F_{p_a}`
and `F_{q_b}`; call the pair an E-pair or an F-pair accordingly (one of them, if both). If (E) fails, each `q_b` is in
at most one E-pair, so in at least two F-pairs: at least 6 F-pairs. If (F) fails, each `p_a` is in at most one F-pair:
at most 3 F-pairs. So (E) or (F) holds. In case (E), with the three classes in mode E, the E-sides of the three members
are picked (for `q_b` its dead side); `E_{p_a} ∋ n_{π_a}`, `E_{p_c} ∋ n_{π_c - 1}`, and both meet `E_{q_b}`. Case (F)
is symmetric. The three classes are distinct, so the modes can be chosen independently. ∎

The merge bypasses the clauses strictly between `π_a` and `π_c` (at least one, since `π_c >= π_a + 2`): `s` reaches
`t` as soon as all other clauses have a true literal.

**Corollary 4.2 (assignment-faithfulness fails; proved).** Call an instance of setting S *faithful* if for every
assignment `σ`, `s, t` are connected under `σ` iff `σ` satisfies `φ`. Let `φ_k` (`k >= 32`) consist of the clauses
`A_i = (x_i ∨ a_i)`, `B_i = (¬x_i ∨ b_i)`, `i = 1..k`, in any order (`a_i, b_i` fresh). No instance of setting S for
`φ_k` is faithful.

*Proof.* Each `x_i` has one E-occurrence and one F-occurrence (one of `A_i`, `B_i` contains its E-literal). Number the
clause positions `1..2k`. Call a clause *special* if it belongs to one of the six variables chosen below. Pick three
variables whose E-occurrence clauses are pairwise at least 14 positions apart (take the 1st, 15th and 29th smallest
of the `k` E-occurrence positions), then three other variables whose F-occurrence clauses are pairwise at least 14 apart
(among the `k - 3 >= 29` remaining). Lemma 4.1 applies; say (E) holds with `p_a, p_c, q_b` (case (F) is symmetric).
At most 12 clauses are special, and at least 13 clauses lie strictly between `π_a` and `π_c`, so one of them, `K`, is
not special; `K` is `A_i` or `B_i` of a variable `x_i` not among the six. Let `σ` put the classes of `p_a`, `p_c`, `q_b`
into mode E, make the literal of `x_i` in `K` false and the fresh literal of `K` false, and make the fresh literal of
every other clause true. Then `K` is the only false clause, so `σ ⊭ φ_k`; all clauses before `π_a` and after `π_c`
are true (their junction links are present), and Lemma 4.1 joins `n_{π_a}` to `n_{π_c - 1}`: `s` and `t` are connected.
∎

*Checked* (`r4-hard/o1check.py`, outputs `r4-hard/run-o1-2.txt`): seed 2, 500 random instances of setting S for
`φ_32` (random clause order, random E-literal per variable, random P2 completion with fresh or reused witness nodes,
reuse probability uniform in `[0, 1]`; P2 and "dead sides hold witness nodes only" asserted): the construction of the
proof found a configuration of Lemma 4.1 every time (471 of case (E), 29 of case (F)), and the assignment it builds
falsifies exactly the clause `K` and connects `s, t` in all 500. Small formulas (seed 2, 1000 random CNFs with 3-6
variables, 3-8 clauses of 1-3 literals, random completions, all assignments enumerated): satisfying assignments always
connect (asserted), and 829 of the 1000 completions are unfaithful; the 171 faithful ones are formulas too small for
Lemma 4.1 or completions where the merges happen to land harmlessly.

**Remarks.** (1) Lemma 4.1 needs no restriction on the witness nodes (shared hubs, private nodes, any number), and
none on the clause order; it is the rigorous form of the sketch in `theory-hardness.md` §6.2, transferred from the
graph reduction to the class encoding. (2) Faithfulness is what all known encodings have; an unfaithful reduction would
need the bypassed clauses to be implied by the rest of the formula and the three activating literals (for an
unsatisfiable formula: every assignment with those literals that satisfies the clauses outside the stretch must fail
inside it). For the complete formula `K_w` (all `2^w` clauses on `w` variables, unsatisfiable, each assignment
falsifies exactly one clause) the reduction fails as soon as the clause order contains, for some six variables, an
alternation `A B A B A B` of a clause `A` agreeing with the E-literals of the six and a clause `B` agreeing with their
F-literals (put `π_a`, `κ_b` at these clauses; the falsified clause is a `B` resp. `A` inside the stretch). Whether
every order of `K_w` contains such an alternation for large `w` is a Ramsey-type question not settled here
(conjecture). (3) The setting excludes helper members and middle witnesses; §5 discusses them.

### 4.3 The hub lemma: the general form of the counting (proved)

**Lemma 4.3 (hub lemma; proved).** Let `A, B ⊆ Q`, `|A| = |B| = n >= 1`, every `a ∈ A` incomparable with every
`b ∈ B`, in any ZZ instance with P2. Then (L) some `b ∈ B` and some `A' ⊆ A` with `|A'| >= ⌈n/2⌉` are such that every
`a ∈ A'` has a common `R`-neighbour `w_a` with `b` strictly below both, or (U) dually some `a ∈ A` and `B' ⊆ B`,
`|B'| >= ⌈n/2⌉`, with common `R`-neighbours strictly above. In case (L), in every down-set `D` with `b ∉ D`,
`A' ∩ D = ∅` and all `w_a ∈ D` (automatic for bottom witnesses), `b` and `A'` lie in one component of `G_D`.

*Proof.* Give each pair `(a, b)` one witness (P2) and call the pair L or U by its direction. If every `b` is in at
most `⌈n/2⌉ - 1` L-pairs, at least `n (n - ⌈n/2⌉ + 1) = n (⌊n/2⌋ + 1)` pairs are U-pairs, so some `a` is in at least
`⌊n/2⌋ + 1 >= ⌈n/2⌉` of them. In case (L) the edges `w_a a`, `w_a b` have their lower end in `D` and upper end outside,
so they are in `G_D`. ∎

Lemma 4.1 is the case `n = 3`. The lemma is the quantitative form of N1 of the brief: P2 alone forces, inside every
`n × n` block of incomparable pairs, a witnessed star with `n/2` leaves around one element of the block, active in the
down-sets in which the star's elements are on the same side and its witnesses on the other. A reduction must make every
such star harmless in every down-set where it is active; for bottom/top witnesses the only freedom is the choice of
the centre and the leaves, which Lemma 4.1 and Corollary 4.2 show to be insufficient for series encodings. For middle
witnesses the activation needs the witnesses on the right side, which a construction can make costly (§5).

### 4.4 Unfaithful reductions with short merges (sketch)

A correct but unfaithful reduction could tolerate merges whose span is short (e.g. if the formula is repeated several
times in series, a merge shorter than one copy leaves a full copy to be satisfied). Requiring every merge to span at most
`w` positions is impossible when E- and F-members are spread: let each F-member `q` have its E-contacts (case (E)
partners) inside a window `W(q)` of width `w` and each E-member `p` its F-contacts inside a window `W'(p)`. Every pair
`(p, q)` of different classes has a contact of one kind, so for two E-members `p_1, p_2` at distance `> w`, every
F-member misses `p_1` or `p_2` with its window and therefore lies in `W'(p_1)` or `W'(p_2)`: all F-members of the other
classes lie in two windows of width `w`. Repeating the formula, or any formula with F-occurrences spread over more than
`2w` positions, violates this (sketch: the argument ignores merges through chains of several contacts, which only make
things worse for the reduction).

## 5. Conditional (middle) witnesses: the guard mechanism and its regress (G, sketch)

A middle lower witness `w` of `x, y` (`w < x, y`) is active only if `w ∈ D`, which needs `↓w ⊆ D`. Put a *guard*
`g < w`, an element of peak type on the main line (all `u`-`v` connections pass a junction that is joined only
through `g`). Then `x ∈ D` or `y ∈ D` forces `g ∈ D` (order), so the line is cut at `g` unless a *bypass* exists, and
the link is active only with `g ∈ D`. Provide bypass members `b_x` (valley type, live exactly when `x ∈ D`, e.g. a
member of the class of `x`) and `b_y` whose main sides join the two neighbours of `g`. Then:
- when `x ∈ D` or `y ∈ D`, `g` is dead but bypassed (intended solutions survive);
- when `x, y ∉ D` and `w ∈ D` (the only combination in which the link is active), `g` is dead and not bypassed, so the
  link cannot help (Lemma D of `dc-hardness.md` in a conditional form).
For one pair this is a complete gadget (sketch; it is the dead-end mechanism of `R_L` with the separator created by the
order). *Regress:* the bypass member `b_x` is a valley-type element live exactly when the class of `x` is in `D`; it is
incomparable with the elements of every other free variable and needs, by Proposition 2.4 and Lemma 2.2, live-dead
links with the peak-type elements of the other variables, i.e. it is again a member of the critical kind, now located
at the guard. Sharing one guard among many pairs fails because the bypass then exists as soon as one of the involved
classes is in `D` (an OR over all of them), which in any assignment with one false variable lifts every guard. A
hierarchy (links guarded at positions before both ends, guards of guard-links before those) mimics the first-flip
argument of `R_L` but needs two new bypass members per pair at every level; the number of elements grows without
bound. No terminating version was found.

*Why the regress does not close (sketch).* For lower witnesses all bypass members are of valley type (live when their
class is in `D`), so bypass members of different classes form `Vt`-`Vt` pairs, which are harmless (Lemma 2.3). The
pairs that remain are (E-member `p'` in the clause region) × (bypass member `b` in the guard region). If they are
witnessed by nodes, the window argument of §4.4 applies with the guard region in place of the clause positions: either
the dead side of `b` collects live E-members from spread clause positions (a clause shortcut), or the dead side of a
dead `p'` collects live bypass members from spread guard positions, which joins the two sides of a guard whose link is
active and so lifts that guard. If they are guarded in turn, the next level of bypass members is again spread over a
new guard region. Shared guards fail by the OR argument above; placing the guard at the clause of `p` or of `q` turns
the guarded link into an F-type contact of the dead side of the other member (checked by hand on the two placements).
Placing all guards of one class in one contiguous block lets one bypass member per class serve that block, but every
guard serves two classes and a line has no order in which both groupings are contiguous.
So the conditional witnesses of N6 change which contacts occur but, in every arrangement tried, not their number
(Lemma 4.3 applies to the members of every level).

## 6. Tightness: one-sided witnesses suffice for NP-completeness (T3)

*P3 (one-sided witness condition).* Every two incomparable elements `x, y` have: an `R`-neighbour of `x` comparable
with `y`, or an `R`-neighbour of `y` comparable with `x`. (P2 asks for one element that is a common neighbour and
comparable with both, in the same direction.)

**Theorem T3 (proved).** (a) ZZ restricted to instances with P3 is NP-complete. (b) Deciding `cp(u,v) = c(u,v)` is
NP-complete on graphs in which every pair `x, y` has `d(x,y) <= 3` or `c(x,y) <= 2`, even when `d(u,v) = 2` and
`c(u,v) >= 3`. So the distance bound 2 of the class DC is exactly where the known hardness stops.

*Proof.* Membership in NP: Lemma 6 of `theory-dc.md` (a path is tested by one closure computation; for ZZ a zigzag is
tested directly). Hardness: let `I0 = (Q0, <=, R0, u, v)` be the instance of `theory-dc.md` Theorem 13(c) for a
3-CNF formula (no P2). Add, for every `x ∈ Q0 - {u, v}`, a *pendant* `b_x` with `u < b_x < y` for every
`y ∈ Q0 - {u}`, the pendants pairwise incomparable, and the single real edge `b_x x`. Call the result `I`.
- `I` is a ZZ instance: the new relations are transitive (only `u` lies below a pendant; everything above a pendant is
  an old element other than `u`), `u` is least, `v` greatest, the edge `b_x x` joins `b_x < x`. The order among old
  elements is unchanged.
- Same answer: a down-set `D` of `I` meets `Q0` in a down-set of `I0`, and every down-set `D0` of `I0` with
  `u ∈ D0 ∌ v` gives the down-set `D0 ∪ {all pendants}` of `I`. A pendant has one `R`-edge, so in every `G_D` it is a
  leaf or isolated, and `u`, `v` are connected in `G_D` iff they are in `G_{D ∩ Q0}` of `I0`.
- P3: two incomparable old elements `x, y`: `b_x` is an `R`-neighbour of `x` and `b_x < y`. Two pendants `b_x, b_y`:
  `x` is an `R`-neighbour of `b_x` and `b_y < x`. A pendant and an old element are comparable.
- (b) Realise `I` by Theorem 13(b) of `theory-dc.md` (its cut formula and the identification of the minimum cuts with
  the down-sets do not use P2, `dc-algorithm.md` Corollary B'): every strictly comparable pair carries an edge or an
  ear, plus ears `u a`, `b v`; equivalent elements do not occur except through `u`, `v` themselves. Comparable
  elements are at distance `<= 2`; incomparable `x, y` at distance `<= 3` via `x b_x`, then the edge or ear between
  `b_x` and `y` (`b_x < y`); two pendants `b_x, b_y` via the edge or ear between `b_x` and `y` followed by the edge
  `y b_y`, length at most 3. Ear vertices have degree 2, so `c <= 2` for every pair containing one.
  `d(u,v) = 2` (ear `uv`, no edge), `c(u,v) = N >= 3`, and `cp = c` iff `I` has a consistent zigzag. ∎

*Checked* (`r4-hard/t3.py 1 400 4`, output `r4-hard/run-t3-1.txt`): 400 random formulas (1-3 variables, 1-4 clauses
of 1-3 literals; 290 satisfiable, 110 not): order axioms, real edges between strictly comparable elements, P3 by
brute force (0 failures), P2 fails on all 400 (as it must, the reduction is the P2-free one), ZZ answer by
`zz.exact_dfs` and by the independent `verify/equivalence/eqcore.zz_dfs` equal to satisfiability on all 400. Graph
level with the independent realisation `eqcore.realise` and the flow-based PIMC search `eqcore.pimc_flow_dfs` on the
formulas `(x1)` (367 vertices), `(x1)(¬x1)` (530), `(x1 ∨ x2)` (700), `(x1)(¬x1 ∨ x2)` (914): `d(u,v) = 2`,
`c(u,v) = N` (135, 192, 252, 326), every pair of element vertices at distance `<= 3`, every ear vertex of degree 2,
PIMC answer = satisfiability (yes, no, yes, yes).

## 7. Other routes tried (dead ends, sketches)

- **Free variable switches with one-way occurrences** (variables as switches whose sides lie in an always-covered
  region, as the mates of `dc-general.md` §3; occurrences one-way comparable with their variable). The variable switch
  then needs no witnesses, but two occurrences of independent variables are still incomparable (any comparability
  between them either composes to an implication between the two variables, e.g. `Y < q < p < X`, or forbids using both
  in one zigzag), so they need witnesses and §2 applies to them unchanged (sketch).
- **Join witnesses in a lattice of classes.** Let the classes generate a Boolean lattice (an element `S` for a set of
  variables, below/above its variables). The join of two classes is an upper witness that is inactive in every
  *principal* down-set, i.e. every down-set that comes from one assignment, but ZZ ranges over all down-sets, and
  unions of principal ones simulate several assignments at once: for `(x1)(x2)(¬x1 ∨ ¬x2)` the down-set
  `↓{1} ∪ ↓{2}` passes all three clause tests although the formula is unsatisfiable (checked by hand). Forcing
  principality needs the Horn rule "`S, S' ∈ D ⇒ S ∪ S' ∈ D`", which is not an order relation, and connectivity cannot
  enforce it because activating more edges never disconnects.
- **Forcing a join into `D`.** Making `J ∉ D` costly by an essential valley `c > J` freezes both classes below `J`
  (N2); making `c` bypassable when one class is out of `D` needs E-type bypass members, the dual of §5 (sketch).
- **Product (grid) orders.** In a product of chains every incomparable pair has a meet and a join inside the order, so
  P2 can be met by middle witnesses that are themselves order elements; no NP-hard problem on staircases with a natural
  connectivity check was found (not pursued further).

## 8. Verdict, proved statements, checks, open problems

**Verdict.** No NP-hardness proof for ZZ + P2 was found; instead the obstruction is now a theorem for the natural
class encodings: P2 forces witnessed stars (Lemma 4.3), and in every encoding with variables as classes, clauses in
series and node witnesses some star merges two far junctions under a three-literal condition, so the encoding is never
assignment-faithful (Lemma 4.1, Corollary 4.2), while the same reduction becomes NP-complete as soon as P2 is weakened
to one-sided witnesses, i.e. to distance 3 (Theorem T3).

Proved: L1 (liveness form, Lemma 1.1); L2 (Lemmas 2.1-2.3: link combinations, dead elements are hubs, harmless
VV/PP witnesses); L3 (Proposition 2.4: typed instances without incomparable valley-type/peak-type pairs are
polynomial); C1 (3-SAT via ties without P2); O1 (Lemma 4.1, Corollary 4.2); L4 (hub lemma 4.3); T3 (NP-completeness
with one-sided witnesses; graph form for "`d <= 3` or `c <= 2`").
Checked: T3 (`t3.py`, seeds 1 and 2: 1000 formulas, 0 mismatches; four realised graphs of 367-914 vertices with
`d(u,v) = 2`, `c = N`, all element pairs at distance `<= 3`, ears of degree 2, PIMC = satisfiability); Corollary 4.2
(`o1check.py` seed 2: 500 random completions of `φ_32`, construction succeeded in all; 829 of 1000 small random
completions unfaithful).
Sketches: §4.4 (bounded-span unfaithful reductions), §5 (guards and the regress of bypass members), §7.
Open: (1) the complexity of ZZ + P2; by `r4-switch.md` (2CH + P2 in P) and this report, a hardness proof must use
ties together with conditional (middle) witnesses or order relations between middle elements in a way that is not a
series class encoding with node witnesses, and must not be assignment-faithful in the sense of Corollary 4.2 for such
encodings; (2) whether every clause order of the complete formula `K_w` contains the alternation of §4 Remark (2)
(this would turn Corollary 4.2 into a statement about all correct, not only faithful, series class encodings);
(3) whether the regress of §5 can be closed by a construction that is not a line (guards in a tree or a grid);
(4) 2CH with classes + P2 (no middle witnesses): polynomial? `r4-switch.md` §7.2 sketches what carries over; Lemma 4.1
shows that its SAT-style instances are never faithful.

## 9. Files (`r4-hard/`)

| Script | What | Output |
|---|---|---|
| `t3.py` | Theorem T3: pendant construction, order/P3/P2 checks, two exact ZZ solvers vs satisfiability, graph realisation (`eqcore.realise`), distances, ear degrees, PIMC by `eqcore.pimc_flow_dfs` | `run-t3-1.txt` (seed 1, 400 formulas, 4 graphs), `run-t3-2.txt` (seed 2, 600 formulas) |
| `o1check.py` | setting S instances with random P2 completions; construction of Corollary 4.2; faithfulness of small completions by enumeration | `run-o1-2.txt` (seed 2) |

Imported read-only: `dc-algorithm/zz.py` (`from_sat`, `exact_dfs`), `verify/equivalence/eqcore.py` (`zz_dfs`,
`realise`, `Flow`, `pimc_flow_dfs`, `bfs_dist`).
