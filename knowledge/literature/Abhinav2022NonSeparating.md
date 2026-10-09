# Abhinav2022NonSeparating

| | |
|---|---|
| Paper | Abhinav, Bandopadhyay, Banik, Kobayashi, Nagano, Otachi, Saurabh: *Parameterized Complexity of Non-Separating and Non-Disconnecting Paths and Sets*. MFCS 2022, LIPIcs 241, 6:1-6:15. DOI 10.4230/LIPIcs.MFCS.2022.6. Earlier preprint of part of it: Kobayashi, Nagano, Otachi, arXiv 2202.09718 |
| Key | `Abhinav2022NonSeparating` |
| Reading status | full text read 2026-10-09 (DROPS PDF): abstract, Sections 1-2, statements of Section 3-4 |
| Full text | - (open access, DROPS) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- Input: a connected graph G, vertices s, t, an integer k. A path P from s to t is *non-separating* if G - V(P) is connected and *non-disconnecting* if G - E(P) is connected (Definitions 1, 2).
- Motivation (Section 1): a private channel between s and t whose path no other connection uses, so the rest of the network must stay connected without it. Ours is the opposite requirement.
- Both shortest-path problems were known to be NP-hard: the vertex version by Wu and Chen (2009 workshop), the edge version by `Mao2021NonSeparating` (Section 1, "Related work").
- Results: Shortest Non-Separating Path is NP-complete on planar, bipartite and split graphs (Theorem 7) and W[1]-hard in k (Theorem 9); polynomial on chordal graphs when k = d(s, t) (Theorem 23). Shortest Non-Disconnecting Path is FPT in k, time 2^{omega k} n^{O(1)} (Theorem 24), with no polynomial kernel unless coNP is in NP/poly (Theorem 28).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| s, t | u, v | |
| G - E(P) connected (whole graph) | G \ P has no u-v path | theirs asks for connectivity of all of G, ours for separation of u and v |
| length = number of edges | same | unweighted |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Shortest non-disconnecting s-t path: NP-hard (via Mao), FPT in the length k | Section 1 (Related work), Theorem 24 | article 1, introduction, related work | connected undirected graph, unweighted |

## Difference from our work

A non-disconnecting u-v path keeps the graph connected after its edges are removed; Separating Shortest Path asks for a shortest u-v path whose removal separates u from v.

## Doubts and open questions

- No journal version found on 2026-10-09 (web search, Crossref).
