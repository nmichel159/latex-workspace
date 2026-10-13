# Algorithms for the open case of DC (agent DC-algorithm)

Status: working file, version 2 (2026-10-13; version 1 of 2026-10-12 consisted of Sections 1-4, kept unchanged in
substance). Scripts: `dc-algorithm/` (Python 3.13; `checks/mcp.py`, `theory-dc-scripts/pi.py` and, for one round
trip, `verify/equivalence/eqcore.py`, `zzgen.py` imported read-only). Every claim is labeled **proved**, **checked**,
**sketch**, **conjecture** or **refuted**. Notation as in `theory-dc.md`: `c = c(u,v)`, PIMC = "some minimum `u`-`v`
cut contains a `u`-`v` path", ZZ = the zigzag problem of `theory-dc.md` Theorem 13, P2 its distance condition.
An element is *middle* if it is equivalent neither to `u` nor to `v`.

## 0. Summary

| # | Result | Status |
|---|---|---|
| A | PIMC, hence `cp(u,v) = c(u,v)?`, is decidable in `O(e * c! * c^2 * n^3 + n m)` time in every graph (explicit FPT bound in `c`); in the open case of DC this computes `cp`. Method: guess the sequence of flow paths used by the path; for a fixed sequence the problem is a binary CSP with max-closed constraints, solved by arc consistency. | proved; checked on 30,008 + 608 instances |
| A' | The same with `c` replaced by the width `w <= c` of the order of the allowed cuttable edges (any chain decomposition works) | proved |
| B | ZZ without P2 is W[1]-hard parameterized by the width of the order plus the zigzag length (reduction from Multicolored Clique). Graph form: deciding whether a minimum `u`-`v` cut contains a `u`-`v` path (`d(u,v) = 2`) is W[1]-hard parameterized by the length of the path. | proved; reduction checked on 400 instances |
| C | ZZ is polynomial for bounded width of the order (XP, `(q+1)^w` down-sets) | proved (folklore-level) |
| D | Arc consistency (AC) of the path-position CSP does not decide ZZ + P2 (Section 4) | refuted (9-element counterexample) |
| **E** | **Path consistency (PC) of the path-position CSP does not decide ZZ + P2.** The hub instance `H(2,2)` (Section 6): 22 elements, a partial order (no two elements equivalent) or, in a second version, bottoms and tops in the classes of `u`, `v` as in the switch model; P2 holds, no consistent zigzag exists, and PC leaves every relation non-empty for every odd `L >= 19`, in particular for `L = 21`, the length of the decision procedure. Realised as a DC graph (`theory-dc.md` Theorem 13(b)): 417 vertices, `d(u,v) = 2`, `c(u,v) = 160`, `cp = c + 1`. | refuted: P2 and "no zigzag" proved; PC computed by four implementations; graph form checked by the independent code of verify-equivalence |
| F | **Bottom witnesses.** If every two incomparable elements have a common real neighbour equivalent to `u` (for instance a *lower hub*, one element equivalent to `u` joined to every middle element), then P2 holds, two incomparable peaks of a shortest consistent zigzag are consecutive peaks, its minimal peaks are at most two, and ZZ is decidable in `O(q^2 (q + |R|))` time; dually with top witnesses. `H(2,2)` (second version) lies in this class, so PC fails on a polynomial subclass of the open case of DC. | proved; algorithm checked against exact solvers |
| G | Lemma: if PC leaves the CSP with `L` positions non-empty, it does so with `L + 2` positions. So a PC failure persists for all larger `L`. | proved |
| H | PC fails without P2 as well: the switch-model encoding of 3-colouring `K_4` (`k4.py`, 56 elements) passes PC with `L = 55`; each of its 120 switch pairs without P2 admits no single P2 connector that keeps the answer "no". | checked |
| I | Adversarial runs (Section 5): about 506,000 P2 instances evaluated, about 82,000 of them no-instances, 12,850 AC false positives, 0 PC false positives; but the controls without P2 (NP-complete case) also gave 0 PC false positives, so these runs could not detect PC failures at their sizes (at most 21 elements, random structure); all 427 stored AC false positives re-checked. | checked |
| J | Smallest PC counterexample known: 22 elements; it is minimal under deletion of one element or one real edge (except one redundant edge of the partial-order version). The random runs found none with at most 21 elements. | checked |

Open: the complexity of ZZ + P2 (equivalently of the open case of DC). Every PC failure found uses order relations
between middle elements; whether PC decides the switch model 2CH + P2 (middle elements pairwise incomparable,
`dc-hardness.md`) remains open (conjecture, Section 7). Stronger relaxations on `H(2,2)`: Section 6.6.

Consequences for the open case of DC: FPT in `c` (A). PC is not a polynomial algorithm (E). A polynomial algorithm,
or an FPT algorithm in the width or in the path length, must use P2: without P2 the width and the path length do
not help (B). The hub theorem (F) shows how P2 can be satisfied for free by one hub, and that this case is easy.

## 1. Theorem A (FPT in `c`, explicit)

### Setting
`G = (V, E)` a finite graph (parallel edges allowed), `u != v`, `c = c(u,v) >= 1`, `E' ⊆ E` a set of *allowed*
edges (all edges for PIMC in `G`; the real edges for the multigraph `H` of `theory-dc.md` Proposition 5).
Fix a maximum `u`-`v` flow without flow cycles and decompose it into `c` edge-disjoint simple directed `u`-`v`
paths `π_1, ..., π_c` (the *chains*); `π_a[s]` is the `s`-th vertex of `π_a`, `π_a[0] = u`.
Write `U(A)` for the cut `δ(A)` with `u ∈ A`, `v ∉ A`, and call `A` a *minimum side* if `|δ(A)| = c`.
For a vertex `x` let `C(x)` be the smallest minimum side containing `x` if one exists
(Picard-Queyranne: `C(x) = cl(u) ∪ cl(x)` in the residual digraph, `theory-dc.md` Lemma 6, `literature.md` L1, D1);
`x ≤ y` means `x ∈ C(y)` (every minimum side containing `y` contains `x`).
The edge `e_a(s) = π_a[s] π_a[s+1]` is *cuttable* if some minimum side contains `π_a[s]` and not `π_a[s+1]`,
i.e. `C(π_a[s])` exists and does not contain `π_a[s+1]`.

