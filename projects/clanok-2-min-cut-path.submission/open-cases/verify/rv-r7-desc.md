# Referee report on r7-desc.md §2-§3 (Theorem B, Corollary B1)

Status: 2026-10-31, finished. **Verdict: Theorem B and Corollary B1 hold, with one trivial repair of the enumeration; no counterexample.** Working file of an AI referee; not
read by the author; not in the manuscript. Scripts and logs: `verify/rv-r7-desc/`. Notation: `qp-proof.md` §1.4, §4, §5.
Out of scope, not reviewed here: Theorem 2.9, Construction 3.1, Lemma 3.3 of `qp-proof.md`; Lemmas 3.4, 4.2-4.5 are used
as stated (they were read and re-derived only where a hypothesis matters).

## 1. Verdicts (hand derivation, §2-§3; computations, §4)

| Statement | Verdict | Remark |
|---|---|---|
| Lemma S | holds | not used by Theorem B |
| Lemma R (a)-(d) | holds | §2.1 |
| Lemma X | holds | §2.2 |
| Theorem A, Cor. A1 | holds | §2.2 |
| atom `EP`, `FP` facts | holds | §2.3 |
| Lemma J | holds | §2.3 |
| Lemma G | holds | §2.3, walk and count re-derived, all conflict pairs listed |
| Stage 0 | holds | §2.4, with ties and infinite values |
| Orientation | holds | §2.4, all four sign cases; reversal only renames positions |
| (★) | holds | §2.4 |
| Stage 1, Case I, Shape A | holds | §2.5 |
| Shape B claim | holds | §2.5; its second alternative never occurs |
| Case II, Shapes A', B' | holds, but **vacuous**: not the dual of Case I | §3, Proposition C |
| Count 91 | holds (an upper bound; 81 suffices) | §2.6 |
| Corollary B1 | **holds with a one-line repair** | §2.6: the exit formulas of Stage 0 are not instances of the four shapes |

## 2. Derivation

Fixed: general switch form with P2, shortest valid path `P`, objects of Definition 4.1.

### 2.1 Lemmas S, R

*S.* `D*` is a union of intersections of down-sets. `b` lies in its own intersection, so `B ⊆ D*`, `L = ↓B ⊆ D*`. If `a`
lay in the intersection of `b`, then every `D_i ∋ b` has `a`, against separation. An empty index set occurs only if
`A = ∅` (no separation needed), then `D* = M` is fine. Holds.

*R(a).* `Γ' = Fnon − NF(F#_{a_1}) − NF(F#_{a_2}) − ↑a_1 − ↑a_2`, `D = ↓Γ'`. Let `x ∈ Γ' ∩ Up`. Trichotomy for `x`, `a_i`:
`a_i <= x` is excluded by `Π'`; `x < a_i` gives an E-member `e <= x < a_i`, against `a_i ∈ A`; so `x ∥ a_i`, `F_x ≠ ∅`,
`E_{a_i} ≠ ∅`, and Lemma 4.5 gives `a_i ∈ NE(E#_x)` (the other alternative is excluded by `U'`). Both `i`: two elements
of `A ∩ NE(E#_x)` at distance `>= 9`, with `x ∉ L`, against Lemma 4.4. So `Γ' ∩ Up = ∅`, and `↓Γ' ∩ Up = ∅` (4.2(c)).
`b ∈ B − C(a_1) − C(a_2)`: `b ∈ Fnon`, `b ∉ U'`, `b ∉ ↑a_i` (`a_i <= b` contradicts `Up ∩ L = ∅`). So `b ∈ Γ'`. Holds.

