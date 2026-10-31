# Adversarial review of r5-core.md §8 (Lemma 8.1, Theorem 8.2, IDESC, Corollary 8.3)

Status: complete, 2026-10-27 (started 17:07, continued from the skeleton in the relaunch `wf_52e05843-f7f`).
Reviewer: agent rv-r6-core (round 6b). Scripts and logs: `verify/rv-r6-core/` and `verify/rv-r6-core/runs/`. Own code
written from the definitions of `r5-core.md` §3.1, §6.1, §6.3, §8.2 and `r4-general.md` §5.1 (and the ZZ definition of
`r4-brief.md` §1); code of `r5-core/` is imported only by scripts named as cross-checks.
Labels: **holds**, **holds with repair**, **gap**, **false**; every computation with script, seed, sizes, outcome.

Text reviewed: `r5-core.md` §8, lines 505-721 (§8.0-§8.5), as it stood at the start of this review.
- SHA-256 of the whole file `r5-core.md` at start: `d96d9e9e530874f5e193c9857a8a541706114443acd6e0251d605f8784ec8771`
  (re-checked at the relaunch: unchanged)
- SHA-256 of lines 505-721 (§8.0-§8.5): `cc80bbf050dd0f8ecd15a97c062901f00d36f35a0c1e94f2590f079a21c49077`
- SHA-256 of lines 533-655 (§8.2-§8.3, the proofs): `5be4136f38a14cbe7a5e95124056de8f067aa97d3c2e495059f004748958e0e7`
- Used from earlier sections (not re-reviewed line by line, but re-derived where §8 uses them): §6.1 (setting), §6.3
  (Lemmas 6.3, 6.4; reviewed in `verify/rv-core-65.md`: hold), Lemma 6.2.

## 1. Verdicts

Final (2026-10-27 evening). Reading §2 complete; computations §3 complete (two late deep runs are recorded in §3.2
with their state).

| Item | Verdict | Note |
|---|---|---|
| Facts F0-F4 | **holds** | re-derived from the definitions (§2.1); `Up = ↑A`, `L = ↓B`, `Up ∩ L = ∅` from validity only |
| Lemma 8.1 | **holds** | every step re-derived (§2.2-§2.5); Lemmas 6.3, 6.4 used only under their hypotheses (rows in `↑A' ∩ Fnon ⊆ N_F`, so outside `L`; columns `N_E ⊆ L`, so outside `Up`; `P` shortest); duality exhaustive over `x <= y` (impossible), `y < x` (pivot), `x ∥ y` (Lemma 6.4), ties included; damage bound and both inclusions hold for **any** cover by `<= k` rows. One sentence to add: for `m = 1`, `N = 0` and the strict bound for heavy rows is false, but there is no heavy row then (§2.4). Checked: no failure on all ZZ instances with `<= 4` middle elements (785 016 + 1896 shortest paths), on about 3100 adversarial designs (`m` up to 338, up to 572 bad pairs on a path), 4500 random instances and r5-core's 24 stored instances; boundaries `|dam| = θ` and `|A''| = |A'|/2` attained |
| Theorem 8.2 | **holds** | §2.6; levels `<= ⌊log2 m⌋ + 1` because each continue step halves a non-empty residue; the induction `D_1 ∩ .. ∩ D_i ∩ Up ⊆ ↑A^(i+1)` and the final term give `D ∩ Up = ∅`, `L ⊆ D`. Checked with up to 5 levels (`m` up to 338) |
| IDESC soundness | **holds** | every tested set is an intersection of down-sets; the switch form equals ZZ on every down-set (checked on all 1.1 M P2 instances with 4 middle elements). Checked: 301 M + 6.9 M enumerated terms all down-sets; no term connects on any sampled no-instance |
| IDESC completeness | **holds** | the terms of the proof are in the search space (tools `<= k`, any flag pattern, flips `A' ∩ U ⊆ U` resp. `B ∩ U' ⊆ U'`, `<= 9k`, anchors only in the last F-term, `<= N` in total); checked: every yes-instance of the exhaustive sets accepted, every constructed intersection connects (switch form and ZZ graph) |
| Time bound | **holds** (wording repair) | the sequence count `(2^{k+1} m^{10k})^k m^N` assumes the anchors in one term, while IDESC as defined allows `<= a` anchors spread over the terms: count `(2^{k+1} (m+1)^{10k})^k (k(m+1))^N`, or restrict IDESC to the shape of Theorem 8.2; either way `m^{O(log^2 m)} · poly` (§2.8) |
| Corollary 8.3 | **holds** | conditional only on the polynomial reduction of `theory-dc.md` Theorem 13 (reviewed in `verify/equivalence.md`, not re-reviewed here) and the polynomial conversion to the switch form; `2^{O(log^3 n)}`; "not NP-complete unless NP ⊆ QP" and "not under ETH" follow (§2.9) |
| §8.4 (computations) | **holds** as far as re-computed | r5-core's 24 stored instances re-run with own code: 2 levels of the proof's kind on all, one GDESC term with one tool suffices on all (§3.2, §3.4) |

**Overall: the quasi-polynomial bound for the open case of DC stands as stated** (Theorem 8.2, IDESC, Corollary 8.3),
with two wording repairs that do not change any statement. No hidden use of Theorem 6.5, of shortestness beyond Lemma
6.3, or of a property of `A` or `B` that fails with ties was found.

## 2. Line-by-line reading

### 2.1 Setting and facts F0-F4