### Lemma A1 (one edge per chain) — proved
For every minimum side `A`, every edge of `δ(A)` carries one unit of flow from `A` to `V - A`, `V(π_a) ∩ A` is a
prefix `π_a[0..s]` of every chain, and `δ(A) ∩ E(π_a) = {e_a(s)}`.

*Proof.* The flow value is `c = f(A → V-A) - f(V-A → A) <= |δ(A)| = c`, so every edge of `δ(A)` carries one unit
from `A` to `V - A` and no edge carries flow into `A`. `π_a` starts in `A` and ends outside; it uses no edge from
`V - A` to `A`, so once it leaves `A` it never returns, and it crosses `δ(A)` exactly once. ∎

### Lemma A2 (compatibility is max-closed) — proved
Let `a != b` be chains. The set `Good_ab` of pairs `(s, t)` of cuttable positions such that `e_a(s)` and `e_b(t)`
lie in a common minimum cut is closed under componentwise maximum and minimum.

*Proof.* By D1 of `literature.md` (Helly; orientation of a cut edge is the flow direction), two cuttable edges
`e = (t_e, h_e)`, `e' = (t_{e'}, h_{e'})` (tail, head in flow direction) lie in a common minimum cut iff
`h_e ∉ C(t_{e'})` and `h_{e'} ∉ C(t_e)`. Let `Bad1 = {(s,t) : π_a[s+1] ∈ C(π_b[t])}` and
`Bad2 = {(s,t) : π_b[t+1] ∈ C(π_a[s])}`; `Good_ab` is the complement of `Bad1 ∪ Bad2`.
By Lemma A1 every minimum side meets `π_b` in a prefix, so `π_b[t] ∈ C(π_b[t'])` and `C(π_b[t]) ⊆ C(π_b[t'])`
for `t <= t'`; likewise along `π_a`, and every `C(y)` is a down-set of `≤`.
Hence `Bad1` is closed downwards in `s` (`π_a[s''+1] ≤ π_a[s+1]` for `s'' <= s`) and upwards in `t`;
`Bad2` is closed downwards in `t` and upwards in `s`.
Let `(s_1, t_1), (s_2, t_2) ∈ Good_ab`, `s = max(s_1, s_2)`, `t = max(t_1, t_2)`.
If `(s, t) ∈ Bad1`: when `t = t_1`, `s >= s_1` and downward closure in `s` give `(s_1, t_1) ∈ Bad1`; when
`t = t_2`, the same gives `(s_2, t_2) ∈ Bad1`. Contradiction either way. If `(s, t) ∈ Bad2`: when `s = s_1`,
`t >= t_1` and downward closure in `t` give `(s_1, t_1) ∈ Bad2`; when `s = s_2`, `(s_2, t_2) ∈ Bad2`.
So `(s, t) ∈ Good_ab`. The minimum is symmetric. ∎

### Lemma A3 (shared ends are monotone) — proved
For chains `a != b`, the pairs `(s, t)` of cuttable positions with `π_a[s+1] = π_b[t+1]` (same head) form a strictly
increasing partial injection, and so do the pairs with `π_a[s] = π_b[t]` (same tail). Both relations are closed
under componentwise maximum and minimum.

*Proof.* The chains are simple, so each relation is a partial injection. Same head: let `(s,t), (s',t')` be in it
with `s < s'`, `x = π_a[s+1]`, `y = π_a[s'+1]`. As `e_a(s')` is cuttable, `y ∉ C(π_a[s'])`, while
`x ≤ π_a[s']` (because `s + 1 <= s'`). If `t' < t`, then `y = π_b[t'+1] ≤ π_b[t+1] = x ≤ π_a[s']`, so
`y ∈ C(π_a[s'])`, a contradiction; `t' != t` since `x != y`. Same tail: `x = π_a[s]`, `y = π_a[s']`; as `e_a(s)` is
cuttable, `π_a[s+1] ∉ C(x)`, while `π_a[s+1] ≤ y`; `t' < t` would give `y = π_b[t'] ≤ π_b[t] = x`, so
`π_a[s+1] ∈ C(x)`. Two pairs of a strictly increasing relation are comparable componentwise, so their maximum
and minimum are among them. ∎

### Lemma A4 (max-closed binary CSPs) — proved (standard; proof given to be self-contained)
Let a binary CSP have totally ordered finite domains and only constraints closed under componentwise maximum.
If arc consistency leaves every domain non-empty, then giving every variable the largest value left in its domain
satisfies every constraint.

*Proof.* Let `C(x, y)` be a constraint and `p, q` the largest remaining values of `x`, `y`. By arc consistency `p`
has a support `(p, q')` and `q` a support `(p', q)` in `C`, with `q' <= q`, `p' <= p`; their maximum `(p, q)` lies
in `C`. ∎

### Theorem A — proved
PIMC with allowed edges `E'` is decided, and a witness path found, in time `O(e · c! · c^2 · n^3 + n·m)`.
In particular `cp(u,v) = c(u,v)` is decidable in this time in every graph, and in the open case of DC
(`d(u,v) = 2`, `c >= 3`) `cp(u,v) ∈ {c, c+1}` is computed in this time.

*Algorithm.* For every sequence `(i_1, ..., i_L)` of distinct chains with `L` odd, solve the CSP with variables
`s_1, ..., s_L`, domain of `s_j` = allowed cuttable positions on `π_{i_j}`, unary constraints `π_{i_1}[s_1] = u`,
`π_{i_L}[s_L + 1] = v`, the constraint `Good` (Lemma A2) between every two variables, and between `s_j`, `s_{j+1}`
"same head" for odd `j`, "same tail" for even `j` (Lemma A3). By Lemma A4 arc consistency decides it and the
largest values form a solution.

