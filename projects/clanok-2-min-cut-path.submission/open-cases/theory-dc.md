# Open case of the class DC: d(u,v) = 2, c(u,v) >= 3 (agent theory-DC)

Status: working file, 2026-10-12. Scripts: `theory-dc-scripts/` (Python 3.13, import `checks/mcp.py` read-only).
Every claim is labeled **proved**, **sketch**, **conjecture**, **refuted** or **checked**.

## 1. Setting

`G = (V, E)` finite, simple, undirected, connected; `u != v`. `d`, `c`, `cp` as in article 1.
For `X ⊆ V`, `δ(X)` is the set of edges with exactly one end in `X`.
Fact (article 1, proof of Theorem 5.5): every minimum `u`-`v` cut equals `δ(A)` for the vertex set `A` of the
component of `u` in `G` minus the cut. The same holds for any pair `x, y`.

Open case: `G ∈ DC`, `d(u,v) = 2`, `c(u,v) >= 3`. Then `c <= cp <= c + 1`, and `cp = c` iff some minimum
`u`-`v` cut `δ(A)` contains a `u`-`v` path `P` (a cut-path with `c` edges is itself a minimum cut).
Every edge of such a `P` crosses `δ(A)`, so the vertices of `P = x_0 x_1 ... x_L` alternate:
`x_i ∈ A` iff `i` is even; `L` is odd and `L >= 3` (article 1, Lemma 5.4).

Notation used below: `Q = Q(u) = {u} ∪ {x : c(u,x) >= 3}`; `H` the multigraph of Section 3;
`R` the residual digraph of a maximum `u`-`v` flow; `cl(S)` the set of vertices reachable in `R` from `S`.

## 2. Lemmas with proofs

### Lemma 1 (bridges) — proved
Let `c(u,v) >= 2` and let `K` be the component of `G - B` containing `u`, where `B` is the set of bridges of `G`.
Then `v ∈ K`; for `x, y ∈ V(K)` the `x`-`y` paths of `G` are exactly those of `K`; hence `d_K = d_G` and
`c_K = c_G` on `V(K)`, the minimum `x`-`y` cuts of `G` and of `K` are the same edge sets, `cp_G(u,v) = cp_K(u,v)`
and the minimum cut-paths coincide, and `G ∈ DC` implies `K ∈ DC`.

*Proof.* Let `x, y` be vertices joined by a path `R'` that uses a bridge `b = pq`, with `x, ..., p, q, ..., y` in this
order. `G - b` has exactly two components, `C_p ∋ p` and `C_q ∋ q`; the subpath `x ... p` avoids `b`, so
`x ∈ C_p`, and likewise `y ∈ C_q`. Hence `b` separates `x` from `y`.
(i) If `c(u,v) >= 2`, no bridge separates `u` from `v`, so no `u`-`v` path uses a bridge; a `u`-`v` path then lies
in `G - B` and `v ∈ K`.
(ii) If `x, y ∈ V(K)`, they are joined in `G - B ⊆ G - b` for every bridge `b`, so no bridge separates them and no
`x`-`y` path uses a bridge; a path without bridges that starts in `K` stays in the component `K` of `G - B`.
(iii) By (ii) an edge set `S` meets every `x`-`y` path of `G` iff `S ∩ E(K)` meets every `x`-`y` path of `K`.
So `c_G(x,y) = c_K(x,y)`, a minimum cut of `G` lies in `E(K)` (else `S ∩ E(K)` is a smaller cut), and a minimum
cut of `K` is a cut of `G`. Distances agree by (ii).
(iv) `S` is a `u`-`v` cut-path of `G` iff `S` contains a `u`-`v` path (a path of `K`) and meets every `u`-`v` path
(all in `K`); both conditions depend only on `S ∩ E(K)`, so a minimum cut-path lies in `E(K)` and is a cut-path
of `K`, and conversely. (v) DC is a condition on `d` and `c` of pairs, which agree. ∎

From now on `G` is 2-edge-connected (Lemma 1 with `c(u,v) >= 3`).

### Lemma 2 (O1, any graph) — proved
Let `δ(A)` be a minimum `u`-`v` cut that contains a `u`-`v` path `P`. Then `P` has no vertex in any set
`X ⊆ V - {u, v}` with `|δ(X)| <= 2`.

