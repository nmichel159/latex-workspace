# Round 5, agent r5-core: the general core of ZZ + P2 (target B)

Status: version 0.3 in progress (third run, 2026-10-22; version 0.1 of 2026-10-19 = §0-§2, version 0.2 of
2026-10-21 = §3). Sections §4 onward are added as results come; the run logs of version 0.1 were lost with the first
run (the checks of §2 are re-run in §9).
Plan of version 0.3: (a) record the family `W_n` of the second run (§4.1); (b) stress families with mates on both
sides ("global" and "half-global" down- and up-mates) against CDESC, HYB and anchor fixings (§4.2); (c) anchors:
fixing the down-closure of guessed F-members and the up-closure of guessed E-members, with partner centres for the
rest (§5); (d) a completeness proof for a description-plus-antichain algorithm, or a family that defeats it (§6).
Scripts: `r5-core/`, logs: `r5-core/runs/`. Labels: **proved**, **checked**, **sketch**, **conjecture**, **refuted**.
Notation of `r5-brief.md`, `r4-general.md` (general switch form: switches with a preorder, sides `E_w`, `F_w`, modes
a down-set `D` = F-mode, conflict pairs `{E_w, F_z}` with `w <= z`, conflict family `Π(X)`), `r4-switch.md` (F1-F4,
Lemma 1, Theorem 4, Theorem 8, Theorem 10).

## 0. Results so far

