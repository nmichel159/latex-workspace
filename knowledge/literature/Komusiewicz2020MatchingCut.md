# Komusiewicz2020MatchingCut

| | |
|---|---|
| Paper | Komusiewicz, Kratsch, Le: *Matching cut: Kernelization, single-exponential time FPT, and exact exponential algorithms*. Discrete Applied Mathematics 283, 2020, 44-58. DOI 10.1016/j.dam.2019.12.010. Preliminary version IPEC 2018 |
| Key | `Komusiewicz2020MatchingCut` |
| Reading status | parts read 2026-10-09 in the accepted version (Marburg group's page, dated 2019-12-16): abstract, Section 1 |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- Definitions as in `LeLe2019MatchingCut`; it notes that a matching whose removal disconnects G need not be a matching cut (Section 1).
- Section 1 summarizes the complexity: NP-complete (Chvatal 1984), also for maximum degree four, planar graphs of maximum degree four, bipartite graphs of maximum degree four; polynomial for maximum degree three; many graph classes studied.
- Results: kernels for distance to cluster and to clique, single-exponential FPT algorithms, an O*(1.3071^n) randomized algorithm, no polynomial kernel in treewidth plus cut size plus maximum degree unless NP is in coNP/poly (abstract).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| edge cut of a partition (A, B) | delta(A) | same object |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Matching Cut is NP-complete and studied for many classes and parameters | Section 1 | article 1, related work (one clause) | - |

## Difference from our work

It studies cuts with a prescribed structure (matchings) by parameters and exact algorithms; cut-paths prescribe that a cut lies inside few edges together with a path.

## Doubts and open questions

- Cited mainly as the Discrete Applied Mathematics entry point to matching cuts; its own results (kernels, FPT) are not used.
