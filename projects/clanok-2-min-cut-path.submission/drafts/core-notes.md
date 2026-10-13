# Notes on `core.tex` (math core of article 2, 2026-10-12)

`core.tex` holds Sections 2 to 7 of the plan in `SPEC.md` §6 (no Introduction, Abstract, Conclusion).
Test build: `tmp/clanok-2-core/wrapper.tex` (class `sn-jnl`, the sample's package block, the figure PDFs of
`projects/clanok-2-min-cut-path/`): 17 pages with a one-page stub around the body, no LaTeX error, no undefined
reference, no overfull line; `scripts/check-text.ps1 -Path drafts/core.tex`: 0 findings.
Numbers below are those of the test build (theorem, lemma, proposition, corollary on one continuous counter).

## 1. Statements

| No. | Label | Content (one line) | Blueprint | Thesis |
|---|---|---|---|---|
| Def. 1 | `def:cut-path` | cut-path, `cp(u,v)`, minimum cut-path | - | Def. of cut-path (ch. 2) |
| Lemma 1 | `lem:basic-bounds` | `max{c,d} <= cp <= c+d-1`; `cp = d` iff a separating shortest path exists | S0 | Claims 6, 7 |
| Lemma 2 | `lem:minimum-cuts` | a minimum cut `C` leaves exactly two components, `C = delta(A)` for one `A` with `u` in `A`; a `u`-`v` path has an odd number of edges in `delta(A)` | tool for S1-S6 | Claim 14 (parity only) |
| Lemma 3 | `lem:uncrossing` | `\|delta(A∩B)\| + \|delta(A∪B)\| = \|delta(A)\| + \|delta(B)\| - 2m(A,B)` | tool for S5, S6 | - |
| Def. 2 | `def:class` | the class `DC_2` | S13 | Def. 37 |
| Prop. 4 | `prop:class` | `c >= 3` is an equivalence relation; `G` in `DC_2` iff every class has pairwise distances at most two; diameter two and cactus graphs lie in the class | S13 | - |
| Ex. 1 | `ex:counterexamples` | `G_a`, `G_b`: `cp = 3 < c+d-1`, both in the class, in neither subclass | S13 | Fig. 3.3 |
| Prop. 5 | `prop:easy-pairs` | the four kinds of pairs (`d = 1`; `c = 1`; `c = 2`; `d = 2`); in the class every pair is of one kind | S0 | Claims 6, 7 |
| Rem. 1 | `rem:bridges` | the component `K` of `u` after removing all bridges keeps `d`, `c`, `cp` and the class | S0 (bridges) | "G connected" remark after Claim 19 |
| Lemma 6 | `lem:orientation` | (i) a minimum cut = one edge of `p_1` and one of `p_2`, `F ⊆ p_1 ∪ p_2`; (ii) a `u`-`v` path has exactly one edge in each minimum cut, before it in `A`, after it outside; (iii) tail and head are well defined and every `u`-`v` path goes from tail to head | S1, S2 | - |
| Def. 3 | `def:pieces` | tail, head, piece, enters, leaves, square, link | SPEC §4 | Def. 39 (square graph) |
| Lemma 7 | `lem:pieces` | (i) no minimum cut splits a piece; (ii) edges of `F` = edges between different pieces; (iii) a `u`-`v` path visits a piece once, enters by an entering edge, leaves by a leaving edge | S3 | used tacitly |
| Lemma 8 | `lem:degrees` | (i) `u`, `v` in different pieces; (ii) entering and leaving edges of a piece on `p_j`; (iii) every piece is on `p_1` or `p_2`; link = piece on exactly one path | S4 | Claim 19 (terminals on `p_1 ∪ p_2`) |
| Def. 4 | `def:decomposition` | order `S_1..S_k`, terminals `a_i, b_i, c_i, d_i`, entering and leaving terminals, general path | SPEC §4 | Def. 38, 40 |
| Thm 9 | `thm:structure` | (i) entering edges and leaving edges of a square are minimum cuts; (ii) every `u`-`v` path visits all squares in the same order; (iii) the general paths `P_{i,j}` exist, are unique and cover all links and all of `F`; (iv) a `u`-`v` path follows exactly one of `P_{i,1}`, `P_{i,2}`; (v) distinct terminals of a square have `c >= 3` | S5 (i-iv), S6 (v) | Theorem 20 |
| Ex. 2, 3 | `ex:decomposition`, `ex:worked` | decompositions of `G_a` and of the worked example `G_1` | - | Fig. 3.7 |
| Lemma 10 | `lem:criterion` | `G \ R` has a `u`-`v` path iff `alpha_i`, `beta_i` are joined in `S_i \ R` for every `i` | S7 | claim inside the proof of Theorem 22 |
| Thm 11 | `thm:characterization` | `cp = d` iff a square has an `x`-`y` path `p` with (i) `d(u,x) + \|p\| + d(y,v) = d(u,v)` and (ii) `alpha`, `beta` separated in `S_i \ p`; otherwise `cp = d+1`; any graph with `c(u,v) = 2` | S9 | Theorem 22 (correctness part) |
| Ex. 4 | `ex:criterion` | criterion on `G_a`, `G_1` (`cp = d`), `G_1'`, `G_1''` (`cp = d+1`) | - | - |
| Prop. 12 | `prop:lengths` | (i) `u`-`v` paths of `G` = directed `u`-`v` paths of `vec G`; (ii) minimum length of a `u`-`v` path through `g`, `p`, `h` is `lambda^-(g) + \|p\| + lambda^+(h) + 2` | S8 | tables `D_1`, `D_2` of Alg. 7 |
| Cor. 13 | `cor:two-edges` | in the class a shortest `u`-`v` path has at most two edges in a square; `\|p\| = d(x,y) <= 2` | S10 | Claim 21 |
| Lemma 14 | `lem:residual` | (i) minimum cuts = sets closed in the residual digraph `D` of `p_1`, `p_2`; (ii) an edge of `p_1 ∪ p_2` is in `F` iff its ends lie in different strong components of `D` | S11 | - |
| Alg. 1 | `alg:cut-two` | decomposition, then at most four pairs per square, at most four candidate paths per pair | S11 | Algorithms 6, 7 |
| Thm 15 | `thm:linear-time` | in the class: decide `c(u,v) <= 2` and compute `cp` and a minimum cut-path in `O(\|V\|+\|E\|)` | S11 | Theorems 22, 23 |
| Ex. 5 | `ex:two-edges` | `G_a^+`: a trace with two edges in the first square, found through the candidate rule | - | - |
| Cor. 16 | `cor:class-pairs` | all pairs of the class except `d = 2`, `c >= 3`: linear time if `c <= 2`, one minimum cut if `d = 1` | S0, S11 | - |
| Rem. 2 | `rem:coarser` | unions of some minimum cuts give coarser decompositions with the same criterion; relation to the thesis | S14 | Transformations A, B, C, Alg. 5, Def. 40, 41 |
| Thm 17 | `thm:hardness` | deciding `cp = d` is NP-complete for pairs with `c(u,v) = 2` | S12 | - (new) |
| Prop. 18 | `prop:open-pairs` | `cp = c` iff a minimum cut contains a `u`-`v` path; such a path is odd, at least three edges if `d = 2` | S15 | proof of Theorem 15 (diameter two) |

