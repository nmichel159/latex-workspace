# Round 7, agent r7-desc: Conjecture C1 through descriptions

Status: 2026-10-31, main proof written, waiting for an independent referee. Working file of an AI agent; not read by
the author; not in the manuscript; **not reviewed**. Scripts: `r7-desc/`. Labels: proved, checked, sketch, conjecture,
refuted. Notation: `qp-proof.md` §1.4, §4, §5.

## 0. Summary of results

| # | Statement | Status |
|---|---|---|
| S | Monotone separation: a bounded family of down-sets separating every pair of `A × B` gives a connecting down-set, as a monotone formula of the family | proved (§2.1) |
| R | Rectangles without bad pairs: two far members of `A` give an F-term missing `Up` and containing `B − C(a_1) − C(a_2)`; two far members of `B` give an E-term containing `L` and missing `A − C'(b_1) − C'(b_2)` | proved (§2.2; form of `r5-hard.md` Prop. M) |
| X | Cross lemma: without same-type ties, `a ∥ h` excludes far F-contacts of `a` on both sides of `h` together with far E-contacts of `h` on both sides of `a` | proved (§2.3) |
| A | Theorem A: the tie-free case; the middle of `A × B` consists of strict pairs | proved (§2.4), not reviewed |
| G | Lemmas J, G: one and two jumps, with same-type ties | proved (§3), not reviewed |
| B | **Theorem B: every yes-instance with `s ≠ t` has a connecting down-set given by one of four monotone formulas in bounded atoms, built from at most 91 switches. Corollary B1: ZZ + P2, hence the open case of DC, is in P, time `m^{91} · poly`** | proved (§3), **NOT reviewed; needs an independent referee** |

Consequence: C1 in its literal form (one term) is replaced by C1*: a bounded monotone formula of terms, which gives a
polynomial algorithm as well. Theorem B proves C1*. C1 itself stays open and is not needed.

## 1. Why Theorem 5.3 needs `log m` levels, and what one level achieves

1. An E-term picks `P` iff `Γ ∩ L = ∅` and `A ⊆ ↑Γ`; so it must catch every column `y ∈ N_E`. Dually for F-terms.
2. Lemma 4.5 gives the duality `y ∈ NE(E#_x)` or `x ∈ NF(F#_y)` only for `x ∥ y`; for `y < x` (bad pairs) nothing.
3. The pivot `↓x − [x]` catches the strict pairs, but it also removes `dam(x) = A' ∩ (↓x − [x])` from `Γ`.
4. Star catches cost at most 9 flips per tool (Lemma 4.4); pivot damage is unbounded, so it cannot be flipped away.
5. One level (Lemma 5.2) plays the game rows `↑A' ∩ Fnon` against columns `N_E`, light pivots only (`|dam| <= |A'|/(2k)`).
6. Value `>= 1/2`: `k = log m` sampled rows cover all columns; the damage is at most `kθ = |A'|/2`: `D ∩ ↑A' ⊆ ↑A''`, `|A''| <= |A'|/2`.
7. Value `< 1/2`: `k` sampled columns cover the light rows, `N = O(log² m)` anchors drawn from `A'` hit the heavy rows: final.
8. So a level always keeps `L` and removes half of the residue `A'`; only the residue `A''` needs the next level.
9. Hence `log m` levels (halving of the damage), `log m` tools per level (sampling, the minimax has no structure), `log² m` anchors.
10. Every factor comes from insisting that a term catches all rows or columns, i.e. from the bad pairs. §2 drops this: only pairs of `A × B` are separated.

## 2. Results

Fixed: an instance of the general switch form with P2, a shortest valid path `P = X_1 .. X_r`, objects of Definition 4.1.
`pos` is the position on `P`. Contacts: `C(a) = B ∩ NF(F#_a)` for `a ∈ A`, `C'(b) = A ∩ NE(E#_b)` for `b ∈ B`.