Definitions used (from `r5-core.md` §6.1, §3.1, `r4-general.md` §5.1): switches `Q` (middle elements) with a preorder
`<=`; `w < z` means `w <= z` and not `z <= w`; `[x]` the tie class, `↓x − [x]` the strictly lower elements. Modes: a
down-set `D` of `Q` (F-mode = in `D`); picked side `F_w` for `w ∈ D`, `E_w` otherwise. A valid path `P = X_1 .. X_r`:
`s ∈ X_1`, `t ∈ X_r`, `X_i ∩ X_{i+1} ≠ ∅`, distinct switches, no conflict pair `{E_w, F_z}` with `w <= z`.
`W_E`, `W_F` the E- and F-members, `Up = ↑W_E`, `L = ↓W_F`; `A` = E-members with no E-member strictly below,
`B` = F-members with no F-member strictly above. `Enon`, `Fnon`: switches with non-empty E- resp. F-side.
`NE(Z) = {w : E_w ≠ ∅, E_w ∩ Z ≠ ∅}`, `NF(Z)` dually; `N_E = L ∩ Enon`, `N_F = Up ∩ Fnon`.

- `Up ∩ L = ∅`: `w ∈ Up ∩ L` gives an E-member `e <= w` and an F-member `f >= w`, so `e <= f` and `{E_e, F_f}` is a
  conflict pair of `P` (`e ≠ f` as switches of `P` are distinct, and `e = f` is excluded anyway). Holds.
- **F0.** `D` picks every E-member iff `W_E ∩ D = ∅` iff `Up ∩ D = ∅` (`D` down-set: `w ∈ Up ∩ D`, `e <= w`, `e ∈ W_E`
  gives `e ∈ D`); `D` picks every F-member iff `W_F ⊆ D` iff `L ⊆ D`. Then every side of `P` is a picked side, and
  `P` is an `s`-`t` walk in the picked hypergraph. `Up = ↑A`: from an E-member, strict descent inside `W_E` stops
  (finite preorder; a strict chain has no repetition), and its end is in `A`. **Holds.**
- **F1** (Lemma 6.3) and **F2** (Lemma 6.4): taken from §6.3 (reviewed: hold, `verify/rv-core-65.md` §2.3, §2.4);
  their hypotheses at the places of use are checked in §2.3, §2.4 below. The proof of Lemma 6.4 was re-read: a common
  E-node gives `y ∈ NE(E_x)` (`E_y ≠ ∅`), a common F-node `x ∈ NF(F_y)` (`F_x ≠ ∅`), a lower middle witness `z` gives the
  private node of `z y` in `E#_x ∩ E_y`, an upper one the private node of `x z` in `F_x ∩ F#_y`. It needs `E_y ≠ ∅` and
  `F_x ≠ ∅` (both given by `x ∈ N_F`, `y ∈ N_E`) and P2 for the incomparable switches `x`, `y` (P2 of ZZ restricted to
  middle elements; a bottom or top is comparable with everything). Direction needed: ZZ P2 implies switch-form P2 (a
  common bottom neighbour gives a common E-node, a common middle neighbour strictly below both a lower middle witness,
  dually above); the converse is not needed (a common node may come from two bottoms of one component). Holds.
- **F3.** `a, a' ∈ A`, `a' < a` contradicts the definition of `A` (`a'` is an E-member). `w > b` (`b ∈ B`) and
  `w <= b'` (`b' ∈ B`) give `b < b'` (strict: `b' <= b` would give `w <= b`), against the maximality of `b`.
  `↑a ⊆ ↑W_E = Up` and `Up ∩ L = ∅`. **Holds**, also with ties: tied members are never "strictly" below each other.
- **F4.** `w ∈ ↓G' ∩ V`, `w <= g' ∈ G'`, `V` up-set gives `g' ∈ V`; dually. **Holds.**
- `D(τ)` is a down-set: `Q − ↑G` is the complement of an up-set, `↓G'` a down-closure. **Holds.**
- The terms of §8.2 coincide with the E- and F-descriptions of §6.1 (flags allowed on any tool: §6.1 has `T' ⊆ T`
  arbitrary) and with `gdesc.describe` of r5-core (read: same formulas, flips added to the generators). Holds.

### 2.2 Lemma 8.1: rows, columns, light and heavy, the duality claim

- `R = ↑A' ∩ Fnon ⊆ Up ∩ Fnon = N_F`, `C = N_E`. A row is never in `L`, a column never in `Up`.
- `dam(x) = A' ∩ (↓x − [x])`; `dam(a) = ∅` for `a ∈ A'` (F3, ties excluded by `− [a]`). Every element of `A'` is light.
- *Duality for light `x ∈ R`, `y ∈ C`.* The three cases `x <= y` (including ties), `y < x`, `x ∥ y` are exhaustive for a
  preorder. `x <= y`: `x ∈ ↓y ⊆ L`, impossible (`x ∈ Up`). `y < x`: `y ∈ (↓x − [x]) ∩ C ⊆ cov_E(x)` (light). `x ∥ y`:
  Lemma 6.4 with `x ∈ N_F`, `y ∈ N_E` gives `y ∈ NE(E#_x) ∩ C ⊆ cov_E(x)` or `x ∈ NF(F#_y) ∩ R ⊆ cov_F(y)`.
  **Holds.** Ties between a row and a column are impossible (`x ~ y` gives `x <= y`). The case `y < x` with `y ∈ B` is
  covered twice (pivot of `x`, strict anchor of `y`); with `x` heavy it is not claimed (and not needed).