*R(b).* `Γ = Enon − NE(E#_{b_1}) − NE(E#_{b_2}) − ↓b_1 − ↓b_2`. Let `y ∈ Γ ∩ L`. `y <= b_i` is excluded; `b_i < y <= b'`
with `b' ∈ B` contradicts maximality; so `y ∥ b_i`, `F_{b_i}, E_y ≠ ∅`, Lemma 4.5 gives `b_i ∈ NF(F#_y)`; both `i`, with
`y ∉ Up`, contradicts dual Lemma 4.4. So `Γ ∩ L = ∅`, `L ⊆ M − ↑Γ`. `a ∈ A − C'(b_1) − C'(b_2)`: `a ∈ Enon`, `a ∉ U`,
`a ∉ ↓b_i`, so `a ∈ Γ`, `a ∉ D`. Holds.

*R(c).* `Γ' = Fnon − NF(F#_h) − (↑h − [h])`. `h < a <= x` gives `h < x`, `x ∉ Γ'`; so `↑a ∩ Γ' = ∅`, `a ∉ ↓Γ'`.
`b ∈ B − C_h`: `h < b` contradicts `h ∈ B`; so `b ∈ Γ'`. `h ∈ C_h` as `∅ ≠ F_h`. Interval: dual 4.4, `h ∉ Up`. Holds.
*R(d).* Trivial.

### 2.2 Lemma X, Theorem A

Lemma X is Lemma J and Lemma G (§2.3) in the tie-free case. The two-jump split was re-derived:
`pos(a) ∉ (h_1, h_2)` and `pos(h) ∉ (a_1, a_2)` by one jump; for `pos(a) < pos(h)` this forces
`a_1 < pos(a) < h_1 < pos(h) < h_2` and `a_1 < pos(a) < a_2 < pos(h)`; the case `a_2 < h_1` gives sum `<= 8` against
`>= 16`; the case `h_1 < a_2` gives `(h_1 − a_1) + (h_2 − a_2) <= 8` against `>= 5 + 5`. Holds.
Theorem A: the sorts, `E_0`, `H_0` (26 each), `A°`, `B°`; for `a ∈ A°`, `b ∈ B°` the four contacts satisfy Lemma X, so
`b < a`; `X = FP(h) ∪ FP(h')` misses `A°` (R(c)) and contains `B` (two windows of 9 positions containing `pos(h)`,
`pos(h')` are disjoint at distance `>= 17`). All branches check. Holds. Cor. A1: same remark as in §2.6.

### 2.3 Atoms, Lemmas J, G

`EP(a)`: `Γ = Enon − NE(E#_a) − (↓a − [a])`. `b < a`: `↓b ⊆ ↓a − [a]`, so `↓b ∩ Γ = ∅`, `b ∉ ↑Γ`. `a' ∈ A − win(a)`:
`a' ∈ Enon`, `a' ∉ NE(E#_a)`, `a' < a` is impossible, so `a' ∈ Γ`. `|win(a)| <= 9`: Lemma 4.4, `a ∉ L`. `FP`: R(c).

*Contacts.* `b ∈ C(a)`: a node of `F_b ∩ F#_a` is in `F_a` or is `ρ(w', z)`, `z ∈ UMN(a)`, which lies only in `F_{w'}`,
`E_z`; so `w' = b`, `z ∈ UMN(a) ∩ UMN(b)`, and `F_a ∋ ρ(a, z)`, `E_z ∋ ρ(a, z), ρ(b, z)`. Hence between two elements of
`C(a)` a walk `[E_w,] F_a [, E_{w'}]` (possibly shorter if `w = w'`). Dually `[F_z,] E_h [, F_{z'}]` between two elements
of `C'(h)`. Here `b ∈ B`, `a' ∈ A`, and `w > a, b`, `z < h, a'`.

*Conflict list of Lemma G* (E-sides against F-sides; two sides of one type never conflict):

