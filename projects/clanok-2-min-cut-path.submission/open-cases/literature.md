# Open case of DC (d(u,v) = 2, c(u,v) >= 3): literature, agent "literature", 2026-10-12

Reading status of a row: **read** = text of the page or paper opened today (the part is named); **abstract** = abstract page only;
**record** = bibliographic record only; **via X** = known only through another source that was opened.
Statement numbers are those of the version read (named in the row); they are not compared with the journal text.
Our own remarks and checks are in Section 3 and are marked "ours"; nothing in Sections 1 and 2 is ours.

## 0. Result in brief

1. **No source found** that studies Min Cut-Path, "a minimum cut that contains a path", or an equivalent (searches 2-8, 11, 13 and 14 in Section 4,
   and the logs of 2026-10-10 and 2026-10-12 in `knowledge/literature/searches.md`). The open case has no answer in the literature.
2. **The nearest known problem class is "path avoiding forbidden pairs" (PAFP) and "path with a conflict graph".** Section 3 (D1-D3, ours,
   proved and checked) shows that "some minimum u-v cut contains a u-v path" is exactly "there is a u-v path in the graph of cut edges whose
   edges form an antichain of a partial order defined by the residual digraph". General PAFP and path-with-conflicts problems are NP-hard;
   the polynomial cases in print (Kolman-Pangrac, Kovac) are about directed paths in a DAG with pairs placed by the order. No source treats
   conflicts that come from a partial order, and none treats an undirected zigzag path.
3. **O2 (ears) is citable in part.** The auxiliary-graph statement of Dinitz 1992, as restated in Georgiadis-Italiano-Kosinas 2021
   (Section 4.1) and Tsin 2024 (Theorem 1.1), replaces every ear with two distinct attachment vertices by one virtual edge and preserves the
   3-edge-connected classes (and, per Georgiadis et al., the 4-edge-connected classes). Mehlhorn et al., Lemma 11, gives the cactus of the
   2-cuts. The claim "an ear acts like one edge for every minimum u-v cut and every c(u,v)" is in no source; it needs our own proof.
4. **Diameter two.** Payne-Por-Valtr-Wood, Theorem 2, gives min{deg u, deg v} edge-disjoint u-v paths of length at most 4 in every graph of
   diameter 2; Proposition 5 (with Bickle-Schwenk, corrected Theorem 2) describes the non-trivial global minimum cuts: one side is a clique K_delta
   and every vertex of it has exactly one cut edge. Consequence (ours, checked on 4402 graphs): no global minimum cut of a diameter-2 graph
   contains a path with three edges. This is a counting technique for O1/O4, not a statement about DC.
5. **Diameter three.** Le-Le (clique blow-up, one connector per pair of cliques) and Bazgan et al. (n^2 parallel 2-paths per edge, vertex
   set turned into a clique) are the two recipes. Neither carries over to minimum cuts unchanged (Section 3, D6).

## 1. Sources

### 1.1 Structure of minimum cuts, constrained minimum cuts (O6, O1; tasks 1, 2)

| ID | Source | Read | What it states | Relevance |
|---|---|---|---|---|
| L1 | Picard, Queyranne, *On the structure of all minimum cuts in a network and applications*, Math. Programming Study 13 (1980) 8-16; report EP-79-R-15, Ecole Polytechnique de Montreal, 1979: <https://publications.polymtl.ca/5993/1/EP-R-79-15_Picard.pdf> | read: Section 2, Section 3 (OCR text of the report) | Theorem 1: for a maximum flow `f` and the relation `i R j` iff (`(i,j)` arc with `f_ij < c_ij`) or (`(j,i)` arc with `f_ji > 0`), a cut separating `s` from `t` is minimum iff its source side is a closure of `R` containing `s` and not `t`. Proposition 2: closures are closed under union and intersection. Corollary 3: so are minimum cuts. Corollary 6: a saturated arc is in some minimum cut iff its ends lie in different (strong) components of `R` | O6 is Theorem 1; proofs of D1-D4. Note `knowledge/literature/PicardQueyranne1980.md` |
| L2 | Streit, Garg, *Constrained cuts, flows, and lattice-linearity*, arXiv 2512.18141v1 (2025-12-19): <https://arxiv.org/abs/2512.18141> | abstract; HTML text through a page extract (not the full text) | The minimum cuts form a distributive lattice (Section IV, "known", credited to Picard-Queyranne and Queyranne 1998). Theorem V.1: deciding whether some minimum cut satisfies an arbitrary predicate `B` is NP-complete (from SAT; no path, connectivity or conflict structure in the proof). Constraints that are lattice-linear (regular predicates) have fast parallel algorithms after one max-flow | "Path in a minimum cut" is, for a fixed path, a conjunction of closure conditions (D1), hence easy; the difficulty is choosing the path. Generic hardness gives no hint for DC |
| L3 | de Berg, Lopez Martinez, Spieksma, *Finding diverse minimum s-t cuts*, arXiv 2303.07290v3: <https://arxiv.org/abs/2303.07290> | abstract | k diverse minimum cuts: strongly polynomial for sum of Hamming distances and for the size of the union (submodular minimization); NP-hard for the minimum pairwise distance, k = 3 | Marginal: optimization over the family of minimum cuts; no path structure |
| L4 | Bentert et al., network diversion (minimal cut containing a given edge) | via note `knowledge/literature/Bentert2025NetworkDiversion.md`, not reopened | open on undirected graphs, polynomial on planar | the nearest "cut containing a prescribed edge" problem; asks for a minimal, not a minimum, cut |

### 1.2 Paths with forbidden pairs and conflicts (task 2)