Parts of statements are written inline as (i), (ii), ... and cited as `\cref{lem:pieces}(iii)`; the roman numbers
are typed by hand. Statements with parts: `prop:easy-pairs` (i-iv), `lem:orientation` (i-iii), `lem:pieces`
(i-iii), `lem:degrees` (i-iii), `thm:structure` (i-v), `thm:characterization` (conditions i, ii), `prop:lengths`
(i, ii), `lem:residual` (i, ii).

## 2. Deviations from the blueprint (SPEC §5)

1. **S0, linear time.** The brief's result (3) says "linear time for every pair except `d = 2`, `c >= 3`". A
   pair with `d(u,v) = 1` and `c(u,v) >= 3` has `cp = c(u,v)`, which needs one minimum-cut computation, not a
   linear-time one. Theorem 15 is stated for pairs with `c(u,v) <= 2` (decided in linear time by three
   augmentations); Corollary 16 lists the cases.
2. **S0, bridges.** True, proved in Remark 1, but not needed: no statement assumes that `G` is 2-edge-connected.
   Parts of `G` outside the 2-edge-connected component of `u` lie inside the pieces they hang on.
3. **S2.** Tail and head are defined without `p_1`, `p_2` (the end that lies in `A` for every minimum cut
   containing the edge); Lemma 6(iii) shows that this is the direction of `p_i`.
