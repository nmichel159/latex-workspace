# Round 5, target C: NP-hardness of ZZ + P2 (agent r5-hard, fourth run, 2026-10-23)

Status: **in progress** (fifth run, 2026-10-27, workflow `wf_138deda4-8fb`, round 6; the runs of 2026-10-21,
2026-10-22 and 2026-10-23 left only the skeleton). Updated after every result.
Labels: **proved**, **checked** (exact computation on named instances), **sketch**, **conjecture**, **refuted**.
Scripts: `open-cases/r5-hard/`, logs `open-cases/r5-hard/runs/`.

Task of this run (coordinator, 2026-10-23): decide whether the *bad pairs* of `r5-core.md` §6 (pairs `(x, y)`,
`x ∈ N_F`, `y ∈ N_E`, `y < x`, `x ∉ A`, `y ∉ B`, of a shortest valid path) can carry NP-hardness: (1) families in
which every shortest valid path has many bad pairs that no small (fractional) set of cheap tools covers, checked
against GDESC and the exact solvers; (2) a reduction from an NP-complete problem built on them, if they have free
choices; (3) otherwise a theorem bounding the cost of bad pairs in the encodings tried.

## 0. Summary

(Fifth run, 2026-10-27; provisional, updated after every result.)

| # | Statement | Status |
|---|---|---|
| M | **Member stars make bad pairs irrelevant.** On a shortest valid path, every `x ∈ N_F` is covered by `↑a` or by the sibling star `F#_a` for every `a ∈ A` outside one 9-window; so two members `a_1, a_2 ∈ A` at distance `>= 9` give an F-description (tools `F#_{a_1}`, `F#_{a_2}`, E-anchors `a_1`, `a_2`) that picks the path with `|B ∩ (NF(F#_{a_1}) ∪ NF(F#_{a_2}))|` flips, whatever the bad pairs are; dually with `B`. A variant of TCA (`r5-core.md` §5.2) | proved (§2.1) |
| T | **Zone theorem.** The members of `A` whose F-star reaches far split into right-long and left-long ones; no left-long member precedes a right-long one (beyond distance 2), and a right-long and a later left-long member are at distance `>= K`. Hence, if Proposition M is expensive (cost `> 4K`), the path has `>= (K − 22)/2` consecutive positions without minimal E-members (dually without maximal F-members) | proved (§2.2) |
| BP | Family `BP_n`: dense bad pairs (`K_{n,n}`) hung on the rigid family `R_{2n}`: P2, one solution, one shortest valid path, `n^2` bad pairs, vertex cover `n`, LP cover numbers by the cheap tools `τ_E = τ_F = n`; yet GDESC with 1 tool, 1 anchor, 1 flip accepts (a member star at the cheap end of `R_{2n}`) | checked `n <= 9` (§3.1) |

## 1. Setting and notation

