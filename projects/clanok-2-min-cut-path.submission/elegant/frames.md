# Agent `frames`: a different framework for ZZ with P2

Status: in progress (started 2026-11-02, resumed after a session limit). Programs: `elegant/frames/`, logs `elegant/frames/logs/`. Nothing here has been refereed.
Labels: **proved** (complete proof here), **tested** (numbers given), **conjecture**, **refuted**.

## 0. State

Done so far: parameters on the planted families (Section 2), first tests of walk-based frameworks (Section 4), first part of the literature (Section 1).
Working on: conflict structure of shortest walks of the state graph; realisation proposition (Section 3).

## 1. Literature (question 1): log and facts checked at the source

Searches (web search tool, 2026-11-02):
1. *path avoiding forbidden pairs polynomial cases well-parenthesized hierarchical nested forbidden pairs Kolman Pangrac*: Kovac (arXiv 1111.3996), Kolman-Pangrac preprint, German (arXiv 2605.12457), a ZIB record on the PAFP polytope.
2. *shortest path with conflict constraints forbidden vertex pairs transitive conflicts comparability graph polynomial algorithm*: nothing on comparability or transitive conflicts.
3. *minimum s-t cut containing a path OR connected cut edges lattice of minimum cuts distributive closure with connectivity constraint complexity*: nothing on a cut containing a path; de Berg et al. (arXiv 2303.07290) and others are unrelated.
4. *Yinnone "On paths avoiding forbidden pairs of vertices in a graph" skew-symmetric matching augmenting path*: record only, full text not reached.

Facts read at the source:
- J. Kovac, *Complexity of the path avoiding forbidden pairs problem revisited*, arXiv 1111.3996 (HTML read). PAFP on a topologically sorted DAG. With pairs `u<v`, `x<y`, `u<x`: disjoint `u<v<x<y`, nested `u<x<y<v`, halving `u<x<v<y`. Table 1: general and overlapping (no disjoint) and ordered (no nested) NP-hard; well-parenthesized (no halving) `O(n^3)`, `O(n^omega)`; halving only `O(n^5)`, `O(n^{omega+1})`; nested only polynomial; disjoint only linear.
- P. Kolman, O. Pangrac, *On the complexity of paths avoiding forbidden pairs*, Discrete Appl. Math. 157(13), 2009 (KAM preprint text in `frames/logs/kp2009.txt`). DAG `G`, order induced by the paths, pairs comparable in it. Hierarchical: no two pairs `(u,v), (x,y)` with `u < x < v < y` in the path order. Theorem 3.2: NP-complete for the halving structure as they define it (no `v <= x`). Theorem 4.3: polynomial for hierarchical.
- S. German, *Layer-Based Width for PAFP*, arXiv 2605.12457 (abstract read): FPT in BFS-width of the union digraph plus backward arcs; NP-complete on DAGs of BFS-width 2 for the union digraph; polynomial for exact-length width at most 2 by 2-SAT, NP-complete at width 3.
- A. Yinnone, *On paths avoiding forbidden pairs of vertices in a graph*, Discrete Appl. Math. (DOI 10.1016/S0166-218X(96)00017-0): record and abstract fragment read (digraph, mutually disjoint pairs, keywords skew-symmetric, odd-set-cover, matching). Statement known only through Kovac and Kolman-Pangrac. Not opened.

## 2. Parameters (question 2), `frames/params.py`, log `logs/params-1.txt`

Tested, 2 instances per family, m from 61 to 432.

| family | m | q | |A_P| | |B_P| | width of Q | strict pairs of A x B | VC(MA cap B_P) | VC(MB cap A_P) | VC(MA on Q) | VC(MB on Q) |
|---|---|---|---|---|---|---|---|---|---|---|
| B | 242 | 161 | 40 | 50 | 33 | 1496/2000 | 1 | 1 | 2 | >=2 |
| stair | 239 | 161 | 43 | 44 | 25 | 1446/1892 | 1 | 2 | 2 | >=2 |
| mix | 329 | 231 | 45 | 62 | 27 | 1602/2790 | 1 | 2 | 2 | >=2 |
| cross | 432 | 299 | 66 | 76 | 32 | 3092/5016 | 1 | 2 | 2 | >=2 |
| allstrict | 176 | 133 | 25 | 27 | 27 | 675/675 | 1 | 1 | 2 | 2 |
| two | 61 | 53 | 26 | 26 | 26 | 675/676 | 1 | 1 | 3 | 3 |

Width grows with the instance, so it is not bounded. The small VC values are a property of the designs (hubs, shared witnesses); see Section 3 for what can be forced.

## 3. Graph level

To be written: every P2 instance is realised (`checks/realize.py`), so the graph level gives nothing beyond P2.

## 4. Walk-based frameworks: first tests

State graph: states `(x, low)`, `(x, high)`, edges from `R`, a walk from `(u, low)` to `(v, high)`, no validity.

- E1 (`e1_guess.py`, log `logs/e1-1.txt`). Restrict the state graph by two far pairs `a1, a2` of `A_P`, `b1, b2` of `B_P` taken from `P` (highs outside `FR(a1,a2)` and outside `dn(MB(a1) cap MB(a2))`, lows inside `ER(b1,b2)` and outside `up(MA(b1) cap MA(b2))`). `P` survives (assert held). Tested on 20 instances, 200 random far pairs each: distance in the restricted graph stays near 47 against `q` about 160; a shortest walk is rarely valid (only `two` and 2 of 200 on one `allstrict`). So four guesses plus a breadth-first search do not decide. Shortest walks have few conflicts, often one (minimum 1).
- E2 (`e2_branch.py`, logs `e2-5.txt`, `e2b-7.txt`). Exact search: on a conflict `h <= l` of a shortest walk branch on `h in D` or `h notin D`. Yes-instances: 45 to 76 nodes with depth 30 to 50, m up to 351, when the child "in D" is tried first. No-instances (planted with one edge of `P` removed): more than 20000 nodes in 23 of 30 runs. So no polynomial bound in sight without propagation.
- E3 (`e3_greedy.py`, log `e3-3.txt`). Greedy without backtracking (four rules): on tiny instances it fails on about 0.1 percent of 110923 yes-instances, and on all planted families except two runs of `two`. Refuted as a decision procedure.
