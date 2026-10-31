# Round 5, agent r5-classes: 2CH with classes + P2 (target A)

Status: version 0.2 in progress, 2026-10-22, third run (first run 2026-10-19: scripts only; second run 2026-10-21:
version 0.1 = §0-§3.1 below, stopped by the author). §0-§3.1 of version 0.1 are kept; new results are added below as
they come. Scripts: `r5-classes/`, logs: `r5-classes/runs/`. Labels: **proved**, **checked**, **sketch**,
**conjecture**, **refuted**.

## 0. Results at a glance

| # | Statement | Status |
|---|---|---|
| A1-A5 | observations of the brief | proved (§2) |
| W | *Window lemma*: a side not on a shortest valid path `P` whose class is not used on `P` with the other type meets at most 3 consecutive members of `P` | proved (§2b) |
| Q | **2CH with classes + P2 is decidable in time `m^{O(log m)}`** (`m` switches): DESC with `k = ⌊log2 m⌋ + 1` neighbourhood centres and `3k` flips is complete (minimax over the P2 pairs between the switches of the two types of a shortest valid path). Hence target A is **not NP-hard unless NP ⊆ QP** (in particular not under ETH) | proved (§2b) |
| PP | Two partner neighbourhoods of far `T`-members of different classes (plus two class groups and four single sides) cover every needed `O`-side, mates included; the misclassification is `|Err(u, b)|` | proved (§2c) |

## 1. Setting

Nodes, terminals `s != t`, switches `w` with node sets `E_w`, `F_w`, partitioned into classes; a mode vector gives
every class one mode `E` or `F`, and every switch of a class picks the side of that mode. Yes-instance iff `s` and
`t` are connected in the hypergraph of the picked sides. P2 (classes): for switches `w`, `v` of different classes,
`E_w ∩ E_v != ∅` or `F_w ∩ F_v != ∅`. A *valid path* is a sequence of sides `X_1 .. X_r` with `s ∈ X_1`, `t ∈ X_r`,
`X_i ∩ X_{i+1} != ∅`, distinct switches, and no two sides of switches of one class with different types.

## 2. Observations A1-A5 of the brief

Fix a shortest valid path `P = X_1 .. X_r`; `w_a`, `C_a`, `t_a` are the switch, class and type at position `a`;
`X'_a` is the other side of `w_a` (possibly empty); `Ω(C, τ)` is the set of `τ`-sides of the switches of class `C`.

- **(A1) holds (proved).** `X_1 .. X_a X_b .. X_r` (`b >= a + 2`) is a subsequence of `P`, hence a valid path
  (validity is a condition on pairs), and shorter.
- **(A2) holds (proved).** For `C_a != C_b`, P2 gives `X_a ∩ X_b != ∅` or `X'_a ∩ X'_b != ∅` when `t_a = t_b`, and
  `X_a ∩ X'_b != ∅` or `X'_a ∩ X_b != ∅` when `t_a != t_b`; for `|a - b| >= 2` the first pair is disjoint by (A1).
- **(A3) holds (proved).** Let `Z` be an `O`-side of a switch `w` of class `C`, all positions of `C` in `(d, c)`,
  `Z ∩ X_d != ∅ != Z ∩ X_c`. In `Q = X_1 .. X_d Z X_c .. X_r` the switch `w` is at no kept position (every switch of
  `C` on `P` sits in `(d, c)`), and no kept member belongs to `C`, so `Z` conflicts with nothing; `Q` is valid and
  `|Q| = r - (c - d - 2) >= r` gives `c - d <= 2`. With `k >= 2` positions of `C` this is impossible, so the contacts
  of `Z` do not lie on both sides of the span of `C`; for `k = 1` it is Lemma 1 of r4-switch.
