# Round 4 on the open case of DC: brief (coordinator, 2026-10-16)

Question of the author: is the open case of the class DC polynomial or NP-complete?
Open case: `G ∈ DC` (every pair has `d <= 2` or `c <= 2`), `d(u,v) = 2`, `c(u,v) >= 3`; then `cp(u,v) ∈ {c, c+1}`
and `cp = c` iff some minimum `u`-`v` cut contains a `u`-`v` path.
Labels in every report: **proved**, **checked** (exact computation on named instances), **sketch**, **conjecture**,
**refuted**.

## 1. The problem in its equivalent form (proved earlier)

`theory-dc.md` Theorem 13 (re-verified in `verify/equivalence.md`): the open case is polynomially equivalent to
**ZZ + P2**.

*ZZ.* Instance `(Q, ≤, R, u, v)`: a finite preorder with least element `u` and greatest element `v`; `R` a set of
pairs `{a, b}` with `a < b` (real edges), `{u, v} ∉ R`. For a down-set `D` with `u ∈ D ∌ v`, `G_D` is the graph of
the `R`-edges with exactly one end in `D`. Question: does some `G_D` connect `u` and `v`? Equivalently: is there a
consistent zigzag, a `u`-`v` path `x_0 < x_1 > x_2 < ... > x_L` of `(Q, R)` (valleys at even, peaks at odd
positions) in which no valley is `>=` a peak.
*P2.* Every two incomparable elements have a common `R`-neighbour that lies strictly below both or strictly above
both (a *lower* or *upper witness*).
Without P2, ZZ is NP-complete (Theorem 13(c)) and W[1]-hard in width plus length (`dc-algorithm.md` Theorem B).
Every instance of ZZ + P2 is realised by a graph of DC (Theorem 13(b)), so a hardness proof may build posets freely.

*Switch model 2CH* (`dc-hardness.md`, `verify/lth.md` §1): bottoms all equivalent to `u`, tops all equivalent to `v`,
middle elements (*switches*) pairwise incomparable. Contracted form: nodes, terminals `s`, `t`; switch `w` has two
node sets `E_w` (bottom neighbours) and `F_w` (top neighbours); a mode vector picks one side per switch (E-mode =
switch outside `D` = used as a peak; F-mode = inside `D` = used as a valley); question: are `s`, `t` connected in the
hypergraph of picked sides. P2: `E_w ∩ E_v != ∅` or `F_w ∩ F_v != ∅` for all `w != v`.
*2CH with classes*: switches grouped into classes forced into one mode; P2 only between switches of different classes
(this is ZZ + P2 whose middle classes form an antichain).

## 2. What is known (one line each; details in the files named)

| Result | Status | File |
|---|---|---|
| FPT in `c`: `O(e c! c^2 n^3 + nm)` | proved | `dc-algorithm.md` A |
| XP in the width of the order | proved | `dc-algorithm.md` C |
| Polynomial if every incomparable pair has a lower witness (or every pair an upper one) | proved | `dc-algorithm.md` F+ |
| XP in `min(ω(U), ω(Λ))`; `U` = incomparable pairs with no lower witness, `Λ` = with no upper witness | proved | `dc-algorithm.md` Fω |
| Lemma S: in a globally shortest consistent zigzag, two peaks at distance `>= 4` have all common neighbours in `↑P`; two valleys at distance `>= 4` all in `↓V` | proved | `dc-algorithm.md` §11.2 |
| TIC (2CH with interval sides) + P2: polynomial; 2CH + P2 with Helly side families: polynomial; with piercing number `t`: `N^{O(t)}` | proved | `dc-hardness.md` T, H |
| 2CH + P2 with a layout of bounded width and reach: polynomial; without P2 NP-complete already at width 1, reach 2 | proved | `dc-hardness.md` L |
| Certificate theorem GC: walk search with pin sets, sound always, complete when `κ <= k` | proved | `dc-general.md` §1 |
| Ties or one-way comparabilities make `κ` unbounded (family `T_L`, Proposition M) | proved | `dc-general.md` §3 |
| AC does not decide ZZ + P2 (9 elements) | refuted | `dc-algorithm.md` D1 |
| PC does not decide ZZ + P2 (hub `H(2,2)`, 22 elements), but `H(2,2)` lies in the polynomial class F | refuted | `dc-algorithm.md` E, F |
| Bounded number of generators fails (ladder `K(k)`, `A14`, rigid `R_L`, `Z_k`) | refuted | `dc-algorithm.md` §11.6, `theory-dc.md` |
| Rigid family `R_L`: P2, unique solution with alternating modes; dead-end Lemma D | proved | `dc-hardness.md` §2, §3 |
| Shortcut obstruction for 3-SAT encodings with clauses in series and one vertex per literal (counting) | sketch | `theory-hardness.md` §6.2 |
| Conjectures: 2CH + P2 polynomial; PC decides 2CH + P2 | conjecture | `dc-hardness.md` §7, `dc-algorithm.md` §7 |