4. **S5.** The order of the squares is first defined along `p_1` (Def. 4); Theorem 9(ii) shows that it is the
   same for every `u`-`v` path. A general path is defined without `p_1`, `p_2` (it is determined by its first
   edge); only the names `P_{i,1}`, `P_{i,2}` and `a_i..d_i` use the two paths.
5. **S6.** The statement holds as in the blueprint. The proof idea there ("uncross with the entering or leaving
   cut") is not enough by itself: with `z` the other end of the edge of `F` at the terminal `s`, the case
   `z ∈ B` needs that `z` lies on `p_1 ∪ p_2` (so `\|delta(W∩B)\| >= 2`), and the case `z ∉ B` needs the term
   `2m(A,B)` of Lemma 3. Both are in the proof of Theorem 9(v).
6. **S8, S9 (main change).** Theorem 11 uses the distances of `G`: `d(u,x) + \|p\| + d(y,v) = d(u,v)`, not
   `lambda^-`, `lambda^+`. Reason: the statement needs no orientation and the algorithm needs only two
   breadth-first searches in `G`. The two conditions are not equivalent path by path: a path `p` with the
   `G`-distance condition can be only the last part of the trace of the shortest path (when every shortest
   `u`-`x` path enters the square at the other entering terminal). The theorem still holds, and its proof treats
   this case (the part of the trace before `x` joins `alpha` to `x` and avoids `p`). S8 is Proposition 12 as in
   the blueprint, with the cases `i = 1` and `i = k`; the sentence after it gives the blueprint's form of S9.
   Proposition 12 is not used by Theorem 15 and can be cut if the article must be shorter.
7. **S9.** A path `p` with (ii) has at least one edge (`x != y`), because a square is connected.
8. **S11.** Distances in `G` instead of `vec G`. Added: the cut-path that is returned, the decision `c <= 2`,
   and the remark that the algorithm is correct whenever every entering terminal of a square is at distance at
   most two from every leaving terminal of that square (the only use of the class). The strong components of the
   residual digraph are exactly the pieces (true on all tested graphs, not stated in the text; it would save the
   search in `G \ F`).
9. **S12.** The reduction starts from instances with `c_G(u,v) >= 3` (the graphs of the reduction of article 1
   contain at least three edge-disjoint threads), so no case `c_G(u,v) = 1` is needed. "The whole of `G` is one
   square" is stated only for `c_G(u,v) >= 3`; for `c_G(u,v) = 2` the text says that `G` is divided further
   (coordinator's correction, point raised by the figures agent).
10. **S14.** The coarser decompositions are made precise: `F'` = union of a nonempty set of minimum cuts. Then
    Lemma 7(i) holds for the minimum cuts inside `F'` only, and Theorem 9(v) (S6) can fail. See doubt 1 for what
    is not proved about the thesis.
11. **S15.** Stated for every pair (`cp = c` iff a minimum cut contains a `u`-`v` path). By the coordinator's
    instruction the section ends with one sentence: no polynomial algorithm is known for the class and pairs
    with `d = 2`, `c >= 3`; nothing is said about general graphs or about the open questions of article 1.
12. **Figures** are included at natural size (`\includegraphics{name.pdf}`), as the figures README asks, not
    with `width=` as the brief said.

## 3. The thesis (Section 3.3): what is kept, what was wrong or imprecise

Kept and right:
- Definition 37 (the class) and Figure 3.3 (the two counterexamples).
- The notions square graph, general path, general square graph (Definitions 38-40), now defined from the
  minimum cuts. For `G` in the class the decomposition of the article satisfies Definition 40: a square with its
  terminals is a square graph (its edge set is that of the induced subgraph, and condition 2 holds by
  Theorem 9(v)), and a general path with its two end terminals is a general path of Definition 38.
- Claim 19 (critical vertices lie on `p_1 ∪ p_2`): terminals are ends of edges of `F`, and `F ⊆ p_1 ∪ p_2`.
- Claim 21 (a shortest path has at most two edges in a square): Corollary 13.
- Theorem 20 (a decomposition exists in the class): Theorem 9.
- Algorithm 6 and the statement of Theorem 22: Theorem 11 with `\|p\| <= 2`.
- The idea "at most four candidates" of Algorithm 7 and the linear running time of Theorem 23.

Wrong or imprecise (for the author):
1. **Definitions 38-40** describe a decomposition by properties of the subgraphs. They do not say that one
   exists, which one is meant (Figures 3.7 and 3.8 show two for one graph), or that a `u`-`v` path passes the
   squares in order and uses one of the two general paths. The proofs of Claims 19, 21 and Theorem 22 use these
   facts without proof. In the article they are Lemma 7 and Theorem 9(ii), (iv).
2. **Definition 39, condition 2** puts the distance bound into the definition. It is a consequence: distinct
   terminals of one square have cut-value at least three (Theorem 9(v)), so the class gives distance at most two.
3. **Claim 19, proof.** It argues about "the transition from `S_i` to `S_{i+1}`" and degrees of general paths
   and never uses how the squares were obtained. The statement is immediate from `F ⊆ p_1 ∪ p_2`.
4. **Transformations A, B, C and Algorithm 5** are not specified precisely: Transformation B says "find a general
   path `P` contain a vertex from `H_xy`"; Transformation C defines the new general paths as intersections
   (`H_x ∩ P_{x,1} ∩ P_{x,2}`), which are empty or not what is meant; "Count" of cut edges in `S_work` does not
   say what happens to an edge outside it. The proof of Theorem 20 is headed "Intuition of correctness", and the
   bound `O(n^k)` has no `k`. The article does not use the transformations.
5. **Claim 21, proof.** Case 1 uses the distance inside `S_i`, although Definition 39 bounds the distance in
   `G`. Case 2 identifies vertices from Figure 3.12 ("`c_{i-1}` is identified with `d_{i-1}`") and is not an
   argument. Correct proof: the part of a shortest path in a square is a shortest path of `G` between an
   entering and a leaving terminal.
6. **Theorem 22.** The key equivalence ("`cp = d` iff some square has a path that is part of a shortest path and
   separates `alpha` from `beta`") is asserted, not proved; it is Lemma 10 with Theorem 11. One point is missed:
   `d(u,x) + d(x,y) + d(y,v) = d(u,v)` does not make `p` the whole part of the shortest path in the square (see
   deviation 6). The test is still correct. Running time `O(n^k + n^7)` becomes linear.
7. **Algorithm 7.** Lines 10-14 start with `P ← ∅` and then intersect (`P ← P ∩ last edge of path ...`), so `P`
   stays empty; "the last edge of path `alpha` and `x`" is undefined; line 18 "remove edges violating this" is
   not an operation on paths. Line 21 removes the *vertices* of `p`, Algorithm 6 (line 12) the *edges*; edges
   are right. The correctness bullets repeat one bullet twice and do not prove that four candidates suffice. In
   the article the candidates are the paths `x, w, y` with `w` a neighbor of `x` or `y` on one fixed
   `alpha`-`beta` path, with a proof.
8. **Theorem 23** assumes the decomposition as given, and its sentence "for every pair ... such that the
   decomposition `H` of `G` between `u` and `v`" has no verb. The "dynamic programming" tables `D_1`, `D_2` are
   breadth-first search distances. In the article the decomposition is computed in linear time as well
   (Lemma 14), so the whole computation is linear.
9. The thesis solves the pairs with `c(u,v) = 2` only and does not say that deciding `cp = d` is NP-complete for
   such pairs outside the class (Theorem 17, new).

## 4. Graphs to verify

Edges are written `xy`. For every graph the pair is `(u, v)`.

**`G_a`** (counterexample (a)). `V = {u,v,a,b,s,t}`, `E = ua, us, sb, ab, at, tv, bv`.
`d = 3`, `c = 2`, `cp = 3`. Minimum cuts: `{ua,us}`, `{ua,sb}`, `{at,bv}`, `{tv,bv}`. `F = E \ {ab}`, directed
`u→a, u→s, s→b, a→t, t→v, b→v`. Pieces `{u}, {a,b}, {v}, {s}, {t}`. Squares `S_1 = {u}`, `S_2 = {a,b}`,
`S_3 = {v}`; links `{s}`, `{t}`. With `p_1 = u,a,t,v`, `p_2 = u,s,b,v`: `a_2 = c_2 = a`, `b_2 = d_2 = b`;
`P_{1,1} = ua`, `P_{1,2} = us,{s},sb`, `P_{2,1} = at,{t},tv`, `P_{2,2} = bv`. Criterion: `i = 2`,
`(x,alpha) = (a,b)`, `(y,beta) = (b,a)`, `p = a,b`. Minimum cut-path `u,a,b,v`. In the class; diameter 3;
`c(a,b) = 3`. The pair `(s,t)` of the same graph also has `cp = d = 3`.

**`G_b`** (counterexample (b)). `G_a` plus `av`, `ub`. `d = 2`, `c = 3`, `cp = 3`; the minimum cut
`delta({u,s,b}) = {ua,ab,bv}` is the path `u,a,b,v`. In the class; only `s`, `t` are at distance three.

**`G_1`** (worked example). `V = {u,v,1,...,8}`, `E = u1, u2, 12, 13, 23, 36, 24, 45, 57, 67, 68, 7v, 8v`
(10 vertices, 13 edges). `d = 5`, `c = 2`, `cp = 5`. Minimum cuts: `{u1,u2}`, `{36,24}`, `{36,45}`, `{36,57}`,
`{68,7v}`, `{8v,7v}`. `F` = all edges except `12, 13, 23, 67`, directed `u→1, u→2, 3→6, 2→4, 4→5, 5→7, 6→8,
8→v, 7→v`. Pieces `{u}, {1,2,3}, {4}, {5}, {6,7}, {8}, {v}`. Squares `S_1 = {u}`, `S_2 = {1,2,3}`,
`S_3 = {6,7}`, `S_4 = {v}`; links `{4}, {5}, {8}`. With `p_1 = u,1,3,6,8,v`, `p_2 = u,2,4,5,7,v`: `a_2 = 1`,
`b_2 = d_2 = 2`, `c_2 = 3`, `a_3 = c_3 = 6`, `b_3 = d_3 = 7`; `P_{1,1} = u1`, `P_{1,2} = u2`, `P_{2,1} = 36`,
`P_{2,2} = 24,{4},45,{5},57`, `P_{3,1} = 68,{8},8v`, `P_{3,2} = 7v`. Distances from `u`: `1:1, 2:1, 3:2, 4:2,
5:3, 6:3, 7:4, 8:4, v:5`; to `v`: `7:1, 8:1, 5:2, 6:2, 3:3, 4:3, 1:4, 2:4, u:5`. Shortest `u`-`v` paths:
`u,1,3,6,7,v`; `u,2,3,6,7,v`; `u,2,4,5,7,v`; `u,1,3,6,8,v`; `u,2,3,6,8,v`. Criterion: `i = 3`,
`(x,alpha) = (6,7)`, `(y,beta) = (7,6)`, `p = 6,7`. Minimum cut-path `u,1,3,6,7,v`. In the class (diameter 5,
largest cut-value 3).

**`G_1'`** = `G_1` plus a vertex `9` and the edges `69`, `79`. `d = 5`, `c = 2`, `cp = 6`. Same minimum cuts and
`F`; `S_3 = {6,7,9}`. Paths with at least one edge and condition (i): the edges `13`, `23` (in `S_2`) and `67`
(in `S_3`); none satisfies (ii). In the class.

**`G_1''`** = `G_1` without the vertex `5`, plus the edge `47`: `E = u1, u2, 12, 13, 23, 36, 24, 47, 67, 68, 7v,
8v`. `d = 4`, `c = 2`, `cp = 5`. Minimum cuts `{u1,u2}`, `{36,24}`, `{36,47}`, `{68,7v}`, `{8v,7v}`; squares as
in `G_1`, links `{4}`, `{8}`. Only shortest path `u,2,4,7,v`. No path with an edge satisfies (i). In the class.

**`G_a^+`** = `G_a` plus a vertex `r` and the edges `ur`, `rb`. `d = 3`, `c = 2`, `cp = 3`. Minimum cuts
`{at,bv}`, `{tv,bv}`; `F = {at, tv, bv}`. Pieces `{u,s,r,a,b}, {t}, {v}`. Squares `S_1 = {u,s,r,a,b}`,
`S_2 = {v}`; link `{t}`. `a_1 = b_1 = u`, `c_1 = a`, `d_1 = b` (for `p_1 = u,a,t,v`). Criterion:
`(x,alpha) = (u,u)`, `(y,beta) = (b,a)`, `l = 2`, `q = u,a`, candidate `w = a`, `p = u,a,b`. In the class.

Further graphs used in the checks, not in the text:
- `G_a` plus a vertex `w` adjacent to `a`, `b`: `cp = 4 = d + 1` (the edge `ab` no longer separates).
- Four distinct terminals with a separating trace of two edges (not in the class): `E = ux, uk, kl, lA, xB, xz,
  zB, Ay, Aq, qy, xw, wy, yv, Bm, mn, nv` (13 vertices; `A`, `B` stand for `alpha`, `beta`). `d = 4`, `c = 2`,
  `cp = 4`; squares `{u}`, `{A,B,q,w,x,y,z}`, `{v}`; `p = x,w,y`.
- `C_6` with antipodal `u`, `v` (`cp = 4`, squares `{u}`, `{v}`, four links); two 4-cycles sharing a vertex `w`
  (`cp = 5`, squares `{u}`, `{w}`, `{v}`); `K_4` on `1..4` with `u` adjacent to `1, 2` and `v` adjacent to
  `3, 4` (`cp = 4`, squares `{u}`, `{1,2,3,4}`, `{v}`, no link).
- Gadget of Theorem 17: any `G` with `c_G(u,v) >= 3` plus `u'`, `s_1`, `s_2`.

Scratch checks made while writing (scripts in `tmp/clanok-2-core/`, disposable; the checks agent should repeat
them independently): Lemmas 2, 3, 6, 7, 8, 10, 14, Theorems 9, 11, Propositions 4, 12, 18, Corollary 13,
Remark 1, the coarser decompositions of Remark 2 (random subfamilies of minimum cuts), the padding of
Theorem 17 and the output of Algorithm 1 against brute-force `cp`. Inputs: all 995 connected graphs with 2 to 7
vertices (6675 pairs with `c = 2`), about 450 random graphs with 7 to 12 vertices, and about 2400 random chains
of blocks with up to 15 vertices (155 of them with `cp = d`). No failure.

## 5. Figure requests

All seven figures the text uses exist in `projects/clanok-2-min-cut-path/` (state of 2026-10-12, 17:57).

| File | Label | Caption in `core.tex` | Remark |
|---|---|---|---|
| `graph-classes.pdf` | `fig:graph-classes` | The class and its two subclasses; (a) and (b) are the graphs `G_a` and `G_b` | the points (a), (b) of the drawing are named in the caption |
| `counterexamples.pdf` | `fig:counterexamples` | The graphs `G_a` (a) and `G_b` (b); the cut-path `u,a,b,v` is red | - |
| `square-decomposition.pdf` | `fig:square-decomposition` | squares (boxes), links (ellipses), edges of `F` directed from tail to head | `P_{i,1}` from `c_i` to `a_{i+1}`, `P_{i,2}` from `d_i` to `b_{i+1}`, as in Def. 4 |
| `decomposition-example.pdf` | `fig:decomposition-example` | The square decomposition of `G_a` | Example 2 |
| `worked-example.pdf` | `fig:worked-example` | The graph `G_1` and its square decomposition | drawn by the figures agent after this draft named it; exact content: vertices `u, 1..8, v`, edges of `G_1` above; `F` dashed and directed as in Section 4 of these notes; boxes `S_1 = {u}`, `S_2 = {1,2,3}`, `S_3 = {6,7}`, `S_4 = {v}`; ellipses `{4}`, `{5}`, `{8}`. Optional: the cut-path `u,1,3,6,7,v` in red |
| `square-terminals.pdf` | `fig:square-terminals` | A square and a trace `x,w,y` that separates `alpha` from `beta` in (a) and not in (b) | the drawing (parts `{alpha,x,y}` and `{w,beta}`) can occur; the labels have no index `i`, the text has |
| `padding.pdf` | `fig:padding` | The graph `G'` in the proof of Theorem 17; the dashed edges form `F` if `c_G(u,v) >= 3` | names `u'`, `s_1`, `s_2` as in the text |

`transformations.pdf` is not used (the article does not use the transformations; Remark 2 mentions them in one
sentence).

## 6. CITE needs

Each `% CITE:` comment in `core.tex` stands after the sentence that needs the source.

| Place | Fact that needs a source |
|---|---|
| after Lemma 3 | submodularity of the cut function of an undirected graph (the lemma itself is proved) |
| Section 3, first paragraph | Menger's theorem, edge version (article 1 cites Diestel, Corollary 3.3.5) |
| before Lemma 14 | residual graph of a flow; minimum cuts as closed sets of the residual graph (the lemma itself is proved) |
| proof of Theorem 15, first step | augmenting paths: `k` augmentations in `O(k(\|V\|+\|E\|))` time; a flow of value two decomposes into two edge-disjoint paths in linear time (not proved in the text) |
| proof of Theorem 15, running time | breadth-first search; strong components in linear time (Tarjan) |
| proof of Corollary 16 | a polynomial-time algorithm for a minimum `u`-`v` cut |

Citations with locators that must be re-checked against the final texts: article 1 (`Michel2026MinCutPath`):
Lemma 2.3, Corollary 3.12, Lemma 6.1, Theorems 5.5, 6.2, 3.10 (numbers of `projects/clanok-1-min-cut-path/main.tex`
of 2026-10-10); thesis (`Michel2025Thesis`): Section 3.3, Definition 40.

## 7. Macros, packages, preamble

- Macros used: `\cp`, `\DC`, `\MinCutPath`, `\SSP` (`\CP` is not used). Nothing else is needed.
- **cleveref and the shared counter.** With `\newtheorem{lemma}[theorem]{Lemma}` (as the brief proposed)
  `\cref{lem:...}` prints "theorem 6" for Lemma 6. The test build uses, after the sample's package block,
  `\usepackage{thmtools}`, `\usepackage[capitalise,noabbrev]{cleveref}` and
  `\declaretheorem[name=Lemma, style=thmstyleone, sibling=theorem]{lemma}` (the same for theorem, proposition,
  corollary; example, remark, definition keep the sample's `\newtheorem` lines). Then every reference prints
  correctly. `thmtools` is installed.
- `\algrenewcommand\algorithmicrequire{\textbf{Input:}}` and `\algrenewcommand\algorithmicensure{\textbf{Output:}}`.
- Algorithm lines have labels `line:...` (prefix of `latex-conventions.md` §7, not in the list of SPEC §4).
- Subsections 2.1 and 2.2 have the labels `sec:cut-paths`, `sec:class`.
- The class prints "Fig. 3" in captions, `\cref` prints "Figure 3" in the text.
- The test build shows the known pdfTeX warning "destination with the same identifier (name{figure.N})" once
  per figure (project notes, "Known problems": `\RequirePackage{float}` before `\documentclass` removes it).
- The body refers to no label outside itself (not to `sec:introduction`, `sec:conclusion`).

## 8. Open doubts, ranked

1. **Remark 2 and the thesis.** Proved: the statements for `F'` (union of some minimum cuts); that the
   construction of the thesis can stop early (`C_4` with opposite `u`, `v` and the cut at `u`: two squares
   instead of two squares and two links); that the decomposition of the article satisfies Definition 40 in the
   class (checked against Definitions 38-40 by hand, not by a script). Not proved: that every run of Algorithm 5
   of the thesis removes only edges of `F` and ends with a union of minimum cuts; the algorithm is not specified
   well enough to prove it. The remark therefore describes the construction and does not claim it.
2. **Theorem 17** needs that the graphs of the reduction of article 1 are connected and have at least three
   edge-disjoint `u`-`v` paths (article 1, text after Theorem 3.10: `c(u,v) >= 2n + 7m`). Re-check if article 1
   changes. The theorem also answers, for the cut-value, the question about bounded `c(u,v)` in the conclusion of
   article 1; the body does not say so (left to the Introduction and to the author).
3. **First step of Theorem 15** (three augmentations, two edge-disjoint paths from the flow) is cited as
   standard and not proved.
4. **Proposition 12** is correct and tested but not needed for the main line (deviation 6).
5. **Notation inherited from SPEC §4:** `c_i`, `d_i` are terminals while `c(.,.)`, `d(.,.)` are the cut-value
   and the distance; `p` is a path in a square while `p_1`, `p_2` are the two fixed paths; `s`, `t` are vertices
   of `G_a`, the tail and head in Proposition 12 and two terminals in Theorem 9(v); `s_1`, `s_2` are the new
   vertices of Theorem 17. No clash inside one statement.
6. **Vertex names of `G_1`** are digits, so edges print as `12`, `36`.
7. **Running time** assumes adjacency lists; "marking the neighbors of `x` and of `y`" costs their degrees in
   `G`, which is within the bound because a square has at most four edges of `F` at its terminals in total
   beyond its own edges (two entering, two leaving).
8. **Observation for the later phase, not in the text and not fully proved.** In the class, a separating trace
   forces `d(alpha, beta) <= 2` although `alpha`, `beta` are separated in `S_i \ p`. On all tested class graphs
   the squares with a separating trace had at most three distinct terminals (`y = alpha` and `beta = x`;
   `y = alpha` only; `beta = x` only; `x = alpha = u` in `S_1`). A square with four distinct terminals and a
   separating trace exists outside the class (Section 4). This may shorten the algorithm or help with the open
   pairs.
   **Refuted by the checks agent (2026-10-12):** the "at most three distinct terminals" part is false in the
   class. It fails on 3 of 406 chain witnesses; the smallest instance found has 21 vertices and 25 edges
   (`d = cp = 9`, `c = 2`), with the trace `9, 7, 10` in the square `{6, 7, 8, 9, 10}` and the four distinct
   terminals `9, 10, 6, 7` (edge list in `checks/README.md`). The part `d(alpha, beta) <= 2` holds.