| # | Statement | Status |
|---|---|---|
| D | **HYB is incomplete.** The family `Y^d_k` (r4-general's `Y_k` plus one switch `d`) and `Y'^d_k` (`Y'_k` plus `d`): P2, yes-instances with exactly two solutions; forced-exit propagation fixes at most one switch; every run of HYB (plain or refined search after the pruning) with `kd + ks + s < k` and `B < k` rejects. So HYB with any fixed parameters is not a decision procedure for ZZ + P2, and the conjecture of `r4-general.md` §9.2 is refuted | proved (§2); checked `k <= 6` |
| CF | **The obstruction families are cheap for descriptions.** CDESC (closure-based mode descriptions: centres give a set `U` of switches, generators `G = Enon − U` up to `e` flips, `D = Q − ↑G`, or dually) is sound for all parameters; `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k`, `X_L` are solved with one centre and at most one flip (explicit descriptions), `Z_k`, `Z^B_k` likewise | proved (§3.3); checked `k <= 4`, `L <= 8` |
| G | Lemma G: guided cost of a description for a given valid path (flips = uncovered E-sides below F-members + uncovered minimal E-members); up-mates of E-members cost nothing on the E-side | proved (§3.2) |
| W, OB | Families with floating mates on both sides (`W_n`, cyclic contacts; `OB`, critical run with private mate contacts): either the planted path stops being shortest (hubs, non-tight straddles) or a cheap centre appears; all solved by HYB, CDESC, ADESC | checked (§4) |
| 5.2 | **TCA ⇒ ADESC.** Anchored descriptions (anchors fix `↓b` or `↑a`, centres cover the rest) are sound; if some shortest valid path has its maximal F-members in an interval of length 4, or two maximal F-members at distance `>= 5` whose partners meet at most `c` minimal E-members (or the dual), ADESC with 5 anchors, 2 centres and `c` flips succeeds, **whatever the mates are** (node and middle witnesses) | proved (§5.2) |
| 5.2' | Strict anchors: `D = ↓B_0 ∪ ⋃ (↓a − [a])` (`a` minimal E-members) picks a path whose maximal F-members it covers | proved (§5.2) |

## 1. Library and exact routines (`r5-core/gcore.py`)

Own implementation of the general switch form from the definitions of `r4-general.md` §5.1 (conversion from a ZZ
instance through `gsw.GSW` of r4-general, read-only, with the private nodes of middle edges recorded; conversion back
to a ZZ instance, `to_inst`). Exact routines: `brute` (enumeration of the down-sets of the switch preorder,
connectivity of the picked hypergraph), `shortest` (BFS over states (side, `Up`, `Dn`), `Up` the up-closure of the
E-members, `Dn` the down-closure of the F-members; a side `E_w` may follow iff `w ∉ Dn`, a side `F_w` iff `w ∉ Up`),
`all_shortest` (DFS with the side-graph distance to `t` as bound).
*Checked* (`test_gcore.py 1 300 4 10`, `2 600 10 16`): on 900 random P2 instances (generators of `r4-general/test_core.py`)
`brute` = `gcert.exact` (dc-general) = existence of a shortest valid path, and the round trip switch form -> ZZ -> exact
answer is unchanged (one bug of the round trip for `s = t` found and repaired: `u`, `v` in one node are realised by a
fresh bottom-top pair).

## 2. HYB is incomplete: the families `Y^d_k`, `Y'^d_k`

### 2.1 Construction (`r5-core/fool.py`)

Start from `Y_k` (or `Y'_k`) of `r4-general.md` §6 in switch form (`r4-general/yfam.py`, read-only): base switches
`x_1..x_2k` (path side `h_j`: `E(x_j)` for `j <= k`, `F(x_j)` for `j > k`; flip side `Fl_j` the other one), nodes `s`,
`t`, `y_j ∈ h_j ∩ h_{j+1}`, `z_pq ∈ Fl_p ∩ h_q` (`p <= k < q`), `w_pq ∈ Fl_p ∩ Fl_q` (equal modes), mates `m_c > x_c`
(`c <= k`) with `F(m_c) = {f_cb : b <= k, b != c}`, `f_cb ∈ Fl_b`, `E(m_c) = {e_cq : q > k} ∪ {g_cc'}`, `e_cq ∈ Fl_q`;
in `Y'_k` also a private node `fc_c ∈ F(m_c) ∩ h_{k+c}`. Add one switch `d`, incomparable with every switch:

    E(d) = {s} ∪ {γ_c : c <= k} ∪ {δ_q : k < q <= 2k},   γ_c added to E(m_c),  δ_q added to Fl_q = E(x_q);
    F(d) = {ε_b : b <= k},                              ε_b added to Fl_b = F(x_b);
    variant back: F(d) also contains t and a node κ added to E(m_1).

The ZZ form is `gcore.to_inst` (every node a bottom-top pair with a fixed edge).

### 2.2 Proposition D (proved)

For every `k >= 2`, both variants (back or not) of `Y^d_k` and of `Y'^d_k`:
(i) satisfy P2;
(ii) have exactly two solutions: `x_j` in its path mode (E for `j <= k`, F for `j > k`), every mate in E-mode, `d`
in either mode;
(iii) the forced-exit pruning of HYB (`gsw.prune`, `r4-general.md` §7.3) fixes exactly `x_2k` (variant without back)
or no switch (variant back);
(iv) for every `K_E` (union of `kd` sets `N_F[Z]` and `ks` single F-sides), every `K_F`, every `s`, `B` with
`kd + ks + s < k` and `B < k`, the search of Theorem 5' on the pruned instance rejects; for `Y'^d_k` the same holds
for the refined search of `r4-general.md` §6.2 (forbid `K - S`, restrict to the sides reachable from `s`).
Hence HYB (plain or refined) with any fixed parameters `(kd, ks, s, B)` answers "no" on the yes-instance `Y'^d_k` for
`k > max(kd + ks + s, B)`.

*Proof.* (i) The pairs of `Y_k` (`Y'_k`) keep their witnesses (r4-general Theorem Y(i), Proposition Y'). `d` is
incomparable with every switch; `ε_b ∈ F(d) ∩ F(x_b)` for the E-members, `δ_q ∈ E(d) ∩ E(x_q)` for the F-members,
`γ_c ∈ E(d) ∩ E(m_c)` for the mates. In the ZZ form a common node is a common bottom or top neighbour.

(ii) Let `D` be a solution and `r` the least index with `x_r` not in its path mode (`r = 2k + 1` if none). The sides
containing nodes of `h_1, .., h_{r-1}` (nodes `s`, `y_j`, `z_pi` with `p < i < r`, `fc_c` with `k + c < r`) are
`h_1 .. h_r`, `Fl_p` with `p < r`, `E(d)` (only through `s`) and `F(m_c)` (only through `fc_c`). `h_r` is not
picked; `Fl_p` (`p < r`) is not picked because `x_p` is in its path mode; `F(m_c)` with `k + c < r` is not picked
because `m_c ∈ D` would force `x_c ∈ D` with `c < r`. If `d ∈ D`, the component of `s` is
`h_1 ∪ .. ∪ h_{r-1}`; if `d ∉ D` it is that union together with the *blob*: `E(d)`, the picked `E(m_c)` and the picked
`Fl_q` (`q > k`), whose nodes `γ, δ, e, g, w_qq', κ` lie in no other side except `F(d)` (`κ`, not picked as `d ∉ D`).
Neither union contains `t` (`t ∈ h_2k`, `F(d)`) unless `r = 2k + 1`. So every base switch is in its path mode; then
`x_c ∉ D` and `x_c <= m_c` give `m_c ∉ D`. Conversely both choices of `d` connect `s` to `t` along `h_1 .. h_2k`.

(iii) `gsw.refutes` grows the component of `s` (and separately of `t`) by fixed picked sides and fixes a switch only
when exactly one side of an unfixed switch leaves the component. From `s` the two sides `h_1 = E(x_1)` and `E(d)`
contain `s`; so the walk from `s` stops at once unless the trial fixes `x_1` or `d`:
- trial `x_1` F: the only exit is `E(d)`; after fixing `d` E the component is `E(d)`, whose exits are all `E(m_c)` and
  `Fl_q`; stop;
- trial `d` F: the exits are forced along `h_1, h_2, ..`, which reaches `t` (no refutation);
- trial `d` E, `x_1` E: two exits after one step; stop.
From `t`: without back, `t` lies only in `h_2k`, so the trial `x_2k` E is refuted (no exit) and `x_2k` is fixed F; every
other trial reaches `h_2k`, whose node `z_{p,2k}` lies in `Fl_p` for every E-member `p`, so at least `k >= 2` exits
remain (if the trial fixes some `x_c`, `c <= k`, in F-mode, `Fl_c` is a fixed picked side meeting `h_2k`, and the
component then meets every `h_q`, again with many exits). With back, `t` lies in `h_2k` and `F(d)`: two exits, or,
after one forced step, `F(d)` (exits `Fl_b`, `E(m_1)`) or `h_2k` (exits `Fl_p`); no refutation. Repeating the round
with `x_2k` fixed changes nothing. (The contact nodes of `Y'^d_k` only add exits.)

(iv) As in the proof of r4-general Theorem Y(ii), now with `d` present. An accepted walk `W` is valid (Theorem 5'),
so its sides are picked by a solution, hence by (ii) they lie in the side graph of the two solutions: the path
`h_1 .. h_2k`, plus the blob attached at `s` (`d` E) or `F(d)` attached at `t` and to `E(m_1)` (`d` F, back). So `W`
contains every `h_c`, `c <= k`. `Π(h_c) = {Fl_c, F(m_c)}` (`d` is incomparable with `m_c`), so when `h_c` is appended,
`F(m_c) ∈ K ∪ Dc` or `h_c` declares. `F(m_c)` is declared only by a side whose conflict family contains it, i.e. by
`h_c` or `E(m_c)`, each declaring one mate. `F(m_c)` lies in a set `N_F[Z]` only if `Z` meets `F(m_c)`: `Z = F(m_c)`,
`Z = Fl_b` (`b != c`), or (in `Y'^d_k`) `Z = h_{k+c}`; `d` adds no node to `F(m_c)`. `N_F[Fl_b]` contains every
F-member `h_q` (`z_bq`), all on `W`, so it needs storage `>= k`; `N_F[F(m_c)]` and `N_F[h_{k+c}]` contain `F(m_c')`
only for `c' = c` (the sides `F(m_c)` are pairwise disjoint). Hence at most `kd + ks + s` mates are covered when
`B < k`. For the refined search the same count holds (r4-general Proposition Y', whose proof uses only the walk, the
conflict families and the sets `N_F[Z]` containing `F(m_c)`, all unchanged by `d`): `F(m_c)` is reachable from
`h_{k+c}` through `fc_c` unless deleted, deleting it needs a set of `K` containing it, and a set `N_F[h_{k+c}]` puts
the members `h_{k+c-1}, h_{k+c}, h_{k+c+1}` into `S`. ∎

*Checked* (`test_fool.py 2 6`, `test_fool2.py 4 6 refined`; logs in the session record of §9): for `k = 2..6`, both
variants, `Y^d_k` and `Y'^d_k`: P2 holds, `gcert.exact` = yes, `Gen.brute` finds exactly 2 solutions, `gsw.prune`
fixes 1 switch (`x_2k`) or 0; HYB `(1, 0, 1, 3)` rejects for every `k >= 4`, `(1, 1, 2, 6)` accepts `k = 4, 5, 6`
(`B = 6 >= k`, as (iv) allows); the refined search `(1, 0, 1, 3)` accepts `Y^d_k` and rejects `Y'^d_k`, `k = 4, 5, 6`.
Without `d` the same instances are rigid (pruning fixes every switch) and HYB `(1, 0, 1, 3)` accepts, as in r4-general.

### 2.3 Reading

The rigid families `X_L`, `Y_k`, `Y'_k` were solved by HYB only because forced-exit propagation reproduces their
first-flip induction, which starts at the terminal `s` with a single exit. One extra switch that offers a second,
useless exit at `s` (its E-side leads into the dead-end blob of the mates' E-sides; in the back variant the blob
returns to `t` only through the partner `F(d)`) stops the induction before it begins, and the irrelevant mates stay
free. The certificate part of HYB then faces exactly the obstruction of Theorem Y. So HYB's propagation is the weak
point: a correct algorithm must recognise rigidity that local forced exits do not see.

## 3. Closure-based mode descriptions (CDESC)

The certificates of HYB *watch* conflict families during a walk; the families `Y_k`, `Y^d_k` defeat them because
an E-member's conflict family contains the F-side of an irrelevant up-mate. A mode vector can instead be *described*
and tested directly; then the order itself takes care of the up-mates (closure). This is the general-order version of
the "certificates as mode descriptions" of `r5-classes.md` §2a (written there for classes without order; there it is
shown that DESC with bounded parameters decides 2CH + P2, via r4-switch Theorem 8).

### 3.1 Definition and soundness (proved)

`Enon` (`Fnon`) = switches with non-empty E-side (F-side). For a side or node `Z`:
`NE(Z) = {w : E_w ≠ ∅, E_w ∩ Z ≠ ∅}`, `NF(Z) = {w : F_w ≠ ∅, F_w ∩ Z ≠ ∅}` (sets of switches).
*E-description* with centres `Z_1 .. Z_f` and flip set `Φ`: `U = NE(Z_1) ∪ .. ∪ NE(Z_f)`, `G = (Enon − U) △ Φ`,
`D = Q − ↑G`. *F-description*: `U' = NF(Z_1) ∪ ..`, `G' = (Fnon − U') △ Φ`, `D = ↓G'`.
**CDESC(f, e)**: for both kinds, every choice of at most `f` centres (sides and single nodes) and every `Φ` with
`|Φ| <= e`, test whether the picked hypergraph of `D` connects `s` and `t`; answer yes iff some test succeeds.
*Soundness.* `D` is a down-set (complement of an up-set, resp. a down-closure), so every success is an
order-consistent connecting mode vector. *Time.* `O((D_s + N)^f m^e (N + D_s) m)` per kind (`D_s` sides, `N`
nodes, `m` switches): polynomial for fixed `f, e`. No propagation is used.

### 3.2 Lemma G (guided cost; proved)

Let `P` be a valid path, `W_E`, `W_F` its E- and F-members, `L = ↓W_F`, `Up = ↑W_E`, `A` the minimal elements of
`W_E` (no E-member strictly below). For a set `U` of switches put
`out = L ∩ Enon − U`, `G1 = (Enon − U) − L`, `in = {a ∈ A : no element of G1 is <= a}`.
Then the E-description with this `U` and `Φ = out ∪ in` succeeds; so `cost_E(P, U) = |out| + |in|` flips suffice.
Dually `cost_F(P, U') = |Up ∩ Fnon − U'| + |{b maximal in W_F : no element of (Fnon − U') − Up is >= b}|`.
*Proof.* `G = G1 ∪ in`: `out = (Enon − U) ∩ L` is removed by the flip; `in` is disjoint from `Enon − U` (an
element of `A ∩ G1` is `<=` itself, so it is not in `in`, and `A ∩ L = ∅`), so the flip adds exactly `in`. `G ∩ L = ∅`: `G1 ∩ L = ∅`
and `A ∩ L = ∅` (a valid path has `Up ∩ L = ∅`). `L` is a down-set, so `↑G ∩ L = ∅` (`g <= y ∈ L` gives `g ∈ L`),
i.e. `L ⊆ D`. Every `a ∈ A` lies in `↑G` (in `↑G1`, or `a ∈ in ⊆ G`), and every E-member lies above an element of
`A` (finite preorder), so `W_E ⊆ ↑G`, i.e. `W_E ∩ D = ∅`. Hence `D` puts every F-member into F-mode and every
E-member into E-mode, all members of `P` are picked, and `P` joins `s` to `t` in the picked hypergraph. ∎
Two consequences: an up-mate `m > a` of an E-member costs nothing on the E-side (it lies in `↑a ⊆ ↑G` whatever `U`
says), and an E-member costs a flip only if it is minimal, its E-side lies in `U` and nothing below it lies in `G1`.
What the E-side must pay for is the cover of `{E_y : y ∈ L}`: the partners of the F-members and the E-sides of all
switches below F-members (the *strict part* on the F-side).

### 3.3 Proposition CF: the known obstruction families are cheap for CDESC (proved; checked)

(i) `Y_k`, `Y'_k` (`k >= 2`): the E-description with the single centre `Fl_{2k}` (the flip side of the last
F-member) and no flip gives `D = {x_{k+1}, .., x_{2k}}`, the unique solution.
(ii) `Y^d_k`, `Y'^d_k`, both variants: the same centre gives `D = {x_{k+1}, .., x_{2k}, d}`, a solution.
(iii) `X_L`: the centre `E(m_1)` (an odd mate) and no flip for even `L`, one flip (`x_L`) for odd `L`.
(iv) `Z_k`, `Z^B_k`: one centre, no flip (checked `k <= 4`).
*Proof.* (i), (ii) `Fl_{2k} = E(x_{2k})` consists of the nodes `w_{q,2k}` (`k < q < 2k`), `e_{c,2k}` (`c <= k`)
and, in `Y^d`, `δ_{2k}`; the `z`-nodes `z_{p,2k}` lie in `h_{2k}`, not in `Fl_{2k}`. So the E-sides meeting it are
`Fl_q = E(x_q)` (`q > k`), the mate sides `E(m_c)` and `E(d)`: `U = {x_q : q > k} ∪ {m_c} (∪ {d})`. Every switch has
a non-empty E-side, so `G = {x_1, .., x_k}`, `↑G = {x_c, m_c : c <= k}` and `D = {x_q : q > k} (∪ {d})`, which is
the unique solution of `Y_k`, `Y'_k` (r4-general Theorem Y(i), Proposition Y') and a solution of `Y^d_k`, `Y'^d_k`
(Proposition D(ii); `d` may be in either mode). (iii) `E(m_1) = {t} ∪ {c_{1j} : j even}`; the E-sides containing `t`
are `Fl_k = E(x_k)` (`k` even), `E(m_k)` (`k` odd) and `h_L = E(x_L)` if `L` is odd; those containing `c_{1j}` are
`E(m_j)` (`j` even). So `G = {x_k : k odd} − {x_L if L odd}` and `↑G` adds the odd mates; for even `L`,
`D = {x_k, m_k : k even}`, the unique solution (r4-general Proposition X(ii)); for odd `L` the flip of `x_L` gives the
same. ∎ *Checked* (`test_cdesc.py families 4`, `runs/cdesc-fam-4.txt`): `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k` (`k <= 4`,
both variants), `X_L` (`L <= 8`), `Z_k`, `Z^B_k` (`k <= 4`): guided cost 0 or 1 with one centre, and
`decide(1, 1)` finds a solution on all with at most 40 switches.

So none of the families that defeat the walk certificates (HYB, NG, GC) is an obstruction to description-based
algorithms, and HYB's failure on `Y^d_k` is an artefact of watching conflicts during a walk. On the other hand
`decide(1, 1)` rejects 44 of the small portfolio-hard instances of `r4-search` (6 to 8 switches, 2CH-like): their
guided cost is 2 to 3 flips with one or two centres, as expected from r4-switch Theorem 8 (several dominators may be
needed in 2CH). Random instances (`test_cdesc.py random 1 300 6 12`): 196 yes-instances, 178 of them in the core of
r4-general (propagation leaves comparable free switches); guided cost with one centre 0 on 163, 1 on 15 of the core
instances; one instance (not core) has cost 2 and is solved by `decide(1, 2)`.

### 3.4 Where CDESC must pay: the strict parts (sketch, the obstruction to be built or excluded)

By Lemma G the E-side needs a bounded cover of `{E_y : y ∈ L}` with few minimal E-members inside, the F-side a cover of
`{F_z : z ∈ Up}` with few maximal F-members inside. The partner parts are the 2CH situation (r4-switch Theorem 8,
r5-classes Corollary 2a.2), except that F3 fails for comparable pairs (F-member below E-member). For the strict part on
the F-side, a switch `y ∈ L` off `P` has a compatible F-side (a window of at most 3 consecutive positions), and P2
with an F-member `q ∥ y` outside that window gives `E_y ∈ NE(X'_q)` (partner neighbourhood, cost = number of minimal
E-members meeting `X'_q`), with an E-member `b ∥ y` it gives `E_y ∈ NE(X_b)` (cheap) unless `F_y ∩ X'_b ≠ ∅`. So
the strict parts are expensive on both sides only if (a) the F-sides of the switches below F-members meet the
partners of the E-members, (b) the E-sides of the switches above E-members meet the partners of the F-members, and
(c) every member has many contacts of the other type. §4 records the attempts to build this.


## 4. Attempts to build the obstruction of §3.4 (checked)

### 4.1 The family `W_n` (`wfam.py`, second run; checked)

`W_n`: base word `E^n F^n E^n F^n` (blocks A, B, C, D) in switch form with the cyclic contact rule A->B, B->C, C->D,
D->A (every member has `n` contacts of the other type), plus an up-mate for every E-member and a down-mate for every
F-member, all mate sides floating (they meet only flip sides and other mate sides), mates paired by P2 through F-sides
(`F`), E-sides (`E`) or at random. *Checked* (`test_wfam.py`, logs `runs/wfam-3-*.txt`): `n = 1, 2, 3`, all pairings:
P2 holds; for `n >= 3` the shortest valid paths are not the base path but hub paths of length 7 (each flipped block
member shortcuts the next block through its flip side), so the intended structure is destroyed; HYB `(1, 0, 1, 3)` or
`(1, 1, 2, 6)` and CDESC `decide(1, 1)` solve all of them. The mates' P2 obligations among themselves always give a
free centre on one side (pairing `F`: the F-side of a down-mate covers all up-mates; pairing `E` dually); a random
pairing needs about `log n` mate centres, never more (a bipartite graph and its complement cannot both have the property
"every `f` rows have a common neighbour" for `f > log_2 n`).

### 4.2 The family `OB` (`obfam.py`, `test_ob.py`; checked)

Critical-run base `E^K F^M E^K2` (first block forward with contacts in the run, run members forward with contacts in the
last block, optionally `back`: last-block members with contacts in the run) plus `k` down-mates with private E-contact
sets in the last block and F-sides meeting the partners of all other E-members, and `k` up-mates dually; `y_i < z_j` for
all down-mates and up-mates (no P2 between mates). *Checked*: `(K, M, K2, k, sz) = (2,2,2,1,1), (3,3,3,2,1)`: the
planted path is shortest, everything is solved; `(4,4,4,2,2), (6,6,6,3,2)`: the planted path is not shortest (length 12
resp. 18 against 10 resp. 12): with `back` the contacts in both directions form non-tight straddles (r4-switch Lemma 7),
whose double swap is a shortcut; without `back` the last-block E-members have no contacts and their partners are free
centres for the F-description. Propagation, HYB `(1, 0, 1, 3)`, CDESC and ADESC (§5) solve all instances.

**Reading.** An obstruction to descriptions needs, on both sides, members all of whose partners are expensive centres.
In the switch model the straddle condition (r4-switch Lemma 7) makes this impossible near the boundary between forward
and backward members (§5.3); §5 turns this into the conditional theorem TCA ⇒ ADESC, which is independent of the mates.

## 5. Anchored descriptions (ADESC) and the two-cheap-anchors condition (TCA)

### 5.1 Definition and soundness (proved)

Notation of §3 and of a valid path `P`: `W_E`, `W_F` its E- and F-members, `Up = ↑W_E`, `L = ↓W_F`,
`A = {a ∈ W_E : no E-member strictly below a}` (minimal E-members), `B = {b ∈ W_F : no F-member strictly above b}`
(maximal F-members); `pos(w)` is the position of a member.
*Anchored E-description* with F-anchors `B_0`, E-anchors `A_0`, centres `Z_1..Z_f`, flips `Φ` (`adesc.describe`):

    U = NE(Z_1) ∪ .. ∪ NE(Z_f),   G = ((Enon − U) − ↓B_0) △ Φ,   G := G ∪ A_0,   D = Q − ↑G,

skipped when `G ∩ ↓B_0 ≠ ∅` or `↓B_0 ∩ ↑A_0 ≠ ∅`. *Anchored F-description* dually (`U' = ∪ NF(Z_i)`,
`G' = ((Fnon − U') − ↑A_0) △ Φ ∪ B_0`, `D = ↓G'`). **ADESC(a, f, e)**: all descriptions of both kinds with at most `a`
anchors of each kind, `f` centres and `e` flips; answer yes iff some `D` connects `s` and `t`.
*Soundness:* every tested `D` is a down-set, so an accepted `D` is an order-consistent connecting mode vector. *Time:*
`O(m^{2a} (D_s + N)^f m^e (N + D_s) m)`. Centres may be taken in the instance in which the fixed picked sides of the
anchors (`F_v`, `v ∈ ↓B_0`; `E_v`, `v ∈ ↑A_0`) are contracted (as in Theorem R); this changes only which switches a
centre covers, not soundness. Guided cost of a path (`adesc.guided_cost_E`): `out = (L ∩ Enon − U) − ↓B_0`,
`G1 = (Enon − U − ↓B_0) − L`, `in = {a ∈ A : no element of G1 ∪ A_0 is <= a}`; flipping `out` out of and `in` into
`G` gives `L ⊆ D ⊆ Q − Up` (Lemma G with anchors), so `|out| + |in|` flips suffice.

### 5.2 Theorem TCA ⇒ ADESC (proved)

For a valid path `P` and `b ∈ B` let `f*_A(b)` be the set of `a ∈ A` whose path side `X_a` meets `E_b` or meets `F_v`
for some switch `v < b` with `F_v ∩ E_b ≠ ∅` (the second alternative only arises through middle witnesses; without
middle edges `f*_A(b) = f_A(b)`, the minimal E-members among the contacts of `b`). Dually `f*_B(a)` for `a ∈ A`.

**Theorem 5.2.** Let `P` be a shortest valid path of a ZZ + P2 instance in general switch form.
(E1) If the positions of `B` lie in an interval of length 4, the E-description with `B_0 = B` (at most 5 anchors), no
centre and no flip succeeds.
(E2) If `b_1, b_2 ∈ B`, `|pos(b_1) − pos(b_2)| >= 5`, the E-description with `B_0 = {b_1, b_2}`, the centres
`E_{b_1}`, `E_{b_2}` (in the instance with `F_v`, `v ∈ ↓B_0`, contracted) and the flip set `Φ = f*_A(b_1) ∪ f*_A(b_2)`
succeeds. Without middle edges distance `>= 3` suffices.
(F1), (F2) Dually with `A`, F-descriptions, E-anchors `a_1, a_2` and centres `F_{a_1}, F_{a_2}`.
Consequently, if some shortest valid path satisfies **TCA(c)** — (E1), (F1), or (E2)/(F2) with
`|f*(·) ∪ f*(·)| <= c` — then ADESC(5, 2, c) accepts. *The mates do not enter the condition*: TCA is a statement about
the members `A ∪ B` of one shortest path and their contacts only.

*Proof.* Facts used. (a) `y ∈ L` and `y ∉ P` imply that `F_y` is *compatible* with `P` (no E-member `a <= y`, else
`a <= y <= q` for an F-member `q`); the *window* `Win(y) = {c : F_y ∩ X_c ≠ ∅}` then has `max − min <= 2` (else
`X_1 .. X_c F_y X_d .. X_r` is a shorter valid path). (b) If `w > b` for some `b ∈ B`, then `w ∉ L` (else
`b < w <= q`, `q` an F-member, contradicting maximality of `b`), so `E_w` is compatible with `P`; if `w` is a member
it is an E-member and `E_w = X_w`. (c) A valid walk from `s` to `t` contains a valid path of at most its length, so
every valid walk has length `>= r`.
(E1) `U = ∅`, `G = Enon − ↓B` (no flips). `L = ↓B ⊆ D`: an element of `L` above a generator `g` would force
`g ∈ ↓B`. Every `a ∈ A` has `E_a = X_a ≠ ∅` and `a ∉ ↓B` (else `a <= b` with `a` an E-member and `b` an F-member), so
`a ∈ G`; every E-member lies above an element of `A`, so `W_E ⊆ ↑G`, `W_E ∩ D = ∅`. All members are picked by `D`.
(E2) Let `y ∈ L − ↓B_0` with `E_y ≠ ∅`. *`y ∥ b_i`:* `y <= b_i` is excluded; `y >= b_i` together with `y <= b'` for
some `b' ∈ B` gives `b_i <= b'`, hence `b_i ~ b'` by maximality and `y ~ b_i ∈ ↓B_0`, excluded. By P2 for `y, b_i`:
(i) `E_y ∩ E_{b_i} ≠ ∅`; or (i') `F_y ∩ X_{b_i} ≠ ∅` (`F_{b_i} = X_{b_i}`); or (ii) a lower middle witness `w < y, b_i`,
whose side `F_w` meets `E_y` and `E_{b_i}` by private nodes; `w < b_i` puts `w ∈ ↓B_0`, `F_w` is contracted into the
centre, and `E_y` meets the contracted centre; or (iii) an upper middle witness `w > y, b_i`, whose side `E_w` meets `F_y`
and `X_{b_i}`. In cases (i), (ii) `y ∈ U`. Suppose (i') or (iii) holds for both `i = 1, 2` (*links* from `y` to `b_i`,
direct or through `E_{w_i}`). If `y ∉ P`, the walk `X_1 .. X_{b_1}, [E_{w_1}], F_y, [E_{w_2}], X_{b_2} .. X_r` (for
`pos(b_1) < pos(b_2)`) is valid: `F_y` and every `E_{w_i}` are compatible with the kept members by (a), (b), and
`F_y`, `E_{w_i}` do not conflict (`w_i > y`, a conflict pair `{E_w, F_y}` needs `w <= y`); consecutive sides meet; a
`w_i` that is a member is an E-member at distance `<= 1` from `b_i`, which only shortens the walk. Its length is at most
`pos(b_1) + 3 + r − pos(b_2) + 1`, so (c) gives `pos(b_2) − pos(b_1) <= 4`, a contradiction. If `y ∈ P`, `y` is an
F-member with `F_y = X_y`; a direct link gives `|pos(y) − pos(b_i)| <= 1` (F1), a link through `E_{w_i}` gives
`|pos(y) − pos(b_i)| <= 2` (shortcut through the compatible `E_{w_i}`, or `w_i` a member adjacent to both); so
`|pos(b_1) − pos(b_2)| <= 4`, a contradiction. Hence `out = ∅`. Then `G ∩ L = ∅` (`out = ∅` and `Φ ⊆ A`,
`A ∩ L = ∅`), so `L ⊆ D` (`L` is a down-set); `↓B_0 ⊆ D` likewise. Every `a ∈ A` is in `G`: if `X_a` meets no
centre, `a ∈ Enon − U − ↓B_0`; otherwise `a ∈ f*_A(b_1) ∪ f*_A(b_2) = Φ`. So `W_E ⊆ ↑G` and `D` picks every member.
Without middle edges only (i), (i') occur and the window argument needs `|pos(b_1) − pos(b_2)| >= 3`. (F1), (F2): the
same argument for the reversed order (exchange E and F, `A` and `B`, lower and upper witnesses). ∎

**Proposition 5.2' (strict anchors; proved).** For `a ∈ A`, `↓a − [a]` (`[a]` the class of `a`) contains no element of
`Up` (an element `w < a` of `Up` would lie above an E-member `a' < a`). Hence if `B ⊆ ↓B_0 ∪ ⋃_{a ∈ A_1} (↓a − [a])`,
the down-set `D = ↓B_0 ∪ ⋃_{a ∈ A_1} (↓a − [a])` picks every member of `P` (it contains `L`, and it misses `Up`).
Dually with `↑b − [b]`, `b ∈ B`. This is the strict guess of the ladder `K(k)` (`dc-algorithm.md` §11.6).

### 5.3 Is TCA always available? (sketch, checked)

TCA mentions no mates, so it is a statement about one shortest valid path: *some type has its skeleton members in a
short interval, or two far skeleton members with few contacts.* In the switch model (`A = W_E`, `B = W_F`) this is the
two-member form of Hypothesis H of `r5-classes.md`. Sketch of why it should hold there: by Lemma 1 of r4-switch, a
forward member forces every member of the other type at distance `>= 2` to its left to be forward with it as contact,
and a backward member dually; the members near the boundary between the forward and the backward members have few
forced contacts, and the cross contacts between forward members and backward members near the boundary form a
straddle-free matrix (Lemma 7), whose staircase shape leaves at least one cheap member on one side of every crossing
pair; two of the same type are needed. Not proved.
In the general model TCA can fail through *voluntary contacts* between comparable members (`b < a`, `b ∈ B`, `a ∈ A`):
such pairs need no P2 witness, their straddles cannot be swapped (the swap would use `E_b` and `F_a`, a conflict pair),
so they may carry many contacts. The two-zone example `F^n E^n` with `b < a` for all cross pairs and many voluntary
contacts has no cheap skeleton member, but Proposition 5.2' solves it with one strict anchor (`B ⊆ ↓a − [a]` for any
`a ∈ A`); it is a series composition of two antichains. §6 records what happens in between.

## 6. Extending Theorem Q to general ZZ + P2 (fourth run, 2026-10-22 evening; in progress)

Task of the coordinator: extend the minimax argument of `r5-classes.md` Theorem Q (Lemma W, Lemma D, zero-sum game,
`O(log m)` sampled centres, `O(log m)` flips) from 2CH with classes to general ZZ + P2, or find the obstruction.
§1-§5 are under review and are not changed; corrections of them are in §7.

### 6.0 Results of §6-§8

| # | Statement | Status |
|---|---|---|
| 6.2 | Window lemma for chains of `P`-consistent sides (a chain of `j` sides between `X_c` and `X_d` forces `|c − d| <= j + 1`) | proved |
| 6.3 | **Sibling stars are cheap.** For every switch `x ∉ L` the star `E#_x` (`E_x` plus the private nodes of the middle edges at the lower middle neighbours of `x`) meets at most 9 minimal E-members; dually for `F#_y`, `y ∉ Up` | proved; checked (§6.6) |
| 6.4 | **Duality for every incomparable pair**, node or middle witness: for `x ∈ N_F`, `y ∈ N_E`, `x ∥ y`, `E#_x` covers `y` or `F#_y` covers `x` | proved; checked |
| 6.5 | **Theorem Q for general ZZ + P2 up to the bad pairs.** If a shortest valid path has a vertex cover of size `κ` of its *bad pairs* (`y < x`, `x ∈ N_F − A`, `y ∈ N_E − B`), the instance is accepted by GDESC with `⌊log2 m⌋ + 1` star tools, `κ` anchors and `9(⌊log2 m⌋ + 1)` flips; time `m^{O(κ + log m)}`. Theorem Q is the case `κ = 0` | proved |
| 6.5' | The same with any fractional cover: if the needed sides of one type have LP cover number `<= T` by the cheap tools (stars, strict anchors, anchors), `O(T log m)` tools suffice | proved |
| | (in progress) | |

### 6.1 Setting and the `P`-consistent sides

General switch form of `r4-general.md` §5.1 (as in §1): switches `Q` with a preorder, sides `E_w`, `F_w`, a mode vector
is a down-set `D` (F-mode), a middle edge `z v` (`z < v`) is a private node of `F_z ∩ E_v`; `LMN(v)` (`UMN(z)`) are
the lower (upper) middle neighbours. P2 for incomparable `x, y`: a node of `E_x ∩ E_y` or of `F_x ∩ F_y`, or a lower
middle witness `z < x, y` (edges `z x`, `z y`), or an upper middle witness `z > x, y` (edges `x z`, `y z`).
Fix a shortest valid path `P = X_1 .. X_r` with `W_E`, `W_F`, `Up = ↑W_E`, `L = ↓W_F` (`Up ∩ L = ∅`), `A` (minimal
E-members: no E-member strictly below), `B` (maximal F-members). The *needed items* are
`N_E = {y ∈ L : E_y ≠ ∅}` and `N_F = {x ∈ Up : F_x ≠ ∅}`; a down-set `D` picks every member of `P` iff
`L ⊆ D ⊆ Q − Up`. A side is *`P`-consistent* if it is `E_w` with `w ∉ L` or `F_w` with `w ∉ Up`.
(a) A `P`-consistent side conflicts with no member: `E_w` and a member `F_b` conflict iff `w <= b`, which puts `w`
into `L`; dually for `F_w`. (b) A `P`-consistent side of a switch on `P` is a member (`E_w`, `w ∉ L`, `w` on `P`
gives `w ∈ W_E`). (c) Two `P`-consistent sides conflict only if they are `E_w`, `F_z` with `w <= z`, both `w, z`
outside `Up ∪ L` (`w ∈ Up` would give `z ∈ Up`, `z ∈ L` would give `w ∈ L`); in particular `E_x` (`x ∈ Up`) and `F_y`
(`y ∈ L`) never conflict, whatever the order between `x` and `y`.
An *E-description* (GDESC, `gdesc.describe`) with tool switches `T`, flagged tools `T' ⊆ T`, F-anchors `Y_0` and
flips `Φ`:

    U = ∪_{x ∈ T} NE(E#_x),   S = ↓Y_0 ∪ ∪_{x ∈ T'} (↓x − [x]),   G = (Enon − U − S) ∪ Φ,   D = Q − ↑G;

an *F-description* dually (`F#`, up-sets, `D = ↓G'`). Every `D` produced is a down-set, so GDESC is sound for all
parameters; `E#`, `F#` are defined in §6.3.

### 6.2 Windows of chains (Lemma 6.2; proved)

**Lemma 6.2.** Let `Z_1, .., Z_j` (`j >= 1`) be `P`-consistent sides of pairwise distinct switches none of which is on
`P`, no two of them a conflict pair, with `Z_i ∩ Z_{i+1} ≠ ∅`. If `X_c ∩ Z_1 ≠ ∅` and `X_d ∩ Z_j ≠ ∅`, then
`|c − d| <= j + 1`. For `j = 1` this is Lemma W of `r5-classes.md` (window of at most 3 consecutive positions).
*Proof.* Let `c < d` (otherwise reverse the chain). The walk `X_1 .. X_c Z_1 .. Z_j X_d .. X_r` has `s` in its first
and `t` in its last side, consecutive sides meet, and its side set has no conflict pair: members do not conflict
(`P` is valid), a member and a `Z_i` do not by (a), two `Z_i` do not by assumption. A shortest sub-walk from `s` to `t`
of a consistent walk is a valid path (distinct sides of a consistent set belong to distinct switches, since `E_w`,
`F_w` conflict), so `c + j + r − d + 1 >= r`. ∎

### 6.3 Sibling stars: cheap tools for middle witnesses (Lemmas 6.3, 6.4; proved)

For a switch `w` let `E#_w = E_w ∪ {private nodes of the middle edges z v : z ∈ LMN(w)}` and
`F#_w = F_w ∪ {private nodes of the middle edges v z : z ∈ UMN(w)}` (node sets; `gstar.Stars`). The private node of
`z v` lies in `E_v` (and `F_z`) only, so `NE(E#_w) = NE(E_w) ∪ Sib↓(w) ∪ {w}` with `Sib↓(w)` the switches that share a
lower middle neighbour with `w`; dually `NF(F#_w) = NF(F_w) ∪ Sib↑(w) ∪ {w}`. In the classes model (no middle edges)
`E#_w = E_w`.

**Lemma 6.3 (stars are cheap).** For every switch `x ∉ L` the set `S_x = A ∩ NE(E#_x)` lies in an interval of at most
9 consecutive positions; so `|S_x| <= 9`. Dually `|B ∩ NF(F#_y)| <= 9` for every `y ∉ Up`.
*Proof.* `a ∈ S_x` means (i) `X_a ∩ E_x ≠ ∅`, or (ii) some `z ∈ LMN(x) ∩ LMN(a)`. In (ii), `z ∉ Up`: an E-member
`a'' <= z < a` would lie strictly below `a`. So `F_z` is `P`-consistent, and it meets `X_a` and `E_x` (private nodes
of `z a`, `z x`); `F_z`, `E_x` are no conflict pair (that needs `x <= z`, but `z < x`).
*`x` not on `P`, window `win(E_x) = {c : X_c ∩ E_x ≠ ∅} ⊆ [p, p + 2]` non-empty* (Lemma 6.2, `j = 1`). (i) gives
`pos(a) ∈ [p, p + 2]`. In (ii): if `z` is on `P`, it is an F-member (`z ∉ Up`), `X_z = F_z` meets `X_a` and `E_x`, so
`|pos(z) − pos(a)| = 1` (F1) and `pos(z) ∈ win(E_x)`; if `z` is not on `P`, Lemma 6.2 for the chain `F_z, E_x` gives
`|pos(a) − c| <= 3` for `c ∈ win(E_x)`. So `S_x ⊆ [p − 3, p + 5]`.
*`x` not on `P`, `win(E_x) = ∅`.* (i) is empty and `z` is never on `P` (else `X_z ∈ win(E_x)`). For `a, a' ∈ S_x` with
witnesses `z, z'`: if `z = z'`, `pos(a), pos(a') ∈ win(F_z)` differ by `<= 2`; otherwise the chain `F_z, E_x, F_{z'}`
(distinct switches, no conflict pair) gives `|pos(a) − pos(a')| <= 4`.
*`x` on `P`*: `x ∈ W_E` (`x ∉ L`), `E_x = X_x` at position `e`. (i) gives `|pos(a) − e| <= 1` (F1, or `a = x`). In
(ii), `z` on `P` is an F-member adjacent on `P` to `a` and to `x`, so `|pos(a) − e| <= 2`; `z` not on `P` gives
`pos(a), e ∈ win(F_z)`, so `|pos(a) − e| <= 2`. The dual statement is the same proof with the order reversed. ∎

**Lemma 6.4 (duality for incomparable pairs).** Let `x ∈ N_F`, `y ∈ N_E` be incomparable. Then `y ∈ NE(E#_x)` or
`x ∈ NF(F#_y)`.
*Proof.* P2 for `x, y`: a node of `E_x ∩ E_y` gives `y ∈ NE(E_x)`; a node of `F_x ∩ F_y` gives `x ∈ NF(F_y)`; a lower
middle witness `z` has `z ∈ LMN(x)`, and the private node of `z y` lies in `E#_x ∩ E_y`; an upper middle witness `z`
has `z ∈ UMN(y)`, and the private node of `x z` lies in `F_x ∩ F#_y`. ∎
So middle witnesses, the second obstacle named by the coordinator, cost nothing beyond Theorem Q: Lemma D of
`r5-classes.md` holds for every incomparable pair once the centres are the stars, and Lemma W is replaced by Lemma
6.3 (9 instead of 3). Tools are needed only for the comparable pairs (`y < x`; ties between `Up` and `L` are
impossible).

### 6.4 The minimax with anchors (Theorem 6.5; proved)

*Tools.* The *E-tool* of `x ∈ N_F` is the centre `E#_x`, together with the strict anchor `↓x − [x]` if `x ∈ A`; it
covers `cov_E(x) = (NE(E#_x) ∪ (↓x − [x] if x ∈ A)) ∩ N_E`. The *F-tool* of `y ∈ N_E` is `F#_y` with the strict
anchor `↑y − [y]` if `y ∈ B`. A strict anchor at `a ∈ A` contains no element of `Up` (an element `w < a` of `Up` lies
above an E-member strictly below `a`) and no element of `A`; dually for `b ∈ B` (Proposition 5.2').
A pair `(x, y) ∈ N_F × N_E` is *bad* if `y < x`, `x ∉ A` and `y ∉ B`. By Lemma 6.4 and the strict anchors, every pair
that is not bad satisfies the **duality**: `y ∈ cov_E(x)` or `x ∈ cov_F(y)` (incomparable: Lemma 6.4; `y < x` with
`x ∈ A`: the strict anchor at `x`; `y < x` with `y ∈ B`: the strict anchor at `y`).

**Theorem 6.5.** Let `P` be a shortest valid path of a ZZ + P2 instance in general switch form with `m` switches,
`X_0 ⊆ N_F`, `Y_0 ⊆ N_E` such that every bad pair has `x ∈ X_0` or `y ∈ Y_0`, and `k = ⌊log2 m⌋ + 1`. Then one of
(E) and (F) holds:
(E) there are `x_1, .., x_k ∈ N_F` such that the E-description with `T = {x_i}`, `T' = T ∩ A`, F-anchors `Y_0` and
`Φ = A ∩ U` (`|Φ| <= 9k`) picks every member of `P`;
(F) dually, `y_1, .., y_k ∈ N_E`, `T' = T ∩ B`, E-anchors `X_0`, `Φ = B ∩ U'` (`|Φ| <= 9k`).
Hence GDESC with `k` tools (all flag patterns), `|X_0| + |Y_0|` anchors and `9k` flips accepts, in time
`m^{O(k + |X_0| + |Y_0|)} · poly`; with `κ` the vertex cover number of the bipartite graph of the bad pairs, ZZ + P2
is decided in time `m^{O(κ + log m)}` on the instances that have a shortest valid path with at most `κ` bad-pair
cover. In 2CH with classes there are no comparable pairs between `Up` and `L`, so `κ = 0`: this is Theorem Q (with
9 instead of 3 because of the stars, unnecessary without middle edges).
*Proof.* If `N_E − Y_0` is empty, (E) holds with no tool: `G = Enon − ↓Y_0 ⊇ A`, and `G ∩ L = ∅` because every
element of `L ∩ Enon` lies in `↓Y_0`. Likewise if `N_F − X_0` is empty. Otherwise consider the zero-sum game with rows
`x ∈ R = N_F − X_0`, columns `y ∈ C = N_E − Y_0` and payoff `1` if `y ∈ cov_E(x)`, else `0`; let `λ` be its value.
*`λ >= 1/2`.* A distribution `p` on `R` has `Pr_{x~p}[y ∈ cov_E(x)] >= 1/2` for every `y ∈ C`; `k` independent draws
miss a fixed `y` with probability `<= 2^{−k} < 1/m`, so some draw `x_1, .., x_k` has `C ⊆ ∪ cov_E(x_i)`. In the
E-description of (E): every `y ∈ N_E` lies in `U` (`y ∈ NE(E#_{x_i})`), in `↓x_i − [x_i]` for some `x_i ∈ A`, or in
`↓Y_0`, so `y ∉ G − Φ`; `Φ ⊆ A` is disjoint from `L`; elements of `L` with empty E-side are not in `Enon`. Hence
`G ∩ L = ∅`, and `L ⊆ D` because `L` is a down-set. Every `a ∈ A` is in `G`: if `a ∉ U`, then `a ∈ Enon` (`E_a = X_a`),
`a ∉ ↓Y_0` (`a ∉ L`), `a ∉ ↓x_i − [x_i]` (no element of `A` is strictly below an element of `A`); if `a ∈ U`,
`a ∈ Φ`. So `Up = ↑A ⊆ ↑G` and `D ∩ Up = ∅`: `D` picks every member of `P`, hence connects `s` and `t`.
`|Φ| <= 9k` by Lemma 6.3 (`x_i ∈ Up`, so `x_i ∉ L`).
*`λ < 1/2`.* A distribution `q` on `C` has `Pr_{y~q}[y ∈ cov_E(x)] < 1/2` for every `x ∈ R`; no pair of `R × C` is bad,
so by the duality `Pr_{y~q}[x ∈ cov_F(y)] > 1/2` for every `x ∈ R`, and `k` draws cover `R`. The F-description of (F)
is the mirror image: `G' = (Fnon − U' − ↑X_0 − ∪_{y_i ∈ B} (↑y_i − [y_i])) ∪ (B ∩ U')`, `G' ∩ Up = ∅`, `B ⊆ G'`,
`D = ↓G'` picks `P`.
*Algorithm and time.* GDESC tries both kinds, every set of at most `k` tool switches with every flag pattern, every
anchor set of size at most `|X_0| + |Y_0|` and every flip set of size at most `9k` inside `U` (resp. `U'`), and tests
connectivity. It is sound, and by the above it accepts. ∎

**Corollary 6.5' (fractional form; proved).** Call *cheap tools* of `P`: for kind E the stars `E#_w` (`w ∉ L`, cost
`<= 9` flips), with the strict anchor at `w` when `w ∈ A` (free), and the F-anchors `↓z` (`z ∉ Up`, free);
dually for kind F. If the needed items of one kind have LP cover number `<= τ` by its cheap tools, then a cover by
`<= ⌈τ ln m⌉ + 1` cheap tools exists (rounding of the LP; Lovász), hence GDESC with that many tools, anchors and
`9` flips per star accepts. By the proof of Theorem 6.5 the smaller of the two LP cover numbers is at most
`2 + κ`; it can be much smaller (a large matching of bad pairs has `κ` large but costs nothing in the game).
*Proof.* LP duality gives the first claim through the greedy bound `H(|N|) τ`; the second: the duality on
`(N_F − X_0) × (N_E − Y_0)` gives, by the argument of Theorem 6.5, a fractional cover of value `<= 2` of one of the
two reduced sets by stars, and the anchors at `X_0` or `Y_0` add `|X_0|` or `|Y_0|`. ∎

## 7. Corrections of §1-§5 (from `verify/rv-core.md`, 2026-10-23)

The review `verify/rv-core.md` (complete for §1-§5; the partial review `verify/r6-review.md` agrees) found one false
statement, one gap and four wording repairs. §1-§6 are left as they are; what holds is stated here.

| Place | Verdict of the review | What holds |
|---|---|---|
| §0, row D | wording | plain HYB rejects `Y^d_k` and `Y'^d_k`; the *refined* search rejects only `Y'^d_k` (it accepts `Y^d_k` with one dominator `N_F[h_q]`), as Proposition D (iv) itself says |
| Prop. D (iii) | holds with repair | for `gsw.refutes` (each terminal walked with its own copy of the assignment) as written: `x_2k` fixed (variant without back) or nothing (back). With one assignment shared by the two walks (a reading r4-general §7.3 allows) the back variant also gets `x_2k` fixed. In every reading at most one switch (`x_2k`) is fixed and all mates and `d` stay free; (iv) does not depend on this |
| §3.3 CF (iv) | holds as a check | `Z_k`, `Z^B_k` (`k <= 4`): one centre, no flip connects (checked, `verify/rv-core/runs/cf-z-direct-2-4.txt`); no proof is given, so the label is **checked**, not proved. The log `runs/cdesc-fam-4.txt` gives Lemma-G cost 1 for `Z_4` (the description connects anyway), and `decide(1, 1)` was not run on the `Z` instances |
| §5.1 guided cost with anchors | holds with repair | needs `A_0 ∩ L = ∅` (e.g. `A_0 ⊆ A`) and `↓B_0 ∩ Up = ∅` (e.g. `B_0 ⊆ W_F`) |
| §5.2 (E1), (F1) | holds | `B_0 = B` works for every valid path (shortestness not needed); the interval hypothesis only bounds `|B| <= 5` |
| §5.2 (E2), (F2) as written | **false** | see 7.1 |
| §5.2 (E2), (F2) with uncontracted centres | holds with repair | see 7.1 |
| §5.2 "TCA(c) ⇒ ADESC(5, 2, c)" | gap | holds when ADESC also enumerates the centres `Ẑ(b)`, `Ẑ'(a)` of 7.1 (at most `2m` extra centre sets); with ADESC as defined in §5.1 it is proved only in 2CH |
| Prop. 5.2' | holds with repair | needs `B_0 ⊆ L` (e.g. `B_0 ⊆ B`; then `↓B_0 ⊆ L` misses `Up`) and `A_1 ⊆ A`; with arbitrary `B_0` it fails |

### 7.1 Theorem 5.2 (E2), (F2): the counterexample and the repair

*Why (E2) as written fails.* The proof shows `out = ∅` correctly (the core argument holds), but the flip step uses
the centres `E_{b_1}`, `E_{b_2}` *in the instance with `F_v`, `v ∈ ↓B_0`, contracted*: all nodes of all these `F_v`
(including `b_1`, `b_2`, their ties and everything below the other anchor) become one node, so a minimal E-member
whose path side meets any of them lies in `U` without lying in `f*_A(b_1) ∪ f*_A(b_2)`; it is then neither a
generator nor flipped in.
*Counterexample* (`verify/rv-core/cex_e2.py`, checked): `R((EF)^4)` in 2CH form (8 switches, unique solution, unique
valid path `h_1 .. h_8`) plus one node `κ ∈ E(x_2) ∩ F(x_2)`; `b_1 = x_2`, `b_2 = x_8` (distance 6),
`Φ = f*_A(x_2) ∪ f*_A(x_8) = {x_3, x_5, x_7}`. Contracted, `F(x_2) = h_2` is one node lying in `E(x_2)` (through `κ`)
and in `E(x_1) = h_1` (through `y_1`), so `x_1 ∈ U − Φ`, `D = {x_1, x_2, x_4, x_6, x_8}`, and `s` (only in `h_1`) is
isolated. Random general instances: 36 of 4385 E2 pairs and 46 of 4385 F2 pairs fail as written.
*Repair (R2), keeps the constant `c`.* For `b ∈ B_0` take the uncontracted centre
`Ẑ(b) = E_b ∪ ⋃{F_v : v < b, F_v ∩ E_b ≠ ∅}` and `U = NE(Ẑ(b_1)) ∪ NE(Ẑ(b_2))`. Case (i) of the proof gives
`y ∈ U`; in case (ii) `w < b_i` and `F_w` contains the private node of `w b_i ∈ E_{b_i}`, so `F_w ⊆ Ẑ(b_i)` and the
private node of `w y` puts `y` into `U`; the rest of the argument for `out = ∅` is unchanged. Moreover `a ∈ A` lies in
`NE(Ẑ(b_i))` iff `X_a` meets `E_{b_i}` or such an `F_v`, i.e. iff `a ∈ f*_A(b_i)`; so `A ∩ U = Φ`, `G` contains `A`,
misses `L`, and the description picks `P`. Dually `Ẑ'(a) = F_a ∪ ⋃{E_v : v > a, E_v ∩ F_a ≠ ∅}` for (F2). Checked
(rv-core): no failure in 8770 random pairs, and `A ∩ U = f*` in all of them.
*Repair (R1).* Keep the contracted centres and flip `Φ = A ∩ U`: correct, but the number of flips is not bounded by
`|f*|`.
*Wording.* "Without middle edges `f*_A(b) = f_A(b)`" is wrong (a node of `F_v ∩ E_b`, `v < b`, needs no middle
edge). Without middle edges case (ii) does not occur, so the uncontracted centres `E_{b_1}`, `E_{b_2}` with
`Φ = f_A(b_1) ∪ f_A(b_2)` suffice (checked, 2479 pairs).

### 7.2 What §6 uses from §1-§5

Theorem 6.5 and Corollary 6.5' use from §5 only Proposition 5.2' (strict anchors at `x ∈ A`, F-anchors `Y_0 ⊆ N_E ⊆ L`):
both hypotheses of the repaired 5.2' (`A_1 ⊆ A`, `B_0 ⊆ L`) hold there, so §6 is not affected by the corrections.
Theorem 5.2 enters §8 below only in the repaired form (R2).

## 8. The bad pairs (round 5 plan of 2026-10-23; results of round 6, 2026-10-27)

Task of the coordinator: for a shortest valid path, bound the cost of the bad pairs of Theorem 6.5 (vertex cover or
fractional cover by cheap tools), or handle them by other tools, or find a family in which they are expensive for
every description of this kind on every shortest valid path.

Round 6 (2026-10-27, workflow run `wf_138deda4-8fb`): §8.2 onward. Scripts `r5-core/` (new files listed in §10),
logs `r5-core/runs/`.

### 8.0 Results of §8

| # | Statement | Status |
|---|---|---|
| 8.1 | *One level* (Lemma 8.1): for every non-empty residue `A' ⊆ A` some GDESC term (at most `k = ⌊log2 m⌋ + 1` tools, pivots allowed, at most `9k` flips) contains `L` and either misses `↑A'` or leaves at most `|A'|/2` elements of `A'` uncovered; an F-term may need up to `⌈2k ln m⌉` E-anchors | proved (§8.2) |
| 8.2 | **Intersections of descriptions remove the bad pairs.** Every yes-instance of ZZ + P2 (general switch form, `m` switches) has a connecting down-set `D_1 ∩ .. ∩ D_j`, `j <= k`, each `D_i` a GDESC term with at most `k` tools and `9k` flips; only the last term may have anchors (at most `⌈2k ln m⌉` E-anchors) | proved (§8.2) |
| 8.3 | **ZZ + P2 is decided in time `m^{O(log^2 m)}`** (IDESC: intersections of GDESC terms). Hence the open case of DC is in quasi-polynomial time and is **not NP-complete unless NP ⊆ QP** (not under ETH). Uses only Lemmas 6.2-6.4 of §6, not Theorem 6.5 | proved (§8.3); Lemmas 6.2-6.4 reviewed: hold (`verify/rv-core-65.md`); §8 itself not yet reviewed |
| 8.4 | Every claim of the proof checked by `inter.levels` on 5199 + 190 + 1106 + 333 + 178 shortest valid paths (random instances, all known families, designs with up to 516 bad pairs per 40 instances and `κ <= 7`, rigid-word designs with 2 levels); no failure. On 23 designs without a single term of the proof's kind, one GDESC term with one tool (a partner star) still accepts | checked (§8.4) |

### 8.1 Plan

(1) Pivots: the E-tool of `x ∈ N_F` gets the exclusion set `↓x − [x]`; then the duality holds for *every* pair, and
the only price is the *damage* (minimal E-members strictly below a pivot). (2) Bound or remove the damage: choice of
`P`, intersections and unions of descriptions, window lemmas. (3) Computations: exact solvers on exhaustive small
instances and on adversarial instances with many bad pairs.
Outcome: (2) is done by intersections (§8.2): the damage of one description is repaired by the next one, which only
has to exclude the damaged minimal E-members; light pivots (damage at most `|A'|/(2k)`) halve the residue, heavy
pivots are replaced by E-anchors on the F-side.

### 8.2 Intersections of terms (Lemma 8.1, Theorem 8.2; proved)

Notation of §6.1: a shortest valid path `P`, `W_E`, `W_F`, `Up = ↑W_E`, `L = ↓W_F`, `A` (minimal E-members), `B`
(maximal F-members), `N_E = {y ∈ L : E_y ≠ ∅}`, `Enon`, `Fnon`, stars `E#_x`, `F#_y` (§6.3), `NE(Z)`, `NF(Z)` (§3.1).
`m` = number of switches, `k = ⌊log2 m⌋ + 1` (so `2^k > m`), `N = ⌈2k ln m⌉`.

**Terms.** An *E-term* `τ = (E; T, T', Y_0, Φ)` (tools `T`, flagged tools `T' ⊆ T`, F-anchors `Y_0`, flips `Φ`):

    U = ∪_{x ∈ T} NE(E#_x),   S = ↓Y_0 ∪ ∪_{x ∈ T'} (↓x − [x]),   G = (Enon − U − S) ∪ Φ,   D(τ) = Q − ↑G.

An *F-term* `τ = (F; T, T', X_0, Φ)` (E-anchors `X_0`):

    U' = ∪_{y ∈ T} NF(F#_y),  S' = ↑X_0 ∪ ∪_{y ∈ T'} (↑y − [y]),  G' = (Fnon − U' − S') ∪ Φ,  D(τ) = ↓G'.

These are exactly the descriptions of GDESC (§6.1, `gdesc.describe`); a flag on a tool `x` is the *pivot* `↓x − [x]`
(on any switch, not only on minimal E-members). `D(τ)` is a down-set for every term.
For a set `A' ⊆ A` (a *residue*) and a switch `x` the *damage* of `x` is `dam(x) = A' ∩ (↓x − [x])`.

Facts used (all for the fixed shortest valid path `P`):
- (F0) A down-set `D` picks every member of `P` iff `L ⊆ D` and `D ∩ Up = ∅` (§6.1); then `D` connects `s` and `t`.
  `Up = ↑A`: every E-member lies above an element of `A` (the preorder is finite).
- (F1) Lemma 6.3: `|A ∩ NE(E#_x)| <= 9` for every `x ∉ L`; `|B ∩ NF(F#_y)| <= 9` for every `y ∉ Up`.
- (F2) Lemma 6.4: for `x ∈ Up` with `F_x ≠ ∅` and `y ∈ N_E` incomparable, `y ∈ NE(E#_x)` or `x ∈ NF(F#_y)`.
- (F3) No element of `A` lies strictly below an element of `A` (definition of `A`). No element of `L` lies strictly
  above an element of `B` (`w > b`, `w <= b'` with `b' ∈ B` gives `b < b'`, against the maximality of `b`). For
  `a ∈ A`, `↑a ⊆ Up` misses `L`.
- (F4) If `V` is an up-set and `G' ∩ V = ∅`, then `↓G' ∩ V = ∅`; if `W` is a down-set and `G ∩ W = ∅`, then
  `↑G ∩ W = ∅`.

**Lemma 8.1 (one level).** Let `A' ⊆ A` be non-empty. There is a term `τ` with `L ⊆ D(τ)`, at most `k` tools and
at most `9k` flips, such that
- (final) `D(τ) ∩ ↑A' = ∅`, and `τ` is an E-term without anchors or an F-term with at most `N` E-anchors; or
- (continue) `τ` is an E-term without anchors and `D(τ) ∩ ↑A' ⊆ ↑A''` for a set `A'' ⊆ A'` with
  `1 <= |A''| <= |A'|/2`.

*Proof.* Let `R = ↑A' ∩ Fnon` (rows), `C = N_E` (columns), `θ = |A'|/(2k)`; a row `x` is *light* if
`|dam(x)| <= θ`, *heavy* otherwise. Every element of `A'` is light (`dam(a) = ∅` by F3). For `x ∈ R` and `y ∈ C` put

    cov_E(x) = (NE(E#_x) ∪ (↓x − [x] if x is light)) ∩ C,
    cov_F(y) = (NF(F#_y) ∪ (↑y − [y] if y ∈ B)) ∩ R.

*Claim (duality).* For every light `x ∈ R` and every `y ∈ C`: `y ∈ cov_E(x)` or `x ∈ cov_F(y)`. Indeed `x ∈ Up` and
`y ∈ L`, so `x <= y` is impossible (it puts `x` into the down-set `L`); if `y < x`, then `y ∈ ↓x − [x]`, which is
part of `cov_E(x)` for light `x`; if `x ∥ y`, F2 applies (`x ∈ Up`, `F_x ≠ ∅`).

*Trivial cases.* If `C = ∅`, the E-term with no tool, no anchor, no flip has `G = Enon`: `G ∩ L = N_E = ∅`, so
`L ⊆ D` (F4), and `A' ⊆ Enon = G` (E-members have non-empty E-sides), so `D ∩ ↑A' = ∅`: final. If `R = ∅`, the
F-term with nothing has `G' = Fnon`: `G' ∩ ↑A' = R = ∅`, so `D ∩ ↑A' = ∅` (F4), and `B ⊆ Fnon = G'`, so
`L = ↓B ⊆ D`: final.

Otherwise let `v` be the value of the zero-sum game with rows `R`, columns `C` and payoff `M(x, y) = 1` if
`y ∈ cov_E(x)`, else `0` (row player maximises).

*Case `v >= 1/2`.* Some distribution `p` on `R` has `Σ_x p(x) M(x, y) >= 1/2` for every `y ∈ C`. For `x_1, .., x_k`
drawn independently from `p`, a fixed `y` lies in no `cov_E(x_i)` with probability at most `2^{-k} < 1/m <= 1/|C|`;
so some `x_1, .., x_k ∈ R` have `C ⊆ ∪_i cov_E(x_i)`. Take the E-term with `T = {x_i}`, `T'` = the light `x_i`,
`Y_0 = ∅`, `Φ = A' ∩ U`.
- `L ⊆ D(τ)`: every `y ∈ N_E` lies in `U` or in a pivot `↓x_i − [x_i] ⊆ S` (light `x_i`), so `y ∉ Enon − U − S`;
  `Φ ⊆ A' ⊆ Up` misses `L`; elements of `L − N_E` are not in `Enon`. So `G ∩ L = ∅`, and F4 gives `L ⊆ D(τ)`.
- Flips: `x_i ∈ Up`, so `x_i ∉ L`, and F1 gives `|Φ| <= Σ_i |A ∩ NE(E#_{x_i})| <= 9k`.
- Damage: let `A'' = A' − G`. An `a ∈ A'` outside `U ∪ S` lies in `Enon − U − S ⊆ G` (`E_a = X_a ≠ ∅`); an
  `a ∈ A' ∩ U` lies in `Φ ⊆ G`. Hence `A'' ⊆ (A' ∩ S) − U`. `S` is the union of the pivots of the light `x_i`, so
  `A' ∩ S ⊆ ∪_i dam(x_i)` and `|A''| <= kθ = |A'|/2`. Every `w ∈ ↑A' − ↑A''` lies above some `a ∈ A' ∩ G`, so
  `w ∈ ↑G` and `w ∉ D(τ)`: `D(τ) ∩ ↑A' ⊆ ↑A''`. If `A'' = ∅` this is the final case, otherwise the continue case.

*Case `v < 1/2`.* Some distribution `q` on `C` has `Σ_y q(y) M(x, y) < 1/2` for every `x ∈ R`. By the claim,
`Σ_y q(y) [x ∈ cov_F(y)] > 1/2` for every light `x ∈ R`. Draw `y_1, .., y_k` independently from `q`, and
`a_1, .., a_N` independently and uniformly from `A'`. A light row lies in no `cov_F(y_i)` with probability
`< 2^{-k} < 1/m`. A heavy row `x` has `|dam(x)| > θ`, so `Pr[a_j < x] > θ/|A'| = 1/(2k)` and `x` lies above no
`a_j` with probability `< (1 − 1/(2k))^N <= e^{-N/(2k)} <= 1/m`. As `|R| <= m`, the union bound gives a choice in
which every light row lies in some `cov_F(y_i)` and every heavy row lies strictly above some `a_j`. Take the F-term
with `T = {y_i}`, `T' = T ∩ B`, `X_0 = {a_j}` (at most `N` E-anchors, all in `A'`), `Φ = B ∩ U'`.
- `D(τ) ∩ ↑A' = ∅`: an element `x ∈ ↑A' ∩ G'` is not in `Φ ⊆ B ⊆ L` (`x ∈ Up`), so `x ∈ Fnon − U' − S'`, so
  `x ∈ R`. If `x` is light, `x ∈ NF(F#_{y_i}) ⊆ U'` or `x ∈ ↑y_i − [y_i] ⊆ S'` for some `i` (`y_i ∈ B`); if `x` is
  heavy, `x ∈ ↑a_j ⊆ S'`. Either way `x ∉ G'`, a contradiction. So `G' ∩ ↑A' = ∅`, and F4 gives the claim.
- `L ⊆ D(τ)`: every `b ∈ B` lies in `G'`: `b ∈ Fnon` (`F_b = X_b`); if `b ∈ U'`, then `b ∈ Φ`; `b ∉ ↑a_j` (F3);
  `b ∉ ↑y_i − [y_i]` for `y_i ∈ B` (F3). So `L = ↓B ⊆ ↓G' = D(τ)`.
- Flips: `y_i ∈ L`, so `y_i ∉ Up`, and F1 gives `|Φ| <= 9k`. This is the final case. ∎

**Theorem 8.2.** Let a ZZ + P2 instance in general switch form with `m` switches have a valid path. Then there are
terms `τ_1, .., τ_j`, `j <= k`, each with at most `k` tools and at most `9k` flips, all without anchors except
possibly `τ_j`, which is then an F-term with at most `N` E-anchors, such that `D(τ_1) ∩ .. ∩ D(τ_j)` connects `s`
and `t`.

*Proof.* A valid path exists, hence a shortest one, `P`; if `A = ∅` (no E-member), the trivial F-term of the proof of
Lemma 8.1 with `A' = ∅` (`G' = Fnon`, so `L ⊆ D`, and `Up = ∅`) picks `P`; so let `A ≠ ∅`. Put `A^(1) = A` and apply
Lemma 8.1 to `A^(i)` for `i = 1, 2, ..` as long as the continue case occurs, with `A^(i+1) = A''`. Since
`1 <= |A^(i+1)| <= |A^(i)|/2` and `|A| <= m`, the continue case occurs at most `⌊log2 m⌋` times, so the process
stops at some `j <= k` with a final term. Let `D = D(τ_1) ∩ .. ∩ D(τ_j)`, a down-set. `L ⊆ D(τ_i)` for every `i`,
so `L ⊆ D`. By induction `D(τ_1) ∩ .. ∩ D(τ_i) ∩ Up ⊆ ↑A^(i+1)` for `i < j` (`Up = ↑A^(1)` by F0, and each level
gives `D(τ_i) ∩ ↑A^(i) ⊆ ↑A^(i+1)`), and the final term gives `D(τ_j) ∩ ↑A^(j) = ∅`; so `D ∩ Up = ∅`. By F0, `D`
picks every member of `P` and connects `s` and `t`. ∎

Remarks. (1) Nothing about the bad pairs is assumed: a bad pair `(x, y)` (`y < x`) is covered by the pivot of `x` when
`x` is light, and a heavy `x` is covered on the F-side by an E-anchor at one of the many elements of `A'` below it.
The damage of the pivots (the minimal E-members that the pivots push into F-mode) is repaired by the next term,
which only has to keep the damaged minimal E-members in E-mode. (2) In 2CH with classes there are no comparable pairs,
every row is light with empty damage, and one level suffices: this is Theorem Q again (with 9 for 3 because of the
stars). (3) The `log^2` comes from `log m` levels of `log m` tools each (and from the `O(log^2 m)` anchors); the
proof uses several levels when the pivots damage minimal E-members (example in §8.4). Whether some instance needs more
than one term is open (§8.5, item 5); on the example of §8.4 a single term with one tool already connects.

### 8.3 The algorithm IDESC and the consequence for DC (proved)

**IDESC(j, k, a, e)**: for every sequence of at most `j` terms (both kinds, at most `k` tools with every flag pattern,
anchors as in §6.1, flips drawn from the switches caught by the centres, at most `e` flips per term, at most `a`
anchors in total), test whether `D(τ_1) ∩ .. ∩ D(τ_j)` connects `s` and `t`; accept iff some test succeeds.
*Soundness:* every tested set is an intersection of down-sets, hence a down-set (an order-consistent mode vector);
an accepted one connects `s` and `t`. *Completeness:* by Theorem 8.2, IDESC(`k`, `k`, `N`, `9k`) accepts every
yes-instance (the flips of Lemma 8.1 lie in `U`, resp. `U'`, so they are among the caught switches).
*Time:* at most `2 · m^k · 2^k · m^{9k}` anchor-free terms and `m^{N}` times as many anchored ones; at most
`(2^{k+1} m^{10k})^k · m^N` sequences, each tested in `O(m (n_N + m))` (`n_N` nodes). With `k = O(log m)`,
`N = O(log^2 m)` this is `m^{O(log^2 m)} = 2^{O(log^3 m)}` times a polynomial.

**Corollary 8.3.** ZZ + P2 is decidable in quasi-polynomial time `2^{O(log^3 n)}`. By the polynomial equivalence of
the open case of DC with ZZ + P2 (`theory-dc.md` Theorem 13, reviewed in `verify/equivalence.md`), deciding
`cp(u, v) = c(u, v)` for pairs with `d(u, v) = 2`, `c(u, v) >= 3` in graphs of DC is in quasi-polynomial time. Hence
it is **not NP-complete unless NP ⊆ QP** (= `DTIME(2^{polylog n})`); in particular not under the Exponential Time
Hypothesis. *Proof.* A polynomial reduction from 3-SAT followed by IDESC decides 3-SAT in time `2^{O(log^3 n)}`. ∎

Dependencies: Lemmas 6.2, 6.3, 6.4 (§6.2, §6.3) and the model of `r4-general.md` §5.1; not Theorem 6.5, not
Corollary 6.5', not §5. Lemma 6.3 needs `P` shortest; Lemma 6.4 needs P2 in switch form (node or middle witnesses).

### 8.4 Computations (checked)

`inter.levels(G, P)` runs the proof of Theorem 8.2 on a shortest valid path and checks every claim: the duality
claim for every light row and every column, cover sizes `<= k`, anchors `<= N`, flips `<= 9` per tool, damage
`<= |A'|/2`, every term contains `L`, `D(τ) ∩ ↑A' ⊆ ↑A''`, the F-term misses `↑A'`, final `D` picks `P` and connects,
levels `<= k`. Modes: *ilp* (least covers by ILP), *sample* (covers drawn as in the proof, `k` draws from the optimal
row or column strategy of the game, anchors uniform from `A'`, every light tool pivoted), *kth=1* (sample mode with
the light threshold `|A'|/2`; exercises the recursion on small instances; only the logical claims are checked there,
not the bounds). Generators: `gcert.random_inst` and `mixed.random_instance` (as in `test_gstar.py`); `badgen.design`
(planted path, switches `x_i` above sets of E-members and `y_j` below sets of F-members with `y_j < x_i`, random P2
completion by nodes and middle witnesses); `rgen.rdesign` (the rigid word `R(W)` of `r4-general.md` §6 with such
`x_i`, `y_j`, P2 by nodes in dead sides, lower/upper middle witnesses, contacts; sets `S_i`, `T_j` random or lines of
the projective planes of order 2 and 3).

| Script and arguments | Instances | Outcome | Log |
|---|---|---|---|
| `test_inter.py random 11 500 10 18 20` (also seeds 12, 13) | 1500 random, 1229 yes, 5199 shortest paths (716 with bad pairs, `κ <= 4`) | no error; always 1 level (`|A| < 2k`, so every non-zero damage is heavy); cases E 2784, F 138 | `runs/inter-random-1{1,2,3}-10-18.txt` |
| `test_inter.py families 5` | `Y_k`, `Y'_k`, `Y^d_k`, `Y'^d_k` (`k <= 5`, both variants), `X_L` (`L <= 10`), `Z_k`, `Z^B_k` (`k <= 5`), `W_n` (`n <= 3`, pairings E, F), `OB` (2 sizes); 190 shortest paths | no error; 1 level | `runs/inter-families-5.txt` |
| `test_bad.py 1 40 6`, `test_bad.py 2 40 6` | 80 designs, 162 paths, up to 516 bad pairs per 40, `κ <= 5` | no error (ilp and sample) | session record |
| `test_rgen.py 1 10 4 7` | 10 rigid-word designs, 19 paths, `|A| <= 8` | no error; kth=1 reaches 3 levels with damage 3 | session record |
| `test_rgen.py 2 6 12 13` | 6 designs, `m` 31-38, `|A| <= 15`, 10 paths, `κ <= 6` | no error; **2 levels** in ilp and sample modes (damage 2), kth=1 up to 3 levels | session record |
| `test_rgen.py S 60 9 14`, `S = 3, 4, 5` | 180 rigid-word designs (`(EF)^n` or random words, `n` 9-14, 14 with projective-plane sets), all yes; 333 shortest paths (the planted one when shortest: 102 times), `|A| <= 15`, `κ <= 7` | no error in any mode; ilp: 36 paths with 2 levels (damage `<= 2`, anchors `<= 5`); sample: 36 paths with 2 levels (anchors `<= 14 <= N`); kth=1: up to 4 levels, damage `<= 6`. On 31 of the 333 paths no single term of the proof's kind (one level, residue `A`) exists (`inter.min_single`) | `runs/rgen-{3,4,5}-9-14.txt` |
| `test_rgen.py S 80 12 16`, `S = 6, 7` | 160 rigid-word designs (16 with projective-plane sets), all yes, 283 shortest paths, `|A| <= 20`, `κ <= 7` | no error in any mode; 55 paths with 2 levels (ilp and sample; anchors `<= 19`), kth=1 up to 3 levels with damage up to 10 | `runs/rgen-{6,7}-12-16.txt` |
| `enum_inter.py 3` | **all** 7232 ZZ instances with 3 middle elements (own enumerator, `gcert.Inst` -> `gcore.from_inst`): 5830 P2, 1584 yes, 4246 no, 1896 shortest paths (the counts of `verify/rv-core-65.md` §3.1) | no error; BFS = brute force on yes/no; 1 level; cases E 666, F 12, C0 744, R0 474 | `runs/enum-inter-3.txt` |
| `test_bad.py 7 400 8` | 400 designs, 944 paths, 5694 bad pairs, `κ <= 6` | no error (ilp and sample); 1 level | `runs/bad-7-400.txt` |
| `test_multi.py 8 60 10 14 4` | 60 designs, 178 paths (P2 completion shortens the planted path: `|A| <= 3`) | no error; kth=1 up to 2 levels | `runs/multi-8-60.txt` |

The independent review `verify/rv-core-65.md` (2026-10-27) finds Lemmas 6.2, 6.3, 6.4 **hold** (Lemma 6.3 even with 5
consecutive positions, so `9k` can be read `5k` throughout §8), and the switch-form model equal to ZZ on all
instances with at most 4 middle elements; it notes that §8 is outside its scope.

*A run of the proof with two levels* (`show_levels.py 3 60 9 14 runs/two-levels-example.json`, instance saved
there): rigid word `(EF)^10` with 7 extra switches, `m = 27`, `k = 5`, `N = 33`, the planted path (20 members,
`|A| = |B| = 10`), 12 bad pairs, `κ = 3`. Level 1: rows 14 (2 heavy), columns 13, game value 1, one tool whose pivot
covers all 13 columns and damages one minimal E-member (`1 <= θ = 1`); level 2: residue of size 1, rows 3 (the
up-set of the damaged member), game value 0, F-case with one star and one E-anchor. The intersection of the two
terms picks the path and connects `s`, `t`. On the same instance a single GDESC term also connects (`gdesc.decide(G, 1, 0, 0)`
accepts; `decide(G, 1, 1, 2)` finds the E-star of the 16th member, an F-member, with two flips).

*Single terms.* `hunt_single.py 21 80 8 12`, `hunt_single.py 22 80 8 12` (logs `runs/hunt-single-2{1,2}.txt`,
instances `runs/single/single-*.json`): among 160 rigid-word designs (all yes), 23 have no shortest valid path with a
single term of the proof's kind (`inter.min_single`); on all 23 the exhaustive single-term search
`gdesc.decide(G, 1, 1, 2)` accepts, every time with the E-star of an F-member near the end of the rigid word (whose
partner meets only the last two or three E-members) and two flips. So on these instances the extra levels are an
artefact of the proof's restricted tool set (only stars of `P`-consistent sides), not a need of the instance. No
instance was found on which every single GDESC term with one tool, one anchor and two flips fails.

### 8.5 What remains and what changes (2026-10-27)

1. **Review** of Lemma 8.1, Theorem 8.2 and Corollary 8.3 by an independent agent (the proof is two pages and uses
   only Lemmas 6.2-6.4, reviewed in `verify/rv-core-65.md`, and the switch model of `r4-general.md` §5.1).
2. **The chain for the quasi-polynomial bound is short:** open case of DC ⇔ ZZ + P2 (`theory-dc.md` Theorem 13) →
   general switch form (`r4-general.md` §5.1, conversion `gsw.GSW`) → Theorem 8.2. Forced-mode propagation, Theorem R,
   the switch model 2CH, Theorem Q and Theorem 6.5 are **not needed** for it (they remain as the polynomial results
   for their subclasses: 2CH + P2 in P, r4-switch Theorem 10).
3. **Hardness** (agent r5-hard): by Corollary 8.3 an NP-hardness proof of the open case would give NP ⊆ QP; the
   bad pairs cannot carry a reduction (the families `BP_n` of `r5-hard.md`, with `K_{n,n}` of bad pairs, are
   accepted by a single GDESC term, `r5-hard.md` §3.1).
4. **Polynomial bound** (open): the `log^2` comes from `log m` levels of `log m` tools and from `O(log^2 m)` anchors.
   A bound `m^{O(log m)}` would need one level with `O(log m)` anchors; a polynomial bound would need a bounded number
   of tools, which the minimax argument cannot give (`r5-classes.md` §2b, remark 2). On every instance computed, one
   GDESC term with at most two tools sufficed (§8.4).
5. **Lower bound for single terms** (open, not needed for the QP result): a family on which every single GDESC term
   with `O(1)` tools fails while an intersection of two or three terms succeeds; the candidate (projective-plane sets
   `S_i`, `T_j`, all `y_j < x_i`) needs member pairs without cheap partners, which the rigid words do not have (§8.4).

## 9. Computations of version 0.2 (record)

## 10. Scripts (`r5-core/`)

| Script | What |
|---|---|
| `gcore.py`, `test_gcore.py` | library and exact routines (§1) |
| `fool.py`, `test_fool.py`, `test_fool2.py` | families `Y^d_k`, `Y'^d_k` against HYB (§2) |
| `cdesc.py`, `test_cdesc.py` | CDESC: closure descriptions, guided costs, exact enumeration (§3) |
| `wfam.py`, `test_wfam.py` | family `W_n` (§4.1) |
| `gplant.py`, `obfam.py`, `test_ob.py` | planted paths in general switch form; family `OB` (§4.2) |
| `adesc.py` | ADESC: anchored descriptions, guided costs, exact enumeration (§5) |
| `tca.py`, `test_tca.py` | the TCA statistic of Theorem 5.2 on random 2CH, general and family instances (§5.3, §9) |
| `gstar.py`, `gdesc.py`, `test_gstar.py` | stars, pair classes, cheap tools, GDESC (§6) |
| `inter.py` | §8: the proof of Lemma 8.1 / Theorem 8.2 as a program (`levels`: game value by LP, covers by ILP or by sampling as in the proof, every claim checked); `min_single` (one level of the proof's kind) |
| `test_inter.py` | §8.4: Theorem 8.2 on random instances (`random`) and on the families Y, Y', Y^d, Y'^d, X, Z, Z^B, W, OB (`families`) |
| `badgen.py`, `test_bad.py`, `test_multi.py` | §8.4: random designs with many bad pairs (`x_i` above sets of E-members, `y_j` below sets of F-members, `y_j < x_i`), random P2 completion; projective planes of order 2, 3 |
| `rgen.py`, `test_rgen.py` | §8.4: the same on the rigid words `R(W)` (long shortest paths, `|A| >= 2k`, several levels) |
| `hunt_single.py` | §8.4: designs on which no single term of the proof's kind exists; exhaustive single-term GDESC and pairs of one-tool terms on them; JSON save/load of instances |
| `show_levels.py` | §8.4: prints a run of the proof with two levels |
