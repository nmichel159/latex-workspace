# The open case of DC in quasi-polynomial time: the assembled proof

Status: complete (draft for the referee), 2026-10-28 (agent qp-assemble, round 6c). Working file of AI agents; not
read by the author; not in the manuscript. Label of the result: **proved** (every part reviewed, see the Source
lines); this assembly itself is not yet refereed (planned: `verify/rv-qp-referee.md`). Paths are relative to
`open-cases/` unless they start with `knowledge/`.

This file is one proof, with one numbering, of the theorem below. It assembles the reviewed chain
open case of DC → ZZ + P2 (`theory-dc.md` Theorem 13(a)) → general switch form (`r4-general.md` §5.1) → Lemmas 6.2,
6.3, 6.4 → Lemma 8.1, Theorem 8.2 → IDESC, Corollary 8.3 (`r5-core.md` §6.2, §6.3, §8.2, §8.3), with every repair
stated by the reviews `verify/equivalence.md`, `verify/rv-core-65.md`, `verify/rv-r6-core.md`, `verify/rv-r6-chain.md`
(list in §8). It uses neither Theorems R, Q, 6.5, Corollary 6.5', the switch model 2CH, forced-mode propagation, nor
Theorem 13(b), (c). No new mathematics is added; where the route differs from the sources in a step, §9 says so.

**Main theorem (Theorem 7.1, Corollary 7.2).** There is a deterministic algorithm that, given a graph `G` of DC with
`n` vertices and vertices `u`, `v` with `d(u,v) = 2` and `c(u,v) >= 3`, decides whether `cp(u,v) = c(u,v)` in time
`2^{O(log^3 n)}`. Hence this problem is not NP-complete unless NP ⊆ QP, and if the Exponential Time Hypothesis holds,
it is not NP-hard.

*Conventions.* `log` is to base 2 and `ln` is natural. All statements share one counter per section (Definition 1.1,
Lemma 1.3, ...). Each numbered statement ends with a line "Source: ... Reviewed: ...". Inline mathematics is in
backticks, as in the other files of this folder; `∎` ends a proof.

*Numbering against the sources.*

| Here | Source |
|---|---|
| Lemma 1.3 | `theory-dc.md` §1 (minimum cuts as `δ(S)`, `cp = c` criterion), Corollary 3 (triangle inequality) |
| Lemma 1.4 | identity of `verify/equivalence.md` §3 (review of Proposition 11) |
| Lemmas 2.1, 2.2, 2.3, 2.4 | `theory-dc.md` Lemma 1; Lemma 2 with Corollary 3; Lemma 4; Proposition 5 |
| Definition 2.5, Lemmas 2.6, 2.7, 2.8, Theorem 2.9 | `theory-dc.md` Theorem 13(a), Proposition 11, Corollary 12; proofs of `verify/equivalence.md` §3 |
| Construction 3.1, Lemmas 3.2, 3.3 | `r4-general.md` §5.1; proof of `verify/rv-r6-chain.md` §1.2 |
| Lemma 3.4 | `r5-core.md` §6.1, §8.2 (F0); `verify/rv-r6-chain.md` §1.3 |
| Definition 4.1, Lemma 4.2 | `r5-core.md` §3.1, §6.1, §6.3, §8.2 (F0, F3, F4); `r4-switch.md` §2 (F1) |
| Lemmas 4.3, 4.4, 4.5 | `r5-core.md` Lemmas 6.2, 6.3, 6.4 |
| Definition 5.1, Lemma 5.2, Theorem 5.3 | `r5-core.md` §8.2: terms, Lemma 8.1, Theorem 8.2 |
| Definition 6.1, Theorem 6.2 | `r5-core.md` §8.3: IDESC |
| Theorem 7.1, Corollary 7.2 | `r5-core.md` §8.3: Corollary 8.3 |

## 1. Definitions

### 1.1 Graphs, cuts and cut-paths

**Definition 1.1 (cuts and cut-paths).** Let `G` be a finite simple graph with vertex set `V` and edge set `E(G)`, and
`n = |V|`. For `S ⊆ V`, `δ(S)` is the set of edges with exactly one end in `S` (`δ_G(S)` when the graph must be named).
For distinct vertices `x`, `y`, `d(x,y)` is their distance; an *`x`–`y` cut* is a set `C ⊆ E(G)` such that `G − C` has
no `x`–`y` path; `c(x,y)` is the least size of an `x`–`y` cut, and an `x`–`y` cut of that size is *minimum*. For
distinct vertices `u`, `v`, a *`u`–`v` cut-path* is a set `F ⊆ E(G)` that contains the edge set of a `u`–`v` path and
a `u`–`v` cut; `cp(u,v)` is the least size of a `u`–`v` cut-path.
Source: `knowledge/research/min-cut-path.md` §1 (definition of article 1); `theory-dc.md` §1. Reviewed:
`verify/rv-r6-chain.md` §1.1 (as used in the chain).

**Definition 1.2 (the class DC and the open case).** DC is the class of connected graphs in which every two distinct
vertices `x`, `y` satisfy `d(x,y) <= 2` or `c(x,y) <= 2`. An instance of the *open case* is a triple `(G, u, v)` with
`G ∈ DC` and vertices `u`, `v` with `d(u,v) = 2` and `c(u,v) >= 3`; the question is whether `cp(u,v) = c(u,v)`.
Source: `theory-dc.md` §1; `status.md` (question of the author). Reviewed: `verify/rv-r6-chain.md` §1.1.

**Lemma 1.3 (minimum cuts as vertex sets).** Let `G` be connected and `x`, `y`, `z` distinct vertices.
(a) For every `S ⊆ V` with `x ∈ S ∌ y`, `δ(S)` is an `x`–`y` cut. Every minimum `x`–`y` cut `C` equals `δ(S)` for the
vertex set `S` of the component of `x` in `G − C`. Hence `c(x,y) = min{|δ(S)| : x ∈ S ⊆ V − {y}}`.
(b) `c(x,z) >= min(c(x,y), c(y,z))`.
(c) For distinct `u`, `v`: `cp(u,v) >= c(u,v)`, with equality if and only if some minimum `u`–`v` cut contains the
edge set of a `u`–`v` path.
By (a) we also call a set `S ⊆ V` with `u ∈ S ∌ v` and `|δ(S)| = c(u,v)` a *minimum `u`–`v` cut* (vertex form), and say
that it *contains* a path `π` if `E(π) ⊆ δ(S)`.
Source: `theory-dc.md` §1 (fact quoted from article 1, proof of Theorem 5.5; "`cp = c` iff some minimum cut contains a
`u`-`v` path"), §2 Corollary 3 (triangle inequality). Reviewed: `verify/equivalence.md` §1 (Corollary 3: the usual
triangle inequality of local edge connectivity).

*Proof.* (a) A path from `x ∈ S` to `y ∉ S` has an edge with exactly one end in `S`, so `δ(S)` is an `x`–`y` cut. Let
`C` be a minimum `x`–`y` cut and `S` the vertex set of the component of `x` in `G − C`; then `y ∉ S`. An edge of `δ(S)`
not in `C` would put its outer end into the component of `x`; so `δ(S) ⊆ C`. As `δ(S)` is an `x`–`y` cut and `C` is
minimum, `δ(S) = C`.
(b) Let `C` be a minimum `x`–`z` cut. If `y` were joined to both `x` and `z` in `G − C`, then so would be `x` and `z`;
hence `C` is an `x`–`y` cut or a `y`–`z` cut, and `|C| >= min(c(x,y), c(y,z))`.
(c) A cut-path contains a `u`–`v` cut, so `cp(u,v) >= c(u,v)`. If a cut-path `F` has `|F| = c(u,v)`, the cut `C ⊆ F`
has `|C| >= c(u,v) = |F|`, so `C = F` is a minimum cut containing the edge set of a path. Conversely a minimum cut that
contains the edge set of a `u`–`v` path is a cut-path with `c(u,v)` edges. ∎

**Lemma 1.4 (uncrossing).** Let `H` be a multigraph with non-negative edge weights; write `w(δ(S))` for the total
weight of `δ(S)` and `w(S_1, S_2)` for the total weight of the edges between disjoint sets `S_1`, `S_2`. For all vertex
sets `S_1`, `S_2`,

    w(δ(S_1)) + w(δ(S_2)) = w(δ(S_1 ∩ S_2)) + w(δ(S_1 ∪ S_2)) + 2 w(S_1 − S_2, S_2 − S_1).

In particular `|δ(S_1 ∪ S_2)| + |δ(S_1 ∩ S_2)| <= |δ(S_1)| + |δ(S_2)|` in a graph. For distinct vertices `u`, `v` of
`H`, call `S` with `u ∈ S ∌ v` and least `w(δ(S))` a *minimum `u`–`v` cut of `H`* and that least value `c_H(u,v)`. If
`S_1`, `S_2` are minimum `u`–`v` cuts of `H`, so are `S_1 ∩ S_2` and `S_1 ∪ S_2`, and `w(S_1 − S_2, S_2 − S_1) = 0`.
Source: `verify/equivalence.md` §3 (identity used in the review of Proposition 11); `theory-dc.md` §2 Lemma 4
(submodularity), Proposition 11. Reviewed: `verify/equivalence.md` §3 (holds for every non-negative weighting).

*Proof.* Split the vertices into `I = S_1 ∩ S_2`, `X = S_1 − S_2`, `Y = S_2 − S_1` and the rest `O`, and count the
contribution of one edge to the left and to the right side. An edge inside one part contributes 0 to both. Edges
`I X`, `I Y`, `X O`, `Y O` contribute 1 to both sides (for `I X`: to `δ(S_2)` and `δ(S_1 ∩ S_2)`; for `X O`: to
`δ(S_1)` and `δ(S_1 ∪ S_2)`; the other two by symmetry). An edge `I O` contributes 2 to both sides. An edge `X Y` lies in
`δ(S_1)` and `δ(S_2)` and in neither `δ(S_1 ∩ S_2)` nor `δ(S_1 ∪ S_2)`, and is counted twice by the last term. The
inequality follows with unit weights. If `S_1`, `S_2` are minimum `u`–`v` cuts, then `S_1 ∩ S_2` and `S_1 ∪ S_2`
contain `u` and not `v`, so each has weight at least `c_H(u,v)`; the identity and `w >= 0` force both to equal
`c_H(u,v)` and the last term to vanish. ∎

### 1.2 Preorders

**Definition 1.5 (preorders).** A *preorder* `<=` on a finite set is a reflexive and transitive relation. We write
`x < y` if `x <= y` and not `y <= x`; `x ~ y` (*equivalent*, *tied*) if `x <= y` and `y <= x`; `[x]` for the class of
`x`; `x ∥ y` (*incomparable*) if neither `x <= y` nor `y <= x`. For a set `S`, `↓S = {x : x <= y for some y ∈ S}`,
`↑S = {x : x >= y for some y ∈ S}`, `↓x = ↓{x}`, `↑x = ↑{x}`; so `↓x − [x] = {y : y < x}` and `↑x − [x] = {y : y > x}`.
A *down-set* `D` satisfies `↓D = D`, an *up-set* `↑D = D`. Complements of down-sets are up-sets, intersections and
unions of down-sets are down-sets, `↓S` is a down-set, and the complement of `↑S` is a down-set. If `x <= y < z` or
`x < y <= z`, then `x < z` (if `z <= x`, then `z <= y` in the first case and `y <= x` in the second). For every two
elements exactly one of `x <= y`, `y < x`, `x ∥ y` holds.
Source: `r5-core.md` §6.1, §8.2 (notation). Reviewed: `verify/rv-r6-core.md` §2.1.

### 1.3 The problem ZZ

