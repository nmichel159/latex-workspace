# Adversarial verification of the reduction of the open case of DC to ZZ (agent verify-equivalence)

Status: complete, 2026-10-12. Scripts: `verify/equivalence/` (own code; the shared `checks/mcp.py` was imported only
afterwards, by `crosscheck.py`, to cross-check the primitives). Targets: `theory-dc.md` Lemma 1, Lemma 2, Lemma 4, Proposition 5, Proposition 11, Corollary 12,
Theorem 13 (a), (b), (c); `dc-hardness.md` Theorem 1.

Verdict labels: **holds** (every step read and justified; exact checks agree), **holds, repair given** (a step is
missing or misattributed; a complete replacement is written here), **gap** (a step is not justified and no repair is
given), **false** (counterexample).

## 0. Verdicts

| Claim | Verdict | Notes |
|---|---|---|
| Lemma 1 (bridges) | holds | one line added: `K` itself is 2-edge-connected (§1) |
| Lemma 2 (O1) | holds | |
| Corollary 3 | holds | |
| Lemma 4 (ears) | holds | ears at `u` or `v`, ears with `p = s`, ears with `a = b` are covered by the proof and by the checks |
| Proposition 5 | holds | |
| Problem Π, realisation direction | holds, repair given | cites Lemma 4(4) outside its hypotheses; direct argument in §2 |
| Proposition 11 | holds | valid for multigraphs and weighted graphs |
| Corollary 12 (P2) | holds, repair given | theory-dc.md gives no proof; proof in §3 |
| Theorem 13(a) | holds, repair given | "minimum cuts = down-sets" and the equivalence with a consistent zigzag are asserted without argument; proofs in §3 |
| Theorem 13(b) | holds | `M >= 1` already suffices (`O(q^2)` vertices instead of `O(q^4)`); all instances with `N <= 3` are no-instances; `G(Π) ∈ DC` iff P2 (§7) |
| Theorem 13(c) | holds | |
| dc-hardness.md Theorem 1 | holds, scope remark | it concerns `cp = c` for pairs with `d = 2`, `c >= 4`; it says nothing about pairs with `d >= 3`, `c = 3` of that class |

No counterexample was found to any of the claims. Hence, with the repairs of §2-§3, the statement "the open case of DC
is polynomially equivalent to ZZ restricted to P2" is proved; its complexity remains open. Computations: §6.

## 1. Lemmas 1, 2, 4, Corollary 3, Proposition 5 (theory-dc.md §2)

**Lemma 1 — holds.** The first paragraph is right: a simple path uses a bridge `b = pq` once, its two sub-paths avoid
`b`, so its ends lie in different components of `G - b`. (i)-(v) follow as written. The sentence "From now on `G` is
2-edge-connected" needs one more line, not written in theory-dc.md: *`K` has no bridge.* An edge `e` of `K` is not a
bridge of `G`, so it lies on a cycle `C` of `G`; a bridge lies on no cycle, so `C ⊆ G - B`, hence `C ⊆ K` and `e` is
not a bridge of `K`.

**Lemma 2 — holds.** `P` meets `X` and starts and ends outside `X`, so it uses at least two edges of `δ(X)`; with
`|δ(X)| <= 2` these are all of `δ(X)` and `P` meets `X` in one sub-path. The counts are exact:
`|δ(A - X)| = |D| + #{i : y_i ∈ A}`, `|δ(A ∪ X)| = |D| + #{i : y_i ∉ A}` (an edge with no end in `X` is cut by `A - X`
and by `A ∪ X` iff it is cut by `A`; an edge inside `X` is cut by neither). Both sets contain `u` and not `v` because
`X ∩ {u, v} = ∅`.

**Corollary 3 — holds.** `c(x,z) >= min(c(x,y), c(y,z))` is the usual triangle inequality of local edge connectivity.

**Lemma 4 — holds.** (1) `|δ(Y)| >= 1` by connectivity and `!= 1` since there is no bridge. (2), (3) as written; in (3)
"one component" uses that `G[X]` has no edge between its components, so `δ(Z) ⊆ δ(X)` for each component `Z`.
(4) In the case `p, s ∈ A`, `Z = X - A`: every edge of `δ(Z)` ends in `X ∩ A` or is a boundary edge of `X` with outer
end `p` or `s`, so `δ(Z) ⊆ δ(A)`, `δ(A ∪ Z) = δ(A) - δ(Z)` has at most `c - 2` edges: contradiction. The split case is
right: `δ(A ∪ X) = (δ(A) - E[X]) ∪ {sb}` and `δ(A - X) = (δ(A) - E[X]) ∪ {pa}`.
Hidden assumptions checked: the proof never uses `p, s ∉ {u, v}` (`u ∈ A`, `v ∉ A` always, which only fixes the case);
`a = b` (short ear) and `p = s` (then `a != b` in a simple graph) fall under the stated cases; an ear with `p = s` has
no ear edge in `H` and is never split.

