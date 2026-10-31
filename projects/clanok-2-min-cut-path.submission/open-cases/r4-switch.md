# Round 4, agent r4-switch: complexity of the switch model 2CH + P2

Status: version 2, 2026-10-18 (version 1 of 2026-10-17 had the same results; this version writes every case of the
proofs out, records the checks with script, seed and count, and states the running time). Scripts: `r4-switch/`,
logs: `r4-switch/runs/`. Labels: **proved**, **checked**, **sketch**, **conjecture**, **refuted**.

## 0. Results at a glance

**Verdict.** 2CH + P2 (the switch model of the open case of DC) is decidable in polynomial time (Theorem 10); the
proven bound is `O(D^{122})` for `D` sides, i.e. polynomial but not practical, while a small-parameter variant of the
same algorithm agreed with brute force on every instance tested.

| # | Statement | Status |
|---|---|---|
| F1-F4 | Basic facts on a shortest valid path (disjointness, partners of same-type members meet, cross condition, replacement) | proved (§2) |
| L1-L3 | Partners have one-sided contacts; forward partners before backward ones; domination through cross pairs | proved (§2) |
| T4 | Outside one maximal run of one type (the *critical run*), the partners of that type are dominated by two members | proved (§2) |
| T5 | Side-set certificates: for every set `K` of sides the search accepts only valid walks; it accepts whenever some valid path has its partners in `K` and at most `B` members in `K` | proved (§3) |
| L7 | A *straddle* of a shortest path is tight; the swap gives a shortest path with a certificate of 2 neighbourhood sets, 4 single sides, storage 6 | proved (§4) |
| T8 | A shortest valid path without straddle has, per type, a certificate of at most 10 neighbourhood sets and 20 single sides, storage at most 30 | proved (§4) |
| T10 | **2CH + P2 is in P**, time `O(D^{122})` (`D` = number of sides `<= 2n`) | proved (§4) |
| T11 | Search with declarations is sound (used by the practical variant) | proved (§3) |
| Checks | every proof step asserted on all 4,145,828 shortest valid paths of all 2CH + P2 instances with 3-4 nodes and 2-3 switches, and on 20,719 shortest paths of random, planted, saturated and straddle instances (44 swaps); the certificate of the proof is accepted by the search in every case; `decide_full` agrees with brute force on 1,500 instances; the practical variant (`kd = 1`, `ks = 1`, `s = 4`, `B = 8`) on 2,586 instances and on `R_L`, `L <= 14`, and its variants | checked (§6) |
| Open | general ZZ + P2 (ties, one-way comparabilities, middle edges, middle witnesses), i.e. the open case of DC itself; whether PC decides 2CH + P2; a smaller exponent | open (§7) |

## 1. Setting

An instance consists of a finite set of nodes, terminals `s != t` (for `s = t` the answer is yes), and switches `w`,
each with two node sets `E_w`, `F_w` (possibly empty). A *side* is a pair (switch, type) with type `E` or `F` whose
node set is non-empty; sides of different switches are different sides even if their node sets coincide. The
*partner* `X'` of the side `X` is the other side of its switch, or *empty* if that node set is empty. `D` is the
number of sides (`D <= 2n`, `n` switches). P2: for distinct switches `w`, `v`, `E_w ∩ E_v != ∅` or `F_w ∩ F_v != ∅`.

A *valid path* is a sequence of sides `X_1 .. X_r` with `s ∈ X_1`, `t ∈ X_r`, `X_i ∩ X_{i+1} != ∅`, whose switches are
pairwise distinct. The instance is a yes-instance (some mode vector connects `s` and `t` in the hypergraph of picked
sides) iff a valid path exists: a shortest sequence of picked sides from `s` to `t` uses each switch at most once
(each switch has one picked side, and a repeated side would shorten the sequence); conversely the sides of a valid
path belong to distinct switches and are picked by one mode vector. A *valid walk* is a sequence of sides with `s` in
the first, `t` in the last, consecutive sides equal or meeting, and no two sides that are partners; its sides are
picked by one mode vector that connects `s` and `t`, so a valid walk also certifies a yes-instance.

## 2. Structure of a shortest valid path (all proved)

Fix a shortest valid path `P = X_1 .. X_r`; `w_a` is the switch at position `a`, `X'_a` its partner. Position `a` is
a *T-member* (`T ∈ {E, F}`) if `X_a` has type `T`; `O` always denotes the other type. A position `c != a` is a
*contact* of `a` if `X'_a ∩ X_c != ∅` (an empty partner has no contacts).

