# DC-general: the certificate method of Theorem H on general ZZ + P2

Agent: DC-general, 2026-10-13 (resumes the interrupted run whose scripts are `dc-general/gzz.py`, `hsearch.py`,
`hunt_tie.py`, `k4c*.py`, `test_h.py`, `tools.py`; no report had been written). Scripts of this run:
`dc-general/gcert.py` (certificate search, own exact solver, random preorders), `dc-general/test_gcert.py`.
Labels: **proved**, **checked** (exact computation on the instances named), **sketch**, **conjecture**, **refuted**.
Notation as in `theory-dc.md` (ZZ, P2) and `dc-hardness.md` (2CH, Theorem H). `B` = class of `u`, `T` = class of `v`;
an element is *middle* if it is in neither. For a down-set `D` (`u ∈ D ∌ v`) `G_D` is the graph of the `R`-edges
`ab`, `a < b`, with `a ∈ D ∌ b`; ZZ asks whether some `G_D` connects `u` and `v` (`verify/equivalence.md` §3).

## Results

| # | Claim | Status | Evidence |
|---|---|---|---|
| GC | Certificate theorem for general ZZ: pin sets (generators and piercers, below and above) make a walk search that is sound for every pin set and complete when the certificate number `κ <= k`; time `q^{O(k)}`. Theorems F and H are the cases `κ <= 2` and `κ <= 4t` | proved (§1); soundness checked on 15,000 random P2 instances (§6) | `gcert.py`, `test_gcert.py` |
| P | What P2 gives on a shortest path of `G_D`: incomparable valleys at distance `>= 4` have a common `R`-neighbour inside `D` (below both, or above both); dually for peaks | proved (§2) | |
| Br | The three places where the method breaks outside the switch model: (B1) conflict candidates other than the valley itself (ties, smaller middle elements), (B2) comparable valleys in one group, (B3) common neighbours above two valleys inside `D` | proved (§2) | |
| M | **Ties and one-way comparabilities defeat every bounded certificate, even for interval (Helly) sides.** The rigid family `R_L` in interval form, extended by one *mate* per switch (a tie `m_k ~ x_k`, or a one-way relation `m_k < x_k` / `m_k > x_k`), is a ZZ + P2 instance with a unique solution (up to one free switch), classes of size `<= 2`, no edges between middle elements, all sides intervals; its certificate number is exactly `⌊L/2⌋`, while without mates it is `<= 2` | proved (§3); checked `L = 2..8` (P2, answer, number of solutions, least certificate found = `⌊L/2⌋`; GC with `k = 2` fails from `L = 6`, with `k = 3` from `L = 8`) | `families.py`, §3 |
| M' | The same for the 2CH (hypergraph) form of `R_L` with `t` in every flip side | checked `L = 2..8` | `families.rigid` |
| ... | (in progress) | | |

## 1. The certificate theorem (GC)

**Setting.** `I = (Q, ≤, R, u, v)` a ZZ instance, `q = |Q|`. A *walk* is `W = x_0 x_1 ... x_L` with `x_0 = u`,
`x_L = v`, `L` odd, consecutive elements joined by `R`-edges, `x_i < x_{i+1}` for even `i` and `x_i > x_{i+1}` for odd
`i`; `V(W)` (valleys, even positions) and `P(W)` (peaks). A *conflict* is a valley `>=` a peak.
*Peak-capable*: not in `B` and with an `R`-neighbour below; *valley-capable*: not in `T` and with an `R`-neighbour
above. Every peak of a walk is peak-capable and every valley valley-capable (a peak lies strictly above its
neighbours, so it is not in `B`; dually for valleys).

**Lemma 0 (proved).** A conflict-free walk lies in `G_D` for `D = ↓V(W)`, so the instance is a yes-instance;
conversely a consistent zigzag is a conflict-free walk.
*Proof.* `D` is a down-set containing `u`; `v ∉ D` since `v ∈ D` would be a valley `>= v`, a conflict; every peak is
outside `D` (no valley above it), every valley inside, so every edge of `W` crosses `D`. ∎

**Pin sets.** `π = (G-, P-, G+, P+)`, four subsets of `Q` (generators and piercers, below and above);
`|π|` = the sum of their sizes. `D- = ↓(G- ∪ P-)`, `U+ = ↑(G+ ∪ P+)`.
`M-` = elements with an `R`-neighbour in `P-` below them (*stored peaks*), `M+` = elements with an `R`-neighbour in
`P+` above them (*stored valleys*). A walk is *π-admissible* (general mode) if
- (A1) no peak lies in `D-` and no valley in `U+`;
- (A2) for every valley `x ∉ D-`: every peak-capable `y <= x` with `y ∉ D-` lies in `M-`;
- (A3) for every peak `y ∉ U+`: every valley-capable `x >= y` with `x ∉ U+` lies in `M+`;
- (A4) no valley in `M+` is `>=` a peak in `M-`;
- (A5) every element of `P-` is `R`-adjacent to at most two peaks of `W` in `M-`, every element of `P+` to at most
  two valleys of `W` in `M+`.
