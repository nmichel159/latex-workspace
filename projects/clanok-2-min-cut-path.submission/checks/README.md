# Computational checks of article 2 (2026-10-12)

Brute-force and randomized checks of the blueprint S0-S15 (`../SPEC.md`, Section 5) and of the statements, examples
and graphs of the math core (`../drafts/core.tex`, `../drafts/core-notes.md`), plus a reference implementation of the
linear-time algorithm (S11) that uses no brute force. Python 3.13 with networkx 3.6 (graph atlas, class tests, one
independent cross-check); 24 worker processes by default (`--jobs`). Run from this folder, preferably with
`python -B` (no bytecode). Nothing here is sent with the manuscript.

Nothing failed except one claim of the notes (observation 8, see "Failures"). Every statement S0-S15 that the
blueprint makes holds on everything tested.

## Files

| File | What it does | Run time |
|---|---|---|
| `mcp.py` | shared library: graphs, BFS, max-flow, simple paths, three independent computations of `cp` (`cp_brute`: min over simple paths `P` of `\|P\|` + edge connectivity of `G - P`, with an optimal cut-path; `cp_subsets`: article 1's method; `cp_definition`: the definition read literally), `in_dc`, brute-force `F`, orientation, pieces, squares, links, terminals, general paths (`Decomp`), generation of all connected graphs with 2-8 vertices (atlas up to 7, vertex extension for 8, count checked: 11117) | - |
| `check_structure.py` | S0-S10 and S15, each statement as its own counted assertion; also S11 residual lemma, S14 and the statements of `core.tex` in their written form | 3 min (`--maxn 8 --chains 4500 --general 6000`) |
| `algorithm.py` | the algorithm of S11 (two augmentations, residual digraph, strong components, `F`, pieces, `\vec G`, `lambda`, the tests `l = 1`, `l = 2`); no brute force; returns `cp` and a minimum cut-path | - |
| `check_algorithm.py` | `algorithm.py` against brute force: all graphs with 2-8 vertices, long random chains in DC, graphs outside DC (report), coarser decompositions | 15 s |
| `check_robust.py` | `algorithm.solve_robust`, the referee's version without the promise "G in DC" (value, certificate, `p_1`, `p_2` from the flow), five claims plus seven mutation tests; results in `results-robust.txt` | 15 s |
| `check_hardness_padding.py` | S12: the padding `u'`, `s_1`, `s_2`; both cases `c_G(u,v) >= 3` and `c_G(u,v) = 2`; instances of article 1's reduction | 3 s |
| `check_class.py` | S13 and the preliminaries of `core.tex` (`PRE-...`): Corollary 3.12 of article 1, easy pairs, the lemma on minimum cuts, parity, uncrossing, bridges, open pairs | 10 s |
| `explore_open_cases.py` | data for the later phase (no assertions): pairs `d = 2`, `c >= 3`; graphs of diameter three | 3 s |
| `verify_named_graphs.py` | the two counterexamples of the research map, every example of `core.tex`, every graph of `core-notes.md` Section 4, with all quantities printed in the labels of the graph | 2 s |
| `mutation_tests.py` | 18 deliberately broken statements; each must make the check fail | 70 s |
| `time_algorithm.py` | running time of `algorithm.py` on chains of up to 32000 squares (a fresh process per size) | 20 s |
| `chains.py` | generator of random instances with long decompositions (`random_dc_chain`, `random_general_chain`) | - |
| `results-structure.txt`, `-algorithm`, `-robust`, `-hardness-padding`, `-class`, `-open-cases`, `-named-graphs`, `-mutations`, `-timing` | outputs of the final runs of 2026-10-12 | - |

Commands (all from this folder): `python -B check_structure.py --maxn 8 --chains 4500 --general 6000`,
`python -B check_algorithm.py`, `python -B check_robust.py`, `python -B check_hardness_padding.py --maxn 7`, `python -B check_class.py --maxn 8`,
`python -B explore_open_cases.py --maxn 8`, `python -B verify_named_graphs.py`, `python -B mutation_tests.py`,
`python -B time_algorithm.py`. The graphs with 8 vertices are generated once and cached in `tmp/clanok-2-checks/`.

## What is tested, and the result

"Small graphs" = all 12112 connected graphs with 2-8 vertices (1, 2, 6, 21, 112, 853, 11117), all ordered pairs
(662244). "Chains" = random graphs with a long decomposition (`chains.py`), described below. `c = 2` pairs: 181892 on the
small graphs. All counts are in the `results-*.txt` files; the table gives the counts of assertions.

| Statement | Assertion names | Small graphs | Chains in DC (2953 instances, 2.7M paths) | Result |
|---|---|---|---|---|
| S0 `c = 1` or `d = 1` gives `cp = c + d - 1`; in DC a pair with `d >= 3` has `c <= 2`; bridges: `K`, `d`, `c`, `cp` | `S0a`, `S0b`, `S0c-*` | 410756; 47064; 59182 pairs with a bridge | - | PASS |
| S1 `F` within `E(p_1) u E(p_2)`, one edge on each | `S1a`, `S1b` | 9444742 pairs of edge-disjoint paths each | 135347 | PASS |
| S2 orientation well defined, agrees with `p_1`, `p_2`; each path meets each minimum cut once and traverses `F` tail to head | `S2a`-`S2d` | 181892; 9444742; 4819642 paths each | 2668744 paths | PASS |
| S3 `F`-edges join different pieces; a path visits a piece in one block | `S3a`, `S3b` | 181892; 4819642 | 2668744 | PASS |
| S4 degrees of pieces | `S4a`-`S4c` | 181892 each | 2953 | PASS |
| S5 entering/leaving edges of a square form a minimum cut; common order of the squares; the two general paths; a path uses exactly one completely | `S5o`, `S5a`-`S5e` | 207624 (`S5a`, `S5b`); 4819642 (`S5c`); 207624 (`S5d`) + cover 181892; 5236968 (`S5e`) | 11340; 2668744; 11340 + cover 2953; 13281684 | PASS |
| S6 distinct terminals of a square have `c >= 3` | `S6` | 381786 pairs of terminals | 14317 | PASS |
| S7 separation criterion (`alpha_i`, `beta_i`) | `S7pre`, `S7` | 4819642 paths (190272 separate `u` from `v`) | 2668744 (1161225 separate) | PASS |
| S8 paths of `G` = directed paths of `\vec G`; length formula with `lambda`; trace exactly `p` | `S8a`-`S8d` | 181892; 5192374 triples `(g, p, h)` each | 86176 triples | PASS |
| S9 `cp = d` iff a square has a path `p` with count `= d` that separates `alpha`, `beta`; else `cp = d + 1` | `S9a`, `S9b` | 181892 (282 with `cp = d`) | 2953 (364 with `cp = d`) | PASS |
| S9 in the form of `core.tex` (G-distances `d(u,x) + \|p\| + d(y,v) = d(u,v)`, terminal pairs) | `S9-core` | 181892 | 2953 | PASS |
| S10 witness `p` has `\|p\| = d(x,y) <= 2` in DC; shortest paths have at most two edges per square | `S10`, `S10-core-p`, `S10-core-shortest` | 282; 176550; 176550 | 406; 2953; 2953 | PASS |
| S11 `F` = path edges whose ends lie in different strong components of the residual digraph | `S11-res-i`, `S11-res-ii`; `ALG-F`, `ALG-tail`, `ALG-pieces`, `ALG-scc` | 1004700; 1004700; 176550 each | 139; 16215; 2983 each | PASS |
| S11 value and cut-path of `algorithm.py` | `ALG-value`, `ALG-cutpath` | 258424 pairs with `c <= 2` (all DC: 11575 graphs) | 2983 instances (369 `cp = d`, 2614 `cp = d + 1`) | PASS |
| S12 padding | `S12-*` | 32094 pairs (`c >= 2`), graphs with 2-7 vertices; 4 instances of article 1 | - | PASS |
| S13 class | `S13-*` | 12112 graphs | - | PASS |
| S14 coarser decompositions: S7, S9 on `F'` = union of some minimum cuts; the algorithm on them | `S14-*`, `ALG-coarse` | 226160 decompositions | 20170 | PASS |
| S15 open pairs `d = 2`, `c >= 3`; and the proposition for all pairs (`PRE-open-pairs`) | `S15a`-`S15c` | 131186 pairs (800 with `cp = c`) | - | PASS |

Notes on the table.
- All graphs with at most 7 vertices lie in DC (a pair with `d >= 3` and `c >= 3` needs degree 3 at both ends and
  disjoint neighborhoods, hence 8 vertices). The first graphs outside DC have 8 vertices: 537 of the 11117, 536 of
  them of diameter three. So the class is vacuous below 8 vertices; the chains (up to 40 vertices) and the 537
  graphs carry the class-specific statements.
- Outside DC the structure statements S1-S9 were tested as well (they are claimed for every graph with `c = 2`):
  2401 random instances (2105 checked, the others have more than 20000 paths), 2.9M paths, no failure. S10 is not claimed there; in 61 of
  the 132 pairs with `cp = d` of these instances every witness `p` has at least three edges.
- `cp = d` is rare on small graphs (282 of 181892 pairs with `c = 2`), which is why `chains.py` was tuned to the
  pattern of the six-vertex example (entering and leaving terminals of a square are the same two vertices): 12 % of
  the chain instances have `cp = d` (364 of 2953), 88 % have `cp = d + 1`.
- `algorithm.py`: value and cut-path agree with brute force on all 258424 pairs with `c <= 2` of the 11575 small
  graphs in DC (and on all 5342 pairs with `c = 2` of the 537 small graphs outside DC), on 2983 chain instances in DC
  (decompositions with `k = 3 ... 10` squares, up to 40 vertices, mean 26), and refuses all 373748 pairs with `c >= 3`
  of the small graphs in DC (three augmentations). The returned set always contains a `u`-`v` path and a `u`-`v` cut and has `cp` edges.

### The algorithm outside DC

The proof in `core.tex` uses the class only through the condition (*): every entering terminal of every square is at
distance at most two from every leaving terminal of the same square. Tested: whenever (*) holds the value is right
(`ALG-star`: 176550 pairs in DC, 4108 pairs in the 537 graphs outside DC, 394 pairs in 4789 random instances outside
DC; also for coarser decompositions, `ALG-coarse`: 26145 decompositions). It does fail when (*) fails: on 111 of
4789 random instances outside DC (2.3 %, 38 % of those with `cp = d`), always by returning `d + 1` where `cp = d`;
531 of 36482 coarser decompositions. Deterministic family (`crossed_path_instance(k)`, `k >= 3`): `u` is joined to `x`
by an edge and to `y` by a path with `k + 1` edges, `v` to `y` by an edge and to `x` by a path with `k + 1` edges,
and `x`, `y` by a path with `k` edges; `3k + 3` vertices (12 for `k = 3`), `c = 2`, `d = k + 2 = cp`, the pair
`(x, y)` has `c = 3` and `d = k`, so the graph is outside DC, and the algorithm returns `d + 1`. The smallest random
failure has 13 vertices. All 537 graphs with 8 vertices outside DC are handled correctly, so the class is needed only
from some size between 9 and 12 vertices on.

### The version without the promise (`algorithm.solve_robust`, `check_robust.py`, `results-robust.txt`)

The referee's version works for every connected graph and every pair with `c(u,v) = 2`. For every square and every pair
of an entering terminal `x` and a leaving terminal `y`, `x != y`, it computes `l = d(u,v) - d(u,x) - d(y,v)` (distances
in `G`). If `l = 1` it tests the edge `xy`, if `l = 2` the at most four paths `x, w, y` through the neighbors of `x` or `y` on a
fixed `alpha`-`beta` path `q` (only if `alpha != beta`); a tested path that separates `alpha` from `beta` in the square
is returned as `R_x u p u R_y` with value `d` (outcome "path"). If `l >= 3` the pair `(x, y)` is recorded
(whether or not `alpha = beta`). If nothing was returned the value is `d + 1` with `R u C`, with the recorded pair as a
certificate if there is one (outcome "certificate"), else without (outcome "value"). `p_1`, `p_2` are found by two
searches in the digraph of the flow-carrying edges, `D` is the residual digraph of the flow along `p_1`, `p_2` only
(so a cycle in the net flow is harmless), `F` = edges of `p_1 u p_2` with ends in different strong components of `D`.

Instances: the 12112 graphs with at most 8 vertices (181892 ordered pairs with `c = 2`; for graphs with at most 7
vertices also 26700 runs on random flows of value two as input, a third of them with a cycle), 2983 chains in DC,
4789 random instances outside DC, `crossed_path_instance(3..8)`: 216370 runs of the algorithm. Result, 1758504
assertions, none failed:

| Claim | Assertion | Count | Result |
|---|---|---|---|
| 1. a returned path is a cut-path with `d = cp` edges | `R1` | 883 (all outcomes "path": 278 + 4 small graphs, 369 chains, 180 outside DC, 52 with random flows) | PASS |
| 2. no pair recorded: the value equals `cp`; in the case "value" the returned set is a cut-path with `d + 1` edges | `R2`, `R2c` | 216198; 215315 | PASS |
| 3. every pair with `l >= 3` has `d(x,y) >= 3` and `c(x,y) >= 3`; no pair for `G` in DC | `R3a`, `R3b`, `R3c` | 193 pairs (all pairs with `l >= 3`, not only the first); 206233 pairs in DC, none recorded; 172 certificates, all outside DC | PASS |
| 4. pair recorded, no path: the returned set is a cut-path with `d + 1` edges | `R4` | 172 certificates (166 in the random instances outside DC, 6 in the crossed family, none in the 537 small graphs outside DC) | PASS |
| 5. `p_1`, `p_2` from two searches in the flow digraph are edge-disjoint `u`-`v` paths along the flow | `R5` | 253858, of which 25837 on flows with a cycle (9037 flows for `c = 2`, 16800 for pairs with `c >= 3`; the two augmentations of the algorithm itself never produced a cycle) | PASS |

Claim 4, how often the certified value `d + 1` is wrong (`cp = d`): in the random instances outside DC 111 of 166
certificates (66.9 %), the other 55 have `cp = d + 1`; in the crossed family 6 of 6; none occur elsewhere. So a
certificate means "G is not in the class and the value `d + 1` may be wrong"; in the 111 instances the old
`solve` was wrong exactly there, and `solve_robust` flags them. Consistency checks: `R-F` (`F` and orientation from
`p_1`, `p_2` and `D` equal the brute-force ones, 216370), `R6` (stopping at the first path gives the same outcome and
value as the exhaustive scan, 216370), `R0` (applies to every pair with `c = 2`, every square has two entering and two
leaving edges).

Mutation tests (graphs with at most 7 vertices, 600 chains, 1500 instances outside DC, crossed family): all seven
detected. Record the pair only if `l >= 4`: `R2` fails (17; smallest the 12-vertex crossed instance with `d = cp = 5`,
value 6 returned without a pair). Never record a pair (the certificate dropped): `R2` (23). Record already if `l >= 2`:
`R3a` (533; a pair with `d = 2`, `c = 3` on 7 vertices) and `R3b`, `R3c`. Skip the test `l = 2`: `R2` (9; 7 vertices).
Accept `l = 1` without the separation test: `R1` (5063). Return the shortest path without the cut: `R2c` (14223) and `R4`.
Second search does not remove the arcs of the first path: `R5` (78527).

### Running time (`results-timing.txt`)

Chains of `k = 500 ... 32000` squares (3360 to 218118 vertices, up to 325117 edges), worst case (every square
examined), garbage collector off, a fresh process per size: 1.8-2.0 microseconds per vertex and edge in the final run
(1.0-1.4 in an earlier run on a less loaded machine; the absolute value depends on the load), exponent 1.01
between the smallest and the largest instance. Timing within one long-lived Python process drifted by a factor of three
with the state of the memory allocator and with the garbage collector (first attempt), and bit masks of edge sets
(big integers) made the first version quadratic: `algorithm.py` therefore uses Boolean lists and sets. This is
empirical evidence for the claim, not a proof.

## Mutation tests (`results-mutations.txt`)

Each check was run once with the tested statement broken on purpose, on all graphs with 2-7 vertices plus 600
chains; every mutation was detected (18 of 18).

| Mutation | Detected by | Failing assertions |
|---|---|---|
| order of the squares reversed | `S5c` | 403683 of 403683 |
| an entering and a leaving edge of one square taken as the minimum cut | `S5a` | 3440 of 17170 |
| a path claimed to use the `F`-edges of both general paths | `S5e` | 1485562 of 1485562 |
| `c >= 3` claimed for any two vertices of a square | `S6` | 71253 of 153972 |
| `c >= 4` claimed for distinct terminals | `S6` | 15192 of 24173 |
| `(x_i, y_i)` instead of `(alpha_i, beta_i)` in S7 | `S7` | 44356 of 403683 |
| length condition dropped from S9 / separation condition dropped from S9 | `S9a` | 3572 of 13730 / 13658 of 13730 |
| length formula of S8 off by one | `S8b` | 186302 of 186302 |
| orientation of `F` reversed | `S2d` | 403683 of 403683 |
| condition (i) of the theorem of `core.tex` dropped | `S9-core` | 3572 of 13730 |
| residual digraph: arcs of the path edges flipped / path edges keep both arcs | `S11-res-i` / `S11-res-ii` | 64564 of 64564 / 66604 of 66604 |
| algorithm: never test `l = 2` / `l = 1` accepted without the separation test / never test `l = 1` / `lambda^+` for `lambda^-` / first square only | `ALG-value` | 8 / 10362 / 64 / 115 / 70 of 21335 pairs |

A finding from the mutation tests: flipping all path arcs of the residual digraph cannot be seen by statement (ii)
of the residual lemma (reversing every arc of a digraph does not change its strong components), only by (i); (ii)
is therefore independent of the direction convention.

## Failures

**Observation 8 of `core-notes.md` ("in the class, a separating trace has at most three distinct terminals") is
false.** Assertion `OBS8-terminals` fails on 3 of 406 witnesses of the chain instances in DC (`results-structure.txt`;
the other half of the observation, `OBS8-distance`, holds: `d(alpha, beta) <= 2` in all 406). The observation holds
on all 12112 graphs with at most 8 vertices (282 witnesses, one per pair with `cp = d`) and on every chain witness
except these three.
Minimal counterexample found by greedy deletion (21 vertices, 25 edges; it is the output of a search, not a proof
of minimality; two independent computations, `mcp.py` and networkx, agree on every quantity):

- vertices `0, ..., 20`, edges `01 02 1-13 2-13 2-14 2-15 34 39 4-15 5-14 5-16 68 6-10 6-18 79 7-10 7-19 89 8-10
  10-11 11-12 12-20 16-17 17-18 19-20`, `u = 1`, `v = 11` (written with hyphens where a name has two digits);
- `d(u,v) = 9`, `c(u,v) = 2`, `cp(u,v) = 9`, the graph is in DC (no pair with `d >= 3` and `c >= 3`);
- exactly two shortest paths separate: `1,0,2,15,4,3,9,7,10,11` and `1,13,2,15,4,3,9,7,10,11`;
- the third square is `{6, 7, 8, 9, 10}` with the edges `68 6-10 79 7-10 89 8-10`; entering edges end in `9`
  and `6`, leaving edges start in `7` and `10`; the trace of both paths is `p = 9, 7, 10`, so `x = 9`, `y = 10`,
  `alpha = 6`, `beta = 7`: four distinct terminals; `beta = 7` has degree two in the square and lies on `p`;
  `d(alpha, beta) = 2`.

The statement `core.tex` makes (Theorem "Separating shortest paths" and Corollary "two edges") is not affected: only
the "observation for the later phase" in `core-notes.md`, Section 8, doubt 8. The graph is in `results-named-graphs.txt`.

Nothing else failed. In particular no counterexample to any of S0-S15 or to any statement, example or graph of
`core.tex` and `core-notes.md` that I could test (see below).

## The math core (`drafts/core.tex`, `drafts/core-notes.md`)

- Every graph and value of the five examples of `core.tex` (`ex:counterexamples`, `ex:decomposition`, `ex:worked`,
  `ex:criterion` with `G_1'` and `G_1''`, `ex:two-edges`) and of Section 4 of the notes ("Graphs to verify": `G_a`
  with the pair `(s,t)`, `G_b`, `G_1` with distances and shortest paths, `G_1'`, `G_1''`, `G_a^+`, `G_a + w`,
  the 13-vertex graph outside DC with a separating trace of two edges and four terminals, `C_6`, two 4-cycles
  sharing a vertex, the `K_4` chain) was computed and compared: 113 claims, 0 mismatches
  (`results-named-graphs.txt`). Graph values: counterexample (a): `d = 3`, `c = 2`, `cp = 3`, `F` = all edges
  but `ab`, squares `{u}, {a,b}, {v}`, links `{s}, {t}`, `c(a,b) = 3`; counterexample (b): `d = 2`, `c = 3`,
  `cp = 3`, the minimum cut `{ua, ab, bv}` contains the path `u, a, b, v`, algorithm not applicable.
- Statements tested in the form written in `core.tex`: Lemma basic bounds with Corollary 3.12 (`PRE-cor312`), minimum
  cuts (`PRE-minimum-cuts`, `PRE-parity`), uncrossing identity (`PRE-uncrossing`), class (`S13-*`), easy pairs
  (`PRE-easy-*`), bridges (`S0c-*`, `PRE-bridges-DC`), orientation to degrees (`S2`-`S4`), Theorem "Square
  decomposition" (`S5`, `S6`), separation criterion (`S7`), Theorem "Separating shortest paths" (`S9-core`),
  Proposition "lengths" (`S8`), Corollary "two edges" (`S10-core-*`), residual lemma (`S11-res-*`), Remark "coarser
  decompositions" (`S14-*`, `ALG-coarse`), hardness (`S12-*`, including "every `u'`-`v` path consists of `u', s_j, u`
  and a `u`-`v` path of `G`" and the terminals `a_2 = b_2 = u`, `c_2 = d_2 = v`), proposition "open pairs"
  (`PRE-open-pairs`), and the remark of the notes that the strong components of the residual digraph are exactly the
  pieces (`ALG-scc`, 176550 + 2983 pairs).
- The two formulations of S9 (with `lambda^-`, `lambda^+` and edges `g`, `h`, as in the blueprint, and with
  `G`-distances to terminals, as in `core.tex`) are not equivalent path by path (deviation 6 of the notes) but give the
  same answer for `cp = d` on every instance (`S9a`, `S9-core`).

## Blueprint: ambiguities and corrections found

1. **S12** needs the hypothesis `c_G(u,v) >= 3` for "the whole of `G` is one square" (stated by the coordinator, now
   tested as two separate cases). For `c_G(u,v) >= 3` (18744 pairs): `F(u',v)` is the four new edges, `k = 2`, the
   piece of `v` is `V(G)`, with terminals `u, u` and `v, v`. For `c_G(u,v) = 2` (13350 pairs): `F(u',v) = F(u,v)` plus
   the four new edges and the squares of `(G', u', v)` are `{u'}` and the squares of `(G, u, v)`. The instances of
   article 1's reduction have `c(u,v) = 2n + 7m` (9, 18, 20, 13 on the four formulas tested), so the padding applies.
2. **S11** "two augmentations": `p_1`, `p_2` must be taken from the net flow, not from the two augmenting paths: the
   second augmenting path cancels flow on an edge of the first for 16 of the 13350 pairs with `c = 2` and at most 7
   vertices. `core.tex` defines `D` from two edge-disjoint paths, which is right.
3. **S11** the algorithm is correct under the weaker condition (*) (above), not only in DC; and the strong components
   of the residual digraph are exactly the pieces.
4. **S13/S0**: "in DC a pair with `d >= 3` has `c <= 2`" is the definition; the class is vacuous for graphs with at most
   7 vertices, so a test of a statement about DC on small graphs tests the statement for all graphs.
5. **S9** counts the squares' paths `p` from `x` to `y` with at least one edge for a separating trace (`x != y`
   because a square is connected); trivial paths never separate, as stated in `core.tex`.