- **(A4) holds (proved).** If `Z` (type `T`, class `C` used with type `T`, `Z` not on `P`) met `X_d` and `X_c` with
  `c >= d + 3`, then `w_Z` is not on `P` (its `T`-side is `Z`, not on `P`, and its `O`-side cannot be on `P`), `Z`
  conflicts with nothing on `P`, and `X_1 .. X_d Z X_c .. X_r` is a shorter valid path. For a `T`-member `b` of
  another class with `Z ∩ X_b = ∅`, P2 gives `Z' ∩ X'_b != ∅` (`Z'` the `O`-side of `w_Z`).
- **(A5) holds (proved; the proof is the one of r4-switch Theorem 5 and is in `ccore.csearch`).** If `Y_i`, `Y_j`
  (`i < j`) conflict, then `Y_i ∈ Π(Y_j) ⊆ K` and `Y_j ∈ Π(Y_i) ⊆ K`, so `(class, type of Y_i)` is stored at step
  `i` and `Y_j` is refused at step `j`.

**Key Lemma K (P2 restated; proved).** Let `C` be a class, `Z` a side of type `O` of a switch `w ∈ C`, `Z'` the
`T`-side of `w` (possibly empty), and `v` a switch of another class with sides `v^O`, `v^T`. Then
`Z ∩ v^O != ∅` or `Z' ∩ v^T != ∅`. Hence `Z ∈ N_O[v^O]` unless `Z'` meets `v^T`.

## 2a. Certificates as mode descriptions (proved)

For a type `τ` and a set `U` of `τ`-sides let `σ_U` be the mode vector that puts a class `C` into mode `1 - τ` iff
`Ω(C, τ) ⊆ U`, and into mode `τ` otherwise; `σ_U^Φ` flips the classes of a set `Φ`.

**Lemma 2a.1.** Let `P` be a valid path with `T`-classes `𝒯` and `O`-classes `𝒪`, and `U` a set of `O`-sides. Then
`σ_U^Φ` with `Φ = {C ∈ 𝒯 : Ω(C, O) ⊄ U} ∪ {D ∈ 𝒪 : Ω(D, O) ⊆ U}` picks every member of `P`; so it connects `s`
and `t`. *Proof.* `σ_U` gives `C ∈ 𝒯` mode `T` iff `Ω(C, O) ⊆ U`, and `D ∈ 𝒪` mode `O` iff `Ω(D, O) ⊄ U`; `Φ` is
exactly the set of classes of `P` on which `σ_U` is wrong. ∎
The number `mis_P(U) = |Φ|` is the *misclassification* of `U`. Algorithm `DESC(f, g, e)`: for both `τ`, every `U` that
is a union of at most `f` sets `N_τ[Z]` and at most `g` class groups `Ω(C, τ)` or single sides, and every set `Φ` of at
most `e` classes, test whether `σ_U^Φ` connects `s` and `t`. It is sound for all parameters (it accepts only a
connecting mode vector) and runs in time `O((2D)^{f+g} n^e (N + D)^2)`.

**Corollary 2a.2 (switch model; proved from r4-switch).** In 2CH + P2 (every class a single switch) a `T`-certificate
of storage `S` in the sense of r4-switch §4 (a set of `O`-sides containing the partners of all `T`-members, `S`
members of `P` in it) is a set `U` with `mis_P(U) <= S`. Hence, by r4-switch Theorem 8, Lemma 7 and the remark of
`verify/r4-switch-review.md` §2.6, `DESC(6, 12, 18)` decides 2CH + P2, in time `O(D^{36} poly)` instead of
`O(D^{74})`: only one of the two certificates of Corollary 9 is needed. *Proof.* A partner `X'_a` of a `T`-member is
the only `O`-side of the singleton class `{w_a}`, so `Ω({w_a}, O) ⊆ U`; an `O`-member `c` has the single `O`-side
`X_c`, so `{w_c}` is misclassified iff `X_c ∈ U`, i.e. iff it counts in the storage. A single side in `U` that is a
partner of a `T`-member completes no `O`-class. ∎

## 2b. Theorem Q: a quasi-polynomial algorithm (proved)