**Definition 1.6 (ZZ and P2).** An instance of *ZZ* is `(Q, <=, R, u, v)`: a finite set `Q` with a preorder `<=` such
that `u <= x <= v` for every `x ∈ Q`, and a set `R` of pairs `{a, b} ⊆ Q` with `a < b` (*real edges*, written `ab`
with `a < b`) such that `{u, v} ∉ R`. For a down-set `D` of `Q` with `u ∈ D ∌ v`, `G_D` is the graph on `Q` whose edges
are the real edges with exactly one end in `D`. The instance is a *yes-instance* if `u` and `v` are connected in `G_D`
for some such `D`. It satisfies *P2* if every two incomparable elements `x`, `y` have a common `R`-neighbour `z` with
`z < x` and `z < y` (a *lower witness*) or with `z > x` and `z > y` (an *upper witness*).
(Equivalently, a consistent zigzag exists, `r4-brief.md` §1; that form is not used here.)
Source: `r4-brief.md` §1; `theory-dc.md` §2 (Definition (problem ZZ), condition P2). Reviewed: `verify/equivalence.md`
§3; `verify/rv-r6-chain.md` §1.2.

### 1.4 The general switch form

**Definition 1.7 (general switch form).** An instance consists of a finite set `Ω` of *nodes* with two *terminals*
`s, t ∈ Ω`; a finite set `M` of *switches*, `m = |M|`, with a preorder `<=`; for every switch `w` an *E-side* and an
*F-side*, with node sets `E_w ⊆ Ω` and `F_w ⊆ Ω`; and a set of *middle edges*, ordered pairs `(z, w)` of switches with
`z < w`, each with a *private node* `ρ(z,w) ∈ Ω` that lies in `F_z` and in `E_w` and in no other side. Sides are
labelled (a side is a switch together with E or F); we denote a side by its node set, `E_w` or `F_w`.
`LMN(w) = {z : (z, w) is a middle edge}` and `UMN(w) = {z : (w, z) is a middle edge}` are the lower and upper middle
neighbours of `w`. The instance satisfies *P2* if every two incomparable switches `x`, `y` have a common E-node
(`E_x ∩ E_y ≠ ∅`), or a common F-node (`F_x ∩ F_y ≠ ∅`), or a *lower middle witness* `z ∈ LMN(x) ∩ LMN(y)`, or an
*upper middle witness* `z ∈ UMN(x) ∩ UMN(y)`.
Source: `r4-general.md` §5.1 (Setting); `r5-core.md` §6.1. Reviewed: `verify/rv-core-65.md` §2.1 (model and P2 in
switch form); `verify/rv-r6-chain.md` §1.2.

**Definition 1.8 (mode vectors, conflict pairs, valid paths).** A *mode vector* is a down-set `D` of `(M, <=)`;
switches in `D` are in *F-mode*, the others in *E-mode*. The mode vector `D` *picks* `F_w` for `w ∈ D` and `E_w` for
`w ∉ D`; it *connects* `s` and `t` if `s = t` or there are picked sides `X_1, .., X_r` (`r >= 1`) with `s ∈ X_1`, `t ∈ X_r` and
`X_i ∩ X_{i+1} ≠ ∅` for `i < r`. The instance is a *yes-instance* if some mode vector connects `s` and `t`.
A *conflict pair* is a pair of sides `{E_w, F_z}` with `w <= z` (in particular `{E_w, F_w}`). A *valid path* is a
sequence `P = X_1 .. X_r` (`r >= 1`) of sides of pairwise distinct switches with `s ∈ X_1`, `t ∈ X_r`,
`X_i ∩ X_{i+1} ≠ ∅` for `i < r`, no two of which form a conflict pair. Its sides are its *members*; a switch is *on*
`P` if one of its sides is a member, and then `pos(w)` is the index of that member. `W_E` (`W_F`) is the set of switches
whose E-side (F-side) is a member, `Up = ↑W_E` and `L = ↓W_F`. A valid path is *shortest* if no valid path has fewer
members.
Source: `r4-general.md` §5.1; `r5-core.md` §6.1, §8.2. Reviewed: `verify/rv-r6-core.md` §2.1; `verify/rv-r6-chain.md`
§1.3; `verify/rv-core-65.md` §2.1.

## 2. Reduction of the open case to ZZ + P2

Throughout this section `(G, u, v)` is an instance of the open case with `n` vertices. Only the direction "graph →
ZZ" of `theory-dc.md` Theorem 13, i.e. Theorem 13(a), is used.

**Lemma 2.1 (bridges).** Let `K` be the component containing `u` of the graph obtained from `G` by deleting all
bridges. Then:
(a) `v ∈ V(K)`;
(b) for `x, y ∈ V(K)` the `x`–`y` paths of `G` are exactly the `x`–`y` paths of `K`; hence `d_K(x,y) = d_G(x,y)`,
`c_K(x,y) = c_G(x,y)`, and an edge set is a minimum `x`–`y` cut of `G` if and only if it is a minimum `x`–`y` cut of
`K`;
(c) some minimum `u`–`v` cut of `G` contains the edge set of a `u`–`v` path if and only if some minimum `u`–`v` cut of
`K` does;
(d) the graph `K` is connected, has no bridge and lies in DC, and `d_K(u,v) = 2`, `c_K(u,v) >= 3`.
Source: `theory-dc.md` §2, Lemma 1. Reviewed: `verify/equivalence.md` §1 (holds; the line "`K` has no bridge" was added
there and is part of (d)); `verify/rv-r6-chain.md` §1.1.

*Proof.* A bridge `b = pq` of the connected graph `G` lies on no cycle, and `G − b` has exactly two components
`C_p ∋ p` and `C_q ∋ q`. (∗) If a path with ends `x`, `y` uses `b`, traversed as `x .. p q .. y`, its sub-paths
`x .. p` and `q .. y` avoid `b`, so `x ∈ C_p`, `y ∈ C_q`, and `b` separates `x` from `y`.
(a) A `u`–`v` path through a bridge `b` would make `{b}` a `u`–`v` cut by (∗), against `c(u,v) >= 3`. As `G` is
connected, a `u`–`v` path exists; it uses no bridge, so it lies in the component `K` of `u`.
(b) Let `x, y ∈ V(K)`. They are joined by a path of `K`, which avoids every bridge `b`, so `x`, `y` lie in one
component of `G − b`, and by (∗) no `x`–`y` path of `G` uses `b`. Hence every `x`–`y` path of `G` avoids all bridges
and, starting in `K`, lies in `K`; conversely every path of `K` is a path of `G`. So the distances agree, and an edge set
`C ⊆ E(G)` meets every `x`–`y` path of `G` if and only if `C ∩ E(K)` meets every `x`–`y` path of `K`. Therefore
`c_G(x,y) = c_K(x,y)`, a minimum cut of `G` lies in `E(K)` (otherwise `C ∩ E(K)` is a smaller cut), and a minimum cut of
`K` is a cut of `G` of the same size.
(c) Apply (b) with `x = u`, `y = v`: the minimum cuts and the `u`–`v` paths are the same in `G` and `K`.
(d) The graph `K` is a component, hence connected. An edge `e` of `K` is not a bridge of `G`, so it lies on a cycle of `G`; that
cycle contains no bridge, so it lies in the component `K`, and `e` is not a bridge of `K`. DC is a condition on `d` and
`c` of pairs of vertices, which agree by (b); so `K ∈ DC`, `d_K(u,v) = 2` and `c_K(u,v) = c_G(u,v) >= 3`. ∎

From now on all distances, cuts and connectivities are taken in `K`; `c = c_K(u,v) = c_G(u,v)`, and

    Q = {u} ∪ {x ∈ V(K) : c_K(u,x) >= 3};   v ∈ Q because c >= 3.

**Lemma 2.2 (paths inside minimum cuts lie in `Q`).**
(a) Let `S` be a minimum `u`–`v` cut of `K` that contains a `u`–`v` path `π`, and let `X ⊆ V(K) − {u, v}` with
`|δ_K(X)| <= 2`. Then `π` has no vertex in `X`.
(b) Every vertex of such a path `π` lies in `Q`.
(c) Every two distinct `x, y ∈ Q` satisfy `c_K(x,y) >= 3` and `d_K(x,y) <= 2`.
Source: `theory-dc.md` §2, Lemma 2 and Corollary 3. Reviewed: `verify/equivalence.md` §1 (both hold; the counts of the
proof are exact).

*Proof.* (a) Suppose that `π` has a vertex in `X`. It starts at `u ∉ X` and ends at `v ∉ X`, so the edge by which it
first enters `X` and the edge by which it last leaves `X` are two distinct edges of `δ(X)`; as `|δ(X)| <= 2`,
`δ(X) = {e_1, e_2}` with `e_i = x_i y_i`, `x_i ∈ X`, `y_i ∉ X`, and `e_1, e_2 ∈ E(π) ⊆ δ(S)`. Let `J` be the set of edges
of `δ(S)` with no end in `X`; then `|δ(S)| >= |J| + 2`. The sets `S − X` and `S ∪ X` contain `u` and not `v`. An edge
with no end in `X` lies in `δ(S − X)`, and in `δ(S ∪ X)`, if and only if it lies in `δ(S)`, i.e. in `J`; an edge with
both ends in `X` lies in neither; `e_i` lies in `δ(S − X)` if and only if `y_i ∈ S`, and in `δ(S ∪ X)` if and only if
`y_i ∉ S`. Hence `|δ(S − X)| = |J| + #{i : y_i ∈ S}` and `|δ(S ∪ X)| = |J| + #{i : y_i ∉ S}`. The two counts sum to 2,
so one of the two sets has at most `|J| + 1 < |δ(S)| = c` boundary edges, and by Lemma 1.3(a) it gives a `u`–`v` cut
with fewer than `c` edges: a contradiction.
(b) The ends `u`, `v` lie in `Q`. Let `x ∈ V(π) − {u, v}` and suppose `x ∉ Q`, so `c_K(u,x) <= 2`. By Lemma 1.3(a) there is `Y` with
`x ∈ Y ∌ u` and `|δ(Y)| = c_K(x,u) <= 2`. If `v ∈ Y`, then `δ(Y)` is a `u`–`v` cut with at most `2 < c` edges; so
`v ∉ Y`, `Y ⊆ V(K) − {u, v}`, and `x ∈ Y` contradicts (a).
(c) If `x = u` or `y = u`, `c_K(x,y) >= 3` by the definition of `Q`; otherwise Lemma 1.3(b) gives
`c_K(x,y) >= min(c_K(x,u), c_K(u,y)) >= 3`. As `K ∈ DC` (Lemma 2.1(d)), `d_K(x,y) <= 2`. ∎

**Lemma 2.3 (ears).** Call `Y ⊆ V(K)` an *ear set* if `Y ≠ ∅`, `Y ∩ Q = ∅` and `|δ_K(Y)| = 2`.
(a) Every vertex of `V(K) − Q` lies in an ear set.
(b) If two ear sets intersect or are joined by an edge, their union is an ear set.
(c) The inclusion-maximal ear sets (*ears*) are exactly the vertex sets of the components of `K − Q`; they partition
`V(K) − Q`, no edge joins two ears, and every ear `Y` has `δ_K(Y) = {pa, p'a'}` with `a, a' ∈ Y` and `p, p' ∈ Q` (its
*attachments*; `a = a'` or `p = p'` is allowed).
(d) Let `E[Y] = E(K[Y]) ∪ δ_K(Y)` for an ear `Y`. If the attachments `p`, `p'` of `Y` are distinct and `S ⊆ V(K)`
contains exactly one of them, then `δ_K(S) ∩ E[Y] ≠ ∅`. Every edge of `K` lies either in `K[Q]` or in `E[Y]` for exactly
one ear `Y`.
Source: `theory-dc.md` §2, Lemma 4 (1)-(3), and the first step of the split case of Lemma 4(4) ("`E[X]` contains a
`p`-`s` path, which crosses `δ(A)`"). Reviewed: `verify/equivalence.md` §1 (holds; ears at `u` or `v`, ears with
`p = p'`, ears with `a = a'` are covered).