*Proof.* Suppose `P` has a vertex in `X`. `P` starts and ends outside `X`, so it enters and leaves `X` through
two distinct edges of `δ(X)`; hence `δ(X) = {e_1, e_2} ⊆ P ⊆ δ(A)`. Write `e_i = x_i y_i` with `x_i ∈ X`,
`y_i ∉ X`. Let `D` be the set of edges of `δ(A)` with no end in `X`.
`|δ(A)| >= |D| + 2` (the two edges `e_1, e_2`). The sets `A - X` and `A ∪ X` contain `u` and not `v`.
An edge of `δ(A - X)` either has no end in `X` (then it lies in `δ(A)`, so in `D`) or is `e_i` with `y_i ∈ A`
(edges inside `X` have both ends outside `A - X`). So `|δ(A - X)| <= |D| + #{i : y_i ∈ A}`, and likewise
`|δ(A ∪ X)| <= |D| + #{i : y_i ∉ A}`. The two counts sum to 2, so one of the cuts has at most `|D| + 1 < |δ(A)|`
edges, which contradicts minimality. ∎

### Corollary 3 (path inside Q) — proved
If moreover `c(u,v) >= 3`, every vertex `x` of `P` lies in `Q(u)`. The relation `x ~ y` iff `x = y` or
`c(x,y) >= 3` is an equivalence (a cut separating `x` from `z` separates `y` from `x` or from `z`, so
`c(x,z) >= min(c(x,y), c(y,z))`), and `Q(u)` is the class of `u`; it contains `v`. If `G ∈ DC`, then
`d_G(x,y) <= 2` for all `x, y ∈ Q`.

*Proof.* Let `x ∈ V(P) - {u, v}` with `c(u,x) <= 2` and let `δ(Y)` be a minimum `x`-`u` cut, `x ∈ Y`, `u ∉ Y`.
If `v ∈ Y`, `δ(Y)` is a `u`-`v` cut with at most 2 < `c(u,v)` edges; so `Y ⊆ V - {u, v}` and Lemma 2 is
contradicted. ∎

### Lemma 4 (O2, ears) — proved
Let `G` be 2-edge-connected, `Q = Q(u)`, `v ∈ Q`. Call `X ⊆ V` an *ear set* if `X != ∅`, `X ∩ Q = ∅`,
`|δ(X)| = 2`.
1. Every vertex outside `Q` lies in an ear set.
2. If ear sets `X, Y` intersect or are joined by an edge, `X ∪ Y` is an ear set.
3. The maximal ear sets (*ears*) partition `V - Q`; no edge joins two ears; each ear induces a connected
   subgraph; both edges of `δ(X)` have their outer end in `Q`. Write `δ(X) = {pa, sb}`, `p, s ∈ Q`, `a, b ∈ X`
   (`a = b` and `p = s` are allowed).
4. Let `δ(A)` be a minimum `u`-`v` cut and `X` an ear. If `p, s ∈ A` then `X ⊆ A`; if `p, s ∉ A` then
   `X ∩ A = ∅`; if exactly one of `p, s` lies in `A`, then `δ(A)` contains exactly one edge of
   `E[X] = E(G[X]) ∪ δ(X)`, and `δ(A ∪ X)`, `δ(A - X)` are minimum cuts that agree with `δ(A)` outside `E[X]`.
5. A `u`-`v` path inside a minimum `u`-`v` cut has no vertex in an ear (Corollary 3).

*Proof.* (1) For `x ∉ Q` take a minimum `x`-`u` cut `δ(Y)`, `x ∈ Y`, `u ∉ Y`: `|δ(Y)| <= 2`, and
`|δ(Y)| = 2` because `G` is connected and has no bridge. A vertex `q ∈ Y ∩ Q` would give `c(q,u) <= 2`, so
`Y ∩ Q = ∅`. (2) If `X ∩ Y != ∅`: submodularity `|δ(X ∪ Y)| + |δ(X ∩ Y)| <= |δ(X)| + |δ(Y)| = 4`, and both
sets are non-empty proper subsets (`X ∪ Y` misses `Q`), so each has at least 2 boundary edges; hence
`|δ(X ∪ Y)| = 2`. If `X ∩ Y = ∅` with `t >= 1` edges between them, `|δ(X ∪ Y)| = 4 - 2t <= 2`, hence `= 2`.
(3) Distinct maximal ear sets are disjoint and non-adjacent by (2), and cover `V - Q` by (1). A component `Z` of
`G[X]` has `δ(Z) ⊆ δ(X)` and `|δ(Z)| >= 2`, so there is one component. The outer end `w` of an edge of `δ(X)` is
not in another ear (no edge joins two ears), so `w ∈ Q`.
(4) Let `p, s ∈ A` and `Z = X - A != ∅`. Every edge of `δ(Z)` ends in `X ∩ A` or is an edge of `δ(X)` whose outer
end `p` or `s` lies in `A`; so `δ(Z) ⊆ δ(A)`. As `Z ∩ A = ∅`, `δ(A ∪ Z) = δ(A) Δ δ(Z) = δ(A) - δ(Z)` has at
most `c - 2` edges and separates `u` from `v`, a contradiction. The case `p, s ∉ A` is symmetric (apply the
argument to `V - A`). If `p ∈ A`, `s ∉ A`: `E[X]` contains a `p`-`s` path, which crosses `δ(A)`, so
`|δ(A) ∩ E[X]| >= 1`; `δ(A ∪ X) = (δ(A) - E[X]) ∪ {sb}` and `δ(A - X) = (δ(A) - E[X]) ∪ {pa}` have at most
`c` edges, so `|δ(A) ∩ E[X]| = 1` and both are minimum. ∎