ZZ instance `(Q, <=, R, u, v)`, down-set `D` (`u ∈ D ∌ v`), `G_D` = the `R`-edges `ab` (`a < b`) with `a ∈ D ∌ b`;
P2 = every incomparable pair has a common `R`-neighbour strictly below both or strictly above both (`r4-brief.md` §1).
General switch form (`r4-general.md` §5.1): nodes, terminals `s`, `t`, switches (middle elements) with a preorder,
sides `E_w`, `F_w`; `D` = switches in F-mode (a down-set); a middle edge `y x` (`y < x`) is a private node of
`F_y ∩ E_x`; conflict pair `{E_w, F_z}` with `w <= z`; yes iff a valid walk (no conflict pair) joins `s` to `t`.
For a valid path `P`: `W_E`, `W_F` (E-, F-members), `Up = ↑W_E`, `L = ↓W_F`, `A` (minimal E-members), `B` (maximal
F-members), `N_F = {x ∈ Up : F_x ≠ ∅}`, `N_E = {y ∈ L : E_y ≠ ∅}`; bad pair `(x, y) ∈ N_F × N_E` with `y < x`,
`x ∉ A`, `y ∉ B` (`r5-core.md` §6.4). Cheap tools: stars `E#_w` (`w ∉ L`), strict anchors at `A`, F-anchors `↓z`
(`z ∉ Up`), dually (`r5-core.md` Cor. 6.5').
What a hardness proof must avoid (proved earlier, reviewed in `verify/r5-review.md`): 2CH + P2 is in P (r4-switch
Theorem 10); after a sound fixing with pairwise incomparable free switches the instance contracts to 2CH + P2
(Theorem R, exception vacuous); series class encodings with node witnesses are never assignment-faithful (r4-hard
Corollary 4.2); T3: with one-sided witnesses (distance 3) ZZ is NP-complete.

## 2. Results

Throughout: `P = X_1 .. X_r` a shortest valid path, `pos(w)` the position of a member, (F1) `X_c ∩ X_d = ∅` for
`|c − d| >= 2` (`r4-switch.md` F1; same proof in the general model), and *fact (c)*: every valid walk from `s` to `t`
(sides may repeat) has at least `r` sides (its shortest sub-walk is a valid path, `r5-core.md` §5.2). Sibling stars
`E#_w`, `F#_w`, `NE(·)`, `NF(·)` as in `r5-core.md` §6.3: `F#_a = F_a ∪ {p(v, z) : z ∈ UMN(a)}`, with `p(v, z)` the
private node of the middle edge `v z` (it lies in `F_v` and `E_z` only).

### 2.1 Proposition M: member stars (proved)

**Lemma M1.** Let `x ∈ N_F` and `a ∈ A`. Then `x ∈ ↑a`, or `x ∈ NF(F#_a)`, or `a ∈ S_x := A ∩ NE(E#_x)`; and `S_x`
lies in an interval of at most 9 consecutive positions (`r5-core.md` Lemma 6.3).
*Proof.* `x < a` is impossible: `x ∈ Up` gives an E-member `e <= x`, hence `e < a` (if `a <= e` then `a <= x`),
against the minimality of `a`. If `x`, `a` are tied or `a < x`, then `x ∈ ↑a`. If `x ∥ a`, P2 for `x, a` gives one of:
a node of `E_x ∩ E_a` (`a ∈ NE(E#_x)`); a node of `F_x ∩ F_a` (`x ∈ NF(F#_a)`); a lower middle witness `z < x, a`
(`z ∈ LMN(x)`, the private node `p(z, a)` lies in `E#_x` and in `E_a`, so `a ∈ NE(E#_x)`); an upper middle witness
`z > x, a` (`z ∈ UMN(a)`, `p(x, z)` lies in `F#_a` and in `F_x`, so `x ∈ NF(F#_a)`). This is the argument of
`r5-core.md` Lemma 6.4 for a pair inside `Up`. `x ∈ Up` gives `x ∉ L`, so Lemma 6.3 applies to `S_x`. ∎

**Proposition M.** If `a_1, a_2 ∈ A` and `|pos(a_1) − pos(a_2)| >= 9`, the F-description

    U' = NF(F#_{a_1}) ∪ NF(F#_{a_2}),   S' = ↑a_1 ∪ ↑a_2,   G' = (Fnon − U' − S') ∪ (B ∩ U'),   D = ↓G'

picks every member of `P`. Dually, `b_1, b_2 ∈ B` at distance `>= 9` give the E-description with
`U = NE(E#_{b_1}) ∪ NE(E#_{b_2})`, F-anchors `↓b_1 ∪ ↓b_2`, flips `A ∩ U` and `D = Q − ↑G`. The cost is the number of
flips, `|B ∩ U'|` (resp. `|A ∩ U|`); the bad pairs do not enter.
*Proof.* `G' ∩ Up = ∅`: an element `x ∈ Up ∩ Fnon` lies in `N_F`; both `a_1, a_2` cannot lie in the 9-window `S_x`, so
by Lemma M1 `x ∈ ↑a_i ∪ NF(F#_{a_i})` for some `i`; the flips lie in `B ⊆ L`. As `Up` is an up-set, `D = ↓G'` misses
`Up`. `B ⊆ G'`: `b ∈ B` has `F_b = X_b ≠ ∅`, `b ∉ ↑a_i` (`b ∉ Up`), and if `b ∈ U'` it is flipped in. Hence
`L = ↓B ⊆ D` (every F-member lies below a maximal one). The dual is the same argument with Lemma 6.3 for `F#_y`,
`y ∉ Up`, and with `b < y` impossible for `y ∈ L`, `b ∈ B` (it would put `b` strictly below an F-member). ∎