### 2.1 Monotone separation (proved)

**Lemma S.** Let `D_1, .., D_q` be down-sets such that for every `(a, b) ∈ A × B` some `D_i` has `b ∈ D_i ∌ a`. Then
`D* = ⋃_{b ∈ B} ⋂_{i : b ∈ D_i} D_i` is a down-set with `L ⊆ D* ⊆ M − Up` (for `B = ∅` read `D* = ∅`). So it connects `s`, `t`.
*Proof.* Unions and intersections of down-sets are down-sets, and `b` lies in its own intersection, so `L = ↓B ⊆ D*`.
If `a` lay in the intersection of `b`, then `b ∈ D_i` would imply `a ∈ D_i` for all `i`, against separation. So `A ∩ D* = ∅`,
and `Up = ↑A` misses the down-set `D*`. Lemma 3.4(a) ends the proof. ∎

### 2.2 Atoms (proved)

The *atoms* are these down-sets; all are computed from at most two switches, and every choice gives a down-set.
- `FR(a_1, a_2)`: the F-term with `T = Ψ = {a_1, a_2}`, `T' = Φ = ∅`.
- `ER(b_1, b_2)`: the E-term with `T = Y = {b_1, b_2}`, `T' = Φ = ∅` (F-anchors `Y` as in `r5-core.md` §6.1).
- `FP(h)`: the F-term with `T = T' = {h}`, `Ψ = Φ = ∅`.
- `↓b`, and `M − ↑a`.

**Lemma R.** (a) If `a_1, a_2 ∈ A` and `|pos(a_1) − pos(a_2)| >= 9`, then `FR(a_1, a_2) ∩ Up = ∅` and `FR(a_1, a_2) ⊇ B − C(a_1) − C(a_2)`.
(b) If `b_1, b_2 ∈ B` and `|pos(b_1) − pos(b_2)| >= 9`, then `ER(b_1, b_2) ⊇ L` and `ER(b_1, b_2)` misses `A − C'(b_1) − C'(b_2)`.
(c) For `h ∈ B`: `FP(h)` misses every `a ∈ A` with `h < a`, and contains `B − C_h`, with `C_h = B ∩ NF(F#_h)` inside an interval of at most 9 positions containing `pos(h)`.
(d) `↓b ⊇ {b}`, `↓b ∩ Up = ∅`; `M − ↑a ⊇ L`, `a ∉ M − ↑a`.
*Proof.* (a) Let `x ∈ N_F`, `i ∈ {1, 2}`. `x < a_i` is impossible (an E-member `e <= x` would have `e < a_i`). So `x ∈ ↑a_i`, or `x ∥ a_i` and Lemma 4.5 gives `x ∈ NF(F#_{a_i})` or `a_i ∈ NE(E#_x)`. Both `a_1, a_2 ∈ NE(E#_x)` contradicts Lemma 4.4 (`x ∉ L`). So `x ∉ Γ'`, hence `Γ' ∩ Up = ∅` and `↓Γ' ∩ Up = ∅` (Lemma 4.2(c)). A `b ∈ B − C(a_1) − C(a_2)` lies in `Fnon`, outside `↑a_i` (Lemma 4.2(b)), so in `Γ'`.
(b) Dual: for `y ∈ N_E`, `b_i < y` is impossible (`y <= b'` with `b' ∈ B` gives `b_i < b'`). So `y <= b_i`, or `y ∥ b_i` and Lemma 4.5 gives `y ∈ NE(E#_{b_i})` or `b_i ∈ NF(F#_y)`. Both `b_1, b_2 ∈ NF(F#_y)` contradicts the dual of Lemma 4.4 (`y ∉ Up`). So `Γ ∩ L = ∅`, `L ⊆ M − ↑Γ`. An `a ∈ A − C'(b_1) − C'(b_2)` lies in `Enon`, outside `↓b_i`, so in `Γ`.
(c) `x >= a > h` gives `x ∈ ↑h − [h]`, so `↑a ∩ Γ' = ∅`. `b ∈ B − C_h` is in `Fnon`, and `b > h` is impossible since `h` is a maximal F-member; so `b ∈ Γ'`. The interval is Lemma 4.4 (dual), `h ∉ Up`; `h ∈ C_h` since `∅ ≠ F_h ⊆ F#_h`.
(d) `Up ∩ L = ∅`, and `↑a ∩ L = ∅`. ∎