*Proof.* Every set `Z` with `∅ ≠ Z ⊊ V(K)` has `|δ_K(Z)| >= 2`: at least one edge since `K` is connected, and a single
edge would be a bridge, which `K` has not (Lemma 2.1(d)). (∗∗)
(a) Let `x ∈ V(K) − Q`; then `x ≠ u` and `c_K(u,x) <= 2`. By Lemma 1.3(a) there is `Y` with `x ∈ Y ∌ u` and
`|δ(Y)| = c_K(x,u) <= 2`, and `|δ(Y)| = 2` by (∗∗). If `q ∈ Y ∩ Q`, then `q ≠ u` and `δ(Y)` separates `q` from `u`, so
`c_K(u,q) <= 2`, against `q ∈ Q`. So `Y` is an ear set containing `x`.
(b) Let `Y`, `Y'` be ear sets. If `Y ∩ Y' ≠ ∅`, then `Y ∪ Y'` and `Y ∩ Y'` are non-empty and miss `u`, so by (∗∗) and
Lemma 1.4, `4 <= |δ(Y ∪ Y')| + |δ(Y ∩ Y')| <= |δ(Y)| + |δ(Y')| = 4`, whence `|δ(Y ∪ Y')| = 2`. If `Y ∩ Y' = ∅` and
`t_0 >= 1` edges join them, then `|δ(Y ∪ Y')| = 4 − 2 t_0 <= 2`, and `>= 2` by (∗∗). In both cases `Y ∪ Y'` misses `Q`.
(c) By (b), two distinct maximal ear sets are disjoint and not joined by an edge (their union would be a larger ear
set); by (a) every vertex of `V(K) − Q` lies in a maximal ear set. Let `Y` be an ear. Distinct components `Z` of `K[Y]`
have disjoint sets `δ(Z) ⊆ δ(Y)` (no edge joins `Z` to `Y − Z`), each of size at least 2 by (∗∗); as `|δ(Y)| = 2`,
`K[Y]` is connected. The outer end of an edge of `δ(Y)` lies outside `Y` and in no other ear, so it lies in `Q`. Hence
the ears are connected subsets of `K − Q`, pairwise non-adjacent, covering `V(K) − Q`: they are the vertex sets of the
components of `K − Q`.
(d) Let `δ(Y) = {pa, p'a'}` with `p ≠ p'`. The walk `p a .. a' p'`, with `a .. a'` a path in the connected graph `K[Y]`,
is a `p`–`p'` path with edges in `E[Y]`; since `S` contains exactly one of its ends, one of its edges lies in `δ(S)`.
An edge with an end in an ear `Y` has its other end in `Y` or in `Q` by (c), so it lies in `E[Y]` and in no `E[Y']`,
`Y' ≠ Y`; an edge with no end in an ear lies in `K[Q]`. ∎

**Lemma 2.4 (the multigraph `H`).** Let `H` be the multigraph on `Q` whose edges are the edges of `K[Q]` (*real
edges*) and, for every ear with distinct attachments `p`, `p'`, one edge `pp'` (its *ear edge*); every edge has weight
1, so `|δ_H(B)|` counts edges with multiplicity. For every ear `Y` fix an order `(p_Y, p'_Y)` of its attachments, and
for `B ⊆ Q` put `A(B) = B ∪ ⋃{Y : Y an ear with p_Y ∈ B}`. Then:
(a) `A(B) ∩ Q = B` and `|δ_K(A(B))| = |δ_H(B)|` for every `B ⊆ Q`;
(b) `|δ_K(S)| >= |δ_H(S ∩ Q)|` for every `S ⊆ V(K)`;
(c) `c_H(u,v) = c`; for every minimum `u`–`v` cut `S` of `K`, `S ∩ Q` is a minimum `u`–`v` cut of `H`, and for every
minimum `u`–`v` cut `B` of `H`, `A(B)` is a minimum `u`–`v` cut of `K`;
(d) some minimum `u`–`v` cut of `K` contains a `u`–`v` path if and only if some minimum `u`–`v` cut `B` of `H` has a
`u`–`v` path of real edges all of which lie in `δ_H(B)`;
(e) every two distinct `x, y ∈ Q` are joined by a real edge or by an ear edge, or have a common neighbour `z ∈ Q` in
`K` (so that `xz`, `yz` are real edges).
Source: `theory-dc.md` §2, Proposition 5. Reviewed: `verify/equivalence.md` §1 (holds).

*Proof.* By Lemma 2.3(d), every edge of `K` is a real edge or lies in `E[Y]` for exactly one ear `Y`.
(a) The equality `A(B) ∩ Q = B` holds since ears miss `Q`. A real edge lies in `δ_K(A(B))` if and only if it lies in `δ_H(B)`. Edges of
`K[Y]` never lie in `δ_K(A(B))`, since `Y ⊆ A(B)` or `Y ∩ A(B) = ∅`. Let `δ(Y) = {p_Y a, p'_Y a'}`. If `p_Y ∈ B`, then
`Y ⊆ A(B)`, `p_Y a` is not cut, and `p'_Y a'` is cut if and only if `p'_Y ∉ B`; if `p_Y ∉ B`, then `Y ∩ A(B) = ∅`,
`p_Y a` is not cut, and `p'_Y a'` is cut if and only if `p'_Y ∈ B`. So the ear contributes 1 exactly when `B` contains
exactly one of `p_Y`, `p'_Y`; this needs `p_Y ≠ p'_Y`, and then it is exactly the case that its ear edge lies in
`δ_H(B)`. Otherwise it contributes 0.
(b) Every real edge of `δ_H(S ∩ Q)` lies in `δ_K(S)`. For every ear edge of `δ_H(S ∩ Q)`, `S` contains exactly one
attachment of its ear `Y`, so `δ_K(S)` contains an edge of `E[Y]` (Lemma 2.3(d)); these edges are distinct for distinct
ears and are not real edges.
(c) For a minimum `u`–`v` cut `B` of `H`, `A(B)` contains `u` and not `v` by (a), so
`c <= |δ_K(A(B))| = |δ_H(B)| = c_H(u,v)`. For a minimum `u`–`v` cut `S` of `K`, `S ∩ Q` contains `u` and not `v`, so
`c_H(u,v) <= |δ_H(S ∩ Q)| <= |δ_K(S)| = c` by (b). Hence `c_H(u,v) = c`, and all these inequalities are equalities.
(d) Let `S` be a minimum `u`–`v` cut of `K` containing a `u`–`v` path `π`. By Lemma 2.2(b) all vertices of `π` lie in
`Q`, so its edges are real edges; each has exactly one end in `S`, hence exactly one in `S ∩ Q`, a minimum cut of `H`
by (c). Conversely, let `B` be a minimum cut of `H` and `π` a `u`–`v` path of real edges in `δ_H(B)`. Each edge of `π`
has both ends in `Q` and exactly one of them in `B = A(B) ∩ Q`, so it lies in `δ_K(A(B))`, a minimum cut of `K` by (c).
(e) By Lemma 2.2(c), `d_K(x,y) <= 2`. If `xy ∈ E(K)`, it is a real edge. Otherwise `x`, `y` have a common neighbour
`z`. If `z ∈ Q`, then `xz`, `yz` are real edges. If `z ∉ Q`, then `z` lies in an ear `Y` (Lemma 2.3(c)), and `xz`, `yz`
are two distinct edges of `δ_K(Y)`; as `|δ_K(Y)| = 2`, the attachments of `Y` are `x ≠ y`, and `H` has the ear edge
`xy`. ∎

**Definition 2.5 (the ZZ instance of `(G, u, v)`).** For `x, y ∈ Q` let `x <= y` if every minimum `u`–`v` cut of `H`
that contains `y` contains `x`. Let `R` be the set of real edges of `H` whose ends are not equivalent. The *ZZ instance
of* `(G, u, v)` is `(Q, <=, R, u, v)`.
Source: `theory-dc.md` §2, Theorem 13(a). Reviewed: `verify/equivalence.md` §3; `verify/rv-r6-chain.md` §1.1.

**Lemma 2.6 (uncrossing of incomparable elements).** `<=` is a preorder on `Q` with `u <= x <= v` for every `x ∈ Q`,
and `u < v`. If `x, y ∈ Q` are incomparable, no edge of `H` (real or ear) joins them. Hence every edge of `R` joins two
strictly comparable elements, and `{u, v} ∉ R`.
Source: `theory-dc.md` §2, Proposition 11 and the first sentence of Theorem 13(a). Reviewed: `verify/equivalence.md` §3
(holds, also for multigraphs and weighted graphs).

*Proof.* Reflexivity and transitivity follow from the definition. Every minimum cut contains `u`, so `u <= x`; none
contains `v`, so `x <= v`. A minimum `u`–`v` cut of `H` exists and contains `u` but not `v`, so not `v <= u`: `u < v`.
Let `x ∥ y`. As not `x <= y`, some minimum cut `S_2` contains `y` and not `x`; as not `y <= x`, some minimum cut `S_1`
contains `x` and not `y`. By Lemma 1.4 (weights = multiplicities), no edge joins `S_1 − S_2 ∋ x` and `S_2 − S_1 ∋ y`.
An edge of `R` joins non-equivalent ends, which are comparable by what was just shown, hence strictly comparable.
`uv ∉ E(K)` since `d_K(u,v) = 2`, so `{u, v}` is not a real edge. ∎

**Lemma 2.7 (minimum cuts are down-sets).** A set `D ⊆ Q` is a minimum `u`–`v` cut of `H` if and only if `D` is a
down-set of `(Q, <=)` with `u ∈ D ∌ v`.
Source: `theory-dc.md` §2, Theorem 13(a) (asserted there without argument); proof of `verify/equivalence.md` §3 (i).
Reviewed: `verify/equivalence.md` §3 (holds with the repair given there, which is this proof).

*Proof.* Let `D` be a minimum cut, `y ∈ D` and `x <= y`; by the definition of `<=`, `x ∈ D`. So `D` is a down-set, and
`u ∈ D ∌ v`. Conversely let `D` be a down-set with `u ∈ D ∌ v`, and `y ∈ D`. Some minimum cut contains `y`: otherwise
`v <= y` holds vacuously and `v ∈ D`. The intersection `C(y)` of the minimum cuts containing `y` is a minimum cut (Lemma
1.4, applied repeatedly), and by the definition of `<=` it equals `{x : x <= y}`, which lies in `D` as `D` is a
down-set. So `D = ⋃_{y ∈ D} C(y)` is a union of minimum cuts (non-empty, as `u ∈ D`), hence a minimum cut by Lemma
1.4. ∎

**Lemma 2.8 (P2).** The ZZ instance `(Q, <=, R, u, v)` satisfies P2.
Source: `theory-dc.md` §2, Corollary 12 (stated there without proof); proof of `verify/equivalence.md` §3. Reviewed:
`verify/equivalence.md` §3 (holds with the repair given there, which is this proof); `verify/rv-r6-chain.md` §1.1 (DC is
used exactly here).

*Proof.* Let `x ∥ y` (so `x ≠ y`). By Lemma 2.4(e), `x` and `y` are joined by a real or an ear edge, or have a common
neighbour `z ∈ Q` with real edges `xz`, `yz`. The first two cases are excluded by Lemma 2.6. By Lemma 2.6, `z` is
comparable with `x` and with `y`. If `x <= z <= y` or `y <= z <= x`, then `x` and `y` would be comparable; hence
`z <= x` and `z <= y`, or `z >= x` and `z >= y`. If `z ~ x`, comparability of `z` and `y` would make `x` and `y`
comparable; so `z` is not equivalent to `x`, and likewise not to `y`. Hence `z < x` and `z < y`, or `z > x` and `z > y`,
and `xz`, `yz` join non-equivalent elements, so they belong to `R`: `z` is a lower or an upper witness. ∎

**Theorem 2.9 (reduction).** Let `(G, u, v)` be an instance of the open case with `n` vertices. Its ZZ instance
`(Q, <=, R, u, v)` satisfies P2 and `u < v`, has `|Q| <= n` and `|R| <= |E(G)|`, and is computable in time polynomial
in `n`. Moreover `cp(u,v) = c(u,v)` if and only if it is a yes-instance of ZZ.
Source: `theory-dc.md` §2, Theorem 13(a); `verify/equivalence.md` §3 (ii); `verify/rv-r6-chain.md` §1.1 (direction
used, sizes, cost) and §3 items 2, 4. Reviewed: `verify/equivalence.md` §3, §6 (holds with the repairs included here);
`verify/rv-r6-chain.md` §1.1, §2.2 (holds; all 121 588 open-case pairs of graphs with at most 8 vertices and further
runs, 0 mismatches; sizes on 249 649 records).