**(F1)** `X_a ∩ X_b = ∅` for `|a - b| >= 2`. *Proof.* For `a < b`, `X_1 .. X_a X_b .. X_r` would be a shorter valid
path. ∎
**(F2)** If `a`, `b` have the same type and `|a - b| >= 2`, then `X'_a`, `X'_b` are non-empty and meet. *Proof.* P2 for
`w_a != w_b`: of the two pairs `{E_a, E_b}`, `{F_a, F_b}` one is `{X_a, X_b}`, disjoint by (F1); the other is
`{X'_a, X'_b}`. ∎
**(F3)** If `a`, `b` have opposite types and `|a - b| >= 2`, then `X'_a ∩ X_b != ∅` or `X_a ∩ X'_b != ∅`. *Proof.* The
two pairs of P2 are `{X_a, X'_b}` and `{X'_a, X_b}`. ∎
**(F4) Replacement.** Let `1 <= d < c <= r`, `k >= 1`, and `Y_1 .. Y_k` sides with `Y_1 ∩ X_d != ∅`,
`Y_i ∩ Y_{i+1} != ∅`, `Y_k ∩ X_c != ∅`, whose switches are pairwise distinct and none of `w_1 .. w_d, w_c .. w_r`.
Then `X_1 .. X_d Y_1 .. Y_k X_c .. X_r` is a valid path, so `k >= c - d - 1`. *Proof.* The terminals, the meeting of
consecutive sides and the distinctness of switches are immediate; its length `d + k + r - c + 1` is at least `r`. ∎

**Lemma 1 (one-sided contacts).** If `d < a < c` are contacts of `a`, then `d = a - 1` and `c = a + 1`.
*Proof.* (F4) with `k = 1`, `Y_1 = X'_a` (its switch `w_a` has position `a` strictly between `d` and `c`):
`1 >= c - d - 1`, so `c - d <= 2`. ∎
Hence each position `a` is of exactly one *kind*: *forward* (some contact `>= a + 2`; then every contact is
`>= a + 1`), *backward* (some contact `<= a - 2`; then every contact is `<= a - 1`), or *local* (all contacts in
`{a - 1, a + 1}`; this includes an empty partner). A contact `<= a - 1` and one `>= a + 2` cannot coexist by Lemma 1,
which gives the parentheses and the exclusiveness.

**Lemma 2 (forward before backward).** (a) If `a` is forward, `b < a` and `X'_a ∩ X'_b != ∅`, then `b` has no contact
`< b`. (b) If `a` is backward, `b > a` and `X'_a ∩ X'_b != ∅`, then `b` has no contact `> b`.
*Proof.* (a) Let `d < b` be a contact of `b` and `c >= a + 2` a contact of `a`. Then `d < b < a < c`, and (F4) with
`Y_1 = X'_b`, `Y_2 = X'_a` gives `2 >= c - d - 1 >= (a + 2) - (b - 1) - 1 = a - b + 2 >= 3`, a contradiction.
(b) Let `d > b` be a contact of `b` and `c <= a - 2` a contact of `a`. Then `c < a < b < d`, and (F4) between `X_c`
and `X_d` with `Y_1 = X'_a`, `Y_2 = X'_b` gives `2 >= d - c - 1 >= (b + 1) - (a - 2) - 1 = b - a + 2 >= 3`. ∎

**Lemma 3 (domination by cross pairs).** Let `a` be a `T`-member, `q` an `O`-member, `|a - q| >= 2`, and `a` not a
contact of `q`. Then `X'_a ∩ X_q != ∅`. *Proof.* By (F3), `X'_a ∩ X_q != ∅` or `X_a ∩ X'_q != ∅`; the second says
that `a` is a contact of `q`. ∎

**Theorem 4 (critical run).** Fix `T`, and assume that no `O`-member is local and that some `O`-member exists. Let
`q_f` be the largest forward `O`-member (`q_f = -∞` if none) and `q_b` the smallest backward `O`-member (`+∞` if none).
(a) If both are finite, `q_b >= q_f - 1`.
(b) Every `T`-member `a <= q_f - 2` has `X'_a ∩ X_{q_f} != ∅`; every `T`-member `a >= q_b + 2` has
`X'_a ∩ X_{q_b} != ∅`.
(c) Every position `c` with `q_f < c < q_b` is a `T`-member. These positions form the *critical run* `R`.
*Proof.* (a) `q_b != q_f` since kinds are exclusive. If `q_b <= q_f - 2`, the `O`-members `q_b`, `q_f` have meeting
partners (F2), `q_f` is forward and `q_b < q_f`, so by Lemma 2(a) `q_b` has no contact `< q_b`, contradicting that
it is backward. (b) The contacts of the forward `q_f` are `>= q_f + 1`, so `a <= q_f - 2` is not a contact; Lemma 3.
The contacts of the backward `q_b` are `<= q_b - 1`, so `a >= q_b + 2` is not a contact; Lemma 3. (c) An `O`-member
`c` with `q_f < c < q_b` is not forward (`c > q_f`), not backward (`c < q_b`) and not local (assumption). ∎

## 3. The search with side-set certificates (proved)