**Proposition 5 — holds.** In `A(B)` the labels `p, s` of each ear are fixed once; a split ear then contributes exactly
one cut edge (`sb` if `X ⊆ A(B)`, `pa` otherwise), an unsplit ear none. With Lemma 4(4) this gives
`|δ_G(A)| = |δ_H(A ∩ Q)|` for minimum cuts `A` of `G`, and `A(B) ∩ Q = B` gives surjectivity. Paths: Corollary 3 puts
a path inside a minimum cut of `G` into `G[Q]`. Distance clause: a common neighbour `w ∉ Q` of `x, y ∈ Q` lies in an ear
whose two boundary edges are `xw, yw`.

## 2. Problem Π (realisation direction) — holds, repair given

The direction `G -> Π` is Proposition 5 (DC gives the Π distance condition through its distance clause). For
`Π -> G(Π)` theory-dc.md says the minimum cuts correspond "as in Lemma 4(4)"; Lemma 4 assumes that `Q` is the
3-edge-connected class of `u` in a 2-edge-connected graph and that the ears are maximal ear sets, which `G(Π)` need not
satisfy (theory-dc.md itself notes that `c(x,y) >= 3` on `Q` is not needed). Replacement: for `B ⊆ Q`, an ear vertex
`w` with neighbours `p, s` adds 0 cut edges if it lies on the side of both, 1 if `p, s` are split, 2 if it lies opposite
both; so `min{|δ(A)| : A ∩ Q = B} = W(δ(B))`, attained exactly when every ear vertex lies on the side of one of its
neighbours. Hence the minimum cuts of `G(Π)` are these sets over the minimum cuts `B` of `W`, `c_{G(Π)} = c_W`, an ear
vertex has at most one cut edge (so it is never internal to a path inside a minimum cut), and a `u`-`v` path inside a
minimum cut of `G(Π)` is a real path inside `δ_W(B)` and conversely.

## 3. Proposition 11, Corollary 12, Theorem 13(a)

**Proposition 11 — holds.** The identity
`w(δ(A_1)) + w(δ(A_2)) = w(δ(A_1 ∩ A_2)) + w(δ(A_1 ∪ A_2)) + 2 w(A_1 - A_2, A_2 - A_1)` holds for every non-negative
weighting, so the proof is valid in `H` (multigraph) and in `W`. Its hypothesis is "`x` and `y` incomparable".

**Corollary 12 — holds, repair given (theory-dc.md states it without proof).**
*Proof.* Let `x, y` be incomparable. By Proposition 11 no real or ear edge joins them, so by the distance condition of
Π they have a common real neighbour `z`. By Proposition 11 (edges `zx`, `zy`) `z` is comparable with `x` and with `y`.
`y <= z <= x` or `x <= z <= y` would make `x, y` comparable, so `z <= x, y` or `z >= x, y`. If `z` were equivalent to
`x`, comparability of `z` and `y` would make `x, y` comparable; likewise for `y`. So `zx, zy` join non-equivalent
elements (they lie in the `R` of Theorem 13(a)) and `z` lies strictly below both or strictly above both. ∎

**Theorem 13(a) — holds, repair given.** Two steps are asserted without argument in theory-dc.md.
*(i) The minimum cuts of `H` are exactly the down-sets `D` with `u ∈ D`, `v ∉ D`.* A minimum cut is a down-set by the
definition of `<=`. Conversely, for `y ∈ D` some minimum cut contains `y` (otherwise `v <= y` vacuously and `v ∈ D`);
the intersection `C(y)` of the minimum cuts containing `y` is a minimum cut (the identity above: intersections and unions
of minimum cuts are minimum cuts) and equals `{x : x <= y} ⊆ D`. So `D = ⋃_{y ∈ D} C(y)` is a minimum cut. No
Picard-Queyranne argument is needed.
*(ii) `cp = c` iff a consistent zigzag exists.* If a real path `x_0 ... x_L` lies in `δ(A)` with `A` a minimum cut, then
`x_i ∈ A` iff `i` is even; consecutive vertices are comparable (Proposition 11) and `x_{i+1} <= x_i` would put
`x_{i+1}` into `A` for even `i` (similarly for odd `i`), so the path alternates strictly; it uses no edge between
equivalent elements; a valley `a >= ` a peak `b` would put `b ∈ A`. Conversely, for a consistent zigzag put
`D = {x : x <= a for some valley a}`: `u ∈ D`; a peak `b ∈ D` (in particular `b = v`) would give a valley `a >= b`; so
`D` is a minimum cut by (i), every zigzag edge crosses it, and Proposition 5 lifts it to `G`. Dropping real edges
between equivalent elements loses nothing, since such edges are cut by no minimum cut.