Notation: `P = X_1 .. X_r` a shortest valid path, `𝒯` (`𝒪`) the classes used on `P` with type `T` (`O`). For a
switch `w` let `w^T`, `w^O` be its `T`- and `O`-side (possibly empty). A side `Y` is *`P`-consistent* if its class
is not used on `P` with the type opposite to the type of `Y`.

**Lemma W (window; proved).** If a `P`-consistent side `Y` is not on `P`, the positions `c` with `Y ∩ X_c != ∅` lie
in `{d, d + 1, d + 2}` for some `d`. *Proof.* Let `Y ∩ X_d != ∅ != Y ∩ X_c`, `c >= d + 3`. The switch `w` of `Y` is
not on `P`: if `w` sat at position `e`, then `X_e` would be the side of `w` of the type used on `P` by its class,
which is the type of `Y` (`Y` is `P`-consistent and the class is used on `P`), so `X_e = Y` would be on `P`.
`Q = X_1 .. X_d Y X_c .. X_r` has `s` in the first and `t` in the last side, consecutive sides meet, its switches are
distinct, and `Y` conflicts with no kept member (its class is used on `P` only with the type of `Y`, if at all);
so `Q` is a valid path of length `r - (c - d - 2) < r`, a contradiction. ∎
For a member `X_q` the same holds by (A1): only `X_{q-1}, X_q, X_{q+1}` meet it. A4 of the brief is the case of a
`T`-side of a mate of a `T`-class.

**Lemma D (duality; proved).** Let `w` be a switch of a class of `𝒯` and `v` a switch of a class of `𝒪`. Then
`w^O ∩ v^O != ∅` or `w^T ∩ v^T != ∅`. *Proof.* P2 for `w`, `v` (different classes: one class is used with `T`, the
other with `O`); the two pairs of P2 are the `O`-sides and the `T`-sides. ∎
Here `w^O` is a side the `T`-certificate must contain (a *needed* `O`-side, partner or mate side) and `v^O` is a
`P`-consistent side; dually `v^T` is needed by the `O`-certificate and `w^T` is `P`-consistent.

**Theorem Q (proved).** Let `m` be the number of switches and `k = ⌊log2 m⌋ + 1`. Every yes-instance of 2CH with
classes + P2 has a type `τ`, sides `Y_1, .., Y_k` and a set `Φ` of at most `3k` classes such that `σ_U^Φ`, with
`U = N_τ[Y_1] ∪ .. ∪ N_τ[Y_k]`, connects `s` and `t` (`σ_U`, `σ_U^Φ` as in §2a). Hence DESC(`k`, 0, `3k`), which
tests all these mode vectors, decides 2CH with classes + P2 in time `O((2m + 1)^k (m + 1)^{3k} · (N + m)^2)`, i.e.
`m^{O(log m)}` for instances with `N <= poly(m)` nodes.