| ID | Source | Read | What it states | Relevance |
|---|---|---|---|---|
| L5 | Kolman, Pangrac, *On the complexity of paths avoiding forbidden pairs*, Discrete Appl. Math. 157(13) (2009) 2871-2876, DOI 10.1016/j.dam.2009.03.018 (record read). Text: KAM series preprint <https://kam.mff.cuni.cz/kamserie/clanky/2008/s888.pdf> | read: abstract, Sections 1-2, statements of Observation 2.1, Theorems 3.2 and 4.3, end of Section 4 (proofs not read) | PAFP: directed acyclic graph, terminals `s`, `t`, set `F` of pairs, find an `s`-`t` path with at most one vertex of each pair; the order is reachability in `G` (the pairs are oriented so that the first vertex reaches the second; the order symbols were lost in the text extraction, so strictness is not checked). NP-complete if the pairs have the *halving structure* (no two pairs `(u,v)`, `(x,y)` with `v` before `x` or `v = x`) (Theorem 3.2); polynomial, `O(n^3)`, if the pairs have the *hierarchical structure* (no two pairs with `u`, `x`, `v`, `y` in this order) (Theorem 4.3); NP-complete even if `G` and `(V,F)` are planar (Observation 2.1); the algorithm also gives shortest and k shortest paths | closest classification in which the pairs are defined by the reachability order. Not applicable as it stands: directed paths in a DAG only |
| L6 | Kovac, *Complexity of the path avoiding forbidden pairs problem revisited*, Discrete Appl. Math. 161(10-11) (2013) 1506-1512, DOI 10.1016/j.dam.2012.12.022 (record read); arXiv 1111.3996v3 <https://arxiv.org/abs/1111.3996> | read: abstract, Sections 1-2, Table 1, statements of Theorems 1-4 | topological order of a DAG; two pairs are disjoint, nested or halving. NP-hard in general (Gabow et al.) and when all pairs overlap (Theorem 1); NP-hard when no two pairs are nested (Theorem 2); `O(n^3)` when no two are halving (Theorem 3), improved to `O(M(n))`, `M(n)` = time of boolean matrix multiplication (abstract, Table 1) | same as L5; positional rather than reachability structure |
| L7 | Yinnone, *On paths avoiding forbidden pairs of vertices in a graph*, Discrete Appl. Math. 74(1) (1997) 85-92, DOI 10.1016/S0166-218X(96)00017-0 | record read; statement via L5 (Section 1) and L6 (Section 1.2) | skew-symmetry condition (pairs `{u,u'}`, `{v,v'}` and an edge `u -> v` imply an edge `v' -> u'`): polynomial, equivalent to finding an augmenting path for a matching | pairs must be disjoint; our conflicts are not of this form (ours, D2). Not opened |
| L8 | Gabow, Maheshwari, Osterweil, *On two problems in the generation of program test paths*, IEEE Trans. Software Eng. SE-2(3) (1976) 227-231 | via L5 (reference list, Section 1) and L6 (Section 1.1) | PAFP is NP-complete, already for directed acyclic graphs | origin of the problem. Not opened |
| L9 | Darmann, Pferschy, Schauer, Woeginger, *Paths, trees and matchings under disjunctive constraints*, Discrete Appl. Math. 159(16) (2011) 1726-1735, DOI 10.1016/j.dam.2010.12.016 (record read). Text: preprint <https://optimization-online.org/wp-content/uploads/2009/10/2422.pdf> | read: abstract, Section 1, list of theorems | conflict graph on the edges of `G`; shortest path with a conflict graph is NPO PB-complete even if the conflict graph is a matching ("2-ladder"), a result of Kann 1994 quoted in Section 1, not proved there; shortest path with a *forcing* graph is APX-hard even for a 2-ladder (Theorems 14, 15); spanning tree with 3-ladder conflicts strongly NP-hard (Theorem 1) | path with conflicts on edges: hard for arbitrary conflict graphs; ours is a comparability graph of a poset (D2). Kann 1994 not opened |
| L10 | German, *Layer-based width for PAFP*, arXiv 2605.12457 (IWOCA 2026 per the listing): <https://arxiv.org/abs/2605.12457> | abstract | PAFP is FPT in the BFS-width of the union digraph plus the number of backward arcs; NP-complete even if the union digraph is a DAG of width 2; polynomial for DAGs of exact-length width at most 2 (2-SAT) | parameter route; weak |
| L11 | Bellitto, Li, Okrasa, Pilipczuk, Sorge, *The complexity of connectivity problems in forbidden-transition graphs and edge-colored graphs*, arXiv 2009.12892: <https://arxiv.org/abs/2009.12892> | abstract | simple path compatible with forbidden transitions at vertices: W[1]-hard for the distance to a linear forest | local (adjacent-edge) conflicts only; the alternation of the path in O6 is a local condition of this kind (ours, D2) |
| L12 | Bachtler, Bergner, Krumke, *Almost disjoint paths and separating by forbidden pairs*, arXiv 2202.10090: <https://arxiv.org/abs/2202.10090> | abstract | separating `s` from `t` by pairs of arcs is Sigma_2^P-complete on DAGs | not a cut problem; weak |
| L13 | Kalyanasundaram, Kumar, *Conflict-free cuts in planar and 3-degenerate graphs with 1-regular conflicts*, arXiv 2605.12068: <https://arxiv.org/abs/2605.12068> | abstract | a cut whose edges are pairwise non-conflicting; NP-complete for planar graphs of maximum degree 5 | pairwise compatibility of the edges of one cut, the same flavour as D1; no path |

### 1.3 3-edge-connected classes, 2-cuts, ears, Gomory-Hu trees (task 3; O1, O2)