### Proposition 5 (reduction to a multigraph on Q) — proved
Let `H` be the multigraph on `Q` with the edges of `G[Q]` (*real edges*) and one edge `ps` for every ear with
`p != s` (*ear edges*). Then `c_H(u,v) = c_G(u,v)`, `A ↦ A ∩ Q` maps the minimum `u`-`v` cuts of `G` onto those
of `H` with `|δ_G(A)| = |δ_H(A ∩ Q)|`, and: some minimum `u`-`v` cut of `G` contains a `u`-`v` path iff some
minimum `u`-`v` cut of `H` contains a `u`-`v` path of real edges.
For `x, y ∈ Q`: `d_G(x,y) <= 2` iff `x, y` are adjacent in `G[Q]`, or have a common neighbour in `Q`, or there
is a *short ear* with attachments `x, y` (an ear whose two boundary edges share the inner end `a = b`).

*Proof.* For `B ⊆ Q` with `u ∈ B`, `v ∉ B` let `A(B) = B ∪ ⋃{X : ear with p ∈ B}`; then
`|δ_G(A(B))| = |δ_H(B)|` (ears with both attachments on one side contribute 0, split ears exactly 1 edge, `pa`
or `sb`). Hence `c_G <= c_H`. For a minimum cut `δ(A)` of `G`, Lemma 4(4) gives `|δ_G(A)| = |δ_H(A ∩ Q)|`, so
`c_H <= c_G`, and `A ∩ Q` is a minimum cut of `H`; every minimum cut `B` of `H` is the image of `A(B)`.
A path inside a minimum cut of `G` lies in `G[Q]` (Corollary 3), and its edges are real edges of `δ_H(A ∩ Q)`.
Conversely a real path inside `δ_H(B)` lies inside `δ_G(A(B))`. For distances: a common neighbour `w ∉ Q` of
`x, y ∈ Q` lies in an ear `X` with `xw, yw ∈ δ(X)`, so `δ(X) = {xw, yw}`, a short ear. ∎

### Problem Π (equivalent form of the open case) — proved equivalence
*Instance:* a set `Q`, a simple graph `R` on `Q` (real edges), integer weights `W(x,y) >= [xy ∈ R]` on pairs
(`W - R` = number of ear edges), `u, v ∈ Q` not adjacent in `R`, such that every two vertices of `Q` are adjacent
in `R`, have a common `R`-neighbour, or carry an ear edge. *Question:* does some minimum `u`-`v` cut of the
weighted graph `W` contain a `u`-`v` path of `R`?

By Proposition 5 the open case of DC reduces to Π (in linear time after one computation of the 3-edge-connected
class `Q`, i.e. `O(|V|)` max-flow computations with value at most 3 or a 3-edge-connected-components algorithm).
Conversely an instance of Π is realised by the simple graph `G(Π)` with one new vertex of degree two per ear edge;
`G(Π) ∈ DC` (pairs in `Q` are at distance at most two, new vertices have degree two), `d(u,v) = 2`, and a degree-two
vertex is never inside a path in a minimum cut (Lemma 2 with `X = {w}`), so the answers agree; the minimum
cuts of `G(Π)` and `W` correspond as in Lemma 4(4). (The condition `c(x,y) >= 3` inside `Q` is not needed for
this direction.)
Checked: 216 random Π-instances realised as graphs; `c`, the answer, `cp_brute` and DC membership agree
(`explore_pi.py 1 3000`, 0 mismatches).

### Lemma 6 (O3/O6: test of a given path) — proved
A `u`-`v` path `P = x_0 ... x_L` lies in some minimum `u`-`v` cut iff `L` is odd and the maximum number of
edge-disjoint paths between `E_P = {x_0, x_2, ...}` and `O_P = {x_1, x_3, ...}` equals `c(u,v)`; equivalently
(Picard-Queyranne, Theorem 1 of the 1979 report, read in `knowledge/literature/PicardQueyranne1980.md`) iff no
vertex of `O_P` is reachable from `E_P` in `R`, and then `cl(E_P)` is the smallest such cut.