*Peak-pinned mode:* every peak in `U+`, no valley in `U+` (only `G+` matters). *Valley-pinned mode:* dually.

**Lemma 1 (soundness; proved).** For every pin set, a π-admissible walk (in any mode) is conflict-free.
*Proof.* Let a valley `x` be `>=` a peak `y`. Peak-pinned mode: `y ∈ U+`, so `x ∈ U+` (up-set), excluded.
Valley-pinned: dual. General mode: `y ∉ D-` by (A1), hence `x ∉ D-` (`D-` is a down-set and `y <= x`); `x ∉ U+` by
(A1), hence `y ∉ U+`. By (A2) at `x` (`y` is peak-capable, `y <= x`, `y ∉ D-`) `y ∈ M-`; by (A3) at `y`, `x ∈ M+`;
this contradicts (A4). ∎ ((A5) is not used: it only bounds the search.)

**Lemma 2 (search; proved).** For a fixed pin set the existence of a π-admissible walk is decided by a breadth-first
search over states (current element, parity, set `S` of the elements of `M- ∪ M+` visited so far as stored peaks or
valleys); (A1)-(A3) are conditions on single elements, (A4) and (A5) are checked when an element enters `S`. By
(A5) `|S| <= 2|P-| + 2|P+|`, so there are `O(q^{2|π|+1})` states and the search takes `O(q^{2|π|} |R|)` time.
Pinned modes are a plain search in `G_{Q - U+}` (peak-pinned) or `G_{D-}` (valley-pinned).

**Lemma 3 (completeness; proved).** Let `D` be a down-set with `u ∈ D ∌ v`, `Z` a shortest `u`-`v` path of `G_D`,
and `π` a pin set with `G- ∪ P- ⊆ D`, `(G+ ∪ P+) ∩ D = ∅`, such that (A2) holds at the valleys of `Z` and (A3) at its
peaks. Then `Z` is π-admissible. Likewise in peak-pinned mode if `P(Z) ⊆ U+` and `(G+) ∩ D = ∅`.
*Proof.* (A1): `D- ⊆ D` and peaks are outside `D`; `U+ ∩ D = ∅` (an element of `U+ ∩ D` is above a pin that would lie
in `D`), and valleys are inside `D`. (A4): `Z` is consistent. (A5): a pin `φ ∈ P- ⊆ D` and a peak `y ∈ M-` adjacent to
it give an edge `φy` of `G_D`; the vertices of a shortest path adjacent to one vertex lie within three consecutive
positions (otherwise the path can be shortened through `φ`), which contain at most two peaks. Dually for `P+`. ∎

**Definition.** The *certificate number* `κ(I)` is the least `|π|` over all `D`, shortest paths `Z` of `G_D` and pin
sets as in Lemma 3 (any mode); `κ(I) = ∞` on no-instances.

**Theorem GC (proved).** For fixed `k`, the algorithm "for every pin set with `|π| <= k` and every mode, search for a
π-admissible walk" runs in `q^{O(k)}` time, never accepts a no-instance (Lemmas 0, 1), and accepts every instance
with `κ(I) <= k` (Lemma 3). In particular ZZ is polynomial on every class of instances with bounded `κ`.

**Special cases.**
1. *Theorem F (bottom witnesses).* With `A` the minimal middle peaks of `Z` (at most two, `dc-algorithm.md` Theorem
   F(ii)), `G+ = A` (or `{v}` if `A = ∅`) is a peak-pinned certificate: `κ <= 2`.
2. *Theorem H (switch model).* In the ZZ form of 2CH the middle elements are pairwise incomparable and every
   `R`-neighbour below a middle element lies in `B`. For a middle valley `x` the only peak-capable `y <= x` outside
   `B` is `x` itself, so (A2) reads "`x` has an `R`-neighbour in `P-`", i.e. the partner side of `x` meets the node
   set `P-` (condition (i) of Theorem H); likewise (A3). If for each of the four groups (valleys or peaks of `Z`, by
   position mod 4) the partner sides can be pierced by `t` nodes, `P- ∪ P+` of size `4t` is a certificate:
   `κ <= 4t` (with Lemma 4 below this is Theorem H).