So bad pairs, non-members and heavy rows are gone: (a), (b) use no information on rows and columns other than Lemmas 4.4, 4.5.

### 2.3 Cross lemma (proved)

Call `P` *tie-free* if no two E-members of `P` are tied and no two F-members of `P` are tied (ties with switches off `P` are allowed).

**Lemma X.** Let `P` be tie-free, `a ∈ A`, `h ∈ B`, `a ∥ h`. There are no positions `h_1, h_2` of elements of `C(a)` and `a_1, a_2` of elements of `C'(h)` with
`h_1 <= pos(h) − 4`, `h_2 >= pos(h) + 4`, `a_1 <= pos(a) − 4`, `a_2 >= pos(a) + 4`.
*Proof.* *Chains.* `b ∈ C(a)` means `F_b ∩ F_a ≠ ∅`, or there is `w ∈ UMN(a) ∩ UMN(b)`; then `F_a, E_w, X_b` is a chain (private nodes `ρ(a,w)`, `ρ(b,w)`). So `F#_a` gives a chain of at most 3 sides `F_a` or `E_w, F_a, E_{w'}` between `X_{h_1}` and `X_{h_2}`. Likewise `a' ∈ C'(h)` means `E_{a'} ∩ E_h ≠ ∅` or there is `z ∈ LMN(h) ∩ LMN(a')`; this gives a chain `E_h` or `F_z, E_h, F_{z'}` between `X_{a_1}` and `X_{a_2}`.
*No conflicts.* Let `S` be the set of all these chain sides, together with the members kept below. Elements `w` as above satisfy `w > b` with `b ∈ B`, so `w ∉ L`; elements `z` satisfy `z < a'` with `a' ∈ A`, so `z ∉ Up`. Hence: `E_w` conflicts with no F-member; `F_z` conflicts with no E-member; `E_w`, `F_z` do not conflict (`w <= z` gives `b < w <= z < h`, against `b ∈ B`, `h` an F-member); `E_w`, `F_a` do not (`a < w`); `E_h`, `F_z` do not (`z < h`); `E_h`, `F_a` do not (`a ∥ h`). `F_a` conflicts among members only with `X_a` (an E-member `<= a` is tied with `a`, since `a ∈ A`; tie-free), `E_h` only with `X_h`.
*Counting.* A conflict-free set of sides containing a walk from `s` to `t` is picked by one mode vector (Lemma 3.4(a), argument for `L`, `Up`), so by Lemma 3.4(b) `r` is at most the number of its sides.
*Single jump.* If `h_1 < pos(a) < h_2`, then `X_1 .. X_{h_1}`, chain, `X_{h_2} .. X_r` avoids `X_a`, so `r <= h_1 + 3 + r − h_2 + 1`: `h_2 − h_1 <= 4`, against `h_2 − h_1 >= 8`. So `pos(a) ∉ (h_1, h_2)`; likewise `pos(h) ∉ (a_1, a_2)`.
*Two jumps.* The case `pos(h) < pos(a)` is the mirror image (reverse `P`). Let `pos(a) < pos(h)`. Then `pos(a) < h_1`, `a_2 < pos(h)` (positions of different types differ), so `a_1 < pos(a) < h_1 < pos(h) < h_2`, `a_1 < pos(a) < a_2 < pos(h)`.
If `a_2 < h_1`: the walk `X_1 .. X_{a_1}`, chain, `X_{a_2} .. X_{h_1}`, chain, `X_{h_2} .. X_r` avoids `X_a`, `X_h`, so `(a_2 − a_1) + (h_2 − h_1) <= 8`, against `>= 16`.
If `h_1 < a_2`: the walk `X_1 .. X_{a_1}`, chain, `X_{a_2}, X_{a_2 − 1} .. X_{h_1}`, chain, `X_{h_2} .. X_r` avoids `X_a`, `X_h`, so `(h_1 − a_1) + (h_2 − a_2) <= 8`; but `h_1 − a_1 >= 5` and `h_2 − a_2 >= 5`. ∎