**Theorem 5.** Let `K` be a set of sides and `B >= 0`. Call a walk `Y_1 .. Y_m` (sides, `s ∈ Y_1`, `t ∈ Y_m`,
consecutive sides equal or meeting) *K-admissible* if for every `j`:
(i) `Y'_j` is empty or lies in `K`; (ii) `Y'_j ∉ {Y_1, .., Y_{j-1}} ∩ K`; and (iii) `|{Y_1, .., Y_m} ∩ K| <= B`.
(1) *Soundness.* A K-admissible walk is a valid walk; in particular the instance is a yes-instance.
(2) *Completeness.* If `P` is a valid path whose non-empty partners all lie in `K` and `|P ∩ K| <= B`, then `P` is
K-admissible.
(3) *Search.* Whether a K-admissible walk exists is decided by a breadth-first search over the states
`(Y_j, {Y_1, .., Y_j} ∩ K)` in time `O(B · D^{B+2})` (at most `D (D + 1)^B` states, at most `D` transitions each).
*Proof.* (1) Suppose `Y_i`, `Y_j` (`i < j`) are partners. Both are non-empty, so by (i) `Y_j = Y'_i ∈ K` and
`Y_i = Y'_j ∈ K`; then `Y'_j = Y_i ∈ {Y_1, .., Y_{j-1}} ∩ K`, contradicting (ii) at `j`. (2) (i) holds by assumption,
(ii) because a valid path contains no two partner sides, (iii) by assumption. (3) Conditions (i), (ii) at step `j`
and the update of `{..} ∩ K` depend only on `Y_j` and the stored set; (iii) bounds the stored sets. ∎
Theorem H of dc-hardness.md is the special case in which `K` is a union of node stars.

**Theorem 11 (declarations; proved, used only by the practical variant).** Fix `K`, `B`, `s`. Walk states carry
`St` (members lying in `K`) and `Dc` (*declared* sides). `Y` may be appended iff `Y ∉ Dc`, `Y' ∉ St`, and either `Y'`
is empty, `Y' ∈ K`, `Y' ∈ Dc`, or (`Y ∉ K`, `|Dc| < s`; then `Y'` is added to `Dc`); if `Y ∈ K` it is added to `St`
(`|St| <= B`). Every accepted walk is a valid walk.
*Proof.* Let `X` (first used at step `i`) and `X'` (first used at step `j > i`) both occur. If `X'` was added to `Dc`
at step `i` (only an occurrence of `X` adds `X'`), `X'` is refused at step `j`. Otherwise `X' ∈ K` (the other
alternatives at step `i` are `X'` empty, impossible, or `X' ∈ Dc`, which needs an earlier occurrence of `X`). At step
`j`, `X'` cannot declare (it lies in `K`), and `X ∉ Dc` (only an occurrence of `X'` adds `X`); so `X ∈ K`, `X` was put
into `St` at step `i`, and `X'` is refused because `X'' = X ∈ St`. ∎

## 4. Certificates exist: 2CH + P2 is in P (proved)

Notation for a shortest valid path `P`. For a `T`-member `a`, `f(a)` is the set of `O`-members `c` with
`X'_a ∩ X_c != ∅`. For a side `Z` and a type `O`, `N_O[Z]` is the set of sides of type `O` that meet `Z` (it contains
`Z` if `Z` has type `O`). A *T-certificate* of `P` is a set of `O`-sides containing the non-empty partners of all
`T`-members; its *storage* is the number of members of `P` in it. Three facts:
(S1) a single side `{X'_a}` adds no storage, since `P` contains no partner of its members;
(S2) for a member `X_c`, `N_O[X_c]` contains at most 3 members of `P` (positions `c - 1, c, c + 1`, by (F1));
(S3) for a `T`-member `a` with non-empty partner, the members of `P` in `N_O[X'_a]` are exactly the `X_c`, `c ∈ f(a)`
(a member in `N_O[X'_a]` has type `O`, so it is not `X_a`).
A *certificate* of `P` is a pair (`E`-certificate, `F`-certificate); by Theorem 5(2) the search with `K` = their union
and `B` = total storage accepts.

**Definition (straddle).** A *T-straddle* of `P` consists of a `T`-member `x`, an `O`-member `p`, `T`-members
`x_1 < x < x_2` with `X'_p ∩ X_{x_1} != ∅` and `X'_p ∩ X_{x_2} != ∅`, and `O`-members `p_1 < p < p_2` with
`X'_x ∩ X_{p_1} != ∅` and `X'_x ∩ X_{p_2} != ∅`, such that `x_2 < p_1` or `p_2 < x_1`.

