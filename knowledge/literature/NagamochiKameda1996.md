# NagamochiKameda1996

| | |
|---|---|
| Paper | Nagamochi, Kameda: *Constructing Cactus Representation for All Minimum Cuts in an Undirected Network*. Journal of the Operations Research Society of Japan 39(2), 1996, 135-158. DOI 10.15807/jorsj.39.135 |
| Key | `NagamochiKameda1996` |
| Reading status | parts, read 2026-10-12 in the publisher's PDF (orsj.org archive; scan with a poor text layer, p. 136 missing): abstract, Section 1, Sections 3.1-3.3 (statements), headings of Sections 6, 7, references |
| Full text | - (open access at the publisher) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Section 3; cited in article 1 for cactus representations |

## What the paper does

- Subject: an algorithm that builds a cactus representation of all **global** minimum cuts of an edge-weighted undirected network; for unit weights it runs in `O(|E| + λ|V|^2)` time, `λ` the weight of a minimum cut (abstract).
- Section 1, p. 135: a network is a cactus if two of its cycles share at most one vertex. All minimum cuts of a network can be embedded in a cactus of size `O(|V|)`; credited to Dinits, Karzanov and Lomonosov (1976, in Russian) and to Gabow (1991). All minimum cuts separating two specified vertices are found from one maximum flow; credited to Picard and Queyranne.
- Section 3.1, Lemmas 3.1 and 3.2 (the first credited to Bixby, to Dinits et al. and to Naor and Vazirani; the second its restatement): two crossing minimum cuts split the vertex set into four parts that form a circular MC-partition.
- Section 3.3, Lemma 3.4, p. 141 (credited to Dinits et al. and to Karzanov and Timofeev): if `(s,t)` is an edge with `λ(s,t) = λ(N)` (a critical edge), all minimum cuts of `N` that separate `s` and `t` are nested, so they belong to one ordered partition `(V_1, ..., V_r)` (the `(s,t)`-MC-partition), represented by a chain of 2-cycles. Page 142: a 4-cycle with two opposite vertices shows that this fails when `s` and `t` are not adjacent.
- Lemma 3.5, p. 142: the `(s,t)`-MC-partition is obtained from one maximum flow; the proof sketch says that Picard and Queyranne introduced a directed acyclic graph that represents all `s`-`t` cuts of weight `λ(s,t)`.
- Section 6: the `(s,t)`-cactus representation (the minimum cuts compatible with the `(s,t)`-MC-partition).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| min-cut: a cut of weight `λ(N)`, the global minimum | minimum `u`-`v` cut: a cut of `c(u,v)` edges | the notions agree for the pair `u`, `v` only if `c(u,v)` equals the edge-connectivity of the graph |
| `λ(u,v;N)` | `c(u,v)` | |
| cactus: a network in which two cycles share at most one vertex; representations use cycles of length two | cactus graph of article 1 | |
| critical edge `(s,t)` | - | `s`, `t` adjacent; in article 2 the pair is at distance at least two |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| attribution: all minimum cuts of a graph have a cactus representation (Dinits, Karzanov, Lomonosov 1976) | Section 1, p. 135; Section 2 | article 2, Introduction and the remark on the cactus in Section 3 (the Russian original is cited only through this paper) | global minimum cuts |
| crossing minimum cuts have a circular structure; the minimum cuts separating the ends of a critical edge are nested | Lemmas 3.2, 3.4 | background for S5; not needed as a tool | |

## Difference from our work

Nagamochi and Kameda represent the global minimum cuts of a graph; the minimum cuts between two fixed vertices appear only for the ends of an edge, where they are nested.
In article 2 the two vertices are not adjacent and their minimum cuts may cross, which is why two general paths with several links join consecutive squares.

## Doubts and open questions

- Page 136 (end of Section 1, beginning of Section 2) is missing from the scan and was not read.
- The paper does not state that contracting the 3-edge-connected classes of a 2-edge-connected graph gives the cactus; that statement is Lemma 11 of `Mehlhorn2017Certifying`.