*Proof.* Take a shortest valid path `P` and a type `T` (either). Let `W*` be the switches of `𝒯`-classes with
`w^O != ∅` and `V*` the switches of `𝒪`-classes with `v^T != ∅`; `Ω(C, O) = {w^O : w ∈ C ∩ W*}` for `C ∈ 𝒯` and
`Ω(D, T) = {v^T : v ∈ D ∩ V*}` for `D ∈ 𝒪`. If `W*` is empty, `U = ∅` with `τ = O` gives `σ_∅`, which puts a
class into mode `T` iff it has no `O`-side; every `𝒯`-class then goes to `T` and every `𝒪`-class (it has an
`O`-member) to `O`, so `σ_∅` picks `P`. Likewise if `V*` is empty (with `τ = T`). Otherwise consider the zero-sum game
with rows `v ∈ V` (all switches of `𝒪`-classes), columns `w ∈ W*` and payoff `M[v][w] = 1` if `v^O ∩ w^O != ∅`, else
0, with value `λ` (von Neumann).
*Case `λ >= 1/2`.* Some distribution `p` on `V` has `Pr_{v~p}[v^O ∩ w^O != ∅] >= 1/2` for every `w ∈ W*`. Draw
`v_1, .., v_k` independently from `p`; a fixed `w` is missed by all with probability `<= 2^{-k} < 1/m`, so some
draw meets every `w^O`, `w ∈ W*`. Put `τ = O`, `Y_i = v_i^O` (an empty `Y_i` contributes nothing). Then
`Ω(C, O) ⊆ U` for every `C ∈ 𝒯`, so `σ_U` puts every `𝒯`-class into mode `T`. Each `Y_i` is `P`-consistent (an
`O`-side of an `𝒪`-class), so by Lemma W (or (A1) if `Y_i` is a member) `N_O[Y_i]` contains at most 3 members of
`P`. A class `D ∈ 𝒪` is put into mode `T` by `σ_U` only if `Ω(D, O) ⊆ U`, in particular only if a member of `P` of
class `D` lies in `U`; so at most `3k` classes of `𝒪` are misclassified. With `Φ` = these classes, `σ_U^Φ` picks
every member of `P` (Lemma 2a.1) and connects `s`, `t`.
*Case `λ < 1/2`.* Some distribution `q` on `W*` has `Pr_{w~q}[v^O ∩ w^O != ∅] < 1/2` for every `v ∈ V`; by Lemma D
`Pr_{w~q}[w^T ∩ v^T != ∅] > 1/2` for every `v ∈ V`, in particular for `v ∈ V*`. Draw `w_1, .., w_k` from `q`;
some draw meets every `v^T`, `v ∈ V*`. Put `τ = T`, `Y_i = w_i^T`: `σ_U` puts every `𝒪`-class into mode `O`
(`Ω(D, T) ⊆ U`), each `Y_i` is `P`-consistent, `N_T[Y_i]` contains at most 3 members of `P`, at most `3k` classes
of `𝒯` are misclassified, and `σ_U^Φ` picks `P`.
*Algorithm.* DESC(`k`, 0, `3k`) tries both `τ`, every union of at most `k` sets `N_τ[Z]` (`Z` any of the at most
`2m` sides) and every set of at most `3k` classes to flip, and tests connectivity of the picked hypergraph; it
accepts only connecting mode vectors (sound), and by the above it accepts every yes-instance. ∎

**Corollary Q.** If 2CH with classes + P2 is NP-hard, then NP ⊆ DTIME(`2^{O(log^2 n)}`) (quasi-polynomial time),
which contradicts the Exponential Time Hypothesis. So target A cannot give NP-hardness of the open case of DC unless
NP ⊆ QP; with Theorem R of `r4-general.md` (§8, reviewed: holds) and its ties version (§9.1), every ZZ + P2 instance
whose sound fixing leaves only ties among the free switches is decided in quasi-polynomial time. *Proof.* A
polynomial reduction from 3-SAT followed by Theorem Q decides 3-SAT in time `n^{O(log n)}`. ∎

Remarks. (1) The argument does not use Lemma 1, critical runs or straddles: the duality of Lemma D between the two
certificates and the window bound of Lemma W suffice. It also gives a new (quasi-polynomial) proof for 2CH + P2.
(2) The `log m` comes only from the sampling; a polynomial bound needs a bounded number of centres, which the minimax
argument alone cannot give (random bipartite tournaments need `Θ(log m)` dominators on both sides). §3 and §4 study
whether the structure of shortest paths excludes such tournaments.

## 2c. Lemma PP: partner pairs cover mates (proved)

For a `T`-member `u` let `Err(u, b)` (`b` another `T`-member) be the set of classes `D ∈ 𝒪` all of whose `O`-sides
meet `X'_u` or `X'_b`.