**Lemma 7 (swap).** If `P` has a `T`-straddle, then `x_2 = x + 1`, `x_1 = x - 1`, `p_2 = p + 1`, `p_1 = p - 1`, and
the sequence `P*` obtained from `P` by putting `X'_p` at position `x` and `X'_x` at position `p` is a shortest valid
path. `P*` has the `T`-certificate `K*_T = N_O[X_p] ∪ {partners of the T-members of P* at x - 1 and x + 1}` and the
`O`-certificate `K*_O = N_T[X_x] ∪ {partners of the O-members of P* at p - 1 and p + 1}`, each of storage at most 3.
*Proof.* Let `M = {1..r} \ ((x_1, x_2) ∪ (p_1, p_2))` (open intervals). If `x_2 < p_1`, let `Q` be
`X_1 .. X_{x_1}, X'_p, X_{x_2} .. X_{p_1}, X'_x, X_{p_2} .. X_r`; if `p_2 < x_1`, let `Q` be
`X_1 .. X_{p_1}, X'_x, X_{p_2} .. X_{x_1}, X'_p, X_{x_2} .. X_r`. In both cases `Q` consists of the `X_c`, `c ∈ M`, and
`X'_p`, `X'_x`. `1`, `r ∈ M` (the endpoints `x_1, p_1 >= 1` and `x_2, p_2 <= r` are not removed), so `s`, `t` are in
the first and last side. Consecutive sides meet: inside `M` they are consecutive in `P`, and the four new junctions
are the four assumed intersections. Switches: those of `X_c`, `c ∈ M`, are distinct; `w_p` and `w_x` are distinct
from each other and, because `p ∈ (p_1, p_2)` and `x ∈ (x_1, x_2)`, from every `w_c`, `c ∈ M`. So `Q` is a valid
path of length `|M| + 2 = r - (x_2 - x_1 - 2) - (p_2 - p_1 - 2)`. Both brackets are `>= 0`, and `|Q| >= r`, so both
vanish: `x_2 = x_1 + 2`, `p_2 = p_1 + 2`, hence `x_1 = x - 1`, `x_2 = x + 1`, `p_1 = p - 1`, `p_2 = p + 1`, and `Q = P*`
is a shortest valid path.
Members of `P*`: `Y_c = X_c` for `c ∉ {x, p}`, `Y_x = X'_p` (type `T`, as `X_p` has type `O`), `Y_p = X'_x` (type `O`);
so every position keeps its type, and the partners are `Y'_x = X_p`, `Y'_p = X_x`, `Y'_c = X'_c` otherwise. (F1) and
(F2) hold for `P*` because it is a shortest valid path.
*The T-certificate.* Let `c` be a `T`-member of `P*` with non-empty partner. If `|c - x| >= 2`, (F2) for `P*` gives
`Y'_c ∩ Y'_x = Y'_c ∩ X_p != ∅`, and `Y'_c` has type `O`, so `Y'_c ∈ N_O[X_p]`. If `c = x`, `Y'_x = X_p ∈ N_O[X_p]`.
If `c = x ± 1`, `Y'_c` is one of the two single sides. Storage: a member of `P*` in `N_O[X_p]` has type `O` and meets
`X_p`; `Y_x` has type `T`; `Y_c = X_c` (`c ∉ {x, p}`) meets `X_p` only if `|c - p| <= 1` by (F1) for `P`; `Y_p` may
meet it. So only positions `p - 1, p, p + 1` count: storage `<= 3`; the single sides add nothing (S1 for `P*`).
*The O-certificate.* Let `c` be an `O`-member of `P*` with non-empty partner. If `|c - p| >= 2`, (F2) for `P*` gives
`Y'_c ∩ Y'_p = Y'_c ∩ X_x != ∅`, and `Y'_c` has type `T`, so `Y'_c ∈ N_T[X_x]`. If `c = p`, `Y'_p = X_x ∈ N_T[X_x]`.
If `c = p ± 1`, single side. Storage: a member of `P*` in `N_T[X_x]` has type `T` and meets `X_x`; `Y_p` has type `O`;
`Y_c = X_c` (`c ∉ {x, p}`) meets `X_x` only if `|c - x| <= 1`; `Y_x` may meet it. So positions `x - 1, x, x + 1`:
storage `<= 3`. ∎

**Theorem 8 (bounded certificate without straddle).** Let `P` be a shortest valid path without straddle (of either
type). For each type `T`, `P` has a `T`-certificate that is the union of at most 10 sets `N_O[Z]` (`Z` a side) and at
most 20 single sides, of storage at most 30.
*Proof.* Fix `T`. The steps are tried in order; the first that applies gives the certificate.

*(0) Some `T`-member `a` has an empty partner.* If `b` is a `T`-member with `|b - a| >= 2`, (F2) says that `X'_a` is
non-empty, a contradiction. So every `T`-member lies in `{a - 1, a, a + 1}`; take the non-empty partners of the
`T`-members `a ± 1` as single sides. Storage 0.
From now on every `T`-member has a non-empty partner.

*(1) Some `T`-member `a` has `|f(a)| <= 3`.* Take `N_O[X'_a]` and, as single sides, the partners of the `T`-members
`a ± 1`. A `T`-member `b` with `|b - a| >= 2` has `X'_b ∩ X'_a != ∅` (F2) and `X'_b` of type `O`, so
`X'_b ∈ N_O[X'_a]`; `X'_a ∈ N_O[X'_a]`. Storage `|f(a)| <= 3` by (S3).
From now on `|f(a)| >= 4` for every `T`-member `a`; in particular no `T`-member is local (a local position has at
most the 2 contacts `a ± 1`).

*(2) Some `O`-member `q` is local.* Take `N_O[X_q]` and the partners of the `T`-members `q ± 1`. A `T`-member `a` with
`|a - q| >= 2` is not a contact of `q` (contacts of `q` lie in `{q - 1, q + 1}`), so `X'_a ∈ N_O[X_q]` by Lemma 3.
Storage `<= 3` (S2).
If there is no `O`-member at all, `f(a) = ∅` and step (1) applied; so from now on Theorem 4 applies, with `q_f`,
`q_b` and the critical run `R`.