*Proof.* P2 is Lemma 2.8; `u < v` and the form of `R` are Lemma 2.6. `Q ⊆ V(K) ⊆ V` and `R ⊆ E(K[Q]) ⊆ E(G)`.
*Answer.* By Lemma 1.3(c), `cp_G(u,v) = c_G(u,v)` if and only if some minimum `u`–`v` cut of `G` contains the edge set
of a `u`–`v` path; by Lemma 2.1(c) and Lemma 1.3(a) if and only if some minimum `u`–`v` cut `S` of `K` (vertex form)
contains a `u`–`v` path; by Lemma 2.4(d) if and only if some minimum `u`–`v` cut `B` of `H` has a `u`–`v` path of real
edges inside `δ_H(B)`. By Lemma 2.7 these `B` are exactly the
down-sets `D` with `u ∈ D ∌ v`. For such `D`, a real edge with exactly one end in `D` joins non-equivalent elements (a
down-set contains, with an element, its whole class), so it lies in `R`; conversely an edge of `R` with exactly one end
in `D` is a real edge in `δ_H(D)`. So the real edges inside `δ_H(D)` are exactly the edges of `G_D`, and the condition
says that `u` and `v` are connected in `G_D` for some such `D`.
*Time.* The bridges and `K` take `O(n + |E(G)|)`. The set `Q` takes one test "`c_K(u,x) >= 3`" per vertex, each by at
most three augmenting-path searches. The ears are the components of `K − Q` (Lemma 2.3(c)), with their attachments read off
their boundary edges; this gives `H`, with `|Q| <= n` vertices and at most `|E(G)| + n` edges. The value `c` takes one maximum-flow
computation. For the preorder: `x <= y` holds if `x = y`, `x = u` or `y = v`; otherwise it holds if and only if no
minimum `u`–`v` cut of `H` contains `y` but not `x`, i.e. if and only if the least `|δ_H(S)|` over all `S` with
`{u, y} ⊆ S ⊆ Q − {x, v}` exceeds `c`, which is one maximum-flow computation between `{u, y}` and `{x, v}`. So at most
`|Q|^2` flow computations in `H`, and `R` follows. All of this is polynomial in `n`. ∎

## 3. The general switch form of a ZZ instance

**Construction 3.1 (switch form of a ZZ instance).** Let `(Q, <=, R, u, v)` be a ZZ instance with `u < v`, and let
`[u]`, `[v]` be the classes of `u` and `v` (disjoint, as `u < v`). The *switches* are the elements of
`M = Q − [u] − [v]`, with the restriction of `<=`; `m = |M|`. A real edge `ab` (`a < b`) is of one of four kinds:
`a ∈ [u]`, `b ∈ [v]`; `a ∈ [u]`, `b ∈ M`; `a ∈ M`, `b ∈ [v]`; `a, b ∈ M`. (Its ends are strictly comparable, so they
are not both in `[u]` or both in `[v]`; `a ∈ [v]` would give `v <= a < b <= v`, and `b ∈ [u]` would give
`u <= a < b <= u`.) The *nodes* are the vertex sets of the components of the graph on `[u] ∪ [v]` whose edges are the
real edges of the first kind (`node(x)` denotes the component of `x ∈ [u] ∪ [v]`), and one new node `ρ(a,b)` for every
real edge `ab` of the fourth kind. The terminals are `s = node(u)` and `t = node(v)`. For `w ∈ M`,

    E_w = {node(a) : aw ∈ R, a ∈ [u]} ∪ {ρ(a,w) : aw ∈ R, a ∈ M, a < w},
    F_w = {node(b) : wb ∈ R, b ∈ [v]} ∪ {ρ(w,b) : wb ∈ R, b ∈ M, w < b}.

The middle edges are the pairs `(a, b)` for the real edges `ab` of the fourth kind, with private node `ρ(a,b)`.
Source: `r4-general.md` §5.1 (Setting); the reading of the conversion `gsw.GSW` in `verify/rv-r6-chain.md` §1.2.
Reviewed: `verify/rv-r6-chain.md` §1.2, §2.2 (an own conversion is identical to `gsw.GSW` on every instance);
`verify/rv-core-65.md` §2.1.

**Lemma 3.2 (well defined, P2, sizes).** Construction 3.1 gives an instance of the general switch form: every middle
edge `(a, b)` has `a < b`, and `ρ(a,b)` lies in `F_a` and `E_b` and in no other side. If the ZZ instance satisfies P2,
so does its switch form. Moreover `m <= |Q| − 2`, `|Ω| <= |Q| + |R|`, `Σ_{w ∈ M} (|E_w| + |F_w|) <= 2|R|`, and the
construction takes polynomial time.
Source: `r4-general.md` §5.1; `verify/rv-r6-chain.md` §1.2 (P2 in the form used), §3 item 4 (sizes). Reviewed:
`verify/rv-r6-chain.md` §1.2 (holds), §2.2 (sizes checked on 249 649 records).

*Proof.* The node `ρ(a,b)` is put into `F_a` (second part of `F_w` for `w = a`) and into `E_b` (second part of `E_w` for
`w = b`) and nowhere else. P2: let `x, y ∈ M` be incomparable (in `M`, equivalently in `Q`) and `z` a common
`R`-neighbour. If `z < x` and `z < y`, then `z ∉ [v]` (otherwise `v <= z < x <= v`); for `z ∈ [u]`, `node(z)` lies in
`E_x ∩ E_y`; for `z ∈ M`, `(z, x)` and `(z, y)` are middle edges and `z` is a lower middle witness. If `z > x` and
`z > y`, then dually `z ∉ [u]`; for `z ∈ [v]`, `node(z) ∈ F_x ∩ F_y`; for `z ∈ M`, `z` is an upper middle witness.
Sizes: `[u]` and `[v]` are non-empty and disjoint, so `m <= |Q| − 2`; there are at most `|[u] ∪ [v]|` components and at
most `|R|` private nodes. A real edge of the second or third kind puts one node into one side, one of the fourth kind
its private node into two sides, one of the first kind none. ∎

**Lemma 3.3 (answers agree).** A ZZ instance with `u < v` is a yes-instance if and only if its switch form is a
yes-instance.
Source: `r4-general.md` §5.1 (stated and checked there); proof of `verify/rv-r6-chain.md` §1.2. Reviewed:
`verify/rv-r6-chain.md` §1.2 (proved there), §2.2; checked in `verify/rv-core-65.md` §3.2 (`zz_check`: all 1 535 744 ZZ
instances with 4 middle elements) and `verify/rv-r6-core.md` §3.1.

*Proof.* (i) *Down-sets.* Let `D'` range over the down-sets of `(Q, <=)` with `u ∈ D' ∌ v`, and `D` over the mode
vectors. The maps `D' ↦ D' ∩ M` and `D ↦ [u] ∪ D` are inverse bijections. Indeed `D'` contains `[u]` (`b <= u ∈ D'`)
and misses `[v]` (`t' ∈ D' ∩ [v]` gives `v <= t'` and `v ∈ D'`), and `D' ∩ M` is a down-set of `M`. Conversely, for a
mode vector `D`, an element below some `b ∈ [u]` lies in `[u]` (`x <= b <= u <= x`), and an element `x` below some
`d ∈ D` lies in `[u]`, or in `M` and then in `D`, but not in `[v]` (`v <= x <= d` would put `d` into `[v]`); so
`[u] ∪ D` is a down-set, and it contains `u` and not `v`.
(ii) *Edges.* Let `D' = [u] ∪ D` and let `pk(w)` be the side picked by `D` for `w ∈ M`. The edges of `G_{D'}` are:
every real edge of the first kind; every real edge `aw` of the second kind with `w ∉ D`, and then
`node(a) ∈ E_w = pk(w)`; every real edge `wb` of the third kind with `w ∈ D`, and then `node(b) ∈ F_w = pk(w)`; every
real edge `zw` of the fourth kind (`z < w`) with `z ∈ D ∌ w` (exactly one end in `D`, and `w ∈ D` forces `z ∈ D`), and
then `ρ(z,w) ∈ F_z ∩ E_w = pk(z) ∩ pk(w)`. In particular, an edge of `G_{D'}` between `w ∈ M` and `e ∈ [u] ∪ [v]` puts
`node(e)` into `pk(w)`.
(iii) *If `u` and `v` are connected in `G_{D'}`, then `D` connects `s` and `t`.* Take a `u`–`v` path of `G_{D'}`. A
maximal run of consecutive vertices in `[u] ∪ [v]` is joined by edges of the first kind, so all its vertices have the
same node. If the path has no vertex in `M`, then `node(u) = node(v)`, i.e. `s = t`. Otherwise let `w_1, .., w_h` be
its vertices in `M` in order. If `w_i` and `w_{i+1}` are adjacent on the path, `pk(w_i) ∩ pk(w_{i+1})` contains the
private node of their edge; otherwise the vertices between them form a run with one node `o`, and by (ii) the edges from
`w_i` and `w_{i+1}` into that run put `o` into `pk(w_i)` and `pk(w_{i+1})`. The run before `w_1` contains `u`, so by (ii)
`s = node(u) ∈ pk(w_1)`; likewise `t ∈ pk(w_h)`. So `pk(w_1), .., pk(w_h)` connect `s` and `t`.
(iv) *If `D` connects `s` and `t`, then `u` and `v` are connected in `G_{D'}`.* If `s = t`, then `u` and `v` lie in one
component of the graph of the real edges of the first kind, all of which are edges of `G_{D'}`. Otherwise let
`X_1, .., X_r` be picked sides, `X_i = pk(w_i)`, with `s ∈ X_1`, `t ∈ X_r` and `X_i ∩ X_{i+1} ≠ ∅`. If a node `o` lies in
`pk(w) ∩ pk(w')` with `w ≠ w'`, then `w` and `w'` are connected in `G_{D'}`: if `o` is a component node, then by the
construction and (ii) `w` and `w'` have `G_{D'}`-neighbours `e`, `e'` in the component `o`, and `e`, `e'` are joined by
edges of the first kind; if `o = ρ(z, w'')`, it lies only in `F_z` and `E_{w''}`, so `{w, w'} = {z, w''}`, `z ∈ D ∌ w''`,
and `zw''` is an edge of `G_{D'}`. Finally `s ∈ pk(w_1)` is a component node, so `w_1` has a `G_{D'}`-neighbour in the
component `s ∋ u`, which is joined to `u` by edges of the first kind; likewise `w_r` is connected to `v`.
By (i), (iii), (iv), some `G_{D'}` connects `u` and `v` if and only if some mode vector connects `s` and `t`. ∎

**Lemma 3.4 (valid paths and yes-instances).** Consider an instance of the general switch form.
(a) Let `P` be a valid path. Then `Up ∩ L = ∅`, and a mode vector `D` picks every member of `P` if and only if
`L ⊆ D ⊆ M − Up`. In particular the mode vector `L` picks every member of `P`, and every mode vector that picks every
member of `P` connects `s` and `t`.
(b) If `s ≠ t` and some mode vector connects `s` and `t`, then a valid path exists.
(c) The instance is a yes-instance if and only if `s = t` or a valid path exists; if `s = t`, every mode vector connects
`s` and `t`.
Source: `r4-general.md` §5.1 ("valid walks exist iff the instance is a yes-instance"); `r5-core.md` §6.1 (pick
criterion), §8.2 (F0); `verify/rv-r6-chain.md` §1.3 and §3 item 1 (repair for `s = t`). Reviewed:
`verify/rv-r6-chain.md` §1.3 (holds with the repair "yes-instance = `s = t` or a valid path exists", included as (c)),
§2.3 (checked on 3000 instances, every down-set); `verify/rv-r6-core.md` §2.1; `verify/rv-core-65.md` §2.1.

