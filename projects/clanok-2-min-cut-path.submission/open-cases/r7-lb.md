# Round 7, agent r7-lb: lower bounds for single-term descriptions (Conjecture C1)

Status: in progress (started 2026-10-28, resumed 2026-10-29 and 2026-10-31). Working file of an AI agent; not read by the author; not
in the manuscript. Scripts: `r7-lb/`, logs `r7-lb/runs/`. Paths relative to `open-cases/`.
Labels: proved, checked (exact computation on named instances), sketch, conjecture, refuted.

Goal (author): decide whether the open case of DC is in P. This report tests Conjecture C1 from the lower-bound side:
for yes-instances of ZZ + P2 in general switch form, compute the exact minimum cost of a single connecting GDESC term
and search for instances where it grows.

## 0. Summary

(provisional; updated after every result)

## 1. Definitions used (from `qp-proof.md` §1-§5, `r5-core.md` §6.1, §8.2)

Instance: general switch form with P2 (`qp-proof.md` Definitions 1.7, 1.8). A *term* (single GDESC term) is

- an *E-term* `(T, T', Y, Φ)`: tools `T`, flagged tools `T' ⊆ T`, F-anchors `Y`, flips `Φ`;
  `U = ∪_{x∈T} NE(E#_x)`, `Π = ↓Y ∪ ∪_{x∈T'} (↓x − [x])`, `Γ = (Enon − U − Π) ∪ Φ`, `D = M − ↑Γ`;
- an *F-term* dually: `U' = ∪ NF(F#_y)`, `Π' = ↑Ψ ∪ ∪_{y∈T'} (↑y − [y])`, `Γ' = (Fnon − U' − Π') ∪ Φ`, `D = ↓Γ'`.

The *cost* of a term is `|T| + |Y| + |Φ|` (tools + anchors + flips); `GDESC(t, a, f)` enumerates all terms with at most
`t` tools, `a` anchors, `f` flips in time `m^{O(t+a+f)}` times a polynomial, and is sound for every choice. Flips are
allowed to be **arbitrary switches** here (in `qp-proof.md` Definition 6.1 and `gdesc.decide` they lie in the caught
set `U`); every term of the restricted kind is a term here, so a lower bound proved here holds for the restricted kind,
and the polynomial algorithm of C1 may enumerate arbitrary flips. Anchors are allowed in both kinds (`r5-core.md` §6.1).

`cost(I)` = least cost of a term whose `D` connects `s` and `t` (0 if `s = t`). Profile: for `t = 0, 1, 2, 3`, the least
`anchors + flips` of a connecting term with at most `t` tools.

## 2. Exact minimum single-term cost: the method and its verification

`r7-lb/lbcore.py` (docstring has the full argument). `D` connects `s` and `t` iff `L_P <= D <= M - Up_P` for a valid
path `P` (`qp-proof.md` Lemma 3.4), so only the inclusion-minimal pairs `(L, Up)` matter (`valid_pairs`). For one pair
and one kind the least cost is a covering problem plus a hitting set (`e_term`: columns `L ∩ Enon` must be caught by
a tool star, a flagged tool, or an anchor; then flips hit the minimal elements of `Up` that lose their generators);
F-terms are E-terms of the reversed instance. Every term found is rebuilt with `zzl.term_D` and tested with
`I.connects` (`verified=True`).

Checked: `test_lb.py` compares `mincost` with an independent enumeration of all terms of total cost `<= cap`
(`brute_mincost`) on random P2 instances: runs `test-lb-1-3-7.txt` (400 instances, m = 3..7, 232 yes, costs 0:201,
1:31, agreement everywhere) and `test-lb-2-6-9.txt` (150 instances, m = 6..9, 113 yes, costs 0:97, 1:16, agreement
everywhere).

## 3. Searches

### 3.1 Exhaustive and saved instances (checked)

- `enum_lb.py 3` (`runs/enum/enum-K3.txt`): all ZZ instances with `K = 3` middle elements: 7232 instances, 5830 with
  P2, 1584 yes, **cost 0: 1044, cost 1: 540**, no yes-instance with cost 2. Saved: `enum-K3-max-cost0.json`,
  `enum-K3-max-cost1.json`.
- `scan_files.py` (`runs/scan-saved.txt`): the 212 yes-instances saved by earlier rounds (`r5-core/runs`, 24 of them;
  `verify/rv-r6-core/runs`, 188; m from 17 to 703, all rigid, one minimal pair): **every one has exact cost 1**, a
  single tool (169 E-terms, 43 F-terms), no anchor, no flip. With no tool, the anchors and flips alone cost 2 to 12
  (or are impossible) on these instances; with one tool the cost is 0 extra. So on the saved families one tool
  suffices and anchors are irrelevant.

### 3.2 Annealing on planted-path designs (checked)