*(3) The general case.* Take `N_O[X_{q_f}]` (if `q_f` is finite), `N_O[X_{q_b}]` (if finite), and the partners of the
`T`-members `q_f - 1`, `q_b + 1` as single sides. By Theorem 4(b) these cover every `T`-member `a <= q_f - 2` or
`a >= q_b + 2`. A `T`-member with `q_f - 1 <= a <= q_b + 1` is `q_f - 1`, `q_b + 1` or lies in `R` (the positions
`q_f`, `q_b` are `O`-members). Every `a ∈ R` is forward or backward (no `T`-member is local); let `R→`, `R←` be the
forward and the backward ones.

*(3→) Forward rows.* Let `C = {O-members c : c >= q_b}` and `A = R→ \ {q_b - 1}`; add the partner of `q_b - 1` as a
single side if `q_b - 1 ∈ R→`. For `p ∈ C` let `b(p) = {y ∈ R : X'_p ∩ X_y != ∅}`.
(F0) *For `a ∈ A`: `f(a) ⊆ C`, and `p >= a + 2` for `p ∈ C`.* The contacts of the forward `a` are `>= a + 1`; the
positions from `a + 1` to `q_b - 1` (or to `r` if `q_b = +∞`) lie in `R` and are `T`-members, so every `O`-member
`>= a + 1` lies in `C`. As `a ∈ R`, `a != q_b - 1`, we have `a <= q_b - 2 <= p - 2`.
(Since `|f(a)| >= 4`, `A != ∅` implies that `q_b` is finite.)
(F1→) *For `a ∈ A`, `p ∈ C`: `p ∈ f(a)` or `a ∈ b(p)`.* (F3) for the pair `a`, `p` (opposite types, `|a - p| >= 2`):
`X'_a ∩ X_p != ∅` or `X_a ∩ X'_p != ∅`, and `a ∈ R`.
The *span* of `a ∈ A` is the integer interval `[min f(a), max f(a)]`; `p ∈ C` is a *hole* of `a` if
`min f(a) < p < max f(a)` and `p ∉ f(a)`.
(F2→) *If `a ∈ A`, `p ∈ C`, `min f(a) < p < max f(a)` and `b(p)` contains `y_1 < a < y_2`, then `P` has a
`T`-straddle.* Take `x = a`, `x_1 = y_1`, `x_2 = y_2` (`T`-members, as `R` consists of `T`-members, with `X'_p`
meeting `X_{x_1}`, `X_{x_2}`), `p_1 = max{c ∈ f(a) : c < p}`, `p_2 = min{c ∈ f(a) : c > p}` (`O`-members with
`X'_a` meeting `X_{p_1}`, `X_{p_2}`). As `x_2 ∈ R` and `p_1 ∈ C`, `x_2 < q_b <= p_1`.
(F3→) *Each `p ∈ C` is a hole of at most two elements of `A`.* If `p` is a hole of `a`, then `p ∉ f(a)`, so
`a ∈ b(p)` (F1→); as there is no straddle, (F2→) shows that `b(p)` has no elements on both sides of `a`, so `a` is the
least or the largest element of `b(p)`.
(F4→) *No five elements of `A` have pairwise disjoint spans.* Suppose `a_1, .., a_5` do, numbered so that the spans
lie in this order from left to right. By the Erdős–Szekeres theorem (every sequence of more than `(k - 1)(l - 1)`
distinct numbers has an increasing subsequence of length `k` or a decreasing one of length `l`; here `k = l = 3`) the
positions `a_1, .., a_5` contain `a_i, a_j, a_k` (`i < j < k`) with `a_j` strictly between `a_i` and `a_k`. Let `p`
be an element of `f(a_j)` other than its least and largest (it exists, `|f(a_j)| >= 4`). Then `p ∈ C`, `p` lies
strictly inside the span of `a_j`, and `p ∉ f(a_i) ∪ f(a_k)` because the spans of `a_i`, `a_k` are disjoint from that of
`a_j`. By (F1→) `a_i, a_k ∈ b(p)`, and (F2→) gives a straddle, a contradiction.
(F5→) *There is `H ⊆ C`, `|H| <= 4`, meeting every span of an element of `A`.* Process `A` in order of increasing
`max f(a)`, starting with `H = ∅`; when the span of `a` misses `H`, add `max f(a)` to `H`. Every span is met at the
end. If `a` and later `a'` both added a point, then `max f(a) <= max f(a')` and `max f(a) ∉` span of `a'`, so
`max f(a) < min f(a')`: the spans of the elements that added points are pairwise disjoint, hence at most 4 (F4→).
Elements of `H` are maxima of sets `f(a) ⊆ C`.
For each `h ∈ H` take `N_O[X_h]`. For `a ∈ A` choose `h ∈ H` in its span: if `h ∈ f(a)`, then `X'_a ∩ X_h != ∅` and
`X'_a ∈ N_O[X_h]`; otherwise `h` is a hole of `a` (the ends of the span are in `f(a)`), which happens for at most 2
elements `a` per `h` (F3→); their partners are added as single sides (at most 8).