- Lemma 6.4 is applied only to rows (`x ∈ Up`, `F_x ≠ ∅`, so `x ∈ N_F`, `x ∉ L`) and columns (`y ∈ N_E`). Holds.

### 2.3 Lemma 8.1, trivial cases and the case `v >= 1/2`

- `C = ∅`: `G = Enon`, `G ∩ L = N_E = ∅`, F4 gives `L ⊆ D`; `A' ⊆ Enon` (an E-member's side `X_a = E_a` is non-empty:
  it contains `s` or meets a neighbouring side), so `↑A' ⊆ ↑G` misses `D`. `R = ∅`: `G' = Fnon`, `G' ∩ ↑A' = R = ∅`,
  F4; `B ⊆ Fnon` (`X_b = F_b ≠ ∅`), `L = ↓B` (every F-member lies below a maximal one, finite preorder), so `L ⊆ D`.
  Both final, without tools, anchors or flips. **Holds.**
- The game has non-empty `R`, `C`; `|R|, |C| <= m`. With `p` optimal, `Pr[y ∉ cov_E(x_i)] <= 1/2` per draw, so
  `Pr[y uncovered by k draws] <= 2^{-k}`; `k = ⌊log2 m⌋ + 1` gives `2^k > m`; the union bound over `|C| <= m`
  columns gives failure probability `<= |C| 2^{-k} < |C|/m <= 1`. Strict, also for `m = 1, 2`. Repeated draws only
  shrink `T`. **Holds.**
- `L ⊆ D(τ)`: `G ∩ L ⊆ (Enon ∩ L − U − S) ∪ (Φ ∩ L)`; `Enon ∩ L = C`, each `y ∈ C` is in `NE(E#_{x_i}) ⊆ U` or, for a
  light `x_i`, in `↓x_i − [x_i] ⊆ S`; `Φ ⊆ A' ⊆ Up`. So `G ∩ L = ∅`, F4. **Holds.**
- Flips: `Φ = A' ∩ U ⊆ ∪_i (A ∩ NE(E#_{x_i}))`; each `x_i ∈ R ⊆ Up` is outside `L`, the hypothesis of Lemma 6.3; `P` is
  shortest (Theorem 8.2 picks a shortest `P`; Lemma 6.3 is the only place where shortestness enters). `|Φ| <= 9k`
  (`5k` by the sharper bound of `verify/rv-core-65.md`). `Φ ⊆ U`, so it is a flip set of IDESC. **Holds.**
- Damage: `a ∈ A' − U − S` lies in `Enon − U − S ⊆ G`; `a ∈ A' ∩ U` lies in `Φ ⊆ G`; so `A'' = A' − G ⊆ (A' ∩ S) − U`.
  With `Y_0 = ∅`, `S` is the union of the pivots of the light tools, `A' ∩ S ⊆ ∪_{light x_i} dam(x_i)`, so
  `|A''| <= (number of light tools) · θ <= kθ = |A'|/2`. **Holds** (any cover by at most `k` tools works; the
  probabilistic argument is needed only for the existence of the cover).
- `D(τ) ∩ ↑A' ⊆ ↑A''`: `w ∈ ↑A'`, `w ∉ ↑A''`: every `a ∈ A'` with `a <= w` lies in `A' − A'' ⊆ G`, so `w ∈ ↑G`,
  `w ∉ D(τ)`. **Holds.** `A'' = ∅` gives the final case (E-term without anchors).
- Heavy tools are allowed in the cover (the row player's `p` may put weight on them); they get no flag, and their
  `cov_E` has no pivot part, consistent with the payoff. Holds.

### 2.4 Lemma 8.1, the case `v < 1/2`

- For light `x`: `Σ_y q(y) [x ∈ cov_F(y)] >= Σ_y q(y) (1 − M(x, y)) = 1 − Σ_y q(y) M(x, y) > 1/2` (the duality gives
  `M(x, y) = 1` or `x ∈ cov_F(y)` for every `y`). One draw misses `x` with probability `< 1/2`, `k` draws with
  probability `< 2^{-k} < 1/m`. **Holds.**
- For heavy `x`: `Pr[a_j ∉ dam(x)] = 1 − |dam(x)|/|A'| < 1 − 1/(2k)`, so `Pr[no a_j < x] = (1 − |dam(x)|/|A'|)^N`, which
  is `< (1 − 1/(2k))^N` **when `N >= 1`**, and `(1 − 1/(2k))^N <= e^{−N/(2k)} <= e^{−ln m} = 1/m` (`N >= 2k ln m`).
  For `m >= 2`, `N >= ⌈4 ln 2⌉ = 3`, strict. For `m = 1`, `N = 0` and the strict inequality fails, but then there is
  no heavy row: a heavy row needs an element of `A'` strictly below it, i.e. two switches. *Repair of wording*: add
  "for `m = 1` there is no heavy row". The union bound over all rows (light and heavy events are on independent draws,
  but the bound does not need independence): `Σ_x Pr[x fails] < |R|/m <= 1`. **Holds with this one-sentence repair.**
- `D(τ) ∩ ↑A' = ∅`: `x ∈ ↑A' ∩ G'`; `x ∉ Φ` (`Φ ⊆ B ⊆ L`, `x ∈ Up`); so `x ∈ Fnon − U' − S'`, `x ∈ R`. A light row
  lies in `NF(F#_{y_i}) ⊆ U'` or in `↑y_i − [y_i]` with `y_i ∈ B ∩ T = T' ` (`S'`); a heavy row lies in `↑a_j ⊆ S'`
  (`a_j < x`). Contradiction in every case; `↑A'` is an up-set, F4. **Holds.**
- `L ⊆ D(τ)`: `b ∈ B` is in `Fnon`; if `b ∈ U'` then `b ∈ Φ = B ∩ U'`; otherwise `b ∉ ↑a_j` (`↑a_j ⊆ Up`, `b ∈ L`) and
  `b ∉ ↑y_i − [y_i]` for `y_i ∈ B` (F3: `y_i < b` with both maximal F-members is impossible; ties allowed). So
  `B ⊆ G'` and `L = ↓B ⊆ ↓G'`. **Holds.**
- Flips `Φ = B ∩ U' ⊆ ∪_i (B ∩ NF(F#_{y_i}))`, `y_i ∈ C ⊆ L`, so `y_i ∉ Up`: the hypothesis of the dual of Lemma 6.3.
  `|Φ| <= 9k`, `Φ ⊆ U'`. Anchors `X_0 = {a_j} ⊆ A'`, `|X_0| <= N`. **Holds.**
- Only `B ∩ C` can carry a strict anchor in `cov_F` (an element of `B` with empty E-side is no column); consistent.

### 2.5 Hidden assumptions searched for in Lemma 8.1

- No use of Theorem 6.5, Corollary 6.5' or §5: the only external results are Lemma 6.3 (with `x ∉ L`, resp. `y ∉ Up`,
  `P` shortest) and Lemma 6.4 (with `x ∈ N_F`, `y ∈ N_E`, P2).