*Proof.* (a) If `x ∈ Up ∩ L`, then `w <= x <= z` for some `w ∈ W_E` and `z ∈ W_F`; `w ≠ z` because the members belong
to distinct switches, and `{E_w, F_z}` is a conflict pair of two members, against validity. The mode vector `D` picks the F-member `F_w`
if and only if `w ∈ D`, so it picks all F-members if and only if `W_F ⊆ D`, i.e. `L = ↓W_F ⊆ D` (`D` is a down-set). `D`
picks the E-member `E_w` if and only if `w ∉ D`, so it picks all E-members if and only if `W_E ∩ D = ∅`, i.e.
`Up ∩ D = ∅` (if `x ∈ Up ∩ D`, then `w <= x` for some `w ∈ W_E`, and `w ∈ D`). The set `L` is a down-set disjoint from `Up`, so
it picks every member. If `D` picks every member, the members `X_1, .., X_r` are picked sides with `s ∈ X_1`,
`t ∈ X_r` and `X_i ∩ X_{i+1} ≠ ∅`.
(b) Let `X_1, .., X_r` be picked sides with `s ∈ X_1`, `t ∈ X_r`, `X_i ∩ X_{i+1} ≠ ∅` and `r` least. The sides are
pairwise distinct (if `X_i = X_j`, `i < j`, drop `X_{i+1}, .., X_j`), hence of distinct switches, since `D` picks one
side per switch. Two picked sides `E_w`, `F_z` never form a conflict pair: `w ∉ D`, `z ∈ D`, and `w <= z` would put `w`
into `D`. So `X_1 .. X_r` is a valid path.
(c) If `s = t`, every mode vector connects `s` and `t` by Definition 1.8. If `s ≠ t`, use (a) and (b). ∎

## 4. Lemmas on a shortest valid path

**Definition 4.1 (objects of a valid path).** Fix an instance of the general switch form and a valid path
`P = X_1 .. X_r`, with `W_E`, `W_F`, `Up`, `L` as in Definition 1.8.
- `A` is the set of *minimal E-members* (E-members with no E-member strictly below) and `B` the set of *maximal
  F-members* (F-members with no F-member strictly above).
- `Enon = {w ∈ M : E_w ≠ ∅}`, `Fnon = {w ∈ M : F_w ≠ ∅}`, `N_E = L ∩ Enon`, `N_F = Up ∩ Fnon`.
- For `Z ⊆ Ω`: `NE(Z) = {w ∈ M : E_w ∩ Z ≠ ∅}` and `NF(Z) = {w ∈ M : F_w ∩ Z ≠ ∅}`.
- *Stars*: `E#_w = E_w ∪ {ρ(z, w') : z ∈ LMN(w), (z, w') a middle edge}` and
  `F#_w = F_w ∪ {ρ(w', z) : z ∈ UMN(w), (w', z) a middle edge}`.
- A side is *`P`-consistent* if it is `E_w` with `w ∉ L` or `F_w` with `w ∉ Up`.
Source: `r5-core.md` §3.1 (`Enon`, `Fnon`, `NE`, `NF`), §6.1 (needed items, `P`-consistent sides), §6.3 (stars), §8.2.
Reviewed: `verify/rv-core-65.md` §2.1 (holds; the identity `NE(E#_w) = NE(E_w) ∪ Sib↓(w) ∪ {w}` of `r5-core.md` §6.3
needs `E_w ≠ ∅` for the term `{w}`; it is not used here); `verify/rv-r6-core.md` §2.1.

**Lemma 4.2 (basic facts).** Let `P` be a valid path; in (e) let `P` be shortest.
(a) Every member is non-empty; so `W_E ⊆ Enon` and `W_F ⊆ Fnon`. `Up ∩ L = ∅`, `Up = ↑A` and `L = ↓B`.
(b) No element of `A` lies strictly below an element of `A`; no element of `L` lies strictly above an element of `B`;
for `a ∈ A`, `↑a ⊆ Up` and `↑a ∩ L = ∅`.
(c) Let `S_1, S_2 ⊆ M` with `S_1 ∩ S_2 = ∅`. If `S_1` is an up-set, then `↓S_2 ∩ S_1 = ∅`; if `S_1` is a down-set,
then `↑S_2 ∩ S_1 = ∅`.
(d) A `P`-consistent side forms no conflict pair with a member.
(e) If `X_c ∩ X_d ≠ ∅`, then `|c − d| <= 1`.
Source: `r5-core.md` §8.2 (F0, F3, F4), §6.1 (fact (a)); `r4-switch.md` §2 (F1) for (e). Reviewed:
`verify/rv-r6-core.md` §2.1 (F0, F3, F4 hold, also with ties); `verify/rv-core-65.md` §2.1 (fact (a) holds), §2.3 (use
of F1); `verify/r4-switch-review.md` §2.2 (F1 holds).

*Proof.* (a) If `r = 1`, `s ∈ X_1`; otherwise every member meets a neighbouring member. The equality `Up ∩ L = ∅` is
Lemma 3.4(a). The inclusion `A ⊆ W_E` gives `↑A ⊆ Up`. For an E-member `w`, choose among the E-members `a <= w` one with `|↓a|` least. If an
E-member `a''` satisfied `a'' < a`, then `↓a'' ⊆ ↓a` and `a ∉ ↓a''`, so `|↓a''| < |↓a|` with `a'' <= w`, against the
choice; so `a ∈ A` and `w ∈ ↑A`. Hence `W_E ⊆ ↑A` and `Up = ↑A`. Dually (choose `|↑b|` least) `L = ↓B`.
(b) The first statement is the definition of `A`. Let `b ∈ B` and `w ∈ L` with `b < w`; by (a), `w <= b'` for some
`b' ∈ B`, so `b < b'` (Definition 1.5), and `b'` is an F-member strictly above `b`, against `b ∈ B`. For `a ∈ A`,
`↑a ⊆ ↑W_E = Up`, which misses `L`.
(c) If `w ∈ ↓S_2 ∩ S_1` with `S_1` an up-set, then `w <= g` for some `g ∈ S_2`, and `g ∈ S_1` as `S_1` is an up-set,
against `S_1 ∩ S_2 = ∅`. The second statement is dual.
(d) A conflict pair consists of an E-side and an F-side. `E_w` with `w ∉ L` and an F-member `F_b` form a conflict pair
only if `w <= b`, which puts `w` into `↓W_F = L`. `F_w` with `w ∉ Up` and an E-member `E_a` form one only if `a <= w`,
which puts `w` into `Up`.
(e) If `c + 2 <= d` and `X_c ∩ X_d ≠ ∅`, then `X_1 .. X_c X_d .. X_r` consists of members of `P` (distinct switches, no
conflict pair), consecutive sides meet, and it starts with `X_1 ∋ s` and ends with `X_r ∋ t`: a valid path with fewer
members than `P`, against the choice of `P`. ∎

**Lemma 4.3 (windows of chains).** Let `P` be a shortest valid path, and let `Z_1, .., Z_j` (`j >= 1`) be `P`-consistent
sides of pairwise distinct switches none of which is on `P`, no two of them a conflict pair, with `Z_i ∩ Z_{i+1} ≠ ∅`
for `i < j`. If `X_c ∩ Z_1 ≠ ∅` and `X_d ∩ Z_j ≠ ∅`, then `|c − d| <= j + 1`.
Source: `r5-core.md` §6.2, Lemma 6.2. Reviewed: `verify/rv-core-65.md` §2.2 (holds; the walk below is itself a valid
path, so the "shortest sub-walk" step of the source is not needed and is omitted).

*Proof.* If `c = d` there is nothing to prove; if `c > d`, the reversed chain `Z_j, .., Z_1` satisfies the same
hypotheses with the roles of `c` and `d` exchanged. So let `c < d`. The sequence `X_1 .. X_c Z_1 .. Z_j X_d .. X_r`
starts with `X_1 ∋ s`, ends with `X_r ∋ t`, consecutive sides meet, and its sides belong to pairwise distinct switches
(the members to distinct switches of `P`, the `Z_i` to distinct switches not on `P`). No two of its sides form a
conflict pair: two members do not (`P` is valid), a member and some `Z_i` do not (Lemma 4.2(d)), two `Z_i` do not
(hypothesis). So it is a valid path with `c + j + (r − d + 1)` members, and `c + j + r − d + 1 >= r` because `P` is
shortest: `d − c <= j + 1`. ∎

**Lemma 4.4 (stars meet few minimal E-members).** Let `P` be a shortest valid path. For every switch `x ∉ L`, the set
`A_x = A ∩ NE(E#_x)` lies in an interval of at most 9 consecutive positions of `P`; in particular
`|A ∩ NE(E#_x)| <= 9`. Dually, for every switch `y ∉ Up`, `B ∩ NF(F#_y)` lies in an interval of at most 9 consecutive
positions, and `|B ∩ NF(F#_y)| <= 9`.
Source: `r5-core.md` §6.3, Lemma 6.3. Reviewed: `verify/rv-core-65.md` §2.3 (holds in every case, with ties and empty
window; the proof even gives 5 positions).

*Proof.* *Two types.* Let `a ∈ A_x`. As `a ∈ W_E`, `E_a = X_a`. By definition `E_a` meets `E_x` (type (i)) or contains a
private node `ρ(z, w')` with `z ∈ LMN(x)`; that node lies only in `F_z` and `E_{w'}`, so `w' = a` and
`z ∈ LMN(x) ∩ LMN(a)` (type (ii), with *witness* `z`).
*Facts on a witness `z`.* Middle edges are strict, so `z < a` and `z < x`. Also `z ∉ Up`: an E-member `a'' <= z` would
satisfy `a'' < a` (Definition 1.5), against `a ∈ A`. So `F_z` is `P`-consistent; it meets `X_a` (in `ρ(z,a)`) and `E_x`
(in `ρ(z,x)`); and `{E_x, F_z}` is not a conflict pair (that needs `x <= z`, but `z < x`). If `z` is on `P`, then
`z ∉ Up ⊇ W_E` gives `z ∈ W_F` and `X_z = F_z`.
*Case 1: `x` is not on `P`.* The side `E_x` is `P`-consistent (`x ∉ L`); let `win = {c : X_c ∩ E_x ≠ ∅}`.
*Case 1a: `win ≠ ∅`.* For `c, c' ∈ win`, Lemma 4.3 for the chain `E_x` (`j = 1`) gives `|c − c'| <= 2`; so
`win ⊆ [ℓ, ℓ + 2]` with `ℓ = min win`. Type (i): `pos(a) ∈ win`. Type (ii) with `z` on `P`: `X_z = F_z` meets `E_x`,
so `pos(z) ∈ win`, and it meets `X_a`, so `|pos(z) − pos(a)| <= 1` by Lemma 4.2(e); hence `pos(a) ∈ [ℓ − 1, ℓ + 3]`. Type
(ii) with `z` not on `P`: the chain `F_z, E_x` satisfies the hypotheses of Lemma 4.3 (`P`-consistent sides of the
distinct switches `z`, `x`, neither on `P`, no conflict pair, `F_z ∩ E_x ≠ ∅`); as `X_a` meets `F_z` and `X_ℓ` meets
`E_x`, `|pos(a) − ℓ| <= 3`. In every case `pos(a) ∈ [ℓ − 3, ℓ + 5]`, an interval of 9 positions.
*Case 1b: `win = ∅`.* Type (i) does not occur, and no witness is on `P` (it would put `pos(z)` into `win`). Let
`a, a' ∈ A_x` with witnesses `z`, `z'`. If `z = z'`, the `P`-consistent side `F_z` of a switch not on `P` meets `X_a`
and `X_{a'}`, so `|pos(a) − pos(a')| <= 2` by Lemma 4.3 (`j = 1`). If `z ≠ z'`, the chain `F_z, E_x, F_{z'}` consists of
`P`-consistent sides of the distinct switches `z`, `x`, `z'` (`z, z' < x`), none on `P`; consecutive sides meet (in
`ρ(z,x)` and `ρ(z',x)`); no two form a conflict pair (`{F_z, F_{z'}}` has no E-side, and `{E_x, F_z}`, `{E_x, F_{z'}}`
are none by the facts above); `X_a` meets `F_z` and `X_{a'}` meets `F_{z'}`. So `|pos(a) − pos(a')| <= 4` by Lemma 4.3
(`j = 3`), and `A_x` lies in 5 consecutive positions.
*Case 2: `x` is on `P`.* As `x ∉ L ⊇ W_F`, `x ∈ W_E` and `E_x = X_x`; let `e = pos(x)`. Type (i): `X_a` meets `X_x`, so
`a = x` or `|pos(a) − e| <= 1` (Lemma 4.2(e)). Type (ii) with `z` on `P`: `X_z = F_z` meets `X_a` and `X_x`, so
`|pos(a) − e| <= 2` (Lemma 4.2(e) twice). Type (ii) with `z` not on `P`: `F_z` meets `X_a` and `X_x`, so
`|pos(a) − e| <= 2` by Lemma 4.3 (`j = 1`). So `A_x ⊆ [e − 2, e + 2]`.
*Dual statement.* The *reversed instance* has the same nodes, terminals and switches, the preorder `<=^op`
(`x <=^op y` if `y <= x`), sides `E^op_w = F_w`, `F^op_w = E_w`, and a middle edge `(w, z)` for every middle edge
`(z, w)`, with the same private node, which lies in `F^op_w = E_w` and `E^op_z = F_z` and in no other side. It is an
instance of the general switch form, with P2 if the original has it (common E-nodes and F-nodes are exchanged, lower and
upper middle witnesses are exchanged). Its mode vectors are the complements of the original ones and pick the same node
sets; its conflict pairs `{E^op_w, F^op_z}`, `w <=^op z`, are the pairs `{F_w, E_z}` with `z <= w`, i.e. the original
ones. So `P` is a shortest valid path of it, with `W^op_E = W_F`, `Up^op = L`, `L^op = Up`, `A^op = B`,
`LMN^op = UMN`, `E#^op_w = F#_w` and `NE^op = NF`. The first statement for the reversed instance and `y ∉ L^op = Up` is
the dual statement. ∎

