# Round 4, agent r4-general: general ZZ + P2 beyond the switch model

Status: version 2 (2026-10-16 to 2026-10-22, with several interruptions; version 2 adds §8.1 and §10). Scripts: `r4-general/`.
Labels: **proved**, **checked** (exact computation on named instances), **sketch**, **conjecture**, **refuted**.
Notation as in `r4-brief.md`, `dc-algorithm.md` (ZZ, P2, `G_D`, zigzag, valley, peak, Lemma S), `dc-general.md` (pin
sets, Theorem GC, families `T_L^tie`, `T_L^one`), `dc-hardness.md` (2CH, TIC, Theorem H), `r4-switch.md` (side-set
certificates, Theorem 10: 2CH + P2 is in P). `B`, `T` are the classes of `u`, `v`; *middle* = neither. For `S ⊆ Q`:
`↑S`, `↓S` closures; `N^-(S)` = elements with an `R`-neighbour in `S` strictly above them, `N^+(S)` dually. A
*globally shortest* zigzag is a consistent zigzag of least length over the whole instance. Instances and code of other
agents (`r4-search/instances/*.json`, `r4-switch/sw.py`, `alg.py`, generators of earlier rounds) are used read-only.

## 0. Summary

**Verdict.** No polynomial algorithm for general ZZ + P2 and no reduction to 2CH + P2 was found; but the general
case collapses to the switch model (now known to be polynomial) whenever propagation of forced modes removes every
comparability between switches that still have a choice (Theorem R), and the known obstacles are located exactly
there: certificate methods fail on irrelevant comparabilities (families `X_L`, `Y_k`, `Y'_k`), which propagation
removes on every known instance.

| # | Result | Status |
|---|---|---|
| NG | **Neighbourhood generators.** `D(Γ, Π, Y) = Q - ↑(((Γ ∪ N^-(Π)) - ↓(Y ∪ {u})) ∪ {v})` is a down-set for every choice of pins (sound search); it contains a solution as soon as every minimal peak class of some consistent zigzag is in `Γ` or below an `R`-neighbour in `Π` and the lower neighbours of `Π` below valleys are covered by `Y`. For a globally shortest zigzag the pins pierce pairwise intersecting families (Lemma S + P2), `Y` needs two valleys per pin plus a cover of the *junk* | proved (§2) |
| NG-sw | In the switch model the junk is empty: 2CH + P2 is decided in `N^{2t} n^{4t}` time when the F-sides of every family of switches with pairwise disjoint E-sides can be pierced by `t` nodes (or dually); one-sided piercing suffices (weaker hypothesis than Theorem H). Superseded in complexity by r4-switch's Theorem 10, but a much smaller exponent | proved (§2.3) |
| NG ⊇ | Theorems F, F+, Fω, H, T, the ladders, `T_L^tie`, `T_L^one` (certificate number `⌊L/2⌋` in Theorem GC) are special cases with one or two pins | proved (§2.3) |
| NG-c | NG with at most 2 pins solves all 185 yes-instances of the earlier families and of `r4-search/instances` (133 portfolio-hard instances) | checked (§2.4) |
| Sub | Middle-middle edges not needed as witness edges can be subdivided (answer and P2 kept) | proved (§3.1) |
| Mon | A comparability whose removal creates a solution cannot be eliminated by adding elements or edges | proved (§3.2) |
| MW | A middle witness can be replaced neither by a bottom nor by a top witness (9-element example MW2) | proved, checked (§3.3) |
| X | **`X_L`**: rigid family plus one one-way mate per switch; P2, unique solution; every NG certificate and every GC certificate has size `>= ⌊L/2⌋` (junk is a real obstacle for pin certificates) | proved (§4); checked `L <= 12` |
| 5' | Side-set search of r4-switch extended to the general model by *conflict families* (`Π(E_w)` = F-sides of all `w' >= w`), with declarations: sound for all parameters; with `(1, 0, 2, 6)` or `(1, 1, 4, 8)` it solves every known yes-instance including `X_L` | proved (§5.1); checked |
| Y | **`Y_k`**: `R(E^k F^k)` plus one irrelevant one-way mate per E-member; P2, unique solution; the extended side-set search rejects it unless `kd + ks + s >= k` or `B >= k`; NG needs `>= ⌈k/2⌉` pins, GC `>= k`. **`Y'_k`** (one more private node per mate) also defeats the refinement "forbid the certificate, prune by reachability". Every walk certificate must watch every irrelevant comparability | proved (§6); checked `k <= 8` |
| HYB | **Propagation + certificates.** Forced-exit propagation fixes modes that every solution has (sound); followed by the extended side-set search it is a sound polynomial algorithm for every parameter, and with `(1, 0, 1, 3)` it solves all 196 yes-instances known (including `X_L`, `Y_k`, `Y'_k`) and 900 random instances. Caveat: 176 of the 196 are rigid (propagation fixes every switch) | proved (soundness, §7.3); checked |
| R | **Reduction to 2CH + P2.** If after a sound fixing the free switches are pairwise incomparable (and every pair of free switches has a common node or a fixed middle witness), contracting the fixed picked sides gives an equivalent 2CH + P2 instance, decided by r4-switch's Theorem 10. Applies to 188 of 192 family instances and to about 82% of random instances; answers agree with the exact ones on all | proved (§8); checked |
| R+ | **FPT in the free comparabilities.** Branching on a vertex cover `C` of the comparability graph of the switches left free by propagation gives `2^{|C|}` instances of 2CH + P2 (free middle witnesses are covered automatically): FPT in the vertex cover number, for any width | proved (§8.1); checked on 2000 random instances and the hub and two-route families |
| 10 | **One-way relations after propagation** (round 4b): free middle witnesses are free comparabilities (covered by R+); Lemmas 10.A-10.C and Prop. 10.D carry r4-switch's structure theory over to conflict families and show where it breaks (partner neighbourhoods with large storage, as in `Y_k`); pruning by the switch model (HYB-2CH, sound, polynomial via Theorem 10) | proved (§10); completeness open |
| Z | Two independent rigid routes cannot coexist under P2 without hubs that shortcut them (counting); the two-route family `Z_k` keeps its mates free, but its shortest solutions use the hubs and HYB solves it | sketch; checked `k <= 5` (§7.4) |
| Open | General ZZ + P2 when propagation leaves comparable free switches (ties or one-way relations between switches that still have a choice), or free middle witnesses. No instance of this kind is known on which HYB fails | open (§9) |

## 1. Two reformulations used throughout (proved)

**(R1) Consistency is a bipartite condition between minimal peaks and maximal valleys.** For any zigzag `W` let
`A(W)` be its minimal peaks and `B(W)` its maximal valleys. `W` is consistent iff no element of `A(W)` is `<=` an
element of `B(W)`: a conflict `x >= y` (valley `x`, peak `y`) gives `a <= y <= x <= b` for some `a ∈ A(W)`, `b ∈ B(W)`.

**(R2) Anchors.** If `Gen ⊆ Q` and every peak of `W` lies in `↑(Gen ∪ {v})` while no valley does, then `W` lies in
`G_D` for the down-set `D = Q - ↑(Gen ∪ {v})`, hence is consistent. The guess algorithms (Theorems F, F+, Fω) choose
`Gen = A(Z)` directly; Section 2 chooses `Gen` through the neighbourhoods of few pins.

## 2. Theorem NG: generators given through the neighbourhoods of few pins

### 2.1 Statement and proof

Let `Z` be a consistent zigzag with peaks `P`, valleys `V`. Take one representative of every *minimal peak class*
(class of a peak with no peak strictly below it), at its first occurrence on `Z`; call the set `A = A(Z)` and list it
by position, `a_1, a_2, ..., a_m`; `A_1 = {a_1, a_3, ...}`, `A_2 = {a_2, a_4, ...}`.
For *pins* `Γ, Π, Y ⊆ Q` put

    G = (Γ ∪ N^-(Π)) - ↓(Y ∪ {u}),        D(Γ, Π, Y) = Q - ↑(G ∪ {v}).

**Lemma NG1 (soundness; proved).** `D = D(Γ, Π, Y)` is a down-set with `u ∈ D`, `v ∉ D`; so every `u`-`v` path of
`G_D` is a consistent zigzag, for every choice of pins.
*Proof.* `D` is the complement of an up-set. `v ∈ ↑{v}`. `u ∈ ↑(G ∪ {v})` would need `g <= u` for some `g ∈ G`,
i.e. `g ∈ ↓u`, which `G` excludes, or `v <= u`, which is false. A `u`-`v` path of `G_D` is a consistent zigzag
(`verify/equivalence.md` §3). ∎