- Shortestness: used only through Lemma 6.3 (flip bound). F0, F3, F4, the duality, the damage bound and both inclusions
  use validity only. Without shortestness the lemma still holds with "at most `|A ∩ U|` flips".
- Ties: among members of `A` (`dam(a) = ∅` because `↓a − [a]` excludes ties), among members of `B` (strict anchors
  `↑y − [y]` never contain a tied `b`), between rows and elements of `A'` (a row tied with `a ∈ A'` has `dam = ∅`),
  between rows and columns (impossible). No step fails with ties.
- The value `v = 1/2` exactly belongs to the first case; there the bound `<= 1/2` per draw gives `<= 2^{-k}`, enough.

### 2.6 Theorem 8.2

- `A = ∅`: `G' = Fnon` contains `B`, so `L ⊆ ↓Fnon = D`, and `Up = ↑A = ∅`. Picks `P`. Holds.
- Levels: `|A^(1)| <= m`; after `c` continue steps `1 <= |A^(c+1)| <= m 2^{−c}`, so `c <= ⌊log2 m⌋` and `j <= k`.
  Each continue step strictly decreases `|A^(i)|`, so the process terminates. All levels use the same shortest `P`.
- Induction: `D_1 ∩ .. ∩ D_i ∩ Up ⊆ ↑A^(i+1)` (base `D_1 ∩ ↑A^(1) ⊆ ↑A^(2)`; step through `D_{i+1} ∩ ↑A^(i+1)`), and
  `D_j ∩ ↑A^(j) = ∅`, so `D ∩ Up = ∅` (also for `j = 1`). `L ⊆ D_i` for all `i`. F0: `D` picks `P`. **Holds.**
- Only the last term has anchors (E-terms of continue steps have `Y_0 = ∅`; the final term is an E-term without
  anchors or an F-term with at most `N` E-anchors). Tools `<= k`, flips `<= 9k` per term. Holds.

### 2.7 IDESC: soundness and completeness

- Soundness: every tested set is an intersection of down-sets, a down-set; a connecting down-set is a solution of the
  switch form, which equals the ZZ answer (`r4-general.md` §5.1, checked by `verify/rv-core-65.md` `zz_check` on all
  instances with at most 4 middle elements, and re-checked here, §3). **Holds.**
- Completeness: the terms of the proof are in the search space: tools `<= k` (repeated draws merge), flags on light
  tools (any flag pattern is enumerated), E-terms without anchors, final F-term with `<= N` E-anchors, flips `A' ∩ U ⊆ U`
  (E) and `B ∩ U' ⊆ U'` (F), at most `9k` each; at most `k` terms, at most `N` anchors in total. **Holds.**

### 2.8 Time bound

The text counts `2 · m^k · 2^k · m^{9k}` anchor-free terms and `m^N` times as many anchored ones, then
`(2^{k+1} m^{10k})^k · m^N` sequences. As IDESC is *defined* ("at most `a` anchors in total", anchors in any term),
the anchors may be spread over the `j` terms; the count is then at most `(2^{k+1} (m+1)^{10k})^k · (k (m+1))^N`, still
`m^{O(log^2 m)}`. Alternatively restrict IDESC to the shape of Theorem 8.2 (anchors only in the last term), which is
all completeness needs. Subsets of size `<= c` from `m` are `<= (m+1)^c` (the text writes `m^c`). Each test: compute
`↑G` or `↓G'` (`O(m^2)`) and connectivity of the picked hypergraph (linear in the total side size). Total
`m^{O(log^2 m)} · poly(n) = 2^{O(log^3 n)}`. **Holds with the wording repair.** Edge case: `k` is undefined for
`m = 0` (no switch: the instance is trivial, yes iff `s = t`).

### 2.9 Corollary 8.3

Needs a polynomial reduction from the open case of DC to ZZ + P2 (`theory-dc.md` Theorem 13, reviewed in
`verify/equivalence.md`, not re-reviewed here) and the polynomial conversion to the general switch form (`m <= n`).
Then time `2^{O(log^3 n)}`. If the problem were NP-complete, 3-SAT would be in `DTIME(2^{polylog})`, so NP ⊆ QP; under
ETH 3-SAT needs `2^{Ω(n)}`, contradicted by `2^{O(log^3 n^c)}`. **Holds** (conditional on Theorem 13).