## 3. New observations of this round (coordinator; check them before you rely on them)

**(N1) Witness networks; every element is a hub.** Fix `D`. An element `x ∉ D` is joined in `G_D` to each lower
witness `w ∈ D` of its pairs, hence to every partner `y ∉ D` that shares such a witness; an element `x ∈ D` likewise
joins all partners `y ∈ D` that share an upper witness `w ∉ D`. So a shortcut between two parts of a zigzag never needs
a special hub: the dead (unused) member of a witnessed pair is the hub. Call `x` *live* if it is attached to the main
structure by non-witness edges in `G_D`. A witness design is harmless for `D` iff no component of the active witness
network contains two live elements that the main structure keeps apart.

**(N2) When a witness can be switched off.** Let `Z` be a consistent zigzag with peaks `P`, valleys `V`. A lower
witness `w` of `x, y` gives the active edges `w x`, `w y` in some `G_D` with `↓V ⊆ D ⊆ Q - ↑P` iff `x, y ∉ ↓V` and no
peak of `Z` is `<= w` (take `D = ↓V ∪ ↓w`); dually an upper witness is usable iff no valley of `Z` is `>= w`. Hence an
order-based way to switch a lower witness `w` off is a peak `p <= w` on the zigzag, which makes `x, y` unusable as
valleys on that zigzag; if `p` is on every zigzag, `x` and `y` can never be valleys. Every "global" switch-off by the
order therefore freezes the pair itself (`theory-dc.md` §5 observed one instance of this).

**(N3) Comparabilities are free when their forbidden combination never occurs.** A relation `y < x` forbids only
"`x` a valley and `y` a peak" (more precisely `x ∈ D ∌ y`) and needs no witness. A reduction may add every relation
whose forbidden combination occurs in no intended solution, as long as the transitive closure adds no unwanted
constraint. Two elements whose modes vary independently in the intended solutions (members of two free variables)
must be incomparable and need a witness.

**(N4) Prop 14 of `theory-dc.md` generalized as a design constraint.** If every element that can be a valley is
comparable with every element that can be a peak, the sets `N(y) = {x valley-capable : x < y}` form a chain and the
instance is polynomial. A hard family needs incomparable valley-capable/peak-capable pairs, or elements that are both
(flexible elements with lower and upper non-witness neighbours), and N1 then applies to them.

**(N5) Cross condition in 2CH + P2.** Let `X_1, ..., X_r` be a shortest sequence of picked sides from `s` to `t`
(sides at distance `>= 2` in the sequence are disjoint). For a switch `a` used in E-mode and a switch `b` used in
F-mode at non-consecutive positions, `E_a ∩ F_b = ∅`, and P2 gives: the picked `E_a` meets the unpicked `E_b`, or the
unpicked `F_a` meets the picked `F_b`. For two E-mode switches at non-consecutive positions the unpicked `F_a`, `F_b`
meet; for two F-mode switches the unpicked `E_a`, `E_b` meet. So the unpicked partner sides of a solution are tied to
each other and to the solution by many intersections.

**(N6) General ZZ in switch language.** Every middle element is a switch (`E` = lower neighbours, `F` = upper
neighbours); an `R`-edge `y x` between middle elements (`y < x`) is a node in `F_y ∩ E_x`; the order adds implications
(`y < x`: `x` in F-mode implies `y` in F-mode); P2 is required only for incomparable switches and may be met by a
*middle* witness `w` (a switch below both whose F-side meets `E_x` and `E_y`: a connector that exists only when `w` is
in F-mode). So ZZ + P2 = 2CH + implications + P2 with conditional connectors.

## 4. Rules for the agents of this round

- Read this brief, then `theory-dc.md`, `dc-algorithm.md`, `dc-hardness.md`, `dc-general.md` as needed; the
  `verify/*.md` files record what was re-checked.
- Write only your own report `open-cases/r4-<name>.md` and your own script folder `open-cases/r4-<name>/`. Save the
  report as you go (a partial report must survive an interruption). Import other folders' code read-only.
- Files in English. No edit of the manuscript, the project notes or other agents' files.
- Write Python scripts with the file-writing tool, not with shell heredocs (heredocs halve backslashes here). Stop a
  process only by its PID, never by image name.
- Python 3.13 and numpy are available; installing packages needs the author's consent, so do not install anything.
- Every claim labelled; every computation recorded with seed, size and outcome; a claimed proof must be complete
  enough for an independent check.
