# Adversarial review of r5-core.md §6 (Theorem 6.5 and its lemmas)

Status: **final**, 2026-10-28 (started 2026-10-23 14:45). Reviewer: agent rv-core-65 (round 5, workflow run
`wf_d0b705b5-1f0`). All verdicts (§1) are final and every computation of §3 has finished and is recorded; nothing is
pending. No log shows a failure; no verdict changed since 2026-10-27.
Continued 2026-10-27 (round 6, workflow run `wf_138deda4-8fb`): line-by-line reading complete (§2), verdicts final
(§1); computations of §3.1-§3.3 complete, §3.4 (last adversarial and sampled runs) interrupted and relaunched.
Continued 2026-10-27 18:17 (round 6b, workflow run `wf_52e05843-f7f`, computations only): second relaunch, §3.5; its
runs all finished by 19:10 (before the session limit of about 19:20) but the report did not record the four
adversarial runs; recorded 2026-10-28 (round 6c, records only, no new mathematics).
Scripts and logs: `verify/rv-core-65/` and `verify/rv-core-65/runs/`. Own code written from the definitions of
`r5-core.md` §6 and `r4-general.md` §5.1; code of `r5-core/` is imported only by scripts named as cross-checks.
Labels: **holds**, **holds with repair**, **gap**, **false**; every computation with script, seed, sizes, outcome.

