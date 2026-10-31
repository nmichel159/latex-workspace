# Review rv-r6-chain: the chain from graphs of DC to the quasi-polynomial bound (round 6b, 2026-10-27)

Status: **final for the verdicts and for every verdict-bearing run** (2026-10-28; started 2026-10-27 17:05, resumed
18:20; records completed in round 6c, no new mathematics). All verdicts of §0 stand; every run named in §2.2 finished
with 0 errors **except two supplementary runs, `rgen 41 30` and `rgen 41 60`, which were cut off** (header line only,
no summary; one record, no error; see §2.2). No verdict depends on them. Agent rv-r6-chain, independent reviewer.
Scripts: `verify/rv-r6-chain/` (own code; other folders imported read-only only as instance generators and, where
named, as cross-checks), logs `verify/rv-r6-chain/runs/`.
Labels: proved, checked, sketch, conjecture, refuted; verdicts: holds, holds with repair, gap, false.

Claim under review (`r5-core.md` §8.3, §8.5 item 2): deciding `cp(u,v) = c(u,v)` for pairs with `d(u,v) = 2`,
`c(u,v) >= 3` in graphs of DC is in time `2^{O(log^3 n)}`, hence not NP-complete unless NP ⊆ QP, and not NP-hard
under ETH, through the chain: open case of DC -> ZZ + P2 (`theory-dc.md` Theorem 13) -> general switch form
(`r4-general.md` §5.1, `gsw.GSW`) -> Theorem 8.2 of `r5-core.md`.

Texts reviewed (SHA-256 at the start of this session):
- `r5-core.md` `d96d9e9e530874f5e193c9857a8a541706114443acd6e0251d605f8784ec8771` (§6.1-§6.3, §8.0-§8.5)
- `theory-dc.md` `e5b69bd323328059473a775be4cb270fa38fa176a51dfd7c56571076c315ad58` (§1, §2, Theorem 13)
- `r4-general.md` `cd1390621510f6cd9b454543c51adb9053fd3942fe35f5c0de39da1e60b07158` (§5.1)
- `r4-general/gsw.py` `875265eebcfef8b9a7e3ecdeb84333d687757a3afc32aa8808b16e55caf25b2c` (class `GSW`)
- `verify/equivalence.md` (review of Theorem 13, read as the record of what was re-checked there)

## 0. Verdicts

Final. The runs that were still in progress when the verdicts were written are recorded in §2.2 (all finished except
the two supplementary `rgen` runs); no log contradicts a verdict.

| Link | Verdict | Note |
|---|---|---|
| L1 Theorem 13, direction used | **holds** | Only 13(a) (graph -> ZZ + P2) is used; it is polynomial (`O(n)` capped flows, one flow, `n` closures), `|Q| <= n`, `|R| <= |E|`, so `m <= n − 2` switches and at most `n + |E|` nodes; DC is used only for P2 (§1.1). Checked: own Theorem 13(a) on 127,000+ open-case pairs (exhaustive up to 8 vertices, random graphs, realised ZZ + P2 instances up to 3876 vertices): answers equal to graph brute force, P2 on all, round trip 13(a) of 13(b) exact (§2.2) |
| L2 ZZ + P2 -> general switch form; P2 as used by Lemmas 6.3, 6.4 | **holds** | P2 of ZZ gives exactly the four witness kinds of switch-form P2 (common E-node, common F-node, lower / upper middle witness), which are the four cases of Lemma 6.4; Lemma 6.3 uses only that a private node lies in `F_z` and `E_v` of its edge and nowhere else (true by construction). Yes/no preserved (proof in §1.2). Checked: own conversion = `gsw.GSW` (up to renaming of nodes) on every instance; switch-form answers = ZZ answers = graph answers; 25 random down-sets per instance lifted to `G`: switch-form connectivity = path in the minimum cut of `G` (§2.2) |
| L3 F0; valid path iff some down-set connects; ties, empty sides | **holds with repair (wording)** | Correct with ties and empty sides (§1.3, checked exhaustively in §2.3). Repair: "yes-instance" = "some down-set connects `s`, `t`" = "`s = t` or a valid path exists"; Theorem 8.2 ("has a valid path") covers only `s != t`, the case `s = t` (example in §2.3: no switch at all) is accepted by IDESC trivially |
| L4 complexity statements | **holds** (given Theorem 8.2) | `QP = DTIME(2^{polylog n})`; IDESC time `m^{O(log^2 m)} poly = 2^{O(log^3 n)}`; NP-hardness under polynomial (many-one or Turing) reductions would put 3-SAT into QP, and 3-SAT in time `2^{O(log^3 n)}` refutes ETH. Wording: "not under ETH" should read "if ETH holds, it is not NP-hard"; the DC promise is decidable in polynomial time, so promise and language versions agree (§1.4) |
| Theorem 8.2 / IDESC, computed end to end | **no counterexample** | The proof of Lemma 8.1 / Theorem 8.2 executed with exact covers on every computed shortest valid path (every claim checked) and the final intersection lifted to a minimum cut of `G` containing a `u`-`v` path; the blind IDESC(`k, k, N, 9k`) (no path, all terms, all intersections) equals the brute force on all 121588 open-case pairs of graphs with at most 8 vertices and on 1500 realised random instances (§2.2). 0 mismatches in any run |