*Correctness.* A solution gives edges `e_1, ..., e_L` that are pairwise in common minimum cuts, hence (D1, Helly)
all in one minimum cut `δ(A)`; the shared ends make `u = t(e_1), h(e_1) = h(e_2), t(e_2) = t(e_3), ..., h(e_L) = v`
a `u`-`v` walk inside `δ(A)`, which contains a `u`-`v` path of allowed edges. Conversely let `P = x_0 ... x_L` be a
`u`-`v` path of allowed edges inside a minimum cut `δ(A)`. Its even vertices lie in `A`, its odd vertices outside,
so `L` is odd and edge `j` has tail `x_{j-1}` or `x_j`, whichever is even. By Lemma A1 every edge of `δ(A)` lies on
exactly one chain and every chain has exactly one edge in `δ(A)`, so the edges of `P` lie on `L <= c` distinct
chains `i_1, ..., i_L` at cuttable positions; consecutive edges share the head (odd `j`) or the tail (even `j`).
This is a solution for the sequence `(i_1, ..., i_L)`.

*Time.* One maximum flow `O(c·m)`, the closures `O(n·m)`. The number of sequences is
`Σ_{L odd} c!/(c-L)! <= e · c!`. Arc consistency on `L <= c` variables with domains of size `<= n` takes
`O(L^2 · n^2)` per revision round and at most `L · n` rounds that delete a value: `O(c^3 n^3)` crudely,
`O(c^2 n^3)` with the AC-3 queue. ∎

*Remarks.* (1) Article 1, Theorem 8.4 already gives FPT for the threshold `b` (here `b = c`) with no explicit
bound; Theorem A gives `c! · poly` for the special question `cp = c`, by a direct combinatorial algorithm.
(2) The implementation (`chaincsp.py`) enumerates the sequences by depth-first search and runs arc consistency on
every prefix, so infeasible prefixes are cut early (largest search tree seen in the tests: 95 nodes).
(3) Only the chains that carry an allowed cuttable edge matter; in `H` these are the flow paths through real edges.

### Theorem A' (any chain decomposition) — proved
Let `F'` be the set of allowed edges that lie in some minimum cut, ordered by `e < e'` iff `h(e) ≤ t(e')`
(D2 of `literature.md`: a strict partial order, and a set of edges lies in one minimum cut iff it is an antichain).
For any partition of `F'` into chains of this order, Lemmas A2-A4 hold with "position on `π_a`" replaced by
"position on the chain" (the proofs use only that along a chain the heads are `≤` the tails of later edges, and
that two edges with a common tail, or a common head, are incomparable). Hence PIMC is decided in
`O(e · w! · poly)` time, `w` = width of `(F', <)` (a minimum chain partition is found by bipartite matching).
`w <= c` (D2(d)); with all edges allowed `w = c` (a minimum cut is an antichain of size `c`), but with `E'` = real
edges of `H` it can be smaller.

### Checks
`dc-algorithm/test_chaincsp.py SEED COUNT`: families random connected graphs `G(n,p)`, `n` = 5..13, random pair
`u, v` (any distance); Π-instances of `pi.py` (random and planted) realised as simple graphs; the family `G_k` of
`theory-dc.md` Theorem 8 (`k = 1..4`). Each answer is compared with brute force over all minimum cuts
(`chaincsp.pimc_brute`), each witness is re-checked by the closure test of Lemma 6, and Lemma A4 is checked on
every solved sequence (the largest values form a solution).
Seed 1, 300 per family: 608 instances, 0 mismatches. Seed 2, 15000 per family: 30,008 instances
(14,889 yes, 15,119 no; witness lengths 1: 7182, 3: 3279, 5: 1079, 7: 255, 9: 11), 0 mismatches, 0 failures of
Lemma A4.

## 2. Theorem B (no FPT in width or path length without P2)

### Construction — proved
Instance of Multicolored Clique: a graph `K` with vertex classes `V_1, ..., V_k`, `V_i = {(i,1), ..., (i,n_i)}`.
ZZ instance: a preorder with classes `B` (contains `u`), `T` (contains `v`) and `X_{i,r}` (`1 <= i <= k`,
`0 <= r <= n_i`), ordered by `B < X_{i,0} < X_{i,1} < ... < X_{i,n_i} < T`, classes of different `i` incomparable.
The quotient order has width `k`. Order the `C(k,2)` pairs `(i, j)`, `i < j`, and create bottom elements
`g_0 = u, g_1, ..., g_{C(k,2)} ∈ B`. For the `t`-th pair `(i, j)` and every edge `{(i,r), (j,r')}` of `K` create a
private *route* of fresh elements `x1 ∈ X_{i,r}`, `x2 ∈ X_{i,r-1}`, `y ∈ T`, `x3 ∈ X_{j,r'-1}`, `x4 ∈ X_{j,r'}`
with real edges `g_{t-1} x1, x1 x2, x2 y, y x3, x3 x4, x4 g_t`; finally the real edge `g_{C(k,2)} v`.

### Theorem B — proved
The instance has a consistent zigzag iff `K` has a multicolored clique. Every zigzag has length
`ℓ = 6 C(k,2) + 1`. Hence ZZ (without P2) is W[1]-hard parameterized by `k + ℓ`, i.e. by the width of the order
together with the length of the zigzag.