**Theorem NG (completeness; proved).** Suppose
(a) every `a ∈ A` lies in `Γ` or has an upper `R`-neighbour in `Π`;
(b) `(Γ ∪ Π) ∩ ↓V = ∅`;
(c) every element of `N^-(Π)` that lies below some valley of `Z` lies in `↓(Y ∪ {u})`;
(d) `Y ⊆ ↓V`.
Then `Z` lies in `G_D` for `D = D(Γ, Π, Y)`.
*Proof.* No element of `A` lies in `↓(Y ∪ {u})`: by (d) it would lie in `↓V`, and a peak in `↓V` is a conflict.
With (a), `A ⊆ G`. Every peak is `>=` an element of `A` (finite preorder), so `P ⊆ ↑G` and `P ∩ D = ∅`. Let `x` be a
valley in `↑(G ∪ {v})`. `v <= x` would put the peak `v` into `↓V`, which consistency forbids (`↓V ∩ ↑P = ∅`). So
`g <= x` for some `g ∈ G`; then `g ∈ ↓V`, so `g ∉ Γ` by (b) and `g ∈ N^-(Π)`; by (c) `g ∈ ↓(Y ∪ {u})`, contradicting
`g ∈ G`. Hence `V ⊆ D`. Every edge of `Z` joins a valley in `D` to a larger peak outside `D`, so it is an edge of
`G_D`. ∎

Theorem NG uses neither P2 nor minimality of `Z`; they enter only in the size bounds.

### 2.2 Size bounds (proved)

Let the instance satisfy P2 and let `Z` be globally shortest.
1. *Piercing.* For `i = 1, 2` the sets `N^+(a)`, `a ∈ A_i`, pairwise intersect: two elements of `A_i` are
   incomparable minimal peaks at distance `>= 4` (positions are distinct odd numbers), so by Lemma S(d) they have no
   lower witness and by P2 a common upper `R`-neighbour. Let `τ_i(Z)` be the least `|Γ_i| + |Π_i|` with `Γ_i ⊆ A_i`
   and `Π_i` meeting `N^+(a)` for every `a ∈ A_i - Γ_i`. Then `τ_i <= |A_i| <= ω(U)` (Theorem Fω), and `τ_i <= t`
   if pairwise intersecting families of upper neighbourhoods can be pierced by `t` elements.
2. With `Γ = Γ_1 ∪ Γ_2` and `Π = Π_1 ∪ Π_2` (so `Π ⊆ ↑P`), (a) and (b) hold.
3. *Adjacent valleys.* Each `π ∈ Π` lies outside `↓V`; by Lemma S(c) the valleys of `Z` that are `R`-adjacent to `π`
   lie within distance 2 of each other, so there are at most two, and they lie below `π`. Let `Y_0` be the set of
   these valleys over all `π ∈ Π`: `|Y_0| <= 2|Π|`.
4. *Junk.* `J(Z, Π) = (N^-(Π) ∩ ↓V) - ↓(Y_0 ∪ {u})`: lower neighbours of pins that lie below some valley but not
   below a valley adjacent to a pin. They are not on `Z` (a peak below a valley is a conflict; a valley in `N^-(Π)` is
   in `Y_0`). Let `σ(Z, Π)` be the least size of `Y_1 ⊆ ↓V` with `J ⊆ ↓Y_1`. Then `Y = Y_0 ∪ Y_1` satisfies (c), (d).

**Algorithm NG(t, s).** For all `Γ, Π ⊆ Q` with `|Γ| + |Π| <= 2t` and all `Y ⊆ Q` with `|Y| <= 4t + s`, compute
`D(Γ, Π, Y)` and search `G_D` for a `u`-`v` path; then the same on the *dual instance* (order reversed, `u` and `v`
exchanged, same edges and answer, lower and upper witnesses exchanged), which is the valley-side version
`D' = ↓(((Γ' ∪ N^+(Π')) - ↑(Y' ∪ {v})) ∪ {u})` with maximal valley classes and Lemma S(c), (d).
It runs in `O(q^{6t + s} (q + |R|))` time, never accepts a no-instance (Lemma NG1), and accepts every instance having
a globally shortest consistent zigzag `Z` and pins `Π` with `τ_1 + τ_2 <= 2t` and `σ(Z, Π) <= s`, on the peak or on the
valley side.

### 2.3 Special cases (proved)

1. **Theorems F, F+.** If every incomparable pair has a lower witness, each `A_i` has at most one element (two would be
   far incomparable minimal peaks without a lower witness), so `Γ = A`, `Π = Y = ∅`: `D = Q - ↑(A ∪ {v})`, `|A| <= 2`.
2. **Theorem Fω.** `|A_i| <= ω(U)`: `Γ = A`.
3. **Switch model (NG-sw).** In the ZZ form of 2CH (switches pairwise incomparable, `R`-neighbours of a switch are
   bottoms and tops) the upper neighbours of a switch are the tops of its F-side, so `Π` consists of tops, and
   `N^-(Π)` consists of bottoms and switches. A bottom lies in `↓u`; a switch below a valley is that valley itself
   (switches are pairwise incomparable and a switch is not below a bottom), and a valley of `N^-(Π)` lies in `Y_0`. So
   `J = ∅` always. Two switches of one group `A_i` have disjoint E-sides (no lower witness = no common bottom) and,
   by P2, intersecting F-sides. Hence: *if for every family of switches with pairwise disjoint E-sides the F-sides can
   be pierced by `t` nodes (or dually, with E and F exchanged), 2CH + P2 is decided by NG(t, 0) in
   `O(N^{2t} n^{4t} (N + n + |R|))` time.* Theorem H assumes that **every** pairwise intersecting family of E-sides
   **and** every such family of F-sides is pierced by `t` nodes; that implies the hypothesis here (on both sides), so
   NG-sw contains Theorem H; it needs the condition on one side only, and only for F-side families coming from
   E-disjoint switches.
4. **TIC (Theorem T).** Intervals are Helly, so `t = 1`.
5. **Ladder `K(k)`.** `Π = {v}`, `Y = {b_k}`: `N^-(v) = {a_1, ..., a_k, b_k}`, `G = {a_1, ..., a_k}`,
   `D = {u, b_1, ..., b_k}`, the unique solution.
6. **`T_L^tie`, `T_L^one` (`dc-general.md` §3).** Take `Π = {t_L}`, the top of junction `L`, `Γ = ∅`. The F-sides
   containing junction `L` are the flip sides `Fl_k = [k, K]` of the odd switches, the path side `h_L` if `L` is even,
   the side `[L, K]` of `Z`; no mate has `L` in its F-side (`F(m_k) = {K}` for even `k`, `{L + k}` for odd `k`). So
   every minimal peak (odd `x_k`, and `Z` in E-mode) is adjacent to `t_L`; the valleys adjacent to `t_L` are `x_L` (if
   `L` is even) and `Z` (in F-mode), which go into `Y_0`; the junk is empty (an odd `x_k` is a peak, and the mate
   `m_k` with `L ∈ F(m_k)` does not exist). Hence NG(1, 0) solves both families, whose certificate number in Theorem
   GC is `⌊L/2⌋` (Proposition M). The lower bound of Proposition M is a property of the pin-set certificates, not of
   the instances.
7. **Hub `H(m, m')`, classes version.** Theorem F class, item 1.

### 2.4 Checks

`r4-general/ng.py` (NG search; the dual side through `common_r4.dual`), `test_ng_families.py`, `test_ng_random.py`,
`test_ng_rigid.py`. Every accepted down-set is re-checked (down-set, `u ∈ D ∌ v`, a `u`-`v` path in `G_D`).

*Families* (`test_ng_families.py 2 0`, `runs_fam_2_0.txt`): `T_L^tie`, `T_L^one` (`L = 2..8`, `q <= 52`): NG with
one pin; `R_L` Helly form and 2CH form (`L = 2..8`), `R_L` with mates (`dc-general/families.rigid`, both kinds,
`L = 2..8`, `q <= 71`): one or two pins; ladders `K(k)`, `KW(k)` (`k = 2..6`): one pin; all 133 instances of
`r4-search/instances` (portfolio-hard at level 2 or 3, among them `L2-sw-20`, `L2-sw-21`, `L2-tie-23`,
`L2-oneway-23`, `L3-oneway-31`, the 28 instances `enum-q10-*`, the shrunk `R_8`, `T_6`, `T_8` instances): one or two
pins. Total 185 yes-instances, all solved by NG with at most 2 pins (98 with one, 87 with two). The six hub
no-instances `H(1,1)`, `H(2,2)`, `H(2,3)` (both versions) are rejected (as they must be). The single pin of §2.3
item 6 (`Π = {t_L}`, `Y = {x_L}` for even `L`, `Y = ∅` for odd `L`) gives the solution of `T_L^tie` and `T_L^one`
for `L = 2..10` (`check_tl_pin.py`).
*Rigid family, 2CH form* (`test_ng_rigid.py`, `runs_rigid_2.txt`): two pins suffice up to `L = 9`, not for
`L = 10..13`. Here the F-sides of the odd switches meet pairwise only in private `w`-nodes, so the piercing number
grows like `L/4`; this is the non-Helly obstacle of the switch model (Theorem H fails on the same family), not junk.
*Random* (`test_ng_random.py 1 1500`): 1500 instances (general preorders with ties and middle edges from
`gcert.random_inst`, mixed witnesses from `mixed.random_instance`, switch model from `twoch.random_p2_instance`):
788 yes-instances, all solved with one pin (582 with none), 712 no-instances, none accepted; exact answers by
`gcert.exact` and, for `q <= 20`, by the enumeration of all down-sets (0 mismatches).