### 2.10 Remarks (none affects a verdict)

- `9k` may be read `5k` throughout (Lemma 6.3 with 5 positions, `verify/rv-core-65.md`); the runs never saw more
  than `3|T|` flips.
- `k` and `N` could be taken from `|C|`, `|R|` instead of `m`; `m` is used only as an upper bound of both.
- Elements of `↑A'` with empty F-side are no rows; they never enter `G'` (`G' ⊆ Fnon ∪ Φ`, `Φ ⊆ B`), so the F-term
  excludes them automatically.
- In the E-case heavy rows may be drawn as tools (without flag); in the F-case the anchors are drawn from `A'`, not
  from `A`; both are consistent with the payoff and the claims.
- `m = 0` (no switch) leaves `k` undefined; the instance is then trivial (yes iff `s = t`).
- §8.2 Remark (2) (2CH with classes: one level, no damage) and §8.5 item 2 (the chain needs neither Theorem R nor
  Theorem Q nor Theorem 6.5) agree with the reading above.
- The deep designs of §3.2 show that the *proof* can use many levels when the covers are chosen badly (5 levels at
  `m = 335`, `k = 9`), but on every deep design tested for it one term with one tool connects (§3.4); whether
  intersections are ever needed stays open (§8.5 item 5).

## 3. Computations

All scripts in `verify/rv-r6-core/`, own code (`zzl.py`, `proof8.py`, `enum8.py`, `gen8.py`, `adv8.py`); logs in
`runs/`. No script imports code of another agent. A failure is a counter whose name ends in `FAIL`; every log ends
with `FAILURES: none` or the list of failing counters.

What `proof8.levels` checks on a shortest valid path (both kinds of check are written from §8.2, not from r5-core's
code): the setting (rows outside `L` and inside `N_F`, columns outside `Up`, `dam(a) = ∅` for `a ∈ A'`); the duality
claim for every light row and every column; the game value (LP) and the case split; the probabilistic step
numerically (expected number of uncovered columns `Σ_y (1 − c_y)^k < 1` for the optimal row strategy; in the F-case
`Σ_light (1 − d_x)^k + Σ_heavy (1 − |dam(x)|/|A'|)^N < 1`); existence of the promised cover by `<= k` tools
(exhaustive branching) and of `<= N` anchors (minimum hitting set); for **every** enumerated cover (up to 40, plus
padded ones): `D(τ)` a down-set, `L ⊆ D(τ)`, `G ∩ L = ∅`, `|Φ| <= 9|T|` (and how often `> 5|T|`),
`A'' ⊆ (A' ∩ S) − U`, `|A''| <=` sum of the damages of the light tools, `|A''| <= |A'|/2`,
`D(τ) ∩ ↑A' ⊆ ↑A''` (E-terms); `G' ∩ ↑A' = ∅`, `D(τ) ∩ ↑A' = ∅`, `B ⊆ G'` (F-terms); then levels `<= k`, anchors only in
a final F-term and `<= N`, the intersection a down-set containing `L`, missing `Up`, connecting `s` and `t` in the
switch form and in the ZZ graph `G_D` (realisation `zzl.sw_to_zz`, connectivity from the ZZ definition).
Cover choice for the next level: `adversarial` (largest residue `A''`; covers padded with light tools of largest new
damage up to `k` tools, which is still a cover by `<= k` rows, so the proof must work for it), `first` (first
minimal cover found), `sample` (`k` draws from the optimal row/column strategy and `N` uniform anchors, as in the
proof). Mode `stress`: light threshold `|A'|/2` instead of `|A'|/(2k)` (more damage, more levels; only the logical
claims are checked, not the halving).

### 3.1 Exhaustive: all ZZ instances with at most 4 middle elements (`enum8.py`)

Own enumerator (labelled preorders on the `K` middle elements as relation matrices, `u` below and `v` above all,
every set `R` of strict pairs except `{u, v}`), validated against the counts of `verify/rv-core-65.md` §3.1-§3.2.
Per instance: P2 from the ZZ definition = P2 of the own switch form; for every down-set of the middle elements the
ZZ graph `G_D` and the picked hypergraph agree on connectivity; yes iff some down-set connects iff a valid path
exists; per shortest valid path: Lemma 6.3 bound and `levels` in modes proof and stress; IDESC with **all** terms
(both kinds, `<= k` tools, every flag pattern, every flip set inside `U`, every anchor set of size `<= N`) on every
P2 instance for `K <= 3` and on every 61st instance for `K = 4`: every term a down-set; on yes-instances some
intersection of the Theorem 8.2 form connects; on no-instances no term connects (switch form and ZZ graph).