### 2.4 Theorem A (proved; not reviewed)

**Theorem A.** Let `P` be a tie-free shortest valid path. Then there are at most 79 switches such that the following formula of atoms picks every member of `P`:
`D* = F* ∪ (E* ∩ X)`, `F* = FR_L ∪ FR_R ∪ ⋃_{b ∈ H_0} ↓b`, `E* = ER_U ∩ ER_V ∩ ⋂_{a ∈ E_0} (M − ↑a)`, `X = FP(h) ∪ FP(h')`.
*Proof.* If `|A| < 10`, `⋂_{a ∈ A} (M − ↑a)` works; if `|B| < 10`, `⋃_{b ∈ B} ↓b` works. Otherwise let `l(a) = min pos C(a)`, `r(a) = max pos C(a)` (`+∞`, `−∞` if empty), `u(b) = min pos C'(b)`, `v(b) = max pos C'(b)`.
Sort `A` by `l` non-increasing; `L` is the 10th value; `a^L_1`, `a^L_2` are the first and last by position among the first 10 elements, so at distance `>= 9`. `FR_L = FR(a^L_1, a^L_2)` contains all `b ∈ B` with `pos(b) < L` and misses `Up` (Lemma R(a)). Sort `A` by `r` non-decreasing; `R` is the 10th value; `FR_R` contains all `b` with `pos(b) > R`. Dually `U` (10th largest `u`), `V` (10th smallest `v`), and `ER_U ⊇ L` misses all `a` with `pos(a) < U`, `ER_V ⊇ L` misses all `a` with `pos(a) > V` (Lemma R(b)).
`E_0` = the first 9 by `l`, the first 9 by `r`, and all `a` with `pos(a) ∈ [U, U + 4) ∪ (V − 4, V]`: at most 26. `H_0` = the first 9 by `u`, the first 9 by `v`, and all `b` with `pos(b) ∈ [L, L + 4) ∪ (R − 4, R]`: at most 26. Let `A° = A − E_0` inside `[U + 4, V − 4]` and `B° = B − H_0` inside `[L + 4, R − 4]`.
For `a ∈ A°`, `b ∈ B°`: `l(a) <= L <= pos(b) − 4`, `r(a) >= R >= pos(b) + 4`, `u(b) <= U <= pos(a) − 4`, `v(b) >= V >= pos(a) + 4`, all finite. By Lemma X, `a ∥ b` is impossible; `a <= b` is impossible since `Up ∩ L = ∅`. **So `b < a`.**
If `|B°| < 18`, add `B°` to `H_0` and drop `E*`, `X`: `F*` picks `P`. If `A° = ∅`, take `D* = E*`. Otherwise take `h, h' ∈ B°` with `|pos(h) − pos(h')| >= 17`. By Lemma R(c), `X` misses `A°` and contains `B`.
Check: `F*` misses `Up` (Lemma R(a), (d)); `E* ⊇ L`. Each `b ∈ B − B°` lies in `F*`; each `b ∈ B°` lies in `E* ∩ X`. So `L ⊆ D*`. No `a ∈ A` lies in `F*`; `a ∉ A°` is outside `E*`; `a ∈ A°` is outside `X`. So `A ∩ D* = ∅` and `D* ∩ Up = ∅`. Count: `8 + 2 + 26 + 26 + 17 = 79`. ∎