| E-side | F-side | Why no conflict |
|---|---|---|
| kept E-member `e` | kept F-member | `P` valid |
| kept `e` | `F_a` | `e <= a` gives `e ~ a` (`a ∈ A`), `pos(e) ∈ Pos[a]`, not kept |
| kept `e` | `F_z` | `e <= z < a'` contradicts `a' ∈ A` |
| `E_h` | kept F-member `f` | `h <= f` gives `f ~ h` (`h ∈ B`), `pos(f) ∈ Pos[h]`, not kept |
| `E_h` | `F_a` | `h ≰ a` (hypothesis) |
| `E_h` | `F_z` | `z < h` |
| `E_w` | kept `f` | `b < w <= f` contradicts `b ∈ B` |
| `E_w` | `F_a` | `a < w` |
| `E_w` | `F_z` | `b < w <= z < h`, `b, h` F-members, contradicts `b ∈ B` (also for `b ~ h`, `b = h`) |

So the side set is conflict-free; `↓(F-sides)` picks it (no switch has both sides, as `{E_w, F_w}` is a conflict pair);
a shortest sub-walk from `s` to `t` is a valid path. Walks: `p_2 ∈ T(h)`: `1..p_1`, E-chain, `p_2..p_3`, F-chain,
`p_4..r`; `p_3 ∈ T(h)`: `1..p_1`, E-chain, `p_3..p_2` backward, F-chain, `p_4..r`. In both the kept positions are
`[1, p_1] ∪ [p_2, p_3] ∪ [p_4, r]`, disjoint from `Z`. Count `r <= p_1 + 3 + (p_3 − p_2 + 1) + 3 + (r − p_4 + 1)`, i.e. sum
`<= 8`. A chain side that is itself a member only lowers the count. Lemma G holds; J is the same with one chain, sum
`d − c <= 4`. Neither uses P2.

### 2.4 Stage 0, Orientation, (★)

`|A|, |B| >= 10`. The first 10 by `l` have 10 distinct positions and `l >= L`, so `FR_L` (R(a)) contains every `b` with
`pos(b) < L`; likewise `FR_R`, `ER_U`, `ER_V`. `L = +∞` or `R = −∞` gives `C_0 = ∅`; `U = +∞` or `V = −∞` gives
`R_0 = ∅`; `l` never equals `−∞`, `r` never `+∞`. So finite values at the "otherwise". An element outside the first 9 of
a sort has value at most (or at least) the 10th, whatever the tie-breaks. For `a ∈ R_0`: `a ∈ ER_U ∩ ER_V` gives
`U <= pos(a) <= V`, `a ∉ E_0` removes the 5 end positions, and `E*` is a down-set, so the tied elements are in `R_0` as
well: `Pos[a] ⊂ [U + 5, V − 5]`. Same for `C_0`. So `V − U >= 10`, `R − L >= 10`.
Orientation: `U, V` are E-positions, `L, R` F-positions. `U < L`, `R < V`: `Pos[h] ⊂ [L + 5, R − 5] ⊂ (U, V) ⊂ (u(h), v(h))`
against J(b). `L < U`, `V < R`: `Pos[a] ⊂ (l(a), r(a))` against J(a). `L < U`, `R < V`: replace each position `p` by
`r + 1 − p`; `P` reversed is a shortest valid path with `s`, `t` exchanged; `E_0`, `H_0`, `F*`, `E*`, `R_0`, `C_0` stay the
same sets; `(L, R, U, V)` become `(r+1−R, r+1−L, r+1−V, r+1−U)`, so `U < L`, `V < R`; `D` does not depend on the direction.
(★): `p_1 = u(h) <= U`, `p_4 = r(a) >= R`. `ρ >= U + 5`, `γ >= L + 5 > U + 5`; `ρ <= V − 5 < R − 5`, `γ <= R − 5`. So
`p_2 − p_1 >= 5`, `p_4 − p_3 >= 5`, sum `>= 10`. `Z ⊂ (p_1, p_4)` by the inclusions. Lemma G then forces an element of
`Z` in `[p_2, p_3]`. Holds. `ρ ≠ γ` by type.

### 2.5 Stage 1, Case I