## 4. Theorem 13(b), (c)

**Theorem 13(b) — holds.** The four-case count (1, 1, 1, 3 per strict pair `a < b`) is right, including the boundary
cases `a = u` (then `a ∈ A`) and `b = v` (then `b ∉ A`). Remarks:
- The formula is the cut value in the weighted graph `W` on `Q`, i.e. in `G(Π)` with every ear vertex on the side of a
  neighbour (§2); "every cut `δ(A)`" in the statement should be read this way.
- Every strict pair contributes at least 1 whatever `A` is, so a set that splits a class costs at least `N + M`; `M = 1`
  already makes all minimum cuts down-sets. The stated `M > N` is correct but makes the graph `O(q^4)` instead of
  `O(q^2)` (checked with both values, §6).
- Size: `|V(G(Π))| = q + (N - |R|) + #{a < b : a != u} + #{a < b : b != v} + M · #{equivalent pairs}`; polynomial.
- `d(u,v) = 2`: the pair `u < v` is not in `R`, so it gets an ear vertex; no edge `uv` exists.
- DC: strict pairs are at distance 1 or 2, equivalent pairs carry ears, incomparable pairs have a common real neighbour
  by P2, ear vertices have degree 2. Only "some common real neighbour" is used; "above both or below both" then holds
  automatically (argument of Corollary 12).
- Excluded instances: if `N <= 3`, then either `Q = {u, x, v}` with one middle element (a middle element alone gives
  the three pairs `u < x < v`, `u < v`; a second element adds at least two more), and the only `u`-`v` walk `u x v`
  has even length; or every element is equivalent to `u` or `v`, `N = |[u]| · |[v]| <= 3`, one class is a singleton,
  and a zigzag would alternate between the two classes: with `[u] = {u}` it has no second valley, with `[v] = {v}` its
  first peak would be `v` (`uv ∉ R`). So every instance with `N <= 3` is a no-instance (checked: 21 of 21 for
  `q <= 5`), and a many-one reduction maps the instances excluded by "at least three comparable pairs" (and by
  `c >= 4` in dc-hardness.md Theorem 1) to a fixed no-instance.
- The equivalence of the answers is the argument of (a)(ii) together with §2.

**Theorem 13(c) — holds.** The generating relations are acyclic (`c_j < P_{j,k} < T_i / F_i < a_i, a_{i+1}`,
`e_0 < d, a_1`), so they generate a partial order with least `u`, greatest `v`; every `R`-pair is strictly ordered.
In `(Q, R)` the vertices `u, d, e_0, v` have degree at most 2 and the gadgets are diamonds `a_i {T_i, F_i} a_{i+1}`,
`c_j {P_{j,k}}_k c_{j+1}`, so every `u`-`v` path has the stated form and is a zigzag. Valleys are among
`u, e_0, T_i, F_i, c_j`, peaks among `d, a_i, P_{j,k}, v`; the only relations "valley >= peak" are the conflict
relations. NP membership: consistency of a given zigzag is `O(L^2)` comparisons. The graph statement follows from the
realisation of (b), whose cut formula does not use P2.

## 5. dc-hardness.md Theorem 1 — holds, scope remark