*Proof.* The real-edge graph is a series of bundles of internally disjoint paths of length 6 between `g_{t-1}` and
`g_t`, so a simple `u`-`v` path picks one route per pair and has length `ℓ`; along a route the elements go
`g < x1 > x2 < y > x3 < x4 > g'`, and `g_{C(k,2)} < v`, so every `u`-`v` path is a zigzag. Its valleys are the
`g`'s and the `x2, x3` of the chosen routes, its peaks the `x1, x4, y` and `v`. A valley in `B` is above nothing
but `B`; nothing is above `T`; a valley in `X_{i,a}` is `>=` a peak in `X_{i',b}` iff `i = i'` and `a >= b`.
So the zigzag is consistent iff for every `i` all valleys on chain `i` lie below all peaks on chain `i`. A route for
the edge `{(i,r),(j,r')}` puts the valley `r - 1` and the peak `r` on chain `i` (and `r' - 1`, `r'` on chain `j`);
two routes put `(r-1, r)` and `(s-1, s)` on chain `i` consistently iff `r - 1 < s` and `s - 1 < r`, i.e. `r = s`.
Hence consistent zigzags correspond to choices `r_i` with all pairs `(i, r_i), (j, r_j)` adjacent. ∎

### Corollary B' (graphs) — proved, using `theory-dc.md` Theorem 13(b)
Realise the instance as in `theory-dc.md` Theorem 13(b) (weight one on every comparable pair, ears `u a` and `b v`,
heavy ears inside classes); the cut formula `|δ(A)| = N + 2 #{a < b : a ∉ A, b ∈ A}` there does not use P2, so the
minimum cuts are the down-sets, `d(u,v) = 2`, and `cp(u,v) = c(u,v)` iff a consistent zigzag exists. Ear vertices
have degree two and are never on a path inside a minimum cut (`theory-dc.md` Lemma 2), so every such path has
length `ℓ`. Therefore: *deciding whether some minimum `u`-`v` cut contains a `u`-`v` path is W[1]-hard
parameterized by the length of the path*, even when `d(u,v) = 2` and all such paths have the same length, and
(in the multigraph form `H`) W[1]-hard parameterized by the width of the residual order.
Contrast with Theorem A: the path length is at most `c`, and the problem is FPT in `c`.
(The Theorem 13(b) cut formula was proved and checked by agent theory-DC; not re-run here on these instances.)

### Check
`dc-algorithm/mcc.py 1 400`: random Multicolored Clique instances with `k = 2..4`, class sizes 1..3, edge
probability 0.4-0.8; ZZ answer by the exact search `zz.exact_dfs` = clique answer in all 400 (k=2: 126, k=3: 139,
k=4: 135; 269 yes).

## 3. Proposition C (bounded width) — proved
If the quotient of the preorder has width `w` and `q` classes, it has at most `(q/w + 1)^w <= (q+1)^w` down-sets
(each is fixed by one prefix of each chain of a chain partition into `w` chains, Dilworth), so ZZ is solved in
`O((q+1)^w · |R|)` time; for DC the residual order of `H` has width at most `c` (`theory-dc.md` Proposition 10).
By Theorem B this cannot be improved to FPT in `w` without using P2 (unless FPT = W[1]).

## 4. Relaxations of the path-position CSP

*CSP.* Variables `1..L` (`L` odd), value of variable `j` = a real edge `(t, h)`, `t < h`; variable 1 has `t = u`,
variable `L` has `h = v`; consecutive variables share the head (odd `j`) or the tail (even `j`); every two variables
are compatible (`not h ≤ t'`, `not h' ≤ t`). A solution is a `u`-`v` walk in one down-set cut (which contains a
consistent zigzag); a consistent zigzag of length `l <= L` pads to length `L` by going back and forth on its last
edge. So for every odd `L >= q - 1` the CSP decides ZZ exactly. Its arc consistency (AC) and strong path consistency
(PC) are polynomial necessary conditions; the candidate decision procedure was "yes iff PC leaves every relation
non-empty with `L` = the largest odd number `<= q`" (`q = |Q|`).

### Lemma G (monotone in `L`) — proved
If the PC closure of the CSP with `L` positions is non-empty, so is the PC closure with `L + 2` positions.

*Proof.* Let `N` be the PC closure for `L` (relations `R_jk`, domains `R_jj`). Define `N'` on positions `1..L+2`:
positions `L+1`, `L+2` are copies of position `L`, i.e. `R'_{j,L+1} = R'_{j,L+2} = R_{j,L}` for `j < L`, and
`R'_{L,L+1} = R'_{L,L+2} = R'_{L+1,L+2}` = the identity on the domain of `L`; all other relations as in `N`. `N'`
lies inside the base constraints of the `(L+2)`-CSP: an edge shares its head and its tail with itself and is
compatible with itself (`h ≤ t` is impossible for `t < h`); positions `j < L` and `L+1`, `L+2` are not consecutive,
so only compatibility is required there, and `R_{j,L}` satisfies it; the last position `L+2` has head `v` because
position `L` has. `N'` is path consistent: a triple of positions maps to a triple of `N` (copies replaced by `L`),
and supports through a copy are the supports through `L` composed with the identity. The PC closure is the largest
path-consistent network inside the base constraints, so it contains `N'`, which is non-empty. ∎

Consequence: once PC fails to refute a no-instance at some `L`, it fails at every larger odd `L`; enlarging `L` never
helps PC.

### D1: "AC decides ZZ + P2" — refuted
Smallest counterexample found (switch model, `zz.from_sw`, 9 elements): bottoms `b0 = u, b1, b2, b3`, tops
`t0 = v, t1`, fixed edge `b1 t1`, switches `s0: Nb = {b0, b2, b3}, Nt = {t1}`, `s1: Nb = {b1, b2, b3}, Nt = {t0, t1}`,
`s2: Nb = {b2, b3}, Nt = {t0}` (P2 holds). No consistent zigzag (the only routes need `s1` both as a peak and as a
valley); AC leaves all domains non-empty; PC refutes it.

### D2: "PC decides ZZ + P2" — refuted (Section 6)

## 5. Adversarial runs (accounting, 2026-10-12/13)

Hill climbing over no-instances, scored by the largest window `w` for which AC (then PC) of the windowed CSP
(compatibility only between positions at distance `<= w`) still says yes; yes-instances are rejected. Every AC false
positive found while the current instance already was one was tested with PC; the first AC false positive of each
climb was counted without a PC run. The first 20 AC false positives of every run were stored (`runs/*.jsonl`).