*(3←) Backward rows.* Let `C' = {O-members c : c <= q_f}` and `A' = R← \ {q_f + 1}`; add the partner of `q_f + 1` as a
single side if `q_f + 1 ∈ R←`. For `p ∈ C'` let `b'(p) = {y ∈ R : X'_p ∩ X_y != ∅}`.
(B0) *For `a ∈ A'`: `f(a) ⊆ C'`, and `p <= a - 2` for `p ∈ C'`.* The contacts of the backward `a` are `<= a - 1`;
the positions from `q_f + 1` (or `1` if `q_f = -∞`) to `a - 1` lie in `R`, so every `O`-member `<= a - 1` lies in
`C'`. As `a ∈ R`, `a != q_f + 1`, we have `a >= q_f + 2 >= p + 2`.
(B1) *For `a ∈ A'`, `p ∈ C'`: `p ∈ f(a)` or `a ∈ b'(p)`.* (F3) for the pair `p`, `a` (opposite types, `|a - p| >= 2`
by (B0)): `X'_a ∩ X_p != ∅` or `X_a ∩ X'_p != ∅`, and `a ∈ R`.
(B2) *If `a ∈ A'`, `p ∈ C'`, `min f(a) < p < max f(a)` and `b'(p)` contains `y_1 < a < y_2`, then `P` has a
`T`-straddle:* `x = a`, `x_1 = y_1`, `x_2 = y_2`, `p_1`, `p_2` the nearest elements of `f(a)` around `p`; now
`p_2 ∈ C'` and `x_1 ∈ R`, so `p_2 <= q_f < x_1`.
(B3) *Each `p ∈ C'` is a hole of at most two elements of `A'`:* a hole `p` of `a` gives `a ∈ b'(p)` (B1); by (B2)
and the absence of straddles, `a` is the least or the largest element of `b'(p)`.
(B4) *No five elements of `A'` have pairwise disjoint spans.* Suppose `a_1, .., a_5 ∈ A'` do, numbered so that the
spans lie in this order from left to right. By Erdős–Szekeres there are `i < j < k` with `a_j` strictly between `a_i`
and `a_k`. Let `p ∈ f(a_j)` be neither its least nor its largest element (`|f(a_j)| >= 4`). Then `p ∈ C'` (B0), `p`
lies strictly inside the span of `a_j`, and `p ∉ f(a_i) ∪ f(a_k)` (disjoint spans). By (B1) `a_i, a_k ∈ b'(p)`; as
`a_j` lies strictly between them, (B2) gives a straddle, a contradiction.
(B5) *There is `H' ⊆ C'`, `|H'| <= 4`, meeting every span of an element of `A'`.* Process `A'` in order of increasing
`max f(a)`; when the span of `a` misses `H'`, add `max f(a)`. If `a` and later `a'` both added a point, then
`max f(a) <= max f(a')` and `max f(a)` is not in the span of `a'`, so `max f(a) < min f(a')`; these spans are pairwise
disjoint, hence at most 4 (B4). Elements of `H'` lie in `C'` (B0).
For each `h ∈ H'` take `N_O[X_h]`. For `a ∈ A'` choose `h ∈ H'` in its span: if `h ∈ f(a)`, `X'_a ∈ N_O[X_h]`;
otherwise `h` is a hole of `a`, which happens for at most 2 elements `a` per `h` (B3); their partners are single sides
(at most 8).

*Count for step (3).* Sets `N_O[Z]`: `2 + 4 + 4 = 10`, all with `Z` a member of `P`, storage `<= 3` each (S2), total
`<= 30`. Single sides: `2` (`q_f - 1`, `q_b + 1`) `+ 1 + 8` (forward) `+ 1 + 8` (backward) `= 20`, storage 0. Every
`T`-member has been covered: `a <= q_f - 2` or `a >= q_b + 2` by Theorem 4(b); `q_f - 1`, `q_b + 1` as single sides;
`a ∈ R` lies in `A`, `A'`, or is `q_b - 1 ∈ R→` or `q_f + 1 ∈ R←`. ∎

**Corollary 9.** Every yes-instance has a shortest valid path `P` with a certificate whose two parts are unions of at
most 10 sets `N_O[Z]` and at most 20 single sides each, of total storage at most 60.
*Proof.* Take a shortest valid path. If it has a straddle, Lemma 7 gives `P*` with parts of 1 set and 2 single sides,
storage `<= 6`; otherwise Theorem 8 applies to both types. ∎

**Theorem 10 (2CH + P2 is in P).** The algorithm: for every `K_E` (union of at most 10 sets `N_F[Z]` and at most 20
single `F`-sides) and every `K_F` (union of at most 10 sets `N_E[Z]` and at most 20 single `E`-sides), run the search of
Theorem 5 with `K = K_E ∪ K_F` and `B = 60`; answer yes iff some run finds a K-admissible walk. It decides 2CH + P2.
*Proof.* A yes answer comes with a K-admissible walk, which is a valid walk (Theorem 5(1)). On a yes-instance,
Corollary 9 gives `P` and a certificate of the stated shape, which is enumerated; by Theorem 5(2) `P` is
K-admissible, so the search accepts. ∎
**Running time (stated honestly).** Computing the side graph and the `2D` sets `N_O[Z]`: `O(D^2 N)`. Choices:
`Σ_{i<=10} C(D, i) · Σ_{j<=20} C(D, j) <= (D + 1)^{30}` per type, `(D + 1)^{60}` pairs. One search: at most
`D (D + 1)^{60}` states with `D` transitions each and `O(1)` set operations of size `<= 60`: `O(D^{62})`. Total
`O(D^{122})` (plus `O(D^2 N)`), `D <= 2n`. This proves membership in P and nothing about practical efficiency; the
exponent comes from the crude counting of Theorem 8 and of the generic search, and no attempt was made to lower it.