## 3. Reductions between the variants

### 3.1 Subdivision of middle edges (proved; checked)

**Lemma Sub.** Let `e = {y, x} ∈ R`, `y < x`, and let `I'` be `I` with `e` removed and two new elements `b_e` in the
class of `u`, `t_e` in the class of `v`, with the edges `y t_e`, `b_e t_e`, `b_e x`. Then `D ↦ D ∪ {b_e}` is a bijection
between the down-sets of `I` and of `I'` (with `u` in, `v` out), and `u`, `v` are connected in `G_D` iff they are in
`G'_{D ∪ {b_e}}`. P2 holds in `I'` iff every incomparable pair of `I` has a witness `w` whose two edges are not `e`.
*Proof.* `b_e ∈ D'`, `t_e ∉ D'` for every admissible `D'`, so the edge `b_e t_e` is always present; `y t_e` is present
iff `y ∈ D`, `b_e x` iff `x ∉ D`. If `e ∈ G_D` (`y ∈ D ∌ x`) the path `y t_e b_e x` replaces it; otherwise the two new
elements form a pendant path at `y` or at `x`, or are isolated. The new elements are comparable with everything; the
witnesses of the old pairs are unchanged except those using `e`. ∎
Hence every `R`-edge between middle elements may be assumed to be a *witness edge* (needed for P2). In the language
of `r4-brief.md` N6 the general model is: 2CH with a preorder on the switches (the modes form a down-set) in which P2
is met by a common node, or by a *conditional connector* (a middle witness `w < x, y` whose F-side meets `E_x` and
`E_y` through private nodes; dually above). Checked (`test_reductions.py 1 3000`, `runs_reductions_1.txt`): 1068
middle-middle edges of random P2 instances subdivided, answer unchanged in all, P2 kept in 907.

### 3.2 Order relations and ties cannot be removed by adding things (proved)

**Lemma Mon.** If `I'` arises from `I` by adding elements and `R`-edges (the order on the old elements unchanged),
every solution down-set `D` of `I` gives the solution `↓_{I'} D` of `I'` (old elements keep their side, every edge of
`G_D` stays). Consequently, if deleting an order relation `y < x` (or splitting a tie) from `I` creates a solution,
no instance obtained from the relaxed instance by adding elements and edges has the answer of `I`: an
answer-preserving elimination must delete edges, delete elements, or add order relations elsewhere. This is the
precise form of the remark that 2CH has no gadget for an implication: the conflict "`x` a valley, `y` a peak" can
only be excluded by taking connectivity away. ∎

### 3.3 A middle witness is not a bottom or top witness (proved; checked)

**Example MW2** (9 elements; `test_reductions.py`, function `mw_example`). `u = 0`; `z = 1`, `z' = 2` in the class of
`u`; middle `p = 3 < w = 4 < x = 5`, `w < y = 6`, `x < a = 7`; `v = 8`. `R`: `u p, z p, z x, w x, w y, z' y, z' v,
u a, x a, a v, y v`. P2 holds (the incomparable middle pairs are `{x, y}`, witness `w` only, and `{a, y}`, witness
`v`). No solution: a route from `u` to `v` must reach `x` as a peak through `u p z x` (so `p ∉ D`) and continue to `y`
through `w ∈ D`, but `p < w`; the other route `u a x` reaches `x` as a valley, whose only upper neighbour is `a`.
Adding a new bottom witness `b` of `x, y` creates the solution `u p z x b y z' v`; adding instead a new top witness
`τ` creates `u a x τ y v` (`D = ↓{x, y} ∪ B`). So the conditional witness `w` can be replaced neither by an
unconditional lower nor by an unconditional upper witness (checked by `gcert.exact`; the 8-element version without
`a` refutes the bottom replacement only).

## 4. The limits of pin certificates: junk, the family `X_L`

**The family `X_L`** (`r4-general/xfam.py`; switch model with an order on the switches, converted by
`dc-general/families.to_inst`). Base: the rigid family `R_L` in Helly form *without* the `w`-nodes: switches
`x_1 .. x_L`, path side `h_k` (E for odd `k`, F for even `k`), flip side `Fl_k` (the other type); `s ∈ h_1`, `t ∈ h_L`,
`y_k ∈ h_k ∩ h_{k+1}`, `z_pq ∈ Fl_p ∩ h_q` (`p < q`, `q - p` odd), `t ∈ Fl_k` for all `k`. Mates:
- even `k`: `m_k < x_k`, `E(m_k) = {n_k, n'_k} ∪ {n_kj : j even, j != k} ∪ {c_ik : i odd}`, `F(m_k) = {t}`, with
  `n_k, n'_k` added to `h_k = F(x_k)` and `n_kj` added to `Fl_j = E(x_j)`;
- odd `k`: `m_k > x_k`, `E(m_k) = {t} ∪ {c_kj : j even}`, `F(m_k) = {e_k, e'_k} ∪ {n'_kj : j odd, j != k}`, with
  `e_k, e'_k` added to `h_k = E(x_k)` and `n'_kj` added to `Fl_j = F(x_j)`.
Every middle element is comparable with at most one other; no ties, no middle edges, all witnesses are nodes.

**Proposition X (proved; checked `L <= 12`).** For `L >= 2`:
(i) `X_L` satisfies P2;
(ii) `X_L` has exactly one solution: `x_k` in E-mode for odd `k`, F-mode for even `k`, even mates in F-mode, odd mates
in E-mode;
(iii) every NG triple `(Γ, Π, Y)` whose down-set contains a solution has `|Γ| + |Π| + |Y| >= ⌊L/2⌋`, and so has every
triple of the valley-side search;
(iv) the certificate number of Theorem GC is `κ(X_L) = ⌊L/2⌋`.
*Proof.* (i) Same parity: the flip sides share `t`. Opposite parity: `z_pq`. Even mate `m_k` with odd `x_j`:
`F(m_k) = {t} ⊆ Fl_j = F(x_j)`; with even `x_j`, `j != k`: `n_kj ∈ E(m_k) ∩ Fl_j`. Odd mate `m_k` with even `x_j`:
`t ∈ E(m_k) ∩ Fl_j`; with odd `x_j`, `j != k`: `n'_kj ∈ F(m_k) ∩ Fl_j`. Mates of equal parity share `t`; an odd and
an even mate share a `c`-node. A mate and its own switch are comparable.
(ii) Let a mode vector consistent with the order connect `s` and `t`, and let `r` be the least index with `x_r` not in
the mode above. The picked sides `h_1, .., h_{r-1}` contain the nodes `s`, `y_i`, `z_pi` (`p < i`), `n_i, n'_i` (even
`i`), `e_i, e'_i` (odd `i`). The other sides containing them are `h_r` (contains `y_{r-1}`; not picked), `Fl_p` with
`p < i < r` (not picked, `x_p` unflipped), `E(m_i)` for even `i < r` (not picked: `m_i < x_i` and `x_i` in F-mode force
`m_i` into F-mode) and `F(m_i)` for odd `i < r` (not picked: `x_i < m_i`, `x_i` in E-mode forces `m_i` into E-mode).
So the component of `s` is the union of `h_1 .. h_{r-1}`, which does not contain `t` (`t` lies only in `h_L`, in flip
sides and in mate sides). Hence all `x_k` have the stated modes, the order forces the mates, and this vector connects
(`h_1 .. h_L`).
(iii) Let `D = D(Γ, Π, Y)` contain a solution; by (ii) `D = D*`. Each odd `x_k` lies outside `D*`, so some `g ∈ G` is
`<= x_k`; below `x_k` there are only bottoms (excluded from `G`) and `x_k`, so `x_k ∈ Γ ∪ N^-(Π)`. The upper neighbours
of an odd `x_k` are the tops of `t`, of `z_kq` (adjacent below: `x_k`, `x_q`) and of `n'_jk` (adjacent below: `m_j`,
`x_k`); each upper neighbour other than `v = t_t` is adjacent to one odd switch only. If `v ∉ Π`, then
`|Γ| + |Π| >= ⌈L/2⌉`. If `v ∈ Π`, every even mate `m_k` (`F(m_k) = {t}`) lies in `N^-(Π) ∩ D*`, so it must lie in
`↓(Y ∪ {u})`; the elements above `m_k` are `m_k`, `x_k` and the tops (a top in `Y` empties `G`, and `D = Q - T` is not
`D*`), so `Y` meets each of the `⌊L/2⌋` disjoint sets `{m_k, x_k}`. The valley side is symmetric: every even `x_k`
must lie in `Γ' ∪ N^+(Π')`, the lower neighbours of an even `x_k` other than `b_t` serve one even switch each, and if
`b_t ∈ Π'` the odd mates (`t ∈ E(m_k)`) force `|Y'| >= ⌈L/2⌉`.
(iv) Every admissible walk of Theorem GC is a consistent zigzag (Lemma 1 of `dc-general.md`), hence lies in `G_{D*}`,
where the picked sides containing path nodes form the chain `h_1 .. h_L` (`h_i ∩ h_j = ∅` for `|i - j| >= 2`); so it
visits every `x_k`, the even ones as valleys. General mode: (A2) at the valley `x_k` (even) needs `x_k ∈ D-`, or
`m_k ∈ D-`, or `m_k ∈ M-`; a pin `>= m_k` is `m_k`, `x_k` or a top (a top puts the peak `v` into `D-`), and the lower
neighbours of `m_k` (`b_{n_k}, b_{n'_k}, b_{n_kj}, b_{c_ik}`) are adjacent above to `m_k` and otherwise only to
elements that are not even mates. So each even `k` needs a pin in its own set `{m_k, x_k} ∪ N^-(m_k)`, and these sets
are disjoint: `|π| >= ⌊L/2⌋`. Peak-pinned mode needs every odd `x_k` in `G+`, valley-pinned mode every even `x_k` in
`G-`. The valley-pinned certificate `G- = {x_k : k even}` works. ∎