| Round, script | Mode (sizes) | Runs | Instances evaluated | No-instances | AC false positives | PC false positives |
|---|---|---|---|---|---|---|
| 1, `hunt_pc.py` | `sw`: switch model + P2 (up to 12 switches) | seeds 11-14, 6000 steps each | 24,000 steps | not logged | 5,365 | 0 |
| 1, `hunt_pc.py` | `zz`: general ZZ + P2 (10-13 elements) | seeds 21-24, 6000 steps | 24,000 steps | not logged | 510 | 0 |
| 1, `hunt_pc.py` | controls without P2: `swfree`, `zzfree` | seeds 31, 32, 41, 42 | 24,000 steps | not logged | 6,948 | 0 |
| 2, `hunt2.py` | `zz` + P2, 12-17 elements | seeds 51-53 | 364,405 | 68,706 | 6,716 | 0 |
| 2, `hunt2.py` | `zz` + P2, 16-21 elements | seed 54 | 90,139 | 6,023 | 4 | 0 |
| 2, `hunt2.py` | `sw` + P2 (up to 7 bottoms, 7 tops, 12 switches) | seeds 61, 62 | 3,002 | 1,846 | 255 | 0 |
| 2, `hunt2.py` | `rigid`: broken `R_L` (`L <= 7`) + P2 repair | seeds 71, 72 | no progress line logged | | at least 40 | none reported |
| 2, `hunt2.py` | controls without P2: `zzfree` 81, `swfree` 91 | | 7,013 | 5,784 | 2,289 | 0 |

Round 2 stopped after about 32 minutes (the agent stopped); the figures are the last progress lines of the logs.
Totals with P2 (rounds 1 and 2, without `rigid`): about 505,500 instances evaluated (at least 76,575 of them
no-instances in round 2 alone), 12,850 AC false positives, 0 PC false positives.

**Re-check** (`recheck_acfp.py`, `runs/recheck-acfp.txt`): all 427 stored instances (307 with P2: `zz` 144, `sw` 123,
`rigid` 40; 120 controls without P2), with `exact_dfs` and, for `q <= 22`, the enumeration of all down-sets: every
one is a no-instance, AC says yes, PC with the full `L` says no.

**What the runs show.** Nothing about PC under P2: the controls without P2, where ZZ is NP-complete and PC therefore
cannot be exact (unless P = NP), produced no PC false positive either, and the smallest PC failures known with and
without P2 have 22 and 56 elements and a planned structure (Sections 6 and 8). Random hill climbing at these sizes
does not reach them.

**Structured families** (`families_pc.py`, `runs/families-A.txt`, `runs/families-C.txt`; P2 holds in all): `Z_k`,
`Z'_k` of `theory-dc.md` (`k = 2..5`) and their no-variants with one witness edge deleted (64 no-instances: AC and PC
refute all); the rigid family `R_L` (`L = 2..7`) and its no-variants (`t` moved into another side, one `y` node
deleted, a double wire; 54 no-instances, 24 of them AC false positives, PC refutes all 54).

## 6. The hub family: PC does not decide ZZ + P2

Scripts: `hubimp.py` (the family), `hubties_min.py` (the same with classes of equivalent middle elements),
`verify_pcfp.py` (independent check), `realise_check.py` (graph form), `shrink_pcfp.py`; instances in
`runs/pcfp-*.json`.

### 6.1 Construction
Parameters `m, m' >= 1`; list the pairs `(i, j)` (`i < m`, `j < m'`) as gadgets `g_1, ..., g_K`, `K = m m'`
(default: lexicographic order), with *nodes* `n_0 = s, n_1, ..., n_K = a`.
Elements:
- bottoms `b_s = u`, `b_a`, `b_β`, `b_t`;
- tops `t_{n_0}, ..., t_{n_K}` (`t_{n_K} = t_a`) and `t_t = v`;
- middle elements: entries `ε_i` (`i < m`), exits `ξ_j` (`j < m'`), routes `ρ^A_{ij}`, `ρ^B_{ij}` for every gadget.

Order: every bottom is below every middle element and every top, every middle element below every top, and
`ε_i < ρ^A_{ij}` for all `j`, `ξ_j < ρ^B_{ij}` for all `i`; nothing else among middle elements. Two versions:
*classes*: the bottoms are equivalent to `u`, the tops to `v` (the switch-model convention); *partial order*: no two
elements equivalent, `u` least, `v` greatest, the other bottoms pairwise incomparable, the other tops pairwise
incomparable.
Real edges `R`: the fixed edges `b_s t_{n_0}`, `b_a t_a`, `b_t t_t`; for a gadget `g_p = (i, j)` and
`ρ ∈ {ρ^A_{ij}, ρ^B_{ij}}`: `b_β ρ`, `ρ t_{n_{p-1}}`, `ρ t_{n_p}`; the hub edges `b_a ε_i`, `b_β ε_i`, `b_β ξ_j`,
`b_t ξ_j`; in the partial-order version also `u b` for the bottoms `b != u` and `t v` for the tops `t != v`.
Size: `q = 4 + (K + 2) + m + m' + 2K`; `H(2,2)`: `q = 22`, `|R| = 35` (classes) or 43 (partial order).

The intended zigzag: `u t_{n_0} ρ_1 t_{n_1} ... ρ_K t_a b_a ε_i b_β ξ_j b_t v` (`ρ_p` a route of `g_p` as a valley,
`ε_i`, `ξ_j` as peaks), length `2K + 7`. The relation `ε_i < ρ^A_{ij}` says: if the entry `ε_i` is a peak, the
routes `ρ^A_{i·}` are not valleys; likewise for `ξ_j`. Gadget `(i, j)` is blocked by the choice (entry `i`, exit `j`).
In switch-model words: every E-side (bottom neighbourhood of a middle element) contains the hub node `β`, which gives
P2 for free, and the order relations play the role of ties.