6. **Observation 8** of the notes is false (above).

## Method notes and limits of the evidence

- `cp` is computed by `cp_brute` (all simple `u`-`v` paths of at most `UB` edges, `UB` = size of an explicit cut-path;
  for each path the minimum cut of `G - P`), and on every pair with at most 8 vertices also by article 1's method
  (`cp_subsets`, paths and vertex sets) and, up to 6 vertices, by the literal definition over all edge sets: all three
  agree on all 662244 ordered pairs (the last on 3866).
- `F`, orientation, pieces: from all pairs of edges whose removal separates `u` from `v` (`m^2` tests), never from the
  algorithm. For the large chain instances only the pairs (edge of `p_1`, edge of `p_2`) are tested (`fast_cuts`),
  which loses nothing by Menger's pigeonhole (a two-edge cut meets each of two edge-disjoint paths).
- Large instances: the number of simple `u`-`v` paths is capped at 20000 (30 chain instances in DC and 296 outside DC
  were skipped for this reason); `S1` uses at most 300 pairs of edge-disjoint paths per instance (all pairs when there
  are at most 250 paths); `S14` at most 6 random subsets of the minimum cuts; the residual lemma (i) is tested on
  at most 6 pairs of paths and only for graphs with at most 10 vertices.
- Sizes covered: exhaustive for all connected graphs with at most 8 vertices (S0-S11, S13-S15; the cut enumeration of
  `PRE-*` and of `S15b` only up to 7 vertices; S12 up to 7); random chains up to 40 vertices with at most 10 squares,
  built from blocks with at most 5 vertices (DC) or 9 vertices (outside DC), links of at most 4 vertices and pendant
  parts. The chains are not uniform samples: squares that are further split by two-edge cuts, large squares with
  complicated internal structure, and decompositions with many links in series are underrepresented, and the
  generator proposes `cp = d` instances by a pattern (crossed terminals). The evidence supports the statements; it
  proves none of them, and says nothing about large dense squares.
- The `(i)`/`(ii)` split of S9 is checked against `cp` from the definition, not against the proof of `core.tex`.
  `S1`, `S2`, `S4` are pigeonhole-level facts and are tested mainly as consistency checks of the decomposition code.
- Seeds are fixed (`--seed`, default 20261012); results are reproducible except for the timing.
- `mcp.py` is imported read-only by another session (`open-cases/`); its functions were only added to, never changed.
