# Checks of the notes on facial defect colorings

Programs written on 2026-10-13 by an AI assistant; results in `logs/`. Nothing here is sent.

A plane graph is a rotation system: edge `i` has the darts `2i` and `2i+1`, `sigma[d]` is the next dart around
the origin of `d`, the boundary walk continues with `sigma[d ^ 1]`. Edge variants: `W` = trail reading,
`P` = path reading (see the notes, Section 1). Lists are written `E[...]`, `V[...]`, `T[...]` for edge, vertex
and total colorings.

| File | Does | Run |
|---|---|---|
| `pm.js` | library: faces, canonical code (up to reflection), generation steps, constraint solver (backtracking with unit propagation), edge, vertex and total colorings | - |
| `allmaps.js` | all connected plane multigraphs with at most `m` edges; counts the graphs without each coloring | `node --max-old-space-size=12000 allmaps.js 10 9` |
| `poly.js` | all 3-connected plane graphs with at most `m` edges (wheels, edge additions, vertex splits) | `node poly.js 22 full` (all lists), `node poly.js 22 main` |
| `product.js` | product construction (Proposition 3.2) with a trail-free complement | `node product.js poly 22`, `node product.js maps 10` |
| `rand.js` | random plane graphs | `node rand.js <seed> <count> <mmin> <mmax> simple|multi` |
| `hyp.js` | parity criterion (Theorem 3.1) against bipartiteness for every subset `S`; forest and product constructions | `node hyp.js 7 W` |
| `hyp2.js` | 4-coloring form, forced edges, product construction on all multigraphs | `node hyp2.js 8` |
| `planemap.py`, `crosscheck.py` | second implementation (Python) and its counts | `python crosscheck.py 8` |
| `verify_examples.py`, `examples.json` | the example graphs of the notes, checked by the Python implementation | `python verify_examples.py examples.json` |
| `draw.py` | barycentric coordinates of a 3-connected example (start of the figure) | `python draw.py examples.json C21` |

## Results (logs)

| Log | Content |
|---|---|
| `poly22_full.log` | 693 855 3-connected plane graphs with 6 to 22 edges, all lists: no graph without `E[1,1,2]`, `E[1,2,2]`, `E[2,3]`, `E[3,3]`, `E[1,4]`, `V[1,1,2]`, `V[1,2,2]`, `V[2,2,2]`, `V[2,3]`, `V[3,3]`, `V[1,4]`, `T[1,1,1,1,1]`; smallest failures: `E[1,1,1]` 8, `E[1,2]` 8 (W) and 11 (P), `E[2,2]` 15 (W) and 21 (P), `E[1,3]` 15 (W) and 18 (P), `V[2,2]` 15, `V[1,3]` 17 |
| `poly22_main.log`, `poly19_full.log` | earlier runs with the example graphs (lines `EX`) |
| `allmaps10.log` | all 4 897 492 plane multigraphs with at most 10 edges; **written by a watcher when the run ends; `allmaps10.partial.log` is the state when the session stopped** |
| `allmaps8.log` | all 77 274 plane multigraphs with at most 8 edges, all lists, both readings: the only failures are `E[1,1]`, `E[1,1,1]` (from 4 edges), `E[1,2]` (W from 5, P from 6), `V[1,1,1]` (from 6), `E[1,3]` W (one graph with 8 edges); the counts equal those of the Python program |
| `crosscheck_python_m7.log` | Python counts for at most 7 edges (a run to 8 edges gave `E[1,1,1]` 839, `E[1,2]` W 3384, P 226, `V[1,1,1]` 38, `E[1,3]` W 1, nothing else) |
| `product_poly22.log`, `product_maps10.log` | product construction: exists for every 3-connected graph with at most 22 edges; among 2-edge-connected loopless multigraphs it fails for one graph with 9 edges (theta graph with three paths of three edges) and one with 10 |
| `rand_*.log` | 1.6 million simple and 1.2 million general random plane graphs: no failure of `E[1,1,2]` W, `V[1,1,2]`, `V[1,2,2]`, `E[2,3]` W, `E[3,3]` W, `V[3,3]`, `V[2,3]`, `T[1,1,1,1,2]` W |
| `hyp_parity_m7.log` | parity criterion: 0 mismatches over all subsets of all multigraphs with at most 7 edges |
| `hyp2_m8.log` | at most 8 edges: the 4-coloring form always holds; no edge is forced into or out of the third class |
| `verify_examples.log` | Python check of the examples (`A15`, `B15`, `C21`, `D18`, `V15`, `V17`, wheels); `C21` and `D18` are Figure 1 (a) and (b) |

The numbers of graphs per edge count agree with OEIS A006385 (plane multigraphs up to reflection) and A002840
(polyhedral graphs).