### 6.2 Proposition 6.1 — proved
For all `m, m' >= 1`, both versions of `H(m, m')` satisfy P2 and have no consistent zigzag.

*Proof.* P2. In the classes version every element equivalent to `u` or `v` is comparable with everything, so an
incomparable pair consists of two middle elements; `b_β` is adjacent to every middle element and strictly below
both. In the partial-order version incomparable pairs are, in addition, two bottoms other than `u` (common
neighbour `u`, below both) or two tops other than `v` (common neighbour `v`, above both).

No zigzag. Let `D` be a down-set with `u ∈ D`, `v ∉ D`, and `G_D` the graph of real edges crossing `D`; a consistent
zigzag exists iff some `G_D` connects `u` and `v` (`verify/equivalence.md` §3). Classes version: bottoms lie in `D`,
tops outside. In `G_D` a middle element `x` is joined to its bottom neighbours if `x ∉ D` (a peak) and to its top
neighbours if `x ∈ D` (a valley), and the only bottom-top edges are the three fixed edges. The neighbours of
`v = t_t` are `b_t` only; the neighbours of `b_t` are `v` and the exits `ξ_j ∉ D`; a middle element `x ∉ D` is
adjacent to `b_β` and, for an entry, to `b_a`, for an exit, to `b_t`, and to nothing else (its top edges are not
cut). So the component of `v` consists of `v`, `b_t`, `b_β`, `b_a` (if some `ε_i ∉ D`), the middle elements outside
`D`, and what is reached from `b_a` through `t_a`. From `t_a` the cut edges lead only to routes of `g_K` inside `D`,
from a route of `g_p` inside `D` to `t_{n_{p-1}}` and `t_{n_p}`, and `u = b_s` is reached only through `t_{n_0}`.
Hence `u` and `v` are connected iff some exit `ξ_j ∉ D` (else the component of `v` is `{v, b_t}`), some entry
`ε_i ∉ D` (else `b_a` is not reached), and every gadget has a route in `D`. But `ε_i ∉ D` forces `ρ^A_{ij} ∉ D` and
`ξ_j ∉ D` forces `ρ^B_{ij} ∉ D` (`D` is a down-set), so gadget `(i, j)` has no route in `D`.
Partial-order version: if some bottom `b != u` is outside `D`, every middle element and every top is outside `D`
(they lie above `b`), so `G_D` has no edge at a middle element, and the component of `u` is contained in
`{u} ∪ {bottoms} ∪ {t_{n_0}}`. If some top `t != v` is inside `D`, every bottom and middle element is inside `D`,
and the component of `v` is contained in `{v, b_t} ∪ {tops in D}`. Otherwise bottoms are in `D` and tops outside,
the added edges `u b`, `t v` are not cut, and the argument of the classes version applies. ∎

### 6.3 PC on `H(2,2)` — checked
For both versions of `H(2,2)` (`q = 22`) the PC closure of the CSP is non-empty for `L = 19` and `L = 21` and empty
for every odd `L <= 17` (the shortest `u`-`v` walk has length 15; AC already refutes `L <= 13`). By Lemma G it is
non-empty for every odd `L >= 19`. Computed by four implementations that agree: `pcfast.pc_answer` (BLAS products),
`zz.pc_numpy`, `zz.path_consistency` (bit masks), and `verify_pcfp.py`, written from the definitions without
importing `zz.py`, `pcfast.py` or the generators (it also re-checks the order axioms, P2 by brute force and the
answer by enumerating all down-sets: 625 and 663 down-sets, none with a `u`-`v` path).
The same holds for `H(2,3)` (`q = 29`, both versions). For `H(1,1)`, `H(1,2)`, `H(2,1)`, `H(1,3)`, `H(3,1)` PC
refutes, and it also refutes the *two-sided* order of `H(2,2)` (the first two gadgets between `s` and `a`, the other
two between the hub and `t`), `hubties_min.py`.

### 6.4 Graph form — checked
`realise_check.py` (`runs/realise-hubimp-22-strict.txt`), on the partial-order version of `H(2,2)`, with the
independent implementation of agent verify-equivalence: the graph `G(Π)` of `theory-dc.md` Theorem 13(b) has 417
vertices and 833 edges, is simple, `d(u,v) = 2`, `c(u,v) = N = 160`, and `G(Π) ∈ DC`; the prefix search of
`eqcore.pimc_flow_dfs` (independent of ZZ) finds no `u`-`v` path inside a minimum cut, so `cp(u,v) = c + 1 = 161`;
the pipeline of Theorem 13(a) applied to `G(Π)` returns the same `Q`, the same order and the same `R`, and PC on the
returned instance with `L = 21` is non-empty. So PC also fails as an algorithm for the open case of DC stated on
graphs.

### 6.5 Minimality — checked
`shrink_pcfp.py` (three seeds on the partial-order version, one on the classes version) tries every deletion of one
element other than `u`, `v` or of one real edge that keeps P2, the answer "no" and PC "yes": none exists, except the
edge `u b_β` of the partial-order version (redundant for P2), whose deletion gives a 22-element instance with 42 real
edges. The random runs of Section 5 (up to 21 elements) found no PC false positive. Whether a PC false positive with
P2 and at most 21 elements exists is not known.

### 6.6 Stronger relaxations on the hub family — checked
`variants.py` (`runs/variants.txt`), `hub_long_test.py` (`runs/hub-long.txt`):
- *Singleton PC* (fix the value of one position, run PC, delete the value if PC refutes, repeat): refutes `H(2,2)`
  and `H(2,3)` in both versions, and `H(2,2)` (classes version) also with more slack, `L = 25, 31, 41`
  (`spc_slack.py`, `runs/spc-slack.txt`). Interpretation: the fixed value acts as a fourth pebble that never moves
  (entry or exit), which is what Section 6.7 says is missing.
