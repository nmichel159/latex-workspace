# Computational checks of article 1 (2026-10-10)

Brute-force checks of the statements of Sections 2-5 of `projects/clanok-1-min-cut-path/main.tex`.
Python 3.13 with networkx 3.6; run from this folder. Nothing here is sent with the manuscript.

| File | What it does | Run time |
|---|---|---|
| `reduction.py` | executable model of Algorithm 1: `BuildChain`, labelling of the links, `Thread` (threading of Definition 3.4, connecting paths of one edge), `Calibrate`; the free choices (which free edge is subdivided, direction through a crossing edge) are random with a seed | - |
| `check_reduction.py` | Definitions 3.2-3.3, degree facts, counts, Lemmas 3.5-3.8 with items (a), (b) and Table 1, Theorem 3.9 | `--quick` 30 s; full run 13 min |
| `mutation_tests.py` | five broken constructions; each must be caught by a check | 1 s |
| `check_cutpath.py` | Lemma 2.3, minimum cuts are edge boundaries, Theorem 3.10, Lemmas 4.3-4.4, Theorem 4.5, Remark 4.6, Lemma 5.1, Theorem 5.2, the two counterexamples of the class "d <= 2 or c <= 2" | 10 s |
| `results-reduction.txt`, `results-cutpath.txt` | output of the runs of 2026-10-10 | - |

## Results

No check failed.

- **Reduction** (`results-reduction.txt`): 5639 formulas, 5580 satisfiable, 59 unsatisfiable. All formulas with one
  variable and up to three clauses, with two variables and up to two clauses (repeated variables in a clause allowed),
  with three variables and up to two clauses, all multisets of three clauses on three variables, the eight sign
  patterns on three variables (unsatisfiable) and each seven of them, and 540 random formulas with up to six
  variables and 18 clauses. For the smallest families all shortest `u`-`v` paths of `G` were enumerated
  independently and the connectivity of `G - P` was tested for every chain path `P`.
- **Exact sizes** (checked on every instance): `2n + 3m` chain links, `2n + 7m` threads, `4n + 21m` crossing edges,
  `6n + 28m` connecting paths, `Lambda = 10n + 33m + 1`, `18n + 63m + 1` chain edges,
  `|E| = 18n + 63m + 1 + (6n + 28m) Lambda`; balancing adds `6m` edges (two per literal chain link). Inner vertices of
  connecting paths have degree two, ends of crossing edges degree three, every vertex other than `u`, `v` degree at
  most three.
- **The construction does not need three distinct variables in a clause**: the checks pass for clauses such as
  `(x_1 or x_1 or not x_1)`.
- **Small graphs** (`results-cutpath.txt`): all 1251 graphs with 2 to 7 vertices (22590 connected pairs), 60 random
  graphs of diameter two on 8 vertices, 200 random cactus graphs on 8 to 12 vertices. On graphs with at most six
  vertices `cp(u,v)` was also computed from Definition 2.1 over all edge subsets; the two computations agree.
- **Class "d <= 2 or c <= 2 for every pair"**: the two parked counterexamples are the only graphs with at most six
  vertices in which `cp = c + d - 1` fails; 22 graphs with seven vertices fail as well.

## Method notes

- A chain path that shares no edge with a thread is not separating, because the thread is a `u`-`v` path that avoids
  it. This is the only fact used to skip a connectivity test (and for chains with at most 12 links the test is run for
  every chain path anyway).
- Connectivity of `G - P` is tested on the full graph and on the graph whose connecting paths have one edge; the two
  agree on every instance (inner vertices of connecting paths have degree two).
- `cp(u,v) = min |P| + |B - P|` over simple `u`-`v` paths `P` and edge boundaries `B` of vertex sets with `u` inside
  and `v` outside; it is compared with the literal definition on all graphs with at most six vertices.
