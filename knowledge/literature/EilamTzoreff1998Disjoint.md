# EilamTzoreff1998Disjoint

| | |
|---|---|
| Paper | Eilam-Tzoreff, T.: *The disjoint shortest paths problem*. Discrete Applied Mathematics 85(2), 1998, 113-138. DOI 10.1016/S0166-218X(97)00121-2 |
| Key | `EilamTzoreff1998Disjoint` |
| Reading status | parts read 2026-10-10 by a search subagent: abstract and pp. 113-120 (Sections 1, 2, start of 3) of the journal PDF, from an Internet Archive snapshot of the CORE copy; Sections 4-5 not read (`projects/clanok-1-min-cut-path.submission/literature-review-2026-10-10/B1-path-removal.md`, block 1.1). Not re-read by the main session: ScienceDirect answered with a captcha. The article is in Elsevier's open archive |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- `k` disjoint shortest paths: given `k` pairs of vertices in a graph with positive edge lengths, find pairwise
  disjoint shortest paths, one for each pair. Polynomial for two pairs on undirected graphs (abstract);
  NP-complete on planar undirected graphs when `k` is part of the input (Claim 4).
- Section 2, problem 2D1SP: two pairs `(s1, t1)`, `(s2, t2)`; are there disjoint paths `P1` from `s1` to `t1` and
  `P2` from `s2` to `t2` such that `P1` is a shortest path? Claim 1: NP-complete on undirected graphs, vertex- and
  edge-disjoint version; the reduction is from 3SAT and replaces every edge by a path of unit edges, so the claim
  holds for unit lengths. Claim 3: the same for directed graphs.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| two terminal pairs | one pair `u`, `v` | in the reduction the two pairs are different |
| positive edge lengths | unit lengths | Claim 1 holds for unit lengths |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| deciding whether some shortest `s1`-`t1` path is edge-disjoint from some `s2`-`t2` path is NP-complete | Claim 1, Section 2 | article 1, Introduction (related work): the requirement opposite to Separating Shortest Path | undirected graphs, edge-disjoint version, two pairs |

## Difference from our work

In 2D1SP the removal of the edges of a shortest path must leave a second pair of vertices connected; in Separating
Shortest Path it must separate the two ends of the path itself. Neither result implies the other.

## Doubts and open questions

- The one-pair form ("two edge-disjoint `s`-`t` paths, one of them shortest") is the Min-Min disjoint paths problem:
  Xu, Chen, Xiong, Qiao, He, IEEE/ACM Trans. Netw. 14(1) (2006) 147-158, DOI 10.1109/TNET.2005.863451; Guo and Shen,
  Algorithmica 66(3) (2013) 641-653, DOI 10.1007/s00453-012-9656-0. Both read as abstracts only, so they are not
  cited in article 1. `TODO(verify)` in the full texts: hardness for undirected graphs with unit lengths, and
  whether the hard instances ask for a path of length exactly `d(s,t)`.
- Separating Shortest Path is neither this one-pair problem nor its complement (a graph can have a shortest path
  with an edge-disjoint counterpart and another one without).
