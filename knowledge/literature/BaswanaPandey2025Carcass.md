# BaswanaPandey2025Carcass

| | |
|---|---|
| Paper | Baswana, Pandey: *The connectivity carcass of a vertex subset in a graph: both odd and even case*. 2025 Symposium on Simplicity in Algorithms (SOSA), SIAM, 2025, 385-422. DOI 10.1137/1.9781611978315.30; arXiv 2503.06266 |
| Key | `BaswanaPandey2025Carcass` |
| Reading status | parts, read 2026-10-12 in arXiv v4 (2026-03-25, extended version of the SOSA paper): abstract, Sections 1, 1.1, 1.2 (beginning), 4.1, list of references. The proceedings text was not reachable; statement numbers are those of arXiv v4 |
| Full text | - (arXiv) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Section 3 |

## What the paper does

- Subject: for a vertex subset `S` of an undirected unweighted multigraph, a compact structure (the connectivity carcass of Dinitz and Vainshtein) that stores all `S`-mincuts, the smallest edge sets that separate some two vertices of `S`. The paper gives a self-contained treatment for odd and even cut-values.
- The two extreme cases (Section 1): `|S| = 2`, where a DAG of Picard and Queyranne stores and characterizes all `(s,t)`-mincuts; `S = V`, where a cactus of size `O(n)` does so for all global mincuts (credited to Dinitz, Karzanov and Lomonosov).
- Section 1.1: Definition 1 (single-source single-sink balanced DAG: one source, one sink, every other vertex has as many incoming as outgoing edges). For an undirected graph the DAG of Picard and Queyranne "turns out to be a special DAG" (p. 3), namely a balanced one. Definition 2 (quotient graph induced by a family of cuts: two vertices are merged iff no cut of the family separates them).
- Section 4.1 (pp. 17-19 of arXiv v4), the case of two vertices `s`, `t`:
  - Dinitz and Vainshtein introduced a structure called *strip* for storing and characterizing all `(s,t)`-mincuts, using locally orientable graphs; the section restates it with a balanced DAG and a maximum flow.
  - Every edge that joins two vertices separated by an `(s,t)`-mincut carries one unit of every maximum flow; the quotient graph induced by all `(s,t)`-mincuts, with every edge directed along the flow, is a balanced DAG with source `s` and sink `t` (Lemmas 18, 19).
  - Definition 22 (strip): this quotient graph together with the partition of the edges at every non-terminal into entering and leaving edges.
  - Definition 23, Lemma 20: `(A, V - A)` is an `(s,t)`-mincut of `G` iff its image is a transversal cut of the strip, that is, an `(s,t)`-cut whose source side no edge enters.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| `(s,t)`-mincut `(A, V - A)` | minimum `u`-`v` cut `δ(A)` | |
| vertex of the quotient graph induced by all `(s,t)`-mincuts | piece (component of `G - F`) | equal only after a proof: two vertices lie in one piece iff no minimum `u`-`v` cut separates them |
| edges of the strip, directed along a maximum flow | edges of `F`, oriented from tail to head | |
| balanced DAG: indegree = outdegree at every non-terminal | S4: every piece other than those of `u`, `v` has as many entering as leaving edges | for cut-value two the common value is 1 (link) or 2 (square) |
| transversal cut | set of pieces closed under "entering edge" | Lemma 20 is the form of Picard and Queyranne's Theorem 1 for the strip |
| multigraph | simple graph | |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| the structure of all minimum cuts between two vertices of an undirected graph is a balanced DAG (the strip of Dinitz and Vainshtein) | Section 4.1, Lemmas 18-20, Definition 22 (arXiv v4) | article 2, Section 3: attribution of S1-S5; the square decomposition is the strip for cut-value two | undirected unweighted multigraph |
| attribution of the DAG to Picard and Queyranne and of the cactus to Dinitz, Karzanov, Lomonosov | Sections 1, 1.1 | article 2, Introduction | secondary statement |

## Difference from our work

Baswana and Pandey restate the strip of Dinitz and Vainshtein, the balanced acyclic graph that represents all minimum cuts between two vertices, as a step towards the structure for a vertex subset.
Article 2 describes this structure explicitly for cut-value two (squares, links, general paths) and uses it to decide whether a shortest path is a cut; the paper does not consider paths or distances.

## Doubts and open questions

- Numbers (Definitions 1, 2, 22, 23, Lemmas 18-20) are those of arXiv v4; the SOSA text was not compared. Cite the section, or no number. `TODO(verify)`
- The original papers of Dinitz and Vainshtein (STOC 1994; SIAM J. Comput. 30(3), 2000, entry `DinitzVainshtein2000Carcass`, `PARTIAL`) were not read; the attribution of the strip rests on this paper.
- The bibliography of arXiv v4 gives Picard and Queyranne as "Math. Program. 22(1):121, 1982" (a one-page note in the journal); the workspace cites the chapter of 1980 (`PicardQueyranne1980`).