Direction ZZ+P2 to `DC'`: Theorem 13(b) and `DC ⊆ DC'`; instances with `N <= 3` are no-instances (§4).
Direction `DC'` to ZZ+P2: the preorder on `V`, its down-sets = minimum cuts (argument of §3 (i)), traces on `Q4`
(the down-set generated by `D ⊆ Q4` in `V` does not contain `v`, since `v <= d ∈ D` would put `v ∈ D`), Corollary 4.2(b)
of theory-hardness.md (re-read: Lemma 4.1 and the posimodularity step are right), Lemma 4.3 (i), (ii). The exchange
step for `z ∉ Q4` is right: `|δ(C - W)| = |δ(C)| - e(W, V - C) + e(W, C - W)` with `zx, zy ∈ e(W, V - C) ∩ δ(Y)` and
`e(W, C - W) ⊆ δ(Y) - {zx, zy}`, so `|δ(C - Y)| <= c - 1`; the case `z ∉ A ∪ B` is symmetric. The order of the
argument should state "edges join comparable vertices (Lemma 4.3(i))" before using it for the zigzag.
*Scope.* The theorem is about the question `cp = c` for pairs with `d(u,v) = 2`, `c(u,v) >= 4`. In the class
"`d <= 2` or `c <= 3`" the pairs with `d >= 3` have `c <= 3`, and for `c = 3`, `d >= 3` (where
`max(3, d) <= cp <= d + 2`) neither dc-hardness.md nor theory-dc.md gives an algorithm. "The class is polynomially
equivalent to the open case of DC" is therefore true for its `d = 2` part only; the complexity of Min Cut-Path on the
whole class is not settled by Theorem 1.

## 6. Computations (scripts in `verify/equivalence/`)

Own implementation (`eqcore.py`): cut values of all vertex sets tabulated with numpy (`n <= 16`), minimum cuts and
connectivities read off the table, bridges, ears and `H` built from the definitions, the preorder from the list of
minimum cuts, two ZZ solvers (search for a consistent zigzag; enumeration of all down-sets), the realisation of
Theorem 13(b), and for large graphs an exact PIMC search that extends alternating prefixes and prunes with the
separation test "even vertices vs odd vertices + `v` separable by `c` edges" (independent of Lemma 2 and of ears).
Every result file ends with its violation count; all are 0.

| Run (script, result file) | Instances | What is compared | Violations |
|---|---|---|---|
| `run_small.py`, `results-small.txt` | all 12112 connected graphs with 2-8 vertices (8 vertices: `gen8.py`, 12346 graphs, 11117 connected, as in OEIS A000088/A001349), all ordered pairs | Lemma 1 on 142656 pairs (`v ∈ K`, all `d`, all `c`, minimum cut edge sets, `cp`, DC); Lemma 4 (1)-(4) by brute force over all vertex sets on 398478 pairs with `c >= 3` (302266 ears: 189870 at `u` or `v`, 4286 with `p = s`, 18988 with >= 2 vertices); Proposition 5 (`c_H`, traces, surjectivity, PIMC, distance clause); Proposition 11 for every edge of `H` and of `G`; Lemma 2 and Corollary 3 on 443140 paths inside minimum cuts; Theorem 13(a) on 131186 pairs with `d = 2`, `c >= 3` (121588 in DC: 712 yes; P2 holds in all; it fails in 36 non-DC pairs, so the test is not vacuous); `cp` = `c` iff PIMC (`cp` from the definition) on all of them; dc-hardness Theorem 1 on 39266 pairs (482 yes) | 0 |
| `run_random.py 2 2 20000`, `results-random-2-2.txt` | 18824 connected DC graphs, 9-16 vertices (core + ears, planted alternating paths) | as above, unordered pairs: 362733 pairs with `c >= 3`, 1322471 ears, 124258 pairs of the open case (8588 yes; longest witness 3: 6997, 5: 1487, 7: 104), 87263 pairs for Theorem 1 | 0 |
| `run_random.py 3 3 20000`, `results-random-3-3.txt` | 18837 graphs of "`d <= 2` or `c <= 3`" (14714 in DC), 9-16 vertices, with degree-3 connectors | as above; 146539 pairs with `d = 2`, `c >= 3`; 75283 pairs for Theorem 1 (8030 yes) | 0 |
| `run_ears.py 2 10000`, `results-ears.txt` | 9744 DC graphs with adversarial ears (K4 blobs, paths of length 5, triangles with tails, ears on ears, ears between `u` and `v`, `p = s`, pendant trees) | as above; 370857 ears (177931 with >= 2 vertices, 31585 with `p = s`), 205183 Lemma 1 pairs | 0 |
| `exhaustive_b.py 5`, `results-exhaustive-b.txt` | every preorder on `q <= 5` labelled elements with `u` least, `v` greatest (2, 4, 13, 74 for `q = 2..5`), every `R`: 13397 instances | both ZZ solvers agree; all 21 instances with `N <= 3` are no-instances; the 11641 P2 instances realised with `M = N + 1` and `M = 1`: `d = 2`, `c = N`, in DC, PIMC of `G(Π)` = ZZ answer (3198 yes) | 0 |
| `run_realise.py p2 2 4000`, `results-realise-p2.txt` | 4000 random P2 instances, `q = 4..8`, about half planted (1370 yes; zigzag lengths 3, 5, 7), `G(Π)` up to 251 vertices | simple graph, vertex count formula, `d = 2`, `c = N`, DC, the cut formula and "minimum cuts = down-sets" on all subsets of `Q`, PIMC of `G(Π)` by the prefix search = ZZ answer, and the pipeline of Theorem 13(a) applied to `G(Π)` recovers `Q`, the preorder and `R` exactly | 0 |
| `run_realise.py nop2 3 1500`, `results-realise-nop2.txt` | 1500 random instances without enforcing P2 | as above except DC; `G(Π) ∈ DC` iff the instance has P2 (1117 / 383) | 0 |
| `run_roundtrip.py 2 3000`, `results-roundtrip.txt` | 2057 random 2-edge-connected DC graphs, 13788 open-case pairs (1014 yes) | `G -> ZZ -> G(Π)` with `M = N + 1` and `M = 1` (up to 590 and 88 vertices): `d = 2`, `c = N`, DC, PIMC(`G(Π)`) = PIMC(`G`) | 0 |
| `sat_check.py 2 3000 40 8`, `results-sat.txt` | 3000 random CNF formulas, 1-4 variables, 1-8 clauses (1790 satisfiable) | partial order, `R ⊆ <`, all 588256 `u`-`v` paths enumerated for 2902 formulas (count `2^n Π|C_j|`, stated form, zigzag, only conflict relations violate consistency), ZZ = SAT, P2 fails in all; 40 one-variable formulas realised (up to 123 vertices): PIMC = SAT | 0 |
| `crosscheck.py 5 300`, `results-crosscheck.txt` | 995 connected graphs with <= 7 vertices and 300 random DC graphs with 9-12 vertices, 34220 pairs | own `cp` (0-1-BFS formula) vs `checks/mcp.py` `cp_brute`; own DC test vs `mcp.in_dc`; own PIMC vs `cp == c` | 0 |

