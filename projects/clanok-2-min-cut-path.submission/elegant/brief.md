# Brief: better and more elegant proofs for article 3

Goal of the author (2026-11-02): find more elegant proofs. The bound `O(n^30)` for the open case is large. Any of these is progress, in this order of value:
a small exponent (say at most 10) by a new idea; a much shorter proof at any polynomial exponent; a smaller constant in the present proof.

## The text

`projects/clanok-2-min-cut-path/main.tex`, read selectively. Do not edit it. Labels: `sec:zz-zigzag` (reduction, valid walks), `sec:pa-polynomial` (the algorithm), `thm:pa-formulas` (main proof), `sec:squares` (pairs with `c <= 2`).
The proof holds: `projects/clanok-2-min-cut-path.submission/review/referee-direct.md`.

## The problem in one page (ZZ with P2)

`Q` is a finite set with a preorder, `u <= x <= v` for all `x`, `u < v`. `R` is a set of pairs `ab` with `a < b`. `x, y` *meet below* if `zx, zy` are in `R` for some `z`, and *meet above* if `xz, yz` are in `R` for some `z`.
**P2:** every two incomparable elements meet below or meet above. A down-set `D` with `u in D`, `v notin D` gives the graph `G_D` of the edges of `R` with lower end in `D` and upper end outside `D`. Question: are `u` and `v` connected in `G_D` for some `D`?
Equivalently: a *valid walk* is a sequence from `u` to `v` of odd length with positions labeled alternately low and high, `u` low, `v` high, each consecutive pair an edge of `R` with lower end at the low position, such that no high is `<=` a low. `L_P` is the down-closure of the lows and `U_P` the up-closure of the highs; they are disjoint, and any down-set between them works.

Without P2 the problem is NP-complete (`rem:zz-no-p2`, 3-SAT, `thm:dt-hardness`). So P2 must be used.

## The present proof, in short

Fix a shortest valid walk `P`. `A_P`: minimal highs. `B_P`: maximal lows. Enough: a down-set containing `B_P` and missing `A_P`.

- *One detour* (`lem:pa-one`): if `a, a'` in `A_P` meet `x` below and `x` is not `<=` any low outside `(pos a, pos a')`, then `|pos a - pos a'| <= 4`. So for `x notin L_P`, at most 3 elements of `A_P` meet `x` below. Dually for `B_P` and meeting above.
- *Far pair*: two elements of `A_P` (or of `B_P`) at positions at distance `>= 6`. *Atoms* (`def:pa-atoms`): for a far pair `a_1, a_2`, the set `FR(a_1, a_2)`, the down-closure of everything not above `a_i` and not meeting `a_i` above, misses `U_P` and contains every `b in B_P` that meets neither `a_i` above. Dually `ER(b_1, b_2)`. Also `EP(a)`, which contains every `b in B_P` with `b < a` and misses all but three elements of `A_P`.
- *Two detours* (`lem:pa-two`): for `a in A_P`, `h in B_P`, `h` not `<= a`, shortcuts on both sides of a kept middle part have total saving at most 8, unless the positions of the classes of `a`, `h` block them. This gives property `(star)`.
- *`thm:pa-formulas`*: four thresholds on contact positions, two ranges of positions, an orientation case analysis, classes of tied elements, a tail, Shapes A and B. The result is a formula over at most 28 elements. See `tab:pa-exits`.
- The algorithm enumerates all formulas and tests each. Exponent 30 = 28 + 2. It uses nothing else about the structure.

Ties matter: tied elements have one side in every `D`, but they are not joined in `G_D`, so classes cannot be contracted. A class of `A_P` can have many positions along `P`.

Far conflicts are real: in hard instances, shorter walks are blocked only by a pair `h <= a` of a high and a low that lie far apart. So a window DP that checks conflicts only locally does not work as it stands.

## Tools

`projects/clanok-2-min-cut-path.submission/checks/`: `zz_core.py` (class `Inst`, atoms, exact solver `shortest_walk`), `zz_proof.py` (the proof with asserts; `Cfg` holds its constants), `zz_design.py` (planted hard families that reach Shapes A and B: A, B, stair, ties, mix, cross, allstrict, small, kappa, two), `run_planted.py`, `run_mut.py`. Reuse them by import; do not edit them.
Older material: `projects/clanok-2-min-cut-path.submission/open-cases/r7-lb.md` (lower bounds for single-term descriptions and hostile designs), `status.md`, `r7-desc.md`. Read only what you need.

## Rules

- Write in English. Save as you go to your own report `projects/clanok-2-min-cut-path.submission/elegant/<your name>.md`, and put your programs and small logs in `elegant/<your name>/` (logs under 2 MB in total). Touch no other file.
- Write scripts with the Write tool, never with heredocs (backslashes get halved on this machine). Long runs go in the background, at most 3 processes at a time; record their PIDs in your report. Stop a process only by its PID, never by image name. Do not commit.
- A claim is one of: **proved** (complete proof written in your report), **tested** (with the numbers and what the tests could not reach), **conjecture**. A counterexample to an idea is a valuable result: save it and say what it rules out. Try to refute your own idea by program early.
- Do not report more than you have. Nothing is a result until an independent referee has read it.
- End the report with: what is proved, what would change in the article and how many pages it saves, what the new exponent is, and what failed and why.
- Read selectively. If you hit a session limit, your report must already hold your state.