| Run (log) | Instances | Outcome |
|---|---|---|
| `enum8.py 2 0 1 1` (console) | 96, 87 P2, 8 yes, 79 no, 8 paths | no failure |
| `enum8.py 3 0 1 1 runs/enum8-3-idesc.txt` | **7232, 5830 P2, 1584 yes, 4246 no, 1896 shortest paths** (= the counts of `rv-core-65` §3.1) | no failure; IDESC: 6 903 520 terms, all down-sets; every yes-instance accepted (already by one term), no no-instance; levels always 1; cases C0 1488, R0 948, E 1332, F 24 (all F with anchors, max 1 anchor); max `|A ∩ NE(E#_x)|` = 1 |
| `enum8.py 4 P 6 61`, `P = 0..5` (`runs/enum8-4-p*.txt`, total `runs/enum8-4-total.txt` by `agg.py`; PIDs 40224, 10036, 24172, 4564, 36912, 23992, all finished) | **all 1 535 744 instances with 4 middle elements: 1 111 740 P2, 530 236 yes, 581 504 no, 785 016 shortest valid paths, 29 184 of them with a bad pair** (every count = `rv-core-65` §3.2) | **no failure**. Switch form = ZZ on every down-set of every P2 instance; P2 in both forms agree. Proof (both modes) on all 785 016 paths: always 1 level; cases C0 496 560, R0 362 280, E 692 760, F 18 432 (all with anchors, at most 1); duality checked on 942 552 light-row/column pairs; 827 112 E-terms and 18 432 F-terms checked; max `|A ∩ NE(E#_x)|` = 2, max `|Φ|/|T|` = 2. IDESC with all terms on 18 215 sampled P2 instances (8717 yes, 9498 no): 301 200 160 terms, all down-sets; every sampled yes-instance accepted, no term connects on a no-instance |

For `K <= 4` there is never a second level: `|A| <= 4 < 2k = 6`, so a light row has no damage; the exhaustive runs
check the one-level logic (both cases, heavy rows, anchors), the model and IDESC soundness.

### 3.2 Adversarial designs (`adv8.py`, `gen8.py`)

Rigid designs (`gen8.rigid_design`): the rigid word `R(W)` of `r4-general.md` §6 (own implementation) plus
X-switches strictly above sets `S_i` of E-members (rows with damage `|S_i ∩ A'|`), Y-switches strictly below sets of
F-members (columns), relations `y < x` (bad pairs), chains among the X, ties (extra with extra, X with an E-member,
Y with an F-member, member with member of the same type), middle edges between comparable switches whose private node
lies in no path side, P2 by fresh nodes placed in a flip side of the base switch or in extra sides (or one hub node
per type among extras). *Why the planted path is the unique valid path* (used instead of an exact path search for
`n > 14`): extra sides contain no node of a path side, so the argument of `r4-general.md` Theorem Y (i) applies
verbatim: if `r` is the first base switch not in its path mode, the picked sides containing nodes of
`h_1 .. h_{r−1}` are only `h_1 .. h_{r−1}` (the `z_{pi}`, `p < i < r`, lie in flip sides `Fl_p` that are not picked;
extra sides contain no path node), so `s` and `t` are not connected; hence every solution has the base in its path
modes; then the picked sides containing path nodes are exactly `h_1 .. h_n`, which form an induced path (`h_i ∩ h_j = ∅`
for `|i − j| >= 2`), so every valid path is `h_1 .. h_n`. `gen8.rigid_certificate` checks these incidences on every
design; for `n <= 14` the exact search confirms uniqueness.
Deep designs (`gen8.deep_design(L, k)`): `nE = 2k 2^{L−2}` E-members (word `(EF)^{nE}`), for each level
`i = 1 .. L − 1` a family of `k` X-switches with disjoint sets `S` of size `2^{L−1−i}` nested in the union of the previous
family, every Y below every X; `k` must be `⌊log2 m⌋ + 1` (L = 3: `k = 7`, `m` about 80; L = 4: `k = 8`, `m` about 160;
L = 5: `k = 9`, `m` about 330). With adversarial covers the proof then runs `L` levels, with `|dam| = θ` exactly
(boundary of "light") and `|A''| = |A'|/2` exactly (boundary of the halving).