**Corollary A1.** Algorithm: for every choice of at most 79 switches in the roles above, test whether the formula connects `s`, `t`. Sound for all choices, since each formula is a down-set. Time `m^{79} · poly`. It accepts every yes-instance having a tie-free shortest valid path. Not claimed for other instances.

## 3. Theorem B: the general case, with ties (proved; NOT reviewed; checks in §4)

Notation. For `w ∈ A`, `Pos[w]` is the set of positions of the E-members tied with `w` (all of them lie in `A`); for `w ∈ B`, of the F-members tied with `w` (all in `B`). `S(a) = pos C(a)`, `T(h) = pos C'(h)`. Atoms are down-sets, so an atom missing `a` misses the whole class of `a`, and an atom containing `b` contains the class of `b`.

One more atom: `EP(a)`, `a ∈ A`, the E-term with `T = T' = {a}`, `Y = Φ = ∅`. It contains every `b ∈ B` with `b < a` (`↓b ⊆ ↓a − [a]`) and misses every element of `A − win(a)`, `win(a) = A ∩ NE(E#_a)`, `|win(a)| <= 9` (Lemma 4.4). Dually `FP(h)` misses `a > h` and contains `B − win(h)`, `win(h) = B ∩ NF(F#_h)`, `|win(h)| <= 9`.

**Lemma J (one jump).** (a) If `c < d` lie in `S(a)` and `Pos[a] ⊂ (c, d)`, then `d − c <= 4`. (b) If `c < d` lie in `T(h)` and `Pos[h] ⊂ (c, d)`, then `d − c <= 4`.

**Lemma G (two jumps).** Let `a ∈ A`, `h ∈ B`, `h ≰ a`, `Z = Pos[a] ∪ Pos[h]`. Let `p_1 < p_2 < p_3 < p_4` with `p_1 ∈ T(h)`, `p_4 ∈ S(a)`, one of `p_2, p_3` in `T(h)` and the other in `S(a)`, `Z ⊂ (p_1, p_2) ∪ (p_3, p_4)`. Then `(p_2 − p_1) + (p_4 − p_3) <= 8`.
*Proof.* The chains of Lemma X (at most 3 sides each). If `p_2 ∈ T(h)`: `X_1 .. X_{p_1}`, E-chain, `X_{p_2} .. X_{p_3}`, F-chain, `X_{p_4} .. X_r`. If `p_3 ∈ T(h)`: `X_1 .. X_{p_1}`, E-chain, `X_{p_3}, X_{p_3 − 1} .. X_{p_2}`, F-chain, `X_{p_4} .. X_r`. No member kept lies in `Z`. Conflicts: `F_a` conflicts among E-members only with those `<= a`, which are tied with `a` (`a ∈ A`), so in `Pos[a]`, not kept; `E_h` likewise; `E_h`, `F_a` do not conflict as `h ≰ a`; the chain sides `E_w`, `F_z` conflict with nothing, by the list in the proof of Lemma X (it uses only `b ∈ B`, `a' ∈ A`, not tie-freeness). Counting as in Lemma X: `r <= p_1 + 3 + (p_3 − p_2 + 1) + 3 + (r − p_4 + 1)`. ∎
Lemma J is the same count with one chain. Neither lemma uses P2.

**Theorem B.** Let an instance of the general switch form with P2 have a shortest valid path `P`. Then one of four explicit monotone formulas in bounded atoms, built from at most 91 switches (shapes A, B, A', B' below), is a down-set `D` with `L ⊆ D ⊆ M − Up`; so `D` connects `s`, `t`.