`sa_lb.py` (genome of `design.py`: path word over `{E, F}`, `nx` extra switches, relations, contacts EE / FF / LW /
UW, voluntary nodes; P2 and validity by construction; score `10 * cost - min(log2(1 + N), 9.9)` with `cost` the exact
minimum single-term cost and `N` the number of connecting terms of that cost, so the search prefers fewer cheap
terms). Moves: contact, relation, voluntary node, tie. Older short runs `runs/sa-old/sa11..16` (about 90 s each,
`T0 = 1`; best cost 1 for sa11, sa13, sa14; 2 for sa12, sa15, sa16) are superseded by the following.

Six runs of 3000 s each (`T0 = 0.40`, moves `crvt`, default contact `R` = random EE/FF, logs `runs/sa/sa2*.log`,
best genome and instance `runs/sa/sa2*-best*.json`). "Steps" = last logged iteration (the loop stops at 3000 s):

| run (seed) | path word | nx | m | steps | start cost | best cost | N | term of the best instance | minimal pairs |
|---|---|---|---|---|---|---|---|---|---|
| sa21 | EFEFEFEFEF | 4 | 14 | 91 500 | 1 | **1** | 7 | F, anchor {0} | 1 |
| sa22 | EEEEEFFFFF | 4 | 14 | 103 500 | 2 | **2** | 8 | E, anchors {5, 9} | 1 |
| sa23 | EEEEEEFFFFFF | 6 | 18 | 61 500 | 2 | **2** | 2 | E, anchors {11, 6} | 1 |
| sa24 | EFEFEFEF | 6 | 14 | 92 000 | 1 | **1** | 2 | E, anchor {7} | 24 (start instance, never beaten) |
| sa25 | EEFFEEFFEEFF | 4 | 16 | 90 000 | 1 | **1** | 2 | F, anchor {1} | 1 |
| sa26 | FFEEFFEE | 6 | 14 | 89 500 | 1 | **1** | 2 | F, tool {3} (no anchor) | 7 |

Every best score was reached within the first 1500 steps (25 s; sa21 at step 100, sa24 at step 0) and not improved
in the remaining 50 minutes (`cur` stayed 1 to 3 points below `best`): the landscape has a wide plateau at cost 1 or 2, no gradient
towards cost 3. The summary in `status.md` ("no tool and one or two anchors") is exact for five runs; the best
instance of sa26 is solved by one tool and no anchor. Re-verified in this round (2026-10-31) with `lbcore.mincost`
and independently with `brute_mincost(cap = 2)` (enumeration of every term): sa21 cost 1, sa22 cost 2, sa23 cost 2,
sa25 cost 1, sa26 cost 1, all terms verified; for sa22 and sa23 the brute force confirms that no term of cost 1
exists. The sa24 files were not written by the run (the start instance was never beaten); the start genome is
regenerated from seed 24 in `runs/sa/sa24-best*.json` (cost 1, N = 2, 24 minimal pairs, same as the log).

**Result of Section 3.2: largest single-term cost 2 (sa22, sa23: rigid instances with two anchors, no tool).**
Evidence for Conjecture C1, not a proof.

### 3.3 Anchor-hostile structured designs (2026-10-31; `r7-lb/adv.py`, `r7-lb/enum_zone.py`)

Why the annealing of Section 3.2 stayed at cost 2: its moves change contacts and relations of a random design with
m <= 18 and rarely create the two features an anchor-hostile instance needs, namely hub switches (one switch `bottom`
below everything, one `top` above everything) and *antichains of members whose pairwise contacts are tool-friendly
for exactly one of the two kinds of term*. `adv.py` builds them directly (through `design.py`, so P2 holds by
construction and the planted path is valid; the P2 check `I.p2_switch()` and a realisation as a ZZ instance
(`zzl.sw_to_zz`, `zz_p2`, connectivity of all down-sets compared with `I.connects`) were run on the best instances):

- path word `E^K F^K` (or any word), members `a_0..a_{K-1}` (E) and `b_0..b_{K-1}` (F);
- hubs `bottom < everything < top`; `Q` bad-pair extras `Y_i` (E-side nodes) and `X_j` (F-side nodes) with
  `Y_i < X_j` for all `i, j`, `Y_i <` some `b`, `X_j >` some `a` (the bad pairs of `r5-core.md` §6.4);
- contacts of two E-members: FF or UW(top); of two F-members: EE or LW(bottom) (the contacts that cannot shortcut the
  planted path, because they are not between two sides of the mode the path uses);
- contacts of a cross pair `(a_i, b_j)`: EE, FF, LW(bottom), UW(top) or `b_j < a_i` without contact, with weights
  `PROBS` (default E3 F3 L1 U1 C1).

Objective of the annealing: `10 * cost + min(mean, 6) - 0.1 log2(1 + N)` (objective 1) or
`8 * cost + (c0 + c1 + c2 + c3)/2 + mean/2 - 0.1 log2(1 + N)` (objective 2, `ADV_OBJ=2`), where `mean` is the mean of
the exact single-term cost of the individual minimal pairs (so that the cheap pairs of a non-rigid instance are
pushed up too) and `c_t` the exact least cost with at most `t` tools.

**Outcome so far (checked): cost 3 occurs and is common.** `adv.py sample` (random designs, exact cost by
`lbcore.mincost`; cost = minimum over all minimal pairs):

