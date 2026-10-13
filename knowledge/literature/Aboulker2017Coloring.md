# Aboulker2017Coloring

| | |
|---|---|
| Paper | Aboulker, Brettell, Havet, Marx, Trotignon: *Coloring Graphs with Constraints on Connectivity*. Journal of Graph Theory 85(4), 2017, 814-838. DOI 10.1002/jgt.22109; arXiv 1505.01616 (title there: *Colouring ...*) |
| Key | `Aboulker2017Coloring` |
| Reading status | parts, read 2026-10-12 in arXiv v2 (2016-10-14): abstract, Section 1 (pp. 1-4). The journal text was not compared |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Section 2 (the class) |

## What the paper does

- Colouring problems on graph classes defined by bounds on local connectivity (Section 1, p. 2). `κ(x,y)`: maximum number of internally vertex-disjoint `x`-`y` paths; `λ(x,y)`: maximum number of edge-disjoint `x`-`y` paths (local edge-connectivity).
- Four nested classes for an integer `k`: maximum degree `k`; `λ(x,y) ≤ k` for all pairs of distinct vertices; `κ(x,y) ≤ k` for all pairs; `κ(x,y) ≤ k` for all edges `xy`. A graph of the second class "has maximal local edge-connectivity `k`". All four are closed under taking subgraphs.
- Theorem 1.2: a `k`-connected graph with maximal local edge-connectivity `k`, `k ≥ 3`, is `k`-colourable iff it is not a complete graph or an odd wheel. Further results for `k = 3` and hardness results (abstract).
- For `k = 1` the largest class is the class of forests; for `k = 2` the chromatic number is computed in polynomial time in all four classes (p. 4). Section 1 gives no structural description of the graphs with `λ(x,y) ≤ 2` for all pairs.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| `λ(x,y)`, local edge-connectivity | `c(x,y)`, cut-value | equal by Menger's theorem |
| maximal local edge-connectivity `k`: `λ(x,y) ≤ k` for all pairs | - | for `k = 2`: the graphs of Lemma 6.1 of article 1 (every block an edge or a cycle; cactus graphs when connected) |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| a named family of classes defined by `λ(x,y) ≤ k` for all pairs | Section 1, p. 2 | article 2, Section 2: the nearest classes in the literature to `DC_2`; the condition of `DC_2` relaxes `λ(x,y) ≤ 2` to the pairs at distance at least three | no distance condition in the paper |

## Difference from our work

Aboulker et al. bound the local edge-connectivity of all pairs of vertices; the class of article 2 bounds it by two only for pairs at distance at least three, so it also contains all graphs of diameter two.

## Doubts and open questions

- Related line, not read: Stiebitz and Toft, *A Brooks type theorem for the maximum local edge connectivity*, Electron. J. Combin. 25(1), 2018, DOI 10.37236/6043 (record seen in OpenAlex and in a web search only).