*Proof.* If `P ⊆ δ(A)`, then `E_P ⊆ A`, `O_P ∩ A = ∅`, so `δ(A)` separates the two sets with `c` edges; any
cut separating them separates `u ∈ E_P` from `v ∈ O_P`, so the separation value is exactly `c`. Conversely a
minimum `E_P`-`O_P` cut `δ(A)` (`E_P ⊆ A`) with `c` edges is a minimum `u`-`v` cut, and every edge `x_i x_{i+1}`
joins `E_P` and `O_P`, so it crosses. Closed sets of `R` containing `u` and not `v` are exactly the minimum cuts;
the smallest closed set containing `E_P` is `cl(E_P)`. ∎
For paths of length 3 (O3) this is one max-flow per edge `ab` with `ua, bv ∈ E`.

### Lemma 7 (one side is thin) — proved
In an instance of Π, let `δ(A)` be a minimum `u`-`v` cut of `W`, `B = Q - A`. Call a vertex *incident* if it is
an end of an edge (real or ear) of `δ(A)`. Then all vertices of `A` are incident or all vertices of `B` are
incident. If all vertices of the side `K` containing `r ∈ {u, v}` are incident, then
`Σ_{x ∈ K - r} deg_C(x) <= Σ_{x ∈ K - r} W(r,x)` and `|K| <= c`, where `deg_C(x)` is the number of cut edges at `x`.
For a path `P` of length `2k+1` inside `δ(A)`, `r` has `W(r, K - r) >= |K| - 1 + k`.

*Proof.* `x ∈ A`, `y ∈ B` not incident: they are not joined by a real or ear edge (it would be a cut edge),
and a common `R`-neighbour `z` gives a cut edge `xz` or `zy`; this contradicts the distance condition.
Every cut edge has exactly one end in `K`, so `c = Σ_{x ∈ K} deg_C(x) >= |K|`; with `c <= deg_W(r) =
deg_C(r) + W(r, K - r)` this gives the inequality. The `k` interior vertices of `P` in `K` have `deg_C >= 2`. ∎
(In `G` itself: one of the sets `A ∩ Q`, `B ∩ Q` consists of vertices incident to `δ_G(A)`; this is
Lemma 5.3 of article 1 restricted to `Q`.)

## 3. Conjecture status

### O4 (bounded path length) — refuted, both forms
**Theorem 8 (proved).** For `k >= 1` let `G_k` have vertices `x_0, ..., x_{2k+1}`, `a_1, ..., a_k`,
`b_1, ..., b_k` (`n = 4k + 2`), `u = x_0`, `v = x_{2k+1}`, and edges: the path `P = x_0 x_1 ... x_{2k+1}`; all
pairs of even-indexed `x`'s (a clique on `E = {x_0, x_2, ..., x_{2k}}`); all pairs of odd-indexed `x`'s (a clique on
`O = {x_1, ..., x_{2k+1}}`); `a_i` adjacent to `u` and `x_{2i}`; `b_j` adjacent to `x_{2j-1}` and `v`.
Then `G_k ∈ DC`, `d(u,v) = 2`, `c(u,v) = cp(u,v) = 2k+1`, and `E(P)` is the only minimum `u`-`v` cut that
contains a `u`-`v` path; the only such path is `P`, of length `2k+1`.

