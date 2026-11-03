# Czap2021FacialPaths

| | |
|---|---|
| Paper | Czap, J., Fabrici, I., Jendroľ, S.: *Colorings of plane graphs without long monochromatic facial paths*. Discussiones Mathematicae Graph Theory 41, 2021, 801-808. DOI 10.7151/dmgt.2319 |
| Key | `Czap2021FacialPaths` |
| Reading status | full, publisher's PDF, 2026-10-13 |
| Full text | - (open access at the DOI) |
| Topic | [../research/facial-defect-colorings.md](../research/facial-defect-colorings.md) |

## What the paper does

- Setting: simple connected plane graphs; a facial path is a subpath of a boundary walk; `P_k` has `k` vertices.
- Theorem 1 (p. 803): every plane graph has a 2-coloring without monochromatic facial 5-paths (add diagonals in
  the faces, 4-color, merge color pairs). Theorem 2: 2-connected plane graphs without 5-faces have a 2-coloring
  without monochromatic facial 4-paths. Conjecture 3: every plane graph has one.
- Theorem 4 (p. 804): infinitely many plane graphs in which every 2-coloring has a monochromatic facial 3-path
  (a configuration of six vertices, Figure 2).
- Theorem 5: every plane graph has a 3-coloring without monochromatic facial 4-paths (via 1-planar graphs and six
  colors). Conjecture 6: without monochromatic facial 3-paths (proved in `Jendrol2026ThreeColoring`).
- Section 3: list versions (Theorem 7, Conjecture 8).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| 2-coloring without monochromatic facial `(k+1)`-paths | `[k,k]`-vertex coloring | vertices, not edges |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| `[4,4]` holds, `[3,3]` conjectured, `[2,2]` fails (vertices) | Theorem 1, Conjecture 3, Theorem 4 | `poznamky-facial-defect`, Section 4 (comparison with the edge version) | simple connected plane graphs |

## Difference from our work

The paper treats vertex colorings; the notes give the first data on two-color edge colorings with facial defect
(`[2,2]` and `[1,3]` fail) and found no published statement on them (searches of 2026-10-13).

## Doubts and open questions

- Our computer search agrees with the paper: no 3-connected plane graph with at most 22 edges lacks a `[3,3]`-
  or `[2,3]`-vertex coloring; the smallest without a `[2,2]`-vertex coloring has 15 edges.