## 7. Additional facts found while checking (proved here)

**Fact 1 (the realisation is in DC exactly under P2).** For every ZZ instance with `N >= 3`, `G(Π)` of Theorem 13(b)
is in DC iff the instance satisfies P2.
*Proof.* "If" is Theorem 13(b). Conversely let `x, y` be incomparable; both are middle elements (`u < x < v`). Three
edge-disjoint `x`-`u` paths: the edge or ear vertex of the pair `u < x`; the ear `u x` added for the pair `x < v`; the
edge or ear of the pair `x < v` followed by the ear vertex of the pair `u < v` (`uv ∉ R`). So `c(x,u) >= 3`, likewise
`c(y,u) >= 3`, hence `c(x,y) >= 3`, and DC gives `d(x,y) <= 2`. `R` joins comparable elements only and every ear
vertex is adjacent to a comparable pair, so `x, y` are not adjacent and a common neighbour is a common real neighbour;
it lies above both or below both by the argument of Corollary 12. ∎ (Checked: 1117 / 383 instances.)

**Fact 2 (13(b) is a section of 13(a); checked, proof sketch).** On all 5500 realised instances the pipeline of
Theorem 13(a) applied to `G(Π)` returned `Q`, the preorder and `R` unchanged. Sketch: middle elements have
`c(x,u) >= 3` (Fact 1); the minimum cuts are the down-sets avoiding `v`, and these determine the preorder
(`↓y` is such a down-set for `y` not equivalent to `v`). Elements equivalent to `u` or `v` were not treated in general.

**Fact 3.** `M = 1` suffices in Theorem 13(b) (§4); checked on 11641 + 13788 instances.

## 8. Wording slips (no effect on the results)

- theory-dc.md Theorem 13(b): "comparable pairs carry an ear" — pairs in `R` carry an edge, the others an ear.
- theory-dc.md Theorem 13(b): "every cut `δ(A)` ... has `|δ(A)| = N + 2 #...`" refers to the weighted graph `W` on `Q`.
- theory-dc.md Problem Π: "correspond as in Lemma 4(4)" — replace by the argument of §2.
- dc-hardness.md Theorem 1: "decided by inspection" — they are all no-instances (§4).

Live findings log: three bullets posted on 2026-10-12 (§0 summary, Theorem 13(b) and Fact 1, scope of dc-hardness Theorem 1).