| Run (log) | Instances | Outcome |
|---|---|---|
| `adv8.py rigid 1 10 8 14` (console) | 10 designs, `m <= 17` | no failure; exact search: planted path unique shortest in all 10 |
| `adv8.py layered 2 30 24 40` (console) | 30 designs, `m <= 52`, `|A| <= 23`, up to 48 bad pairs on a path | no failure; proof mode: 2 levels on 21 designs (51 runs over the three picks); stress up to 3 levels |
| `adv8.py deep 5 4 3 7` (console) | 4 designs, L = 3, `k = 7`, `m` 79-82, `|A| = 28`, up to 204 bad pairs | no failure; **3 levels** (proof, adversarial covers) on 2 of 4 (perturbation none and middle edges; with ties 2 levels); first/sample covers: 2 levels |
| `adv8.py rigid 101 2000 8 30` (`runs/adv-rigid-101.txt`, PID 16576, finished) | 2000 rigid designs, `m <= 49`, `|A| <= 18`, 24 976 bad pairs (up to 143 on a path), 11 628 games (518 with value exactly 1/2) | **no failure**; planted path unique shortest by exact search on all 634 designs with `n <= 14`; proof mode 2 levels on 1411 of 6000 runs (3 picks), stress up to 5 levels; 36 346 E-terms, 33 894 F-terms checked; max anchors (minimum) 6, sampled anchors up to 18 distinct; max `|A ∩ NE(E#_x)|` = 3, max `|Φ|/|T|` = 3 |
| `adv8.py layered 102 1000 20 48` (`runs/adv-layered-102.txt`, PID 27472, finished) | 1000 layered rigid designs (`|S_i|` about `θ`), `m <= 65`, `|A| <= 33`, 19 479 bad pairs (up to 150 on a path), 7527 games (575 with value 1/2) | **no failure**; proof mode 2 levels on 2432 of 3000 runs; stress up to 6 levels; 43 006 E-terms and 27 353 F-terms checked; minimum anchors up to 8, sampled anchors up to 25 distinct (`N >= 50` there) |
| `adv8.py deep 103 40 3 7` (`runs/adv-deep-103-L3.txt`, PID 10664, finished) | 40 deep designs L = 3, `k = 7`, `m <= 83`, `|A| = 28`, up to 231 bad pairs on a path | **no failure**; proof/adversarial: 3 levels on 26 of 40 (all 10 unperturbed, all 10 with middle edges, 5 of 10 with member ties, 1 of 10 with extra ties), else 2; first and sample picks: at most 2 levels; 26 designs saved in `runs/deep/` |
| `adv8.py deep 104 12 4 8` (`runs/adv-deep-104-L4.txt`, PID 11672, finished) | 12 deep designs L = 4, `k = 8`, `m` 160-165, `|A| = 64`, up to 290 bad pairs on a path | **no failure**; proof/adversarial: **4 levels** on 6 of 12 (3 unperturbed, 3 with middle edges), 3 levels on 4, 2 levels on 2 (member or extra ties change the nesting); first/sample: at most 2; minimum anchors up to 10 (`N = ⌈16 ln m⌉ = 82`) |
| `adv8.py deep 105 3 5 9` (`runs/adv-deep-105-L5.txt`; first attempt `*-v1-dumpbug.txt` died in the JSON dump of a 40 000-bit mask after its checks, a second one was stopped by PID at 21 GB because the realisation built a `q × q` order matrix; both repaired) | 3 deep designs L = 5, `k = 9`, `m` 334-338, `|A| = 144`, up to 520 bad pairs on a path | **no failure**; proof/adversarial: **5 levels** on design 0 (unperturbed), 3 on designs 1, 2 (ties); boundary `|dam| = θ` used by 124 tools, `|A''| = |A'|/2` exactly 19 times; minimum anchors up to 10 (`N = 105`) |
| `adv8.py deep 106 16 5 9` (`runs/adv-deep-106-L5.txt`, PID 22840, finished) | 16 deep designs L = 5, `k = 9`, `m` 333-338, `|A| = 144`, up to 572 bad pairs on a path | **no failure**; proof/adversarial: **5 levels** on 7 (3 unperturbed, all 4 with middle edges), 4 on 1, 3 on 8 (ties); boundary `|dam| = θ` 879 tools, `|A''| = |A'|/2` exactly 136 times; minimum anchors up to 12 |
| `adv8.py deep 107 2 6 10` (`runs/adv-deep-107-L6.txt`, PID 15404) | 2 deep designs L = 6, `k = 10`, `m` about 700, `|A| = 320` | design 0 (`m = 701`, unperturbed): no failure (a failure saves a JSON in `runs/fail/`, which stayed empty), proof/adversarial **5 levels**, first/sample 2; design 1: see the log (summary line `FAILURES: ...` at the end) |
| `adv8.py random 201 3000 4 12` (`runs/adv-random-201.txt`) | 3000 random general switch-form instances (`m` 4-12, ties, middle edges, P2 repair), 1720 yes, 1278 no, 3650 shortest paths, 1366 bad pairs; switch form = ZZ realisation on every down-set; yes by brute force = valid path exists | **no failure**; 2 instances skipped (path search over the budget of 300 000 DFS visits); always 1 level in proof mode (`|A| <= 4`), stress up to 2 |
| `adv8.py random 202 1500 10 16` (`runs/adv-random-202.txt`) | 1500 random instances (`m` 10-16), 1212 yes, 284 no, 3743 paths, 3827 bad pairs (up to 45 on a path); model check for `m <= 12` | **no failure**; 4 skipped (budget); 1 level in proof mode, stress up to 2 |

*Two generator bugs found and repaired on the way (no effect on any verdict):* (1) version 1 of `gen8.random_sw` let
the P2 repair reuse a node of `x`'s side for `y`, which could be the private node of a middle edge; such an instance
is not a switch form (a private node must lie only in `F_z` and `E_v`), and its ZZ realisation differs; the first
`random 201` run reported 36 "final D does not connect in ZZ" on such instances (logs `runs/adv-random-201-v1-generator.txt`,
instances in `runs/fail-v1-generator/`; `dbg_zz.py` shows the privacy violations and the down-set mismatches). Repaired:
only non-private nodes are reused, and every random or designed instance is now checked for privacy and (`m <= 12`) for
switch form = ZZ on all down-sets. The proof's switch-form claims held on all those invalid instances too.
(2) The DFS for all shortest valid paths had no budget and hung on two random instances (logs `*-v2-stuck.txt`,
stopped by PID); it now skips an instance after 300 000 visits (counted).

