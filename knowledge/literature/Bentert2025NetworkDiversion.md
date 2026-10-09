# Bentert2025NetworkDiversion

| | |
|---|---|
| Paper | Bentert, Drange, Fomin, Simonnes: *Planar Network Diversion*. SEA 2025, LIPIcs 338, 6:1-6:14. DOI 10.4230/LIPIcs.SEA.2025.6; arXiv 2502.16714 |
| Key | `Bentert2025NetworkDiversion` |
| Reading status | parts read 2026-10-09 (DROPS PDF): abstract, Section 1 with the problem definition and related work, statement of Theorem 8 |
| Full text | - (open access, DROPS) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- Network Diversion: given G, vertices s, t, an edge b and k, remove at most k edges so that every s-t path uses b while some s-t path remains; equivalently, find a minimal s-t cut of size at most k + 1 that contains b (Section 1).
- Status stated in Section 1: NP-hard on directed graphs (Curet 2001); open on undirected graphs; polynomial on planar graphs (Cullenbine, Wood, Newman 2013 for s, t on one face; Bentert et al., ICALP 2024, in general).
- Result: a deterministic O(n log n) algorithm for weighted planar graphs (Theorem 8), and an implementation.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| b is an s-t bridge in G - F | - | the diversion set F plus b is a minimal s-t cut |
| weighted edges | unweighted | |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Minimal s-t cut containing a prescribed edge: open on undirected graphs, polynomial on planar graphs | Section 1, Theorem 8 | article 1, introduction (related work) and conclusion (planar graphs) | undirected; planar for the algorithm |

## Difference from our work

Network Diversion asks for a minimal u-v cut that contains a prescribed edge; Separating Shortest Path asks for a u-v cut contained in a shortest u-v path.

## Doubts and open questions

- The NP-hardness on directed graphs is attributed to Curet (2001, Military Operations Research); not read.