## 1. Reading of the chain

### 1.1 L1: which direction of Theorem 13 is used, and its size

The algorithmic chain uses only **Theorem 13(a)** (graph -> ZZ + P2): an instance of the open case (a graph
`G ∈ DC` with `n` vertices, a pair `u, v` with `d(u,v) = 2`, `c(u,v) >= 3`) is mapped to a ZZ + P2 instance with the
same answer, and ZZ + P2 is then decided. Theorem 13(b) (ZZ + P2 -> graph) is used only for the remark "every ZZ + P2
instance is realised by a graph of DC" (hardness side) and is not needed for the upper bound.
The map of 13(a), step by step, with its cost:
1. Lemma 1: restrict to the component `K` of `u` in `G` minus its bridges (`O(n + |E|)`); `d`, `c`, the minimum
   `u`-`v` cuts and `cp(u,v)` are unchanged, and `K ∈ DC` (`verify/equivalence.md` §1 adds that `K` is bridgeless).
2. `Q = {u} ∪ {x : c(u,x) >= 3}`: `O(n)` maximum-flow computations capped at value 3.
3. Ears = components of `K − Q` (Lemma 4), multigraph `H` on `Q` with the real edges of `K[Q]` and one ear edge per
   ear with two distinct attachments (Proposition 5): `O(n + |E|)`.
4. One maximum `u`-`v` flow in `H`, its residual graph, and for every `y ∈ Q` the closure `cl({u, y})`: the preorder
   `x <= y` iff every minimum cut containing `y` contains `x` is `x ∈ cl({u,y})` (with `x <= y` for all `x` when
   `v ∈ cl({u,y})`): `O(n (n + |E|))`. `R` = the real edges of `K[Q]` between non-equivalent elements.

Output size: `|Q| <= n` elements, `|R| <= |E(G)|` pairs, the preorder as an `|Q| × |Q|` table. So the ZZ instance has
size polynomial in `n`, and the number of switches `m` of the general switch form (middle elements of `Q`) satisfies
`m <= n − 2`; the number of nodes is at most `|Q| + |R| <= n + n^2`. **The reduction is polynomial and
answer-preserving** (Theorem 13(a) with the repairs of `verify/equivalence.md` §3: minimum cuts of `H` = down-sets
containing `u` and not `v`; `cp = c` iff a consistent zigzag exists; P2 by the repaired Corollary 12). The DC
hypothesis is used exactly once, for P2: incomparable `x, y ∈ Q` have `c(x,y) >= 3`, hence `d_G(x,y) <= 2`; an edge
or a short ear between them would make them comparable (Proposition 11), so they have a common real neighbour `z ∈ Q`,
comparable with both, hence strictly below both or strictly above both.
Verdict on reading: **holds**.

### 1.2 L2: ZZ + P2 -> general switch form; the P2 used by Lemmas 6.3, 6.4

Conversion (`r4-general.md` §5.1, `gsw.GSW.__init__`, read line by line): `B`, `T` = classes of `u`, `v`; nodes =
components of the graph of the `R`-edges between `B` and `T` (union-find), plus one private node per `R`-edge between
two middle elements; `E_w` = nodes of the lower `R`-neighbours of `w` (bottom nodes, private nodes of edges `z w`),
`F_w` = nodes of the upper `R`-neighbours (top nodes, private nodes of edges `w z`); the preorder restricted to the
middle elements; `s`, `t` = nodes of `u`, `v`.

*Yes/no is preserved (proved here).* (i) Down-sets: for a down-set `D'` of `Q` with `u ∈ D' ∌ v`, `D' ⊇ B`,
`D' ∩ T = ∅`, and `D = D' ∩ middle` is a down-set of the middle preorder; conversely for such a `D`, `B ∪ D` is a
down-set of `Q` (an element below a middle element is middle or in `B`; an element of `T` is below no middle element)
that contains `u` and not `v`. (ii) Connectivity: in `G_{D'}` every `B`-`T` edge is active; an edge `b w` (`b ∈ B`,
`w` middle) is active iff `w ∉ D`, i.e. iff `w` picks `E_w`, which contains the node of `b`; an edge `w t'` (`t' ∈ T`)
is active iff `w ∈ D` (picks `F_w`); a middle edge `z w` (`z < w`) is active iff `z ∈ D ∌ w`, i.e. iff its private
node lies in both picked sides `F_z` and `E_w`; a private node lies in exactly two sides (`F_z`, `E_w`), so when only
one of them is picked it is a dead end. Hence `u`, `v` are connected in `G_{D'}` iff `s`, `t` are connected in the
hypergraph of the sides picked by `D`. With (i) the ZZ instance is a yes-instance iff some down-set of the switches
connects `s` and `t`. The code does exactly this (`R` oriented `a < b`; the three branches `a in idx and b in idx`,
`a in idx` (top `b`), `b in idx` (bottom `a`); `B`-`T` edges into the union-find; no other kind of edge exists,
since `R` is strict).

