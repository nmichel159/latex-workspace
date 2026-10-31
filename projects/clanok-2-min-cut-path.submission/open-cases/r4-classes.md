# Agent r4-classes (continuation of r4-switch): the switch model with classes (ties) + P2

Status: version 0.1, started 2026-10-22. Scripts: `r4-classes/`, logs: `r4-classes/runs/`. Labels: **proved**,
**checked**, **sketch**, **conjecture**, **refuted**. Task (coordinator): decide the complexity of 2CH with classes +
P2 (switches grouped into classes forced into one mode; P2 only between switches of different classes), the part of
the open case that Theorem R of `r4-general.md` reduces to but cannot reduce further.

Relation to round 5: the agent r5-classes works on the same problem (target A of `r5-brief.md`); its report
`r5-classes.md` (version 0.2 in progress, read 2026-10-22) proves **Theorem Q: 2CH with classes + P2 is decidable in
time `m^{O(log m)}`** (minimax over the P2 pairs, Lemma W, Lemma D), hence not NP-hard unless NP ⊆ QP. This report
builds on that result (cited, re-read here, code imported read-only) and does not repeat it.

## 0. Results at a glance

(filled in as the work proceeds)

## 1. Setting and notation

Nodes, terminals `s != t`, switches `w` with node sets `E_w`, `F_w`, a partition of the switches into classes; a mode
vector gives every class one mode, every switch picks the side of its class's mode; yes-instance iff `s`, `t` are
connected in the hypergraph of the picked sides. P2: switches of different classes have meeting `E`-sets or meeting
`F`-sets. A *valid path* `X_1 .. X_r`: sides (non-empty), `s ∈ X_1`, `t ∈ X_r`, consecutive sides meet, distinct
switches, no two sides of switches of one class with different types. Yes iff a valid path exists (a shortest
sequence of picked sides is one; conversely the sides of a valid path are picked by one mode vector). For a shortest
valid path `P` and a type `T` (`O` the other type): `𝒯`, `𝒪` = classes used on `P` with type `T`, `O`; a *mate* is a
switch of a class of `P` that is not on `P`; `Ω(C, τ)` = the `τ`-sides of the switches of `C`; `w^τ` = the `τ`-side
of `w` (possibly empty).

## 2. Where the difficulty is (analysis; labels per item)

**2.1 Reduction of the question to one hypothesis (proved from r5-classes Lemma PP).** By Lemma PP of r5-classes, if
some shortest valid path `P` and type `T` have `T`-members `u`, `b` of different classes with `|u - b| >= 3`, then
`U = N_O[X'_u] ∪ N_O[X'_b] ∪ Ω(cls(u), O) ∪ Ω(cls(b), O) ∪ {at most 4 single sides}` covers every needed `O`-side,
mates included, and `σ_U` misclassifies only the classes of `Err(u, b)`, all of whose `O`-sides meet `X'_u` or `X'_b`;
such a class has all its `O`-members in `f(u) ∪ f(b)`, so `|Err(u, b)| <= |f(u) ∪ f(b)|`. Hence:

> **Hypothesis P.** There is a constant `c` such that every shortest valid path `P` of every 2CH-with-classes + P2
> instance has a type `T` with either all `T`-members in at most 3 classes, or two `T`-members `u`, `b` of different
> classes, `|u - b| >= 3`, with `|f(u) ∪ f(b)| <= c`.

implies that DESC(2, 6, `c`) of r5-classes decides 2CH with classes + P2 in polynomial time (if all `T`-members lie
in at most 3 classes, 3 class groups give misclassification 0, r5-classes §2c). Hypothesis P is about the members of
`P` only; mates do not enter it. It is the class version of Hypothesis H2 of r5-classes.

**2.2 Why the obvious lower-bound families fail (checked).** A family on which DESC needs `Ω(log m)` centres must
make every partner neighbourhood expensive on both types (all `|f|` large) and add dead mates with a random mate
tournament (r5-classes `tourn.py`). In the switch model this is impossible in all instances tested (§3). With
multi-position classes (round robin `(C_1 .. C_K)^R`, where Lemma 1 of r4-switch fails) I tried to make every partner
meet all members of all opposite-type classes on one side (`r4-classes/lbfam.py`): the planted path is then not
shortest (`lbtest.py`: `K = 6, 8`, `R = 2`: shortest length 5-6 instead of 12-16; shortcuts use partners of two
classes chained through a partner–partner node (forced by P2), or fold the round robin through two members of one
class that a partner meets in different rounds). Dense contacts of partners create shortcuts; this is the same
mechanism as the straddles of r4-switch and supports Hypothesis P.