*Relation to earlier work.* This is a variant of `r5-core.md` Theorem 5.2 (F2)/(E2) (TCA) in its repaired,
uncontracted form (`r5-core.md` §7.1): sibling stars instead of `Ẑ'(a)`, distance 9 instead of 5, and a short proof
from Lemmas 6.3, 6.4. Its use here: **the bad pairs of Theorem 6.5 are an obstruction only on paths on which this
member-star description is expensive for both kinds**, i.e. on which TCA fails. A hardness construction from bad pairs
must therefore also make every far pair of `A` and every far pair of `B` expensive. §3.1 gives a family in which the
bad pairs are as expensive as possible for the cheap tools and Proposition M costs 5 flips.

### 2.2 The zone theorem (proved)

Assume that no member of `P` is tied with another member. For `a ∈ A` at position `p` let

    C(a) = {c != p : X_c ∩ F_a ≠ ∅, or X_c ∩ E_z ≠ ∅ for some upper middle neighbour z of a}.

The catches of `F#_a` lie in `C(a)`: if `b ∈ B` and `F_b ∩ F#_a ≠ ∅`, either `X_b = F_b` meets `F_a`, or `F_b` contains
a private node `p(v, z)` with `z ∈ UMN(a)`, which forces `v = b` and `p(b, z) ∈ E_z ∩ X_b`.

**Lemma S1 (span).** If `c, d ∈ C(a)` and `c < p < d`, then `d − c <= 4`.
*Proof.* Take the walk `X_1 .. X_c, [E_z], F_a, [E_{z'}], X_d .. X_r`, with `E_z` (`E_{z'}`) inserted when the contact
`c` (`d`) is through `E_z` (`E_{z'}`), `z, z' ∈ UMN(a)`; the private node `p(a, z) ∈ F_a ∩ E_z` joins them. No conflict
pair: `F_a` conflicts only with E-sides of switches `<= a`; among the kept members these are E-members `<= a`, i.e. `a`
itself (minimal, no ties), whose position is skipped; `E_z` conflicts only with F-sides of switches `>= z`, all in `Up`
since `z > a`, so with no F-member and not with `F_a`; two E-sides never conflict. Fact (c): `c + 3 + (r − d + 1) >= r`. ∎

**Lemma S2 (linked pairs).** Let `a, a' ∈ A`, `p = pos(a) < p' = pos(a')`, `p' − p >= 3`. (a) `F_a ∩ F_{a'} ≠ ∅`, or
`a`, `a'` have a common upper middle neighbour `w`. (b) If `c < p < p' < d` with `c, d ∈ C(a) ∪ C(a')`, then
`d − c <= 6`.
*Proof.* (a) `a ∥ a'` (minimal, no ties). In P2, `E_a ∩ E_{a'} = X_p ∩ X_{p'} = ∅` by (F1); a lower middle witness
`z < a, a'` has `z ∉ Up` (an E-member `<= z` would lie strictly below `a`), so `F_z` is `P`-consistent and meets `X_p`
and `X_{p'}` through private nodes; if `z` is not on `P`, Lemma 6.2 (`j = 1`) gives `p' − p <= 2`; if `z` is on `P`, it
is an F-member and (F1) gives `p' − p <= 2`. So the witness is a node of `F_a ∩ F_{a'}` or an upper middle witness.
(b) If `c` and `d` lie in `C` of one member, Lemma S1 applies. Otherwise take
`X_1 .. X_c, [E_z], F_α, [E_w], F_β, [E_{z'}], X_d .. X_r` (`{α, β} = {a, a'}`, `E_w` inserted when the link is through
`w`). Validity as in S1; in addition `E_z` (`z ∈ UMN(α)`) and `F_β` conflict only if `z <= β`, which with `z > α`
gives `α < β`, impossible in `A`; `w` lies above both. Fact (c): `c + 5 + (r − d + 1) >= r`. ∎

