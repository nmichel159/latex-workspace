# Adversarial review of r5-classes.md (version 0.2, 2026-10-22): Theorem Q and its companions

Status: reading complete and verdicts final (2026-10-22); computations recorded 2026-10-28 (§3, §4; round 6c, records
only): 38 of the 40 logs are complete, `hunt-11-band-h` was cut off (empty log), `tourn-abstract-2` is ambiguous; no
log shows a failure and none contradicts a verdict of §1. §5 and §6 were never written by the reviewer (the review was
stopped on 2026-10-22 about 20:40); they contain pointers only. Reviewer: agent rv-classes-q (round 5). Scripts and
logs: `verify/rv-classes-q/` (own code written from the definitions of r5-classes.md §1-§2c; `r5-classes/` is not
imported by any script except the cross-check `crosscheck_author.py`; `verify/r4-switch-review/` is imported only by
`crosscheck_cor22.py`, named as a cross-check). Labels: **holds**, **holds with repair**, **gap**, **false**;
computations with script, seed, sizes, counts, outcome.

## 1. Verdicts

| Statement | Verdict | Notes |
|---|---|---|
| §1 setting (valid path ⇔ yes-instance) | holds | §2.1 |
| A1, A2, A3, A4, A5, Key Lemma K | holds | §2.2; A5 is soundness only |
| §2a definitions (`σ_U`, `Ω(C, τ)`, misclassification, DESC), Lemma 2a.1, soundness and time of DESC | holds | §2.3 |
| Corollary 2a.2 (`DESC(6, 12, 18)` decides 2CH + P2) | holds | §2.4; one type `τ` suffices |
| Lemma W | holds | §2.5 |
| Lemma D | holds | §2.5 (it is P2 for one pair) |
| Theorem Q | holds | §2.6; non-trivial only when the number of classes exceeds `3k` (§5) |
| Corollary Q | holds | §2.7 |
| Lemma PP and the two consequences after it | holds | §2.8 |
| Remark (2) after Theorem Q | holds as a statement about the minimax argument only | §5 |

(Computational support: §3 and §4; all runs finished or were cut off as recorded there.)

## 2. Line-by-line reading

### 2.1 Setting (§1)

Sides are pairs (switch, type); `Ω(C, τ)` and `N_τ[Z]` contain only non-empty sides (the proof of Theorem Q writes
`Ω(C, O) = {w^O : w ∈ C ∩ W*}` with `W*` the switches with non-empty `O`-side, so this is the reading of the text).
A shortest sequence of picked sides from `s` to `t` repeats no side, each switch has one picked side, and a class
has one mode, so it is a valid path; conversely the classes used on a valid path have one type each, give them that
mode, and every side of the path is picked. `s ≠ t` is assumed (for `s = t` the valid-path characterisation would be
wrong, the connectivity question trivial). A switch with both sides empty violates P2 against every switch of
another class, so with at least two classes every switch has a side. **Holds.**

### 2.2 A1-A5, Key Lemma K (§2)

- A1: `X_1 .. X_a X_b .. X_r` keeps `s`, `t`, distinct switches and single types per class; shorter. Holds.
- A2: the two P2 pairs of `w_a`, `w_b` (different classes) are the same-type pairs; for equal types one of them is
  `{X_a, X_b}` (disjoint by A1 when `|a - b| >= 2`), for opposite types they are `{X_a, X'_b}` and `{X'_a, X_b}`
  (no distance condition needed). Holds.
- A3: `Z` is an `O`-side of `w ∈ C`, `C` used with `T`, so `Z` is not on `P`; every switch of `C` on `P` sits in
  `(d, c)`, so `w` is at no kept position and no kept member is of class `C`; `X_1 .. X_d Z X_c .. X_r` is valid,
  of length `r - (c - d - 2)`, so `c - d <= 2`; two positions of `C` in `(d, c)` need `c - d >= 3`. Holds.
- A4: `w_Z` is not on `P` (its `T`-side is `Z ∉ P`; its `O`-side would conflict with the `T`-members of `C`); the
  shortcut argument is that of Lemma W; the P2 consequence is the other same-type pair. Holds.
- A5 (soundness of the class search): if `Y_i`, `Y_j` (`i < j`) are sides of one class with different types, then
  `Y_i ∈ Π(Y_j) ⊆ K` by (i) at step `j`, so `(class, type of Y_i)` was stored at step `i`, and it is exactly the pair
  refused for `Y_j` by (ii). The argument uses no bound and no minimality, so every accepted walk is a valid walk
  for every `K`, `B`. Holds. (The text claims nothing about completeness; the obvious analogue of r4-switch
  Theorem 5(2) holds as well: a valid path with `Π(X) ⊆ K` for its members and at most `B` stored pairs is
  accepted, since a valid path has no conflicting pair.)
- Key Lemma K is P2 for the pair `w`, `v` written with the two same-type pairs. Holds.

### 2.3 Descriptions (§2a)