**Lemma PP.** Let `u`, `b` be `T`-members with `cls(u) != cls(b)` and `|u - b| >= 3`, and
`U = N_O[X'_u] ∪ N_O[X'_b] ∪ Ω(cls(u), O) ∪ Ω(cls(b), O) ∪ {X'_a : a ∈ {u ± 1, b ± 1} a T-member}`. Then
`Ω(C, O) ⊆ U` for every `C ∈ 𝒯`, and `σ_U` misclassifies exactly the classes of `Err(u, b)` (none of `𝒯`).
*Proof.* Let `Z = w^O`, `w ∈ C ∈ 𝒯`, `C ∉ {cls(u), cls(b)}`. If `w` sits on `P` at `a`: for `|a - u| >= 2`, P2 for
`w`, `w_u` (same type `T` on `P`, `X_a ∩ X_u = ∅` by A1) gives `X'_a ∩ X'_u != ∅`; for `|a - u| = 1`, `X'_a` is one
of the single sides. If `w` is a mate: P2 for `w`, `w_u` gives `w^T ∩ X_u != ∅` or `Z ∩ X'_u != ∅`, and likewise
for `b`; `w^T` cannot meet both `X_u` and `X_b` (Lemma W, `|u - b| >= 3`), so `Z` meets `X'_u` or `X'_b`. The class
groups and single sides contain only `O`-sides of `𝒯`-classes, so a class `D ∈ 𝒪` has `Ω(D, O) ⊆ U` iff every
`O`-side of `D` meets `X'_u` or `X'_b`. ∎
Hence DESC(2, 6, `e`) accepts whenever some shortest valid path and type have such a pair with `|Err(u, b)| <= e`;
if no such pair exists for `T`, at most 3 classes are used with `T` (all `T`-members at distance `>= 3` from the
first one share its class) and 3 class groups give misclassification 0.

## 3. Structure theory of shortest valid paths with classes

(in progress)

### 3.1 What a certificate must cover with classes: the mates

For a `T`-class `C` every `O`-side of every switch of `C` must lie in a `T`-cover, not only the partners of the
members of `C` on `P`. Call a switch of a class of `P` that is not on `P` a *mate*. By Key Lemma K a mate's `O`-side
`Z` lies in `N_O[X_q]` (`q` an `O`-member) unless the mate's `T`-side `Z'` meets `X'_q`, and in `N_O[X'_b]` (`b` a
`T`-member of another class) unless `Z'` meets `X_b`. A *dead mate* (`Z'` meets no member of `P` but meets every
`X'_q`) is therefore covered by no `O`-member neighbourhood; it is covered by `N_O[X'_b]` for every `T`-member `b` of
another class, whose cost is the number of `O`-classes all of whose `O`-sides meet `X'_b`. The partner
neighbourhoods of the members are what Theorem 8 of r4-switch avoids in its step (3); so classes need a statement
r4-switch did not need:

**Hypothesis H (switch model).** In every shortest valid path of a 2CH + P2 instance some member `u` has
`|f(u)| <= c` (`f(u)` = members of the other type meeting `X'_u`), for an absolute constant `c`.

*Checked* (`hyp_h.py`, hill climbing on abstract planted paths realised with private nodes, P2 and shortest-path
property verified exactly by `ccore.shortest_valid_paths`; objective: maximise the least `|f(u)|`): seeds 1-6,
`r = 8, 12, 16, 20`, 24 runs of 300-3000 steps (`runs/hyp-h-*.txt`): the least `|f(u)|` reached is 2 in 13 runs and
1 in 11; never 3.

## 4. Attacks: families, reductions

(in progress)

## 5. Checks (script, seed, size, outcome)

| What | Script and arguments | Instances | Outcome |
|---|---|---|---|

## 6. Scripts (`r5-classes/`)

| Script | What |
|---|---|
| `ccore.py` | instances with classes, P2 check, brute force, exact search, all shortest valid paths, class certificate search (`csearch`), forced-exit propagation, probing, contraction, blob normal form, generators (first run) |
| `cdecide.py` | certificate shapes, `decide`, search with class declarations, guided certificate costs (first run) |
| `cfam.py` | rigid word family `R(W)` with tied mates (`ytie`) (first run) |
| `branchfam.py` | `Y_k` with tied mates and decoy branchings at both terminals (`ybranch`, `ybranch_fake`) (first run) |
| `cdesc.py` | bounded-description mode vectors (first run) |