Remarks. (1) The pin sets of one side need not be split by groups: making a piercer available to every group only
weakens (A2) and does not change `M-`; groups matter only in the completeness argument. (2) Generators are new
compared with Theorem H: a valley `x ∈ D-` needs no piercing at all, and `D-` removes elements from the conflict
sets of other valleys.

## 2. What P2 gives, and where the method breaks

**Lemma 4 (proved).** Let `D`, `Z = x_0 ... x_L` be as in Lemma 3 and `x_a`, `x_b` valleys with `b - a >= 4`.
Every common `R`-neighbour of `x_a`, `x_b` lies in `D`. Hence, if `x_a`, `x_b` are incomparable, P2 gives a common
`R`-neighbour `z ∈ D` that lies below both or above both. Dually two incomparable peaks at distance `>= 4` have a
common `R`-neighbour outside `D`, below both or above both.
*Proof.* A common neighbour above both outside `D` is adjacent to both in `G_D`, and `x_0 .. x_a z x_b .. x_L`
contains a shorter `u`-`v` path. A common neighbour below both lies in `D` because `D` is a down-set. ∎

In the switch model the second alternative cannot occur (above a middle element there is only `T`, outside `D`), so
the partner sides of a group pairwise meet; this is the step of Theorem H. In general ZZ + P2 the method needs, at a
valley `x` of group `g` not covered by a generator, that **every** peak-capable `y <= x` outside `D-` be pierced. The
step fails in exactly three ways:
- **(B1) Extra conflict candidates.** `↓x - D-` may contain peak-capable elements other than `x`: elements
  equivalent to `x` (ties) or middle elements below `x` (one-way comparabilities). Lemma 4 says nothing about them:
  they are not on `Z`, and a candidate `y ~ x` is not related by P2 to `x`.
- **(B2) Comparable valleys.** Two valleys of one group may be equivalent or comparable; P2 does not apply.
- **(B3) Upper witnesses inside `D`.** Incomparable valleys may have only common neighbours above both, inside `D`
  (middle elements above middle elements, with real edges between middle elements); then their below-neighbourhoods
  need not meet.
(B2) and (B3) come with a common upper bound inside `D` (the larger valley, or `z`), so one generator covers both
valleys; whether boundedly many generators suffice is a Helly question for up-sets inside `D` that P2 does not
answer. (B1) is the essential break: neither piercing nor P2 controls the candidates.

## 3. Ties and one-way comparabilities: a family with unbounded certificate number (Proposition M)

**The family `T_L` (`families.tic_rigid`).** Line of junctions `0..K`, `K = 2L + 1`, `s = 0`, `t = K`; a side is a set
of consecutive junctions (TIC, `dc-hardness.md` Section 5), so same-type sides are Helly. Switches `x_1 .. x_L`:
path side `h_k = [k-1, k]` (type E for odd `k`, F for even `k`), flip side `Fl_k = [k, K]` (the other type); switch
`Z` with `E = F = [L, K]` (covers the region `Y = [L, K]` in either mode). This is `R_L` in interval form with every
flip side extended to `K` and the region `Y` appended. *Mates*: for even `k`, `E(m_k) = {L + k}`, `F(m_k) = {K}`; for
odd `k`, `E(m_k) = [L, K]`, `F(m_k) = {L + k}`. Two versions: `T_L^tie` (classes `{x_k, m_k}`) and `T_L^one`
(partial order `m_k < x_k` for even `k`, `x_k < m_k` for odd `k`, all other middle pairs incomparable). ZZ form as in
`verify/lth.md` §1 (bottom and top per junction, fixed edges, member elements; equivalent or ordered members as
stated); no `R`-edge joins two middle elements.

**Proposition M (proved).** For `L >= 2`, `T_L^tie` and `T_L^one` satisfy P2, are yes-instances, and
`κ(T_L^tie) = κ(T_L^one) = ⌊L/2⌋`; without mates `κ(T_L) <= 2`. Hence the algorithm of Theorem GC with any fixed `k`
fails on `T_L^tie` and `T_L^one` for `L >= 2k + 2`, although these instances have interval sides, classes of size at
most 2 (resp. each middle element comparable with at most one other middle element) and a unique solution up to the
mode of `Z`.