| ID | Source | Read | What it states | Relevance |
|---|---|---|---|---|
| L14 | Georgiadis, Italiano, Kosinas, *Computing the 4-edge-connected components of a graph in linear time*, ESA 2021 (venue per Tsin's reference list), arXiv 2105.02910v1: <https://arxiv.org/abs/2105.02910> | read: abstract, Section 1, intro of Section 3, Section 4.1, reference list | Section 1: `u`, `v` are `k`-edge-connected iff no `(k-1)`-cut separates them, iff `k` edge-disjoint paths join them (Menger); a `k`-edge-connected component is a maximal vertex set of pairwise `k`-edge-connected vertices. Section 4.1: for a 2-edge-connected component `H`, shrinking its 3-edge-connected components `C_i` gives a quotient `Q` that is a tree of cycles (credited to Dinitz 1992); if two edges `(C_i,C_j)`, `(C_i,C_k)` of one cycle correspond to edges `(x,y)`, `(x',y')` of `G` with `x != x'` in `C_i`, add a virtual edge `(x,x')` to `G[C_i]`; the result `C_i'` is 3-edge-connected and its 4-edge-connected components are exactly those of `G` inside `C_i`. Section 3: the number of 3-cuts of a 3-edge-connected graph is `O(n)` (well known, from the cactus) | O2: an ear of `Q` is the union of the other nodes of one cycle through `C_i`; its boundary is the two cycle edges at `C_i`; the virtual edge replaces it. Holds for 3- and 4-edge-connectivity only |
| L15 | Tsin, *A simple linear-time algorithm for generating auxiliary 3-edge-connected subgraphs*, arXiv 2309.13827v2 (2024-08-12): <https://arxiv.org/abs/2309.13827> | read: abstract, Section 1 (venue not seen) | Theorem 1.1 (based on Dinitz 1992): for each 3-edge-connected component replace every 2-cut `{(v,w),(v',w')}` with `v != v'` in the component by a new edge `(v,v')`; then `x`, `y` are 3-edge-connected in the new graph iff they are in `G`. The component with these auxiliary edges is the auxiliary 3-edge-connected subgraph | the citable statement for O2 on the 3-edge-connected classes `Q` |
| L16 | Mehlhorn, Neumann, Schmidt, *Certifying 3-edge-connectivity*, Algorithmica 77(2) (2017) 309-335, DOI 10.1007/s00453-015-0075-x; arXiv 1211.6553v3 <https://arxiv.org/abs/1211.6553> | read: Section 10 (p. 16) | Lemma 11 (credited to Nagamochi-Ibaraki 2008, Section 2.3.5): for a 2-edge-connected graph that is not 3-edge-connected, contracting the 3-edge-connected components gives a cactus representation of the 2-cuts; edges of the cactus correspond one-to-one to the edges that lie in a 2-cut; blobs are the components | structure of the 2-cuts (the cycles of O2). Note `Mehlhorn2017Certifying.md` |
| L17 | Abboud, Krauthgamer, Li, Panigrahi, Saranurak, Trabelsi, *Breaking the cubic barrier for all-pairs max-flow: Gomory-Hu tree in nearly quadratic time*, arXiv 2111.04958v3 (2022-08-03): <https://arxiv.org/abs/2111.04958> | read: abstract, Section 1 | Theorem 1.2 (Gomory-Hu 1961, as restated): every undirected edge-weighted graph has a cut tree: a tree `T` on `V` such that for all `s`, `t` the `(s,t)` minimum cut of `T` is an `(s,t)` minimum cut of `G` of the same value; computable with `n-1` max-flow calls | a citable form of "the 3-edge-connected classes are the components of the Gomory-Hu tree restricted to edges of weight at least 3" (that restriction is ours, immediate). Gomory-Hu 1961 not opened |
| L18 | Nagamochi, Kameda, *Constructing cactus representation for all minimum cuts in an undirected network*, J. Oper. Res. Soc. Japan 39(2) (1996) 135-158 | via note `NagamochiKameda1996.md` (read 2026-10-12, not reopened) | Lemma 3.4: the minimum cuts that separate the ends of an edge of weight lambda(N) are nested | for adjacent `u`, `v` the structure is a chain; not needed for d(u,v) = 2 |

Not opened: Dinitz, *The 3-edge-components and a structural description of all 3-edge-cuts in a graph*, Graph-Theoretic Concepts in Computer Science (WG '92), LNCS, pp. 145-157, DOI 10.1007/3-540-56402-0_44 (Crossref record read; Crossref gives the year 1993) (the source of L14 Section 4.1 and L15 Theorem 1.1, per Tsin's reference [1]); Dinitz-Karzanov-Lomonosov 1976; Nagamochi-Ibaraki, *Algorithmic Aspects of Graph Connectivity*, 2008; Gomory-Hu 1961; Galil-Italiano 1991.

### 1.4 Diameter-three hardness techniques (task 4)

| ID | Source | Read | What it states | Relevance |
|---|---|---|---|---|
| L19 | Le, Le, *A complexity dichotomy for matching cut in (bipartite) graphs of fixed diameter*, Theor. Comput. Sci. 770 (2019) 69-78; arXiv 1804.11102v2 <https://arxiv.org/abs/1804.11102> | read: Sections 1-2 (construction, Lemmas 1-3, Theorem 1), statements of Theorems 2, 3 | Section 2: from `G` on `v_1..v_n` build `G'`: each `v_i` gets a clique `Q_i` of `n` new vertices all joined to `v_i`, and `q_ij`, `q_ji` are joined for all `i != j`. Properties: `N(v_i)` gains `V(Q_i)`; each `q` has at most one neighbour outside `V(Q_i) + v_i`. Lemma 1: diameter 3. Lemma 2: `G'` has a matching cut iff `G` has. Lemma 3 and Theorem 1: NP-complete for every fixed diameter `d >= 3` (a chain of `K_{2,2}` raises the diameter); Theorem 2: bipartite, `d >= 4`; Theorem 3: bipartite diameter 3 polynomial | generic trick 1: blow every vertex up into a clique that no cut can split, add one connector per pair of cliques |
| L20 | Bazgan, Fluschnik, Nichterlein, Niedermeier, Stahlberg, *A more fine-grained complexity analysis of finding the most vital edges for undirected shortest paths*, Networks 73(1) (2019) 23-37; arXiv 1804.09155v1 <https://arxiv.org/abs/1804.09155> | read: Theorem 4, Theorem 5, Proposition 1 and their proofs | Theorem 4: NP-hard on split graphs (unit lengths), so on diameter 3: subdivide every edge of `G` by `n^2` parallel 2-paths (new vertices `w^j_{uv}`), make `V(G)` a clique, budget `k' = C(n,2) + k n^2`, length bound `2 l`. Theorem 5: NP-hard on complete graphs for arbitrary lengths (edges of the complement get length `l + 1`). Proposition 1: linear time on diameter at most 2; the proof uses L23 (Theorem 2) and, for `l <= 4`, a polynomial result of Itai et al. | generic trick 2: heavy edges as parallel 2-paths, clique on the original vertices. Proposition 1 is an application of the diameter-two path result of L23 to a cut-type problem |
| L21 | Bouquet, Picouleau, *The complexity of the perfect matching-cut problem*, arXiv 2011.03318v2: <https://arxiv.org/abs/2011.03318> | abstract | NP-complete for diameter 3 and for bipartite diameter 4; polynomial for diameter 2 and for bipartite diameter 3 | another cut problem with the same boundary (diameter 2 / 3) |
| L22 | Lucke, Paulusma, Ries, *Dichotomies for maximum matching cut: H-freeness, bounded diameter, bounded radius*, arXiv 2304.01099v6: <https://arxiv.org/abs/2304.01099> | abstract | complete dichotomies for bounded diameter; the thresholds are not in the abstract | not read further |

Earlier notes: `LeLe2019MatchingCut.md`, `Bazgan2019MostVital.md`, `Baier2010LengthBounded.md` (length-bounded cuts, Theorem 3.11 of the manuscript).

### 1.5 Diameter two and local edge-connectivity (task 5; O1, O4)

| ID | Source | Read | What it states | Relevance |
|---|---|---|---|---|
| L23 | Payne, Por, Valtr, Wood, *On the connectivity of visibility graphs*, Discrete Comput. Geom. 48(3) (2012) 669-681, DOI 10.1007/s00454-012-9446-0 (record read); arXiv 1106.3622v1 <https://arxiv.org/abs/1106.3622> | read: Section 2 in full (Theorems 2, 4, Proposition 5, Theorem 6 up to its proof) | Theorem 2: in a graph of diameter 2, for distinct `v`, `w` and `d = min{deg v, deg w}` there are `d` edge-disjoint `v`-`w` paths of length at most 4 (constructive proof: common neighbours, a maximal matching between leftover neighbours, a common neighbour for each remaining pair). Proposition 5: a graph of diameter at most 2 and minimum degree `delta >= 2` has a non-trivial edge cut of size `delta` iff `V = A + B + C` with `G[A] = K_delta`, `|B + C| >= delta`, every vertex of `A` has exactly one neighbour in `B` and none in `C`, every vertex of `B` has a neighbour in `A`, and `B` is completely joined to `C`. Its proof counts: a vertex of the side `X` has at least `delta - (|X| - 1)` cut edges. Theorem 6: in non-collinear visibility graphs every minimum cut is a vertex star. The paper credits Plesnik (1975) for lambda = delta | O1/O4: counting technique; D5 |
| L24 | Bickle, Schwenk, *Minimum edge cuts in diameter 2 graphs*, Discuss. Math. Graph Theory 39(3) (2019) 605-608, DOI 10.7151/dmgt.2097; *Corrigendum*, same journal 45 (2025) 411-414, DOI 10.7151/dmgt.2517 | corrigendum: read in full; original: first page and references only (abstract: streamlined proof of Plesnik's theorem, characterization of the diameter-2 graphs with a non-trivial minimum edge cut) | the original Theorem 3 and Corollaries 4, 5 were wrong (an inequality was taken as equality). Corrected: Corollary 1 (credited to Chartrand-Lesniak, textbook): in a diameter-2 graph one side of a minimum cut is `K_1` or `K_delta`. Theorem 2: a graph has diameter 2 and a non-trivial minimum edge cut iff it is `K_n x K_2` (`n >= 4`) or has the partition `S_1, S_2, S_3` of L23 (`S_1 = K_d`, `d` cut edges, each vertex of `S_1 + S_2` on one of them, `S_2`-`S_3` complete). Theorem 4: there is a single non-trivial minimum cut except for `C_4` and one explicit family | independent second source for L23, Proposition 5. Use the corrigendum, not the 2019 note |
| L25 | Stuart, *The eavesdropping number of a graph*, Czechoslovak Math. J. 59(3) (2009) 623-636 | via note `Stuart2009Eavesdropping.md` | Theorem 11: lambda(u,v) = min{deg u, deg v} for diameter at most 2, credited to Fricke, Oellermann, Swart (unpublished) | c(u,v) in diameter 2; already in article 1 |
| L26 | Plesnik, *Critical graphs of given diameter*, Acta Fac. Rerum Natur. Univ. Comenian. Math. 30 (1975) 71-93 | via L23 (Section 2) and L24 (abstract, references) | edge-connectivity equals minimum degree in diameter 2 | global form. Not opened |

Not opened or not reachable: Hellwig-Volkmann, *Maximally edge-connected and vertex-connected graphs and digraphs: a survey*, Discrete Math. 308 (2008) 3265-3296 (record only, seen in a search summary); Fricke-Oellermann-Swart manuscript.

## 2. What the literature does and does not give for each observation

| Obs. | Status in the literature |
|---|---|
| O1 | no source; the 3-edge-connected class `Q` is defined in L14, L15, L17; "vertices of `Q` are pairwise at distance at most 2" is the definition of DC |
| O2 | partly: L14 Section 4.1 and L15 Theorem 1.1 (virtual edges for ears, preserve 3- and 4-edge-connectivity), L16 Lemma 11 (cactus of the 2-cuts). Not covered: preservation of minimum `u`-`v` cuts and of distances (a one-vertex ear is a 2-path) for arbitrary `c(u,v)` |
| O3 | no source; a consequence of L1 Theorem 1 (D4); checked |
| O4 | no source; nothing on the length of a path inside a minimum cut |
| O5 | no source |
| O6 | L1 Theorem 1; the alternation is our remark (D4); checked |

## 3. Derived here (ours); proofs and tests

Setting for D1-D4: `G` finite simple connected, `u != v`, `c = c(u,v)`, `f` a maximum `u`-`v` flow in the symmetric digraph of `G`
(arcs `xy`, `yx`, capacity 1 each), `R` its residual relation as in L1, `cl(X)` the set of vertices reachable from `X` in `R` (the smallest `R`-closed
set containing `X`). By L1, Theorem 1, the minimum cuts are the `delta(A)` with `A` closed, `u in A`, `v not in A`. A union of closed sets is closed.

**D1 (Helly property of minimum cuts; ours, proved, checked).**
*Statement.* For a set `S` of edges: `S` lies in some minimum `u`-`v` cut iff every `{e, e'}` with `e, e' in S` (also `e = e'`) lies in some minimum cut.
*Proof.* (i) If `e = xy` lies in `delta(A)`, `A` closed, `x in A`, `y not in A`, then `f_xy = 1` (else `x R y`) and `f_yx = 0` (else `x R y` by the second clause).
So `e` carries one unit from `x` to `y`; call `t(e) = x` the tail and `h(e) = y` the head. The orientation depends on `f` only, not on `A`.
(ii) Let `S` consist of oriented edges and `A_S = cl({u} + {t(e) : e in S}) = cl(u) + the union of cl(t(e)), e in S`. If `S` lies in `delta(A)` for a minimum cut `A`,
then `A` contains `u` and all tails, so `A` contains `A_S` (as `A` is closed), and `A` contains no head and not `v`, so `A_S` contains none of them. Conversely, if `A_S` contains no head and not `v`, it is closed,
contains `u` and not `v`, hence a minimum cut, and every `e in S` has `t(e) in A_S`, `h(e) not in A_S`, so `S` lies in `delta(A_S)`.
(iii) Therefore `S` lies in a minimum cut iff all edges of `S` are oriented and, for all `e, e'` in `S`, `h(e)` and `v` are not in `cl(u) + cl(t(e'))`. Each condition involves at most the pair `(e, e')`; the same
characterization applied to `{e, e'}` shows that it is the conjunction of the pair conditions (e,e), (e,e'), (e',e), (e',e'). Hence the joint condition equals the pairwise one. QED
*Tests.* (T1a) all connected graphs with 3..7 vertices (994), all vertex pairs, all simple `u`-`v` paths: 358,567 triples, 10,728 with the path inside a minimum cut; "path inside a minimum cut" = "all pairs of its edges inside a common minimum cut" in every case.
(T1b) connected graphs with 3..6 vertices (141), all pairs, all edge subsets of size at most 5 of the union of the minimum cuts: 62,124 subsets, 17,585 inside a common minimum cut; no exception. Brute force: all minimum cuts by vertex sets (`mcp.min_cuts_by_sets`).

**D2 (partial order of the cut edges; ours, proved, checked).**
Let `F` be the set of edges that lie in some minimum `u`-`v` cut. For `e, e'` in `F` write `e < e'` iff `t(e')` reaches `h(e)` in `R` (`t(e') R* h(e)`).
*Statement.* (a) `<` is a strict partial order on `F`. (b) Two edges of `F` lie in a common minimum cut iff they are incomparable. (c) Hence a set of edges lies in a minimum cut iff it is an antichain of `(F, <)` (by D1). (d) The edges of one flow path of an acyclic maximum flow form a chain (an edge before another on the path is smaller), so every antichain has at most `c` edges and meets each of the `c` flow paths at most once; a minimum cut is an antichain of size `c`.
*Proof.* Transitivity: `e < e'`, `e' < e''` give `t(e'') R* h(e')`, and `h(e') R t(e')` (the only residual arc of a flow edge points from head to tail), so `t(e'') R* h(e')  R t(e') R* h(e)`. Irreflexivity: `t(e) R* h(e)` would put `h(e)` into every closed set that contains `t(e)`, so `e` would lie in no minimum cut. (b) is the pair case of D1 (ii)-(iii): `h(e)` not in `cl(t(e'))` and `h(e')` not in `cl(t(e))`. (d): along a flow path `t(e') R* h(e)` follows by walking backwards. QED
*Tests.* (T3) all connected graphs with 3..8 vertices (12,111 graphs, 331,121 vertex pairs): edge in some minimum cut iff oriented, `h(e)` and `v` outside `cl(u) + cl(t(e))` (4,702,482 edge checks); `<` irreflexive, transitive, antisymmetric; common minimum cut iff incomparable (4,101,139 edge pairs); maximum flow by `networkx.maximum_flow`; no exception.

**D3 (reformulation; ours).** `cp(u,v) = c(u,v)` iff `(V,F)` contains a `u`-`v` path whose edge set is an antichain of `(F, <)`. (A cut-path of size `c` is a minimum cut that contains a path; D1, D2.) Equivalently a `u`-`v` *walk* with pairwise incomparable edges, since the edges of a path inside a walk form a subset of an antichain. The length of the path is odd and at most `c`; its edges lie on distinct flow paths.
Reading: a path-with-conflicts problem on `(V,F)`, conflict graph = comparability graph of a poset of width `c`; the local part of the conflict (two path edges sharing a vertex must be both heads or both tails there) is the alternation of O6. L9: for arbitrary conflict graphs NPO PB-complete (hard already for a matching); L5-L6: the polynomial PAFP cases need the pairs placed by a DAG order, and are for directed paths. A path in an undirected graph with conflicts from a poset is covered by none of them (search 9, 12: nothing).

*Data on lengths (T5; checked only).* A path of length `l` inside a minimum cut needs `c(u,v) >= l` (antichain of size `l`), so `l = 5` needs `c >= 5`. Exhaustive over all connected graphs with 3..8 vertices and all pairs (any distance, any `c`): the lengths of `u`-`v` paths inside a minimum `u`-`v` cut are 1 or 3 only. Number of (graph, pair) with such a path: length 1, `d = 1`: 170,883; length 3: 702 with `d = 1`, 400 with `d = 2`, 3 with `d >= 3`; no path of length 5 or more in any graph with at most 8 vertices. The 400 pairs with `d = 2` agree with `results-open-cases.txt` of the lead. The data up to 8 vertices are consistent with both forms of O4 but contain no path of length 5, so they say nothing about longer paths.

**D4 (O6 and O3; ours, proved, checked).** O6: a `u`-`v` path `x_0 = u, ..., x_k = v` lies in a minimum cut iff `k` is odd and `cl(even-indexed vertices)` contains no odd-indexed vertex. Proof: if the path lies in `delta(A)`, `u in A`, the vertices alternate sides, so even ones are in `A`, odd ones outside (so `k` odd as `v` is outside), and `A` contains `cl(evens)`. Conversely `A = cl(evens)` is closed, contains `u`, avoids the odd vertices and so `v`; by L1 it is a minimum cut, and every path edge has one end in `A`. O3 (path `u a b v`): the sets `{u, b}` and `{a, v}` are the even and odd vertices; a minimum cut between the two sets has size at least `c` (it is a `u`-`v` cut), with equality iff some minimum `u`-`v` cut separates them, which is O6. QED
*Tests.* (T4) all connected graphs with 3..7 vertices: O6 criterion (flow `networkx.maximum_flow`, closure of the even vertices) against brute force on 358,567 paths (10,728 positive); O3 (minimum cut between the vertex sets with a super source and sink of infinite capacity) against brute force on 59,678 paths with three edges (65 positive). No exception.

**D5 (diameter two; ours, from L23; checked).** In a graph of diameter at most 2 and minimum degree at least 2, every minimum global cut contains no path with three edges. Proof from L23, Proposition 5: a trivial minimum cut is a star; a non-trivial one is `delta(A)` with `G[A] = K_delta` and each vertex of `A` incident to exactly one cut edge, so a path `a_1 b_1 a_2 b_2` would give `a_2` two cut edges. QED
*Tests.* (T2) all connected graphs with 4..8 vertices, diameter at most 2, minimum degree at least 2: 4402 graphs. lambda = delta in all (Plesnik); 92 have a non-trivial minimum cut, and the existence of the partition of Proposition 5 is equivalent to the existence of a non-trivial minimum cut in all 4402; no minimum cut contains a path with three edges.
Scope: this is the *global* minimum cut; for a pair `u`, `v` with `c(u,v) > delta` the minimum `u`-`v` cuts are not covered. For diameter 2 and `d(u,v) = 2` no minimum `u`-`v` cut contains a path at all (`cp = c + 1`, article 1, Theorem 5.5). The technique of L23, Proposition 5 (a vertex of a side `X` has at least `delta - (|X| - 1)` cut edges) needs a degree lower bound for the vertices on the path; in DC only `c(x,u) >= 3` is known for them (O1).

**D6 (diameter-three recipes; ours, unverified).** L19 works because a matching cut cannot split a clique and the connectors do not change which edge sets are matchings. For a minimum cut the connectors between `n` cliques add `|A||B|`-type terms to every cut, so `c(u,v)` and the family of minimum cuts change. L20 deletes all clique edges inside its budget `C(n,2)` and makes the original edges expensive by `n^2` parallel 2-paths. A hardness proof for Min Cut-Path on diameter 3 would have to control `c(u,v)` and `cp(u,v)` in the presence of the clique; neither source does this.

**D7 (local conflicts are easy; ours, sketch).** If only the alternation of O6 is required, the question is the existence of a `u`-`v` path of odd length in `(V,F)` oriented alternately: a path in the bipartite double cover, linear time. All difficulty is in the non-adjacent pairs of D2.

## 4. Searches

All dates 2026-10-12. "WS" = WebSearch tool (standard mode). Queries as entered.

| # | Query | Engine | Outcome |
|---|---|---|---|
| 1 | *paths avoiding forbidden pairs of vertices Gabow Maheshwari Osterweil Yinnone Kolman Pangrac complexity polynomial special cases* | WS | L5, L6 (arXiv 1111.3996, KAM preprint); Gabow, Yinnone not returned |
| 2 | *minimum s-t cut whose edges contain an s-t path, "connected" minimum cut edge set induces connected subgraph, alternating path across cut* | WS | nothing on the problem; only "simple cut" (the side is connected) and unrelated hits (Bezakova, edge-induced vertex cuts, arXiv cs/0607109, not opened) |
| 3 | arXiv API `abs:"minimum cut" AND abs:"contains a path"` | export.arxiv.org | 0 |
| 4 | arXiv API `abs:"minimum cut" AND abs:"alternating path" AND abs:"edge-connectivity"` | export.arxiv.org | 0 |
| 5 | arXiv API `all:"minimum cut" AND all:"path inside" OR all:"path contained in a minimum cut" OR all:"connected minimum cut"` | export.arxiv.org | 0 |
| 6 | arXiv API `abs:"minimum cut" AND abs:"cut edges" AND abs:"form a path"` | export.arxiv.org | 0 |
| 7 | *"cut" "δ(S)" "connected as a subgraph" OR "induces a connected bipartite subgraph" OR "cut-set is connected" minimum edge cut separating s and t both endpoints connected within the cut edges* | WS | nothing; "connected cut" literature concerns a connected side `G[S]`, not a connected cut subgraph |
| 8 | *minimum cuts "residual graph" closed sets "Picard Queyranne" path alternating directions edge-disjoint paths all minimum s-t cuts constrained selection problem* | WS | L1 (report), arXiv 2406.15129, 2512.00153 (strip graph, titles only); nothing on paths |
| 9 | *s-t path avoiding conflicting edge pairs conflict graph is comparability graph OR "transitive" OR "interval" OR "perfect" polynomial NP-hard path with conflicts* | WS | L5, Szeider-type transition results (L11); nothing on comparability conflict graphs |
| 10 | *Darmann Pferschy Schauer Woeginger "Paths, trees and matchings under disjunctive constraints" conflict graph path problem NP-hard special conflict graphs* | WS | L9 (preprint read); Pferschy-Schauer, maximum flow with disjunctive constraints (J. Comb. Optim., seen in a search summary only) |
| 11 | *minimum cut distributive lattice constrained problem NP-hard "min cut" with additional constraint connected OR path OR "forbidden pair" closed sets residual graph minimum s-t cut with side constraint complexity* | WS | L2, L3; no connectivity or path constraint |
| 12 | *path in directed acyclic graph avoiding forbidden pairs defined by reachability "forbidden pairs" "transitive" OR "comparable" OR "partial order" polynomial algorithm hierarchical halving Kolman Pangrac follow-up* | WS | L5, L6, L10 (2026); no poset-conflict variant |
| 13 | *antichain edge set path in poset "zigzag" OR "fence" OR "alternating" path whose edges form an antichain in the edge poset of a DAG, minimum cuts maximal antichains flow* | WS | nothing on paths; arXiv 2410.00315 (Ghrist et al., lattice-valued bottleneck duality; abstract read, the claimed antichain-cut bijection is not in the abstract, not used) |
| 14 | *shortest path problem with precedence constraints OR "closure constraints" OR "implication constraints" vertex pairs "if vertex u is on the path then vertex v must be" NP-hard graph path with logical constraints* | WS | nothing close (precedence-constrained arborescences, Hamiltonian paths with partial orders: not opened) |
| 15 | *Georgiadis Italiano Kosinas "Computing the 4-edge-connected components of a graph in linear time" 3-edge-connected components cactus 2-edge cuts preliminaries* | WS | L14 |
| 16 | arXiv API `abs:"3-edge-connected components" AND abs:cactus` | export.arxiv.org | 4: Tsin 2309.13827 (L15), Tsin 2306.14103 and 2002.04727 (abstract lines only), Mehlhorn 1211.6553 (L16) |
| 17 | arXiv API `abs:"Gomory-Hu" AND abs:"edge connectivity" AND abs:"unweighted"` | export.arxiv.org | 2: 2110.15891, 2212.00359 (not opened) |
| 18 | *All-Pairs Max-Flow is no Harder than Single-Pair Max-Flow: Gomory-Hu Trees in Almost-Linear Time arXiv* | WS | FOCS 2023 paper (Abboud, Li, Panigrahi, Saranurak) has no arXiv id in the results; L17 used instead. A first guess of the arXiv id (2303.15724) opened an unrelated paper and was discarded |
| 19 | Crossref `works?query.bibliographic=` *Yinnone On paths avoiding forbidden pairs of vertices in a graph*; *Kovac Complexity of the path avoiding forbidden pairs problem revisited*; *Kolman Pangrac On the complexity of paths avoiding forbidden pairs* (HTTP 429, not repeated; its record was in the results of the first query); *Dinitz The 3-edge-components and a structural description of all 3-edge-cuts in a graph*; `works/10.1007/s00454-012-9446-0`; `works/10.1016/j.dam.2010.12.016` | api.crossref.org | records of L5-L7, L9, L23 and of Dinitz 1992 |
| 20 | *Payne visibility OR "visibility graphs" "local edge-connectivity" diameter two "min{deg" edge-disjoint paths Theorem 2 Fricke Oellermann Swart 2012* | WS | L23 |
| 21 | *Plesnik "Critical graphs of given diameter" Acta Fac. Rerum Natur. Univ. Comenian. Math. 30 1975 edge-connectivity equals minimum degree diameter 2* | WS | the 1975 paper itself not reachable; L24 found (DMGT 39, 2019) |
| 22 | *Hellwig Volkmann "Sufficient conditions for graphs to be lambda'-optimal, super-edge-connected, and maximally edge-connected" OR "maximally local-edge-connected graphs" diameter 2 local edge-connectivity min degree survey Discrete Mathematics 2008* | WS | survey record only (DOI 10.1016/j.disc.2007.06.035 per the search summary); text not reached |
| 23 | `dmgt.uz.zgora.pl/publish/article.php?doi=2097`, `.../pdf.php?doi=2517` | publisher site | L24 (corrigendum read in full) |
| 24 | *edge cut problem complexity "diameter two" polynomial "diameter three" NP-complete matching cut OR "disconnected cut" OR "stable cut" OR "d-cut" small diameter graphs* | WS | L19, L21, L22; d-cut paper (secondary summary only, not opened); nothing for disconnected or stable cut |
| 25 | pages `arxiv.org/abs/2303.07290`, `2605.12457`, `2410.00315`, `2512.18141`, `2605.12068`, `2009.12892`, `2202.10090`, `2304.01099`, `2011.03318` | arXiv abstract pages; HTML for 2512.18141 | L2, L3, L10-L13, L21, L22 (abstracts) |
| 26 | PDFs `arxiv.org/pdf/1111.3996`, `kam.mff.cuni.cz/.../s888.pdf`, `optimization-online.org/.../2422.pdf`, `arxiv.org/pdf/2105.02910`, `2309.13827`, `2111.04958`, `1106.3622`, `1804.11102`, `1804.09155`, `1211.6553v3`, `publications.polymtl.ca/5993/1/EP-R-79-15_Picard.pdf` | WebFetch; text extracted locally with `pdftotext` | full or partial text for L1, L5, L6, L9, L14-L17, L19, L20, L23 |

Not searched: Google Scholar, MathSciNet, DBLP (bot check on earlier attempts, see `searches.md`).

## 5. Not done, open points

- T4 (O6, O3) was run for n <= 7 only; a run for n = 8 was stopped as too slow (one max-flow per path with three edges). T1a is also n <= 7; T3 and T5 cover n <= 8.
- Not opened: Gabow et al. 1976, Yinnone 1997, Kann 1994 (all quoted through opened sources), Dinitz 1992, Gomory-Hu 1961, Plesnik 1975, Nagamochi-Ibaraki 2008, Szeider's dichotomy for forbidden transitions (named by a search summary only, not used).
- No `.bib` entry and no reading note were added (rule of this task). Candidates for notes if the text relies on them: Payne et al. 2012 (Theorem 2, Proposition 5), Bickle-Schwenk corrigendum 2025, Kolman-Pangrac 2009, Kovac 2013, Georgiadis et al. 2021, Tsin 2024.
- The literature does not say whether the order of D2 can make PAFP polynomial; that is a question for the theory agents (D3 gives the exact formulation).

## Appendix. Check scripts (ours)

Run from any directory with `python -I script.py <arg>`; they import `checks/mcp.py` read-only (`sys.path` insert). Written to the scratchpad of the session, reproduced here.

### check_lit.py (T1a, T1b, T2; arguments `t1a 7`, `t1b 6`, `t2 8`)

```python
"""Checks of the literature agent (open case of DC).  Imports the shared routines of checks/mcp.py read-only.

T1  Helly lemma: for a fixed pair (u,v), an edge set S lies in a common minimum u-v cut iff every two edges of S
    (also e = f) lie in a common minimum u-v cut.  Tested on (a) all u-v paths of all connected graphs with
    n <= 7 vertices, (b) all edge subsets of size <= 5 of the union of the minimum cuts, n <= 6.
T2  Payne-Por-Valtr-Wood, Proposition 5 (arXiv 1106.3622v1): a graph of diameter <= 2 and minimum degree d >= 2
    has a non-trivial edge cut of size d iff its vertices split into A, B, C with G[A] = K_d, |B u C| >= d,
    every vertex of A has exactly one neighbour in B and none in C, every vertex of B has a neighbour in A,
    and B is completely joined to C.  Tested on all connected graphs with n <= 8 vertices; also tests
    Plesnik's lambda = delta, and that no minimum global cut of such a graph contains a path with 3 edges.
"""
import itertools
import os
import sys

sys.path.insert(0, "C:/Users/norom/Documents/latex/projects/clanok-2-min-cut-path.submission/checks")
import mcp  # read-only import

CACHE = "C:/Users/norom/Documents/latex/tmp/clanok-2-checks"


def t1a(nmax):
    graphs = 0
    triples = 0
    paths_in_cut = 0
    for n in range(3, nmax + 1):
        for _, es in mcp.connected_graphs(n, CACHE):
            g = mcp.Gr(n, es)
            graphs += 1
            for u in range(n):
                for v in range(u + 1, n):
                    c, cuts = mcp.min_cuts_by_sets(g, u, v)
                    compat = {}
                    for e in range(g.m):
                        for f in range(e, g.m):
                            both = (1 << e) | (1 << f)
                            compat[(e, f)] = any((cm & both) == both for cm in cuts)
                    for vs, pe in mcp.simple_paths(g, u, v):
                        pm = 0
                        for e in pe:
                            pm |= 1 << e
                        joint = any((cm & pm) == pm for cm in cuts)
                        pair = all(compat[(min(e, f), max(e, f))] for e in pe for f in pe)
                        assert joint == pair, (n, es, u, v, pe)
                        triples += 1
                        paths_in_cut += joint
    return graphs, triples, paths_in_cut


def t1b(nmax, kmax=5):
    graphs = 0
    subsets = 0
    pos = 0
    for n in range(3, nmax + 1):
        for _, es in mcp.connected_graphs(n, CACHE):
            g = mcp.Gr(n, es)
            graphs += 1
            for u in range(n):
                for v in range(u + 1, n):
                    c, cuts = mcp.min_cuts_by_sets(g, u, v)
                    union = 0
                    for cm in cuts:
                        union |= cm
                    ues = [e for e in range(g.m) if (union >> e) & 1]
                    compat = {}
                    for e in ues:
                        for f in ues:
                            if e <= f:
                                both = (1 << e) | (1 << f)
                                compat[(e, f)] = any((cm & both) == both for cm in cuts)
                    for k in range(1, min(kmax, len(ues)) + 1):
                        for S in itertools.combinations(ues, k):
                            sm = 0
                            for e in S:
                                sm |= 1 << e
                            joint = any((cm & sm) == sm for cm in cuts)
                            pair = all(compat[(min(e, f), max(e, f))] for e in S for f in S)
                            assert joint == pair, (n, es, u, v, S)
                            subsets += 1
                            pos += joint
    return graphs, subsets, pos


def t2(nmax):
    stats = dict(graphs=0, diam2=0, lam_ok=0, nontriv=0, prop5_ok=0, path3=0)
    for n in range(4, nmax + 1):
        for _, es in mcp.connected_graphs(n, CACHE):
            g = mcp.Gr(n, es)
            D = mcp.dist_matrix(g)
            if max(max(r) for r in D) > 2:
                continue
            deg = [len(g.adj[x]) for x in range(n)]
            d = min(deg)
            if d < 2:
                continue
            stats["graphs"] += 1
            stats["diam2"] += 1
            # global edge connectivity by enumerating vertex sets (n <= 8)
            best = None
            cuts = []
            for A in range(1, (1 << n) - 1):
                if not (A & 1):
                    continue
                mask = 0
                for e, (a, b) in enumerate(g.edges):
                    if ((A >> a) ^ (A >> b)) & 1:
                        mask |= 1 << e
                k = mcp.popcount(mask)
                if best is None or k < best:
                    best, cuts = k, [(A, mask)]
                elif k == best:
                    cuts.append((A, mask))
            assert best == d, ("Plesnik fails?", n, es)
            stats["lam_ok"] += 1
            nontrivial = [(A, m) for A, m in cuts
                          if mcp.popcount(A) >= 2 and n - mcp.popcount(A) >= 2]
            has_nt = bool(nontrivial)
            # Proposition 5: search for the partition
            ok = False
            for Aset in itertools.combinations(range(n), d):
                if not all(g.has_edge(a, b) for a, b in itertools.combinations(Aset, 2)):
                    continue
                inA = set(Aset)
                B = set()
                bad = False
                for a in Aset:
                    nb = [y for y, _ in g.adj[a] if y not in inA]
                    if len(nb) != 1:
                        bad = True
                        break
                    B.add(nb[0])
                if bad:
                    continue
                C = set(range(n)) - inA - B
                if len(B) + len(C) < d:
                    continue
                if any(y in inA for c in C for y, _ in g.adj[c]):
                    continue  # a vertex of A with a neighbour in C
                if any(not g.has_edge(b, c) for b in B for c in C):
                    continue
                if any(not any(y in inA for y, _ in g.adj[b]) for b in B):
                    continue
                ok = True
                break
            assert ok == has_nt, ("Prop 5 mismatch", n, es, ok, has_nt)
            stats["prop5_ok"] += 1
            stats["nontriv"] += has_nt
            # no global minimum cut contains a path with 3 edges (cut graph = bipartite graph on the cut edges)
            for A, m in cuts:
                for e in range(g.m):
                    if not (m >> e) & 1:
                        continue
                # longest path in the cut subgraph: brute force over simple paths with 3 edges
                ce = [g.edges[e] for e in range(g.m) if (m >> e) & 1]
                adj = {}
                for a, b in ce:
                    adj.setdefault(a, set()).add(b)
                    adj.setdefault(b, set()).add(a)
                for x in adj:
                    for y in adj[x]:
                        for z in adj[y]:
                            if z == x:
                                continue
                            for w in adj[z]:
                                if w not in (x, y):
                                    stats["path3"] += 1
    return stats


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "t1a":
        print("T1a graphs, (graph,pair,path) triples, triples with path in a min cut:", t1a(int(sys.argv[2])))
    elif which == "t1b":
        print("T1b graphs, edge subsets, subsets in a common min cut:", t1b(int(sys.argv[2])))
    elif which == "t2":
        print("T2", t2(int(sys.argv[2])))
```

### check_poset.py (T3; argument `8`)

```python
"""T3 (literature agent): the partial order on the edges of minimum u-v cuts.

For a maximum u-v flow f of the symmetric digraph of G (arcs xy and yx of capacity 1) let R be the residual
relation of Picard and Queyranne (i R j iff arc (i,j) with f_ij < 1, or arc (j,i) with f_ji > 0) and R* its
reflexive-transitive closure.  An edge xy with f_xy = 1, f_yx = 0 has tail t = x and head h = y.
Claim: (a) an edge lies in some minimum cut iff it has a tail, a head, and neither h nor v is R*-reachable from
{u, t}; (b) for two such edges e, e': they lie in a common minimum cut iff t(e') does not R*-reach h(e) and
t(e) does not R*-reach h(e'); (c) the relation e < e' iff t(e') R* h(e) is a strict partial order on these edges.
Tested against brute force (all minimum cuts by vertex sets) on all connected graphs with n <= 7 and all pairs.
"""
import sys
import networkx as nx

sys.path.insert(0, "C:/Users/norom/Documents/latex/projects/clanok-2-min-cut-path.submission/checks")
import mcp  # read-only import


def reach(adj, sources):
    seen = set(sources)
    st = list(sources)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def run(nmax):
    graphs = pairs = edges_checked = pairs_checked = 0
    for n in range(3, nmax + 1):
        for _, es in mcp.connected_graphs(n, "C:/Users/norom/Documents/latex/tmp/clanok-2-checks"):
            g = mcp.Gr(n, es)
            graphs += 1
            D = nx.DiGraph()
            for a, b in g.edges:
                D.add_edge(a, b, capacity=1)
                D.add_edge(b, a, capacity=1)
            for u in range(n):
                for v in range(u + 1, n):
                    pairs += 1
                    val, fd = nx.maximum_flow(D, u, v)
                    c, cuts = mcp.min_cuts_by_sets(g, u, v)
                    assert val == c
                    radj = {x: set() for x in range(n)}
                    for i in range(n):
                        for j in D.successors(i):
                            if fd[i][j] < 1:
                                radj[i].add(j)
                            if fd[j][i] > 0:
                                radj[i].add(j)  # (j,i) arc with positive flow: i R j  (arc j->i exists in D)
                    # note: i R j via the second clause needs arc (j,i) in A with f_ji > 0; D is symmetric
                    star = {x: reach(radj, [x]) for x in range(n)}
                    cl_u = star[u]
                    tail = {}
                    for e, (a, b) in enumerate(g.edges):
                        if fd[a][b] == 1 and fd[b][a] == 0:
                            tail[e] = (a, b)
                        elif fd[b][a] == 1 and fd[a][b] == 0:
                            tail[e] = (b, a)
                    union = 0
                    for cm in cuts:
                        union |= cm
                    ok_edges = []
                    for e in range(g.m):
                        inc = bool((union >> e) & 1)
                        if e in tail:
                            t, h = tail[e]
                            A = cl_u | star[t]
                            pred = (v not in A) and (h not in A)
                        else:
                            pred = False
                        assert pred == inc, ("(a)", n, es, u, v, e)
                        edges_checked += 1
                        if inc:
                            ok_edges.append(e)
                    less = {}
                    for e in ok_edges:
                        for f in ok_edges:
                            te, he = tail[e]
                            tf, hf = tail[f]
                            less[(e, f)] = he in star[tf]  # e < f iff t(f) R* h(e)
                    for e in ok_edges:
                        assert not less[(e, e)]
                    for e in ok_edges:
                        for f in ok_edges:
                            for h in ok_edges:
                                if less[(e, f)] and less[(f, h)]:
                                    assert less[(e, h)], ("(c) transitivity", n, es, u, v)
                            assert not (less[(e, f)] and less[(f, e)]), ("(c) antisymmetry", n, es, u, v)
                    for i, e in enumerate(ok_edges):
                        for f in ok_edges[i:]:
                            both = (1 << e) | (1 << f)
                            brute = any((cm & both) == both for cm in cuts)
                            poset = (not less[(e, f)]) and (not less[(f, e)])
                            assert brute == poset, ("(b)", n, es, u, v, e, f)
                            pairs_checked += 1
    return graphs, pairs, edges_checked, pairs_checked


if __name__ == "__main__":
    print("T3 graphs, vertex pairs, (edge) checks (a), edge-pair checks (b):", run(int(sys.argv[1])))
```

### check_o3o6.py (T4; argument `7`)

```python
"""T4 (literature agent): the lead's observations O6 and O3, tested against brute force.

O6: a u-v path x0=u, x1, ..., xk=v lies in a minimum u-v cut iff k is odd and the R-closure of the even-indexed
    vertices contains no odd-indexed vertex (R = residual relation of any maximum flow, Picard-Queyranne).
O3: a path u-a-b-v lies in a minimum cut iff ua, ab, bv are edges and the minimum cut between the vertex sets
    {u, b} and {a, v} has size c(u, v).
Brute force: all minimum cuts by vertex sets (mcp.min_cuts_by_sets).  All connected graphs with n <= 7, all pairs,
all simple u-v paths (O6) and all paths with three edges (O3).
"""
import sys
import networkx as nx

sys.path.insert(0, "C:/Users/norom/Documents/latex/projects/clanok-2-min-cut-path.submission/checks")
import mcp  # read-only import

CACHE = "C:/Users/norom/Documents/latex/tmp/clanok-2-checks"


def reach(adj, sources):
    seen = set(sources)
    st = list(sources)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def run(nmax):
    n_o6 = n_o3 = n_pos6 = n_pos3 = 0
    for n in range(3, nmax + 1):
        for _, es in mcp.connected_graphs(n, CACHE):
            g = mcp.Gr(n, es)
            D = nx.DiGraph()
            for a, b in g.edges:
                D.add_edge(a, b, capacity=1)
                D.add_edge(b, a, capacity=1)
            for u in range(n):
                for v in range(u + 1, n):
                    val, fd = nx.maximum_flow(D, u, v)
                    c, cuts = mcp.min_cuts_by_sets(g, u, v)
                    radj = {x: set() for x in range(n)}
                    for i in range(n):
                        for j in D.successors(i):
                            if fd[i][j] < 1 or fd[j][i] > 0:
                                radj[i].add(j)
                    for vs, pe in mcp.simple_paths(g, u, v):
                        pm = 0
                        for e in pe:
                            pm |= 1 << e
                        brute = any((cm & pm) == pm for cm in cuts)
                        k = len(pe)
                        evens = [vs[i] for i in range(0, k + 1, 2)]
                        odds = [vs[i] for i in range(1, k + 1, 2)]
                        A = reach(radj, evens)
                        crit = (k % 2 == 1) and not any(x in A for x in odds) and v not in A
                        assert crit == brute, ("O6", n, es, u, v, vs)
                        n_o6 += 1
                        n_pos6 += brute
                        if k == 3:
                            a, b = vs[1], vs[2]
                            H = nx.DiGraph()
                            for x, y in g.edges:
                                H.add_edge(x, y, capacity=1)
                                H.add_edge(y, x, capacity=1)
                            for x in (u, b):
                                H.add_edge("S", x, capacity=10 ** 6)
                            for y in (a, v):
                                H.add_edge(y, "T", capacity=10 ** 6)
                            cv, _ = nx.maximum_flow(H, "S", "T")
                            o3 = (cv == c)
                            assert o3 == brute, ("O3", n, es, u, v, vs, cv, c)
                            n_o3 += 1
                            n_pos3 += brute
    return n_o6, n_pos6, n_o3, n_pos3


if __name__ == "__main__":
    print("T4 O6 paths checked, positives, O3 paths checked, positives:", run(int(sys.argv[1])))
```

### check_len.py (T5; argument `8`)

```python
"""T5 (literature agent): lengths of u-v paths that lie inside a minimum u-v cut, all connected graphs with n <= 8.

For every graph, every pair (u,v) and every minimum cut delta(A) (all vertex sets A with u in A, v not in A) the cut edges
form a bipartite graph H; a u-v path inside the cut is a u-v path of H.  We record, per graph and pair, the set of lengths
of simple u-v paths of H and report the counts by length and the smallest graph (fewest vertices, then edges) with a
path of length 5 or more.  Only pairs with c(u,v) >= ell can have a path of length ell (antichain of size ell, D2/D3).
"""
import sys
import itertools
from collections import Counter

sys.path.insert(0, "C:/Users/norom/Documents/latex/projects/clanok-2-min-cut-path.submission/checks")
import mcp  # read-only import

CACHE = "C:/Users/norom/Documents/latex/tmp/clanok-2-checks"


def cut_paths(n, edges_in_cut, u, v):
    adj = {}
    for a, b in edges_in_cut:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    res = set()
    seen = {u}

    def rec(x, k):
        if x == v:
            res.add(k)
            return
        for y in adj.get(x, ()):
            if y not in seen:
                seen.add(y)
                rec(y, k + 1)
                seen.discard(y)

    rec(u, 0)
    return res


def run(nmax):
    cnt = Counter()
    first = {}
    for n in range(3, nmax + 1):
        for _, es in mcp.connected_graphs(n, CACHE):
            g = mcp.Gr(n, es)
            D = mcp.dist_matrix(g)
            for u in range(n):
                for v in range(u + 1, n):
                    c = mcp.edge_conn(g, u, v)
                    others = [x for x in range(n) if x != u and x != v]
                    lens = set()
                    for r in range(len(others) + 1):
                        for sub in itertools.combinations(others, r):
                            A = {u, *sub}
                            ce = [(a, b) for a, b in g.edges if (a in A) != (b in A)]
                            if len(ce) != c:
                                continue
                            lens |= cut_paths(n, ce, u, v)
                    for L in lens:
                        cnt[(L, D[u][v] if D[u][v] <= 3 else 3)] += 1
                        if L >= 5 and L not in first:
                            first[L] = (n, es, u, v, c)
    return cnt, first


if __name__ == "__main__":
    cnt, first = run(int(sys.argv[1]))
    print("(path length in a minimum cut, min(d(u,v),3)) -> number of (graph, pair) with such a path:")
    for k in sorted(cnt):
        print(k, cnt[k])
    print("first graph with a path of length >= 5:", first)
```
