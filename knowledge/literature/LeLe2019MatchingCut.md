# LeLe2019MatchingCut

| | |
|---|---|
| Paper | Le, Le: *A complexity dichotomy for matching cut in (bipartite) graphs of fixed diameter*. Theoretical Computer Science 770, 2019, 69-78. DOI 10.1016/j.tcs.2018.10.029; arXiv 1804.11102 |
| Key | `LeLe2019MatchingCut` |
| Reading status | parts read 2026-10-09 in arXiv v2 (accepted version, 2018-10-26): abstract, Sections 1-2 (Theorem 1), Section 4.2 |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- A matching cut is an edge cut (all edges between the two sides of a vertex partition) that is a matching; Matching Cut asks whether a graph has one (Section 1).
- Previous results (Section 1.1): NP-complete, also for maximum degree four (Chvatal 1984); polynomial for diameter two (Borowiecki, Jesse-Jozefczyk 2008).
- Theorem 1: for every fixed d >= 3, Matching Cut is NP-complete on graphs of diameter d. Theorem 2: for d >= 4 also on bipartite graphs of diameter d. Section 4.2: a new O(|V| |E|^2) algorithm for diameter two.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| cut = vertex partition (X, Y); edge cut = edges between X and Y | u-v cut = edge set meeting every u-v path; a minimum one is delta(A) | their edge cut matches our delta(A) |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Matching Cut polynomial on diameter two, NP-complete on every fixed diameter d >= 3 | Section 1.1, Theorem 1 | article 1, related work; a remark next to Section 4 | simple graphs |

## Difference from our work

Matching Cut asks for an edge cut with a prescribed structure (a matching); Separating Shortest Path asks for a u-v cut contained in a shortest path. Both are polynomial on graphs of diameter two.

## Doubts and open questions

- Chvatal (1984) itself was not read; cite it only after reading.