*Cross-check on r5-core's data* (`cross_r5data.py runs/cross-r5data.txt`; reads the JSON instances
`r5-core/runs/two-levels-example.json` and `r5-core/runs/single/*.json`, no code): 24 instances, `m` 27-37, `|A|` 10-12,
one shortest valid path each (the stored path of the two-level example is shortest). Own proof program: **no
failure**; proof mode needs 2 levels on every one of the 24 paths with every pick (agrees with r5-core §8.4: no single
term of the proof's kind), stress up to 4. *Own bug found on the way:* the first run (`runs/cross-r5data-v1-bug.txt`)
reported 202 duality failures; cause: `zzl.SW` built the stars by *summing* the private-node masks of the lower
middle neighbours, and r5-core's instances carry several middle edges between the same pair (several private nodes),
so a neighbour listed twice corrupted the mask. Repaired (bitwise OR); my generators and the ZZ enumerator never
produce parallel middle edges, so no other run is affected.

### 3.3 Attempts to make the construction fail

The proof is deterministic once the covers exist: every claim of a level follows from "`T` covers `C`" (E) or
"`T` covers the light rows and the anchors hit the heavy rows" (F). So a failing instance needs either a cover that
does not exist (contradicting the minimax and the probabilistic step), or a failure of Lemma 6.3/6.4 or of the model.
The runs aimed at each of these, and at the boundaries of every inequality:
- *Boundaries.* Deep designs make the light threshold tight (`|dam(x)| = θ` exactly: 121 tools in 4 designs of
  `adv8.py deep 9 4 3 7`) and the halving tight (`|A''| = |A'|/2` exactly: 22 times); games with value exactly 1/2
  (518 + 575 + 179 + 256 in the rigid, layered and random runs) fall into the E-case and the E-cover always existed.
- *Worst covers.* The adversarial pick pads every cover with the light tools of largest new damage up to `k` tools; the
  proof's claims are checked for every enumerated cover, not only the chosen one (exhaustive runs: 828 564 E-terms and
  18 456 F-terms; adversarial, random and cross-check runs of §3.2 up to `deep 105`: 121 330 E-terms and 70 553
  F-terms, `agg.py`). Levels reached: 3 (L = 3 designs), 4 (L = 4), 5 (L = 5), never more than `k`.
- *Ties.* Members tied with members of the same type, X tied with E-members, Y tied with F-members, extras tied with
  extras (rigid, layered, deep runs, `ptie` up to 0.3); random preorders with ties (random runs); the exhaustive runs
  contain every labelled preorder on 3 and 4 middle elements, so every tie pattern. No claim failed.
- *Middle edges and stars.* Middle edges between all comparable pairs allowed by the private-node rule (rigid
  `pme` up to 0.5, random up to 0.3; parallel middle edges in r5-core's stored instances); max `|A ∩ NE(E#_x)|` = 3
  (bound 9, reviewed bound 5), max `|Φ|/|T|` = 3.
- *Many bad pairs.* Up to 290 bad pairs on one path (deep L = 4), `y < x` for every Y and every X.
- *Heavy rows in the F-case.* Minimum anchor sets up to 10, sampled anchor sets (as in the proof) up to 25 distinct
  elements, always `<= N` and always hitting every heavy row.
- *Model.* Switch form = ZZ realisation on every down-set of all 1 111 740 P2 instances with 4 middle elements and of
  all random instances with `m <= 12`; final intersections connect in the ZZ graph in every run.
Nothing failed. I found no instance on which the construction of the proof fails, and the reading of §2 shows why
none exists.

### 3.4 Side claims of §8.4 (single terms)

| Run (log) | Instances | Outcome |
|---|---|---|
| `single8.py 1 0 0 two-levels-example.json --r5` (console) | r5-core's two-level example (`m = 27`) | one E-term with one tool (switch 19, flagged), no anchor, no flip connects: agrees with "`gdesc.decide(G, 1, 0, 0)` accepts" |
| `single8.py 1 1 2 r5-core/runs/single/*.json --r5 --log runs/single-r5-112.txt` | the 23 instances of `hunt_single.py` | all 23 accepted by one term with `<= 1` tool, `<= 1` anchor, `<= 2` flips (mostly the E-star of an F-member near the end of the word with two flips; on some the first term found also has one F-anchor): agrees with §8.4 |
| `single8.py 1 0 2 runs/deep/deep-L3-k7-103-*.json --log runs/single-deep-102.txt` | the 26 own deep designs (L = 3) on which the proof uses 3 levels | all 26 accepted by **one** term with one tool, no anchor, two flips (the E-star of the F-member at position 52, or once an F-star): the extra levels are an artefact of the proof's tool set, as §8.4 says for r5-core's designs. So these designs say nothing against a polynomial bound |

## 4. Scripts

| Script | What |
|---|---|
| `zzl.py` | ZZ instances, own converter ZZ -> switch form (`zz_to_sw`) and back (`sw_to_zz`), P2 in both forms, connectivity from the definitions, down-sets, all shortest valid paths (iterative deepening), `Skel` (`W_E`, `W_F`, `Up`, `L`, `A`, `B`, `N_E`, `N_F`), stars `E#`, `F#`, terms `D(τ)` of §8.2 |
| `proof8.py` | Lemma 8.1 / Theorem 8.2 as a program with every claim checked (`levels`, `one_level`), game value by LP, exhaustive covers, minimum hitting sets, Lemma 6.3 bound |
| `enum8.py` | exhaustive run over all ZZ instances with `K` middle elements, IDESC with all terms |
| `gen8.py` | rigid designs, deep designs, rigidity certificate, random general switch-form instances |
| `adv8.py` | adversarial runs (`rigid`, `layered`, `deep`, `random`, `hill`), privacy and model checks, JSON save of failures and deep designs (`runs/deep/`) |
| `cross_r5data.py` | cross-check on r5-core's stored instances (reads their JSON data, imports no code of r5-core) |
| `single8.py` | exhaustive search for one connecting GDESC term with few tools, anchors, flips |
| `probcheck.py` | the numeric inequalities `2^k > m`, `(1 − 1/(2k))^N <= 1/m`, `N >= 1` for `m = 1 .. 10^6` (`runs/probcheck-1e6.txt`: no violation, minimum margin 0.158 in the logarithm) |
| `agg.py` | sums the counters of several logs |
| `dbg_duality.py`, `dbg_zz.py` | diagnostics of the two own bugs (§3.1 cross-check, §3.2 generator) |