- *Simple-path CSP* (walks replaced by simple paths: edges at non-consecutive positions vertex-disjoint, consecutive
  edges different; one CSP for each odd `L <= q`): PC refutes every `L` for `H(2,2)` and `H(2,3)`, both versions.
- *Long routes* (`hubimp(..., long=True)`: every route also has a longer parallel version through a private top, so simple paths of several lengths exist): pending.

### 6.7 Anatomy of the failure (interpretation, not proved)
PC equals the existential 3-pebble game on the positions. To refute `H(2,2)` Spoiler must hold the entry `ε_i` and
the exit `ξ_j` (two pebbles) and find the blocked gadget `(i, j)` with the third. The PC-closed domains at `L = 19`
(printed in this session) show how Duplicator escapes: the walk may stall at `s` (`b_s t_s` repeated), at `a`
(`b_a t_a` repeated) and at the hub (`b_β ρ b_β` with any route element `ρ` as a peak), so the position of gadget
`(i, j)` is not fixed by the two hub pebbles, and pinning it needs two more pebbles. With no slack (`L <= 17`), with
the gadgets on both sides of the hub, with simple paths, or with one value fixed (singleton PC), the instance is
refuted. What an obstruction to PC needs, in the examples known: (1) a refutation that must hold two "mode facts"
(here entry and exit) while locating a third element on the walk, and (2) freedom in the position of that element.

## 7. Witnesses at the bottom: a polynomial class containing the PC counterexamples

**Theorem F (proved).** Let `(Q, ≤, R, u, v)` be a ZZ instance in which every two incomparable elements have a
common R-neighbour equivalent to `u` (*bottom witnesses*). Then
(i) the instance satisfies P2;
(ii) for every down-set `D` (`u ∈ D`, `v ∉ D`) and every shortest `u`-`v` path `Z'` of the graph `G_D` of R-edges
crossing `D`, two incomparable peaks of `Z'` are consecutive peaks (their positions differ by 2); hence if `A` holds
one element of each minimal class of the set of middle peaks of `Z'`, then `|A| <= 2`;
(iii) ZZ is decided in `O(q^2 (q + |R|))` time: for every set `A` of at most two elements (including `A = ∅`) put
`D_A = Q - ↑(A ∪ {v})` and search `G_{D_A}` for a `u`-`v` path.
Dually, with *top witnesses* (common R-neighbours equivalent to `v`): two incomparable valleys of `Z'` are
consecutive valleys, and `D_A = ↓(A ∪ {u})` over sets `A` of at most two elements decides ZZ.
Special case: a *lower hub*, an element equivalent to `u` with an R-edge to every middle element (an *upper hub*
dually); this is the case of the classes version of `H(m, m')`.

*Proof.* (i) Elements equivalent to `u` or `v` are comparable with every element, so two incomparable elements are
middle, and their bottom witness is strictly below both.
(ii) `Z' = x_0 ... x_L` is a consistent zigzag (its even vertices lie in `D`, its odd ones outside, and an R-edge joins
a smaller to a larger element). A peak lies outside `D`; an element `w` equivalent to `u` lies in `D` (`w ≤ u`).
Let `x_i`, `x_j` be incomparable peaks with `j >= i + 4` and `w` a bottom witness of them: the edges `w x_i`, `w x_j`
cross `D`, and `x_0 ... x_i w x_j ... x_L` is a `u`-`v` walk in `G_D` shorter than `Z'`, which contains a shorter
path; a contradiction. The elements of `A` are pairwise incomparable, so their positions differ pairwise by exactly
2, which three positions cannot do.
(iii) Let `Z` be a consistent zigzag, `D` the down-set generated by its valleys (`v ∉ D` by consistency), and `Z'` a
shortest `u`-`v` path in `G_D` (`Z` lies in `G_D`); let `A` be as in (ii). Every peak of `Z'` is equivalent to `v` or
is a middle peak, hence lies above an element of `A`; so all peaks lie in `↑(A ∪ {v})`. `D` is a down-set without
peaks and without `v`, so `D ∩ ↑(A ∪ {v}) = ∅`, i.e. `D ⊆ D_A`. Every valley of `Z'` lies in `D ⊆ D_A` and every peak
outside `D_A`, so `Z'` lies in `G_{D_A}`. Conversely `D_A` is a down-set (complement of an up-set) with `u ∈ D_A` (no
middle element and not `v` lies below `u`) and `v ∉ D_A`, and a `u`-`v` path in `G_{D_A}` is a consistent zigzag.
There are `O(q^2)` sets `A`; with the up-sets `↑x` precomputed (`O(q^2)` once) `D_A` costs `O(q)`, the search
`O(q + |R|)`. The dual statement follows by reversing the order and exchanging `u` and `v`. ∎

*Checked* (`bottom_witness.py`, `runs/bottom-witness-*.txt`): random instances with bottom witnesses or with top
witnesses (1-3 elements equivalent to `u`, 2-9 middle elements, 1-3 equivalent to `v`; witnesses added at random):
the algorithm of (iii) agrees with `exact_dfs` and with the enumeration of all down-sets on all 60,300 instances
(seeds 1-4; 29,791 yes, 30,509 no; about half with top witnesses). On these random no-instances AC was wrong 68 times
and PC never.
It answers "no" on `H(2,2)`, `H(2,3)`, `H(3,3)` (classes version).

*Remarks.* (1) The classes version of `H(m, m')` has the lower hub `b_β`, so PC fails on a polynomial subclass of
ZZ + P2. The partial-order version is not covered as stated (`b_β` is not equivalent to `u`, and the tops other
than `v` are not equivalent to `v`); it is a no-instance by Proposition 6.1 directly.
(2) In graph terms (Theorem 13(a)) a bottom witness is a vertex of `Q` that lies in every minimum `u`-`v` cut; the
condition says that every two vertices of `Q` that minimum cuts can separate in both orders have such a common real
neighbour.
(3) In the switch model (2CH, `dc-hardness.md`) bottom witnesses mean that all E-sides pairwise intersect. Then a
shortest solution uses at most two switches in E-mode, with no Helly or piercing assumption; this sharpens
`dc-hardness.md` Theorem H for this case. `theory-dc.md` Section 5 had the special case "all switches share one
bottom". What remains open is the mixed case, in which some incomparable pairs have only bottom witnesses, others
only top witnesses, and others only middle witnesses; a middle witness `w` of two valleys shortens a zigzag only when
`w ∉ D`, so (ii) does not extend to it.

