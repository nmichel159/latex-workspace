# Voleskova2026FacialDefect

| | |
|---|---|
| Paper | Volesková, S. (joint work with I. Fabrici): *Colorings of plane graphs with small facial defect*. Abstract of a talk, 61st Czech-Slovak Conference on Graph Theory, 1-5 June 2026. https://csgt2026.tuke.sk/pdfs/VOLESKOVA.pdf |
| Key | `Voleskova2026FacialDefect` |
| Reading status | full (one page), 2026-10-13 |
| Full text | `knowledge/sources/papers/Voleskova2026FacialDefect.pdf` |
| Topic | [../research/facial-defect-colorings.md](../research/facial-defect-colorings.md) |

## What the paper does

- Defines facially adjacent edges (adjacent and consecutive around their common end vertex), facially proper edge
  colorings and facially proper total colorings.
- Recalls Jendroľ's 3-coloring of the vertices in which, on each face, a monochromatic path has at most two
  vertices, and writes it as a `[2,2,2]`-vertex coloring.
- Announces: every plane graph has a `[1,2,2]`-edge coloring (no facially adjacent edges of color 1; on each face
  monochromatic paths of colors 2 and 3 have at most two edges) and a `[1,1,1,2,2]`-total coloring. No proofs.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| monochromatic path on a face | facial trail (trail reading) or facial path (path reading) | the abstract does not say whether three edges of a triangular face count |
| defect of a total coloring | type-wise reading | not defined in the abstract; TODO(verify) |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| every plane graph has a `[1,2,2]`-edge coloring | second paragraph | `poznamky-facial-defect`, Section 1 (the theorem whose list we try to lower) | "each plane graph"; multigraphs not mentioned |

## Difference from our work

The abstract proves the list `[1,2,2]`; the notes ask about `[1,1,2]`, find no counterexample by computer and give
a parity criterion for the third color class.

## Doubts and open questions

- No paper or preprint found (searches of 2026-10-13). Which cases the talk left open is unknown: TODO(verify).
