# Jendrol2026ThreeColoring

| | |
|---|---|
| Paper | Jendroľ, S.: *On a 3-coloring of plane graphs without monochromatic facial 3-paths*. Discussiones Mathematicae Graph Theory 46(2), 2026, 341-351. DOI 10.7151/dmgt.2584. Corrigendum: same journal 46, 2026, 353-355, DOI 10.7151/dmgt.2602 (`Jendrol2026Corrigendum`) |
| Key | `Jendrol2026ThreeColoring` |
| Reading status | publisher's PDF 2026-10-13: Sections 1-3 and the end of the proof in full, the claims of the proof skimmed; corrigendum: abstract, Sections 1-2 |
| Full text | - (open access at the DOI) |
| Topic | [../research/facial-defect-colorings.md](../research/facial-defect-colorings.md) |

## What the paper does

- Theorem 3 (p. 343): every plane graph has a 3-coloring of the vertices in which every monochromatic facial path
  has at most two vertices; "the bound 2 is optimal for 4-chromatic plane graphs". This proves Conjecture 6 of
  `Czap2021FacialPaths`.
- Setting (p. 341): connected plane graphs, loops and multiple edges allowed. A facial path is a path that is a
  consecutive part of the boundary walk of a face; two edges are facially adjacent if they are adjacent and
  consecutive on a boundary walk (p. 342).
- Method: minimal counterexample, reducible configurations, Lebesgue's theorem on normal plane maps.
- Corrigendum: Claim 10 ("no 3-vertex") was wrong; it is replaced by "every 3-vertex lies in a separating
  4-cycle" and the end of the proof is rewritten.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| 3-coloring without monochromatic facial 3-paths | `[2,2,2]`-vertex coloring | the list notation is from `Voleskova2026FacialDefect` |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| `[2,2,2]`-vertex coloring exists | Theorem 3, p. 343 | `poznamky-facial-defect`, Section 1 | every connected plane graph, loops and multiple edges allowed |

## Difference from our work

The paper settles three colors with defect two for vertices; the notes test the lists `[1,2,2]` and `[1,1,2]` for
vertices by computer (no counterexample) and study the edge version.

## Doubts and open questions

- "Optimal" refers to the list `[1,1,1]` only; the lists `[1,2,2]` and `[1,1,2]` are not discussed.
