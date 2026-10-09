# Mao2021NonSeparating

| | |
|---|---|
| Paper | Mao: *Shortest non-separating st-path on chordal graphs*. arXiv 2101.03519 (v3, 2021-02-09), preprint |
| Key | `Mao2021NonSeparating` |
| Reading status | parts read 2026-10-09 in arXiv v3: abstract, Section 1, Section 2 (definitions), Section 9 (NP-hardness) |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- A non-separating path is a path whose edge removal leaves the graph connected (Definition 1.1); the vertex version (Definition 1.2) is the classical one, going back to Lovasz's path removal conjecture.
- Deciding whether a non-separating s-t path exists is NP-hard on general graphs (Theorem 1.6; proof in Section 9 by a reduction from 3-SAT with a chain of variable gadgets and clause vertices attached by subdivided edges).
- On connected chordal graphs a non-separating s-t path exists iff s and t are not separated by a bridge (Theorem 1.5); a shortest one is found in O(n log n + m) time (Theorem 1.4).
- Section 2 calls a path *separating* if its edge set disconnects G (any two vertices), not only s and t.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| separating path: G \ E(P) disconnected | separating: G \ P has no u-v path | ours is relative to u, v |
| S, T | u, v | |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Existence of a non-separating (edge version) s-t path is NP-hard | Theorem 1.6, Section 9 | article 1, related work | general undirected graphs |

## Difference from our work

A non-separating u-v path leaves the graph connected after its edges are removed; Separating Shortest Path asks for the opposite, a shortest u-v path whose edges contain a u-v cut.

## Doubts and open questions

- Preprint only (no published version found 2026-10-09); the published `Abhinav2022NonSeparating` cites it for the edge-version hardness. The reduction in Section 9 is a sketch ("one can see that ...").