| script call (seed, word, Q, samples, probs) | cost 1 | cost 2 | cost 3 | cost >= 4 |
|---|---|---|---|---|
| sample 2, E4F4, 1, 200 | 70 | 118 | 12 | 0 |
| sample 2, E5F5, 1, 200 | 68 | 127 | 5 | 0 |
| sample 2, E6F6, 2, 200 | 138 | 62 | 0 | 0 |
| sample 2, E7F7, 2, 200 | 149 | 51 | 0 | 0 |
| sample 3, E4F4, 0, 3000 | 680 | 1998 | 322 | 0 |
| sample 3, E4F4, 1, 3000 | 954 | 1849 | 197 | 0 |
| sample 3, E4F4, 2, 3000 | 1221 | 1666 | 113 | 0 |
| sample 3, E5F5, 0, 3000 | 658 | 1978 | 364 | 0 |
| sample 3, E5F5, 2, 3000 | 1733 | 1249 | 18 | 0 |
| sample 3, E6F6, 1, 3000 | 1691 | 1297 | 12 | 0 |
| sample 3, E6F6, 3, 3000 | 2244 | 756 | 0 | 0 |

(sample 3, E8F8, Q = 1 was stopped by PID after 675 samples: best cost 2 with 11 to 67 minimal pairs; logs
`runs/adv/grid-K*-Q*.txt`, probs E3F3L1U1C1.)

Cost 3 instances (files `runs/adv/sample-K4-Q1.txt.best-inst.json`: m = 12, one minimal pair, rigid, exact cost 3,
term E, tool {0}, flips {0, 2}; independent enumeration `brute_mincost`: no term of cost <= 2, a term of cost 3;
`sample-K5-Q1.txt.best-inst.json`: m = 14, 5 pairs, cost 3; `grid-K4-Q0.txt.best-inst.json`: m = 10, 3 pairs of costs
3, 3, 4). Exhaustive `enum_zone.py 3` (all 512 pure 0/1 tournaments of E^3 F^3 without hubs): costs 1:338, 2:174,
no cost 3.

**Cost 4 (checked).** `adv.py sample 5 5 0 100000 E3F3L1U1C1 runs/adv/big-K5-Q0-p1.txt` (seed 5, word E5F5, Q = 0, 100 000
random designs, 649 s): cost 1: 21 162, cost 2: 66 862, cost 3: 11 975, **cost 4: 1** (the 57 852nd sample). Instance
`inst/cost4-E5F5-Q0-seed5.json` (genome `inst/cost4-E5F5-Q0-seed5-genome.json`): m = 12 switches (5 E-members, 5
F-members, `bottom`, `top`), **one** minimal valid pair (rigid; only 1 of the 322 down-sets of the switch preorder
connects `s` and `t`), P2 holds (`p2_switch` and the ZZ realisation `zz_p2`; connectivity of all 322 down-sets
agrees between the ZZ realisation and the switch form). Exact single-term cost **4**: `lbcore.mincost` finds an E-term
with one tool (switch 1) and three flips (0, 1, 2); the independent enumeration `brute_mincost` finds no term of cost
3 and a term of cost 4, also when the flips are restricted to the caught set `U` (definition of `qp-proof.md` 6.1).
Cross matrix of the planted pair (rows a_0..a_4, columns b_0..b_4; E = EE contact, F = FF contact, L = LW(bottom),
U = UW(top), < = b_j < a_i without contact):

```
a0  E F E E <        a-a: FF, except UW(top) for (0,4), (1,3), (2,4)
a1  F E < U L        b-b: EE, except LW(bottom) for (5,9), (6,8), (6,9), (7,8), (7,9)
a2  E F E E L        extras: bottom (below all), top (above all), nothing else
a3  F E U E <
a4  < F < U E
```

Why the cost is 4 (from the covering table of the pair, checked by a script that lists for every switch which columns it
catches and which minimal E-members it loses): for the E-term the columns are the five F-members. Every switch that
catches all five columns as a tool (b_0, b_1, b_2, b_3, b_4, a_1, a_2) loses at least three of the five minimal
E-members, which then need flips: tool plus three flips = 4. The flagged tool a_0 catches four columns and loses two:
flagged tool, one anchor for the fifth column and two flips = 4. Five anchors (one per F-member, losing nothing) cost 5;
a plain tool catching three columns plus two anchors plus two flips costs 5. The F-term is symmetric. So the mechanism is
the game of Theorem 6.5 (tools against flips), with the shortcuts of the path removed by the comparabilities `<` and the
LW/UW contacts.

The annealing started from the cost-4 genome (`adv.py sa 33 ... ADV_OBJ=2`, 187 s, 51 500 steps, stopped by PID) found
no cost-5 neighbour; the annealing from random structured starts (`sa 31`, `sa 32`: 104 s and 405 s, stopped by PID)
stayed at cost 3. So the cost-4 instance is isolated for single-contact moves.

## 4. Results

(updated after every result; see Section 3 for the outcomes so far)

## 5. What the failed attempts show

(to be filled)
