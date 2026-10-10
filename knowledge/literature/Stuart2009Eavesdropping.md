# Stuart2009Eavesdropping

| | |
|---|---|
| Paper | Stuart, J. L.: *The eavesdropping number of a graph*. Czechoslovak Mathematical Journal 59(3), 2009, 623-636. DOI 10.1007/s10587-009-0056-9 |
| Key | `Stuart2009Eavesdropping` |
| Reading status | parts read 2026-10-10 in the journal text (DML-CZ, dml.cz/dmlcz/140505): abstract, Section 4 up to Theorem 12, reference list. A subagent read the full text the same day (`projects/clanok-1-min-cut-path.submission/literature-review-2026-10-10/B2-path-and-cut.md`) |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- For distinct vertices `u`, `v` of a connected simple graph, `lambda(u,v)` is the size of a smallest set of edges
  whose removal disconnects `u` and `v` (abstract). The eavesdropping number is the maximum of `lambda(u,v)` over
  all pairs; the edge connectivity is the minimum.
- Section 4, p. 627: a graph is *maximally locally connected* if `lambda(u,v) = min{d(u), d(v)}` for all distinct
  `u`, `v` (`d` = degree). Theorem 11: if `diam(G) <= 2`, then `lambda(u,v) = min{d(u), d(v)}` for all pairs of
  distinct vertices. No proof; credited to Fricke, Oellermann and Swart, "The edge-connectivity, average
  edge-connectivity and degree conditions", manuscript, 2000 (its reference [4]).
- Motivation (Section 1, per the subagent's reading): intercepting the communication between any two centres of a
  network; cuts only, no path.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| `lambda(u,v)`, minimum `{u,v}`-separating set | `c(u,v)`, minimum `u`-`v` cut | same object (edge sets) |
| `d(u)` | `deg(u)` | our `d(u,v)` is the distance |
| maximally locally connected | - | other authors: maximally local-edge-connected (Hellwig, Volkmann) |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| `lambda(u,v) = min{d(u), d(v)}` in graphs of diameter at most two | Theorem 11, p. 627 (statement only) | article 1: attribution of the first equality of Corollary `cor:diameter-two-degrees` (5.7), cited in the Introduction | finite simple undirected graph, `diam(G) <= 2`, `u != v` |

## Difference from our work

The theorem gives the cut-value `c(u,v)` in graphs of diameter two; it says nothing about a path inside a cut or
about `cp(u,v)`. Theorem 5.5 of article 1 (`cp = c + d - 1`) is not in this literature.

## Doubts and open questions

- The original proof is in an unpublished manuscript (Fricke, Oellermann, Swart, 2000); no copy found. A published
  proof of a generalization to digraphs: Hellwig, Volkmann, *Maximally local-edge-connected graphs and digraphs*,
  Ars Combinatoria 72 (2004) 295-306 (zbMATH Zbl 1082.05055; record only, not read). The statement with both
  attributions was read by the subagent in Hellwig's dissertation (RWTH Aachen, 2005, Theorems 1.23 and 6.1).
- The survey of Hellwig and Volkmann (Discrete Mathematics 308(15), 2008, 3265-3296, DOI
  10.1016/j.disc.2007.06.035) covers the topic; its text could not be opened (ScienceDirect, HTTP 403), so the
  theorem number there is `TODO(verify)`.
- Global version (edge connectivity equals minimum degree in diameter two): Plesník, *Critical graphs of given
  diameter*, Acta Fac. Rerum Natur. Univ. Comenian. Math. 30 (1975) 71-93 (record only).