Text reviewed: `r5-core.md` §6 (lines 322-455) as it stood at the start of this review.
- SHA-256 of the whole file `r5-core.md` at start: `53c3ebad725aa5234e1a5f132e70c01ca29bc8582d262d24a861affe90de2a34`
- SHA-256 of lines 322-456 (§6.0-§6.4 with Corollary 6.5', 135 lines): `8f3b137663b764738430f9662037be3a66b16d6d2507a271f5dcd59c690fe6e1`
- 2026-10-27: the whole file has changed (SHA-256 `e4811861b98076755cbb8bc2160c3afdd25436d25b0e77adfbd3993cb56c7b5c`,
  §7 onward appended), lines 322-456 still have the SHA above, so the reviewed text is unchanged.

## 1. Verdicts

| Target | Verdict | Notes |
|---|---|---|
| §6.1 setting, needed items, `P`-consistent sides, facts (a)-(c) | holds | re-derived (§2.1); pick criterion `L ⊆ D ⊆ Q − Up` exact; one wording slip in §6.3 (`{w}` belongs to `NE(E#_w)` only if `E_w ≠ ∅`) |
| §6.1 GDESC and its soundness | holds | every `D` is a down-set; with `Φ ⊆ U` (as the algorithm enumerates) `∪ Φ` and `△ Φ` agree |
| Lemma 6.2 (windows of chains) | holds | the walk is itself a valid path (distinct sides of distinct switches), no sub-walk needed |
| Lemma 6.3 (stars meet at most 9 minimal E-members) | holds | every case re-derived (x on `P` or not, `z` on `P` or not, ties, empty window); the proof even gives **5** consecutive positions (span `<= 4`) in every case, so `9k` flips can be lowered to `5k`; the text's `[p − 3, p + 5]` is a correct but loose step |
| Lemma 6.4 (duality, incomparable pairs) | holds | four witness types, uses only P2 and `E_y, F_x ≠ ∅` |
| Duality for comparable pairs that are not bad (strict anchors) | holds | `x <= y` and ties are impossible for `x ∈ Up`, `y ∈ L`; strict anchors miss `Up` and `A` |
| Theorem 6.5 | holds | game, sampling (`2^{−k} < 1/m`, union bound over `|C| <= m`), both descriptions, `|Φ| <= 9k`, time `m^{O(k + κ)} poly` re-derived; wording: "decided on the instances that have ..." is a promise statement (GDESC with a given bound `κ` is correct on no-instances and on yes-instances with `κ* <= κ`); the theorem also holds with the narrower bad pairs of r5-core's code (not covered by a star) and with `x ∈ [A]`, `y ∈ [B]` exempted (§2.10); the reference "checked (§6.6)" of the table §6.0 points to a section that does not exist |
| Corollary 6.5' | holds with repair | the bound `⌈τ ln m⌉ + 1` is true (randomized rounding with one extra tool) but does not follow from the greedy bound `H(|N|) τ` cited in the proof (that is larger for `τ >= 4`, e.g. `τ = 10`, `|N| = m = 100`: `51.9 > 48`); `min(τ_E, τ_F) <= 2 + κ` holds, in fact `<= 2 + max(|X_0|, |Y_0|)`; the closing remark on matchings is unproved in the text but true: `min(τ_E, τ_F) <= 8` when the bad pairs form a matching (§2.8) |
| Theorem 6.5 with `κ = 0` is Theorem Q | holds | 2CH with classes has no strict relations, so no bad pairs, no middle edges, `E# = E`, empty strict anchors, Lemma 6.3 gives 3 positions; each GDESC description is a `σ_U^{Φ'}` of `r5-classes.md` §2a with `U` a union of `N_E[E_x]`, so GDESC(`k`, 0, `3k`) accepting implies DESC(`k`, 0, `3k`) accepting |

Computations (§3) agree with every verdict: no run of any kind produced a failure counter (§3.1-§3.5). The table is
final for the reading and for the computations.

## 2. Line-by-line reading

Notation as in `r5-core.md` §6.1. Every step below was re-derived; "✓" marks a step that holds as written.

### 2.1 Setting (§6.1)

*Model.* Matches `r4-general.md` §5.1: in ZZ the edges `R` join strictly comparable elements only (`r4-brief.md` §1), so
a middle edge `z v` has `z < v` strictly and its private node lies in `F_z` and `E_v` and in no other side ✓. P2 in
switch form: a lower witness in the bottom class gives a node of `E_x ∩ E_y`, an upper one in the top class a node of
`F_x ∩ F_y`, a middle lower witness `z` the middle edges `z x`, `z y`, a middle upper one the edges `x z`, `y z` ✓.

*`Up ∩ L = ∅`* iff no conflict pair among the members ✓. *Pick criterion:* `D` puts every F-member into F-mode iff
`W_F ⊆ D` iff `L ⊆ D` (`D` a down-set); it puts every E-member into E-mode iff `W_E ∩ D = ∅` iff `Up ∩ D = ∅` (`Q − D`
an up-set) ✓.

*(a)* `E_w`, `w ∉ L`, conflicts with an F-member `b` iff `w <= b`, i.e. `w ∈ ↓b ⊆ L` ✓; dually `F_w`, `w ∉ Up` ✓.
*(b)* `E_w`, `w ∉ L`, `w` on `P`: `w` is not an F-member (`W_F ⊆ L`), so `X_w = E_w` ✓.
*(c)* A conflict between consistent sides is `E_w`, `F_z`, `w <= z`, `w ∉ L`, `z ∉ Up`; `w ∈ Up` would give `z ∈ Up`,
`z ∈ L` would give `w ∈ L` ✓. "In particular": `E_x` with `x ∈ Up` is consistent (`Up ∩ L = ∅`) and would need
`x ∉ Up` ✓.

*GDESC.* `D = Q − ↑G` is the complement of an up-set, `D = ↓G'` a down-closure; an accepted `D` is an
order-consistent mode vector that connects `s` and `t`, hence a solution (a down-set of the middle elements extends
to a down-set of the ZZ preorder containing the bottom class and missing the top class) ✓. The text writes `∪ Φ`
where §3 and §5 write `△ Φ`; the algorithm of Theorem 6.5 takes `Φ ⊆ U`, which is disjoint from `Enon − U − S`, so
both agree ✓.

*Wording (§6.3, first paragraph).* `NE(E#_w) = NE(E_w) ∪ Sib↓(w) ∪ {w}` needs `E_w ≠ ∅` for the term `{w}`: if
`E_w = ∅`, then `LMN(w) = ∅` (a middle edge `z w` puts its private node into `E_w`), `E#_w = ∅` and `NE(E#_w) = ∅`.
Nothing later uses `w ∈ NE(E#_w)`. The identity itself is right: the private node of `z v` lies only in `E_v`.

### 2.2 Lemma 6.2

`c = d` is trivial, `c > d` reduces to `c < d` by reversing the chain ✓. The walk `X_1 .. X_c Z_1 .. Z_j X_d .. X_r`
consists of distinct sides of distinct switches (the `Z_i` are of distinct switches not on `P`), consecutive sides
meet, `s ∈ X_1`, `t ∈ X_r`, and no conflict pair occurs (members: `P` valid; member and `Z_i`: (a); `Z_i`, `Z_l`:
hypothesis). So it is itself a valid path; its length `c + j + r − d + 1 >= r` gives `d − c <= j + 1` ✓. (The text's
"shortest sub-walk" detour is not needed but is correct.) Holds.

### 2.3 Lemma 6.3 (all cases)

`a ∈ S_x = A ∩ NE(E#_x)` means `E_a = X_a` meets `E_x` (type (i)) or contains the private node of a middle edge
`z v` with `z ∈ LMN(x)`; that node lies only in `E_v`, so `v = a` and `z ∈ LMN(x) ∩ LMN(a)` (type (ii)) ✓.

*Facts for (ii).* `z < a` and `z < x` strictly (middle edges are strict). `z ∉ Up`: an E-member `a'' <= z` gives
`a'' <= z < a`; `a'' ~ a` would give `a <= z`, so `a'' < a` strictly, against `a ∈ A` ✓ (this also covers `z` tied with
an E-member). So `F_z` is `P`-consistent; it meets `X_a` (node of `z a`) and `E_x` (node of `z x`); `{E_x, F_z}` is no
conflict pair (needs `x <= z`) ✓. If `z` is on `P`, it is an F-member (`z ∉ Up`) and `X_z = F_z` ✓.

*`x` not on `P`.* `E_x` is consistent (`x ∉ L`), so `W = win(E_x)` has `max W − min W <= 2` (Lemma 6.2, `j = 1`) ✓.
Write `a ∈ (i)`, `(ii-P)` (`z` on `P`), `(ii-o)` (`z` off `P`):
- `(i)`: `pos(a) ∈ W` ✓.
- `(ii-P)`: `pos(z) ∈ W` (`X_z ∩ E_x ≠ ∅`) and `|pos(a) − pos(z)| = 1` (F1, `z ≠ a`) ✓.
- `(ii-o)`: Lemma 6.2 for the chain `F_z, E_x` (`j = 2`; distinct switches, both off `P`, consistent, no conflict)
  gives `|pos(a) − c| <= 3` for every `c ∈ W` ✓.

The text concludes `S_x ⊆ [p − 3, p + 5]` (`p = min W`), 9 positions ✓ (correct, since each `pos(a)` lies within 3
of some `c ∈ [p, p + 2]`). Sharper, pairwise: `(i)/(i)` `<= 2`; `(i)/(ii-P)` `<= 3`; `(i)/(ii-o)` `<= 3`;
`(ii-P)/(ii-P)` `<= 2 + 2`; `(ii-P)/(ii-o)` `<= 1 + 3` (chain `F_{z'}, E_x` from `X_{a'}` to `X_z`); `(ii-o)/(ii-o)`
with the same `z`: `<= 2` (window of `F_z`), with `z ≠ z'`: `<= 4` (chain `F_z, E_x, F_{z'}`, `j = 3`, distinct
switches off `P`, no conflict pair: `z, z' < x`, two F-sides). So every two elements of `S_x` are at distance `<= 4`:
**5 consecutive positions**.
*`W = ∅`.* (i) and (ii-P) are empty (a `z` on `P` would put `pos(z)` into `W`) ✓; same `z`: `<= 2`, different `z`:
`<= 4` by the 3-chain ✓ (5 positions, as the text says).
*`x` on `P`.* `x ∉ L` makes `x` an E-member, `E_x = X_x` at `e` ✓. (i): `|pos(a) − e| <= 1` (F1 or `a = x`) ✓.
(ii-P): `z` is an F-member meeting `X_a` and `X_x`, so `|pos(a) − e| <= 2` ✓. (ii-o): `F_z` consistent, off `P`,
meets `X_a` and `X_x`, so `|pos(a) − e| <= 2` (Lemma 6.2, `j = 1`) ✓. 5 positions.
*Dual.* Reversing the preorder and exchanging `E` and `F` maps instances to instances (down-sets of `≤^op` are the
complements of down-sets of `≤`, with the same picked sides; a middle edge `z v` becomes the edge `v z` of `≤^op` with
its private node in `F'_v ∩ E'_z`; conflict pairs, P2, `A`, `B`, `Up`, `L` are exchanged), so the dual statement is
the same lemma ✓.
**Holds**; the bound 9 can be replaced by 5 (so `9k` flips by `5k` in Theorem 6.5 and `9` per star in Corollary
6.5'). Checked: the largest span found in all computations of §3 is 4.

### 2.4 Lemma 6.4

P2 for `x ∥ y`: `E_x ∩ E_y ≠ ∅` gives `y ∈ NE(E_x)` (`E_y ≠ ∅`) ✓; `F_x ∩ F_y ≠ ∅` gives `x ∈ NF(F_y)` (`F_x ≠ ∅`) ✓;
a lower middle witness `z` has `z ∈ LMN(x)` and the private node of `z y` lies in `E#_x ∩ E_y` ✓; an upper middle
witness `z` has `z ∈ UMN(y)` and the private node of `x z` lies in `F#_y ∩ F_x` ✓. The lemma does not use `P`
beyond `E_y, F_x ≠ ∅`. Holds.

### 2.5 Duality with strict anchors

For `x ∈ N_F ⊆ Up`, `y ∈ N_E ⊆ L`: `x <= y` would put `x ∈ L`; a tie likewise; so a comparable pair has `y < x`
strictly ✓. Not bad means `x ∈ A` (then `y ∈ ↓x − [x]` and `y ∈ N_E`, so `y ∈ cov_E(x)`) or `y ∈ B` (then
`x ∈ cov_F(y)`) ✓. Strict anchor at `a ∈ A`: `w ∈ ↓a − [a]` means `w < a` strictly; `w ∈ Up` gives an E-member
`a'' <= w < a`, strictly below `a`; `w ∈ A` is itself such an E-member ✓. Holds.

### 2.6 Theorem 6.5

*Empty cases.* `C = N_E − Y_0 = ∅`: `U = ∅`, `S = ↓Y_0 ⊆ L`, `G = Enon − ↓Y_0`; `A ⊆ G` (`E_a = X_a ≠ ∅`, `a ∉ L`);
`G ∩ L = ∅` because `L ∩ Enon = N_E = Y_0 ⊆ ↓Y_0`; then `↑G ∩ L = ∅` (`L` a down-set) and `Up = ↑A ⊆ ↑G` ✓. `R = ∅`
dually ✓.
*Game.* Rows `R`, columns `C`, payoff `[y ∈ cov_E(x)]`, value `λ` (von Neumann) ✓.
*`λ >= 1/2`.* Some `p` on `R` covers every `y ∈ C` with probability `>= 1/2`; `k` independent draws miss a fixed `y`
with probability `<= 2^{−k}`; `k = ⌊log2 m⌋ + 1 > log2 m` gives `2^{−k} < 1/m`; union bound over `|C| <= m`
(`C ⊆ L`, in fact `|C| < m` as `R ≠ ∅`) gives failure probability `< 1`, so some draw covers `C` ✓ (repeated draws
only shrink `T`). In the description: `y ∈ L ∩ G` would be in `Enon` (`Φ ⊆ A` misses `L`), hence `y ∈ N_E`, hence in
`↓Y_0 ⊆ S` or covered (in `U`, or in `↓x_i − [x_i] ⊆ S` for a flagged `x_i ∈ T' = T ∩ A`), contradiction ✓; `L ⊆ D` ✓. `a ∈ A`:
`a ∉ U` gives `a ∈ Enon − U − S` (`↓Y_0 ⊆ L`; `↓x_i − [x_i]` misses `A`, §2.5) ✓; `a ∈ U` gives `a ∈ Φ` ✓;
`Up = ↑A` (every E-member lies above a minimal one: take an E-member below it with the least down-set) ✓, so
`D ∩ Up = ∅` ✓. `|Φ| = |∪ S_{x_i}| <= 9k` since `x_i ∈ Up` gives `x_i ∉ L` ✓ (`<= 5k` by §2.3).
*`λ < 1/2`.* Some `q` on `C` has `Pr_q[y ∈ cov_E(x)] <= λ < 1/2` for every `x ∈ R`; no pair of `R × C` is bad (every
bad pair has an end in `X_0` or `Y_0`), so by §2.4/§2.5 `Pr_q[x ∈ cov_F(y)] > 1/2`, and `k` draws cover `R` ✓.
Mirror description: `G' ∩ Up = ∅` (an element of `Up ∩ Fnon = N_F` is in `↑X_0` or in `R`, covered by `U'` or by
`↑y_i − [y_i]`, `y_i ∈ B`; `B ∩ U' ⊆ L`) ✓; `B ⊆ G'` (`F_b = X_b ≠ ∅`; `↑X_0 ⊆ Up`; `↑y_i − [y_i]` misses `B`) ✓;
`D = ↓G' ⊇ ↓B = L`, and `↓G' ∩ Up = ∅` because `Up` is an up-set and `G' ∩ Up = ∅` ✓. `|B ∩ U'| <= 9k` by the dual
of Lemma 6.3, `y_i ∈ L` ✓.
*Algorithm and time.* GDESC enumerates both kinds, `<= m^k` tool sets, `2^k <= 2m` flag patterns, `<= m^{|X_0|+|Y_0|}`
anchor sets, `<= m^{9k}` flip sets inside `U` (the needed `Φ = A ∩ U` is among them; GDESC need not know `A`), and one
connectivity test each: `m^{O(k + κ)} · poly(N, m)` ✓.
*Wording.* "ZZ + P2 is decided in time `m^{O(κ + log m)}` on the instances that have a shortest valid path with at most
`κ` bad-pair cover": GDESC(`k`, `κ`, `9k`) is sound on every instance and complete on yes-instances with
`κ* := min_P κ(P) <= κ`; without a bound on `κ*` the run cannot stop early on no-instances, so this is a promise
statement (as intended). The table of §6.0 says "`κ` anchors": correct with `(X_0, Y_0)` a minimum vertex cover
(`|Y_0|`, `|X_0| <= κ`).
**Holds.**

### 2.7 Corollary 6.5'

*Cheap tools give descriptions.* For kind E with stars `E#_w` (`w ∉ L`), strict anchors at `w ∈ A ∩ T`, F-anchors
`↓z` (`z ∉ Up`): `↓z ∩ Up = ∅`, so `S ∩ A = ∅`; a cover of `N_E` gives `G ∩ L = ∅` and `A ⊆ G` with `Φ = A ∩ U`,
`|Φ| <= 9` per star (Lemma 6.3, `w ∉ L`) ✓. Note: the anchors `↓z` need not lie in `L`; they are subtracted from the
generators, so only `↓z ∩ A = ∅` is needed (the hypothesis `B_0 ⊆ L` of the repaired Proposition 5.2' is not needed
here). Every needed item has a cheap tool (`↓y` for `y ∈ N_E`), so `τ` is finite.
*Rounding.* Claim: integer cover `<= ⌈τ ln m⌉ + 1`. True: draw `t = ⌈τ ln n⌉` tools from the optimal LP solution
normalised to a distribution (`n = |N_E| <= m`); an item is missed by all draws with probability
`<= (1 − 1/τ)^t <= e^{−t/τ} <= 1/n`, so the expected number of uncovered items is `<= 1` and some draw leaves at most
one, which one more tool covers. **Repair:** the proof cites the greedy bound `H(|N|) τ` (Lovász), which is not
`<= ⌈τ ln m⌉ + 1` in general (it exceeds it for `τ >= 4` and large `m`, e.g. `τ = 10`, `|N| = m = 100`:
`H(100) · 10 = 51.9 > 48`); with the rounding argument above, or with the weaker bound `(1 + ln m) τ`, the corollary
holds. The asymptotic content (`O(τ log m)` tools) is unaffected.
*`min(τ_E, τ_F) <= 2 + κ`.* `λ >= 1/2`: weights `2p` on the E-tools of `R` cover `C` fractionally (value 2), the
anchors `↓y`, `y ∈ Y_0` (cheap: `y ∈ L`, so `y ∉ Up`) cover `Y_0`: `τ_E <= 2 + |Y_0|`. `λ < 1/2`: weights `2q` cover `R`
(each `x` with probability `> 1/2`), anchors `↑x`, `x ∈ X_0` (cheap: `x ∉ L`): `τ_F <= 2 + |X_0|`. Empty cases:
`τ_E <= |Y_0|` or `τ_F <= |X_0|` ✓. So `min <= 2 + max(|X_0|, |Y_0|) <= 2 + κ` ✓.
*Closing remark* ("a large matching of bad pairs has `κ` large but costs nothing in the game"): not proved in the
text; see §2.8 for a proof with a constant.
*Observation.* The anchors `↓b`, `b ∈ B`, are cheap E-tools (`b ∉ Up`) and cover `N_E ⊆ L = ↓B`, so always
`τ_E <= |B|` and dually `τ_F <= |A|` (this is (E1)/(F1) of Theorem 5.2 in the language of tools). Hence
`min(τ_E, τ_F) <= min(2 + κ, |A|, |B|)`; the corollary is informative only for paths with many maximal F-members and
many minimal E-members.
**Holds with repair** (proof of the rounding constant).

### 2.8 Reviewer's remark: bad pairs of bounded degree on one side are cheap (proved here; not reviewed)

*Claim.* If every `y ∈ N_E` lies in at most `d` bad pairs, then `min(τ_E, τ_F) <= 4d + 4` (cheap tools of
Corollary 6.5', no anchors at bad pairs needed); dually if every `x ∈ N_F` lies in at most `d` bad pairs. In
particular a matching of bad pairs (`d = 1`) gives `<= 8`, whatever its size, so GDESC with
`O(d log m)` tools accepts.
*Proof.* Play the game of Theorem 6.5 on all of `N_F × N_E` (no cover removed). If `λ >= 1/2`, `τ_E <= 2`. Otherwise
take `q` on `N_E` with `Pr_q[y ∈ cov_E(x)] < 1/2` for every `x ∈ N_F`, and let `β(x) = q(bad partners of x)`. Then
`Σ_x β(x) = Σ_y q(y) · #(bad pairs at y) <= d`, so `H = {x : β(x) >= 1/4}` has `|H| <= 4d`. For `x ∉ H` the
duality fails only at bad partners, so `Pr_q[x ∈ cov_F(y)] >= 1 − Pr_q[y ∈ cov_E(x)] − β(x) > 1/4`, and weights `4q`
cover `N_F − H` fractionally with value 4; the E-anchors `↑x`, `x ∈ H` (cheap, `x ∉ L`) cover `H`. So
`τ_F <= 4d + 4`. ∎
This bears on §8 of `r5-core.md` (the bad pairs): only bad-pair graphs in which some `x` *and* some `y` have large
degree can be expensive for the fractional form.

### 2.9 Theorem 6.5 with `κ = 0` and Theorem Q

2CH with classes + P2 is a general switch form whose preorder has only ties (classes): every union of classes is a
down-set, P2 is required exactly between different classes, there are no middle edges (they need `z < v` strictly).
Theorem 6.5 uses only the switch-form axioms, so it applies. There are no strict relations, hence no bad pairs
(`κ = 0`), `E#_w = E_w`, strict anchors are empty, and in Lemma 6.3 only type (i) occurs, so `S_x` lies in 3
consecutive positions (Lemma W of `r5-classes.md`): `|Φ| <= 3k`. A GDESC E-description with tools `T` and flips
`Φ ⊆ A ∩ U` is `D = Q − ↑G`, `G = (Enon − U) ∪ Φ`; with classes `↑G` is the union of the classes meeting `G`, so a
class goes to F-mode iff all its non-empty E-sides lie in `U = ∪_{x ∈ T} N_E[E_x]` and none of its switches is
flipped: this is `σ_U^{Φ'}` of `r5-classes.md` §2a with `τ = E` and `Φ'` the classes of the flipped switches that
`σ_U` puts into F-mode (`|Φ'| <= |Φ| <= 3k`). So GDESC(`k`, 0, `3k`) accepting implies DESC(`k`, 0, `3k`) accepting,
and Theorem 6.5 with `κ = 0` gives Theorem Q (same `k`, same `3k`, same time). The games differ (Theorem Q plays on
`V × W*`, Theorem 6.5 on `N_F × N_E`; in the classes model `N_F = W*` for `T = E`), but both arguments are complete.
**Holds.** Checked in `test_classes.py` (§3).

### 2.10 Further remarks (none affects a verdict)

1. *Dangling reference.* Row 6.3 of the table §6.0 says "checked (§6.6)"; the reviewed text has no §6.6 (§6 ends
   with §6.4), and rows 6.4 and 6.5 give no check either. The checks of the lemmas are therefore not recorded in the
   reviewed text; §3 below supplies them.
2. *Narrower bad pairs.* The proof of Theorem 6.5 uses the badness of a pair only through the duality on `R × C`.
   So the theorem holds verbatim when "bad" means "bad by the order and covered by neither star" (`y ∉ NE(E#_x)`,
   `x ∉ NF(F#_y)`), which is what the code of r5-core computes (`gstar.classify`); this gives a smaller `κ` (about 39%
   of the order-bad pairs are covered by a star in the cross-check of §3.2). Checked in §3.3 (`test_narrow.py`).
3. *Tie classes of `A`, `B`.* The strict anchor at `x ∈ Up` is free (contains no element of `Up`) iff no E-member
   lies strictly below `x`, i.e. iff `x` is tied with an element of `A`. So the E-tool of a non-member `x` tied with
   some `a ∈ A` may also carry the strict anchor (`↓x − [x] = ↓a − [a]`), and pairs `(x, y)` with `x ∈ [A]` (dually
   `y ∈ [B]`) need not be counted as bad. GDESC already enumerates all flag patterns, so only the definition of `κ`
   changes.
4. *Use of §6 in §8.* `r5-core.md` §8 (appended after the reviewed version, not reviewed here) states that its
   Theorem 8.3 uses only Lemmas 6.2-6.4 of §6; all three hold (§2.2-§2.4), Lemma 6.3 even with 5 in place of 9. Its
   terms put flags ("pivots") on tools outside `A`, whose sets `↓x − [x]` may contain elements of `Up`; §8 accounts
   for this by its own damage bound, which is outside this review.

## 3. Computations

All scripts in `verify/rv-core-65/`, own code (`gsf.py`, `thy.py`, `planted.py`); logs in `runs/`. No script imports
code of another agent, except the cross-check `cross_r5core.py` (named as such). Checks in every run: facts (a)-(c), the pick criterion against all down-sets, Lemma 6.2 for
all chains of `j <= 3` consistent sides, Lemma 6.3 and its dual (span of `S_x`), Lemma 6.4, the duality with strict
anchors (test_lemmas); for every shortest valid path and several covers of its bad pairs (all minimum covers up to
6, all bad `x`, all bad `y`, random supersets): duality on `R × C`, exact fractional cover numbers `τ_E`, `τ_F`
(rational simplex), the case split `λ >= 1/2` iff `τ_E <= 2`, covers by `<= k` tools in the right case, every
inclusion-minimal cover giving a description that picks and connects with `|Φ| <= 9|T|`, the literal statement (E) or
(F), Corollary 6.5' (LP and integer cover numbers, rounding bound, `min <= 2 + κ`), and exhaustive GDESC(`k`,
`κ_min`, `9k`) against brute force for `m <= 6` (test_thm65).

### 3.1 Runs of 2026-10-23 (first part of this review)

| Run | Script, arguments | Instances | Outcome |
|---|---|---|---|
| methods-1 | `test_methods.py 1 400 4 11` | 400 (337 yes, 63 no), 547 paths | down-set method = state BFS + DFS (lengths, path sets), yes/no = brute force: no disagreement |
| enum-zz-3 | `enum_zz.py 3 6` (all ZZ instances with 3 middle elements) | 7232, 5830 with P2, 1584 yes, 1896 paths | no failure of any check; no bad pair occurs; GDESC(`k`, 0, `9k`) accepts every yes-instance and no no-instance (4246) |
| enum-zz-4 parts 1, 2, 3, 4, 6, 7 of 8 | `enum_zz.py 4 6 PART 8` | see §3.2 | no failure; parts 0 and 5 were stopped on 2026-10-23 before writing output and are re-run (§3.2) |
| json-r4search-14 | `test_json.py ../../r4-search/instances/*.json 14 20 0` | 157 files (data of r4-search, read only) | no failure; 3 instances with `κ_min = 1`; max span in Lemma 6.3: 4 |

### 3.2 Runs of 2026-10-27

Started with `launch.ps1` (PIDs, arguments and start times in `runs/pids.tsv`); each log ends with the summary of
counters; a failure would appear as a counter in capitals (`... FAILS`, `... REJECTS A YES-INSTANCE`, `... ACCEPTS A
NO-INSTANCE`, `NO COVER BY k ...`, `REVIEWER: ...`). "No failure" below means that no such counter occurs.

| Run (log) | Script, arguments | Instances | Outcome |
|---|---|---|---|
| enum-zz-4-p0-rerun, enum-zz-4-p5-rerun; total of all 8 parts: `enum-zz-4-total.txt` (`agg.py`) | `enum_zz.py 4 6 PART 8` | **all** ZZ instances with 4 middle elements: 1 535 744, of which 1 111 740 satisfy P2; 530 236 yes, 581 504 no; 785 016 shortest valid paths, 29 184 of them with a bad pair (`κ <= 1`), 15 534 yes-instances with `κ_min = 1` | no failure. GDESC(`k`, `κ_min`, `9k`) accepts all 530 236 yes-instances; GDESC(`min(k, 2)`, 1, `9k`) accepts none of the 581 504 no-instances; max span in Lemma 6.3: 2; max `min(k_E, k_F)` = 1; Lemma 6.2: max `|c − d| − j` = 0 |
| zz-check-3 | `zz_check.py 3` | all 7232 ZZ instances with 3 middle elements | ZZ answer from the definition (down-sets `D ∋ u`, `∌ v`, edges with one end in `D`) = answer of the switch form with private nodes, for all; P2 in ZZ form = P2 in switch form for all (5830 P2) |
| methods-2 | `test_methods.py 2 1500 6 15` | 1500 (1364 yes, 136 no), 2831 paths | the two path methods and brute force agree |
| lemmas-mix-201, -dmed-202, -dord-203, -ties-204 | `test_lemmas.py SEED N 6 14 30 3 PROFILE`, `N` = 600, 400, 400, 400 | 1800 random P2 instances, 1591 yes, 3843 paths, 2532 bad pairs | no failure; max span 3; max `|c − d| − j` = 1 (Lemma 6.2 tight) |
| lemmas-mix-211, -dmed-212, -dord-213, -ties-214 | `test_lemmas.py SEED N 6 16 30 3 PROFILE`, `N` = 10 000, 8000, 8000, 8000 | 34 000 random P2 instances, 30 463 yes, 77 655 paths, 61 431 bad pairs (up to 45 on one path), 25 226 incomparable pairs of `N_F × N_E`, 92 026 non-bad comparable pairs | no failure of (a)-(c), pick criterion, Lemma 6.2 (55.1 M chains with `j <= 3` and contacts at both ends; max `|c − d| − j` = 1, so the bound `j + 1` is attained), Lemma 6.3 (max span 4, attained in dense-med; max `|S_x|` = 3), Lemma 6.4, duality with strict anchors |
| zz-check-4 | `zz_check.py 4` | **all** 1 535 744 ZZ instances with 4 middle elements | ZZ answer from the definition = switch-form answer (private nodes) for all; ZZ P2 = switch-form P2 for all (1 111 740 P2) |
| thm65-both-401 | `test_thm65.py 401 20000 5 14 both 20 6` | 20 000 (18 027 yes, 1973 no), 34 384 paths, 6962 with bad pairs (up to 36 bad pairs, `κ <= 6`), 53 419 covers, 2797 yes-instances with `κ_min > 0` (up to 6) | no failure. `λ >= 1/2` in 24 363 covers, `< 1/2` in 6478 (exactly `1/2`: 1253); 83 505 descriptions from minimal covers all pick `P` and connect; max `min(k_E, k_F)` = 2 (`k = 3` or 4); max `|Φ|/|T|` = 4 (`<= 5` as in §2.3); max integer/LP = 8/5; max `min(τ_E, τ_F) − κ` = 2; GDESC(`k`, `κ_min`, `9k`) accepts all 3230 yes-instances with `m <= 6`, GDESC(`min(k, 2)`, 1, `9k`) none of 427 no-instances with `m <= 5` |
| cross-r5core-601 | `cross_r5core.py 601 2000 5 14` (**cross-check**: imports `r5-core/gcore.py`, `gstar.py`, `gdesc.py` read only) | 2000 P2 instances, 3399 paths, 3767 bad pairs, 16 995 random descriptions | stars `E#`, `F#` and `NE(E#)`, `NF(F#)`, `A`, `B`, `N_E`, `N_F`, `Up`, `L`, tool covers, vertex cover sizes and every description agree with r5-core's code. **Difference in the notion of bad pair:** `gstar.classify` calls a pair bad only if it is bad by the order *and* no star covers it; 1465 of the 3767 order-bad pairs are covered by a star. The text defines bad pairs by the order alone; the proof of Theorem 6.5 needs only the duality on `R × C`, so the theorem also holds with the narrower notion (smaller `κ`); checked in §3.3 |
| thm65-both-301, thm65-planted-302 | `test_thm65.py 301 400 5 12 both 20 6`, `test_thm65.py 302 400 6 12 planted 20 6` | 800, 752 yes, 1263 paths (278 with bad pairs, `κ <= 3`), 2007 covers | no failure; `λ >= 1/2` in 970 covers, `< 1/2` in 316, exactly `1/2` in 50; max `min(k_E, k_F)` = 2 (`k >= 3`); max `|Φ|/|T|` = 3; max `min(τ_E, τ_F) − κ` = 2; GDESC(`k`, `κ_min`, `9k`) accepts all 132 yes-instances with `m <= 6` and none of 16 no-instances |
| classes-501 | `test_classes.py 501 3000 4 12 20 7` | 3000 classes instances (1896 yes, 1104 no), 3589 paths | no bad pair; every GDESC description equals `σ_U^{Φ'}` (1640 comparisons); `|A ∩ U| <= 3|T|`, `|Φ'| <= 3k`; DESC(`k`, 0, `3k`) and GDESC(`k`, 0, `3k`) equal brute force on all 1368 instances with `m <= 7` |

*GDESC acceptance for `m >= 7`.* Exhaustive GDESC is run for `m <= 6` (and `m <= 7` in adv-kappa-14, §3.3). For
larger instances acceptance is certified per path and per minimum cover by the "literal" check of `test_thm65.py`: it
exhibits tools `T ⊆ N_F` (or `N_E`) with `|T| <= k`, flags `T ∩ A`, the anchors of the cover (`<= κ`) and the flips
`A ∩ U` (`<= 9k`) whose description picks `P`, which is a description in the search space of GDESC(`k`, `κ`, `9k`);
it never failed.

### 3.3 Narrower bad pairs, the remark of §2.8, adversarial search

| Run (log) | Script, arguments | Instances | Outcome |
|---|---|---|---|
| narrow-701 | `test_narrow.py 701 10000 5 14 both 20 6` | 9009 yes-instances, 16 752 paths, 2949 with narrow bad pairs (bad by the order and covered by no star), `κ_narrow <= 4`; on 681 paths `κ_narrow < κ`, in 205 instances `κ_min` drops | Theorem 6.5 with covers of the **narrow** bad pairs: no failure of any check of `check_cover` (18 317 covers, 26 475 descriptions); GDESC(`k`, `κ_narrow_min`, `9k`) accepts all 1594 yes-instances with `m <= 6` |
| remark-801 | `test_remark.py 801 10000 8 16 both 10` | 5140 paths with bad pairs, bad-pair degree `d` up to 6, `κ` up to 6 | remark §2.8 (`min(τ_E, τ_F) <= 4d + 4`) never fails; in fact `min(τ_E, τ_F) <= 2` on every path: the anchors `↓b`, `b ∈ B`, are cheap tools and cover `N_E ⊆ L = ↓B`, so `τ_E <= |B|` and `τ_F <= |A|` always, and random paths have few maximal F-members |
| adv-kappa-14 | `adv65.py kappa 14 300 200 5 7 7` (hill climbing on `κ_min`, 300 restarts × 200 steps) | 60 300 evaluated instances, `m` 5-7, all checks on every shortest path, 249 826 covers | no failure; `κ_min` reached 2; **exhaustive GDESC(`k`, `κ_min`, `9k`) accepts all 60 016 yes-instances evaluated** |
| find-span4-901 | `find_span4.py 901 20000 6 16 4` (dense middle edges) | 243 097 sets `S_x` (`x ∉ L`) on all shortest paths | spans: 0: 216 063, 1: 20 531, 2: 6060, 3: 121, **4: 22**, `> 4`: none. Span 4 occurs with `x` on `P` (8; `S_x = [e − 2, e + 2]`, ends through (ii-P)) and with `x` off `P`, non-empty window (14; ends through (ii-P) and (ii-o)). Saved: `runs/span4/span4-901-{1..4}.json` (instance, path, `x`). So the bound of 5 positions of §2.3 is attained, and 9 is not |

(adversarial runs on span, tools, flips and LP, and the sampled `K = 5` runs: interrupted, relaunched and finished,
§3.4 and §3.5)

### 3.4 Interrupted runs and their re-runs (round 6b, 2026-10-27, from 17:02)

The coordinator stopped all processes on 2026-10-27 at about 10:52-10:55. Killed (logs end without a summary):
`adv65.py span 11 400 300 8 14 0 runs/adv`, `adv65.py tools 12 400 300 8 14 0 runs/adv`, `adv65.py phi 13 300 300
8 14 0 runs/adv`, `adv65.py lp 15 300 300 8 14 0 runs/adv` (started 10:30), and `sample_zz5.py 5 200 1 6 P 3`,
`P = 0, 1, 2` (started 10:36). Their partial logs (`runs/adv-*.txt`, `runs/zz5-sample-p*.txt`) are kept unchanged.
The re-runs use the same arguments (all scripts are deterministic for a given seed), with new log tags
(`*-rerun.txt`) and the adversarial best instances in `runs/adv-rerun/`; PIDs in `runs/pids.tsv`.
Status of this subsection: historical. These re-runs were stopped by the coordinator at 17:08-17:10 and relaunched
under the tags `*-rerun2` (§3.5), which finished; the outcomes are in §3.5. The two finished runs at the end of this
subsection (`lemmas-dmed-j4-221`, `thm65-planted-402`) are complete.

**Still running when this agent had to hand in its output (2026-10-27 17:06; no failure counter, empty `.err` so
far; stopped at 17:08-17:10, see §3.5)**, all in `verify/rv-core-65/`, logs in `runs/`:

| PID | Log | Command | Progress at 17:06 | Expected end |
|---|---|---|---|---|
| 23536 | `adv-span-11-rerun.txt` | `python -u adv65.py span 11 400 300 8 14 0 runs/adv-rerun` | 33 of 400 restarts | about 17:40 |
| 13160 | `adv-tools-12-rerun.txt` | `python -u adv65.py tools 12 400 300 8 14 0 runs/adv-rerun` | 37 of 400 | about 17:35 |
| 14296 | `adv-phi-13-rerun.txt` | `python -u adv65.py phi 13 300 300 8 14 0 runs/adv-rerun` | 25 of 300 | about 17:35 |
| 37036 | `adv-lp-15-rerun.txt` | `python -u adv65.py lp 15 300 300 8 14 0 runs/adv-rerun` | 24 of 300 | about 17:40 |
| 7524, 30412, 19936 | `zz5-sample-p{0,1,2}-rerun.txt` | `python -u sample_zz5.py 5 200 1 6 P 3`, `P = 0, 1, 2` | 400 of 2314 preorders each | about 17:20 |

A finished run ends with a summary (`adv65 target ...`, `sample_zz5 K ...`) followed by the counters; a failure
appears as a counter in capitals (§3.2). (The summaries of the relaunch are recorded in §3.5; the three `zz5` parts
are aggregated there with `agg.py`.)

*Determinism.* After about 90 s the first 16-21 restart lines of each adversarial re-run were compared with the killed
logs (elapsed times removed): identical. So the killed logs are prefixes of the re-runs.

*Killed logs at the moment of the stop* (no failure counter in any of them): span-11 237 of 400 restarts (71 337
evaluations), tools-12 266 of 400 (80 066), phi-13 219 of 300 (65 919), lp-15 173 of 300 (52 073); maxima over the
four: span in Lemma 6.3 4, `κ_min` 6, `min(k_E, k_F)` 2, `|Φ|/|T|` 3, `min(τ_E, τ_F) − κ` 2, integer/LP 8/5.
`zz5-sample-p0/1/2`: each at 2200 of its 2314 preorders (6942 preorders on 5 elements in all; the docstring's
"4231" is the number of partial orders) when killed; they print only progress lines, so their counters were lost.

*Two finished runs of 2026-10-27 morning that §3.3 did not record.* Their logs (`runs/lemmas-dmed-j4-221.txt`,
`runs/thm65-planted-402.txt`, written by a foreground call, without a `pids.tsv` line) end with a complete summary;
the command line was read off the summary header and both were re-run under `launch.ps1`: the summaries agree
counter for counter.

| Run (log) | Script, arguments | Instances | Outcome |
|---|---|---|---|
| lemmas-dmed-j4-221, -rerun | `test_lemmas.py 221 1500 6 12 20 4 dense-med` (chains up to `j = 4`) | 1500 random P2 instances (1211 yes, 289 no), 2467 paths, 1153 bad pairs (up to 18 on a path) | no failure; Lemma 6.2 on 1 874 647 chains with contacts (`j = 1..4`: 19 785, 71 854, 332 856, 1 450 152), max `|c − d| − j` = 1; Lemma 6.3 max span 3, max `|S_x|` = 4; Lemma 6.4 on 880 incomparable pairs |
| thm65-planted-402, -rerun | `test_thm65.py 402 3000 12 16 planted 10 0` (planted paths, `m` 12-16) | 3000 yes-instances, 6510 paths, 3021 with bad pairs (up to 42 on a path, `κ <= 6`), 1195 instances with `κ_min > 0` (up to 6), 15 151 covers | no failure; `λ >= 1/2` in 9321 covers, `< 1/2` in 2357 (exactly `1/2`: 515); 35 565 descriptions from minimal covers; max `min(k_E, k_F)` = 2 (`k = 4` or 5); max `|Φ|/|T|` = 4; max integer/LP = 3/2; max `min(τ_E, τ_F) − κ` = 2 |

### 3.5 Round 6b, second relaunch (2026-10-27, from 18:17)

The re-runs of 17:02 (§3.4) were stopped by the coordinator at about 17:08-17:10 (logs end at 17:10 without a
summary; empty `.err`). Their logs, kept unchanged, reached 92 (span), 97 (tools), 75 (phi), 69 (lp) restart lines
and 1200 preorders per `zz5` part; no failure key occurs in them. In `adv65.py` every restart line prints all failure
keys that are non-zero (and a failure prints `FAILURE saved ...` at once), so every partial adversarial log certifies
"no failure" for the restarts it shows; `sample_zz5.py` prints only progress lines, so its counters exist only in
a finished log.

Relaunched 2026-10-27 18:17 with `launch.ps1`, same arguments, new tags `*-rerun2`, adversarial best instances in
`runs/adv-rerun2/` (7 processes; PIDs in `runs/pids.tsv`):

| PID | Log | Command |
|---|---|---|
| 25596 | `adv-span-11-rerun2.txt` | `python -u adv65.py span 11 400 300 8 14 0 runs/adv-rerun2` |
| 15364 | `adv-tools-12-rerun2.txt` | `python -u adv65.py tools 12 400 300 8 14 0 runs/adv-rerun2` |
| 35088 | `adv-phi-13-rerun2.txt` | `python -u adv65.py phi 13 300 300 8 14 0 runs/adv-rerun2` |
| 21000 | `adv-lp-15-rerun2.txt` | `python -u adv65.py lp 15 300 300 8 14 0 runs/adv-rerun2` |
| 27028, 1808, 21004 | `zz5-sample-p{0,1,2}-rerun2.txt` | `python -u sample_zz5.py 5 200 1 6 P 3`, `P = 0, 1, 2` |

All seven processes ran to the end (the `zz5` parts finished 18:40, the adversarial runs between 19:00 and 19:10);
none was stopped, no Python process of this review is left, every `.err` is empty, no `FAILURE` line occurs in any
log and no `fail-*.json` file exists in `runs/` or `runs/adv-rerun2/`. Outcomes below.
*Progress 18:50* (adversarial runs still running, no failure key, empty `.err`): span 252 of 400 restarts, tools 274
of 400, phi 229 of 300, lp 182 of 300; so all four already exceeded the killed logs of 10:30.
*Determinism.* The first 4-8 restart lines of each adversarial run (elapsed times removed) are identical to the killed
logs of 10:30 (`adv-*.txt`); so the killed logs and the `-rerun` logs of 17:02 are prefixes of these runs. Checked
again on the finished logs (2026-10-28, restart lines with the elapsed times removed): the 237, 266, 219, 173 restart
lines of the killed logs (span, tools, phi, lp) and the 92, 97, 75, 69 lines of the `-rerun` logs are identical,
line for line, to the first lines of the `-rerun2` logs (400, 400, 300, 300 lines).

| Run (log) | Script, arguments | Instances | Outcome |
|---|---|---|---|
| zz5-sample-p0/p1/p2-rerun2; total `runs/zz5-sample-total.txt` (`agg.py`; its line "preorders (all parts)" sums the three copies of 6942 and is meaningless) | `sample_zz5.py 5 200 1 6 P 3`, `P = 0, 1, 2` (rng seed `1000 + P`; 1338-1353 s each, finished 18:40) | **every** preorder on 5 middle elements (6942), 200 sampled edge sets each (edge probability from {0.3, 0.5, 0.7}): 1 388 400 ZZ instances, 506 650 with P2; 372 958 yes, 133 692 no; 903 280 shortest valid paths, 69 382 with bad pairs (at most 2 on a path, `κ <= 1`), 13 698 yes-instances with `κ_min = 1` | no failure (no failure key in any summary, empty `.err`). Facts (a)-(c) (1 685 977 conflicting consistent pairs), pick criterion; Lemma 6.2 on 12 763 281 chains with contacts (`j <= 3`), max `|c − d| − j` = 1; Lemma 6.3 and dual max span 2, max `|S_x|` = 2; Lemma 6.4 on 6822 incomparable pairs; duality with strict anchors on 1 069 810 non-bad comparable pairs; 1 056 489 covers, `λ >= 1/2` in 639 840, `< 1/2` in 10 268 (exactly `1/2`: 12); 1 637 864 descriptions (E'), (F') and 1 444 107 of Cor. 6.5' all pick and connect; max `min(k_E, k_F)` = 1; max `|Φ|/|T|` = 2; max integer/LP = 4/3; max `min(τ_E, τ_F) − κ` = 1. Exhaustive GDESC (`m = 5 <= 6`): GDESC(`k`, `κ_min`, `9k`) accepts all 372 958 yes-instances (even GDESC(`k`, 0, `9k`) accepts all of them: the counter of yes-instances needing anchors is absent), GDESC(`min(k, 2)`, 1, `9k`) accepts none of the 133 692 no-instances |
| adv-span-11-rerun2 (PID 25596; start 18:17, end 19:09) | `adv65.py span 11 400 300 8 14 0 runs/adv-rerun2` (hill climbing on the span of `S_x`; seed 11, 400 restarts × 300 steps, `m` 8-14, `GD = 0`: no exhaustive GDESC) | 3128 s; 400 restart lines; **120 400 evaluated instances** (400 × 301), all checks on all their shortest valid paths; 625 086 covers tested; 1 920 442 bad pairs; best score `76/25` (`runs/adv-rerun2/best-span-11.json`) | no failure counter printed (no `FAILURE` line, empty `.err`). Max span in Lemma 6.3 (E, F) = 3 (3), max `\|S_x\|` (`\|S_y\|` dual) = 4 (4); Lemma 6.2 max `\|c − d\| − j` = 1; max `\|Φ\|/\|T\|` = 3 (E), 3 (F); max `min(k_E, k_F)` = 2; max `κ_min` = 5; max `min LP cover − κ` = 2; max integer/LP = 8/5; `λ >= 1/2` in 306 502 covers, `< 1/2` in 33 097, exactly `1/2` in 2643 |
| adv-tools-12-rerun2 (PID 15364; 18:17-19:06) | `adv65.py tools 12 400 300 8 14 0 runs/adv-rerun2` (hill climbing on `min(k_E, k_F)`; seed 12, 400 × 300, `m` 8-14, `GD = 0`) | 2896 s; 400 restart lines; **120 400 evaluated instances**; 568 838 covers; 2 283 850 bad pairs; best score `13/5` (`best-tools-12.json`) | no failure counter printed (no `FAILURE` line, empty `.err`). Max span (E, F) = 4 (4), max `\|S_x\|` (dual) = 4 (4); max `\|c − d\| − j` = 1; max `\|Φ\|/\|T\|` = 3 (3); max `min(k_E, k_F)` = 2; max `κ_min` = 6; max `min LP cover − κ` = 2; max integer/LP = 8/5; `λ >= 1/2` in 293 781 covers, `< 1/2` in 34 347, exactly `1/2` in 12 062 |
| adv-phi-13-rerun2 (PID 35088; 18:17-19:00) | `adv65.py phi 13 300 300 8 14 0 runs/adv-rerun2` (hill climbing on `\|Φ\|/\|T\|`; seed 13, 300 × 300, `m` 8-14, `GD = 0`) | 2584 s; 300 restart lines; **90 300 evaluated instances**; 470 711 covers; 1 440 078 bad pairs; best score `3` (`best-phi-13.json`) | no failure counter printed (no `FAILURE` line, empty `.err`). Max span (E, F) = 4 (4), max `\|S_x\|` (dual) = 4 (4); max `\|c − d\| − j` = 1; max `\|Φ\|/\|T\|` = 3 (3), so the bound `<= 5` of §2.3 is not reached; max `min(k_E, k_F)` = 2; max `κ_min` = 6; max `min LP cover − κ` = 1; max integer/LP = 8/5; `λ >= 1/2` in 248 423 covers, `< 1/2` in 21 041, exactly `1/2` in 1657 |
| adv-lp-15-rerun2 (PID 21000; 18:17-19:09) | `adv65.py lp 15 300 300 8 14 0 runs/adv-rerun2` (hill climbing on `min(τ_E*, τ_F*) − κ`; seed 15, 300 × 300, `m` 8-14, `GD = 0`) | 3120 s; 300 restart lines; **90 300 evaluated instances**; 335 399 covers; 735 019 bad pairs; best score `1` (`best-lp-15.json`) | no failure counter printed (no `FAILURE` line, empty `.err`). Max span (E, F) = 4 (3), max `\|S_x\|` (dual) = 3 (3); max `\|c − d\| − j` = 1; max `\|Φ\|/\|T\|` = 3 (3); max `min(k_E, k_F)` = 2; max `κ_min` = 6; max `min LP cover − κ` = 1; max integer/LP = 8/5; `λ >= 1/2` in 152 414 covers, `< 1/2` in 12 838, exactly `1/2` in 691 |

The four rows together: 421 400 evaluated instances (120 400 + 120 400 + 90 300 + 90 300), 2 000 034 covers tested.
Counters common to all four summaries, as printed (span / tools / phi / lp): `(E') descriptions` 639 197 / 630 690 /
520 881 / 312 070; `(F') descriptions` 846 462 / 736 782 / 683 633 / 380 971; `cor 6.5' descriptions` 906 505 /
801 465 / 703 547 / 483 470; `(c) conflicting consistent pairs` 4 359 421 / 3 951 858 / 3 715 468 / 3 197 661;
`6.2 chains with contacts j=1` 5 551 631 / 4 872 899 / 4 395 819 / 3 255 910, `j=2` 26 903 938 / 23 719 092 /
22 594 040 / 17 433 468; `6.4 incomparable pairs` 515 073 / 499 420 / 347 764 / 169 320; `comparable pairs
(anchored)` 2 301 401 / 1 937 961 / 1 796 650 / 992 450; `comparable pairs (bad)` = `bad pairs`; `case C empty`
138 821 / 117 445 / 109 423 / 93 656; `case R empty` 146 666 / 123 265 / 91 824 / 76 491; `improvements` 265 / 614 /
167 / 135; `max bad pairs on a path` 36 in all four. Every failure key of `adv65.py` (`FAILKEYS`: 41 names, e.g.
`LEMMA 6.3 FAILS`, `GDESC(k, kappa_min, 9k) REJECTS A YES-INSTANCE`, `REVIEWER: SPAN > 4`, `REVIEWER: |Phi| > 5|T|`)
is absent from every restart line and from every summary. These runs use `GD = 0`, so they do not test GDESC
acceptance (that is done exhaustively in `adv-kappa-14`, `enum-zz-4`, `zz5-sample`, §3.2-§3.5).
Maxima over the four runs: span in Lemma 6.3 = 4 (so the bound of 5 positions of §2.3 is respected and, as in
`find-span4-901`, attained; the loose bound 9 is not); `|Φ|/|T|` = 3 (`<= 5`); `min(k_E, k_F)` = 2 (`<= k`, as
`k >= 4` for `m >= 8`); `min(τ_E, τ_F) − κ` = 2 (Corollary 6.5' claims `<= 2`: the bound is attained, in the span and
tools runs); max integer/LP = 8/5; `κ_min` up to 6; `max |c − d| − j` = 1 (Lemma 6.2: the bound `j + 1` is
attained). These are the same maxima as in the killed logs of 10:30 (§3.4), reached again by the full runs, so the
longer runs found nothing new. No verdict of §1 changes.

## 4. Scripts

| Script | What |
|---|---|
| `gsf.py` | general switch form from the definitions (instances, preorder, P2, down-sets, brute force, all shortest valid paths by two methods, ZZ -> switch form converter `from_zz`, random generator with P2 repair) |
| `thy.py` | objects of §6: `Skel` (members, `Up`, `L`, `A`, `B`, `N_E`, `N_F`), `Stars` (`E#`, `F#`), `cov_E`, `cov_F`, bad pairs, minimum vertex covers, the descriptions of Theorem 6.5, exact LP cover number (rational simplex), integer covers, exhaustive GDESC |
| `planted.py` | planted paths with many bad pairs (chain types E/F, relations down-mate < up-mate), P2 by fresh nodes or middle witnesses |
| `test_methods.py` | self-check of the exact routines |
| `test_lemmas.py` | facts (a)-(c), pick criterion, Lemmas 6.2, 6.3, 6.4, duality with strict anchors, on every shortest valid path |
| `test_thm65.py` | Theorem 6.5 (per path and cover), Corollary 6.5', GDESC against brute force |
| `test_classes.py` | `κ = 0` against Theorem Q: classes instances, GDESC descriptions = `σ_U^{Φ'}`, DESC(`k`, 0, `3k`) and GDESC(`k`, 0, `3k`) against brute force |
| `enum_zz.py` | all ZZ instances with `K` middle elements (every preorder, every edge set of strict pairs), checks of test_lemmas and test_thm65 |
| `test_json.py` | the same checks on stored ZZ instances (`r4-search/instances`, read only) |
| `diag_planted.py` | diagnostic: how often the planted path stays shortest |
| `launch.ps1` | starts background runs and records PID, log and arguments in `runs/pids.tsv` |
| `agg.py` | sums the counters of several logs (maxima for `max` keys) |
| `zz_check.py` | end-to-end check of the private-node model: ZZ answer and ZZ P2 from the definitions against the switch form, all instances with `K` middle elements |
| `sample_zz5.py` | every preorder on `K = 5` middle elements with sampled edge sets, checks of enum_zz |
| `test_narrow.py` | Theorem 6.5 with covers of the narrow bad pairs (order-bad and covered by no star) |
| `test_remark.py` | the reviewer's remark §2.8 |
| `adv65.py` | adversarial hill climbing (targets: span of `S_x`, number of tools, `|Φ|/|T|`, `κ_min` with exhaustive GDESC, LP cover minus `κ`); all checks on every evaluated instance |
| `find_span4.py` | instances with span 4 in Lemma 6.3 (tightness of the bound 5) |
| `cross_r5core.py` | **cross-check** against `r5-core/gcore.py`, `gstar.py`, `gdesc.py` (imported read only) |
