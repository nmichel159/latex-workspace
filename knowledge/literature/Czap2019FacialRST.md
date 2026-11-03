# Czap2019FacialRST

| | |
|---|---|
| Paper | Czap, J., Jendroľ, S., Šugerek, P., Valiska, J.: *Facial [r,s,t]-colorings of plane graphs*. Discussiones Mathematicae Graph Theory 39, 2019, 629-645. DOI 10.7151/dmgt.2135 |
| Key | `Czap2019FacialRST` |
| Reading status | parts, publisher's PDF, 2026-10-13: abstract, Section 1 (pp. 629-631), Section 4.1, reference list |
| Full text | - (open access at the DOI) |
| Topic | [../research/facial-defect-colorings.md](../research/facial-defect-colorings.md) |

## What the paper does

- Facial `[r,s,t]`-colorings of vertices and edges: adjacent vertices differ by at least `r`, facially adjacent
  edges by at least `s`, incident vertex and edge by at least `t`. Main bound `3r + 3s + t + 1` colors.
- Background stated in Section 1 (p. 631): a facial `[0,1,0]`-coloring is a facial edge-coloring; Tait observed
  that the Four Color Problem is equivalent to the facial 3-edge-colorability of plane triangulations and of
  cubic bridgeless plane graphs; every plane graph has a facial edge-coloring with at most four colors (their
  reference [9], Fabrici, Jendroľ, Vrbjarová, Discrete Appl. Math. 185 (2015)); "the bound four is tight", seen
  on the wheel on six vertices.
- Section 4.1: facial `[1,1,1]`-colorings are the facial total-colorings of Fabrici, Jendroľ and Voigt (their
  reference [11], Discrete Math. 339 (2016) 2826-2831); Theorem 14: at most six colors; Conjecture 15 (from
  Fabrici, Jendroľ, Vrbjarová, Discrete Math. 339 (2016) 626-631): five colors; proved for triangulations,
  outerplane graphs and bipartite plane graphs.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| facial edge-coloring | `[1,...,1]`-edge coloring | |
| facial total-coloring with `k` colors | type-wise total coloring with the list `[1,...,1]` | |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| four colors suffice for a facial edge-coloring, three do not; Tait's equivalence | p. 631 | `poznamky-facial-defect`, Sections 1 and 3 | plane graphs |
| facial total-coloring: six colors (theorem), five (conjecture) | Theorem 14, Conjecture 15 | `poznamky-facial-defect`, Section 1 | plane graphs |

## Difference from our work

The paper bounds numbers of colors for proper facial colorings; the notes fix three colors and relax one of them.

## Doubts and open questions

- The cited originals (their references [9], [10], [11]) were not opened; the notes cite this paper for their
  statements. Our search found the wheel with four spokes (8 edges) already without a facial 3-edge-coloring.