`σ_U` (`U` a set of `τ`-sides) gives `C` mode `1 - τ` iff `Ω(C, τ) ⊆ U`. Lemma 2a.1: for `C ∈ 𝒯`, `σ_U` is right iff
`Ω(C, O) ⊆ U`; for `D ∈ 𝒪` it is right iff `Ω(D, O) ⊄ U`; so `Φ` is exactly the set of classes of `P` on which
`σ_U` is wrong, `σ_U^Φ` gives every class of `P` its type on `P`, picks every member, and `s`, `t` are connected
through `P`. Classes not on `P` are irrelevant. Holds.
DESC tests only mode vectors for connectivity, so it is sound for all parameters. Its time: at most
`Σ_{i<=f} C(D, i) · Σ_{j<=g} C(c + D, j) <= (D + 1)^f (2D + 1)^g` sets `U` per type, at most `(c + 1)^e` sets `Φ`,
one connectivity test each; `O((2D)^{f+g} n^e (N + D)^2)` is right up to the usual `+1`s. Holds.

### 2.4 Corollary 2a.2

In 2CH + P2 each class is a singleton. For a `T`-certificate `K_T` (a set of `O`-sides containing every non-empty
partner of a `T`-member): a `T`-class `{w_a}` has `Ω = {X'_a}` or `∅`, contained in `K_T`, so it is never
misclassified; an `O`-class `{w_c}` has `Ω = {X_c}` and is misclassified iff `X_c ∈ K_T`. So `mis_P(K_T)` equals the
storage `|P ∩ K_T|` exactly (every member in `K_T` is an `O`-member). For any fixed `T`, the reviewed results give a
shortest valid path `P°` and a `T`-certificate of the needed shape: if `P` has a `T`-straddle, Lemma 7 gives `P*`
with `K*_T = N_O[X_p] ∪` two single sides, storage `<= 3`; otherwise Theorem 8 with the remark of
`verify/r4-switch-review.md` §2.6 (re-derived here: three elements of `A` with pairwise disjoint spans, the middle
one by position has an inner element `p` of `f(a_j)` — `|f(a_j)| >= 4` after step (1) — outside `f(a_i) ∪ f(a_k)`,
so `a_i, a_k ∈ b(p)` by (F1→) and (F2→) gives a `T`-straddle; so `|H|, |H'| <= 2`) gives at most `2 + 2 + 2 = 6`
sets `N_O[Z]`, `2 + 5 + 5 = 12` single sides and storage `<= 18`; steps (0)-(2) give less. With `U = K_T`, `τ = O`
and `Φ` the at most 18 stored `O`-classes, `σ_U^Φ` connects `s`, `t`, and this `(U, Φ)` is enumerated by
`DESC(6, 12, 18)`. The time is `O((2D)^{18} n^{18} (N + D)^2) = O(D^{36} (N + D)^2)` (`n <= D` under P2 with two or
more switches). **Holds.** Remark: the certificate of one type suffices for every choice of `T`, so DESC can be run
with one `τ` only.

### 2.5 Lemma W, Lemma D

Lemma W: if the switch `w` of the `P`-consistent side `Y` sat at position `e`, its class would be used on `P` with
the type of `X_e`, which by `P`-consistency is the type of `Y`, so `X_e = Y` (same switch, same type), against
`Y ∉ P`. Then `X_1 .. X_d Y X_c .. X_r` is valid (`w` is new; `Y` has the type of its class on `P` or its class is
not on `P`) and shorter when `c >= d + 3`. The member version is A1. Holds.
Lemma D: the classes of `w` (in `𝒯`) and `v` (in `𝒪`) differ (a valid path uses a class with one type), so P2
applies; its two pairs are `{w^O, v^O}` and `{w^T, v^T}`. Holds.

### 2.6 Theorem Q

Re-derived step by step:
1. *Families.* `𝒯 ∩ 𝒪 = ∅`. `W*` (switches of `𝒯`-classes with `w^O ≠ ∅`, mates included), `V` (all switches of
   `𝒪`-classes), `V* ⊆ V` (those with `v^T ≠ ∅`). `Ω(C, O)` for `C ∈ 𝒯` is exactly `{w^O : w ∈ C ∩ W*}`; likewise
   `Ω(D, T)`.
2. *Empty cases.* `W* = ∅`: `σ_∅` with `τ = O` gives `T` exactly to the classes without `O`-side; every `𝒯`-class
   is one, every `𝒪`-class has its `O`-member; `σ_∅` picks `P`. `V* = ∅` is symmetric with `τ = T`. Correct.
3. *Game.* `V` and `W*` are non-empty (`V* ≠ ∅`). Finite zero-sum game, value `λ`, optimal mixed strategies `p`
   (rows) and `q` (columns) exist (von Neumann): `min_w Σ_v p_v M[v][w] = λ = max_v Σ_w M[v][w] q_w`.
4. *Case `λ >= 1/2`.* With `p`: every column `w ∈ W*` is met with probability `>= 1/2`; `k` independent draws miss a
   fixed `w` with probability `<= 2^{-k}`; union bound over `|W*| <= m` columns: `<= |W*| 2^{-k} < |W*| / m <= 1`
   because `2^k > m` (`k = ⌊log2 m⌋ + 1`). So some draw `v_1..v_k` (from the support of `p`) has `v_i^O` meeting
   every `w^O`, i.e. `Ω(C, O) ⊆ U = ∪ N_O[v_i^O]` for all `C ∈ 𝒯`. Each `v_i^O` is an `O`-side of an `𝒪`-class,
   hence `P`-consistent; by Lemma W (or A1) the members of `P` meeting it lie in a window of 3, so `U` contains at
   most `3k` members of `P`, all of type `O`. A class `D ∈ 𝒪` is misclassified only if `Ω(D, O) ⊆ U`, which needs
   its `O`-member in `U`; distinct classes have distinct members, so at most `3k` misclassified classes, and no
   `𝒯`-class is misclassified. Lemma 2a.1 gives the connecting `σ_U^Φ`.
