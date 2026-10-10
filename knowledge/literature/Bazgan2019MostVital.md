# Bazgan2019MostVital

| | |
|---|---|
| Paper | Bazgan, Fluschnik, Nichterlein, Niedermeier, Stahlberg: *A more fine-grained complexity analysis of finding the most vital edges for undirected shortest paths*. Networks 73(1), 2019, 23-37. DOI 10.1002/net.21832; arXiv 1804.09155 |
| Key | `Bazgan2019MostVital` |
| Reading status | parts read 2026-10-09 in arXiv v1 (2018-04-24): abstract, Section 1, Theorems 1, 3, 4, Proposition 1. Journal text not reachable (Wiley refused the request); theorem numbers below are those of the preprint |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- Shortest Path Most Vital Edges (SP-MVE): given G, s, t, k, l, is there a set S of at most k edges such that every s-t path in G - S has length at least l? Equivalent names: interdiction, edge blocker; with unit lengths it is the minimum length-bounded edge cut of Baier et al. (2010) and Bounded Edge Undirected Cut of Golovach and Thilikos (2011) (Section 1).
- NP-complete (Bar-Noy, Khuller, Schieber 1995, cited in Section 1). New: NP-hard already for unit lengths, b = l - d(s,t) = 2, l = 9 and diameter 8 (Theorem 1); NP-hard on split graphs, hence on diameter three (Theorem 4); linear time on graphs of diameter at most two with unit lengths (Proposition 1). The case b = 1 is polynomial (Baier et al.). For arbitrary positive integer edge lengths SP-MVE is NP-hard already on complete graphs, so on diameter one (Theorem 5, read 2026-10-10); the diameter results (Theorem 4, Proposition 1) are for unit lengths.
- Parameterized results (Figure 1): FPT in (k, l), W[1]-hard in k, parameters of graph structure.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| s, t; dist_G(s,t) | u, v; d(u,v) | |
| s-t edge cut | u-v cut | same notion |
| k smaller than every s-t cut (assumed) | - | with k at least the cut size the problem is a minimum cut |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| SP-MVE NP-hard; linear time on diameter at most two, NP-hard on diameter three | Section 1; Proposition 1; Theorem 4 (preprint numbering) | article 1, introduction (related work), possibly Section 5 | unit edge lengths for the diameter results |

## Difference from our work

SP-MVE deletes few edges so that every remaining u-v path is long; a cut-path must meet every u-v path and contain one of them. Both problems become easy on graphs of diameter two.

## Doubts and open questions

- Compare Theorem 4 and Proposition 1 with the journal version before citing their numbers; otherwise cite the paper without numbers.