*Proof.* DC: two `x`'s of equal parity are adjacent; `x_{2i}`, `x_{2j+1}` with `i != j` have the common neighbour
`x_{2j}`; `a_i`, `b_j` have degree 2. `d(u,v) = 2`: `u x_{2k} v` is a path, and `u v` is not an edge (the only
edges between `E` and `O` are path edges, and `x_0`'s is `x_0 x_1`, `x_1 != v`).
Let `A = E ∪ {a_1, ..., a_k}`. The edges between `A` and `V - A` are exactly the `2k+1` edges of `P`.
Flow of value `2k+1`: for a path edge `e` with even end `x_{2i}` and odd end `x_{2j-1}` route `u → x_{2i}` inside
`A` and `x_{2j-1} → v` inside `V - A`, using for `x_{2i}` (`i >= 1`, tail of two path edges) the routes
`u x_{2i}` and `u a_i x_{2i}`, for `x_{2j-1}` (`j <= k`, head of two path edges) the routes `x_{2j-1} v` and
`x_{2j-1} b_j v`, and the empty route at `u = x_0` and at `v = x_{2k+1}`. These `2k+1` paths are edge-disjoint,
so `c = 2k+1` and `δ(A) = E(P)` is a minimum cut with `cp = c`.
All minimum cuts (closed sets of the residual digraph `R` of this flow, Picard-Queyranne): `v` has no
in-arc in `R` (all its edges carry flow into `v`). `cl(u) = {u}` (all edges at `u` carry flow out of `u`).
`cl(a_i) = {a_i, u}`. For `i >= 1`, `x_{2i}` has arcs to `u`, `a_i` (reverse arcs) and to every even `x` (clique
edges without flow), so `cl(x_{2i}) = A`. An odd `x_{2j-1}`, `j <= k`, has arcs to `x_{2j-2}` (reverse of a
path edge) and to every odd `x` other than `v` (clique edges without flow), and no arc to `b_j` or `v`; so
`cl(x_{2j-1}) = A ∪ (O - {v})` and `cl(b_j) = cl(x_{2j-1}) ∪ {b_j}`.
Hence every minimum cut `A'` is (i) `{u} ∪ S` with `S ⊆ {a_i}`, or (ii) `A`, or (iii) `A ∪ (O - {v}) ∪ T`
with `T ⊆ {b_j}`. A `u`-`v` path inside `δ(A')` has length `>= 3` (odd, `d = 2`) and its interior vertices lie in
`Q = E ∪ O` (Corollary 3). In case (i) its third vertex would lie in `A' - {u} ⊆ {a_i}`; in case (iii) its
second vertex would lie in `(V - A') ∩ Q = {v}`, i.e. the path would be the edge `uv`. Both are impossible, so
`A' = A`, and `δ(A) = E(P)` contains no `u`-`v` path other than `P`. ∎
Checked: `ex_long_path.py`, `xcheck_cuts.py` (k = 2, 3, 4: DC membership, all minimum cuts by two independent
enumerations for `n <= 16`, `cp_brute`, no length-3 path in a minimum cut). The experiments agent found the same
family independently (`experiments/results-family.txt`, up to `k = 5`) and reports no 9-vertex graph with a
path of length `>= 5` inside a minimum cut (`experiments/results-extend9.txt`), so `G_2` (10 vertices) is the
smallest example with length 5 by their exhaustive check.

Consequence: no bounded length `L` suffices; the `n^{O(L)}` test of O3 does not decide DC.

### C1 (one generator) — refuted
Candidate: if some minimum cut contains a `u`-`v` path, then so does `cl({u, x})` for some `x`, or the largest
minimum cut avoiding some `y` (complement of the vertices that reach `{v, y}` in `R`).
Held on about 7900 planted yes-instances (`crit_variants.py`, seeds 11-18), each one-sided version failing a few
times; **fails** on the Π-instance `Q = {0..5}`, `u = 0`, `v = 1`, real edges `04 05 13 15 23 24 45`, ears
`03 ×2, 04 ×1, 12 ×2, 15 ×1` (realised graph: 12 vertices). The only witness cut is `A = {0, 3, 4}` with path
`0-5-4-2-3-1`; `cl(3) = {0,3}`, `cl(4) = {0,4}`, and dually `{1,2,5}` needs the two generators `2, 5`
(`test_S.py` seed 26; `inspect_pi.py`).


### Bounded number of generators — refuted
**Family `Z_k` (Π-instances, checked k = 1..5; `antichain.py`).** `Q = {u, v, x_1..x_k, y_1..y_k}`; real edges:
the path `u y_1 x_1 y_2 x_2 ... y_k x_k v`, `u x_i`, `v y_j`; ears: `x_i y_j` for every pair that is not a path edge;
`W(u, x_i)` and `W(v, y_j)` topped up with ears to the cut degree of `x_i` (resp. `y_j`) in `A = {u} ∪ X`.
Distances: `x`'s pairwise via `u`, `y`'s via `v`, `u`-`y_j` via `x_j`, `x_i`-`v` via `y_{i+1}`, `u`-`v` via `y_1`.
Cut function (computed by hand, confirmed): `c(A) = k^2 + 2 + 2(k - s)(k - t)` for `s = |A ∩ X|`, `t = |Y - A|`,
so the minimum cuts are `{u} ∪ S` (`S ⊆ X`) and `{u} ∪ X ∪ T` (`T ⊆ Y`); `c = k^2 + 2`; the only witness is
`{u} ∪ X` with the path of length `2k + 1`; `X` and `Y` are antichains of the residual order, so the witness needs
`k` generators on either side (two generators fail from `k = 3`).
Variant `Z'_k` (`antichain2.py`): the real edges `u x_i`, `v y_j` replaced by edges to a bottom vertex `w_0` and a
top vertex `z_0` (tied to `u`, `v` by heavy ears), distances to `u`, `v` by balanced ear pairs: the same unique
witness, and now the far-apart incomparable evens `x_i` are not real neighbours of `u` (refutes "H1" below).

### Other candidate polynomial criteria — refuted or not exact (all on random/planted Π-instances, `q <= 12`)
| Criterion | Result | Script |
|---|---|---|
| some witness among the two extreme minimum cuts | fails (about 10% of yes-instances) | `crit_variants.py` |
| some witness among unions of levels of the residual order (height or depth) | fails, smallest `q = 6` | `levels.py` seed 74 |
| local windows: a simple alternating path with "even does not reach odd" for index distance `<= w` is consistent | per path false for `w = 3` and `w = 5` (`q = 11`) | `locality_path.py` seed 41 |
| existence of an alternating walk with consecutive (W1) or distance-3 (W3) constraints | 7 false positives in 18000 instances | `walks.py` seeds 51-56 |
| H1: in a shortest witness, far incomparable evens are real neighbours of `u` | refuted by `Z'_k` | `shortest_struct.py`, `antichain2.py` |

### Positive partial results
**Proposition 9 (proved).** A `u`-`v` path inside a minimum cut has at most `c(u,v)` edges (its edges are
distinct cut edges). Hence for `c(u,v) ∈ {3, 4}` the length-3 test of Lemma 6 decides `cp = c` in polynomial time,
and in general the test of all alternating paths of length at most `c` decides it in `n^{O(c)}` time.
Theorem 8 shows the bound is attained (`L = c` in `G_k`).

**Proposition 10 (proved).** Fix a maximum flow given as `c` edge-disjoint `u`-`v` paths `π_1..π_c`. Every class
of the residual order contains a vertex of some `π_i`, and along each `π_i` the order is monotone
(`π_i[s+1]` reaches `π_i[s]` by the reverse arc of a flow edge). So the order has width at most `c`, a minimum cut is
determined by one prefix of each `π_i`, and there are at most `(n+1)^c` minimum cuts.
*Proof.* A class without flow vertex has all its edges without flow, so both residual arcs of each edge exist and
the class is closed under neighbours, hence it is `V` (G connected), which contains `u`. Each class meets some
`π_i`; on `π_i` the class of `π_i[s+1]` reaches that of `π_i[s]`, so the classes on `π_i` form a chain. ∎
Also: every edge of a path inside a minimum cut carries flow from its even to its odd end in every maximum flow
(a minimum cut is saturated from the `u`-side); so the path alternates flow directions (O6).

**Proposition 11 (proved; uncrossing of incomparable classes, any graph).** If no minimum cut is forced to put
`x` and `y` in a fixed order (neither "`x` in `A` implies `y` in `A`" nor the converse), then no edge (real or ear)
joins `x` and `y`.
*Proof.* Take minimum cuts `A_1 ∋ x`, `y ∉ A_1` and `A_2 ∋ y`, `x ∉ A_2`. `A_1 ∪ A_2`, `A_1 ∩ A_2` are minimum, so
equality holds in submodularity, which means `e(A_1 - A_2, A_2 - A_1) = 0`. ∎
**Corollary 12 (P2, uses DC).** In Π, two incomparable vertices have a common real neighbour that lies above both
or below both in the order.

### The open case as a problem on an ordered set
**Definition (problem ZZ).** An instance is `(Q, ≤, R, u, v)`: a finite preorder `≤` on `Q` with least element `u`
and greatest element `v` (`x < y` means `x ≤ y` and not `y ≤ x`), and a set `R` of pairs `{a, b}` with `a < b`
(*real edges*), `{u, v} ∉ R`. A *zigzag* is a path `u = x_0, x_1, ..., x_L = v` of the graph `(Q, R)` with
`x_i < x_{i+1}` for even `i` and `x_i > x_{i+1}` for odd `i` (valleys at even, peaks at odd positions; `L` odd).
It is *consistent* if no valley is `≥` a peak. Question: is there a consistent zigzag?
*Condition P2:* every two incomparable elements have a common `R`-neighbour that is above both or below both.

**Theorem 13 (proved; equivalence).**
(a) Let `G ∈ DC`, `d(u,v) = 2`, `c(u,v) >= 3`, and `H` the multigraph of Proposition 5. Put `x ≤ y` iff every
minimum `u`-`v` cut of `H` that contains `y` contains `x` (so `u` is least, `v` greatest), and let `R` be the
real edges of `H` between elements that are not equivalent. Then the real edges join comparable elements
(Proposition 11), P2 holds (Corollary 12), the minimum cuts are exactly the down-sets that contain `u` and not `v`,
and `cp(u,v) = c(u,v)` iff the ZZ-instance has a consistent zigzag.
(b) Conversely, let `(Q, ≤, R, u, v)` satisfy P2 and have at least three comparable pairs. Give every pair `a < b`
weight one (a real edge if `{a,b} ∈ R`, an ear otherwise) and add an ear `u a` (if `a != u`) and an ear `b v`
(if `b != v`) for every such pair; join equivalent elements by `M > ` (number of pairs) ears. In the resulting
simple graph `G(Π)` (ears = vertices of degree two) every cut `δ(A)` with `u ∈ A ∌ v` that does not split a class has
`|δ(A)| = N + 2·#{a < b : a ∉ A, b ∈ A}`, `N` the number of comparable pairs (each pair contributes 1, 1, 1 or 3
in the four cases `a, b ∈ A`; `a ∈ A ∌ b`; `a, b ∉ A`; `b ∈ A ∌ a`). So the minimum cuts are exactly the
down-sets, `c = N >= 3`, `d(u,v) = 2` (ear `uv`, no real edge), `G(Π) ∈ DC` (comparable pairs carry an ear,
incomparable ones a common real neighbour by P2), and `cp(u,v) = c(u,v)` iff a consistent zigzag exists.
Hence **the open case of DC is polynomially equivalent to ZZ restricted to instances with P2.**
(c) **Without P2, ZZ is NP-complete**, and so is the question `cp(u,v) = c(u,v)` for pairs with `d(u,v) = 2` in
general graphs. In NP: a zigzag is checked by one closure computation (Lemma 6). Hardness from 3-SAT: elements
`u, d, e_0, a_1..a_{n+1}, T_i, F_i (i <= n), c_1..c_{m+1}, P_{j,k}` (literal `k` of clause `j`), `v`; order
generated by `u <` everything `< v`, `e_0 < d`, `e_0 < a_1`, `T_i, F_i < a_i, a_{i+1}`, `c_1 < a_{n+1}`,
`c_j, c_{j+1} < P_{j,k}`, and the *conflict relations* `P_{j,k} < F_i` if the literal is `x_i`, `P_{j,k} < T_i`
if it is `¬x_i`; `R` = the pairs `u d, e_0 d, e_0 a_1, T_i a_i, T_i a_{i+1}, F_i a_i, F_i a_{i+1}, c_1 a_{n+1},
c_j P_{j,k}, c_{j+1} P_{j,k}, c_{m+1} v`. Every zigzag is `u d e_0 a_1 X_1 a_2 ... X_n a_{n+1} c_1 P_{1,k_1} c_2 ...
c_{m+1} v` with `X_i ∈ {T_i, F_i}`; the only valley-above-peak pairs are the conflict relations, so a consistent
zigzag is a satisfying assignment (`x_i` true iff `X_i = T_i`) together with a true literal per clause.
Checked: `test_realise.py` (400 random posets: minimum cuts = down-sets and `c = N` in all; 174 with P2 realised
as graphs: all in DC, `d = 2`, and `cp = c` iff a consistent zigzag); `sat_general.py` (150 random formulas with
up to 3 variables and 4 clauses: answer = satisfiability in all).

**Proposition 14 (proved; a polynomial special case).** If `R` is bipartite with sides `V_0 ∋ u`, `V_1 ∋ v` and
every `x ∈ V_0`, `y ∈ V_1` are comparable, then ZZ is solvable in `O(|Q| · |R|)` time.
*Proof.* Valleys lie in `V_0`, peaks in `V_1`. For `y ∈ V_1` let `N(y) = {x ∈ V_0 : x < y}`. The sets `N(y)` form a
chain: if `x ∈ N(y) - N(y')` and `x' ∈ N(y') - N(y)`, comparability gives `y' < x` and `y < x'`, so
`y < x' < y' < x < y`. A zigzag is consistent iff every valley lies below every peak. Given a consistent zigzag,
let `y*` be a peak with the smallest `N(y*)`; all valleys lie in `N(y*)` and all peaks `y` satisfy
`N(y) ⊇ N(y*)`. Conversely every zigzag inside `N(y*) ∪ {y : N(y) ⊇ N(y*)}` is consistent. So try every `y*`
and search the restricted graph. ∎
(This is the case "every possible valley is comparable with every possible peak"; 3-SAT needs incomparable
valley-peak pairs, because the conflict relation of a formula is in general not of this chain type.)

## 4. Algorithm

Input `G ∈ DC`, `u != v`. Output `cp(u,v)` and a minimum cut-path.
1. Compute `d = d(u,v)` (BFS) and `c = c(u,v)` (at most three augmentations decide `c <= 2`; otherwise a full
   maximum flow, `O(c·m)`).
2. `c <= 1` or `d <= 1`: `cp = c + d - 1`; output a minimum cut plus a shortest path (article 1, Lemma 2.3).
3. `c = 2`: square decomposition and the linear-time test of the SPEC (S1-S11).
4. `d >= 3`: then `c <= 2` in DC; handled above.
5. `d = 2`, `c >= 3` (open case): `cp ∈ {c, c+1}`.
   a. Reduce to the 2-edge-connected component (Lemma 1), compute `Q = Q(u)` (`O(n)` flows of value at most 3),
      the ears (components of `G - Q`) and `H` (Proposition 5): `O(n·m)`.
   b. From one maximum flow in `H`, the residual digraph and its strong components give all minimum cuts as
      closed sets (Picard-Queyranne).
   c. Decide whether some minimum cut contains a real `u`-`v` path:
      - `c ∈ {3, 4}`: only paths of length 3 can occur (Proposition 9): for every real edge `ab` with `ua`, `bv`
        real edges, one closure test (Lemma 6): `O(m · (n + m))`.
      - general `c`: enumerate the alternating paths of length at most `c` and test each, or enumerate the at most
        `(n+1)^c` minimum cuts (prefixes of the flow paths, Proposition 10) and search each for a real path:
        `n^{O(c)}` time. **No polynomial algorithm is known** (Section 5).
   d. If a path `P` inside a minimum cut `δ(A)` is found: `cp = c` and `δ(A)` (lifted to `G` by Lemma 4(4)) is a
      minimum cut-path. Otherwise `cp = c + 1` and a minimum cut plus a shortest path is one.

## 5. Open gaps

**Main gap: the complexity of ZZ under P2** (equivalently of the open case of DC, Theorem 13). Status after this
work: polynomial for `c <= 4` and in the special cases of Proposition 14 and of chains (a total preorder has only
`|Q|` down-sets); `n^{O(c)}` in general; NP-complete without P2. Neither a polynomial algorithm nor a hardness
proof is known.

**Why the 3-SAT reduction does not survive P2 (analysis, not a theorem).** The reduction of Theorem 13(c) has many
incomparable pairs (`T_i` vs `T_l`, `T_i` vs most `P_{j,k}`, `P` vs `P`). P2 demands a common real neighbour `w`
for each, above both or below both. Such a `w` opens a new zigzag segment: an upper `w` lets the path go
`x ↗ w ↘ y` with `x, y` as valleys, a lower `w` gives `x ↘ w ↗ y` with `x, y` as peaks. In a series construction
this skips gadgets. The usual cure, a conflict that forbids the new segment, is not available: if `w < x` and
`w ≥ p` for a peak `p` on every zigzag, then `x ≥ p` and `x` itself can never be a valley (and dually for upper
`w`). For a valley `x` that carries a conflict `x > y` (a literal vertex), even "x is never a peak" cannot be
enforced by an always-present valley `g ≥ x`, since then `g > y` and `y` could never be a peak. Making the
conflict vertices pairwise comparable instead forces the chain structure of Proposition 14, which is
polynomial. The same obstruction appears for the switch encoding below. A hardness proof would need gadgets
whose P2-segments lead nowhere; a polynomial algorithm would have to exploit that every incomparable pair is
joined by such a segment.

**A clean subproblem (switch model SW).** Fixed elements: bottom ones (in every minimum cut, `u` among them),
top ones (in none, `v` among them), always-cut real edges between bottom and top elements; *switches*, pairwise
incomparable, each with real edges to a set `N_b(s)` of bottom and `N_t(s)` of top elements and balanced weights,
so that every assignment of sides to the switches is a minimum cut. A switch on the `v`-side joins `N_b(s)`, on
the `u`-side `N_t(s)`. P2 reads: every two switches share a bottom or a top neighbour. SW is a special case of
ZZ (realisable in DC by Theorem 13(b)). Without P2 SW is NP-hard (the switches are crossings that a path can use
in one direction only; standard reduction, sketch). With P2: polynomial if all switches share one bottom element
(guess the two switches through which a zigzag enters and leaves the merged bottom part); in random instances
(`sw_gaps.py`, 300000 trials) the relaxation that allows both modes of a switch is wrong in 1848 cases, and up to
four switches must be fixed jointly to see the obstruction (`sw.py`, `sw_minswitch.py`: up to 6 switches
needed on a shortest valid connection). Complexity of SW + P2: open.

**Smaller gaps.**
- Whether `G_2` (10 vertices) is the smallest graph with a path of length 5 inside a minimum cut relies on the
  experiments agent's exhaustive 9-vertex search (`experiments/results-extend9.txt`), not on a proof.
- FPT in `c`? The order has width at most `c` and the path length is at most `c`, but the consistency condition
  is global; no FPT algorithm is known.
- Lemma 7 (one side thin) is proved but not used by any algorithm; the per-root inequality
  `Σ_{x ∈ K - r} deg_C(x) <= W(r, K - r)` does not force the thin side into `N(r)` (`thin_stats.py`: 116 of 1993
  thin sides have a vertex not adjacent to the root).

## 6. Checks

| Script | What | Result |
|---|---|---|
| `dctools.py` | minimum cuts by residual closures, path test of Lemma 6 | library |
| `ex_long_path.py`, `xcheck_cuts.py` | Theorem 8 for k = 2, 3, 4 | as stated; enumerations agree |
| `pi.py`, `explore_pi.py` | Problem Π, realisation cross-check | 216 instances, 0 mismatches |
| `crit_variants.py`, `test_S.py` | single-generator criteria | C1 refuted (seed 26) |