*Stage 0.* If `|A| < 10` or `|B| < 10`, use `⋂ (M − ↑a)` or `⋃ ↓b`. Otherwise define `l, r, u, v`, `L, R, U, V`, `FR_L, FR_R, ER_U, ER_V` as in Theorem A. Let `E_0` = the first 9 elements by `l`, the first 9 by `r`, and all `a` with `pos(a) ∈ [U, U + 5) ∪ (V − 5, V]` (at most 28); `H_0` dually (at most 28). Let `F* = FR_L ∪ FR_R ∪ ⋃_{H_0} ↓b` (misses `Up`) and `E* = ER_U ∩ ER_V ∩ ⋂_{E_0} (M − ↑a)` (contains `L`). Let `R_0 = A ∩ E*` and `C_0 = B − F*`, closed under ties. If `C_0 = ∅`, `F*` picks `P`; if `R_0 = ∅`, `E*` picks `P`. Otherwise `L, R, U, V` are finite, and for `a ∈ R_0`, `h ∈ C_0`:
`Pos[a] ⊂ [U + 5, V − 5]`, `l(a) <= L`, `r(a) >= R`; `Pos[h] ⊂ [L + 5, R − 5]`, `u(h) <= U`, `v(h) >= V`.

*Orientation.* `U, V` are positions of E-members and `L, R` of F-members, so they differ. If `U < L` and `R < V`, then `Pos[h] ⊂ (u(h), v(h))` with `v(h) − u(h) >= V − U > 10`, against Lemma J(b). If `L < U` and `V < R`, Lemma J(a) contradicts in the same way. If `L < U` and `R < V`, reverse `P` (exchange `s`, `t`; atoms and contacts do not change). So let `U < L`, `V < R`.

*(★)* For `a ∈ R_0`, `h ∈ C_0` with `h ≰ a`, let `ρ` be a position of an element of `R_0`, `γ` a position of an element of `C_0`, `ρ ∈ T(h)`, `γ ∈ S(a)`. Then the closed interval between `ρ` and `γ` contains an element of `Pos[a] ∪ Pos[h]`.
Proof: apply Lemma G with `p_1 = u(h) <= U`, `p_4 = r(a) >= R`, `{p_2, p_3} = {ρ, γ}`. `Z ⊂ (p_1, p_4)` by the inclusions above and `U < L`, `V < R`. And `p_2 >= U + 5 >= p_1 + 5`, `p_3 <= R − 5 <= p_4 − 5`, so the sum is at least 10. ∎

*Stage 1.* Let `𝓚` be the tie classes of `R_0` and of `C_0`, each with its set of positions. If `|𝓚| < 20`, one representative per class (`M − ↑a` or `↓b`) ends the proof: `D = F* ∪ ⋃ ↓b` over the classes of `C_0`. Otherwise sort `𝓚` by the last position, let `κ_1, .., κ_20` be the first 20, `p*` the last position of `κ_20`, `tail = (p*, ∞)`. Every other class has a position in `tail`, and `κ_1, .., κ_20` have none. Let `E_κ = ⋂ (M − ↑a)`, `F_κ = ⋃ ↓b` over representatives of the `κ_i`.