5. *Case `λ < 1/2`.* `q` gives every row `v ∈ V` payoff `< 1/2`; by Lemma D, for every `v ∈ V` and `w ∈ W*`,
   `[w^T ∩ v^T ≠ ∅] >= 1 - M[v][w]`, so `Pr_q[w^T ∩ v^T ≠ ∅] > 1/2`. Union bound over `|V*| <= m`. Each `w_i^T` is a
   `T`-side of a `𝒯`-class, `P`-consistent; `U = ∪ N_T[w_i^T]` contains `Ω(D, T)` for every `D ∈ 𝒪` and at most `3k`
   `T`-members; at most `3k` `𝒯`-classes are misclassified. Correct. (In this case every `v ∈ V` has `v^T ≠ ∅`: a
   `v` with `v^T = ∅` meets every `w^O` by P2, so its row is all ones and `λ = 1`.)
6. *Algorithm.* `DESC(k, 0, 3k)` enumerates both `τ`, all unions of at most `k` sets `N_τ[Z]` (`Z` over all sides,
   which includes the `Y_i` of the proof; an empty `Y_i` or a repeated one only means fewer sets) and all `Φ` of at
   most `3k` classes; sound by §2.3, complete by steps 2-5. Time `O(2 (2m + 1)^k (m + 1)^{3k} (N + m)^2)`, i.e.
   `m^{O(log m)} · poly(N)`, quasi-polynomial in the input size.
No step uses P2 for a pair it does not cover (only `𝒯`-`𝒪` pairs in Lemma D), ties are the classes themselves, and
the empty sides are handled (an empty `Y_i` meets nothing; `Ω` lists non-empty sides). **Holds.**

### 2.7 Corollary Q

A polynomial (Karp) reduction from 3-SAT to 2CH with classes + P2 maps a formula of size `n` to an instance with
`m, N <= poly(n)`; Theorem Q decides it in `2^{O(log^2 n)}`, so NP ⊆ QP = DTIME(`2^{polylog}`), and under ETH 3-SAT
would have a `2^{o(n)}` algorithm. P2 is checkable in polynomial time, so the problem is a decision problem on
checkable instances. The part about ZZ + P2 rests on Theorem R and its ties version (reviewed in
`verify/r5-review.md` §3.4, not re-checked here): the fixing and the contraction are polynomial, the contraction
has at most as many switches, and its classes are the tie classes of the free switches. **Holds.**

### 2.8 Lemma PP (§2c)

On-path `w` at `a`: `|a - u| >= 2` gives `X'_a ∩ X'_u ≠ ∅` by P2 for `w`, `w_u` (different classes, same type `T`,
`X_a ∩ X_u = ∅` by A1), so `X'_a ∈ N_O[X'_u]`; `|a - u| = 1` is a single side (a `T`-member, as `C ∈ 𝒯`); `a = u` is
excluded (`C ≠ cls(u)`). Mates `w` of `C ∉ {cls(u), cls(b)}`: P2 for `w`, `w_u` and for `w`, `w_b`; `w^T` is
`P`-consistent and not on `P`, so by Lemma W it cannot meet both `X_u` and `X_b` (`|u - b| >= 3`), hence `w^O`
meets `X'_u` or `X'_b` (also when `w^T = ∅`, or when `X'_u = ∅`: then every mate side must meet `X'_b`, and every
`T`-member of another class lies next to `u`). `cls(u)`, `cls(b)` are covered by their groups. The class groups and
single sides are `O`-sides of switches of `𝒯`-classes, so for `D ∈ 𝒪`, `Ω(D, O) ⊆ U` iff every `O`-side of `D`
meets `X'_u` or `X'_b`, i.e. `D ∈ Err(u, b)`. The consequences: `U` has 2 sets `N_O[·]` and at most 2 groups + 4
single sides, so `DESC(2, 6, |Err(u, b)|)` accepts; if no such pair exists, every `T`-member at distance `>= 3`
from the first one shares its class, so at most 3 `𝒯`-classes, and their 3 groups give misclassification 0
(`DESC(0, 3, 0)`). **Holds.** (It gives a polynomial algorithm only together with a bound on `min |Err(u, b)|`,
which the text does not claim.)

## 3. Computations

Recorded 2026-10-28 (round 6c, records only, no new mathematics) from the 40 log files in `verify/rv-classes-q/runs/`
and the scripts in `verify/rv-classes-q/`. All logs were written on 2026-10-22 between 20:22 and 20:38; no file of
the folder is dated later, so whatever the continuations of 2026-10-23 to 2026-10-27 started left no log here.
Own code written from the definitions of `r5-classes.md` §1-§2c (`qcore.py` the model, solvers and descriptions,
`qgen.py`, `qgen2.py` generators, `qchecks.py` the checks of A1-A5, Lemma W, Lemma 2a.1, the proof steps of Theorem
Q, Lemma PP); `r5-classes/` is imported only by `crosscheck_author.py` and `verify/r4-switch-review/` only by
`crosscheck_cor22.py` (§4).