*P2.* In ZZ + P2 an incomparable pair consists of middle elements (elements of `B` or `T` are comparable with
everything). Its common `R`-neighbour `z` strictly below both is either in `B` (then the node of `z` lies in
`E_x ∩ E_y`: a common node) or middle (a *lower middle witness*: edges `z x`, `z y`, private nodes in `F_z ∩ E_x` and
`F_z ∩ E_y`); dually above. These are exactly the four cases of P2 in switch form (`r5-core.md` §6.1) and of the
proof of Lemma 6.4, so the conversion preserves P2 in the form used. (Switch-form P2 is formally weaker: a common node
of `E_x ∩ E_y` may come from two different bottoms in one `B`-`T` component; Lemmas 6.3, 6.4 only need the weaker
form.) Lemma 6.3 uses in addition: the private node of a middle edge `z v` lies in `F_z` and `E_v` and in no other
side (true by construction: one fresh node per edge, put into `F[z]` and `E[v]` only), and `NE(E#_x) = NE(E_x) ∪
Sib↓(x) ∪ {x}` (an E-side containing the private node of `z v` is `E_v`). Lemma 6.4 uses: a lower middle witness `z`
of `x, y` is in `LMN(x)` and the private node of `z y` lies in `E#_x ∩ E_y`; dually. Both are what the conversion
produces. No other property of P2 enters §8 (F2 of §8.2 is Lemma 6.4).
Verdict on reading: **holds** (the computations of §2 compare `GSW` with an own conversion and check P2 on both
sides).

### 1.3 L3: F0 and "valid path exists iff some down-set connects"

*Valid path -> connecting down-set.* Let `P` be valid, `W_E`, `W_F` its E- and F-members, `L = ↓W_F`,
`Up = ↑W_E`. Validity (no `E_w`, `F_z` on `P` with `w <= z`) is `Up ∩ L = ∅` (if `x ∈ Up ∩ L`, then `w <= x <= z`
for members `w ∈ W_E`, `z ∈ W_F`). A down-set `D` picks every F-member iff `W_F ⊆ D` iff `L ⊆ D`, and picks every
E-member iff `W_E ∩ D = ∅` iff `Up ∩ D = ∅` (`D` is a down-set). So `D = L` picks `P`, and every picked walk from
`s` to `t` connects. This is F0. Ties: equivalent `w ≡ z` satisfy `w <= z` and `z <= w`, so `E_w`, `F_z` conflict in
both orders and a tie class is used in one mode only, as a down-set requires; `E_w`, `F_w` conflict (`w <= w`), so a
valid path uses each switch at most once. `Up = ↑A` with `A` the E-members with no E-member strictly below: the strict
order of a finite preorder is well founded.
*Connecting down-set -> valid path.* If the sides picked by a down-set `D` connect `s` and `t`, a shortest walk of
picked sides from `s` to `t` has distinct sides; two picked sides never conflict (`E_w` picked means `w ∉ D`, `F_z`
picked means `z ∈ D`, and `w <= z` would put `w` into `D`). So it is a valid path.
*Empty sides.* A switch with an empty side never has that side on a valid path (a side of a path contains `s` or meets
a neighbour), so `N_E`, `N_F`, `Enon`, `Fnon` only exclude switches that cannot matter; a switch outside `Enon` is put
into F-mode by an E-term unless it lies above an element of `G` (`D = Q − ↑G`), which is harmless because `L` is a
down-set disjoint from `G` (F4).
*Case `s = t`.* If `u` and `v` lie in one node (a `u`-`v` path alternating between the classes of `u` and `v`, which
lies in every minimum cut, so `cp = c`), every down-set connects `s` and `t` but a valid path in the sense "sequence of
`r >= 1` sides with `s ∈ X_1`, `t ∈ X_r`" need not exist (for instance when no side contains `s`). Theorem 8.2 is
stated for instances "with a valid path"; IDESC accepts such an instance anyway (its first test already connects).
**Repair of wording**: "yes-instance" = some down-set connects `s` and `t`; it is equivalent to "`s = t` or a valid
path exists"; Theorem 8.2 covers the second alternative and the first is trivial. `GSW.is_valid_walk` already accepts
the empty walk when `s = t`; `r5-core.md` §1 records the same case for the round trip.
Verdict on reading: **holds with repair** (wording only).

### 1.4 L4: the complexity statements

- `QP = DTIME(2^{polylog n}) = ∪_c DTIME(2^{(log n)^c})`. It is closed under polynomial-time many-one and Turing
  reductions: an instance of size `n` is mapped to instances of size `<= n^a`, and `2^{(log n^a)^c} = 2^{a^c (log n)^c}`.
- IDESC time (§8.3): sequences of at most `k` terms, each fixed by at most `k` tools (`<= m^k`), a flag pattern
  (`2^k`), at most `9k` flips from the caught switches (`<= m^{9k}`) and the kind; anchors in total at most
  `N = ⌈2k ln m⌉` (`<= m^N`); per sequence a polynomial test. Total `(2 · 2^k m^{10k})^k · m^N · poly =
  m^{O(log^2 m)} · poly = 2^{O(log^3 m)} · poly`, and with `m <= n` and the polynomial reduction of L1, deciding the
  open case takes `2^{O(log^3 n)}` time on graphs with `n` vertices (the input length is at least `n`).