*Checked* (`test_xfam.py`, `runs_xfam_*.txt`): `L = 2..8`: P2, exactly one solution (brute force over the
order-consistent mode vectors of the `2L` switches), exact answer; NG with budget 1 solves `L <= 5` only (`|Y_0| <= 2`
absorbs at most two mates), budget 2 (four exceptions) `L <= 9`, budget 3 `L <= 12` (as (iii) predicts, through
dummy pins that only enlarge `Y`); GC: `κ <= 2` for `L <= 5`, `κ = 3` for `L = 6, 7` (pinned modes), no certificate of
size `<= 3` for `L = 8`.

**Reading.** In the switch model the junk of Theorem NG is empty (§2.3, item 3) and the neighbourhood certificate is
bounded whenever one-sided piercing is; `X_L` shows that a single one-way relation per switch suffices to make every
pin-based certificate (stored conflicts of Theorem GC, neighbourhood generators of Theorem NG, guesses of Theorems F,
Fω) unbounded. The obstacle is exactly the junk: elements off every solution that lie below a valley (or above a
peak) and next to every useful pin.

## 5. Side-set certificates of r4-switch on the general model

`r4-switch.md` (version of 2026-10-17, read-only) proves that 2CH + P2 is in P (its Theorem 10): certificates are sets
`K` of sides, unions of a bounded number of *neighbourhoods of sides* `N_O[Z]` and single sides; a walk of sides is
admissible if the partner of every member lies in `K` and no member is the partner of a stored member. The natural
extension to the general model replaces the partner `X'` of a side `X` by its *conflict family* `Π(X)`: for `X = E_w`
the F-sides of all `w' >= w`, for `X = F_w` the E-sides of all `w' <= w` (ties included). Soundness carries over
verbatim (a conflict pair `X`, `Y` has `Y ∈ Π(X)` and `X ∈ Π(Y)`, so both are stored and the later one is refused).
On `X_L` the conflict families are covered by two neighbourhoods: `N_E[E(m_1)]` contains the E-sides of all even mates
(through the nodes `c_1k`) and all `Fl_k`, `k` even (through `t`); `N_F[Fl_{L'}]` (`L'` the largest odd index)
contains the F-sides of the other odd mates (through `n'_{k L'}`) and all odd `Fl_k`; the storage is bounded (only
`h_L` among the path sides meets `E(m_1)`, and only path sides `h_q` with `q > L'` meet `Fl_{L'}`). So `X_L` is not an
obstruction to side-set certificates (checked in §5.1).

### 5.1 The generalized search (proved) and its checks

**Setting (general switch form, `r4-general/gsw.py`).** Nodes: the components of the graph of the `R`-edges between
`B` and `T`, plus one private node for each `R`-edge between two middle elements (Lemma Sub); switches: the middle
elements, with `E_w` = nodes of the lower `R`-neighbours, `F_w` = nodes of the upper ones; the modes must form a
down-set of the preorder. Then `u`, `v` are connected in `G_D` iff `s`, `t` are connected in the hypergraph of the
picked sides (checked against brute force on all random instances with at most 14 switches, see below). A walk of
sides (consecutive sides equal or meeting, `s` in the first, `t` in the last) is *valid* if no two of its sides form a
conflict pair (`E_w`, `F_{w'}` with `w <= w'`); valid walks exist iff the instance is a yes-instance.

**Theorem 5' (soundness; proved).** Fix a set `K` of sides and bounds `B`, `s`. Search over walks with state (current
side, `St` = members lying in `K`, `Dc` = declared sides, number of declarations). A side `Y` may be appended iff
`Y ∉ Dc`, `Π(Y) ∩ St = ∅`, and either `Π(Y) ⊆ K ∪ Dc`, or `Y ∉ K` and fewer than `s` declarations were made, in which
case `Π(Y) - K - Dc` is added to `Dc`; a side `Y ∈ K` is stored. Every accepted walk is valid.
*Proof.* Let `X` (first used at time `i`) and `Y` (first used at time `j > i`) be a conflict pair, so `Y ∈ Π(X)` and
`X ∈ Π(Y)`. At time `i`, `Y ∈ K`, or `Y ∈ Dc`, or `X` declares `Y`; in the last two cases `Y` is refused at time `j`.
So `Y ∈ K`, hence `Y` cannot declare. At time `j`: if `X ∈ K`, `X` was stored at time `i` and `Y` is refused. If
`X ∉ K` and `X ∉ Dc`, then `X ∈ Π(Y) - K - Dc` and `Y` would have to declare: refused. If `X ∉ K` but `X ∈ Dc`, then
`X` was declared after time `i` (it was appended at `i`) by a member `Z` with `X ∈ Π(Z)`, used after `X`; the pair
`X`, `Z` is a conflict pair with `Z` later, and the argument just given (applied to `Z` at its time, when `X ∉ K ∪ Dc`)
shows that `Z` lies in `K` and has to declare `X`, which is not allowed. ∎
Completeness for a valid path `P`: it suffices that `K` contains `Π(Y)` for every member `Y` except at most `s`
members outside `K`, and `|P ∩ K| <= B`. With `K = K_E ∪ K_F`, `K_E` a union of `kd` sets `N_F[Z]` and `ks` single
F-sides and `K_F` likewise, this is r4-switch's Theorem 11 when the order is trivial (`Π(Y)` = the partner).

*Checked* (`test_gsw.py`): random general instances (`random 1 900`: 900 instances, all with P2, 457 yes): the
conversion agrees with brute force on all instances with at most 14 switches, the search never accepts a
no-instance, and parameters `(kd, ks, s, B) = (1, 0, 2, 6)` solve all 457 yes-instances. Families
(`runs_gsw_fam_1026.txt`): with `(1, 0, 2, 6)` the search solves `X_L` (`L <= 8`; one dominator per type),
`T_L^tie`, `T_L^one`, `R_L` with mates, `R_L` 2CH form, the ladders, and 104 of the 133 instances of `r4-search`; the
29 others (`enum-q10-*`, `L2-q10-b`: 10 elements, ties and middle edges) need one single side; with `(1, 1, 4, 8)`
all 186 yes-instances of this run are solved (`runs_gsw_fam_1148.txt`, `min_cert.py`). The hub no-instances are rejected.

## 6. An obstruction for every known certificate: the family `Y_k`

**The family `Y_k`** (`r4-general/yfam.py`). Base: the rigid word family `R(E^k F^k)` in 2CH form (switches
`x_1 .. x_{2k}`; path side `h_j` of type E for `j <= k` and F for `j > k`, flip side `Fl_j` of the other type; nodes
`s ∈ h_1`, `t ∈ h_{2k}`, `y_j ∈ h_j ∩ h_{j+1}`, `z_pq ∈ Fl_p ∩ h_q` for `p < q` of different modes, `w_pq ∈ Fl_p ∩ Fl_q`
for `p < q` of equal modes). For every E-member `c <= k` a mate `m_c > x_c` (one-way relation) with
`F(m_c) = {f_cb : b <= k, b != c}`, `f_cb` added to `Fl_b = F(x_b)`, and
`E(m_c) = {e_cq : q > k} ∪ {g_cc' : c' <= k, c' != c}`, `e_cq` added to `Fl_q = E(x_q)`, `g_cc'` shared by `m_c`, `m_c'`.