*Proof.* **P2.** Incomparable pairs are pairs of members of different classes (resp. all middle pairs except
`{x_k, m_k}`); a common bottom means a common junction of the E-sides, a common top one of the F-sides.
`x_p, x_q` (`p < q`): same parity, the flip sides (same type) share `K`; opposite parity, `Fl_p ⊇ h_q` (same type)
since `q - 1 >= p`. `Z` with `x_k`: `Fl_k ∩ [L, K] ∋ K` (same type as one side of `Z`). Mates: even `m_k` with even
`m_j`: F-sides share `K`; odd with odd: E-sides `[L, K]`; even `m_k` with odd `m_j`: `L + k ∈ [L, K]`; even `m_k` with
`x_j`: `j` even, `L + k ∈ Fl_j` (E); `j` odd, `K ∈ Fl_j` (F); odd `m_k` with `x_j`: `j` odd, `L + k ∈ Fl_j` (F);
`j` even, `[L, K] ∩ Fl_j ∋ K` (E); mates with `Z`: `L + k ∈ [L, K]` or `[L, K]` itself (E).
**Solutions.** A down-set `D` corresponds to modes (a middle element in `D` uses its F-side). Connectivity of `u`, `v`
in `G_D` is coverage of all edges `(j-1, j)` by picked sides. Let `r <= L` be the first switch `x_r` not in its intended
mode (E for odd, F for even). The edge `(r-1, r)` lies only in `h_r` (not picked), in `Fl_p` with `p <= r - 1` (not
picked: `x_p` has its intended mode), and in no mate side or side of `Z` (those lie in `Y`, or are single junctions);
so no picked side contains both `r-1` and `r`, and `u`, `v` are disconnected. With all switches in intended mode the
path sides and `Z` cover everything. Mates do not affect connectivity (their sides lie in `Y`, which `Z` covers), and in
`T^one` their modes are forced by the order (`m_k <= x_k` puts `m_k` into `D` with `x_k`, even `k`; `x_k <= m_k` keeps
`m_k` out with `x_k`, odd `k`). So the solutions are the intended modes, `Z` free.
**Every admissible walk passes all switches.** By Lemma 1 an admissible walk `W` is conflict-free and lies in
`G_{D}`, `D = ↓V(W)`, a solution. A member element adjacent in `G_D` to junction elements on both sides of the edge
`(k-1, k)`, `k <= L`, has a picked side containing `k - 1` and `k`; only `h_k` qualifies. So `W` visits `x_k`, as a
valley for even `k` and as a peak for odd `k`.
**Lower bound.** Let `W` be π-admissible. *General mode:* for even `k`, (A2) at the valley `x_k` requires `x_k ∈ D-`
or (`m_k` is peak-capable, its only `R`-neighbour below is the bottom of `L + k`, and `m_k <= x_k`) `m_k ∈ D- ∪ M-`.
An element of `T` in `G- ∪ P-` makes `D- = Q ∋ v`, which (A1) forbids (`v` is a peak). So some pin lies in
`S_k = {x_k, m_k} ∪ {bottom of L + k}`: a member pin above `x_k` or `m_k` (only `x_k`, `m_k` qualify), or the piercer
that stores `m_k`. The sets `S_k` (`k` even) are pairwise disjoint, so `|π| >= ⌊L/2⌋`. *Peak-pinned mode:* every odd
`x_k` (a peak) lies in `U+`, so `G+` contains an element `<= x_k` other than an element of `B` (which would put the
valley `u` into `U+`): `x_k` or (ties) `m_k`; disjoint over odd `k`: `|π| >= ⌈L/2⌉`. *Valley-pinned mode:* dually
`>= ⌊L/2⌋`. **Upper bound:** valley-pinned with `G- = {x_k : k even}`. **Without mates:** `P- = {bottom of K}`,
`P+ = {v}` is a certificate (every flip side contains `K`; (A2) at an even `x_k` needs only `x_k ∈ M-`, (A3) at an odd
`x_k` only `x_k ∈ M+`; the stored elements adjacent to the two pins are at most `Z` and `v`, resp. `Z` and the bottom
of `K`). ∎

*Checked* (`families.py`, scratch runs of this session): `L = 2..8`, both versions: P2, answer (own exact solver),
number of witness down-sets (2 for `L <= 5`), and the least certificate found by `gcert.certificate`: `⌊L/2⌋` with
mates (pinned modes), 1-2 without mates; `k = 2` fails for `L = 6`, `k = 3` for `L = 8`. The 2CH form of `R_L` with `t`
in every flip side and analogous mates (`families.rigid`) gives the same numbers (`L = 2..8`).

**Reading.** The mates are useless for connectivity, yet a walk search must remember, for each even `k`, that the
class of `x_k` has been used as a valley, because a later walk may use `m_k` as a peak; condition (A2) forces this
through piercers or generators, one per mate. This is break (B1) in its purest form: the conflict candidate `m_k` is
not on the walk, and P2 relates it to nothing that a bounded pin set can see. In `T^one` the same happens without any
tie. Theorems T and H do not extend to ties or one-way comparabilities by adding pins.