`κ`: last positions are distinct, so the tail statement is right. Case I: 10 distinct last positions, `a_1`, `a_2` at
distance `>= 9`. `W ∩ (EP(a_1) ∪ EP(a_2))` misses `A`: an `a ∈ win(a_1) ∪ win(a_2)` is outside `W`, any other is outside
both `EP`. `F^1` misses `Up`. For `h` in a class of `𝓒_1`: every tied F-member is outside `FR(a_1, a_2)`, so lies in
`C(a_1) ∪ C(a_2)` (R(a)); `h < a_i` gives `h ∈ EP(a_i) ∩ W`; `h ~ a_i` is impossible (`L ∩ Up = ∅`). So `h ≰ a_i`.
Shape A holds. As `F_κ ⊆ F^1`, no class of `𝓒_1` is in `κ`; every such class has a position in `tail`.

*Shape B.* 20 elements of 20 classes, so 20 distinct positions; two pairs at distance `>= 9` from disjoint classes; R(b):
`D ⊇ L`. Let `a ∈ A ∩ D`: `a ∈ R_0`, its class is outside `κ`, so it has a position in `tail`. `Λ` has both types, so
consecutive `ρ` (element `a''`, class of `R_0` inside `D`) and `γ` (element `g`, class of `𝓒_1`). At most one of the four
classes `[h_i]` contains `g`, so a pair, say `h_1, h_2`, avoids `γ`. `a'' ∈ ER(h_1, h_2)` gives `ρ ∈ T(h)`, `h ∈ {h_1, h_2}`
(R(b)); `g ∉ FR(a_1, a_2)` gives `γ ∈ S(a')`, `a' ∈ {a_1, a_2}` (R(a)). The closed interval between `ρ` and `γ` lies in
`tail`, so it misses `Pos[a']`; interior points are not in `Λ`, so not in `Pos[h]` (`[h] ∈ 𝓒_1`); `ρ ∉ Pos[h]` by type;
`γ ∉ Pos[h]` by the choice of the pair. `h ≰ a'`, `a' ∈ R_0`, `h ∈ C_0`: against (★). The claim holds; since
`|𝓒_1| >= 20` and all its classes are outside `κ`, the second alternative of the claim never occurs: **`D` misses `A`.**

### 2.6 Count, Corollary B1

Shape A: `FR_L, FR_R` 4; `H_0` 28; representatives of classes of `C_0` in `κ` at most 10; `a_1, a_2` 2; `W` 18; `𝓒_1` 19.
That is 81; the stated 91 is an upper bound. Shape B: `ER_U, ER_V` 4, `E_0` 28, `E_κ` at most 20, 4: 56.

*Defect (trivial).* Theorem B's text says "one of four explicit monotone formulas" and Cor. B1 enumerates "the four
shapes", but the proof also exits with `⋂_{a ∈ A} (M − ↑a)`, `|A| < 10`, and `⋃_{b ∈ B} ↓b`, `|B| < 10` (Stage 0). When
both `|A|, |B| < 10` these are not instances of a shape, since a shape forces `FR(x, y)` or `ER(x, y)` with free `x, y`,
and those need not be correct for near `x, y`. The other exits `F*`, `E*`, `F* ∪ ⋃ ↓b` are harmless: with `|A|, |B| >= 10`
adding a far `FR(a_1, a_2)` with its `W ∩ EP` part keeps `D ∩ Up = ∅`, and they are also trivially enumerable.
*Repair, in full:* in Cor. B1 also test, for every set `S` of at most 9 switches, `⋂_{a ∈ S} (M − ↑a)` and
`⋃_{b ∈ S} ↓b`, and in the formulas allow every role to be empty. Soundness is unaffected (every result is a down-set),
and completeness now covers every exit.
Soundness: all formula values are down-sets, and a connecting mode vector is a yes-certificate by definition. Completeness:
`s = t` accepted; `s ≠ t`, yes-instance: Lemma 3.4(c) gives a valid path, hence a shortest one, and Theorem B gives a
formula picking it. Holds with this repair.

## 3. Case II, written out; Proposition C