*How to read the logs.* The scripts print their summary at the very end of a run (one JSON line of counters, in
`test_exh`, `test_rand`, `test_planted`, `test_desc_k`, `test_a5`, `crosscheck_*`, `pp_stats`; `hunt_q` prints
progress lines and a final line; `tourn_abstract` one line per size `n`). So a log with its summary is a finished
run. A failed check would appear as a counter `FAIL`, a line `FAILURES n ...`, `SOUNDNESS FAIL`, `COMPLETENESS FAIL`,
`failures n` or `mismatch n` with `n > 0`, and a file `runs/fail-*.json`. **None occurs in any of the 40 logs, and
`runs/` holds no `fail-*.json`.**
*Arguments.* The logs do not record the command line. The arguments below come from the script docstrings, the log
headers and the file names (the tag is the seed). Marks: **(V)** = verified on 2026-10-28 by running the script with
these arguments (many short runs, about 15 minutes of wall-clock in all, the longest 4 minutes, at most 8 processes at
a time, none left running; scripts unchanged): the output equals the log character for character; **(V\*)** = equal
except for counters the script gained after the log was written (see §3.4); **(I)** = inferred, not rerun (reason
given); **(n.r.)** = not recorded in the log and not recoverable. The number of workers `W` does not change any counter
except `desc_yes_runs` and `desc_no_runs` of `test_exh`.
*Finished or cut off.* 38 of the 40 logs are complete (they end with their summary or final line). **Cut off:
`hunt-11-band-h.txt`** (empty, 0 bytes, written 20:31:36; no result). **Ambiguous: `tourn-abstract-2.txt`** (it ends
after `n = 256`; whether larger `n` was requested is not recorded; last write 20:38:07, about two minutes before the
review was stopped). `tourn-abstract-1.txt` ends after `n = 64`, and `-2` continues with larger `n`.

### 3.1 Exhaustive: `test_exh.py N n W [D]`

All instances with nodes `0..N-1` (`s = 0`, `t = 1`), `n` switches with arbitrary sides (empty allowed), every
class partition (one representative per partition shape). On every P2 instance: brute force over the class mode
vectors = path search; on every shortest valid path A1-A4, Lemma W, Lemma 2a.1, the proof steps of Theorem Q for
both types, full covers `<= k`, Lemma PP; on every `D`-th P2 instance `DESC(h, 0, 3h)` accepts yes-instances and
`emin(f, 0)`, `f <= 2`, is recorded, and a DESC run rejects no-instances. All four runs finished; **no failure**.

| Log (bytes; last write) | Arguments | Outcome |
|---|---|---|
| `exh-4-2` (498; 20:22:49) | `test_exh.py 4 2 12 25` **(V)** (`W = 12`, `D = 25` found by running (`W = 1..8`, `D` = 20-100) and by emulating the worker split (`W` = 10, 12, 14, 16, 18, 20, 24, 28, 32 with `D = 25`): only `W = 12`, `D = 25` reproduces `desc_yes_runs` and `desc_no_runs`; all other counters are the same for every `W`) | 65 792 instances, 62 511 with P2 (48 556 yes, 13 955 no), 70 260 shortest valid paths; 1898 yes-runs and 568 no-runs of DESC; max `h` (Theorem Q) 1, max `\|Φ\|` 1, `W_maxwidth` 0 |
| `exh-5-2` (523; 20:23:03) | `test_exh.py 5 2 12 50` **(V)** (rerun 2026-10-28 with the same 48 jobs on 8 processes, 9 s) | 1 049 600 instances, 1 020 075 with P2 (807 490 yes, 212 585 no), 1 162 688 paths; 16 027 yes-runs, 4352 no-runs; max `h` 1, max `\|Φ\|` 1, `W_maxwidth` 0 |
| `exh-3-4` (554; 20:22:47) | `test_exh.py 3 4 12 50` **(I)**: `N = 3`, `n = 4` from the header; `D = 50` from the ratio (122 527 + 2699 DESC runs) / 6 264 607 P2 instances = 1/50.03; `W = 12` as in the two verified runs; not rerun (about 11 M instances) | 10 952 240 instances, 6 264 607 with P2 (6 120 017 yes, 144 590 no), 15 212 210 paths; 122 527 yes-runs, 2699 no-runs; max `h` 2, max `\|Φ\|` 1, max members of `P` in `U` 1, `W_maxwidth` 1, `fullcover_min_max` 2 (`<= k`), `emin(f, 0)` max 1 for `f = 0, 1, 2` |
| `exh-4-3` (597; 20:27:21) | `test_exh.py 4 3 12 200` **(I)**: `N = 4`, `n = 3` from the header; `D = 200` from (55 732 + 3900) / 11 933 205 = 1/200.1; not rerun (about 14 M instances) | 14 079 488 instances, 11 933 205 with P2 (11 165 810 yes, 767 395 no), 21 030 786 paths; 55 732 yes-runs, 3900 no-runs; max `h` 1, max `\|Φ\|` 2, max members in `U` 2, `W_maxwidth` 1, `fullcover_min_max` 1 |

### 3.2 Random instances: `test_rand.py SEED COUNT NMIN NMAX nmin nmax W [plim] [dmax]`