*Case I: at least 10 of the `κ_i` are classes of `R_0`.* Their last positions are 10 distinct positions; `a_1`, `a_2` are the elements at the first and last of them, at distance `>= 9`; `Pos[a_i] ∩ tail = ∅`. Let `W = ⋂_{a ∈ win(a_1) ∪ win(a_2)} (M − ↑a)` (at most 18 switches) and
`F^1 = F* ∪ F_κ ∪ FR(a_1, a_2) ∪ (W ∩ (EP(a_1) ∪ EP(a_2)))`.
`F^1` misses `Up`: `W ∩ (EP(a_1) ∪ EP(a_2))` misses `A`. Let `𝓒_1` be the classes of `C_0` not contained in `F^1`. For `h` in such a class: all of `Pos[h]` lie in `S(a_1) ∪ S(a_2)` (else `FR(a_1, a_2)` contains the class), and `h ≮ a_1`, `h ≮ a_2` (else `EP(a_i)` and `W ⊇ L` contain it), so `h ≰ a_i`.
- *Shape A.* If `|𝓒_1| < 20`, `D = F^1 ∪ ⋃ ↓b` (a representative of each class of `𝓒_1`) contains `B` and misses `Up`.
- *Shape B.* Otherwise take 20 classes of `𝓒_1`, one element of each; `h_1, h_2` are at distance `>= 9` among the first 10, `h_3, h_4` among the others. Let `D = E* ∩ E_κ ∩ ER(h_1, h_2) ∩ ER(h_3, h_4)`; it contains `L`. **Claim: `D` misses `A`, or `𝓒_1` has no class outside `κ`**; in the second case `F^1` picks `P`.
*Proof of the claim.* Suppose `a ∈ A ∩ D` and some class of `𝓒_1` is outside `κ`. Then `[a]` is a class of `R_0` outside `κ`, and all its positions lie in `T(h_1) ∪ T(h_2)` and in `T(h_3) ∪ T(h_4)`. Let `Λ` be the positions in `tail` of the classes of `R_0` inside `D` and of the classes of `𝓒_1`. It contains positions of both types, so two consecutive elements `ρ` (of `R_0`), `γ` (of `C_0`) of `Λ`. Some pair, say `h_1, h_2`, has classes not containing `γ`: the two pairs use disjoint classes. Choose `h ∈ {h_1, h_2}` with `ρ ∈ T(h)` and `a' ∈ {a_1, a_2}` with `γ ∈ S(a')`. Strictly between `ρ`, `γ` there is no position of `[h]` (its class is in `𝓒_1`, so its positions in `tail` are in `Λ`) and none of `[a']` (none in `tail`); and `ρ, γ ∉ Pos[a'] ∪ Pos[h]`. With `h ≰ a'` this contradicts (★). ∎

*Case II: at least 10 of the `κ_i` are classes of `C_0`.* Dual, with `h_1`, `h_2` in these classes, `V_0 = ⋃_{b ∈ win(h_1) ∪ win(h_2)} ↓b`, `E^1 = E* ∩ E_κ ∩ ER(h_1, h_2) ∩ (V_0 ∪ (FP(h_1) ∩ FP(h_2)))`, which contains `L`, and `𝓡_1` the classes of `R_0` meeting `E^1`. *Shape A'*: `|𝓡_1| < 20`, `D = E^1 ∩ ⋂ (M − ↑a)`. *Shape B'*: otherwise `a_1, a_2` and `a_3, a_4` from disjoint classes of `𝓡_1`, `D = F* ∪ F_κ ∪ FR(a_1, a_2) ∪ FR(a_3, a_4)`, and `D` contains `B` or `𝓡_1` has no class outside `κ`: same proof, `a' ≯ h` because `a'` is in `𝓡_1`, and (★) needs nothing else.
*Count.* Shape A: `4 + 28 + 20 + 2 + 18 + 19 = 91` switches; shape B: `4 + 28 + 20 + 4 = 56`. ∎

**Corollary B1 (the open case of DC is in P, if Theorem B stands).** Algorithm for the general switch form: if `s = t` accept; otherwise, for each of the four shapes and each choice of at most 91 switches in its roles, compute the formula and test whether it connects `s`, `t`; accept iff some test succeeds. Sound: every formula is a union and intersection of down-sets, hence a mode vector. Complete: Lemma 3.4(c) and Theorem B. Time `m^{91} · poly(m, ν, σ)`. With Theorem 2.9, Construction 3.1, Lemma 3.3 of `qp-proof.md`, deciding `cp(u, v) = c(u, v)` in the open case is polynomial.

*Relation to C1.* Theorem B does not give one GDESC term; it gives a monotone formula of GDESC terms and principal sets. C1 in its literal form stays open and is not needed.

## 4. Computations (checked)

Scripts `r7-desc/check_a.py`, `check_b.py`, `check_fam.py`, `check_zz.py`, on the reviewed library `verify/rv-r6-core/zzl.py`; logs `r7-desc/runs/`. Every log ends with `FAILURES: none`. Exact shortest lengths: `zzl.all_shortest_valid_paths`, and `check_b.shortest_len` (BFS over `(side, Up, Dn)` with dominance).

