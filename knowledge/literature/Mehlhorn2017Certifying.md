# Mehlhorn2017Certifying

| | |
|---|---|
| Paper | Mehlhorn, Neumann, Schmidt: *Certifying 3-Edge-Connectivity*. Algorithmica 77(2), 2017, 309-335. DOI 10.1007/s00453-015-0075-x; arXiv 1211.6553 |
| Key | `Mehlhorn2017Certifying` |
| Reading status | parts, read 2026-10-12 in arXiv v3 (2015-10-07, posted after acceptance): abstract, Sections 1, 2, 4 (beginning), 10, 11 (statements), 12, references. The journal text is behind a paywall; statement numbers are those of arXiv v3 |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Sections 2 and 3; cited in article 1 for the certification of 3-edge-connectivity |

## What the paper does

- A linear-time certifying algorithm for 3-edge-connectivity: a 2-edge cut if the graph is not 3-edge-connected, a construction sequence of Mader otherwise (abstract, Section 1).
- Section 1, p. 2: the 3-edge-connected components of a graph are the maximal subsets of the vertex set in which any two vertices are connected by three edge-disjoint paths; the paths need not stay inside the subset. (They are classes of vertices, not subgraphs.)
- Section 2: earlier linear-time algorithms for 3-edge-connectivity: Galil and Italiano 1991, Nagamochi and Ibaraki 1992 and their book of 2008, Taoka, Watanabe and Onaga 1992, Tsin 2007 and 2009; all but the first also compute the 3-edge-connected components.
- Section 4, Lemma 1 (credited to Schmidt 2013): a graph is 2-edge-connected iff it is connected and the chains of a chain decomposition partition its edge set.
- Section 10, pp. 16-17: a cactus is a graph in which every edge is contained in exactly one cycle. Dinits, Karzanov and Lomonosov showed that the minimum cuts of any graph have a cactus representation `(C, φ)`, `φ : V(G) → V(C)`: the minimum cuts of `G` are exactly the preimages of the minimum cuts of `C`. In general nodes with empty preimage are needed; not when the minimum cuts have size two.
- Lemma 11 (credited to Nagamochi and Ibaraki 2008, Section 2.3.5): let `G` be 2-edge-connected and not 3-edge-connected. Contracting each 3-edge-connected component of `G` into a node yields a cactus representation `(C, φ)` of `G` such that (i) the edges of `C` correspond one-to-one to the edges of `G` that are contained in a 2-cut, and (ii) the preimage of every node is a 3-edge-connected component of `G`.
- Sections 10, 11 (Lemma 15): the 3-edge-connected components and this cactus are computed and certified in linear time.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| 3-edge-connected component: a maximal set of vertices pairwise joined by three edge-disjoint paths | class of the relation `c(x,y) ≥ 3` | the same by Menger's theorem; "component" is not a subgraph here |
| cactus: every edge lies in exactly one cycle (cycles of length two allowed, the cactus is a multigraph) | cactus graph of article 1: connected, two cycles share at most one vertex | their cactus has no bridges; two parallel edges form a cycle |
| mincut given by a vertex set (footnote 2) | `δ(A)` | |
| blob = preimage of a node | 3-edge-connected class | |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| contracting the 3-edge-connected components of a 2-edge-connected graph gives a cactus that represents its 2-edge cuts | Lemma 11 (arXiv v3), credited to Nagamochi and Ibaraki 2008 | article 2, Section 3 (remark: relation of the square decomposition to the cactus), S13 | `G` 2-edge-connected, not 3-edge-connected; multigraph cactus |
| the 3-edge-connected components are computed in linear time | Sections 2, 10, 11 | article 2, S13 (recognition of the class) and the remark above | |

## Difference from our work

The cactus of Lemma 11 represents all 2-edge cuts of a 2-edge-connected graph at once.
For a pair `u`, `v` with `c(u,v) = 2`, the minimum `u`-`v` cuts are the pairs of edges of one cycle of this cactus that separate the nodes of `u` and `v`; these cycles form a chain between the two nodes, which is the square decomposition of article 2 (our derivation, to be proved in the article; the paper does not consider a fixed pair, paths or distances).

## Doubts and open questions

- Lemma 11 is the number in arXiv v3; compare with the journal text before citing the number. `TODO(verify)`
- The primary source of Lemma 11, Section 2.3.5 of the book of Nagamochi and Ibaraki (entry `NagamochiIbaraki2008`, `PARTIAL`), was not read.
- The paper writes "Dinits, Karzanov, and Lomonsov ... Studies in Discrete Mathematics (in Russian)"; Nagamochi and Kameda 1996 give the title of the volume as "Studies in Discrete Optimization". The Russian original was not seen.