*Atom by atom.* Case II: at least 10 of the `κ_i` are classes of `C_0`; `h_1`, `h_2` are elements at the first and last of
their 10 last positions, distance `>= 9`, `Pos[h_i] ∩ tail = ∅`.
`E^1 = E* ∩ E_κ ∩ ER(h_1, h_2) ∩ (V_0 ∪ (FP(h_1) ∩ FP(h_2)))`, `V_0 = ⋃_{b ∈ win(h_1) ∪ win(h_2)} ↓b`.
`E^1 ⊇ L`: a `b ∈ B` is in `V_0` or outside both windows, then in both `FP` (R(c)). Under the reversed instance (`qp-proof.md`
Lemma 4.4) `FR` is the complement of `ER`, `EP` of `FP`, `↓b` of `M − ↑b`, unions and intersections swap; so `E^1` is the
complement of `F^1` of the reversed instance. For `a` in a class of `𝓡_1` (classes of `R_0` meeting `E^1`): `Pos[a]` lies
in `T(h_1) ∪ T(h_2)` (R(b)); `a > h_i` gives `a ∉ FP(h_i)` and `a ∉ V_0`, so `a ∉ E^1`; `a ~ h_i` is impossible. So `h_i ≰ a`.
Shape A': `D = E^1 ∩ ⋂_{𝓡_1} (M − ↑a)` contains `L`, misses `A`. Holds.
Shape B': `D = F* ∪ F_κ ∪ FR(a_1, a_2) ∪ FR(a_3, a_4)`, misses `Up`. Let `g ∈ B − D`: `g ∈ C_0`, class outside `κ`, position
in `tail`. Classes of `𝓡_1` are outside `κ` (`E^1 ⊆ E_κ`). `Λ` = positions in `tail` of the classes of `C_0` outside `D` and of
the classes of `𝓡_1`; consecutive `γ`, `ρ` of different type; a pair `a_1, a_2` whose classes avoid `ρ`; `γ ∈ S(a')` (R(a));
`ρ ∈ T(h')`, `h' ∈ {h_1, h_2}` (R(b)). Closed interval in `tail`, so no `Pos[h']`; interior not in `Pos[a']`; `ρ ∉ Pos[a']` by the
choice; `γ ∉ Pos[a']` by type. `h' ≰ a'`: against (★). Holds, directly, with the same (★); no duality is needed.

*What the dual really is.* The reversed instance exchanges `(l, r, L, R)` and `(u, v, U, V)`; the orientation `U < L`, `V < R`
becomes `L < U`, `R < V`, so the path must be reversed as well, and then "sorted by last position" becomes "sorted by first
position, from the right". So the dual of Case I is the *mirror case* II°: `κ'` = the 20 classes with the largest first
positions, `tail' = (−∞, p*)`. Case II as written (tail on the right) is not the dual of anything, and it is vacuous:

**Proposition C.** After Orientation (`U < L`, `V < R`, `R_0, C_0 ≠ ∅`):
(a) every class of `C_0` has a position `> V`, and every class of `R_0` has a position `< L`;
(b) all positions of `R_0` are `<= V − 5`, all positions of `C_0` are `>= L + 5`; hence in the sort by last position every
class of `R_0` comes before every class of `C_0`, and in the sort by first position every class of `R_0` comes before every
class of `C_0` as well;
(c) in Case II all classes of `R_0` lie in `κ`, so `E_κ` misses `R_0`, `E* ∩ E_κ` misses `A`, `𝓡_1 = ∅`. Shape B' and Shape A'
with `𝓡_1 ≠ ∅` never occur; Case II ends with `D = E* ∩ E_κ` (at most `4 + 28 + 10` switches);
(d) so Theorem B needs Case I only: if `R_0` has at most 10 classes, `E* ∩ ⋂ (M − ↑a)` (representatives) picks `P`;
otherwise Case I. Shapes A', B' can be deleted; two shapes and the exits remain.
*Proof.* (a) `u(h) <= U`, `v(h) >= V`, `v(h) − u(h) >= 10`, so by J(b) `Pos[h] ⊄ (u(h), v(h))`; positions differ from `u(h)`, `v(h)` by
type; `Pos[h] >= L + 5 > U >= u(h)`; so some position is `> v(h) >= V`. Dually `l(a) <= L`, `r(a) >= R`, `r(a) − l(a) >= 10`,
`Pos[a] <= V − 5 < R <= r(a)`, so some position is `< l(a) <= L`. (b) `V − 5 < V <` last position of a `C_0` class;
`L >` first position of an `R_0` class, `L + 5 <=` first position of a `C_0` class. (c) If at least 10 of the first 20 classes
are of `C_0`, then some class of `C_0` is in `κ`, and by (b) all classes of `R_0` precede it. (d) follows. ∎