*Note (not used).* By the pairwise distances of the proof (Case 1a: types (i)/(i) at most 2 apart, (i)/(ii) at most 3,
(ii)/(ii) at most 4), `A_x` always lies in 5 consecutive positions (`verify/rv-core-65.md` §2.3); then `9k` can be read
`5k` in §5 and §6. The bound 9 is kept, as in the source.

**Lemma 4.5 (duality for incomparable pairs).** In an instance of the general switch form with P2, let `x`, `y` be
incomparable switches with `F_x ≠ ∅` and `E_y ≠ ∅` (for a valid path, in particular `x ∈ N_F` and `y ∈ N_E`). Then
`y ∈ NE(E#_x)` or `x ∈ NF(F#_y)`.
Source: `r5-core.md` §6.3, Lemma 6.4. Reviewed: `verify/rv-core-65.md` §2.4 (holds; uses only P2 and
`E_y, F_x ≠ ∅`); `verify/rv-r6-chain.md` §1.2 (the four witness kinds are what Construction 3.1 produces).

*Proof.* P2 gives four cases. A common E-node lies in `E_y ∩ E_x ⊆ E_y ∩ E#_x`, so `y ∈ NE(E#_x)`. A common F-node lies
in `F_x ∩ F_y ⊆ F_x ∩ F#_y`, so `x ∈ NF(F#_y)`. A lower middle witness `z ∈ LMN(x) ∩ LMN(y)`: `(z, y)` is a middle edge
and `z ∈ LMN(x)`, so `ρ(z,y) ∈ E#_x ∩ E_y` and `y ∈ NE(E#_x)`. An upper middle witness `z ∈ UMN(x) ∩ UMN(y)`: `(x, z)`
is a middle edge and `z ∈ UMN(y)`, so `ρ(x,z) ∈ F#_y ∩ F_x` and `x ∈ NF(F#_y)`. ∎

## 5. Intersections of terms

