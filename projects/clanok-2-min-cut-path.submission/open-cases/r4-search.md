# Round 4: computational search for hard instances of ZZ + P2 (agent r4-search)

Status: in progress (version 2, 2026-10-17; version 1 of 2026-10-16 was the skeleton). Scripts and instances:
`open-cases/r4-search/` (Python 3.13 and one Node.js file; other agents' code imported read-only). Labels:
**proved**, **checked** (exact computation on named instances), **conjecture**, **refuted**. Every computation names
its script, seed, sizes and counts. `q` = number of elements of the ZZ form, `|R|` = number of real edges.

## 0. Summary

| # | Result | Status |
|---|---|---|
| P | A portfolio of all known polynomial methods (Section 1), validated against exact solvers on 1200 random instances (0 discrepancies) | checked |
| Y1 | **Smallest portfolio-hard yes-instances at level 2 have exactly `q = 10` elements.** No P2 yes-instance with `q <= 9` defeats the 2-guess together with the lattice guesses (exhaustive, Section 3.1); with `q = 10` at least 28 iso classes defeat G2, LAT2 and GC2 (e.g. `L2-q10-a.json`: 6 middle elements ordered as a matching `a_i < b_i`, two elements in the class of `u`, two in the class of `v`, 16 real edges, a unique solution). All have width 3, so the 3-guess solves them | checked |
| Y2 | Smallest **switch-model** (2CH + P2) instance found that defeats level 2 (G2, LAT2, H1, GC2): `L2-sw-20.json`, `q = 20`, 8 switches, 9 nodes, unique solution with 4 switches in each mode; it also defeats G3, GC3 and H1, but Theorem H with `t = 2` solves it. Lower bound `q >= 14` (proved earlier for G2 alone) | checked (upper bound); the exact minimum is open |
| Y3 | Level-3 hard (G3, LAT2, GC3 fail) general instance: `L3-oneway-31.json`, `q = 31`, switch model plus one one-way relation (so H1, H2 do not apply) | checked |
| N1 | **Path consistency decides ZZ + P2 for `q <= 7`; the smallest AC false positive has exactly `q = 7`.** Exhaustive over all preorders and all maximal no-instances (monotonicity argument, Section 3.2): `q = 4..7`: 16, 92, 724, 7913 maximal P2 no-instances (iso classes); AC false positives 0, 0, 0, 615; PC refutes all 615 | checked |
| S | Shrinking and annealing (Section 4): from `T_6` to 23 elements (one tie or one one-way relation), from `R_8` to 21, annealing to 20 (switch model); from `T_8` at level 3 to 31 | checked |

## 1. The portfolio (`r4-search/portfolio.py`)

Witness methods (sound "yes", with a solution; the solution down-set is re-checked by `common.check_downset_solution`):
- `G_K`: the `K`-guess on both sides (Theorems F, F+, Fω): `D_A = Q - ↑(A ∪ {v})` and `D^B = ↓(B ∪ {u})` over sets
  `A`, `B` of at most `K` middle classes (own bit-mask code, checked against `dc-algorithm/mixed.py`).
- `LAT2`: lattice guesses: unions and intersections of at most two basic down-sets `↓a`, `{x : x < a}`, `Q - ↑a`,
  `{x : not a < x}` (`a` any element). Contains the strict guesses of `dc-algorithm/ladder.py` and the 2-guess.
- `H1`: Theorem H search with `t = 1` (`dc-hardness/helly2ch.py`), switch-model instances only. Used through
  `h1.js`, a Node.js port with the same semantics (BFS per stored set with bit masks, plus a sound pre-filter:
  relaxed reachability without the stored-set constraints), about 500 times faster (`R_8`: 0.02 s against 9.7 s).
- `GC_K`: certificate search of Theorem GC (`dc-general/gcert.certificate`), pin sets of size `<= K`, all modes.
- `H2` (optional, switch model): Theorem H with `t = 2`, realised as GC general mode with at most 4 piercers in `B`
  and 4 in `T` (complete whenever Theorem H with `t = 2` is, by `κ <= 4t`, `dc-general.md` §1).
Relaxations (sound "no"): `AC`, `PC` (`zz.py`, `pcfast.py`; `L` = largest odd number `<= q`), `SPC` (singleton PC,
`dc-algorithm/variants.spc`), `SPPC` (PC of the simple-path CSP, refutes iff it refutes every odd `L <= q`).
Complete-class certificates (a failed witness method then proves "no"): width `<= K`;
`2 min(ω(U), ω(Λ)) <= K` (Theorem Fω); switch model with Helly side families (Theorem H).

**Levels.** Level 2 = {G2, LAT2, H1, GC2}; level 3 = {G3, LAT2, H1, H2, GC3}. An instance is **portfolio-hard
(level K)** if it is a yes-instance on which no witness method of the level finds a solution, or a no-instance that
no relaxation refutes; *strictly hard* if, for a no-instance, no complete-class certificate applies either.

## 2. Validation of the imported routines

`validate.py SEED 400`, seeds 11, 12, 13 (`runs/validate-1{1,2,3}.txt`): 1200 random instances (430 random 2CH + P2
from `twoch.random_p2_instance`; 332 general preorders with ties and middle edges from `gcert.random_inst`; 438 from
`mixed.random_instance` with lower, upper or mixed witnesses), `q <= 22`; 489 yes, 711 no.
Checked on every instance: `zz.exact` (all down-sets) = `zz.exact_dfs` = `gcert.exact` = `gcert.exact_downsets`; for
2CH also brute force over mode vectors and the round trip `zz_to_sw(sw_to_zz(.))` (answer and P2); `G_K`
(`K = 1, 2, 3`) succeeds iff some solution down-set has `g_low <= K` or `g_up <= K` iff `mixed.guess_low/up`
succeeds; LAT2, GC2 (walk re-checked), H1, the strict guess sound; strict guess ⊆ LAT2; AC, PC, SPC, SPPC never refute
a yes-instance; `pcfast.pc_answer` = `zz.pc_numpy`. Result: **0 discrepancies** (4 AC false positives, all refuted by
PC). Note: random instances are easy (GC2 solved all 489 yes-instances).
`h1fast.py 1 300`: `h1.js` = `helly2ch.helly_solve` on 160 random 2CH + P2 instances (`N <= 10`; 91 yes) and on
`R_2..R_8` in both forms; `R_9` only with the fast code.

## 3. Exhaustive enumeration

### 3.1 Yes-instances, level 2 (`enum_yes.py`)

**Lemma Y (proved).** Fix the preorder. (a) G2 and LAT2 find a solution iff some solution down-set lies in the family
`G` of down-sets with `g_low(D) <= 2` or `g_up(D) <= 2` or `D` a LAT2 set; `G` depends only on the order. (b) "No
`D ∈ G` connects `u`, `v` in `G_D(R)`" is closed under removing real edges; "yes-instance" and P2 are closed under
adding real edges. (c) A yes-instance defeating G2 has a solution `D` with at least 3 maximal middle classes in `D`
and at least 3 minimal middle classes outside, hence at least 6 middle classes.
*Proof.* (a) `D_A` for `|A| <= 2` is a down-set whose complement `↑(A ∪ {v})` has at most `|A|` minimal classes
besides that of `v`; conversely a down-set `D` with `g_low(D) <= 2` equals `D_A` for `A` its minimal classes outside
(the complement of a down-set is the up-closure of its minimal classes); dually for `D^B`; LAT2 tests a fixed family
of down-sets. (b) `G_D(R)` grows with `R`; a witness of P2 stays a witness. (c) `g_low`, `g_up` count classes. ∎
**Lemma Y' (proved earlier, `dc-algorithm.md` §11.6).** A switch-model instance defeating G2 has `q >= 14`; so for
`q <= 13` H1 cannot matter and level 2 reduces to {G2, LAT2, GC2}.
*Method.* Middle posets up to isomorphism (`posets.py`, counts 1, 1, 2, 5, 16, 63, 318, 2045, 16999 for 0..8
elements = OEIS A000112), kept if some down-set has `>= 3` maximal elements and `>= 3` minimal elements outside;
class sizes and the sizes of the classes of `u`, `v` distributed up to automorphism; for each preorder a branch and
bound over the real-edge set with three prunings (included edges make some `D ∈ G` connect; included plus undecided
edges make no `D ∉ G` connect; included plus undecided edges violate P2). By Lemma Y the leaves are exactly the P2
yes-instances defeating G2 and LAT2; they are reduced to orbits under the automorphisms of the order and tested
with GC2.

| `q` | orders (with a non-guessable down-set) | B&B nodes | leaves (iso classes) | GC2 fails | time |
|---|---|---|---|---|---|
| 8 | 36 (4) | 1,754 | 0 | - | 1 s |
| 9 | 878 (86) | 921,316 | 0 | - | 12 s |
| 10, 6 or 7 middle classes (part: 7 middle classes up to poset 640 of 665) | 5,661 (507) | 1.8e8 | 42 at the last log line | at least 28 (file `runs/enum-yes-hard-q10.jsonl`) | 3055 s |
| 10, rest | running | | | | |

Control without LAT2 (G2 only): `q = 8`: 18 iso classes defeat G2, all solved by GC2 (the ladder `K(3)` is of this
kind); `q = 9`: 10,174 defeat G2, of which 2,404 also defeat GC2. So LAT2 is the method that disposes of all
instances with `q <= 9`.
**Result (checked).** No P2 yes-instance with `q <= 9` defeats level 2; with `q = 10` there are such instances, so
the minimum is exactly 10. The 28 found so far: 4 with 6 middle elements (`|B| = |T| = 2`), 24 with 7 middle elements
(`|B| = 2` or `|T| = 2`); none is a partial order with `|B| = |T| = 1` so far (8 middle elements not yet done).

*Structure of `L2-q10-a.json`* (`enum-q10-00`): elements `u = 0`, `1 ~ u`, middle `2..7`, `8 ~ v`, `v = 9`; middle
order `2 < 5`, `3 < 6`, `4 < 7` (a matching), nothing else; width 3; `R`: `0-2 0-3 0-7 1-2 1-4 1-5 1-6 2-5 2-9 3-6
3-8 4-7 4-8 5-8 6-8 7-8`. Unique solution down-set `D = {0, 1, 2, 3, 4}`, zigzag `0 7 4 8 3 6 1 5 2 9`
(`g_low = g_up = 3`). Witnesses: 4 pairs bottom only, 4 top only, 4 both; `ω(U) = ω(Λ) = 2`. G3 and GC3 solve it
(pinned mode with generators `{5, 6, 7}`).

### 3.2 No-instances: relaxations (`enum_no.py`)

**Lemma N (proved).** Fix the preorder. (a) "No-instance" is closed under removing real edges; (b) P2 is closed under
adding real edges; (c) "AC (PC, SPC, SPPC) does not refute" is closed under adding real edges. Hence a relaxation fails
on some P2 no-instance with this order iff it fails on a maximal no-instance (no real edge can be added without
creating a consistent zigzag) that satisfies P2.
*Proof of (c).* The CSP of a subset `R' ⊆ R` (same order, same `L`) is the sub-CSP of the CSP of `R` induced by the
values in `R'`: domains are subsets of real edges, the constraints between two values depend only on the order and on
the two edges. A consistency closure (AC, PC, singleton PC, PC of the simple-path CSP) is the greatest fixpoint of a
monotone operator, so the closure of the sub-CSP is contained in the closure of the full CSP; if the former has no
empty relation, neither has the latter. ∎
*Method.* All preorders on `q` elements with `u` least and `v` greatest (middle posets up to isomorphism, sizes up to
automorphism); branch and bound enumerating the maximal no-instances; leaves reduced to orbits; P2; AC; PC if AC fails;
SPC and SPPC if PC fails.

| `q` | orders | maximal P2 no-instances (iso classes) | AC false positives | PC false positives | time |
|---|---|---|---|---|---|
| 4 | 8 | 16 | 0 | 0 | 0 s |
| 5 | 22 | 92 | 0 | 0 | 0 s |
| 6 | 69 | 724 | 0 | 0 | 1 s |
| 7 | 255 | 7,913 | 615 | 0 | 79 s |
| 8 | running | | | | |

**Result (checked).** Every P2 no-instance with `q <= 7` is refuted by PC; AC refutes all with `q <= 6`, and the
smallest AC false positives have `q = 7` (the 9-element instance D1 of `dc-algorithm.md` was not minimal).

### 3.3 Switch model

(to be filled)

## 4. Structured search

**Known families under the portfolio** (`try_known.py`, level 2 unless stated):

| Instance | `q` | Level 2 verdict |
|---|---|---|
| `A14` | 14 | H1 solves |
| `K(3)`, `K(4)`, `KW(3)` (ladders) | 8, 10, 10 | LAT2 solves (G2 fails) |
| `R_4`, `R_6` (2CH form) | 18, 33 | G2 / H1 solve |
| `R_8` (2CH form) | 52 | **hard** (G2, LAT2, H1, GC2 fail) |
| `T_4^tie`, `T_4^one` | 28 | G2 solves |
| `T_6^tie`, `T_6^one` | 40 | **hard** |
| `T_6`, `T_7` at level 3 | 40, 46 | G3, GC3 solve |
| `T_8^tie`, `T_8^one` at level 3 | 52 | **hard** |

**Greedy shrinking** (`shrink.py`: delete an edge, an element or a cover relation (mode `zz`), or remove a node from a
side, merge or delete nodes, delete a switch (mode `sw`); keep P2, "yes" and level-K hardness; stop at a local
minimum). Final sizes `(q, |R|)`:
- `T_6^one`, level 2, seeds 1-16: `q` = 23 (twice), 24-27; `T_6^tie`, seeds 1-16: 23 (five times), 24-31. The
  23-element minima are the switch model plus **one tie** (`L2-tie-23.json`) or plus **one one-way relation**
  (`L2-oneway-23.json`); G3 and GC3 solve both.
- `R_8` (mode `sw`), level 2, seeds 1-40: minimum 21 (`L2-sw-21.json`), most runs 23-25; `R_9`, seeds 1-20: 24-27.
- `T_8^one`, `T_8^tie`, level 3, seed 1: 31 (`L3-oneway-31.json`) and 33.
**Annealing** (`anneal_sw.py`, from `L2-sw-21`, seeds 1-4, 20,000 steps, level 2): best `q = 20`, `|R| = 32` in
three runs (`instances/anneal-sw-s{1,3,4}.json`), 33 in one; stored as `L2-sw-20.json`.

*Structure of `L2-sw-20.json`* (2CH, nodes `0..8`, `s = 0`, `t = 3`):

| switch | E-side | F-side |
|---|---|---|
| 0 | {s, 2} | {6, 7, 8} |
| 1 | {5, 8} | {2, 8} |
| 2 | {1, 8} | {6} |
| 3 | {4, 5} | {6} |
| 4 | {5} | {6, 7} |
| 5 | {1, 8} | {4, 6} |
| 6 | {1, 5} | {t, 7} |
| 7 | {1, 5} | {7} |

Unique connecting mode vector: switches 1, 4, 5, 6 in F-mode, 0, 2, 3, 7 in E-mode (so G3 fails); H1 fails (both
implementations), GC3 fails, H2 finds the solution.

## 5. Gadget search

(to be filled)

## 6. Files (`open-cases/r4-search/`)

| File | What |
|---|---|
| `common.py` | imports, conversions (2CH ↔ ZZ, ZZ → gcert), exact solvers, JSON format |
| `portfolio.py` | the portfolio |
| `h1.js`, `h1fast.py` | fast Theorem H search (`t = 1`) and its check against `helly2ch.py` |
| `validate.py` | validation of the imported routines |
| `known.py`, `try_known.py` | known families and their verdicts |
| `posets.py`, `enum_yes.py`, `enum_no.py` | exhaustive enumeration (Sections 3.1, 3.2) |
| `shrink.py`, `anneal_sw.py` | structured search |
| `describe.py`, `finalize.py` | description and independent re-check of an instance |
| `instances/*.json` | instances; format in `common.py` (`n`, `u`, `v`, `le`, `R`, optional `2ch`, `verdict`, `notes`) |
| `runs/` | logs |