Random instances with classes + P2 (generator `qgen.random_instance`, P2 repaired); every claim as in §3.1 on every
shortest valid path (at most `plim`) and both types; if the number of classes is at most `dmax`: exact hypercube
distance to the solution set, `DESC(h, 0, 3h)` and (for `k <= 3`) `DESC(k, 0, 3k)` accept yes-instances, every DESC
run rejects no-instances. Both finished; **no failure**.

| Log (bytes; last write) | Arguments | Outcome |
|---|---|---|
| `rand-11` (546; 20:25:58) | `test_rand.py 11 20000 ...`: seed and count from the tag and `inst`; `NMIN NMAX nmin nmax W plim dmax` **(n.r.)** (not recoverable from the log; from it: `r_max` 6, all instances had P2, `dmax` at least the largest number of classes) | 20 000 instances (17 944 yes, 2056 no), 43 003 shortest valid paths, 17 944 DESC runs of which 10 560 with `DESC(k, 0, 3k)` (`k <= 3`); max `h` 2, max `\|Φ\|` 2, max members in `U` 3, `W_maxwidth` 2, `fullcover_min_max` 2, `emin(1, 0)`, `emin(2, 0)` max 1, `PP_minErr_max` 1 |
| `rand-12` (534; 20:26:00) | `test_rand.py 12 4000 ...` (as above; `r_max` 4) **(n.r.)** | 4000 instances (3924 yes, 76 no), 13 147 paths, 3924 DESC runs (855 with `DESC(k, 0, 3k)`); max `h` 2, max `\|Φ\|` 2, max members in `U` 2, `W_maxwidth` 2, `fullcover_min_max` 2, `emin(1, 0)`, `emin(2, 0)` max 1, `PP_minErr_max` 0 |

### 3.3 Planted instances: `test_planted.py GEN SEED COUNT W [key=value ...]`

`band` and `inc` generators of `qgen2.py`: the planted path is a shortest valid path (exact search); on all shortest
valid paths (at most `plim`) A1-A4, Lemma W, Lemma 2a.1, Theorem Q for both types (case, centres `h`, `|Φ|`), full
covers `<= k`, Lemma PP; if the number of classes is at most `dmax`: exact DESC (`emin(h, 0) <= 3h`, `emin(k, 0)` if
`k <= 3`, `emin(1, 0)`, `emin(2, 0)`). `COUNT` equals `inst` for `band` and `inst + gen_reject` for `inc`. All 11 runs
finished; **no failure**; in every one `W_maxwidth` = 2 (windows of 3 positions) and `fullcover_min_max <= 3`
(`<= k`). Arguments of all 11 **(V)**: `W` is irrelevant for the output (each instance has its own seed), the
key=value list is the part of the header that differs from the defaults `r=9 nTc=3 nOc=2 mT=4 mO=4 offc=0 ptour=0.5
mates=1 offn=1 pextra=0.5 plim=40 dmax=13 lam=None word=0`.

| Log (bytes; last write) | Arguments after `test_planted.py` | Instances, paths | Extremes (max over the run) |
|---|---|---|---|
| `band-21` (911; 20:29:21) | `band 21 600 W r=10 nTc=3 nOc=2 mT=8 mO=8` | 600, 1236 | `n` 50, `c` 5; `h` 3, `\|Φ\|` 1, members in `U` 3; `PP_minErr` 3 |
| `band-22` (799; 20:35:24) | `band 22 60 W r=12 nTc=6 nOc=3 mT=12 mO=12 plim=4 dmax=12` | 60, 110 | `n` 120, `c` 9; `h` 3, `\|Φ\|` 0, members in `U` 4; `PP_minErr` 3 |
| `band-23` (1015; 20:33:09) | `band 23 300 W r=14 nTc=8 nOc=3 mT=3 mO=3 offc=3 dmax=12` | 300, 887 (279 DESC runs: `c <= 12`) | `n` 53, `c` 14; `h` 3, `\|Φ\|` 3, members in `U` 3; `PP_minErr` 3 |
| `band-24` (800; 20:34:16) | `band 24 120 W r=8 nTc=2 nOc=2 mT=16 mO=16 plim=3 dmax=8` | 120, 180 | `n` 72, `c` 4; `h` 3, `\|Φ\|` 0, members in `U` 3; `PP_minErr` 2 |
| `band-25` (842; 20:34:18) | `band 25 200 W r=20 nTc=4 nOc=3 mT=3 mO=3 plim=6 dmax=10` | 200, 305 | `n` 41, `c` 7; `h` 2, `\|Φ\|` 1, members in `U` 3; `PP_minErr` 3 |
| `band-26` (748; 20:36:58) | `band 26 32 W r=8 nTc=1 nOc=1 mT=40 mO=40 plim=2 dmax=4` | 32, 36 | `n` 88, `c` 2; `h` 3, `\|Φ\|` 0, members in `U` 3; `PP_minErr` 0 |
| `band-27` (784; 20:36:54) | `band 27 24 W r=8 nTc=2 nOc=2 mT=24 mO=24 plim=2 dmax=6` | 24, 31 | `n` 104, `c` 4; `h` 3, `\|Φ\|` 0, members in `U` 2; `PP_minErr` 2 |
| `inc-31` (1102; 20:33:14) | `inc 31 800 W r=8 nTc=3 nOc=3 offc=1 word=3` | 584 (+216 rejected), 2748 | `n` 15, `c` 7; `h` 2, `\|Φ\|` 4, members in `U` 5; `PP_minErr` 5 |
| `inc-32` (1131; 20:33:35) | `inc 32 400 W r=10 nTc=4 nOc=3 mates=2 offc=1 word=2` | 287 (+113), 4903 | `n` 25, `c` 8; `h` 3, `\|Φ\|` 4, members in `U` 6; `PP_minErr` 4 |
| `inc-33` (1080; 20:33:53) | `inc 33 400 W r=12 nTc=5 nOc=5 word=2` | 255 (+145), 1941 | `n` 21, `c` 9; `h` 3, `\|Φ\|` 4, members in `U` 6; `PP_minErr` 5 |
| `inc-34` (950; 20:34:36) | `inc 34 400 W r=12 nTc=2 nOc=2 mates=2 word=2 plim=20` | 311 (+89), 1753 | `n` 20, `c` 4; `h` 2, `\|Φ\|` 2, members in `U` 6; `PP_minErr` 2 |