*Optional simplification (from C, not needed).* If `R_0` has at most 10 classes, `E* ∩ ⋂ (M − ↑a)` picks `P` (at most 42 switches). Otherwise let `κ` be the first 10
classes of `R_0` by last position; every other class of `R_0` and every class of `C_0` has a position in `tail`; `F_κ` disappears. Shape A then has at most
`4 + 28 + 2 + 18 + 19 = 71` switches and Shape B at most `4 + 28 + 10 + 4 = 46`, so the exponent 91 becomes 71.

## 4. Computations

Own code in `rv-r7-desc/`: `swf.py` (general switch form, P2, Construction 3.1, solver over states `(side, Up, Dn)` with dominance, all shortest paths, enumeration of
down-sets, atoms), `proof.py` (the construction with every claim asserted: Lemmas 4.2, 4.4, 4.5, R, EP, FP, J, G, X, Theorem A, Stage 0, Orientation, Proposition C, (★), Stage 1,
Case I, Shapes A, B, Case II as written, mirror case II° with Shapes A', B'; each `D` tested as a down-set, `L ⊆ D ⊆ M − Up`, connecting), `design.py`, `run_*.py`; logs in `runs/`,
summary in `runs/planted-summary.txt`, totals by `totals.py`. Sorts use random tie-breaks; the subsets of `κ` and the 20 classes are random. Nothing of `open-cases/r7-desc/` is
imported, except in `cross_check_final.py`. **All logs end with `FAILURES: none`; `ce/` is empty.**

| Run | Instances | Stages reached |
|---|---|---|
| `run_tiny.py` (12 parts) | exhaustive: preorders on `m <= 3` up to isomorphism, all sides over `{s, t, n}` (`m <= 2`: `{s, t, n, n'}`), middle edges on strict pairs: 6,985,685 instances, 11,527,654 paths; solver equal to the enumeration of down-sets | Stage 0 only (`|A|, |B| < 10`) |
| `run_random.py` | 120,000 random P2 instances with few classes, 77,955 yes, 308,732 paths | Stage 0 only |
| `run_sound.py` | random switches in the roles of all shapes and exits: 720,000 values on 4000 instances (1392 no): always a down-set, never connecting on a no-instance | soundness of Cor. B1 |
| `run_saved.py` | `r7-lb/inst` (4), `r7-lb/runs/adv` (61), `r7-lb/runs/sa` (6), `r4-search/instances` (157), `r5-core/runs/single` (23), `rv-r6-core/runs/deep` (188): 439 files, all shortest paths, 1088 paths | `|A| < 10` or `|B| < 10` except in `single`, `deep`, which end at the exits `F*`, `E*`. The `r7-lb` instances of cost 3, 4 are too small for Stage 1 |
| `run_fam.py` | `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k` (`k <= 14`; `back` variants `k <= 5`), `X_L` (`L <= 40`) | exits `F*`, `E*` from `k = 10`, `L = 20`; never past Stage 0 |
| `run_planted.py` | designs below: 114 verified bases, 20,814 accepted moves, 9,146 rejected; 27,624 runs of the construction, `m`, `r` up to 306 | table below |
| `run_mut.py` | harness power: planted paths made non-shortest: an assertion fires on 59 of 61 (Lemma G 57, Lemma J 2) | |
| `cross_check_final.py` | the author's `check_b.run_path`, `shortest_len` on 16 of my planted instances: same lengths, same stage counts (Case I 14, Case II 2, Shape A 6, Shape B 6, `F^1` alone 2) | agreement |

