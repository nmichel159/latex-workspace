# PicardQueyranne1980

| | |
|---|---|
| Paper | Picard, Queyranne: *On the structure of all minimum cuts in a network and applications*. Combinatorial Optimization II (Mathematical Programming Studies 13), 1980, 8-16. DOI 10.1007/BFb0120902 |
| Key | `PicardQueyranne1980` |
| Reading status | full text of the authors' technical report with the same title and abstract (École Polytechnique de Montréal, Rapport Technique EP-79-R-15, March 1979, 23 pages, <https://publications.polymtl.ca/5993/>), read 2026-10-12; of the published chapter only the abstract (publisher's page). Statement numbers below are those of the **report**; the chapter was not compared |
| Full text | - (report: open access at PolyPublie) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Sections 3 and 5 |

## What the paper does

- Problem: describe all minimum cuts that separate a source `s` from a sink `t` in a directed network with positive arc capacities (Section 1). There can be exponentially many (`2^(n-2)` in the example of Section 1).
- Theorem 1 (Section 2, p. 4): let `f` be any maximum flow and define `i R j` iff (`(i,j)` is an arc and `f_ij < c_ij`) or (`(j,i)` is an arc and `f_ji > 0`). A cut `(S, V - S)` separating `s` from `t` is a minimum cut iff `S` is a closure for `R` that contains `s` and not `t`. A closure is a set `C` such that `i ∈ C` and `i R j` imply `j ∈ C`.
- Corollary 3 (p. 5): unions and intersections of (source sides of) minimum cuts are minimum cuts.
- Pages 5-6: different maximum flows give relations with the same transitive closure (Propositions 4, 5); shrinking the strong connected components gives an acyclic relation; the component of `t` with its predecessors and the component of `s` with its successors are removed, and every closure of the rest gives a minimum cut.
- Corollary 6 (Section 3, p. 8): a saturated arc belongs to some minimum cut iff its ends do not lie in the same connected component of `R` (the strong components of p. 6).
- Section 3: applications (sensitivity analysis, most vital arcs, vertex packing, maximum closure, enumeration of all minimum cuts).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| directed network `N = (V, A, c)`, positive capacities | undirected graph, every edge of capacity one | an edge `{x,y}` is the two arcs `(x,y)`, `(y,x)`; an edge that carries flow from `x` to `y` gives only `y R x`, an edge without flow gives `x R y` and `y R x` |
| relation `R` of a maximum flow | arcs of the residual digraph | `i R j` iff the residual digraph has the arc `(i,j)` |
| closure (hereditary subset) | closed set: no residual arc leaves it | |
| cut `(S, V - S)`: the arcs from `S` to `V - S` | `δ(S)` | for an undirected graph the two notions agree |
| "connected component of the relation `R`" (Corollary 6) | strongly connected component of the residual digraph | the report says "strong connected components" on p. 6 and "connected component" in the corollary |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| source sides of minimum `s`-`t` cuts = closed sets of the residual digraph that contain `s` and not `t` | Theorem 1 (report, p. 4) | article 2, S11 (the minimum `u`-`v` cuts are read from the residual digraph of `p_1`, `p_2`) | any maximum flow; directed network, positive capacities |
| a saturated arc lies in some minimum cut iff its ends lie in different strong components | Corollary 6 (report, p. 8) | article 2, S11 (computation of `F`) | the arc must be saturated; for an undirected edge of capacity one: the edge carries flow, i.e. lies on `p_1` or `p_2` |
| minimum cuts are closed under union and intersection | Corollary 3 (report, p. 5) | article 2, S6 (uncrossing) if a citation is wanted | |

## Difference from our work

Picard and Queyranne describe all minimum cuts between two vertices of a directed network by the closed sets of a relation obtained from one maximum flow.
Article 2 uses this description for cut-value two in an undirected graph, where it becomes a chain of squares joined by pairs of general paths, and asks which shortest paths are cuts.

## Doubts and open questions

- The numbers (Theorem 1, Corollary 6) are those of the report; compare with the published chapter before citing a number. Until then cite the paper without a number. `TODO(verify)`
- Corollary 6 needs the arc to be saturated. In an undirected graph with `c(u,v) = 2` every edge off `p_1 ∪ p_2` has both residual arcs, so its ends lie in one strong component, and it lies in no minimum cut; the article should say this in one sentence or prove the criterion directly.
- The report merges the strong component of `s` with its successors and that of `t` with its predecessors (p. 6). For an undirected graph and a flow that is a set of edge-disjoint paths, every vertex reachable from `s` in the residual digraph also reaches `s`, so the strong components are exactly the classes of vertices that no minimum cut separates. This is our argument, not a statement of the paper; it has to be proved in the article if the pieces are defined as strong components.