The extremes respect the bounds asserted by the checks (`qchecks.check_theorem_q`: at most 3 members of `P` per
centre, at most `3h` members in `U`, `|Φ| <= 3h <= 3k`, at most `k` centres). In `inc-34` and in the `desck-inc-*`
runs of §3.4 `Q_h_max` is 2 and `Q_members_in_U_max` is 6 (and `Q_phi_max` is 6 in `desck-inc-42`, `-44`, `-45`), so
the bounds `3h` are attained there. Every log also ends with the histogram of the triples (case, `h`, `|Φ|`); none has
`|Φ| > 3h`.

### 3.4 `DESC(k, 0, 3k)` with the parameters of Theorem Q where it is not a brute force: `test_desc_k.py KIND SEED COUNT W args`

`k = ⌊log2 m⌋ + 1`; instances with more than `3k` classes are non-degenerate (otherwise the descriptions with `3k`
flips contain every class set). Per instance: `DESC(k, 0, 3k)` run as an algorithm must accept iff the instance is
a yes-instance (exact answer from all `2^c` mode vectors); `emin(1, 0)`, `emin(1, 1)` recorded; on yes-instances the
proof construction of Theorem Q on up to 10 shortest valid paths, both types; since a later edit of the script, also
variants made by deleting nodes (counters `variant_yes`, `variant_no`, `variant_nondegenerate`; `DESC(k, 0, 3k)` =
exact answer on each). All 7 runs finished; **no failure**; every instance planted (all yes). `args` of `band` =
`r nTc nOc mT mO offc`, of `inc` = `r nTc nOc mates offc`. Arguments of all 7 **(V)** or **(V\*)**: the logs of 41,
42, 43, 44 predate the `variant_*` counters (the script was edited at 20:33); the rerun gives identical counters plus
`variant_*` (41: 1 yes, 4 no; 42: 94 yes, 1 no; 43: 4 no; 44: 40 yes, 1 no); 45, 46, 47 identical.

| Log (bytes; last write) | Arguments after `test_desc_k.py` | Instances, paths | Outcome |
|---|---|---|---|
| `desck-band-41` (594; 20:31:59) | `band 41 200 W 16 12 3 0 0 4` (V\*) | 200 yes, 424 | `c` up to 17, `n` up to 24, 43 non-degenerate (`c > 3k`), 157 degenerate; `Q_h_max` 1, `Q_phi_max` 3; `emin(1, 0)` max 1, `emin(1, 1)` max 0 |
| `desck-inc-42` (676; 20:32:15) | `inc 42 300 W 10 8 8 0 8` (V\*) | 170 yes (+130 rejected), 1639 | `c` up to 18, `n` 18; 69 non-degenerate, 101 degenerate; `Q_h_max` 2, `Q_phi_max` 6, members in `U` 6; `emin(1, 0)` max 2, `emin(1, 1)` max 1 |
| `desck-band-43` (588; 20:32:42) | `band 43 100 W 20 15 3 0 0 3` (V\*) | 100 yes, 178 | `c` up to 19, `n` 26; 58 non-degenerate, 42 degenerate; `Q_h_max` 1, `Q_phi_max` 2; `emin(1, 0)` max 1, `emin(1, 1)` max 0 |
| `desck-inc-44` (619; 20:33:15) | `inc 44 200 W 12 9 9 0 9` (V\*) | 71 yes (+129), 702 | `c` up to 20, `n` 21; 62 non-degenerate, 9 degenerate; `Q_h_max` 2, `Q_phi_max` 6, members in `U` 6 |
| `desck-inc-45` (695; 20:33:53) | `inc 45 300 W 10 8 8 0 8` (V) | 154 yes (+146), 1469 | `c` up to 18; 51 non-degenerate, 103 degenerate; `Q_phi_max` 6; variants: 81 yes, 6 no (29 non-degenerate) |
| `desck-band-46` (608; 20:34:04) | `band 46 150 W 16 12 3 0 0 4` (V) | 150 yes, 274 | `c` up to 17; 31 non-degenerate, 119 degenerate; `Q_phi_max` 2; variants: 2 no |
| `desck-inc-47` (600; 20:34:10) | `inc 47 200 W 9 4 4 1 6` (V) | 119 yes (+81), 1156 | `c` up to 13, `n` 22; all 119 degenerate; `Q_phi_max` 5, members in `U` 6; variants: 59 yes |