- NP-hardness under polynomial reductions: if 3-SAT `<=_p` the open case, a formula of size `s` is decided in time
  `poly(s) + 2^{O(log^3 poly(s))} = 2^{O(log^3 s)}`, so 3-SAT ∈ QP and NP ⊆ QP. The problem is in NP (Lemma 6), so
  "NP-complete" and "NP-hard" coincide here. ETH says that 3-SAT with `n` variables has no `2^{o(n)}` algorithm; a
  3-SAT instance with `n` variables has size `O(n^3 log n)` (distinct clauses), so NP ⊆ QP would give a
  `2^{O(log^3 n)} = 2^{o(n)}` algorithm. Hence: if ETH holds, the open case is not NP-hard (and NP ⊆ QP is itself
  considered unlikely; it would refute ETH).
- What is *not* claimed and should not be read into it: membership in P, or hardness for quasi-polynomial reductions.
Verdict on reading: **holds**, provided Theorem 8.2 holds (reviewed separately in `verify/rv-r6-core.md`; my
computations of §2 test it end to end from graphs).

## 2. Computations

### 2.1 Own code (`verify/rv-r6-chain/`)

- `rvc_lib.py` (own, no foreign import): graphs, max flow (BFS augmenting, integer capacities), residual closures,
  bridges, DC test (classes of `c >= 3` by capped flows, then distance `<= 2` inside each class); three brute forces
  for `cp(u,v) = c(u,v)` from the definition: `brute_subsets` (all vertex sets, `n <= 20`), `brute_core` (all
  vertex sets of the core = vertices of degree `>= 3`, for graphs whose other vertices have degree 2 with both
  neighbours in the core, as in the realised graphs; exact by elementary counting, see its docstring), `brute_paths`
  (Lemma 6 / Picard-Queyranne closure test on every alternating walk, search over states (vertex, closure of the even
  vertices, co-closure of the odd vertices), with a state budget); Theorem 13(a) executed literally (`GraphToZZ`:
  Lemma 1 component, `Q`, ears, `H`, flow, preorder from the closures, `R`) with `lift` (down-set of the ZZ elements ->
  vertex set of `G`: ears on the side of an attachment in the set, parts beyond bridges on the side of their bridge
  end) and `cut_check`; Theorem 13(b) realisation with `M = 1` (`realise`); own ZZ solver (`ZZ.exact`); own switch form
  (`SF`, from `r4-general.md` §5.1) with stars, `NE`, `NF`, E- and F-terms of `r5-core.md` §8.2, down-set
  enumeration (`brute`) and shortest valid paths (`shortest`, `all_shortest`); the proof of Lemma 8.1 and Theorem 8.2
  as a program (`level`, `theorem82`): game value by LP (scipy `linprog`), least covers by ILP (scipy `milp`), and
  every claim checked (duality for light rows, `<= k` tools in the case of the value, `<= N` anchors, `<= 9` flips per
  tool, damage `<= |A'|/2`, `L ⊆ D(τ)`, `D(τ) ∩ ↑A' ⊆ ↑A''`, F-term misses `↑A'`, levels `<= k`, final intersection a
  down-set picking `P`); Lemma 6.3 checked on the path (span of `A ∩ NE(E#_x)` at most 9 positions); a blind
  exhaustive search over single terms with reduced parameters (`idesc_small`, 1 tool, 2 flips, 1 anchor).
- `rvc_src.py`: instance generators imported read-only (`verify/equivalence/randgraphs.py`, `dc-general/gcert.py`,
  `dc-algorithm/mixed.py`, `hubimp.py`, `r4-general/yfam.py`, `xfam.py`, `zfam.py`, `r4-search/known.py`,
  `r5-core/fool.py`, `test_bad.py`, `test_rgen.py`, `hunt_single.load`, `gcore.to_inst`), and the cross-check against
  `gsw.GSW` (read-only).
- `rvc_run.py`: the chain per instance. Graph instances: DC test, `d = 2`, `c >= 3`, brute forces, Theorem 13(a),
  P2 in ZZ, own ZZ solver, own switch form, P2 in switch form, `gsw.GSW` equal to the own conversion up to renaming of
  nodes (multiset of node incidence signatures, same switch order and preorder) and its `brute` answer (`m <= 14`),
  switch-form answers (shortest valid path; all down-sets when `m <= 18`), Theorem 8.2 run on up to 12 shortest valid
  paths, the final intersection lifted to `G` and checked to be a minimum cut containing a `u`-`v` path, 25 random
  down-sets lifted (cut value `= c`; switch-form connectivity = ZZ connectivity = path in the cut of `G`), and the blind
  single-term search when `m <= 9`. ZZ instances (families, `r4-search`, random): realised by Theorem 13(b) when
  `q <= 60` (then Fact 1 "DC iff P2" is checked and the chain runs from the graph, and the ZZ instance recovered by
  Theorem 13(a) is compared with the original); larger ones run from the ZZ level (links 2, 3 and Theorem 8.2 only).
- Debug runs (2026-10-27 18:30-18:45, not counted below): `graphs 1 6`, `graphs 2 5`, `zzrand 1 20 3 8`,
  `zzrand 2 10 3 8`, `r4search L*.json` (7 instances, `n` up to 1002, `c` up to 319): no error. The saved
  two-level example of `r5-core.md` §8.4 (`m = 27`, `k = 5`, `N = 33`, `|A| = 10`, 12 bad pairs) is reproduced by the
  own implementation: level 1 game value 1, one tool, damage 1; level 2 value 0, F-term with one star and one
  E-anchor; the intersection connects.

### 2.2 Runs