**Why the hub construction needs order relations between middle elements (sketch).** In the switch model 2CH + P2
of `dc-hardness.md` (middle elements pairwise incomparable) an entry switch blocks a route only if the route is one of
its own sides. Every switch has one F-side; if it were a route in two gadgets it would join their nodes and act as
one long interval, which is the TIC situation that `dc-hardness.md` Theorem T solves (and where PC was never wrong in
the runs of that agent). So in 2CH each entry blocks the routes of one gadget only, and with `m, m' >= 2` some pair
(entry, exit) is unblocked. The counterexample needs one entry to block routes in several separated gadgets, which the
order relations `ε_i < ρ^A_{ij}` (or ties, `hubties_min.py`) provide.

**Conjecture (evidence only).** PC decides 2CH + P2. Evidence: the `sw` runs of Section 5, the rigid and TIC
families of `dc-hardness.md`, and the argument above. A PC false positive in 2CH + P2 would need the obstruction of
Section 6.7 without order relations between switches.

## 8. Control without P2: 3-colouring `K_4` — checked

`k4.py` (built in version 1 of this file, run now: `k4_base.py`, `runs/k4-base.log`; `k4.py isolated`,
`runs/k4-isolated.log`). Switch-model encoding of 3-colouring `K_4`: gadget `p` (a vertex of `K_4`) has three
parallel routes (colours) between `n_p` and `n_{p+1}`; for every edge `{p, q}` and colour `c` a switch
`σ(p, q, c)` has its E-side on route `(p, c)` and its F-side on route `(q, c)`. 29 nodes, 18 switches; ZZ form:
`q = 56`, `|R| = 81`, 120 switch pairs without P2. The answer is "no" (`K_4` is not 3-colourable).
- AC refutes `L = 25` and `L = 27` (no `u`-`v` walk that short); with the full `L = 55` AC and PC both leave every
  relation non-empty (107 s). So PC does not decide ZZ without P2, as expected from Theorem 13(c) of `theory-dc.md`
  unless P = NP, and this is the first explicit instance.
- For each of the 120 pairs without P2, every single connector (one existing or new node added to both E-sides, or to
  both F-sides) turns the answer into "yes". Since connectors only add connections, this encoding has no P2
  completion at all, in line with Lemma D and Section 3 of `dc-hardness.md` (route mixing: an E-E connector inside one
  vertex gadget lets a route change colour halfway, which makes the relaxed `K_4` colourable).

## 9. Next steps
1. A PC false positive in 2CH + P2 (switches pairwise incomparable), or a proof that PC decides 2CH + P2. A direct
   test: the hub family without order relations is impossible (Section 7); the next candidates are non-Helly side
   families with slack.
2. Stronger polynomial relaxations as candidate algorithms for ZZ + P2: singleton PC and the simple-path CSP decide
   the hub family; neither has been tested adversarially. A family that defeats `k`-consistency for every fixed `k`
   would need unboundedly many simultaneous "mode facts"; Theorem F shows that one hub cannot provide them.
3. The complexity of ZZ + P2 (the open case of DC) remains open; the hub family shows that P2 can be satisfied by a
   single hub at the price of a polynomial structure, so a hardness proof has to satisfy P2 by many different common
   neighbours (compare Consequence 1 of `dc-hardness.md` Section 5).

## 10. Scripts (`dc-algorithm/`)

| Script | What | Output |
|---|---|---|
| `chaincsp.py`, `test_chaincsp.py` | Theorem A | console (version 1) |
| `mcc.py` | Theorem B check | console (version 1) |
| `zz.py` | ZZ instances, exact solvers, CSP, AC, PC | library |
| `pcfast.py`, `test_pcfast.py` | PC with BLAS products | library |
| `hunt_pc.py`, `hunt2.py`, `runs/launch_*.sh` | adversarial runs | `runs/hunt*-*.log`, `runs/hunt*-*.jsonl` |
| `recheck_acfp.py` | re-check of the stored AC false positives | `runs/recheck-acfp.txt` |
| `families_pc.py` | structured families | `runs/families-A.txt`, `runs/families-C.txt` |
| `k4.py`, `k4_base.py` | `K_4` encoding (Section 8) | `runs/k4-base.log`, `runs/k4-isolated.log` |
| `hubimp.py` | hub family `H(m, m')`, both versions, long routes | `runs/hubimp.txt`, `runs/pcfp-hubimp-*.json` |
| `tieslib.py`, `hubties_min.py`, `hubties.py` | hub family with classes of middle elements (ties), orders of gadgets | `runs/hubties-min.txt`, `runs/pcfp-hubties-22.json` |
| `verify_pcfp.py` | independent check of a PC false positive (order, P2, all down-sets, PC) | console |
| `realise_check.py` | graph form and round trip with the code of verify-equivalence | `runs/realise-hubimp-22-strict.txt` |
| `shrink_pcfp.py` | deletion minimality | `runs/shrink-*.log`, `runs/pcfp-shrunk-*.json` |
| `variants.py`, `hub_long_test.py` | singleton PC, simple-path CSP | `runs/variants.txt`, `runs/hub-long.txt` |
| `chlib.py`, `hub_test.py` | 2CH helpers; hub instances in pure 2CH with unique routes (AC refutes all) | console |
| `sw2.py`, `sw_sat.py`, `test_relax*.py`, `big_relax.py`, `sat_*.py`, `mcc.py` | version 1 experiments | console |