**Definition 5.1 (terms).** Let an instance of the general switch form have `m >= 1` switches, and put
`k = ⌊log m⌋ + 1` (so `2^k > m`) and `N = ⌈2k ln m⌉`. An *E-term* `τ = (E; T, T', Φ)` consists of a set `T ⊆ M` of
*tools*, a set `T' ⊆ T` of *flagged* tools and a set `Φ ⊆ M` of *flips*; it defines

    U = ⋃_{x ∈ T} NE(E#_x),   Π = ⋃_{x ∈ T'} (↓x − [x]),   Γ = (Enon − U − Π) ∪ Φ,   D(τ) = M − ↑Γ.

The set `↓x − [x]` of a flagged tool `x` is its *pivot*. An *F-term* `τ = (F; T, T', Ψ, Φ)` has in addition a set
`Ψ ⊆ M` of *E-anchors*; it defines

    U' = ⋃_{y ∈ T} NF(F#_y),   Π' = ↑Ψ ∪ ⋃_{y ∈ T'} (↑y − [y]),   Γ' = (Fnon − U' − Π') ∪ Φ,   D(τ) = ↓Γ'.

A term is *anchor-free* if it is an E-term or an F-term with `Ψ = ∅`. For every term, `D(τ)` is a down-set of `M` (the
complement of an up-set, resp. a down-closure), hence a mode vector, and so is every intersection of such sets.
(The terms of `r5-core.md` §8.2 also allow E-terms with F-anchors `Y_0`; every term of Lemma 5.2 has `Y_0 = ∅`, so they
are omitted here.)
Source: `r5-core.md` §8.2 (Terms), §6.1 (GDESC); `verify/rv-r6-core.md` §2.8 (restriction to the shape of Theorem 8.2).
Reviewed: `verify/rv-r6-core.md` §2.1 (every `D(τ)` is a down-set; the terms coincide with the descriptions of GDESC);
`verify/rv-core-65.md` §2.1 (with `Φ ⊆ U`, the union `∪ Φ` used here and the symmetric difference `△ Φ` of `r5-core.md`
§3 agree).

**Lemma 5.2 (one level).** Let an instance of the general switch form with P2 and `m >= 1` switches have a shortest
valid path `P` (objects of Definition 4.1), let `k`, `N` be as in Definition 5.1, and let `A' ⊆ A` be non-empty. Then
there is a term `τ` with `L ⊆ D(τ)`, at most `k` tools and at most `9k` flips, whose flips lie in `U` (E-term) or in
`U'` (F-term), such that
- (final) `D(τ) ∩ ↑A' = ∅`, and `τ` is an E-term or an F-term with at most `N` E-anchors; or
- (continue) `τ` is an E-term and `D(τ) ∩ ↑A' ⊆ ↑A''` for a set `A'' ⊆ A'` with `1 <= |A''| <= |A'|/2`.
Source: `r5-core.md` §8.2, Lemma 8.1. Reviewed: `verify/rv-r6-core.md` §2.2-§2.5 (holds; one-sentence repair for
`m = 1`, included in the proof; no hidden use of Theorem 6.5, of shortestness beyond Lemma 4.4, or of a property that
fails with ties).

*Proof.* Strategy: a zero-sum game between rows (elements of `↑A'` with non-empty F-side) and columns (`N_E`); if the
row player wins, `k` E-stars and pivots cover all columns and give an E-term that damages at most half of `A'`;
otherwise `k` F-stars cover the light rows and `N` anchors drawn from `A'` cover the heavy rows.
*Setting.* Let `ℛ = ↑A' ∩ Fnon` (*rows*), `𝒞 = N_E` (*columns*) and `θ = |A'|/(2k)`. For a switch `x` let
`dam(x) = A' ∩ (↓x − [x])` (its *damage*); `x` is *light* if `|dam(x)| <= θ` and *heavy* otherwise. For `x ∈ ℛ` and
`y ∈ 𝒞` put

    cov_E(x) = (NE(E#_x) ∪ (↓x − [x] if x is light)) ∩ 𝒞,
    cov_F(y) = (NF(F#_y) ∪ (↑y − [y] if y ∈ B)) ∩ ℛ.

Rows lie in `↑A' ⊆ ↑A = Up` (Lemma 4.2(a)), so they lie in `N_F` and not in `L`; columns lie in `L`, so not in `Up`;
`|ℛ|, |𝒞| <= m`. Every element of `A'` is light, since `dam(a) = ∅` for `a ∈ A'` (Lemma 4.2(b)).
*Claim (duality).* For every light `x ∈ ℛ` and every `y ∈ 𝒞`: `y ∈ cov_E(x)` or `x ∈ cov_F(y)`. Indeed, exactly one of
`x <= y`, `y < x`, `x ∥ y` holds (Definition 1.5). `x <= y` would put `x` into the down-set `L ∋ y`, but `x ∈ Up` and
`Up ∩ L = ∅`. If `y < x`, then `y ∈ ↓x − [x]`, which is part of `cov_E(x)` because `x` is light. If `x ∥ y`, Lemma 4.5
(`F_x ≠ ∅` as `x ∈ Fnon`, `E_y ≠ ∅` as `y ∈ Enon`) gives `y ∈ NE(E#_x)`, so `y ∈ cov_E(x)`, or `x ∈ NF(F#_y)`, so
`x ∈ cov_F(y)`.
*Trivial cases.* If `𝒞 = ∅`, take the E-term with `T = T' = Φ = ∅`: `Γ = Enon`, and `Γ ∩ L = L ∩ Enon = N_E = ∅`, so
`L ⊆ D(τ)` by Lemma 4.2(c); `A' ⊆ W_E ⊆ Enon = Γ` (Lemma 4.2(a)), so `↑A' ⊆ ↑Γ` and `D(τ) ∩ ↑A' = ∅`: final. If
`ℛ = ∅`, take the F-term with `T = T' = Ψ = Φ = ∅`: `Γ' = Fnon`, and `Γ' ∩ ↑A' = ℛ = ∅`, so `D(τ) ∩ ↑A' = ∅` by Lemma
4.2(c) (`↑A'` is an up-set); `B ⊆ W_F ⊆ Fnon = Γ'`, so `L = ↓B ⊆ ↓Γ' = D(τ)` (Lemma 4.2(a)): final.
*The game.* Otherwise `ℛ` and `𝒞` are non-empty. In the finite zero-sum game in which the row player chooses `x ∈ ℛ`,
the column player chooses `y ∈ 𝒞`, and the row player receives `μ(x,y) = 1` if `y ∈ cov_E(x)` and `0` otherwise, von
Neumann's minimax theorem gives a value `λ`, a probability distribution `p` on `ℛ` with `Σ_x p(x) μ(x,y) >= λ` for every
`y ∈ 𝒞`, and a probability distribution `q` on `𝒞` with `Σ_y q(y) μ(x,y) <= λ` for every `x ∈ ℛ`.
*Case `λ >= 1/2`.* Draw `x_1, .., x_k` independently from `p`. A fixed column lies in no `cov_E(x_i)` with probability at
most `2^{−k} < 1/m`, so the expected number of columns outside `⋃_i cov_E(x_i)` is less than `|𝒞|/m <= 1`, and some
outcome has `𝒞 ⊆ ⋃_i cov_E(x_i)`. Fix it, and let `τ` be the E-term with `T = {x_1, .., x_k}`,
`T' = {x_i : x_i light}` and `Φ = A' ∩ U`. It has at most `k` tools and `Φ ⊆ U`.
- `L ⊆ D(τ)`. Let `y ∈ L ∩ Γ`. As `Φ ⊆ A' ⊆ Up` misses `L`, `y ∈ Enon − U − Π`, so `y ∈ L ∩ Enon = 𝒞`; then
  `y ∈ cov_E(x_i)` for some `i`, i.e. `y ∈ NE(E#_{x_i}) ⊆ U`, or `x_i` is light and `y ∈ ↓x_i − [x_i] ⊆ Π`: a
  contradiction. So `Γ ∩ L = ∅`, and Lemma 4.2(c) gives `↑Γ ∩ L = ∅`, i.e. `L ⊆ D(τ)`.
- Flips. Every `x_i` lies in `ℛ ⊆ Up`, hence not in `L`, and Lemma 4.4 gives `|A ∩ NE(E#_{x_i})| <= 9`; so
  `|Φ| <= Σ_i |A ∩ NE(E#_{x_i})| <= 9k`.
- Damage. Let `A'' = A' − Γ`. An element of `A'` outside `U ∪ Π` lies in `Enon − U − Π ⊆ Γ` (as `A' ⊆ Enon`); an element
  of `A' ∩ U` lies in `Φ ⊆ Γ`. Hence `A'' ⊆ A' ∩ Π ⊆ ⋃_{x_i light} dam(x_i)` and `|A''| <= kθ = |A'|/2`. If
  `w ∈ ↑A' − ↑A''`, then `w >= a` for some `a ∈ A' − A'' ⊆ Γ`, so `w ∈ ↑Γ` and `w ∉ D(τ)`. Hence
  `D(τ) ∩ ↑A' ⊆ ↑A''`. If `A'' = ∅`, this is the final case with an E-term; otherwise it is the continue case.
*Case `λ < 1/2`.* For a light row `x`, the claim gives `μ(x,y) = 1` or `x ∈ cov_F(y)` for every `y`, so
`Σ_y q(y) [x ∈ cov_F(y)] >= 1 − Σ_y q(y) μ(x,y) >= 1 − λ > 1/2`. Draw `y_1, .., y_k` independently from `q`, and
`a_1, .., a_N` independently and uniformly from `A'`.
- A light row lies in no `cov_F(y_i)` with probability less than `2^{−k} < 1/m`.
- A heavy row `x` has `|dam(x)| > θ`, so one `a_j` lies outside `dam(x)` with probability
  `1 − |dam(x)|/|A'| < 1 − 1/(2k)`. If `m >= 2`, then `k >= 2` and `N >= 2k ln m >= 4 ln 2 > 2`, so `N >= 3`, and no
  `a_j` lies in `dam(x)` with probability less than `(1 − 1/(2k))^N <= e^{−N/(2k)} <= e^{−ln m} = 1/m`. If `m = 1`, there
  is no heavy row: a heavy row has an element of `A'` strictly below it, so `M` would have two elements.
- By the union bound over the at most `m` rows, some outcome has every light row in some `cov_F(y_i)` and every heavy row
  strictly above some `a_j`. Fix it, and let `τ` be the F-term with `T = {y_1, .., y_k}`, `T' = T ∩ B`,
  `Ψ = {a_1, .., a_N} ⊆ A'` and `Φ = B ∩ U'`. It has at most `k` tools, at most `N` E-anchors, and `Φ ⊆ U'`.
- `D(τ) ∩ ↑A' = ∅`. Let `x ∈ ↑A' ∩ Γ'`. As `Φ ⊆ B ⊆ L` and `x ∈ ↑A' ⊆ Up`, `x ∉ Φ`; so `x ∈ Fnon − U' − Π'` and
  `x ∈ ↑A' ∩ Fnon = ℛ`. If `x` is light, `x ∈ cov_F(y_i)` for some `i`: `x ∈ NF(F#_{y_i}) ⊆ U'`, or `y_i ∈ B`, hence
  `y_i ∈ T'`, and `x ∈ ↑y_i − [y_i] ⊆ Π'`. If `x` is heavy, `x > a_j` for some `j`, and `x ∈ ↑Ψ ⊆ Π'`. Either way
  `x ∉ Γ'`, a contradiction. So `Γ' ∩ ↑A' = ∅`, and Lemma 4.2(c) gives `D(τ) ∩ ↑A' = ↓Γ' ∩ ↑A' = ∅`.
- `L ⊆ D(τ)`. Let `b ∈ B`; then `b ∈ Fnon` (Lemma 4.2(a)). If `b ∈ U'`, then `b ∈ Φ ⊆ Γ'`. Otherwise `b ∉ ↑Ψ`, since
  `↑a_j ∩ L = ∅` (Lemma 4.2(b)), and `b ∉ ↑y − [y]` for `y ∈ T' ⊆ B`, since no element of `L` lies strictly above an
  element of `B` (Lemma 4.2(b)); so `b ∈ Fnon − U' − Π' ⊆ Γ'`. Hence `B ⊆ Γ'` and `L = ↓B ⊆ ↓Γ' = D(τ)`.
- Flips. Every `y_i` lies in `𝒞 ⊆ L`, hence not in `Up`, and the dual part of Lemma 4.4 gives
  `|Φ| <= Σ_i |B ∩ NF(F#_{y_i})| <= 9k`.
This is the final case. ∎

**Theorem 5.3 (intersections of terms).** Let an instance of the general switch form with P2 and `m` switches have a
valid path. Then `m >= 1`, and with `k`, `N` as in Definition 5.1 there are terms `τ_1, .., τ_j`, `j <= k`, each with at
most `k` tools and at most `9k` flips, the flips of each term lying in its `U` (resp. `U'`), all anchor-free except
possibly `τ_j`, which is then an F-term with at most `N` E-anchors, such that the mode vector
`D(τ_1) ∩ .. ∩ D(τ_j)` picks every member of a shortest valid path and connects `s` and `t`.
Source: `r5-core.md` §8.2, Theorem 8.2. Reviewed: `verify/rv-r6-core.md` §2.6 (holds; checked with up to 5 levels);
`verify/rv-r6-chain.md` §1.3 (the hypothesis "has a valid path" excludes only the yes-instances with `s = t` and no valid
path, which Definition 6.1 accepts directly).

*Proof.* A valid path has a member, so `m >= 1`. Let `P` be a shortest valid path, with the objects of Definition 4.1.
If `A = ∅`, then `W_E = ∅` (Lemma 4.2(a)) and `Up = ∅`; the F-term `τ_1` with `T = T' = Ψ = Φ = ∅` has
`Γ' = Fnon ⊇ B` (Lemma 4.2(a)), so `L = ↓B ⊆ D(τ_1)` and `D(τ_1) ∩ Up = ∅`; take `j = 1`.
Let `A ≠ ∅`. Put `A^(1) = A` and apply Lemma 5.2 to `A^(i)`, `i = 1, 2, ..`, as long as it yields the continue case,
with `A^(i+1) = A''`; let `τ_i` be the term it yields, and stop at the first final case, `i = j`. As
`1 <= |A^(i+1)| <= |A^(i)|/2` and `|A| <= m`, after `c` continue steps `1 <= |A^(c+1)| <= m 2^{−c}`; so `c <= ⌊log m⌋`,
the process stops, and `j <= ⌊log m⌋ + 1 = k`. The terms of continue steps are E-terms; only `τ_j` may be an F-term,
with at most `N` E-anchors. Let `D_i = D(τ_i)` and `D = D_1 ∩ .. ∩ D_j`, a mode vector. `L ⊆ D_i` for every `i`, so
`L ⊆ D`. By induction on `i < j`, `D_1 ∩ .. ∩ D_i ∩ Up ⊆ ↑A^(i+1)`: for `i = 1`, `Up = ↑A^(1)` (Lemma 4.2(a)) and
`D_1 ∩ ↑A^(1) ⊆ ↑A^(2)`; for the step, `D_1 ∩ .. ∩ D_{i+1} ∩ Up ⊆ D_{i+1} ∩ ↑A^(i+1) ⊆ ↑A^(i+2)`. The final term gives
`D_j ∩ ↑A^(j) = ∅`; hence `D ∩ Up = ∅` (for `j = 1` because `Up = ↑A^(1)`, for `j >= 2` because
`D ∩ Up ⊆ D_j ∩ ↑A^(j)`). By Lemma 3.4(a), `D` picks every member of `P` and connects `s` and `t`. ∎

## 6. The algorithm IDESC

**Definition 6.1 (IDESC).** Input: an instance of the general switch form. If `s = t`, accept. If `m = 0` and `s ≠ t`,
reject. Otherwise let `k`, `N` be as in Definition 5.1 and consider every sequence `τ_1, .., τ_j` of terms such that
- `1 <= j <= k`;
- every term has at most `k` tools, any set `T' ⊆ T` of flagged tools, and flips `Φ ⊆ U` (resp. `Φ ⊆ U'`) with
  `|Φ| <= 9k`;
- `τ_1, .., τ_{j−1}` are anchor-free, and `τ_j` is anchor-free or an F-term with at most `N` E-anchors.
For each sequence compute `D = D(τ_1) ∩ .. ∩ D(τ_j)` and test whether `D` connects `s` and `t`. Accept if some test
succeeds, otherwise reject.
This is IDESC(`k`, `k`, `N`, `9k`) of `r5-core.md` §8.3 restricted to the shape of Theorem 5.3 (anchors only in the last
term, which is an F-term).
Source: `r5-core.md` §8.3 (IDESC(`j, k, a, e`)); `verify/rv-r6-core.md` §2.8 (restriction to the shape of Theorem 8.2),
§2.10 (`m = 0`); `verify/rv-r6-chain.md` §1.3 (`s = t`). Reviewed: `verify/rv-r6-core.md` §2.7, §2.8;
`verify/rv-r6-chain.md` §1.3, §2.2 (IDESC with these parameters equals the graph brute force on all 121 588 open-case
pairs of graphs with at most 8 vertices and on 1500 realised random instances).

**Theorem 6.2 (IDESC decides the general switch form with P2).** Let an instance of the general switch form with P2
have `m` switches, `ν = |Ω|` nodes and total side size `σ = Σ_{w ∈ M} (|E_w| + |F_w|)`. IDESC accepts if and only if
the instance is a yes-instance. For `m >= 1` it tests at most `2k · (2^{k+1} (m+1)^{10k})^k · (m+1)^N` sequences, and it
runs in time `2^{O(log^3 (m+2))} · poly(m, ν, σ)`.
Source: `r5-core.md` §8.3 (soundness, completeness, time). Reviewed: `verify/rv-r6-core.md` §2.7 (soundness and
completeness hold), §2.8 (time bound holds with a wording repair: subsets of size at most `c` of an `m`-set number at
most `(m+1)^c`, not `m^c`, and the count `(2^{k+1} m^{10k})^k m^N` assumes the anchors in one term; the count here
restricts IDESC to that shape, as the review allows); `verify/rv-r6-chain.md` §1.3 (`s = t`).

*Proof.* *Soundness.* If IDESC accepts because `s = t`, the instance is a yes-instance by Lemma 3.4(c). Otherwise it
accepts because some tested `D` connects `s` and `t`; `D` is a mode vector (Definition 5.1), so the instance is a
yes-instance. If `m = 0` and `s ≠ t`, the only mode vector `∅` picks no side and does not connect `s` and `t`, so the
instance is a no-instance and the rejection is correct.
*Completeness.* Let the instance be a yes-instance with `s ≠ t`. By Lemma 3.4(c) it has a valid path, so by Theorem 5.3
`m >= 1` and there are terms `τ_1, .., τ_j` as stated there. They satisfy every condition of Definition 6.1: `j <= k`,
at most `k` tools, a flag set `T' ⊆ T`, flips inside `U` (resp. `U'`) and at most `9k` of them, anchors only in `τ_j`,
which is then an F-term with at most `N` E-anchors. Their intersection connects `s` and `t`, so IDESC accepts.
*Count.* Let `m >= 1`. A subset of `M` of size at most `c` can be chosen in
`Σ_{i <= c} C(m, i) <= Σ_{i <= c} C(c, i) m^i = (m+1)^c` ways. An anchor-free term is fixed by its kind (2 ways), its
tools (at most `(m+1)^k`), its flags (at most `2^k`) and its flips (at most `(m+1)^{9k}`): at most
`α = 2^{k+1} (m+1)^{10k}` anchor-free terms. F-terms with at most `N` E-anchors number at most
`2^k (m+1)^{10k} (m+1)^N <= α (m+1)^N`. So the last term has at most `2α (m+1)^N` choices, the sequences of length `j`
number at most `α^{j−1} · 2α (m+1)^N <= 2 α^k (m+1)^N` (`α >= 1`), and summing over `j <= k` gives the bound.
*Time.* Let `ℓ = log(m + 2)`, so `ℓ > 1`. Then `k <= log m + 1 <= 2ℓ` and, as `ln m <= log m <= ℓ`,
`N <= 2k ln m + 1 <= 4ℓ^2 + 1 <= 5ℓ^2`. The logarithm of the count is at most
`1 + log k + k(k + 1) + (10k^2 + N) log(m + 1) <= 1 + 2ℓ + 2ℓ(2ℓ + 1) + 45ℓ^3 = O(ℓ^3)`. The sets `NE(E#_x)` and
`NF(F#_y)` of all switches are computed once in time `poly(m, ν, σ)`. For each term, `U`, `Π`, `Γ` and `↑Γ` (resp.
`U'`, `Π'`, `Γ'` and `↓Γ'`) take `O(m^2)` time with the table of `<=`; the intersection takes `O(km)`; whether `D`
connects `s` and `t` is decided by a union-find over the nodes of the picked sides in `O(ν + σ + m)` time; listing the
sequences costs `poly(m)` per sequence. So the total time is `2^{O(ℓ^3)} · poly(m, ν, σ)`. ∎

## 7. The main theorem and its complexity consequences

**Theorem 7.1 (main theorem).** There is a deterministic algorithm that, given a graph `G ∈ DC` with `n` vertices and
vertices `u`, `v` with `d(u,v) = 2` and `c(u,v) >= 3`, decides whether `cp(u,v) = c(u,v)` in time `2^{O(log^3 n)}`.
Source: `r5-core.md` §8.3, Corollary 8.3, and §8.5 item 2 (the chain); `verify/rv-r6-chain.md` §3 items 2, 4.
Reviewed: `verify/rv-r6-core.md` §2.9 (holds, conditional on Theorem 13(a), which is Theorem 2.9 here);
`verify/rv-r6-chain.md` §0 (links L1-L4 hold), §1.4, §2.2.

*Proof.* The graph has `n >= 3` vertices, since `u`, `v` and a common neighbour are distinct. The algorithm computes the ZZ instance of
`(G, u, v)` (Theorem 2.9: polynomial time, P2, `u < v`, `|Q| <= n`, `|R| <= |E(G)|`, and it is a yes-instance if and
only if `cp(u,v) = c(u,v)`), then its switch form (Construction 3.1 and Lemma 3.2: polynomial time, P2,
`m <= |Q| − 2 <= n − 2`, `ν <= |Q| + |R| <= n + |E(G)|`, `σ <= 2|R|`; the same answer by Lemma 3.3), and runs IDESC on
it (Theorem 6.2: it accepts if and only if the switch form is a yes-instance). The answer is therefore correct. The
first two steps take `poly(n)` time, and IDESC takes `2^{O(log^3 (m+2))} · poly(m, ν, σ) <= 2^{O(log^3 n)} · poly(n)`
time, since `m + 2 <= n` and `ν, σ <= n + n^2`. As `log n >= 1`, `poly(n) = 2^{O(log n)} <= 2^{O(log^3 n)}`. ∎

**Corollary 7.2 (complexity).** Let OPEN-DC be the problem of Theorem 7.1: given `(G, u, v)` with `G ∈ DC`,
`d(u,v) = 2` and `c(u,v) >= 3` (a promise), decide whether `cp(u,v) = c(u,v)`. Let
`QP = ⋃_{c' >= 1} DTIME(2^{(log s)^{c'}})`, where `s` is the input size.
(a) OPEN-DC is in NP and in QP. The promise is decidable in polynomial time, so the same holds for the language of all
`(G, u, v)` that satisfy the promise and have `cp(u,v) = c(u,v)`.
(b) If OPEN-DC is NP-hard under polynomial-time many-one or Turing reductions (by (a), equivalently NP-complete under
many-one reductions), then NP ⊆ QP.
(c) If the Exponential Time Hypothesis holds, OPEN-DC is not NP-hard.
Membership in P is not claimed.
Source: `r5-core.md` §8.3, Corollary 8.3; `verify/rv-r6-chain.md` §1.4 and §3 item 3 (wording, NP membership, the
promise). Reviewed: `verify/rv-r6-core.md` §2.9 (holds); `verify/rv-r6-chain.md` §1.4 (holds; wording repair "if ETH
holds, it is not NP-hard" instead of "not under ETH", included as (c)).

*Proof.* (a) *NP.* A certificate is a set `S ⊆ V` and a `u`–`v` path `π`; checking `u ∈ S ∌ v`, `|δ(S)| = c(u,v)` (one
maximum-flow computation) and `E(π) ⊆ δ(S)` takes polynomial time, and by Lemma 1.3(a), (c) a certificate exists if and
only if `cp(u,v) = c(u,v)`. *QP.* The input has size `s >= n`, so Theorem 7.1 gives time `2^{O(log^3 s)}`. *Promise.*
Connectivity and all distances by breadth-first search, and for every pair `x`, `y` the test `c(x,y) <= 2` by at most
three augmenting-path searches, take polynomial time; this decides `G ∈ DC`, `d(u,v) = 2` and `c(u,v) >= 3`.
(b) Suppose 3-SAT reduces to OPEN-DC by a polynomial-time Turing reduction (a many-one reduction is a special case). On a
formula of size `s` the reduction runs in time at most `s^a` for a constant `a`, so it asks at most `s^a` queries, each of
size at most `s^a`. Each query is answered in time `2^{O((log s^a)^3)} = 2^{O((log s)^3)}`: one that satisfies the
promise by Theorem 7.1, one that does not (recognised in polynomial time by (a)) by "no", which a reduction to a promise
problem must tolerate and which is the answer of the language of (a). So 3-SAT is in
`DTIME(2^{O((log s)^3)}) ⊆ QP`. Every problem in NP reduces to 3-SAT by a polynomial-time many-one reduction mapping
inputs of size `s` to formulas of size at most `s^b`, so it is decided in time `poly(s) + 2^{O((log s^b)^3)}`, and
NP ⊆ QP. By (a), OPEN-DC is in NP, so NP-hardness under many-one reductions and NP-completeness coincide.
(c) The Exponential Time Hypothesis says that there is `ε > 0` such that no algorithm decides 3-SAT on formulas with
`n_v` variables in time `O(2^{ε n_v})`. After deleting repeated clauses (polynomial time), a 3-CNF formula with `n_v`
variables has at most `(2 n_v)^3` clauses and size `s = O(n_v^3 log n_v)`. If OPEN-DC were NP-hard, the algorithm of (b)
would decide 3-SAT in time `poly(n_v) + 2^{O((log s)^3)} = 2^{O((log n_v)^3)}`, which is `O(2^{ε n_v})`: a contradiction. ∎

## 8. Repairs of the reviews included

| Review | Repair | Where |
|---|---|---|
| `verify/equivalence.md` §1 | `K` has no bridge (one line missing in Lemma 1) | Lemma 2.1(d) |
| `verify/equivalence.md` §3 | proof that the minimum cuts are the down-sets (asserted in Theorem 13(a)) | Lemma 2.7 |
| `verify/equivalence.md` §3 | proof of Corollary 12 (P2) | Lemma 2.8 |
| `verify/equivalence.md` §3 | proof of "`cp = c` iff yes-instance" (asserted in Theorem 13(a)) | Theorem 2.9 (in the `G_D` form; see §9 item 1) |
| `verify/rv-r6-chain.md` §3 item 2 | only Theorem 13(a) is used, with the repairs of `verify/equivalence.md` §3 | §2 |
| `verify/rv-r6-chain.md` §3 item 4 | sizes: `m <= n − 2` switches, at most `|Q| + |R| <= n + |E(G)|` nodes | Theorem 2.9, Lemma 3.2, Theorem 7.1 |
| `verify/rv-r6-chain.md` §1.3, §3 item 1 | `s = t`: yes-instance = `s = t` or a valid path exists; IDESC accepts `s = t` directly | Lemma 3.4(c), Definition 6.1, Theorem 6.2, hypothesis of Theorem 5.3 |
| `verify/rv-r6-chain.md` §1.4, §3 item 3 | "if ETH holds, it is not NP-hard"; NP membership; promise decidable in polynomial time | Corollary 7.2 |
| `verify/rv-core-65.md` §2.2 | the walk of Lemma 6.2 is itself a valid path | Lemma 4.3 |
| `verify/rv-core-65.md` §2.1 | `{w} ⊆ NE(E#_w)` only if `E_w ≠ ∅` (wording of `r5-core.md` §6.3) | Definition 4.1 (the identity is not used) |
| `verify/rv-core-65.md` §2.1 | `∪ Φ` and `△ Φ` agree when `Φ ⊆ U` | Definitions 5.1, 6.1 (union, flips inside `U`, `U'`) |
| `verify/rv-core-65.md` §2.3 | 5 positions suffice in Lemma 6.3 (improvement, not needed) | note after Lemma 4.4 |
| `verify/rv-r6-core.md` §2.4 | `m = 1`: `N = 0` and the strict bound for heavy rows fails, but there is no heavy row | proof of Lemma 5.2 |
| `verify/rv-r6-core.md` §2.8 | count of IDESC: `(m+1)^c` subsets of size `<= c`; anchors restricted to the last term (shape of Theorem 8.2) | Definition 6.1, Theorem 6.2 |
| `verify/rv-r6-core.md` §2.8, §2.10 | `m = 0`: `k` undefined; the instance is a yes-instance iff `s = t` | Definition 6.1, Theorem 6.2 |

## 9. Gaps found while assembling

None. Every step of the chain is proved above from the definitions, the max-flow min-cut theorem (computing `c`) and
von Neumann's minimax theorem; no statement of the sources had to be changed beyond the repairs of §8. The following
departures in route from the sources add no new statement and are recorded for the referee.
1. Theorem 2.9 proves "`cp(u,v) = c(u,v)` iff some `G_D` connects `u` and `v`" directly from Lemmas 2.4(d) and 2.7.
   `verify/equivalence.md` §3 (ii) proves the zigzag form ("iff a consistent zigzag exists"); the `G_D` form is the
   definition of ZZ in `r4-brief.md` §1, and it is the form that Lemma 3.3 needs.
2. Lemma 2.4(b) replaces the exact count of `theory-dc.md` Lemma 4(4) for minimum cuts by the inequality
   `|δ_K(S)| >= |δ_H(S ∩ Q)|` for all `S`, which is the first step of the proof of Lemma 4(4) (a split ear contributes
   at least one cut edge); Lemma 2.4(c) then follows from (a) and (b), and Lemma 4(4) itself is not needed.
3. In Theorem 2.9 the preorder is computed by at most `|Q|^2` maximum-flow computations, directly from Definition 2.5,
   instead of the residual closures `cl({u, y})` of one maximum flow (Picard and Queyranne) that `theory-dc.md` §4 and
   `verify/rv-r6-chain.md` §1.1 use; only polynomial time is claimed.
4. Definition 1.7 states the general switch form by its properties (as `r5-core.md` §6.1 uses it), and Construction
   3.1 with Lemma 3.2 shows that the conversion of `r4-general.md` §5.1 produces it. The dual part of Lemma 4.4 is
   proved by the reversed instance, following `verify/rv-core-65.md` §2.3; `r5-core.md` says only "the same proof with
   the order reversed".
5. Lemma 4.2(e) (fact F1 of `r4-switch.md` §2) is used by the source proof of Lemma 6.3 by reference; it is proved here.
6. Lemma 5.2 and Theorem 5.3 state that the flips lie in `U` (resp. `U'`); the source proof of Lemma 8.1 gives this
   (`Φ = A' ∩ U`, `Φ = B ∩ U'`), and `r5-core.md` §8.3 uses it for the completeness of IDESC. E-terms carry no F-anchors,
   since every E-term of the source proof has `Y_0 = ∅`.
7. NP membership (Corollary 7.2(a)) uses the certificate "a minimum cut and a path in it" (Lemma 1.3) instead of
   `theory-dc.md` Lemma 6 (a path alone, tested by one closure computation); both are polynomial checks.
