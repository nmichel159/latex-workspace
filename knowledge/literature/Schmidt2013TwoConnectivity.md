# Schmidt2013TwoConnectivity

| | |
|---|---|
| Paper | Schmidt: *A simple test on 2-vertex- and 2-edge-connectivity*. Information Processing Letters 113(7), 2013, 241-244. DOI 10.1016/j.ipl.2013.01.016; arXiv 1209.0700 |
| Key | `Schmidt2013TwoConnectivity` |
| Reading status | full text of arXiv v1 (2012-09-04, the only version), read 2026-10-12. The journal text was not compared; statement numbers are those of the preprint |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Section 2 (bridges) |

## What the paper does

- A chain decomposition of a connected graph: a depth-first search tree, then one chain (a path or a cycle) for every back-edge, in the order of the search; computed in linear time (Section 2).
- Theorems 1-3 (Section 2): 2-edge-connectivity and 2-connectivity are read off the chains (Theorem 1: the chains partition the edge set; Theorem 2: for a 2-edge-connected graph, 2-connected iff the first chain is the only cycle).
- Lemma 4: an edge of a simple connected graph is a bridge iff it is contained in no chain.
- Section 4: Lemmas 4 and 5 give all bridges and cut vertices in linear time, and from them the 2-connected components and the 2-edge-connected components (the maximal 2-edge-connected subgraphs).
- Section 1: the first linear-time algorithms for the two tests are credited to Tarjan (1972, 1974).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| 2-edge-connected component: maximal 2-edge-connected subgraph | 2-edge-connected component `K` of `u` (S0) | the same; a component of the graph without its bridges |
| `δ(G)` minimum degree | - | in our texts `δ(A)` is a cut |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| bridges and 2-edge-connected components in linear time | Lemma 4, Section 4 (arXiv v1) | article 2, S0 (restriction to the 2-edge-connected component of `u`), S11 | simple connected graph |

## Difference from our work

Source of a standard linear-time algorithm; no relation to the problem.

## Doubts and open questions

- Tarjan, *A note on finding the bridges of a graph*, Information Processing Letters 2(6), 1974, 160-161 is the original source by this paper; it was not read and has no entry.