So `DESC(k, 0, 3k)` agrees with the exact answer on the 964 planted instances of the seven logs (200 + 170 + 100 + 71
+ 154 + 150 + 119), of which 314 are non-degenerate (`c > 3k`: 43 + 69 + 58 + 62 + 51 + 31), and on 148 node-deletion
variants recorded in the logs of 45, 46, 47 (140 yes, 8 no).

### 3.5 Class search (A5): `test_a5.py SEED COUNT`

Soundness: every accepted walk of the class search (stored (class, type) pairs, at most `B`, certificate `K`) is a
valid walk and the instance is a yes-instance, for 6 random `(K, B)` per instance; completeness analogue: a valid
path with `Π(X) ⊆ K` for its members and at most `B` stored pairs is accepted. Both finished; **no failure**
(`fail` 0).

| Log (bytes; last write) | Arguments | Outcome |
|---|---|---|
| `a5-1` (91; 20:30:42) | `test_a5.py 1 3000` **(V)** | 2988 instances (12 rejected by the generator), 17 928 runs, 3962 accepted, 492 no-instances, 5656 completeness checks, `fail` 0 |
| `a5-2` (93; 20:31:02) | `test_a5.py 2 6000` **(V)** | 5963 instances, 35 778 runs, 7864 accepted, 1001 no-instances, 11 304 completeness checks, `fail` 0 |

### 3.6 Adversarial hill climbing against Theorem Q and Lemma PP: `hunt_q.py SEED STEPS START OBJ [key=value]`

Mutates a planted instance (fresh node in two sides, node added or removed, a P2 pair re-oriented) while P2 holds and
`P` stays a shortest valid path, maximising `OBJ` on `P`; every improved instance is checked with the full proof
construction (both types) and Lemma PP on all its shortest valid paths. `START` = `band` or `inc`; `OBJ`: `h`
(centres used by the proof), `full` (least number of centres any cover needs), `phi` (ratio `|Φ| / 3h`), `err`
(least `|Err(u, b)|` of Lemma PP). A failure would print `FAIL ...` and stop. The logs do not record `STEPS` and the
`key=value` start parameters **(n.r.)**; `SEED`, `START`, `OBJ` are from the file names; `n`, `c`, `k` of the best
instance and `r_max` are in the log. Not rerun (each run is several minutes).

| Log (bytes; last write) | Arguments (seed, start, objective from the name) | State | Outcome |
|---|---|---|---|
| `hunt-11-band-h` (0; 20:31:36) | `hunt_q.py 11 ... band h` | **cut off** (empty file: no progress line, no final line) | none |
| `hunt-12-band-full` (25 247; 20:33:30) | `hunt_q.py 12 ... band full`; `r_max` 10 | finished | one progress line (`step 80 best 3`, `n` 50, `c` 5, `k` 6, `N` 1038, 1 s); `final best 3`, 2291 accepted moves, 2 improved instances checked (25 paths); max `h` 3, max `\|Φ\|` 0; on the visited instances the least cover needs at most 3 of `k = 6` centres |
| `hunt-13-inc-phi` (8895; 20:32:16) | `hunt_q.py 13 ... inc phi`; `r_max` 10 | finished | progress `step 27 best 0.334`, `307: 0.335`, `2665: 0.503` (`n` 16, `c` 6, `k` 5, `N` 1009, 33 s); `final best 0.503`, 2254 accepted moves; max `h` 2, max `\|Φ\|` 3 (consistent with ratio 3/6 = 0.5 plus the tie-break of the objective) |
| `hunt-14-inc-err` (8606; 20:32:33) | `hunt_q.py 14 ... inc err`; `r_max` 10 | finished | progress `step 820 best 1` (`n` 20, `c` 5, `k` 5), `step 1550 best 2` (25 s); `final best 2`, 2061 accepted moves; max `h` 2, max `\|Φ\|` 2 |
| `hunt-15-inc-h` (10 199; 20:31:58) | `hunt_q.py 15 ... inc h`; `r_max` 9 | finished | no progress line; `final best 0`, 2420 accepted moves; max `h` 1, max `\|Φ\|` 0 |
| `hunt-16-inc-phi` (8054; 20:31:38) | `hunt_q.py 16 ... inc phi`; `r_max` 12 | finished | no progress line; `final best 0.0`, 2192 accepted moves; max `h` 2, max `\|Φ\|` 2 |

No hunt found a violated claim (no `FAIL`); the climb did not exceed the bounds (`|Φ| <= 3h`, `h <= k`) in any run.
The final line of each finished log holds the best instance as JSON (`N` up to 2313 nodes) and the path `P`.

### 3.7 Lemma PP statistics: `pp_stats.py SEED COUNT r nTc nOc mates offc`

The least `|Err(u, b)|` over all admissible pairs, per shortest valid path and type, and per instance the least over
its paths and types (not a claim of `r5-classes.md`: Lemma PP gives `DESC(2, 6, |Err(u, b)|)`, and the text claims
no bound on `min |Err|`). All three finished (arguments **(V)**).