Fix `K >= 8`. Call `a ∈ A` *right-long* if `max C(a) >= pos(a) + K`, *left-long* if `min C(a) <= pos(a) − K`,
*short* otherwise (then `C(a) ⊆ (pos(a) − K, pos(a) + K)` and `F#_a` catches at most `2K − 2` members of `B`).

**Theorem T (zones).** (i) No member of `A` is both right-long and left-long. (ii) If `a` is left-long and `a'`
right-long, then `pos(a') <= pos(a) + 2`. (iii) If `a` is right-long, `a'` left-long and `pos(a') >= pos(a) + 3`, then
`min C(a') >= pos(a)` or `max C(a) <= pos(a')`; in both cases `pos(a') − pos(a) >= K`.
*Proof.* (i) Lemma S1 with `c <= p − K`, `d >= p + K`. (ii) Otherwise `p' >= p + 3`, and Lemma S2(b) with
`c = min C(a) <= p − K` and `d = max C(a') >= p' + K` gives `d − c >= 2K + 3 > 6`. (iii) If `c = min C(a') < p` and
`d = max C(a) > p'`, Lemma S2(b) gives `d − c <= 6`, but `d >= p + K > c + K`. In the first remaining case
`p <= min C(a') <= p' − K`, in the second `p + K <= max C(a) <= p'`. ∎

**Corollary T1.** Suppose, in the same setting, that no two members of `A` at distance `>= 9` have
`|B ∩ (NF(F#_{a_1}) ∪ NF(F#_{a_2}))| <= 4K` (Proposition M is expensive for the F-kind), and that `A` does not lie in an
interval of length `<= 8` (if it does, the E-anchors at `A`, at most 9, give the F-description `G' = Fnon − ↑A`,
`D = ↓G'`). Then the short members of `A` lie in one interval of length `<= 8`, and `P` contains at least
`⌈(K − 22)/2⌉` consecutive positions none of which carries a member of `A`. Dually for `B`.
*Proof.* Two short members at distance `>= 9` would give a pair of cost `<= 4K − 4`. Let `R`, `Lf` be the right-long
and left-long members; one of them is non-empty (`A` has two members at distance `>= 9`, not both short). If `R ≠ ∅`,
let `p_R` be the position of its last member. If `Lf = ∅`: `max C(a_R) >= p_R + K`, so the positions
`p_R + 1 .. p_R + K − 1` exist and carry only short members (no right-long member lies after `p_R`, none is
left-long), which lie in an interval of length `<= 8`; one of the two free pieces has length `>= (K − 10)/2`. If
`Lf ≠ ∅`, let `p_L` be the position of its first member. By (ii), `p_R <= p_L + 2`. If `p_L >= p_R + 3`, by (iii)
`p_L − p_R >= K` and `(p_R, p_L)` carries only short members. If `|p_L − p_R| <= 2`, by (iii) every right-long member
outside `[p_L − 2, p_R]` lies at distance `>= K` before `p_L`, and every left-long member outside `[p_L, p_R + 2]` at
distance `>= K` after `p_R`; the `p_R − p_L + 2K − 1 >= 2K − 3` positions of `(p_L − K, p_R + K)` exist (`C(a_R)`
reaches `p_R + K`, `C(a_L)` reaches `p_L − K`) and carry long members only inside an interval of `<= 7` positions
and short ones only inside one of `<= 9`; the at most three free pieces have total `>= 2K − 19`, so one has length
`>= (2K − 19)/3 >= (K − 22)/2`. `R = ∅` is symmetric to `Lf = ∅`. ∎

