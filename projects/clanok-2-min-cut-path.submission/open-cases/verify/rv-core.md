# Review rv-core: adversarial review of `r5-core.md` §1-§5 (round 5)

Reviewer: agent rv-core (round 5, workflow run of 2026-10-22, evening). Status: **complete** for the targets (1)-(3) (2026-10-22, about 21:30); no background run left.
Version reviewed: `r5-core.md` "version 0.3 in progress" as found at 2026-10-22 19:50 (sections §0-§5.3, empty §9,
script list §10), SHA-256 `eeb1103a2ccb97038cfafd4ed6b33241578b5e0b574f48e2c66a00a9adbbe296`. Sections appended later
are not reviewed here.
Scripts: `verify/rv-core/` (own code written from the text: `sw.py` library, `fams.py` families, `gen.py` random
generator; imports of other agents' code only in the cross-checks `cross_d.py`, `cf_z4.py`, `test_cf.py` part (iv)).
Logs: `verify/rv-core/runs/`. Verdicts: holds, holds with repair, gap, false.

## 0. Verdicts

| Target | Verdict | Note |
|---|---|---|
| Prop. D (i) P2 | holds | re-derived; checked `k = 2..5`, all four variants |
| Prop. D (ii) exactly two solutions | holds | re-derived (first-flip argument with the blob); brute force `k = 2..5` |
| Prop. D (iii) propagation | holds with repair | true for `gsw.refutes` (each terminal walked with its own copy of the assignment); with one shared assignment (a reading the text of r4-general §7.3 allows) the back variant also gets `x_2k` fixed. Either way at most one switch is fixed and all mates and `d` stay free |
| Prop. D (iv) HYB rejects | holds | re-derived; own HYB rejects every maximal tuple `kd + ks + s = k - 1`, `B = k - 1`: plain `k = 2..4` all variants and six tuples at `k = 5`; refined on `Y'^d` for `k = 2, 3` (all tuples) and `k = 4` (5 of 8 tuples) |
| Prop. D conclusion (HYB incomplete) | holds | |
| §5.1 ADESC soundness | holds | trivial (every tested `D` is a down-set); the guided cost with anchors needs `A_0 ∩ L = ∅` and `↓B_0 ∩ Up = ∅` (unstated) |
| §5.2 (E1)/(F1) | holds | needs neither shortestness nor the interval: `B_0 = B` always works; the interval only bounds `|B| <= 5` |
| §5.2 (E2)/(F2) as written | **false** | counterexample `R((EF)^4)` + one node in `E_{x_2} ∩ F_{x_2}`; the contraction puts minimal E-members outside `f*` into `U`. Random: 36 + 46 failures in 4385 + 4385 pairs |
| §5.2 (E2)/(F2) repaired | holds with repair | (R2) take the centres `Ẑ(b) = E_b ∪ ⋃{F_v : v < b, F_v ∩ E_b ≠ ∅}` uncontracted: then `A ∩ U = f*` exactly and the proof goes through with `c` unchanged; or (R1) keep the contracted centres and flip `A ∩ U` (cost larger than `|f*|`). No failure of R1 or R2 in 8770 random pairs |
| §5.2 Corollary "TCA(c) ⇒ ADESC(5, 2, c) accepts" | gap | holds if ADESC also enumerates the centres `Ẑ(b)` (R2); with ADESC as defined (sides and nodes, contracted) it is unproved outside 2CH. In 2CH it holds |
| §5.2' strict anchors | holds with repair | needs `B_0 ⊆ L` (e.g. `B_0 ⊆ B`) and `A_1 ⊆ A`; with arbitrary `B_0` it fails (random) |
| §3.1 CDESC soundness | holds | trivial |
| §3.2 Lemma G | holds | re-derived; 97520 random descriptions, no failure |
| §3.3 Proposition CF (i)-(iii) | holds | own families: `Y`, `Y'`, `Y^d`, `Y'^d` `k <= 5`, `X_L` `L <= 10`: `D` equals the claim |
| §3.3 Proposition CF (iv) (`Z_k`, `Z^B_k`) | holds (checked only) | labelled proved in the table but only checked; cross-check `k <= 4`: one centre, no flip |

## 1. Model as re-derived

General switch form as in `r4-general.md` §5.1: nodes, terminals `s`, `t`; switches with a preorder; sides `E_w`,
`F_w`; modes a down-set `D` (F-mode); picked side `F_w` for `w ∈ D`, else `E_w`; yes iff `s`, `t` connected in the
hypergraph of the picked sides. Conflict pair `{E_w, F_z}` with `w <= z`. P2 (incomparable pairs only): a common node
in `E_x ∩ E_y` or `F_x ∩ F_y` (bottom or top witness), or a lower middle witness `w < x, y` (private nodes of the middle
edges in `F_w ∩ E_x`, `F_w ∩ E_y`), or an upper one. A valid walk is a walk of sides without a conflict pair; its
sides are picked by the down-set of its F-members (`sw.py`). Shortest valid paths are computed as the shortest side
paths over all solutions (exact, brute force over down-sets).

## 2. Proposition D (`r5-core.md` §2.2)

**Construction.** Built from the text of r4-general §6 and r5-core §2.1 (`fams.yfam`). Cross-check (`cross_d.py`,
`runs/cross-d-5.txt`): same number of nodes, same multiset of side sizes and of node degrees as the author's
`fool.yd`, `k = 2..5`, all four variants.

**(i) holds.** Pairs of `Y_k` keep their witnesses (adding nodes never destroys P2); `d` is incomparable with all and
meets `F(x_b)` in `ε_b`, `E(x_q)` in `δ_q`, `E(m_c)` in `γ_c`. Checked: no P2 violation (`runs/d-basic-5.txt`).

**(ii) holds.** Re-derived: with `r` the first base switch off its path mode, the nodes of `h_1 .. h_{r-1}` lie only
in `h_1 .. h_r`, in `Fl_p` (`p < i < r`, not picked), in `E(d)` (only `s`) and in `F(m_c)` (`fc_c`, `k + c < r`, not
picked since `m_c ∈ D` forces `x_c ∈ D`). The blob (`E(d)`, picked `E(m_c)`, picked `Fl_q`, `q > k`) is closed: its
nodes `γ, δ, e, g, w_{qq'}, κ` lie in no other picked side (`κ` only in `F(d)`, not picked when `d ∉ D`); a picked
`Fl_p`, `p <= r <= k`, meets only `h_q` with `q > k` and F-sides outside the component. So `t` is not reached for
`r <= 2k`, the base is in its path mode, the mates are in E-mode, `d` is free. Brute force: exactly 2 solutions, the
claimed ones, `k = 2..5`, all variants; without `d`, 1 solution.

**(iii) holds with repair.** My own propagation (`sw.refutes`, one assignment shared by the walks from `s` and from
`t`, iterated to a fixpoint, stopping a walk once it contains the other terminal) fixes exactly `x_2k` in **all four**
variants. In the back variant the trial `x_2k` E is refuted: the walk from `t` has the single exit `F(d)` and fixes
`d` F; then the walk from `s` has the single exit `h_1` (as `E(d)` is dead) and is forced along `h_1 .. h_{2k-1}`, all
of whose exits are dead (`Fl_p` by the fixed `x_p`, `F(m_c)` by the closure `m_c` E, `h_2k` by the trial). The
author's `gsw.refutes` (read-only, applied to my instances) walks from `s` and from `t` each with a fresh copy of the
assignment, and then fixes nothing in the back variant, as (iii) says. Both procedures are sound; the text of
r4-general §7.3 ("... and repeat; the same from `t`") allows both. **Repair:** state (iii) for `gsw.refutes`
(separate walks), or say "fixes `x_2k` and nothing else" for the shared reading. Nothing in (iv) depends on this.

**(iv) holds.** Re-derived: an accepted walk is valid (Theorem 5', reviewed in `verify/r5-review.md`), so its sides
are picked by one of the two solutions, so it passes `h_1 .. h_2k` (in the back variant the part `F(d)`, `E(m_c)` is
attached to the path only through `t`; in the `d`-E solution the blob only through `s`). `Π(h_c) = {Fl_c, F(m_c)}`;
`F(m_c) ∈ Dc` only by a declaration of `h_c` or `E(m_c)` (each covers one mate); `F(m_c) ∈ K` only through `K_E`
(F-sides): `N_F[Z] ∋ F(m_c)` iff `Z ∈ {F(m_c), h_{k+c} (Y'), Fl_b (b ≠ c)}`; `N_F[Fl_b]` contains the `k` F-members
(`z_{bq}`), all on the walk, so storage `>= k`; every other set covers one mate. Refined search: `F(m_c)` is in the
reachable part unless deleted (`fc_c` joins it to the walk side `h_{k+c}` in `Y'^d`), deletion needs `F(m_c) ∈ K`, and
the F-members are on the walk, so they are in `S`; same count. The count `kd + ks + s < k`, `B < k` suffices (for the
refined search this is stronger than r4-general's Proposition Y', which assumed `kd + ks + s + B < k`; the proof above
shows the stronger form).
Checked (own HYB, `sweep_d.py`, `runs/sweep-d-plain-2-4.txt`, `runs/sweep-d-refined-2-4.txt`): for `k = 2, 3, 4`
every maximal tuple `(kd, ks, s)` with `kd + ks + s = k - 1` and `B = k - 1` (the enumeration includes all smaller
tuples), all `K_E`, `K_F`: plain HYB rejects on all four variants; refined HYB rejects `Y'^d_k` (both variants; `k = 4` see §5) and
accepts `Y^d_k` with one dominator, as (iv) allows. With `(1, 1, 2, 6)` plain HYB accepts `k = 3, 4`. `k = 5`: plain HYB rejects for six maximal tuples (§5).
**Wording.** The §0 table of r5-core says "every run of HYB (plain or refined ...) rejects" for both families; the
refined search accepts `Y^d_k` (one dominator `N_F[h_q]` deletes every `Fl_b`), so the refined claim is for `Y'^d_k` only,
as (iv) correctly says.

## 3. Section 5

### 3.1 §5.1 soundness: holds

Every tested `D` is `Q − ↑G` or `↓G'`, a down-set; acceptance is a connectivity test of that `D`. The contraction only
changes `U`. **Remark (repair of wording):** the guided cost "`L ⊆ D ⊆ Q − Up`" with anchors needs `A_0 ∩ L = ∅`
(e.g. `A_0 ⊆ A`) and `↓B_0 ∩ Up = ∅` (e.g. `B_0 ⊆ W_F`); both are unstated.

### 3.2 (E1), (F1): hold

`U = ∅`, `G = Enon − ↓B`: `G ∩ L = ∅` since `L = ↓B`, and every `a ∈ A` is in `G` (`E_a = X_a ≠ ∅`, `a ∉ ↓B` by
validity). This uses only that `P` is valid; the interval hypothesis only gives `|B| <= 5`. Checked: 12190 paths, no
failure of (E1) or (F1).

### 3.3 (E2), (F2): false as written; the core argument holds; two repairs

**The core argument holds.** For `y ∈ L − ↓B_0` with `E_y ≠ ∅`: `y ∥ b_i` (re-derived: `y >= b_i` and `y <= b'`
give `b_i ~ b'`, hence `y ∈ ↓B_0`); P2 gives (i), (i'), (ii) or (iii); (i) and (ii) put `y` into `U`; (i') or (iii) for
both `i` give a valid walk of length `<= pos(b_1) + 4 + r − pos(b_2)` if `y ∉ P` (compatibility of `F_y` by fact (a),
of `E_{w_i}` by fact (b), no conflict between `F_y` and `E_{w_i}` since `w_i > y` strictly), or
`|pos(b_1) − pos(b_2)| <= 4` if `y ∈ P`. So `out = ∅`. Checked: `out` was empty in all 4385 E2 pairs and 4385 F2
pairs of the random runs (contracted centres), and facts (a) held in 18401 tests.

**The flip step is wrong.** The proof says: "Every `a ∈ A` is in `G`: if `X_a` meets no centre, `a ∈ Enon − U − ↓B_0`;
otherwise `a ∈ f*_A(b_1) ∪ f*_A(b_2) = Φ`." But "meets a centre" is meant in the contracted instance, where all nodes
of every `F_v`, `v ∈ ↓B_0` (including `b_1`, `b_2` themselves, ties, and `v <= b_j` for the *other* anchor, merged
transitively) are identified, while `f*_A(b)` only admits a single `v < b` (strictly) with `F_v` meeting both `X_a` and
`E_b`. A minimal E-member in `U − Φ` is neither a generator nor flipped in, and may land in `D`.

**Counterexample** (`cex_e2.py`, `runs/cex-e2-4-kap2.txt`, checked). `R((EF)^4)` in the 2CH form of r4-general §6
(8 switches, no order, no middle edges, P2, unique solution, unique valid path `h_1 .. h_8`) plus one node `κ` in
`E(x_2) ∩ F(x_2)`. `b_1 = x_2`, `b_2 = x_8` (distance 6), `Φ = f*_A(x_2) ∪ f*_A(x_8) = {x_3, x_5, x_7}`. In the
contracted instance `F(x_2) = h_2` is one node, which lies in `E(x_2)` (through `κ`) and in `E(x_1) = h_1` (through
`y_1`); so `x_1 ∈ U − Φ`, `D = {x_1, x_2, x_4, x_6, x_8}`, and `s` (only in `h_1`) is isolated: the description fails.
Without `κ` it succeeds. With `κ` at every F-member of `R((EF)^6)` all six pairs fail (`runs/cex-e2-6-kapall.txt`).
Random general instances (`test_s5.py`, §5): "as written" fails in 36 of 4385 E2 pairs and 46 of 4385 F2 pairs.

**Repair R2 (keeps the statement with the same `c`).** For `b ∈ B_0` use the centre
`Ẑ(b) = E_b ∪ ⋃{F_v : v < b, F_v ∩ E_b ≠ ∅}` in the *uncontracted* instance, `U = NE(Ẑ(b_1)) ∪ NE(Ẑ(b_2))`. Then
(i) gives `y ∈ U`; (ii): `w < b_i` strictly and `F_w ∋` the private node of `w b_i`, which lies in `E_{b_i}`, so
`F_w ⊆ Ẑ(b_i)` and the private node of `w y` puts `y ∈ U`; the rest of the `out = ∅` argument is unchanged. Moreover
`a ∈ A` lies in `NE(Ẑ(b_i))` iff `X_a` meets `E_{b_i}` or some such `F_v`, i.e. iff `a ∈ f*_A(b_i)`. So `A ∩ U = Φ`,
`Φ ⊆ U`, `Φ ∩ ↓B_0 = ∅`, `G = (Enon − U − ↓B_0) ∪ Φ` (disjoint), `G ∩ L = ∅`, `A ⊆ G`. Dually
`Ẑ'(a) = F_a ∪ ⋃{E_v : v > a, E_v ∩ F_a ≠ ∅}`. ADESC must then enumerate these `m` extra centre sets (polynomial).
Checked: no failure in 8770 random pairs, and `A ∩ U = f*` in all of them.
**Repair R1.** Keep the contracted centres and flip `Φ = A ∩ U` (or put the extra minimal E-members into `A_0`): correct,
but the cost is `|A ∩ U|`, which can exceed `|f*|` (random runs: 58 extra flips in total over the E2 pairs).
**Wording.** "Without middle edges `f*_A(b) = f_A(b)`" is not right: a node of `F_v ∩ E_b` with `v < b` needs no
middle edge. Without middle edges case (ii) does not occur, so the uncontracted centres `E_{b_i}` with `Φ = f_A` suffice.
Checked (`runs/s5-seed21-nomiddle.txt`): 2479 pairs without middle edges, uncontracted centres, `Φ = f_A`: no failure
(while the description as written failed once there).

**Corollary TCA(c) ⇒ ADESC(5, 2, c): gap.** With R2 built into ADESC it holds (2 anchors, 2 centres `Ẑ`, `c` flips,
or (E1) with at most 5 anchors). As ADESC is defined in §5.1 (centres sides or nodes, possibly contracted), the proof
gives only cost `|A ∩ U|`. In 2CH the extra elements of `A ∩ U` are E-members adjacent to `b_1` or `b_2` (`F_{b_i}`
meets only `X_{b_i ± 1}` by F1), at most 4, and fit into `A_0`, so the corollary holds there; in the general model
the contracted class of the `F_v` (`v ∈ ↓B_0`) can meet many positions, and no bound is proved.

### 3.4 Proposition 5.2': holds with repair

Re-derived: `w < a` strictly and `w ∈ Up` give an E-member `a' < a`. `↓a − [a]` is a down-set. So
`D = ↓B_0 ∪ ⋃ (↓a − [a])` contains `L` when it contains `B`, and misses `Up` **provided** `↓B_0 ∩ Up = ∅` (e.g.
`B_0 ⊆ B`) and `A_1 ⊆ A`; the text does not say so. Checked: 22720 random choices with `B_0 ⊆ B`, `A_1 ⊆ A`: no
failure; with arbitrary `B_0` 18360 of 20588 qualifying choices fail.

## 4. Section 3

**§3.1 CDESC soundness: holds** (trivial, as §3.1 of this review).

**§3.2 Lemma G: holds.** Re-derived line by line: `in ∩ (Enon − U) = ∅` (an `a ∈ A ∩ (Enon − U)` is not in `L`,
hence in `G1`, and `a <= a`), so the flip gives `G = G1 ∪ in`; `G ∩ L = ∅`; `L` is a down-set, so `L ⊆ D`; every
E-member lies above an element of `A` (the strict order is well founded; ties handled since `A` = no E-member strictly
below). The dual holds likewise. Checked: 48760 E- and 48760 F-descriptions with random `U` on 12190 shortest valid paths of
random general instances: always `L ⊆ D`, `D ∩ Up = ∅`, connected.

**§3.3 Proposition CF.** (i), (ii) **hold**: `Fl_2k = E(x_2k)` meets exactly `Fl_q` (`q > k`), `E(m_c)`, `E(d)`;
`G = {x_1 .. x_k}`, `D = {x_{k+1} .. x_2k} (∪ {d})`; checked `k = 2..5`, all six variants (`runs/cf-5-10.txt`).
(iii) **holds**: checked `L = 2..10` (own `X_L` from the text of r4-general §4: P2, one solution, `D` equal to it).
(iv) **holds as a check only** (the table labels CF "proved"; (iv) has no proof): cross-check with the author's
`zfam` (`cf_z4.py`, `runs/cf-z-direct-2-4.txt`): `Z_k`, `Z^B_k`, `k = 2, 3, 4`, an E-description with one centre and no
flip connects. Note that the author's log `runs/cdesc-fam-4.txt` reports Lemma-G cost 1 (one centre) for `Z_4`; the
direct test shows that one centre and no flip connect anyway. Its line "`decide(1, 1)` finds a solution on all with at
most 40 switches" is not supported by that log for the `Z` instances (`decide` was not run on them: `None`).

## 5. Computations

| Script | Size, seed | Outcome | Log |
|---|---|---|---|
| `test_d.py basic 5` | `k = 2..5`, 4 variants | P2, 2 solutions as claimed, own prune fixes `x_2k` only (all variants); without `d` rigid | `runs/d-basic-5.txt` |
| `cross_d.py 5` | same | signatures equal to `fool.yd`; `gsw.prune`: `x_2k` (no back), nothing (back) | `runs/cross-d-5.txt` |
| `sweep_d.py 2 4` | all maximal tuples, `B = k - 1` | plain HYB rejects all | `runs/sweep-d-plain-2-4.txt` |
| `sweep_d.py 2 4 refined` | same | refined rejects `Y'^d_k`, accepts `Y^d_k` | `runs/sweep-d-refined-2-4.txt` |
| `test_d.py hyb 5 kd ks s 4` | `k = 5`, tuples (1,0,3), (2,0,2), (1,1,2), (4,0,0), (0,1,3), (2,1,1), `B = 4`, 4 variants | plain HYB rejects all 24 runs | `runs/hyb-k5-plain.txt` |
| `test_d.py hyb 4 kd ks s 3 refined 2,3` | `k = 4`, `Y'^d` both variants, maximal tuples | refined rejects for (1,0,2), (2,0,1), (3,0,0), (1,1,1), (0,1,2); the tuples (2,1,0), (1,2,0), (0,3,0) were stopped (slow; PIDs 28888, 32912) | `runs/hyb-k4-refined-contact.txt` |
| `cex_e2.py 4 2`, `4 -`, `6 2,4,...,12` | `R((EF)^n)` + `κ` | (E2) as written fails; R1 and uncontracted succeed | `runs/cex-e2-*.txt` |
| `test_s5.py 11 2000 7 11 3 flip` | seed 11 | E2 written 8 / 635 fail, F2 11 / 644; repairs, Lemma G, E1, F1, 5.2' (with hypothesis), out = ∅: no failure | `runs/s5-seed11.txt` |
| `test_s5.py 12 2000 7 11 3 any` | seed 12 | E2 21 / 362, F2 26 / 424 fail as written; rest no failure | `runs/s5-seed12.txt` |
| `test_s5.py 13 2000 7 12 2 flip nomiddle` | seed 13 | E2 7 / 2708, F2 7 / 2640 fail as written (distance >= 3); rest no failure | `runs/s5-seed13.txt` |
| `test_s5.py 14 1500 8 12 4 flip` | seed 14 | E2 0 / 680, F2 2 / 677 fail as written; rest no failure | `runs/s5-seed14.txt` |
| `test_s5.py 21 2000 7 12 2 flip nomiddle` | seed 21 | E2 1 / 2479, F2 13 / 2727 fail as written; uncontracted `Φ = f_A`: 0 / 2479 | `runs/s5-seed21-nomiddle.txt` |
| `test_cf.py 5 10 0`, `cf_z4.py 2 4` | families | CF (i)-(iv) as above | `runs/cf-5-10.txt`, `runs/cf-z-direct-2-4.txt` |

## 6. Scripts (`verify/rv-core/`)

| Script | What |
|---|---|
| `sw.py` | own library: instances, P2, down-sets, solutions, shortest valid paths, propagation, Theorem 5' search, HYB (plain, refined), descriptions, contraction |
| `fams.py` | own constructions of `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k`, `X_L`, `R(word)` with `κ` nodes |
| `gen.py` | random general instances with P2 (planted path, ties, one-way relations, middle edges and witnesses) |
| `test_d.py`, `sweep_d.py`, `cross_d.py` | Proposition D |
| `cex_e2.py`, `test_s5.py` | §5 (and Lemma G) |
| `test_cf.py`, `cf_z4.py` | Proposition CF |