| Run (log) | Instances | Outcome |
|---|---|---|
| `check_a.py x 1 3000 14 22` (`x-1.txt`) | falsification of Lemma X: planted cell with four far contacts, half through middle edges, random strict pairs; 566 cells | exact search finds a shorter path on all 566 |
| `check_b.py g 1 4000 12 22`, `g 31 6000 22 34` (`g-1.txt`, `g-31.txt`) | falsification of Lemma G with ties: planted configuration with sum `>= 9`; 236 + 666 configurations, 2 over the search budget | a shorter path on all 902 |
| `check_a.py rigid 2 300 24 60 0.0`, `rigid 3 300 24 60 0.3`, `xdesign ...`, `random 4 1500 8 14` | Theorem A's construction; rigid designs, all-strict design up to `n = 100` (branch with `X` on 3), 3418 random paths | no failure; on the tie runs no wrong formula either. Search budget for the planted-shortest check of `xdesign` beyond small `n` |
| `check_b.py rigid 2 150 30 120 0.3` | Theorem B, true thresholds, rigid designs with member ties, 150 paths | formula picks `P` on all; Stage 0 ends all of them |
| `check_b.py files` on `r5-core/runs/single/*.json`, `verify/rv-r6-core/runs/deep/*.json` | 506 shortest paths of the designs on which the proof of Theorem 5.3 needs 2-5 levels | formula picks `P` on all; no `Lemma J, G` failure |
| `check_fam.py 5 30 12` | `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k`, `Z_k`, `Z^B_k` (`k <= 5`), `X_L` (`L <= 30`), `W_n`, `OB`, `BP_n` (`n <= 12`): 80 instances, 2 over the search budget, 219 paths | no failure |
| `check_zz.py` | all 157 instances of `r4-search/instances`, 179 paths | no failure; all with `|A| < 10`, so only Lemmas J, G are tested there |
| `check_b.py xtie 21 3 6 16 16 0 10 5 20`, `22 2 6 16 16 40 ...`, `23 3 6 30 30 0 ...` | crossing classes, dense contacts, true thresholds, planted path verified shortest by exact search; 7 of 80 flips to incomparable class pairs accepted | **Stage 1, Case I reached** on all 8; `F^1` picks `P` |
| `check_b.py sat`, `sat2` (`sat-3.txt`, `sat2-1{1,2,3}.txt`) | saturated planted paths, thresholds lowered to `(3, 1, 4)`; contacts added only if the path stays shortest | no failure; Stage 0 ends all of them |

*What the checks do not cover (stated plainly).* Shapes B, A', B' and Case II were never reached: Stage 0 and `F^1` end every instance computed. So these parts rest on the proof alone. No exhaustive run can test Lemmas G, X: their hypotheses need a sum `>= 9`, hence long paths; below that every formula is trivial. The algorithm of Corollary B1 itself was not run (`m^{91}`); what is run is the construction from a known `P`.

## 5. What remains

1. **An independent referee of §2-§3, first of all Lemma G and the claim of Shape B.** Points to attack: the list of conflicts in Lemma X and Lemma G with ties and middle edges; the reversal step in *Orientation*; that `R_0`, `C_0` are closed under ties and all their positions lie in the stated intervals; that Lemma 4.4, used for far pairs, holds for every member of `A`, `B`.
2. Instances reaching Shapes B, A', B' and Case II (§4), to test those parts computationally.
3. C1 in its literal form (one term): open, not needed. Evidence of `r7-lb` (cost at most 2) suggests a much smaller exponent; not studied.
4. If the proof stands: lower the exponent 91, and assemble graph → ZZ → switch form → Theorem B into one text (`qp-proof.md` §1-§4 can be reused, §5-§6 are replaced).