*Reading.* On a path on which TCA fails with cost `c`, there are stretches of length about `c/8` without minimal
E-members and stretches without maximal F-members. Their E-members are non-minimal (they lie in `Up − A`) and their
F-members non-maximal (`L − B`): exactly the elements that can form bad pairs. So a construction that defeats both
Theorem 6.5 and TCA has the shape *zone of right-long members, stretch of non-extremal members, zone of left-long
members* (§4, route R2). In 2CH (`A = W_E`, `B = W_F`) the stretches are runs of F-members and runs of E-members.

## 3. Computations

Scripts in `r5-hard/`: `hlib.py` (instance builder in general switch form on top of `r5-core/gcore.py`; analysis of all
shortest valid paths with `r5-core/gstar.py`: bad pairs, vertex cover, LP cover numbers by the cheap tools, catches of
member stars, cost of Proposition M with its description built and checked), `bpfam.py`, `test_bp.py`. Code of
`r5-core/` is imported read-only (`gcore` was reviewed in `verify/rv-core.md`; `gstar`, `gdesc` belong to §6, under
review in `verify/rv-core-65.md`).

### 3.1 Family `BP_n` (`bpfam.bp`, `test_bp.py`; route R1 of §4)

Exact runs (no randomness): `python test_bp.py 2 5 1 1 1` (console) and `python test_bp.py 6 9 1 1 1`
(`runs/bp-6-9-111.txt`). For every `n = 2..9`: P2 holds (`Gen.p2_bad` empty); one solution (`Gen.brute`, run for
`n <= 6`, `m = 4n <= 24` switches); exactly one shortest valid path, `h_1 .. h_{2n}` of `R_{2n}` (`Gen.all_shortest`);
`|A| = |B| = n`, `|N_E| = |N_F| = 2n`; the bad pairs are exactly `(X_j, Y_i)` for all `i, j` (`n^2` pairs, vertex
cover `n`); the LP cover numbers of `N_E` and `N_F` by the cheap tools of Corollary 6.5' are `τ_E = τ_F = n`
(`gstar.cover_numbers`). The catches of the member stars are `1, 2, .., n` (`F#_a`) and `0, 1, .., n − 1` (`E#_b`):
`R_{2n}` has a cheap end. Proposition M (pairs at distance `>= 9`, `n >= 6`) costs 5 flips (E-kind, members
`x_{2n−10}`, `x_{2n}`); its description was built and checked to pick the path and connect `s`, `t`, for every pair at
distance `>= 9`. GDESC (`r5-core/gdesc.decide(k=1, a=1, e=1)`) accepts every `BP_n`, `n = 2..9`, with the
E-description: tool `x_{2n−2}` (the last F-member but one), anchor `x_{2n−2}`, flip `x_{2n−1}`.

## 4. Routes tried and why they fail

**R1. Dense bad pairs on a rigid base (`BP_n`, checked).** Take the rigid family `R_{2n}` (unique solution, path
`a_1 b_1 .. a_n b_n`), hang `Y_i < b_i` and `X_j > a_j` below/above its members with `Y_i < X_j` for all `i, j`, and meet
P2 by middle witnesses inside `X ∪ Y` (`X_1` above all `Y`, `Y_1` below all `X`, `X_l` above `Y_i, a_l`, `Y_k` below
`X_j, b_k`) and by nodes `E(Y_i) ∩ Fl(b_k)`, `F(X_j) ∩ Fl(a_l)` on the unpicked flip sides. The bad pairs form a
complete bipartite graph and no cheap tool covers two of them (§3.1). *Why it fails:* the witnesses of `Y_i` with `b_k`
make the member star `E#_{b_k}` cover every `Y_i`, `i != k`; a member star is not a cheap tool, but its cost is its
catches, and the last members of `R_{2n}` catch almost nothing (the first-flip structure of `R_{2n}` points forward).
By Lemma M1 this is unavoidable: whatever witnesses are chosen, every `Y_i` is covered by all but 9 of the stars
`E#_b`, `b ∈ B` (or lies below `b`). So bad pairs must be combined with a base on which every far pair of members is
expensive (TCA fails); Theorem T says what such a base looks like.

## 5. What remains open

(to be filled)