**Theorem Y (proved; checked `k <= 8`).**
(i) `Y_k` satisfies P2 and has exactly one solution (`x_j` in its path mode, mates in E-mode).
(ii) The generalized side-set search of Theorem 5' with `K_E` a union of `kd` sets `N_F[Z]` and `ks` single F-sides
(any `K_F`) and parameters `s`, `B` rejects `Y_k` whenever `kd + ks + s < k` and `B < k`.
(iii) Every successful NG triple (either side) has `|Γ| + |Π| >= ⌈k/2⌉`.
(iv) Every certificate of Theorem GC has at least `k` pins in general mode and `k` generators in the pinned modes.
So `Y_k` defeats simultaneously the pin certificates (GC), the neighbourhood generators (NG) and the side-set
certificates with conflict families; the threshold `B = k` is sharp in the runs (one dominator, at most four
declarations: accepted with `B = k`, rejected with `B = k - 1`, `k = 6, 7, 8`).
*Proof.* (i) P2: switches of equal mode share a `w`-node in their flip sides, of different modes a `z`-node
(`Fl_p ∩ h_q`); `m_c` and an E-member `x_b` (`b != c`) share `f_cb ∈ F`; `m_c` and an F-member `x_q` share
`e_cq ∈ E`; two mates share `g`; `m_c`, `x_c` are comparable. Uniqueness: let `r` be the first switch of the base not
in its path mode. A mate `m_c` with `c < r` is in E-mode (`x_c` is in E-mode and `x_c < m_c`). The nodes of
`h_1, .., h_{r-1}` are `s`, `y`-nodes and `z_pi` with `p < i < r`; they lie in no mate side, in `h_r` only through
`y_{r-1}`, and in flip sides `Fl_p` with `p < r` (not picked). So the component of `s` is `h_1 ∪ .. ∪ h_{r-1}`, which
misses `t`. Hence the base is in its path modes and every mate in E-mode.
(ii) Let the search accept a walk `W`. `W` is valid (Theorem 5'), so the down-set of its modes is a solution, the
unique one; the picked sides that contain path nodes are `h_1, .., h_{2k}`, which form an induced path of the side
graph, and the picked mate sides `E(m_c)` meet only flip sides of F-members and each other, never a path side; so `W`
is a walk along `h_1 .. h_{2k}` and contains every `h_c`, `c <= k`. `Π(h_c) = {Fl_c, F(m_c)}`. `F(m_c)` can be
declared only by a member whose conflict family contains it, i.e. by `h_c = E(x_c)` or `E(m_c)`, and `E(m_c)` is not on
`W`. So for each `c <= k`: `F(m_c) ∈ K`, or `h_c` declares. The nodes `f_cb` of `F(m_c)` lie only in `F(m_c)` and in
`Fl_b`; so a set `N_F[Z]` contains `F(m_c)` only if `Z = F(m_c)` or `Z = Fl_b` (`b != c`). If some dominator is
`N_F[Fl_b]`, it contains all F-members `h_q` (`z_bq ∈ Fl_b ∩ h_q`), which are members of `W`, so `B >= k`. Otherwise every
dominator and every single side contains `F(m_c)` for at most one `c`, and `kd + ks + s >= k`.
(iii) Below an E-member `x_c` lie only bottoms, so every `x_c` must be in `Γ` or have an upper neighbour in `Π`; an
upper neighbour of `x_c` is a top of `z_cq` (adjacent below: `x_c`, `x_q`), of `w_cb` (`x_c`, `x_b`) or of `f_bc`
(`m_b`, `x_c`), so a pin serves at most two E-members. Dually for the F-members on the valley side.
(iv) (A3) at the peak `x_c` concerns the valley-capable `m_c >= x_c`: it needs `m_c ∈ U+` (a generator `<= m_c`, i.e.
`x_c` or `m_c`) or `m_c ∈ M+` (an upper neighbour of `m_c` in `P+`: tops of `f_cb`, adjacent below to `m_c` and `x_b`
only), so each `c` needs its own pin; the pinned modes need every E-member (resp. F-member) as a generator. ∎

**Reading.** In `Y_k` every mate is irrelevant (its F-side is never usable), yet every walk-based certificate must
"watch" the F-side of each mate while the walk passes the E-members, because the only sides that see several mate
F-sides are the flip sides `Fl_b`, whose neighbourhoods contain all F-members of the path. This is the general-model
analogue of the storage problem of r4-switch's critical runs, but here the partners of the members play no role: the
conflict families contain sides of *other* switches, about which P2 says nothing (they are comparable with the
member). The certificate approach therefore needs a relevance test, or a different kind of algorithm (§7).

*Checked* (`test_yfam.py`, `test_yfam_bound.py`, `runs_yfam_bound*.txt`): `k = 2..5`: P2, exactly one solution (brute
force over the `3k` switches), exact answer; NG with two pins fails from `k = 5` on. The side-set search accepts
`Y_6` with `(1, 0, 2, 6)` but not with `(1, 0, 2, 5)`, `Y_7` with `(1, 0, 4, 7)` but not `(1, 0, 4, 6)`, `Y_8` with
`(1, 0, 4, 8)` but not with `(1, 0, 4, 7)` nor with `(2, 1, 4, 7)` (all 1,096,704 pairs `K_E`, `K_F` tried): the
accepting certificate is `K_E = N_F[Fl_1]` (all mate F-sides but one, plus all `k` F-members, stored), one declaration
at `h_1` for `F(m_1)`, as in the proof.

### 6.2 Forbidding the certificate and pruning by reachability; the family `Y'_k`

A natural refinement uses the certificate also as a *forbidden set*: the sides of `K` that are not members of the
path are never used, so they can be deleted. **Refined search** (`gsw.search_refined`): guess `K` (as above) and a
set `S ⊆ K` of at most `B` sides (the members that lie in `K`); delete `K - S`; let `R` be the set of sides reachable
from the sides containing `s` in the side graph of the remaining sides; run the search of Theorem 5' inside `R`, with
conflict families restricted to `R` and `K' = S`. *Sound* for every choice (Theorem 5' for the instance restricted
to `R`: every conflict between two sides of the walk is a conflict inside `R`). On `Y_k` it succeeds with one
dominator `N_F[h_q]` (`q` any F-member; it contains every `Fl_b` through `z_bq`), `S = {h_{q-1}, h_q, h_{q+1}}`: all
`Fl_b` are deleted, every mate side becomes unreachable, and no conflict family needs watching.
**`Y'_k`** (`yfam(k, contact=True)`): `Y_k` plus a private node of `F(m_c)` in the path side `h_{k+c}` of the `c`-th
F-member. P2 and uniqueness are kept (the new node lies in two sides that are never picked together with a path side
of an unflipped prefix; the first-flip argument of Theorem Y(i) is unchanged). Now `F(m_c)` is reachable from
`h_{k+c}`. **Proposition Y' (proved; checked `k = 3, 4, 5`).** The refined search rejects `Y'_k` whenever
`kd + ks + s + B < k`. *Proof.* As in Theorem Y(ii): the walk is `h_1 .. h_{2k}`, all path sides must be in
`S` or outside `K`; for each `c`, `F(m_c)` is reachable unless deleted, so `F(m_c) ∈ S`, or `h_c` declares, or
`F(m_c) ∈ K`; a set `N_F[Z]` containing `F(m_c)` has `Z ∈ {F(m_c), h_{k+c}} ∪ {Fl_b : b != c}`; `N_F[Fl_b]` contains
all F-members, which must then lie in `S` (`|S| >= k`); each of the other choices serves one `c`. ∎ NG and GC fail on
`Y'_k` for the reasons of Theorem Y(iii), (iv) (the new tops are adjacent below to one mate and one F-member).
Checked (`test_refined.py 3 5 1 0 1 3`, `runs_refined_1013.txt`): with `(kd, ks, s, B) = (1, 0, 1, 3)` the refined
search accepts `Y_3, Y_4, Y_5` and `Y'_3`, rejects `Y'_4`, `Y'_5`; the plain search rejects `Y_4, Y_5, Y'_4, Y'_5`.

## 7. What the obstructions say, and a candidate algorithm

1. **Where the general model differs from 2CH (proved by the families above).** In 2CH + P2 the only conflict of a
   member is its own partner, and P2 forces the partners of far members of one type to meet (r4-switch, (F2)); this
   is what makes a bounded number of neighbourhoods suffice. In the general model the conflict family of a member
   `E_w` contains the F-sides of every `w' >= w`; P2 relates `w'` to the switches it is *incomparable* with, never to
   `w` itself, so it puts the sides of `w'` next to the partners of *other* members and nowhere near the member
   whose conflict they are. `Y_k` uses exactly this: each mate is comparable with one switch only and its F-side is
   seen only by the partners of the other E-members. Each refinement of the certificate that we tried (pins of GC,
   neighbourhood generators of NG, side sets with conflict families, forbidding plus reachability) is defeated by a
   one-line change of the mates (`X_L`, `Y_k`, `Y'_k`); all these mates are *irrelevant* (their usable side is never
   used by a solution, `Y_k`, `Y'_k`; or they lie off every solution below a valley, `X_L`).
2. **No reduction by gadgets** (Lemma Mon): a relation `y < x` whose removal creates solutions cannot be removed by
   adding structure; and middle witnesses cannot be made unconditional (MW2). We found no global reduction to
   2CH + P2 either.
3. **Candidate algorithm HYB: pruning by forced exits, then side-set certificates** (`gsw.prune`,
   `gsw.pruned_copy`, `test_pruned.py`). *Forced-exit propagation* (sound refutation of a partial mode assignment):
   close the assignment under the order; grow the component `C` of `s` by the sides already fixed; if no side of an
   unfixed switch meets `C` and leaves it, refute; if exactly one such side exists, fix its switch to that mode and
   repeat; the same from `t`. *Pruning:* for every switch and mode, if the assignment "this switch in this mode" is
   refuted, fix the other mode; iterate. Every fixed mode is a mode of every solution, so the removed sides are used
   by no solution. *HYB(kd, ks, s, B):* prune, delete the sides of the wrong modes, run the search of Theorem 5'.
   **Proposition HYB (proved).** For all parameters HYB never accepts a no-instance (validity is checked on the
   walk's own sides, so even a wrong pruning could only cost completeness), and pruning never removes a side used
   by a solution. HYB with fixed parameters runs in polynomial time.
   *Checked* (`test_pruned.py families 1 0 1 3`, `runs_pruned_fam.txt`; `test_pruned.py random 1 900 1 0 1 3`): with
   `(kd, ks, s, B) = (1, 0, 1, 3)` HYB solves all 196 yes-instances of the families (`X_L` up to `L = 10`, `Y_k` and
   `Y'_k` up to `k = 8`, `T_L`, `R_L` with mates, `R_L` 2CH form, ladders, all 133 `r4-search` instances), rejects the
   six hub instances, and agrees with the exact answer on 900 random instances; the pruning never removed a side used
   by a solution (brute force, instances with at most 14 switches).
   **Caveat (checked): the known hard families are rigid.** In 176 of the 196 yes-instances the pruning alone fixes
   every switch (it reproduces the first-flip induction of `R_L`), so on them HYB is decided by propagation; only
   `T_L` (one free switch `Z`) and eight shrunk instances of `r4-search` keep free switches. Rigidity is what makes
   the lower-bound proofs for certificates easy (one solution), and it is also what makes them easy for propagation.
   A family that defeats HYB needs *choices* (no forced modes) together with comparabilities whose conflicting side
   is used by some solution, on every solution path.
4. **Choices are hard to build under P2 (sketch, with a computed example).** The family `Z_k` (`zfam.py`): two
   disjoint copies of `R(E^k F^k)` between the same terminals, cross P2 by private nodes, mates on both copies.
   Propagation fixes nothing (each copy can be broken while the other is used; `Z_2`: 87 solutions, `Z_3`: 4009), but
   P2 between an E-member of one copy and an F-member of the other must put a path side of one into a flip side of the
   other; with `k^2` such pairs some flip side meets `>= k/2` path sides of the other copy, and when its switch is
   flipped (allowed while the other copy is used) it is a hub that shortcuts that copy. The shortest solutions of
   `Z_k` use such hubs and pass only two or three mated E-members, and HYB with `(1, 0, 1, 3)` solves `Z_2 .. Z_5`
   (`test_zfam.py`; NG with two pins solves them too). This is the same counting obstruction that makes 3-SAT
   encodings with choices in series fail under P2 (`theory-hardness.md` §6.2, `dc-hardness.md` §3).
   In the general model order relations *can* switch such hubs off (a hub side of type E is excluded when its switch
   lies below a valley that every solution of the other copy contains; this is N2 of `r4-brief.md` used
   constructively). The variant `Z^B_k` (`zfam(k, block=True)`: every F-member of one copy below the last F-member of
   the other) has no hubs (`Z^B_2`: 17 solutions, `Z^B_3`: 53), propagation fixes only the F-members, and still HYB
   with `(1, 0, 1, 3)` and NG with two pins solve `Z^B_2 .. Z^B_4`, with or without the contact nodes: the mates'
   P2 obligations towards the other copy must be met either by their F-sides inside the other copy's flip sides,
   whose neighbourhood then dominates all mates without touching the walk (a free dominator), or by their E-sides
   inside the other copy's path sides, a new hub. Choices plus irrelevant comparabilities keep producing either
   shortcuts or free dominators.
5. **Status of the open case.** With 2CH + P2 in P (r4-switch, Theorem 10), every NP-hardness proof must use ties,
   one-way comparabilities, middle edges or middle witnesses; our families show that exactly these features defeat the
   certificate method, so the question of the open case of DC is now the question whether irrelevant comparabilities
   can be removed (or ignored) in polynomial time.

## 8. Theorem R: a reduction to the switch model after propagation

Setting: the general switch form of §5.1 (nodes, switches = middle elements with a preorder, sides `E_w`, `F_w`,
private nodes for middle edges). A *sound fixing* is a set of pairs (switch, mode) that every solution satisfies,
closed under the order (`w` fixed F and `w' <= w` imply `w'` fixed F; `w` fixed E and `w' >= w` imply `w'` fixed E);
the pruning of §7.3 produces one. *Free* switches are the others. The *contraction* identifies all nodes of each
side picked by a fixed switch (`F_w` if `w` is fixed F, `E_w` otherwise), keeps the free switches with their sides
mapped to the contracted nodes, and drops the fixed switches.

**Theorem R (proved).** Let `I` be a ZZ + P2 instance with a sound fixing in which the free switches are pairwise
incomparable (no ties and no strict relations among them). Then:
(a) `I` is a yes-instance iff the contraction `I*` (a 2CH instance) is;
(b) `I*` satisfies P2, unless some pair of free switches has only free middle witnesses (in which case P2 may fail;
the reduction then needs the general model);
(c) if `I*` satisfies P2, `I` is decided in polynomial time by Theorem 10 of `r4-switch.md`.
*Proof.* (a) Every solution satisfies the fixing, so the solutions of `I` are the order-consistent mode vectors that
extend the fixing and connect `s`, `t`. A free switch `x` and a fixed switch `y` impose no constraint on `x`: if
`x < y` and `y` is fixed F, closure would have fixed `x` (F); if `x < y` and `y` is fixed E, the relation only forbids
`y ∈ D ∌ x`, which cannot happen; the case `x > y` is dual. Free switches are pairwise incomparable. So every mode
vector of the free switches extends the fixing to an order-consistent vector, and the picked hypergraph is the union
of the fixed picked sides and the free picked sides. Contracting each fixed picked side (always present) to a node
keeps `s`-`t` connectivity for every vector of the free switches.
(b) Let `x, y` be free and incomparable. A common node (in `E_x ∩ E_y` or `F_x ∩ F_y`) stays common. A lower middle
witness `w < x, y` has `F_w` meeting `E_x` and `E_y` (through the private nodes of the edges `w x`, `w y`); `w` is not
fixed E (that would fix `x`, `y` in E-mode by closure), so if `w` is fixed it is fixed F, `F_w` is contracted to one
node, and `E_x ∩ E_y ≠ ∅` in `I*`. Dually for an upper middle witness (fixed E). So P2 can fail in `I*` only if all
witnesses of the pair are free middle elements.
(c) Theorem 10 of r4-switch decides 2CH + P2 in polynomial time; the contraction and the fixing are polynomial. ∎

**Corollary R'.** On every instance whose propagation (§7.3) leaves the free middle elements pairwise incomparable and
every pair of free elements with a common node or a fixed witness, ZZ + P2 is solved in polynomial time by
propagation + contraction + Theorem 10; the hypothesis is checked in polynomial time. This covers every instance with
one-way relations or ties that propagation removes: in particular `T_L^tie`, `T_L^one`, `X_L`, `Y_k`, `Y'_k`, the
ladders, the rigid families with mates, and all 133 portfolio-hard instances of `r4-search`. What it does not cover
is exactly the case where propagation leaves comparable free elements (or free middle witnesses): ties and one-way
relations *between switches that still have a choice*.

*Checked* (`test_reduce.py`, `runs_reduce_fam.txt`): on 192 family instances the hypothesis holds for 188 (all but the
two-route instances `Z_2`, `Z_3`, where the mates stay free and comparable, and the hub no-instances `H(2,2)`); on all
188 the contracted instance satisfies P2 and its answer, by r4-switch's `alg.decide(1, 1, 4, 8)` and by brute force
over its mode vectors (r4-switch `sw.brute`, read-only), equals the exact answer of the ZZ instance (0 mismatches).
Random instances (`test_reduce.py random 1 1500`, `random 2 1500`): the hypothesis holds for 1234 and 1232 of 1500
each; 0 mismatches.

*Checked, the core* (`test_core.py SEED 3000 10 16`, seeds 2, 3, 4, `runs/core-*.log`): random general instances with
10-16 middle elements and dense orders (ties, one-way relations, mixed witnesses); of the 7271 yes-instances, 6719
are in the core (Theorem R does not apply after propagation); HYB solves all of them, 6713 with `(1, 0, 1, 3)` and 6
with `(1, 1, 2, 6)`. Adversarial hill climbing aimed at HYB (`hunt_hybrid.py`, 4 random starts and 4 starts from
`r4-search` instances, 30,000-40,000 steps each, `runs/hunt-hybrid-*.log`) drifts to short solutions; the largest
parameter set ever needed was `(1, 0, 1, 3)`.

### 8.1 Theorem R+: branching on the free comparabilities (proved; checked)

**Theorem R+.** Let a sound fixing be given, let `H` be the comparability graph of the free switches (an edge for every
pair `x < y`, `y < x` or `x ~ y` of free switches), and let `C` be a vertex cover of `H`. Then the instance is decided by
at most `2^{|C|}` reductions of Theorem R, i.e. in `2^{|C|} · poly` time with r4-switch's Theorem 10. With a greedy
cover (twice a maximal matching) or an exact one (FPT in its size), ZZ + P2 is **FPT in the vertex cover number of the
comparability graph of the switches left free by propagation**.
*Proof.* Branch over the modes of `C`, close each guess under the order, drop the contradictory guesses. The
solutions of the instance are the union over the branches of the solutions extending the branch fixing. In a branch
the free switches form an independent set of `H` (every edge of `H` has an end in `C`, now fixed), so they are pairwise
incomparable, and part (a) of the proof of Theorem R applies verbatim to the solutions extending the branch fixing (it
used only closure, not soundness). For P2 in the contraction: a free middle witness `w` of a free pair `x, y` is
comparable with `x` (and `y`), so `wx` is an edge of `H` and `w ∈ C` (as `x ∉ C`); hence `w` is fixed in the branch,
and fixed in the right mode (a lower witness fixed E would fix `x` by closure), so its picked side is contracted and
`x`, `y` share a node; node witnesses stay. So every branch is a 2CH + P2 instance. ∎
Theorem R is the case `C = ∅`. The bound is in the number of free switches *involved in comparabilities*, not in
their number of comparabilities, so it covers instances with large width (Theorem C needs bounded width).
*Checked* (`test_rplus.py 1 2000 6 12`, `test_rplus_fam.py`): 2000 random instances (greedy covers of size 0-12): the
OR over the branches, each solved by brute force over its 2CH mode vectors and by r4-switch's `alg.decide(1, 1, 4, 8)`,
equals the exact answer on all 2000; no branch ever violated P2. On the instances outside Theorem R: `H(2,2)` (both
versions, cover 8, 81 branches, all no), `Z_2`, `Z^B_2` (cover 8), `Z_3`, `Z^B_3` (cover 12, 729 branches): all
answers right.

## 9. What remains open

1. **The core of the general case.** Yes-instances on which propagation leaves strictly comparable free switches
   (one-way relations between switches that still have a choice) or free middle witnesses. Theorem R reduces
   everything else to 2CH + P2, Theorem R+ everything with a small free comparability cover; §10 treats one-way
   relations and middle witnesses in more detail. With only ties among the free switches the contraction of Theorem R is an instance of
   *2CH with classes + P2* (same proof: the classes stay classes, P2 is needed only between different classes), so
   general ZZ + P2 reduces to 2CH with classes + P2 whenever propagation kills the strict relations between free
   switches (proved; not run separately); the complexity of 2CH with classes + P2 is open.
   The hypothesis cannot simply be dropped: in the hub `H(2,2)` (classes version) propagation fixes no switch, the free
   switches are comparable (`ε_i < ρ^A_ij`), and deleting these relations creates solutions (every gadget becomes
   passable), so comparabilities between free switches carry real constraints, at least in no-instances. In random
   instances (`test_relax_free.py 1 3000 6 12`: 3000 instances) every no-instance is refuted or left without free
   comparabilities by propagation, and all 1714 instances with free comparabilities are yes-instances.
2. **HYB.** Conjecture (evidence: §7.3, §8, the core runs): HYB with bounded parameters decides ZZ + P2. A proof
   would need a version of r4-switch's Theorem 8 for conflict families on instances after propagation; the families
   `X_L`, `Y_k`, `Y'_k` show that propagation is indispensable, and `Z_k`, `Z^B_k` show why choices with irrelevant
   comparabilities are hard to build. A counterexample needs a non-rigid instance whose every solution path carries
   many comparabilities with sides used by other solutions and not dominated by a neighbourhood off the path.
3. **NP-hardness.** By Theorem R a hardness proof must keep strictly comparable switches free after propagation
   (or keep free middle witnesses). The constructive use of order relations to switch hubs off (`Z^B_k`) is the one
   mechanism that P2 alone does not have; whether it can carry a 3-SAT encoding is the question for a hardness proof
   (r4-hard).
4. **Exponents.** NG with `t` pins costs `q^{6t+s}`; Theorem R inherits the exponent of r4-switch's Theorem 10
   (about 120 as proved). On every instance tested the small parameters `(1, 0, 1, 3)` sufficed.

## 10. One-way relations and middle witnesses between free switches (round 4b, 2026-10-22)

Division of work set by the coordinator: ties (2CH with classes) go to r4-switch, the adversarial search against
HYB and Theorem R to r4-search; this section treats strict (one-way) relations between free switches and free middle
witnesses. Setting: the general switch form after a sound fixing and contraction (§8), the free switches carry a
*partial* order (no ties), P2 holds for incomparable free switches by a common node or by a free middle witness.

### 10.1 Free middle witnesses are free comparabilities (proved)

A free middle witness `w` of a free pair `x, y` satisfies `w < x, y` (or `w > x, y`), so it is an edge of the free
comparability graph `H` of §8.1; branching on a vertex cover fixes it (Theorem R+), and a fixed middle witness is
contracted into a common node (Theorem R(b)). So middle witnesses add nothing beyond one-way relations: the open case
is "free one-way relations with unbounded vertex cover". MW2 (§3.3) shows that a middle witness cannot be replaced by
a node witness *before* its mode is known; after branching it can.

### 10.2 What survives of r4-switch's structure theory (proved)

Let `P = X_1 .. X_r` be a shortest valid walk of sides (no conflict pair `E_w`, `F_{w'}` with `w <= w'`), `w_a` the
switch of `X_a`. *E-members* and *F-members* as in r4-switch. A side `Y` not on `P` is *insertable* if no side of `P`
lies in its conflict family `Π(Y)`.

**Lemma 10.A (insertable sides have local contacts).** An insertable side meets members of `P` only at three
consecutive positions at most.
*Proof.* If `Y` meets `X_d` and `X_c`, `c >= d + 3`, then `X_1 .. X_d Y X_c .. X_r` has no conflict pair (a subsequence
of `P` plus a side conflicting with none of `P`) and is shorter than `P`. ∎

**Lemma 10.B (where insertable sides come from).** If `a` is an E-member and `w' >= w_a`, then `E_{w'}` is a member of
`P` or insertable. Dually for F-members and `w' <= w_b`.
*Proof.* `Π(E_{w'})` consists of F-sides of switches `w'' >= w' >= w_a`; such a side on `P` would conflict with `X_a`. ∎

**Lemma 10.C (conflict sides meet partners).** Let `a`, `b` be E-members, `Z = F_{w'} ∈ Π(X_a)`, `w' ∥ w_b`, and let
`b` not be a contact of `Z' = E_{w'}`. Then `Z` meets the partner `X'_b`.
(Assumed: the pair `w'`, `w_b` has a node witness; a middle witness of it is a free comparability, §10.1.)
*Proof.* P2 for `w'`, `w_b` by a node: `E_{w'} ∩ E_{w_b} = Z' ∩ X_b` is empty by assumption, so
`F_{w'} ∩ F_{w_b} = Z ∩ X'_b` is not. ∎

**Proposition 10.D (two partner neighbourhoods cover all conflict sides but those of upper bounds).** Let `b_1`, `b_2`
be E-members at distance `>= 4` whose switches are minimal among the switches of E-members. Every side
`F_{w'} ∈ ∪_a Π(X_a)` (`a` over the E-members) lies in `N_F[X'_{b_1}] ∪ N_F[X'_{b_2}]` unless `w' >= w_{b_1}` or
`w' >= w_{b_2}`. With `m` pairwise far minimal E-members, the exceptions are the F-sides of switches above at least
`m - 1` of them.
*Proof.* `w' >= w_a` for some E-member `a`. If `w' <= w_{b_i}` then `w_a <= w_{b_i}`, so `w_a = w_{b_i}` by
minimality, and `w' = w_{b_i}`: `F_{w'} = X'_{b_i}`. Otherwise `w'` is incomparable with `w_{b_i}` unless `w' >= w_{b_i}`;
by Lemmas 10.A, 10.B the contacts of `E_{w'}` lie in three consecutive positions, which miss `b_1` or `b_2`, and Lemma
10.C applies to that one. ∎
*Reading.* In 2CH + P2 the conflict family is the partner, and r4-switch covers the partners by member
neighbourhoods `N_O[X_q]` exactly when the partner neighbourhoods are expensive (critical runs, Theorem 8). The extra
conflict sides of the general model escape member neighbourhoods (their partners need not meet `X_q`: the cross
condition can be met by `E_{w'} ∩ X'_q`), and Proposition 10.D covers them by partner neighbourhoods `N_F[X'_b]`, whose
storage `|P ∩ N_F[X'_b]|` is the number of F-members meeting `X'_b`. `Y_k` (§6) is precisely a critical run in which
every partner meets every F-member, with one extra conflict side per E-member: Proposition 10.D is sharp, and the
extension of Theorem 8 fails unless the extra conflict sides are removed first (pruning) or another solution path has
cheap partner neighbourhoods.

### 10.3 Pruning by the switch model (proved)

**HYB-2CH.** Replace the forced-exit refutation of §7.3 by: to refute "switch `w` in mode `μ`", fix it, close under the
order, contract (§8), *drop* all order relations between the free switches, add for every pair of free switches that
violates P2 a private node to both F-sides, and decide the resulting 2CH + P2 instance by Theorem 10 of r4-switch;
refute if it is a no-instance. **Sound:** dropping relations and adding nodes only adds solutions, so a no-answer of
the relaxation proves that no solution has `w` in mode `μ`. **Polynomial:** `O(n)` refutation tests per round, at most
`n` rounds, each a call of Theorem 10. HYB-2CH refutes every mode whose impossibility does not depend on the free
order relations; in particular it fixes every mate of `X_L`, `Y_k`, `Y'_k` and of the bypass and decoy variants of
§10.4 whose bypasses are blocked by fixed elements. (Not implemented: Theorem 10 is not practical; forced exits already
fix the known families.)

### 10.4 Why every hard instance we tried to build collapses (sketch, with the decisive lemma proved elsewhere)

To defeat HYB (or HYB-2CH) one needs a yes-instance in which (i) the extra conflict sides are *usable* by some
solution (else pruning removes them), (ii) every solution path carries many of them, (iii) they are covered only by
expensive neighbourhoods (Proposition 10.D's exceptions or large `|f(b)|`), and (iv) each needs its own declaration.
Every gadget that provides (i), i.e. a second way to pass a position so that a switch can change mode, is a new
switch with P2 obligations towards all other switches. The *hub lemma* of `r4-hard.md` (L4, proved there: in every
`n × n` block of incomparable pairs some element shares witnesses of one direction with `⌈n/2⌉` elements of the other
side) then produces, in the attempts made here, one of three things:
- a hub side that shortcuts the solution path (two-route family `Z_k`, §7.4; bypasses whose F-sides meet the F-part;
  decoys whose second side meets later path sides), so the shortest solution carries few extra conflict sides;
- a *free dominator*: a side off the path that meets all extra conflict sides and no path member (the other route's
  flip sides in `Z^B_k`; F-member flip sides for bypass E-sides), so the certificate is cheap;
- or an unguarded connector that reaches a flipped flip side from the solution prefix (decoys with `D_j ∩ Fl_i`,
  `i > j`), which creates new short solutions.
Order relations can switch hubs off (the extra power of the general model, N2 of `r4-brief.md`), but every blocking
relation we added either forbids the very mode change that (i) needs, or creates a cycle (a tie), or is detected by
propagation (a blocker that is forced by forced exits fixes the blocked switch by closure). So no instance with free
one-way relations on which HYB fails is known, and the families that defeat certificates without propagation
(`X_L`, `Y_k`, `Y'_k`) are all rigid.

*The exchange pattern (sketch).* The most elaborate attempt (critical run `E^k F^k` with z-contacts, a mate above
every E-member, a bypass for every E-member blocked by a private F-member in a tail beyond the run, and bypasses for
the tail blockers so that propagation from `t` stalls) shows the mechanism that defeats every design. A dominator for
the mates' F-sides is a flip side `Fl_b` of an E-member; it is expensive for a walk `W` only if it meets many members
of `W`, i.e. only if its contacts lie on `W`. The mates are usable only through solutions `W'` in which some E-member
`x_c` is flipped; there `Fl_c` is picked, and either its contacts lie on `W'` (then `Fl_c` is a hub, the shortest walk of
`W'` uses it, and `N_F[Fl_c]` has storage at most 3) or they do not (then `N_F[Fl_b]` costs nothing on `W'`). Either way
`W'` has a cheap certificate, and HYB accepts through `W'`.
**Conjecture X (exchange).** If a shortest valid walk `P` has extra conflict sides that are used by some solution and
not covered by a bounded certificate, then some solution has a valid walk with a certificate of bounded size (bounded
number of neighbourhoods, single sides, declarations and storage). Conjecture X with r4-switch's Theorem 8 would make
HYB (with forced exits replaced by any sound pruning that removes the unusable sides) complete; it is supported by all
computations and by every failed construction, and it is the general-model analogue of r4-switch's swap Lemma 7.

### 10.5 Status of this part

- **Proved:** free middle witnesses reduce to free comparabilities (10.1); Theorem R+ (FPT in the vertex cover of the
  free comparabilities, §8.1); Lemmas 10.A-10.C and Proposition 10.D (the general-model replacements of r4-switch's
  (F4), Lemma 1 and (F2)); soundness and polynomiality of HYB-2CH (10.3).
- **Not proved:** completeness of HYB or HYB-2CH with bounded parameters when the free one-way relations have
  unbounded vertex cover. The missing piece is an exchange argument in the spirit of r4-switch's Lemma 7: if the
  extra conflict sides of a shortest path are usable and expensive, some other solution path should have a cheap
  certificate. The hub lemma is the natural tool; the failed constructions of 10.4 are evidence for such a statement.
- **No instance on which every method fails** was found: every known instance is solved by HYB with
  `(1, 0, 1, 3)` (§7.3, §8, core runs), and Theorem R+ decides all instances with small free comparability covers.

## 11. Scripts (`r4-general/`)

| Script | What |
|---|---|
| `common_r4.py` | imports (read-only), conversions, dual instance, solution check |
| `ng.py`; `test_ng_families.py`, `test_ng_random.py`, `test_ng_rigid.py` | Theorem NG search; checks (§2.4); logs `runs_fam_2_0.txt`, `runs_rigid_2.txt` |
| `test_reductions.py` | Lemma Sub, examples MW, MW2 (§3); `runs_reductions_1.txt` |
| `xfam.py`, `test_xfam.py` | family `X_L` (§4); `runs_xfam_*.txt` |
| `gsw.py` | general switch form, conflict families, search of Theorem 5', refined search, pruning (forced exits), Theorem R contraction |
| `test_gsw.py`, `min_cert.py` | checks of the extended side-set search (§5.1); `runs_gsw_fam_*.txt` |
| `yfam.py`, `test_yfam.py`, `test_yfam_bound.py`, `show_cert.py` | families `R(W)`, `Y_k`, `Y'_k` (§6); `runs_yfam_bound*.txt` |
| `test_refined.py` | refined search on `Y_k`, `Y'_k` (§6.2); `runs_refined_1013.txt` |
| `test_pruned.py` | HYB on families and random instances (§7.3); `runs_pruned_fam.txt` |
| `zfam.py`, `test_zfam.py`, `show_cert_z.py` | two-route families `Z_k`, `Z^B_k` (§7.4) |
| `test_reduce.py` | Theorem R against r4-switch's algorithm and brute force (§8); `runs_reduce_fam.txt` |
| `test_core.py`, `hunt_hybrid.py` | the core instances; adversarial search against HYB (`runs/`) |
| `test_rplus.py`, `test_rplus_fam.py`, `check_tl_pin.py`, `test_relax_free.py` | Theorem R+ (§8.1); single pin for `T_L` (§2.4); dropping free comparabilities (§9) |