| Log (bytes; last write) | Arguments | Outcome |
|---|---|---|
| `pp-51` (274; 20:35:25) | `pp_stats.py 51 300 8 3 3 1 1` | 281 instances, 6440 checked pairs, 1165 fallbacks (no pair); least `\|Err\|` per (path, type): 0: 567, 1: 298, 2: 477, 3: 208, 4: 3, no pair: 1165; per instance (0 = fallback with misclassification 0): 0: 265, 1: 11, 2: 5 |
| `pp-52` (281; 20:35:51) | `pp_stats.py 52 200 12 5 5 1 0` | 106 instances, 14 892 pairs, 436 fallbacks; per (path, type): 0: 374, 1: 362, 2: 282, 3: 71, 4: 50, 5: 11, no pair: 436; per instance: 0: 93, 1: 10, 2: 3 |
| `pp-53` (269; 20:35:56) | `pp_stats.py 53 200 10 4 3 2 1` | 153 instances, 22 801 pairs, 1490 fallbacks; per (path, type): 0: 1137, 1: 647, 2: 373, 3: 107, 4: 12, no pair: 1490; per instance: 0: 143, 1: 10 |

### 3.8 Remark (2), abstract part: `tourn_abstract.py SEED TRIALS n [n ...]`

For random bipartite tournaments (rows and columns, each pair oriented at random) the least number of rows covering
all columns, and of columns covering all rows; the log gives `min(hR, hC)` (min, median, max over the trials) next to
`⌊log2 n⌋ + 1`. Arguments **(V)**: the two runs reproduce the logs exactly.

| Log (bytes; last write) | Arguments | Outcome (min / median / max of `min(hR, hC)`; `⌊log2 n⌋ + 1`) |
|---|---|---|
| `tourn-abstract-1` (393; 20:36:28) | `tourn_abstract.py 1 40 4 8 16 32 64` | `n = 4`: 1 / 2 / 2 (3); `n = 8`: 1 / 2 / 2 (4); `n = 16`: 2 / 2 / 3 (5); `n = 32`: 2 / 3 / 3 (6); `n = 64`: 3 / 3 / 3 (7); ends after `n = 64` |
| `tourn-abstract-2` (160; 20:38:07) | `tourn_abstract.py 2 10 128 256` (V; larger sizes may have been requested, **ambiguous**) | `n = 128`: 3 / 4 / 4 (8); `n = 256`: 4 / 4 / 4 (9) over 10 trials each |

### 3.9 Scripts without a log

`selftest.py SEED COUNT` (the solvers of `qcore` and `qchecks` against each other), `try_inc.py`, `try_planted.py`
(development helpers for the acceptance rate of the generators) have no log in `runs/`; the libraries `qcore.py`,
`qchecks.py`, `qgen.py`, `qgen2.py` are imported by the scripts above.

## 4. Cross-checks

Both finished; **no failure** (recorded 2026-10-28; arguments **(V)**).

| Log (bytes; last write) | Script, arguments | Outcome |
|---|---|---|
| `crosscheck-author-1` (88; 20:34:50) | `crosscheck_author.py 1 3000` (imports `r5-classes/ccore.py`, read only; the only script that does) | 2977 instances (random instances with classes, 80%, and planted ones), 2626 with P2, 2381 yes, 5792 shortest valid paths, 11 908 class searches; `mismatch` 0: same P2 verdict, same yes/no, same shortest length and same set of shortest valid paths, and the same acceptance of the class search for 4 random `(K, B)` per instance |
| `cor22-1` (268; 20:29:14) | `crosscheck_cor22.py 1 600 W` (`W = 8` used for the rerun; the output does not depend on `W`; imports `verify/r4-switch-review/`, read only) | 3695 instances, 8852 (path, type) checks of Corollary 2a.2: the certificate `K_T` of Lemma 7 (swap, 388 times) or Theorem 8 (steps 0-3) contains the partners of all `T`-members, `mis_P(K_T)` = storage `\|P ∩ K_T\|`, `σ_{K_T}^Φ` picks the path and connects, and the shape lies in `DESC(6, 12, 18)`; max storage 7, max sets `N_O[Z]` 3, max single sides 2; `failures 0` |
| `cor22-2` (268; 20:29:18) | `crosscheck_cor22.py 2 600 W` | 3524 instances, 8424 checks; max storage 9, max sets 4, max single sides 2; `failures 0` |

The extremes (storage 9 against 18, 4 sets against 6, 2 single sides against 12) stay inside the shape of
`DESC(6, 12, 18)`. Supports §1 row "Corollary 2a.2" and §2.4.

## 5. Remarks

Not written: the review was stopped on 2026-10-22 about 20:40, after the computations above, and no later round
resumed it. The two items of §1 that refer to this section rest on: (i) "Theorem Q is non-trivial only when the
number of classes exceeds `3k`": the runs of §3.4 count the non-degenerate instances (`c > 3k`) and check
`DESC(k, 0, 3k)` on them; (ii) "Remark (2) holds as a statement about the minimax argument only": the numbers of
§3.8. No log contradicts a verdict of §1.

## 6. Not checked

Not written by the reviewer (see §5). From the text of this report: the ZZ + P2 part of Corollary Q rests on Theorem
R and its ties version, reviewed in `verify/r5-review.md` §3.4 and not re-checked here (§2.7); Corollary 2a.2 uses
Lemma 7 and Theorem 8 of `r4-switch` as reviewed in `verify/r4-switch-review.md`, and §4 checks the resulting
certificates, not those two statements; no result of `hunt-11-band-h` exists; the arguments of `rand-11`,
`rand-12` and of the `hunt-*` runs are not recoverable (§3).