## 5. The algorithm in practice (not proved complete)

`r4-switch/alg.py`: `decide(inst, kd, ks, s, B)` enumerates `K_E` (unions of at most `kd` sets `N_F[Z]` and at most
`ks` single `F`-sides) and `K_F` (the same with `E`) and runs the search of Theorem 11 with `s` declarations and
storage `B`. It is sound for all parameters (Theorems 5, 11); with `kd = 10`, `ks = 20`, `s = 0`, `B = 60`
(`decide_full`) it is the algorithm of Theorem 10. Time per call: `O(((D + 1)^{kd + ks})^2 · D^{B + s + 2})`.
With `kd = 1`, `ks = 0`, `s = 4`, `B = 8` it answered "no" on one yes-instance out of 2,400 (7 switches,
`runs/alg-33.txt`): the certificate of the proof there needs a single side whose member lies in `K`, where a
declaration is not allowed. With `kd = 1`, `ks = 1`, `s = 4`, `B = 8` no failure occurred (§6). The rigid family
`R_L` is solved with `kd = 1`, `ks = 0` for `L <= 14`, whereas the node-star search of Theorem H with `t = 1` fails
for `L > 8` (dc-hardness.md, Remark 2).

Why neighbourhoods of sides work where node stars fail: the partners of the same-type members of a shortest path
pairwise meet (F2), so one partner's neighbourhood contains all of them; the price is the storage, the number of
path members of the other type meeting it. Theorem 8 shows that either some partner (or some member) has few such
contacts, or the contacts form at most 4 disjoint spans in the critical run, or a swap (Lemma 7) produces a path with
a certificate of storage 6.

## 6. Checks (exact record; all logs in `r4-switch/runs/`)

Checks cannot prove Theorem 10; they test the steps of the proofs on instances where the steps are triggered, and the
implementation. "Proof steps asserted" means `prove.certificate`: for a given shortest valid path it runs the case
distinction of Theorem 8 with an assertion for each claim (Lemma 1, Theorem 4(a)-(c), (F0), the hole bound (F3→)/(B3),
the span bound (F4→)/(B4), tightness and validity of every swap of Lemma 7, coverage and storage of the final
certificate), and then the search of Theorem 5 (`tsearch.admissible_search`) is run with exactly that certificate and
`B` = its storage and must accept with a valid walk. With `prefer_swap` any straddle of the path is used first, which
exercises Lemma 7 also outside the critical run.

| What | Script and arguments (seed, count) | Instances / paths | Outcome |
|---|---|---|---|
| exact solvers, side-CSP PC | `test_sw.py 1 300` | 300 random P2 instances | solvers agree with `twoch.solve`; PC (side CSP and `pcfast` on the ZZ form) exact on all (199 yes, 101 no) |
| proof steps + guided search, **exhaustive** | `exhaustive.py 3 2`, `4 2`, `3 3`, `4 3` (all instances with 3 or 4 nodes, `s = 0`, `t = 1`, 2 or 3 switches, every side any subset including empty, switches sorted) | 1,715 / 29,615 / 29,197 / 2,170,357 P2 instances; 2,056 / 35,348 / 55,466 / 4,052,958 shortest paths, each with and without `prefer_swap` | 0 failures; all 104,076 no-instances answered "no" by `decide(1,1,4,8)` |
| proof steps (random, planted, families) | `test_prove.py 1 300 all` | 553 paths (incl. `R_2..R_12`, A14, A18) | 0 failures |
| proof steps (saturated planted paths: contacts added while the planted path stays shortest) | `saturate.py 1 40 6 11`; `saturate.py 11..14 150 6 13 0.3` | 452 instances, 933 paths, 33 reaching step (3) with rows | 0 failures; at most 3 sets `N_O[Z]` and 2 single sides needed |
| proof steps + `decide(1,0,4,8)` (straddles inserted into saturated instances) | `straddle_hunt.py 1 40 8 12`; `41 150 8 13` | 133 instances, 275 paths, 10 in step (3) | 0 failures; `decide` correct on 133 |
| proof steps (critical-run words `F^2 E^7 F^7`) | `test_prove_core.py 1 20 2 7 7 0.5 0.0` | 20 instances, 84 paths | 0 failures |
| proof steps + guided search, mixed families | `test_guided.py 1 100`; `61 1500`; `62 1500` | 5,278 paths; 566 no-instances | 0 failures; `decide(1,1,4,8)` "no" on all no-instances |
| same, swaps preferred | `test_guided.py 5 1500 swap`; `81 3000 swap`; `82 3000 swap` | 12,383 paths, 30 swaps (Lemma 7) | 0 failures |
| same on saturated instances of length 10-16 | `guided_sat.py 101..103 300 10 16` | 596 instances, 1,213 paths, 14 swaps, 62 certificate calls in step (3) | 0 failures; storage at most 7 |
| lemmas pointwise on every shortest path: Lemma 1, Theorem 4(a)-(c), (F0), (F1→) on holes, the outer rows of (F4→), **Lemma 7 on every straddle found** | `lemma_test.py 1 100 saturated`, `2 600 random`, `3 600 planted`, `21..23 400 saturated`, `71 1500 planted`, `72 800 saturated` | 6,923 paths, 44 straddles, 90 holes | 0 failures (every straddle tight, swap valid, swap certificate storage `<= 6`) |
| `decide_full` (Theorem 10 parameters) vs brute force | `test_full.py 1 300 4`, `2 300 5`, `3 100 6`, `91 400 6`, `92 400 6` | 1,500 random P2 instances with 2-6 switches | agree on all (969 yes, 531 no) |
| `decide(1,0,4,8)` vs brute force | `test_alg.py 1 200 1 0 4 8 families`, `31..33 800 1 0 4 8` | families: `R_2..R_8` (7), Helly forms (7), one-node deletions keeping P2 (70), `t` moved into a flip side (28), A14, A18 and their deletions (15); plus 2,754 random, repair, planted, saturated and broken saturated instances | 1 answer "no" on a yes-instance (`alg-33.txt`, 7 switches; explained in §5), otherwise agree |
| `decide(1,1,4,8)` vs brute force | `test_alg.py 51..53 800 1 1 4 8` | 2,586 instances | agree on all |
| `decide(1,1,4,8)` and guided search on `R_L` | `rigid_big.py 9 12` | `R_9..R_12`, Helly forms, 84 deletions, 38 `t`-moves | agree on all; guided search accepts on all yes-instances |
| `decide(1,0,4,8)` on `R_L` | `rigid_ks0.py 2 14` | `R_2..R_14` | accepted with a valid walk |
| PC on no-variants of critical-run instances | `exp_critical.py 1 6 2 6 2 0.5 0.3`; `2 6 2 9 2 0.5 0.5` | 58 no-variants | PC refutes all |