Launched 2026-10-27 from about 18:45; logs `verify/rv-r6-chain/runs/<tag>.txt` (summary) and `<tag>.jsonl` (one
record per pair). "Errors" counts records with any failed check or any mismatch between the answers (graph brute
forces, own ZZ solver, original ZZ answer, switch form by shortest valid path, switch form by down-sets, `gsw.GSW`
brute force, IDESC via Theorem 8.2, blind IDESC). `rvc_scan.py` re-reads the `.jsonl` files.

| Run (command, seed, sizes) | Instances | Outcome |
|---|---|---|
| `rvc_run.py graphs 11 1500` (`RVC_WORKERS=2`, 4 pairs per graph) | 1500 random graphs of `randgraphs.py` (9-16 vertices; 106 disconnected skipped); 3247 open-case pairs, all in DC | **0 errors.** 275 yes (all certified in `G` by the lifted final down-set: a minimum cut containing a `u`-`v` path; 71 of them with `s = t`), 2972 no; graph brute force by the subset table and the walk search on all 3247 (agree); P2 in ZZ and in switch form on all; `gsw.GSW` identical to the own conversion on all; 219 shortest valid paths through the proof of Theorem 8.2 (1 level; up to 5 heavy rows, 3 bad pairs, 2 flips); 81175 random down-sets lifted, all consistent |
| `rvc_run.py zzrand 21 600 3 10` (`RVC_WORKERS=2`, `RVC_BUDGET=50000`) | 600 random ZZ + P2 instances (`gcert.random_inst`, `mixed.random_instance`, 3-10 middle elements) realised by Theorem 13(b), graphs up to 291 vertices, `c` up to 103 | **0 errors.** Fact 1 (DC iff P2) and the round trip 13(a) of 13(b) hold on all; 287 yes (all certified in `G`), 313 no; graph brute force on all 600 (core table on 590, subset table on 10; walk search within budget on 186, agreeing); 638 shortest valid paths through Theorem 8.2 (1 level, up to 6 heavy rows, 6 bad pairs, 1 anchor); 15000 random down-sets lifted, consistent |
| `rvc_run.py small` (`RVC_WORKERS=2`) | **every** connected graph with at most 8 vertices (networkx atlas for `n <= 7`, `verify/equivalence/graphs8.g6` for `n = 8`), every ordered pair with `d = 2`, `c >= 3`: 122124 pairs, 536 of them in graphs not in DC (skipped), 121588 in DC (`n = 5, 6, 7, 8`: 10, 232, 4512, 116834) | **0 errors.** 712 yes (all certified in `G` by the lifted final down-set), 120876 no; the counts 121588 / 712 equal those of `verify/equivalence.md` §6 (independent code); subset table and walk search agree on all; P2, `gsw.GSW` identical, 754 paths through Theorem 8.2, 3039700 random down-sets lifted. Second run `small` with `RVC_FULLM=11` (tag `small-n8-full`, `m <= 6` on all pairs): **the blind IDESC(`k, k, N, 9k`) accepts exactly the 712 yes-pairs and rejects the 120876 no-pairs**, 0 errors |
| `rvc_run.py families 4 8` (`RVC_WORKERS=1`) | 48 family instances: hub `H(1,1)`, `H(2,2)` (classes and strict order), `Y_k`, `Y'_k` (`k <= 4`), `X_L` (`L <= 8`), `Z_k`, `Z^B_k` (`k <= 4`, block variant), ladders `K(3)`, `K(4)`, `K(3)W`, `A14`, `R_4`, `R_6`, `R_4H`, `T_4`, `T_6` (tie, one-way), `RM_4` (tie, one-way), `Y^d_k`, `Y'^d_k` (`k <= 4`, with and without `back`); 29 realised as graphs (`q <= 60`, up to 3876 vertices, `c` up to 1128), 19 from the ZZ level | **0 errors.** The hubs are no-instances, proved in the graph by the core table (`H(2,2)`: `q = 22`, all `2^20` core traces), and the ZZ and switch-form solvers agree; the 44 others are yes; all 25 realised yes-instances are certified in `G` by the lifted final down-set (a minimum cut containing a `u`-`v` path; for 17 of them no graph brute force was within reach (core above 24 vertices, walk search over budget), so this certificate is the graph-level proof of the answer), the 19 ZZ-level ones by the ZZ connectivity of the lifted down-set; round trip 13(a) of 13(b) exact on all 29 realised; Theorem 8.2 on 90 shortest valid paths, 1 level, up to 4 heavy rows, 4 anchors, 2 tools, 3 flips; `Z_3`, `Z_4` (`m` 18, 24): own ZZ solver over budget, answer from the switch form (shortest valid path) |
| `rvc_run.py zzrand 22 1500 2 8` (`RVC_WORKERS=2`, `RVC_FULLM=11`, `RVC_BUDGET=20000`) | 1500 random ZZ + P2 instances (2-8 middle elements) realised as graphs (up to 232 vertices, `c` up to 81), `m <= 8` | **0 errors.** 484 yes (all certified in `G`; 19 with `s = t`), 1016 no; graph brute force on all 1500; **the blind IDESC(`k, k, N, 9k`) with the parameters of Theorem 8.2 (all terms, all intersections, no path given) accepts exactly the 484 yes-instances and rejects the 1016 no-instances**; 908 paths through Theorem 8.2; 37500 random down-sets lifted |
| `rvc_run.py r4search` (`RVC_WORKERS=2`, `RVC_FULLM=11`, `RVC_COREMAX=21`, `RVC_BUDGET=20000`, tag `r4search-X-full2`) | all 157 instances of `r4-search/instances/` (smallest instances defeating level-2 methods, `shrunk-*`, `hybshr-*`, `anneal-*`, `enum-q10-*`, `L2-*`, `L3-*`), all realised (up to 1137 vertices, `c` up to 362), `m <= 11` | **0 errors.** All 157 are yes; all certified in `G` by the lifted final down-set; core table on 74 (agrees); **blind IDESC(`k, k, N, 9k`) accepts all 157**; 179 shortest valid paths through Theorem 8.2 (1 level, up to 2 heavy rows, 1 anchor, 2 tools, 3 flips; `|A|` up to 6) |
| `rvc_run.py bp 5` (`RVC_WORKERS=1`, `RVC_FULLM=11`) | `BP_n` of `r5-hard.md` (`K_{n,n}` of bad pairs on `R_{2n}`), `n <= 5`, with and without the bad switches (`bpfam.bp`, `gcore.to_inst`); 7 realised (up to 2875 vertices), 3 from the ZZ level | **0 errors.** All yes; the 7 realised ones certified in `G`; blind IDESC accepts the 7 with `m <= 11`; Theorem 8.2: `n^2` bad pairs (up to 25), `n` heavy rows covered by `n` E-anchors in the F-term (N = 30 for `m = 20`), 1 level |
| `rvc_run.py saved` (`RVC_WORKERS=1`) | the 24 saved designs of `r5-core.md` §8.4 (`two-levels-example.json` and `runs/single/*.json`), as ZZ by `gcore.to_inst` (`q` 374-680, too large to realise), `m` 26-37, shortest valid paths of 20-24 sides, `|A|` 10-12 | **0 errors.** All yes (own ZZ solver and switch form agree); **the proof of Theorem 8.2 needs 2 levels on all 24** (level 1: value 1, one tool, damage 1; level 2: value 0, F-term with one E-anchor), up to 35 bad pairs and 5 heavy rows, `k` 5-6, `N` 33-44; every claim holds and the intersection connects at the ZZ level (lifted down-set) |
| `rvc_run.py bad 31 150` (`RVC_WORKERS=1`) | 150 designs of `r5-core/test_bad.py` (planted paths, `x_i` above sets of E-members, `y_j` below F-members, `y_j < x_i`), `q` up to 256, `m` up to 24; 12 realised (up to 4033 vertices, `c` up to 1228), 138 from the ZZ level | **0 errors.** All yes; the 12 realised ones certified in `G`; 374 shortest valid paths, up to 36 bad pairs, 8 heavy rows, 3 E-anchors, 2 tools, 4 flips; 1 level |
| `rvc_run.py zzrand 23 600 4 10` with `RVC_HALF=1` (light threshold `|A'|/2`: stress test of the recursion outside the proof's parameters), `RVC_FULLM=11` | 600 realised random instances | **0 errors.** 311 yes (all certified in `G`), 289 no; blind IDESC with the parameters of Theorem 8.2 again equal to the brute force on all 600; the recursion still stops after 1 level (no light damaging pivot occurs on these instances) |
| `rvc_run.py r4search` with `RVC_HALF=1` (`RVC_WORKERS=2`, `RVC_COREMAX=21`) | the 157 `r4-search` instances, realised | **0 errors.** On 12 of them (`L3-oneway-31`, `shrunk-zz-T6one-*`, `shrunk-zz-T8one-1-K3`; 586-1002 vertices) the recursion takes **2 levels** (level 1: E-term with one pivoted tool, damage 1; level 2: E-term), and the intersection of the two terms, lifted to `G`, is a minimum cut containing a `u`-`v` path: the intersection step of Theorem 8.2 checked end to end in graphs |
| `rvc_sizes.py` (log `runs/sizes.txt`) | all 249649 graph-level records of the runs above | `m <= q − 2`, `q <= n`, `|R| <= |E|`, nodes `<= q + |R|` on all (L1 sizes) |

Runs in progress at 19:10 (PIDs of the parent processes; pool workers are their children): `small` again with the
blind IDESC (`RVC_FULLM=11`, tag `small-n8-full`, PID 28560); `bad 31 150` then `rgen 41 60` (PID 12140, then a new
one); `saved` (PID 23912); `rvc_l3.py 2 3000 2 9` (PID 33688); `bp 5` (PID 2948); `r4search` with the blind IDESC
(tag `r4search-X-full2`). Stopped by PID: the duplicate `r4search` of the families sequence (PID 3956, 3 records in
`r4search-X.jsonl`) and the first `r4search` with the blind IDESC (PID 19140, stopped after 64 records in
`r4search-X-full.jsonl`, all without error, because the core table on the 25-26 element `shrunk-*` instances was too
slow; restarted as `r4search-X-full2` with the core table limited to 21 core vertices).

**Outcomes of the runs named above (recorded 2026-10-28 from the logs, round 6c).** The sentence above is as the
reviewer wrote it; its time "19:10" is later than the last write of this report (19:05), and by their logs all runs but
`rgen` had finished by 19:05. No process of this review is left. Summary = the `runs/<tag>.txt` log; "errors" =
"total records with errors" of the summary, confirmed for every `.jsonl` by `rvc_scan.py` (re-run 2026-10-28, read
only).

| Run named in the text (PID) | Log | State | Outcome |
|---|---|---|---|
| `small` with blind IDESC, `RVC_FULLM=11` (28560) | `small-n8-full.txt`, `.jsonl` (62 836 769 bytes) | **finished**, 306 s, last write 18:59:24 | 268 jobs; 121 588 pairs (536 non-DC skipped); 712 yes, 120 876 no; blind IDESC(`k, k, N, 9k`) run on all 121 588 and accepts exactly the 712 yes-pairs; 712 certified in `G`; 754 paths through Theorem 8.2; 3 039 700 down-sets lifted; 4 pairs with `s = t`; `gsw.GSW` identical and subset table + walk search on all 121 588. **0 errors.** Maxima: `m` 6, `q` 8, `n` 8, `c` 6, 1 level, 1 tool, 1 flip, 3 heavy rows, 2 bad pairs. Agrees with the row `small` above |
| `bad 31 150` (12140) | `bad-31-150.txt`, `.jsonl` | **finished**, 903 s, 19:04:55 | 150 jobs, all yes; 12 realised and certified in `G`, 138 at the ZZ level (no graph brute force; `brute_paths` over budget on the 12); 374 paths; 3750 down-sets lifted; `gsw.GSW` identical on all 150. **0 errors.** Maxima: `m` 24, `q` 256, `n` 4033, `c` 1228, 1 level, 2 tools, 4 flips, 3 anchors, 8 heavy rows, 36 bad pairs, `\|A\|` 5, span 4. Agrees with the row `bad 31 150` |
| `rgen 41 60` (the new PID after 12140) | `rgen-41-60.txt` (only the line "60 jobs, 1 workers"), `.jsonl` (0 bytes) | **not finished** (written 19:05:06, no record, no summary) | none; designs of `test_rgen.make` (rigid words, `n` 9-14) converted by `gcore.to_inst` (`rvc_src.designs`), no result to record |
| `rgen 41 30` (not named above; 2 workers) | `rgen-41-30.txt` (only "30 jobs, 2 workers"), `.jsonl` (403 bytes) | **not finished** (written 19:05:23, one record, no summary) | one record, `rgen-41-0`: `q` 525, `\|R\|` 981, `m` 32, 494 nodes, ZZ level only (too large to realise), yes (ZZ solver, switch form and IDESC agree), 1 path, 1 level, 1 tool, 0 flips, 2 anchors, `k` 6, `N` 42, `\|A\|` = 12, 13 bad pairs; **0 errors** |
| `saved` (23912) | `saved.txt`, `.jsonl` | **finished**, 457 s, 19:04:51 | 24 jobs, all yes, all ZZ level only; 24 paths, **2 levels on all 24**, damage 1, 1 tool, 0 flips, 1 anchor; `m` 26-37, `q` up to 680, `k` 5-6, `N` 33-44, shortest valid paths of 20-24 sides, `\|A\|` up to 12, up to 35 bad pairs, 5 heavy rows; 600 down-sets lifted; `gsw.GSW` identical on all. **0 errors.** Agrees with the row `saved` |
| `rvc_l3.py 2 3000 2 9` (33688) | `l3-2-3000-2-9.txt` | **finished** (summary printed, last write 18:59:05; the script prints no elapsed time) | 3000 instances, 33 777 down-sets, 1 086 703 valid paths with at most 6 sides, 2075 instances with ties, 2716 with empty sides, 40 with `s = t`, 1085 yes. The script prints a counter named `ERROR ...` only when a check fails (the keys beginning `ERROR` in `rvc_l3.py`); none occurs, so **0 errors**; agrees with §2.3 |
| `bp 5` (2948) | `bp-5.txt`, `.jsonl` | **finished**, 231 s, 19:01:48 | 10 jobs, all yes; 7 realised (certified in `G`; up to 2875 vertices, `c` 861) and 3 at the ZZ level; blind IDESC(`k, k, N, 9k`) run on 7 and accepts 7; blind single-term search accepts 6 of 6 run; 10 paths; 250 down-sets lifted; 1 level, 1 tool, 1 flip, 5 anchors, 5 heavy rows, 25 bad pairs, `m` up to 20, `q` 125. **0 errors.** Agrees with the row `bp 5` |
| `r4search` with blind IDESC, tag `r4search-X-full2` | `r4search-X-full2.txt`, `.jsonl` | **finished**, 186 s, 19:01:53 | 157 jobs, all yes, all certified in `G`; blind IDESC accepts all 157 (run on 157); core table on 73 + 1 (core+paths) = 74; 179 paths; 3925 down-sets lifted; `gsw.GSW` identical on 157. **0 errors.** Maxima: `m` 11, `q` 33, `n` 1137, `c` 362, 1 level, 2 tools, 3 flips, 1 anchor, 2 heavy rows, `\|A\|` 6. Agrees with the row `r4search` |
| stopped: duplicate `r4search` of the families sequence (3956) | `r4search-X.txt` (header only), `.jsonl` | **stopped by PID, as written** | 5 records (the text above says 3), all yes, all certified in `G`, **0 errors** |
| stopped: first `r4search` with blind IDESC (19140) | `r4search-X-full.txt` (header only), `.jsonl` | **stopped by PID, as written** | 64 records (as written), all yes, all certified in `G`, 78 paths, **0 errors** |

Elapsed times of the other finished runs (summary lines), all with "total records with errors: 0": `graphs 11 1500`
9 s (3247 pairs), `zzrand 21 600 3 10` 224 s, `small` (without blind IDESC) 171 s, `families 4 8` 402 s, `zzrand 22
1500 2 8` 235 s, `zzrand 23 600 4 10` with `RVC_HALF=1` 201 s, `r4search` with `RVC_HALF=1` 144 s (12 of 157 with 2
levels, damage 1; blind IDESC not run in that tag). Their counters were compared with the rows above: all agree.
Besides, in `runs/` without a summary file (console debug runs, 0 errors each by `rvc_scan.py`): `graphs 1 6` (13
records), `graphs 2 5` (7), `zzrand 1 20 3 8` (20), `zzrand 2 10 3 8` (10), `r4search L*.json` (7), and two not named
in §2.1, `zzrand 3 30 2 6` (30 records: 6 yes, 24 no, 6 certified in `G`) and `zzrand 4 12 7 10` (12 records: 8 yes, 4
no, 8 certified in `G`); their record counts equal the job counts in their names.
Not finished, to rerun if wanted (`RVC_WORKERS=2`, from `verify/rv-r6-chain/`, PowerShell): `python rvc_run.py rgen 41
30`; no verdict rests on these runs.

### 2.3 Link L3 checked separately (`rvc_l3.py`, `rvc_seqt.py`)

`python rvc_l3.py 2 3000 2 9` (log `runs/l3-2-3000-2-9.txt`): 3000 random ZZ + P2 instances (`gcert.random_inst`,
`mixed.random_instance`, 2-9 middle elements), 2075 of them with ties among the switches, 2716 with empty sides, 40
with `s = t`; all 33777 down-sets enumerated, all 1086703 valid paths with at most 6 sides enumerated. Checked: every
connecting down-set has a shortest picked walk that is a valid path; for every valid path `P`, `L = ↓W_F` is a
down-set that picks `P` and connects, `Up ∩ L = ∅`, and for **every** down-set `D`: `D` picks all members of `P` iff
`L ⊆ D` and `D ∩ Up = ∅` (F0); "some down-set connects" iff "`s = t` or a valid path exists". **0 errors** (1085 yes).
`python rvc_seqt.py` (log `runs/seqt.txt`): the edge case of §1.3 made explicit. ZZ instance `u, b, t, v` with
`u ~ b`, `t ~ v`, `R = {u t, b t, b v}` (P2 vacuous; consistent zigzag `u < t > b < v`); switch form: no switch,
one node, `s = t`, no side at all, hence no valid path with `r >= 1`; the blind IDESC accepts; realised graph (11
vertices, in DC, `d(u,v) = 2`, `c = 4`): `cp = c` by both graph brute forces, certified by the lifted (empty) down-set.
So the hypothesis "has a valid path" of Theorem 8.2 must be read as "is a yes-instance with `s != t`"; the case
`s = t` is trivially accepted. Wording repair only.

## 3. Repairs and remarks for the write-up (none changes a result)

1. **`s = t`** (L3). Theorem 8.2 assumes "a valid path"; Corollary 8.3 needs "yes-instance". Add: "If `s = t`, every
   down-set connects and IDESC accepts at its first test; otherwise yes-instance iff a valid path exists (F0)".
   Example with no switch at all in §2.3 (`rvc_seqt.py`).
2. **Direction of Theorem 13** (L1). Corollary 8.3 cites the polynomial *equivalence*; only the reduction of
   Theorem 13(a) is used (and should be cited with the repairs of `verify/equivalence.md` §3: minimum cuts of `H` =
   down-sets; `cp = c` iff a consistent zigzag; P2 by the repaired Corollary 12). Theorem 13(b) is needed only for
   "every ZZ + P2 instance is a graph of DC".
3. **ETH wording** (L4). "Not NP-complete unless NP ⊆ QP (not under ETH)" should read: "not NP-hard under
   polynomial-time reductions unless NP ⊆ QP; in particular, if ETH holds, it is not NP-hard". The problem is in NP
   (Lemma 6), so NP-hard and NP-complete coincide here; the DC promise is checkable in polynomial time (all-pairs
   distances and capped flows), so the promise problem and the language version have the same complexity.
4. **Sizes** (L1). State in Corollary 8.3 that the reduction gives `m <= n − 2` switches and at most `|Q| + |R| <=
   n + |E|` nodes, so `2^{O(log^3 m)} poly(n, |E|) = 2^{O(log^3 n)}`.
5. **Scope of the computations.** All graph-level runs produced one level of the proof (the recursion needs
   `|A| >= 2k` minimal E-members with a light damaging pivot, i.e. long shortest paths, which the realisable instances do
   not have); two levels were exercised only at the ZZ level (the 24 saved designs of `r5-core.md` §8.4, all with
   2 levels, damage 1, value 1 then 0, one E-anchor) and, with the light threshold `|A'|/2` (`RVC_HALF=1`, a stress
   test outside the proof's parameters), on realised `r4-search` instances.
