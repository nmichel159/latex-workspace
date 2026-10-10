# Baier2010LengthBounded

| | |
|---|---|
| Paper | Baier, Erlebach, Hall, Köhler, Kolman, Pangrác, Schilling, Skutella: *Length-bounded cuts and flows*. ACM Transactions on Algorithms 7(1), 2010, 1-27. DOI 10.1145/1868237.1868241 |
| Key | `Baier2010LengthBounded` |
| Reading status | parts read 2026-10-10: the abstract of the published article (Crossref record) and, in the authors' manuscript of the journal version (kam.mff.cuni.cz/~kolman/papers/acmlcuts.pdf, 27 pages), the abstract, Table I, the conventions of Section 2 and Theorems 3.9 and 3.11. The published text was not compared, so theorem numbers are the manuscript's |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- An *`L`-length-bounded edge-cut* (node-cut) for a source `s` and a sink `t` is a set of edges (nodes) after whose
  removal no `s`-`t` path of length at most `L` remains (abstract). Unit lengths and unit capacities unless stated
  otherwise (Section 2).
- The minimum length-bounded cut is NP-hard to approximate within a factor of 1.1377, for `L >= 5` (node-cuts,
  Theorem 3.9) and for `L >= 4` (edge-cuts, Theorem 3.11), in directed and undirected graphs; the reduction is from
  Vertex Cover. Approximation ratios `O(min{L, n/L})` and `O(min{L, n^2/L^2, sqrt m})` (abstract).
- Gaps between minimum length-bounded cuts and maximum length-bounded flows; polynomial cases for small `L`
  (Table I).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| `s`, `t`, length bound `L` | `u`, `v` | a `u`-`v` cut is an `L`-length-bounded edge-cut for every `L` |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| the term length-bounded edge-cut; NP-hardness of approximation within 1.1377 | abstract; Theorem 3.11 of the manuscript | article 1, Introduction (related work) | unit lengths, `L >= 4`, edge version |

## Difference from our work

A length-bounded cut destroys the short `u`-`v` paths and contains no path; a cut-path meets every `u`-`v` path and
contains one.

## Doubts and open questions

- Article number of the published version (the reference list of `Bazgan2019MostVital` writes "7(1):4"): not in
  the Crossref record.
- Under the Unique Games Conjecture no constant factor is possible (Lee, ICALP 2017, DOI
  10.4230/LIPIcs.ICALP.2017.92; abstract read by a subagent on 2026-10-10, not cited).