Not covered by the checks: instances large enough to come near the bounds of Theorem 8 (the construction never used
more than 3 sets `N_O[Z]` and 2 single sides per type, storage at most 7); the tests show that the steps hold where
they are triggered, not that the bounds are tight.

## 7. Consequences and what remains open

1. **Switch model settled (proved).** 2CH + P2 = SW + P2 (`verify/lth.md` §1) is in P. This subsumes Theorems T, H,
   L(a) of dc-hardness.md and Fω of dc-algorithm.md on the switch model. Every NP-hardness proof for the open case of DC
   must therefore use structure that the switch model lacks: ties (classes of middle elements), one-way
   comparabilities between middle elements, real edges between middle elements, or middle witnesses (brief N6).
2. **Ties (2CH with classes): open; what carries over (sketch).** Theorem 5 extends if the partner of a member `Y` is
   replaced by the family `Π(Y)` of the opposite-type sides of its class (store the members in `K`; refuse a member
   one of whose `Π`-sides is stored). (F1), (F2) for direct partners, and a window bound of 3 positions for the
   contacts of unused same-type sides of a used class carry over. What breaks is Lemma 1: inserting the partner
   `X'_q` is invalid when another member of the class of `q` remains on the path, so contacts need not be one-sided,
   and the storage bounds of Theorem 8 are lost. The mate family `T_L^tie` of dc-general.md, which defeats the pin
   sets of Theorem GC, has a side-set certificate of storage `O(1)` (all mate sides meet the side `[L, K]` of the
   switch `Z`), so Proposition M is not an obstruction to side-set certificates (sketch, not computed).
3. **PC.** Whether path consistency decides 2CH + P2 remains a conjecture; it is no longer needed for the complexity
   of 2CH + P2. PC refuted every no-instance tested in this run (§6).
4. **Exponent.** The proven bound `O(D^{122})` is an artefact of crude counting. Conjecture: one or two sets
   `N_O[Z]` and a bounded number of declarations per type suffice (evidence: §6).

## 8. Scripts (`r4-switch/`)

| Script | What |
|---|---|
| `sw.py`, `test_sw.py` | instances, side graph, brute force, exact search, all shortest valid paths, side-CSP PC, generators; self-test |
| `gen.py` | planted-path instances (type word, orientation of cross pairs, extra contacts); `R_L` and its variants |
| `tsearch.py` | search of Theorem 5 (`admissible_search`), typed basic sets |
| `prove.py` | Lemma 7 and Theorem 8 as a procedure with assertions; certificate construction and verification |
| `alg.py` | `decide` (Theorems 10, 11), `decide_full`, `search_v` |
| `exhaustive.py`, `test_prove.py`, `test_prove_core.py`, `saturate.py`, `straddle_hunt.py`, `lemma_test.py`, `test_guided.py`, `guided_sat.py` | checks of the proof steps |
| `test_alg.py`, `test_full.py`, `rigid_big.py`, `rigid_ks0.py` | algorithm against brute force |
| `cert.py`, `certcost.py`, `exp_planted.py`, `exp_runs.py`, `exp_critical.py` | early experiments (certificate costs, PC on no-variants) |