*Designs.* Stage 0 passes only if the far pairs chosen at the sorts touch all of `R_0`, `C_0`. So auxiliary classes `A*` (left of all contacts) and `B*` (right of all contacts), unusable
and with full contacts, fill the top of the sorts. Then: core `a_i`, `f_0`, zipper `x_j v_j y_j` with `{x_j, y_j}` a class and `v_j` a dead end for `E_{h_j}`, `f_1`. Variants: strict pairs (`A`), staircase with
E-contacts into `R_0` (`stair`), ties (`ties`), `R_0` and `C_0` interleaved so that `U < L < V < R` (`mix`), classes `{a^L_k, a^Z_k}` lying entirely in the E-star of `h_k` (`cross`: one pair of Shape B leaves a class, the second
removes it), few classes of `R_0` (`small`), tie-free all-strict (`allstrict`), random layout blocked by strict pairs (`cegis`). Every base: P2 asserted, `P` verified shortest by the exact solver, run on `P`, `P` reversed, the
reversed instance, both. Then random moves (added contacts, removed strict pairs, ties, contacts by middle witnesses, and *attacks*: a whole class of `A` put into the E-stars of 2-4 classes of `B`), each kept only if P2 holds and `P`
stays shortest: 4,549 attacks rejected by the solver, 1,863 kept and tested.

| Stage (runs of the construction, each path with 3 random tie-breaks) | Count |
|---|---|
| Stage 0 passed, `R_0`, `C_0` non-empty | 23,148 |
| of these, some non-strict pair in `R_0 × C_0` | 15,186 |
| Orientation direct / reversed | 11,574 / 11,574 |
| `|𝓚| < 20` / `|𝓚| >= 20` | 10,908 / 12,240 |
| Case I | 10,098 |
| Case I, `F^1` alone | 6,006 |
| **Shape A** with `𝓒_1 ≠ ∅` | 3,478 |
| **Shape B** | 614 (120 of them need the second pair) |
| Case II as written | 2,682, always `𝓡_1 = ∅` (Proposition C asserted on every run) |
| Shape A' with `𝓡_1 ≠ ∅`, Shape B', as written | **never: unreachable by Proposition C** |
| Shape A' / Shape B' in the mirror case II° (the true dual of Case I) | 3,483 / 612 |
| (★), pointwise | 131,639,070 tests |
| claim of Shape B / B', generalized to any `p*` and any far pairs from disjoint classes | 19,481 / 19,292 |

Largest span of `A ∩ NE(E#_x)` seen: 4 (Lemma 4.4 allows 8).

## 5. What is not checked

1. The chain from graphs to the general switch form (out of scope; reviewed elsewhere). The conclusion "DC in P" rests on it.
2. The algorithm of Cor. B1 is not run (`m^{71..91}`). Completeness rests on the construction from a known `P`; soundness is immediate and sampled.
3. The hard branch of the Shape B claim (a class of `R_0` outside `κ` in the stars of both pairs) never occurred: its assertion never failed, and the attacks that try to create it were rejected by the solver or kept without creating it. So this branch rests on the proof and on the (★) tests, which is what the claim predicts, since it says that the branch is empty.
4. Planted instances are my designs, with few usable flips; that is why exact verification of shortestness is feasible. `cegis` (random layout) ends at Stage 0.
5. `Y^d_k` with `back = True`: only `k <= 5` (the exact solver is slow beyond this).

## 6. Overall

The proof of §2-§3 holds. One repair is needed: the enumeration of Cor. B1 (§2.6). One correction of the text is recommended: Case II is not the dual of Case I and can be deleted (§3).
