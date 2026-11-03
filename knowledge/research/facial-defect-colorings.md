# Facial defect colorings of plane graphs - topic map

Side topic opened 2026-10-13 from the abstract of S. Volesková (joint work with I. Fabrici), CSGT 2026
(`knowledge/sources/papers/Voleskova2026FacialDefect.pdf`). Project: `projects/poznamky-facial-defect`
(notes: `projects/poznamky-facial-defect.md`). Everything under "Our results" was produced by an AI assistant on
2026-10-13 and is unrefereed.

## 1. Definitions and notation (as in the notes)

| Term | Meaning |
|---|---|
| plane graph | connected, loops and multiple edges allowed (as in Jendroľ 2026) |
| corner | two consecutive edges of a boundary walk with the vertex between them; belongs to one vertex and one face |
| facially adjacent | two distinct edges that form a corner |
| facial trail / facial path | pairwise distinct consecutive edges of a boundary walk / a facial trail whose vertices are pairwise distinct |
| `[d_1,...,d_k]`-edge coloring | no facial trail with `d_i + 1` edges is monochromatic in color `i` (trail reading); path reading: only facial paths are forbidden for `d_i >= 2` |
| `[d_1,...,d_k]`-vertex coloring | no `d_i + 1` distinct consecutive vertices of a boundary walk are monochromatic in color `i` |
| admissible set `S` | `E \ S` has a facially proper 2-coloring (`S` can be the third class of a `[1,1,2]`-coloring if it is also trail-free) |
| trail-free | contains no facial trail with three edges |
| node, weight | element of `V` or `F`; number of its corners formed by two distinct edges (degree, face length) |
| `H_S` | graph on the nodes in which the ends and sides of every edge of `S` are pairwise adjacent |

The trail reading is stronger (every trail coloring is a path coloring); the readings differ on triangular faces
and on boundary walks that repeat a vertex. The abstract speaks of paths. TODO(verify) with the authors.

## 2. Known results (with sources)

| Statement | Source |
|---|---|
| every plane graph has a facially proper edge coloring with 4 colors; 3 do not suffice (wheel) | `Czap2019FacialRST`, p. 631 |
| every plane graph has a `[1,2,2]`-edge coloring and a `[1,1,1,2,2]`-total coloring | `Voleskova2026FacialDefect` (abstract, no proof) |
| every plane graph has a `[2,2,2]`-vertex coloring; `[1,1,1]` fails for 4-chromatic graphs | `Jendrol2026ThreeColoring`, Theorem 3; `Jendrol2026Corrigendum` |
| vertices, two colors: `[4,4]` holds, `[3,3]` is conjectured, `[2,2]` fails | `Czap2021FacialPaths`, Theorem 1, Conjecture 3, Theorem 4 |
| facial total-coloring: 6 colors suffice, 5 conjectured (proved for triangulations, outerplane, bipartite) | `Czap2019FacialRST`, Theorem 14, Conjecture 15 |

Open after these: `[1,1,2]`-edge; `[1,2,2]`- and `[1,1,2]`-vertex; `[1,1,1,1,2]`-total.

## 3. Our results (2026-10-13, unrefereed)

| Result | Where | Evidence |
|---|---|---|
| no graph without a `[1,1,2]`-edge coloring among all 3-connected plane graphs with at most 22 edges, all 77 274 plane multigraphs with at most 8 edges (9 and 10 edges: run unfinished on 2026-10-13), 2.8 million random graphs | notes, Proposition 2.1 | programs in `projects/poznamky-facial-defect.submission/checks/` |
| the same for `[1,1,2]`-vertex colorings; facial total 5-colorings exist on the 3-connected graphs with at most 22 edges | notes, Proposition 2.1 | same |
| parity criterion: `S` is admissible iff every component of `H_S` has even total weight | notes, Theorem 3.1 | proof; program test on all subsets of all multigraphs with at most 7 edges |
| product construction: for `sigma: V -> {0,1}`, `tau: F -> {0,1}` the edges bichromatic in both can be 2-colored facially properly | notes, Proposition 3.2 | proof |
| quadrangulations (2-edge-connected, all faces of length four) have `[1,1,2]`-edge colorings | notes, Corollary 3.3 | proof (unfriendly partition of the faces) |
| reduction: adding a deleted or contracted edge to an admissible set keeps it admissible; a smallest counterexample has no vertex of degree one and no face of length one | notes, Proposition 3.4 | proof |
| two colors, edges: `[2,2]` and `[1,3]` fail (smallest 3-connected examples: 15 edges in the trail reading; 21 and 18 edges in the path reading); `[2,3]`, `[3,3]`, `[1,4]` no failure found | notes, Table 1, Proposition 4.1 | two programs |

## 4. Proof ideas for the conjecture "every plane graph has a `[1,1,2]`-edge coloring"

- **Monotone and exact.** Admissible sets form an up-set; by the criterion the task is: a trail-free set that
  joins the nodes of odd weight in groups of even size. A set whose `H_S` has one component containing all odd
  nodes is admissible.
- **Sufficient forms** (all checked on small graphs): the complement of a forest `N` that meets every facial
  3-trail and leaves no odd vertex with all its edges in `N`; `J_V` union `J_F` for a join of the odd vertices and
  a dual join of the odd faces (this is the product construction).
- **Exchange argument.** In an inclusion-minimal admissible set, the middle edge `y` of a facial 3-trail on a
  face `f` is the only link between its other face `g` and the rest; `y` can be replaced by either neighbor of
  `y` on `g`, or by any edge joining the two parts. A potential function that makes the exchange terminate is
  missing.
- **4-coloring form.** A facially proper 4-edge-coloring in which two colors never alternate `XYX` on a face
  gives a `[1,1,2]`-coloring (merge the two). Such a coloring exists for every plane multigraph with at most
  8 edges (`checks/logs/hyp2_m8.log`). Equivalent: a trail-free `S` with both `S` and `E \ S` admissible.
- **No forced edge.** In every plane multigraph with at most 8 edges every edge is in the third class of some
  `[1,1,2]`-coloring and outside it in another (same log); a counterexample built from gadgets would need forced
  edges.
- **Limits.** The product construction fails for the theta graph with three paths of three edges and, for
  3-connected graphs (where it holds up to 22 edges), would give a 2-coloring of the vertices without a
  monochromatic facial 3-trail, a case of Conjecture 3 of `Czap2021FacialPaths`.

## 5. Glossary

| EN | SK |
|---|---|
| facially adjacent edges | faciálne susedné hrany |
| facial defect | faciálny defekt |
| facially proper coloring | faciálne vlastné zafarbenie |
