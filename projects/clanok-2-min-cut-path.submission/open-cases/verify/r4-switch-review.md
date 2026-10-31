# Adversarial review of r4-switch.md (version 2, 2026-10-18): is 2CH + P2 in P?

Status: complete, 2026-10-18. Reviewer: agent verify-r4-switch. Scripts and logs: `verify/r4-switch-review/`
(own code written from the definitions of r4-switch.md §1-§4; `r4-switch/` is imported only by `crosscheck.py`, §4).
Labels: **holds**, **holds with repair**, **gap**, **false**; computations with script, seed, sizes, counts, outcome.

**Overall verdict: the proof is correct and complete; 2CH + P2 is in P by Theorem 10 as written, with no repair
needed.** Every step of §§1-4 was re-derived; no counterexample was found to any step, on 17.1 million shortest valid
paths of exhaustive instances and about 283,000 shortest paths of random and adversarial instances (§3), including
3,032 certificates built in step (3) of Theorem 8 (forward and backward rows, two disjoint spans, 945 holes, hole
single sides) and 5,208 swaps of Lemma 7.
Remarks that do not affect correctness: §2.6 (exponent `122 → 74`), §5 (wording, evidential value of one check).

## 1. Verdicts

| Statement | Verdict | Notes |
|---|---|---|
| §1 setting (valid path ⇔ yes-instance; a valid walk certifies yes) | holds | §2.1 |
| F1, F2, F3, F4 | holds | F3 does not need the distance condition |
| Lemma 1 and the three kinds | holds | |
| Lemma 2 | holds | |
| Lemma 3 | holds | also for an empty `X'_q` |
| Theorem 4 | holds | |
| Theorem 5 (1)-(3) | holds | soundness for every `K` and `B`, by a two-line argument |
| Theorem 11 | holds | not used by Theorem 10 |
| S1-S3 | holds | |
| Lemma 7 | holds | |
| Theorem 8 | holds | only the absence of a `T`-straddle is used for the `T`-certificate; the bounds can be lowered (§2.6) |
| Corollary 9 | holds | |
| Theorem 10 and its running time | holds | `O(D^{122})` is correct as stated; the exponent drops to about 74 with the remark of §2.6 |
| Computational record of r4-switch.md §6 | reproduced where re-run | the exhaustive counts agree exactly (§3.1); the `decide_full` row is weaker evidence than it reads (§5) |

Computations: §3; cross-check with the author's code: §4; remarks: §5; not checked: §6.

## 2. Line-by-line reading

### 2.1 Setting

A shortest sequence of picked sides from `s` to `t` has no repeated side, and one mode vector picks one side per
switch, so its switches are distinct: it is a valid path. Conversely the sides of a valid path lie on distinct
switches and are picked by one mode vector. A valid walk has no two partner sides, so its sides are picked by one mode
vector (other switches arbitrary), and consecutive sides meet. `s = t` is answered yes outside the algorithm; `s` or
`t` in no side gives no start state and the answer no, correctly. Sides are non-empty by definition; a switch with
both sets empty has no side and, for `n >= 2`, violates P2. A switch whose two sides meet or coincide gives two
distinct sides that are partners; nothing in the proofs uses `X_a ∩ X'_a = ∅` (contacts exclude `c = a`, and S3
excludes `X_a` by its type). **Holds.**

### 2.2 F1-F4, Lemmas 1-3

F1: the shortcut `X_1 .. X_a X_b .. X_r` keeps distinct switches. F2: of the two P2 pairs for `w_a != w_b`, the
same-type pair is `{X_a, X_b}` (disjoint by F1), so the other pair `{X'_a, X'_b}` meets; in particular both are
non-empty. F3: the P2 pairs are `{X_a, X'_b}` and `{X'_a, X_b}`; with an empty partner the corresponding pair is
empty and the other holds. F3 needs only `a != b`. F4: immediate; length `d + k + r - c + 1 >= r`.

Lemma 1: F4 with `Y_1 = X'_a`; `w_a` sits at `a ∈ (d, c)`, so it is none of `w_1..w_d, w_c..w_r`; `c - d <= 2` and
`d < a < c` force `d = a - 1`, `c = a + 1`. Kinds: a contact `>= a + 2` and a contact `<= a - 1` would contradict
Lemma 1, and symmetrically, so the three kinds are exclusive and exhaustive.

Lemma 2(a): with `d < b` a contact of `b` and `c >= a + 2` a contact of `a`, `d < b < a < c`, the two inserted sides
`X'_b`, `X'_a` belong to `w_b != w_a`, both at positions in `(d, c)`; F4 gives `2 >= c - d - 1 >= a - b + 2 >= 3`.
(b) is the mirror image (F4 between `X_c` and `X_d`, inserted order `X'_a`, `X'_b`); the arithmetic
`d - c - 1 >= (b + 1) - (a - 2) - 1` is right. Lemma 3: F3. **All hold.**

### 2.3 Theorem 4

(a) `q_b != q_f` (exclusive kinds); if `q_b <= q_f - 2`, F2 gives meeting partners, Lemma 2(a) with `a = q_f`,
`b = q_b` says `q_b` has no contact `< q_b`, contradicting that it is backward. (b) contacts of the forward `q_f` are
`>= q_f + 1`, so `a <= q_f - 2` is not a contact of `q_f`, `|a - q_f| >= 2`, Lemma 3. Mirror for `q_b`. (c) an
`O`-member strictly between is neither forward (`> q_f`), backward (`< q_b`) nor local. If both `q_f = -∞` and
`q_b = +∞`, some `O`-member exists and is non-local, a contradiction, so at least one is finite. **Holds.**

### 2.4 Theorem 5 and Theorem 11

(1) If `Y_i`, `Y_j` (`i < j`) are partners, (i) at `j` and at `i` puts both in `K`, so `Y_i = Y'_j` is a stored side
at step `j`, contradicting (ii). The argument uses nothing about `K`, `B`, minimality or repetitions, so **every**
K-admissible walk, for every `K` and `B`, is a valid walk; the algorithm can therefore never answer yes on a
no-instance. (2) (ii) holds on a valid path whatever the order of its members, since it contains no partner pair;
(i) and (iii) are the hypotheses. (3) The conditions at step `j` read only `Y_j` and the stored set, the stored set
grows monotonically, so (iii) on the final set is (iii) at every step; at most `D · Σ_{i<=B} C(|K|, i)` states.
**Holds.**

Theorem 11: at the first occurrence of `X` (step `i`) the partner `X'` (non-empty) is either in `K`, or declared
(no other alternative: `X' ∈ Dc` needs an earlier `X`); declared sides stay in `Dc` and are refused; if `X' ∈ K`, then
`X ∈ K` is forced (a side in `K` cannot declare, and `X ∈ Dc` needs an earlier `X'`), `X` was stored at step `i`, and
`X'` is refused at step `j` because its partner is stored. If `X ∈ K` and `X' ∉ K`, `X` itself is refused. **Holds**
(it is not used for Theorem 10).

### 2.5 S1-S3, Lemma 7

S1: a valid path contains no partner of its members. S2: by F1 only positions `c - 1, c, c + 1` meet `X_c`. S3: a
member of type `O` meeting `X'_a` is an `X_c`, `c ∈ f(a)`, and conversely; `X_a` has type `T`. Hence the storage of
a union of sets is at most the sum of the storages, and storage is counted correctly for the union `K_E ∪ K_F`
(it is `|P ∩ K| <= storage(K_E) + storage(K_F)`). **Holds.**

Lemma 7. The definition puts `p` outside `[x_1, x_2]` and `x` outside `[p_1, p_2]`, and the two removed open
intervals are disjoint (`x_2 < p_1` or `p_2 < x_1`). `Q` keeps the positions `M`, inserts `X'_p` (non-empty, it meets
`X_{x_1}`) and `X'_x`; the four new junctions are the four hypotheses; `w_p`, `w_x` are distinct (opposite types at
distinct positions) and lie at removed positions, so all switches are distinct; `1, r ∈ M`. The length is
`r - (x_2 - x_1 - 2) - (p_2 - p_1 - 2)`, both brackets are `>= 0`, so minimality forces both to vanish. Then `Q = P*`
literally (the kept blocks are everything except `x` and `p`). Types are kept position by position, the partners of
`P*` are as stated, and F1, F2 hold for `P*` because it is a shortest valid path. Certificates: `c` a `T`-member of
`P*`, `|c - x| >= 2`: F2 for `P*` with `Y'_x = X_p`; `c = x`: `X_p ∈ N_O[X_p]`; `c = x ± 1`: these positions are
`T`-members (`x_1`, `x_2`). Storage of `N_O[X_p]` in `P*`: `Y_x` has type `T`; an unchanged `Y_c = X_c` meets `X_p`
only for `|c - p| <= 1` (F1 for `P`); `Y_p` counts; so at most 3. Mirror for the `O`-certificate. **Holds.**

### 2.6 Theorem 8, Corollary 9, Theorem 10

Steps (0)-(2) are right as written (step (1) uses F2 for `|b - a| >= 2` and S3; step (2) uses Lemma 3 and S2; after
step (1) no `T`-member is local since `f(a)` is contained in the contacts). If there is no `T`-member at all the
empty set is a `T`-certificate; the text then still produces a (larger) valid certificate, which is harmless.

Step (3). Theorem 4 applies (no local `O`-member, some `O`-member). Coverage outside `[q_f - 1, q_b + 1]` by
Theorem 4(b); the positions `q_f`, `q_b` are `O`-members; if `q_b = q_f - 1` the window contains no `T`-member.
(F0): `a ∈ R` gives `a + 1 > q_f`, so `a + 1 .. q_b - 1` lie in `R` and are `T`-members; `f(a)` is contained in the
contacts of the forward `a`, all `>= a + 1`, hence in `C`; `a != q_b - 1` gives `a <= q_b - 2 <= p - 2`.
(F1→) is F3. (F2→): `x_1, x_2 ∈ b(p) ⊆ R` are `T`-members, `p_1, p_2 ∈ f(a)` are `O`-members around `p`, and
`x_2 < q_b <= p_1`: the definition of a `T`-straddle is met exactly. (F3→): a hole owner `a` lies in `b(p)` and, with
no straddle, is its least or largest element; so at most two owners per `p`. (F4→): correct; the Erdős-Szekeres step
is valid but not needed, see the remark below. (F5→): the greedy piercing argument is the standard one: if `a` and a
later `a'` both add a point, `max f(a) <= max f(a')` and `max f(a)` was in `H` when `a'` was processed, so
`max f(a) < min f(a')`; the adding spans are pairwise disjoint. For each `a ∈ A`, a point `h ∈ H` in its span is
either in `f(a)` or a hole of `a` (the span ends are in `f(a)`), at most 2 owners per `h`. The backward half
(B0)-(B5) is the mirror image under reversal of the path (which swaps forward and backward kinds and the roles of
`q_f`, `q_b`); I re-derived each line: (B0) `a >= q_f + 2 >= p + 2`; (B2) `p_2 <= q_f < x_1`, the second alternative
of the straddle definition. Counting: `2 + 4 + 4 = 10` sets, `2 + 9 + 9 = 20` single sides, storage `<= 3` per set.
Every `T`-member is covered (the last sentence of the proof lists all cases). **Holds.**

What is actually used: the `T`-certificate needs only the absence of a `T`-straddle (all straddles produced in (F2→)
and (B2) are `T`-straddles). Corollary 9 is right as stated (if a straddle of either type exists, Lemma 7 for that
type gives both certificates of `P*`).

*Remark (not an error; lowers the exponent).* (F4→) holds already for **three** elements: if `a_i, a_j, a_k ∈ A`
have pairwise disjoint spans, let `a_j` be the middle one **by position**; an inner element `p` of `f(a_j)` (it
exists, `|f(a_j)| >= 3`) is in no `f(a_i)`, `f(a_k)`, so `a_i, a_k ∈ b(p)` by (F1→), and (F2→) gives a straddle. The
order of the spans plays no role, so the Erdős-Szekeres theorem is not needed, and `|H|, |H'| <= 2`. With this,
Theorem 8 gives at most `2 + 2 + 2 = 6` sets and `2 + 5 + 5 = 12` single sides per type, storage `<= 18`, `B = 36`,
and the running time becomes `O(D^{74})` instead of `O(D^{122})` by the same count. (Checked: §3, the maximum number of
pairwise disjoint spans observed is recorded in each run.)

Corollary 9: by Lemma 7 or Theorem 8. Theorem 10: on a yes-instance, the certificate of Corollary 9 has the shape
enumerated (each part a union of `<= 10` sets `N_O[Z]` with `Z` a side and `<= 20` single sides; `B = 60` bounds its
storage, and Theorem 5(2) needs only `|P ∩ K| <= B`). On a no-instance every run rejects by Theorem 5(1). Running
time: `Σ_{i<=10} C(D, i) · Σ_{j<=20} C(D, j) <= (D + 1)^{30}` choices per type, at most `D (D + 1)^{60}` states per
search with `D` transitions: `O(D^{122})`, polynomial. **Holds.**

## 3. Computations (own code; logs in `verify/r4-switch-review/runs/`)

Own code: `core.py` (instances, P2, brute force over mode vectors with union-find, enumeration of **all** shortest
valid paths, the search of Theorem 5), `proof.py` (every claim of §§2-4 as an assertion on a given shortest path),
`alg.py` (the algorithm of Theorem 10 with parameters `kd`, `ks`, `B`), generators `planted.py`, `gen_run.py`,
`families.py`. `proof.check_path` asserts on a path: F1, F2, F3; F4 for every detour of 1 and 2 sides of the
instance; Lemma 1 and the kind properties; Lemma 2 (a), (b) for all pairs; Lemma 3 for all pairs; Theorem 4 (a)-(c)
for both types whenever its hypotheses hold; S1, S2, S3; it enumerates **every** straddle of both types and checks
Lemma 7 on each (tightness, `Q = P*` literally, `P*` valid of length `r`, types kept, both certificates cover, storage
`<= 3` each, search accepts with `B` = storage); for each type `T` **without `T`-straddle** it runs steps (0)-(3) of
Theorem 8 with an assertion for each claim ((0); no local `T`-member after (1); Theorem 4 applies in (3); `R`
non-local; (F0)/(B0) both parts; `q_b` resp. `q_f` finite when rows exist; (F1→)/(B1) for all pairs; hole bound and
"hole owner is extreme in `b(p)`" for every `p ∈ C`; at most 4 pairwise disjoint spans, with the maximum recorded;
greedy `H` of size `<= 4` inside `C`; each chosen non-member `h` is a hole; all of `R` covered), then checks coverage of
every `T`-member, counts (`<= 10` sets, `<= 20` single sides), storage `<= 30` and `<= 3` per set; finally it builds
the certificate of Corollary 9 and runs the search with `K` = the certificate and `B` = its exact storage, which must
accept with a valid walk (re-checked by `is_valid_walk`).

### 3.1 Exhaustive (all instances; `s = 0`, `t = 1`; every side any subset including empty; multisets of switches)

Script `exhaustive.py N n 24 50` (`28 200` for `3 5`). On each P2 instance: brute force = own path search; all
shortest paths checked; on no-instances the search is run with **every** `K ⊆` sides and `B ∈ {0, 1, 2, D}` when
`D <= 6` (else 7 sets `K`, `B ∈ {1, D}`) and must reject; on every 50th (200th) yes-instance `alg.decide` is run with
the parameters `(kd, ks, B)` of the proof's certificate and must accept.

| N, n | instances | P2 | yes / no | shortest paths | searches on no-instances | decide runs | failures |
|---|---|---|---|---|---|---|---|
| 3, 2 | 2,080 | 1,715 | 1,382 / 333 | 2,056 | 16,672 | 1 | 0 |
| 3, 3 | 45,760 | 29,197 | 27,544 / 1,653 | 55,466 | 306,112 | 522 | 0 |
| 3, 4 | 766,480 | 360,964 | 354,927 / 6,037 | 931,182 | 328,190 | 7,069 | 0 |
| 3, 5 | 10,424,128 | 3,511,975 | 3,493,748 / 18,227 | 11,432,220 | 334,986 | 17,440 | 0 |
| 4, 2 | 32,896 | 29,615 | 24,182 / 5,433 | 35,348 | 302,560 | 354 | 0 |
| 4, 3 | 2,829,056 | 2,170,357 | 2,073,700 / 96,657 | 4,052,958 | 20,513,728 | 41,358 | 0 |
| 5, 2 | 524,800 | 495,275 | 408,980 / 86,295 | 595,264 | 5,110,144 | 7,695 | 0 |

The rows `3,2`, `3,3`, `4,2`, `4,3` reproduce the counts of r4-switch.md §6 exactly (P2 instances, yes/no, paths).
These instances exercise the degenerate cases (empty sides, coinciding sides, a side with both `s` and `t`, `s`, `t`
in several sides, switches whose sides meet), but only steps (0)-(2): a shortest path has at most `N - 1` sides.

### 3.2 Random and adversarial instances

| Script, arguments (seed, size) | Instances / paths | What is reached | Outcome |
|---|---|---|---|
| `selftest.py 1 3000`, `2 20000` | 23,000 random (with and without P2) | path solver = brute force; full search (`K` = all, `B = D`) = brute force; 5 random `(K, B)` each never accept a no-instance | 0 failures |
| `test_random_par.py 31 280 500 10 10 28` | 140,000 random P2 (`N <= 10`, `n <= 10`); 202,341 paths | steps (0)-(2), 28 swaps | 0 failures; 183,620 searches on 45,905 no-instances reject |
| `test_random_par.py 32 140 200 16 14 28` | 28,000 random P2 (`N <= 16`, `n <= 14`); 56,801 paths | steps (0)-(2), 4 swaps | 0 failures |
| `test_planted.py 21 600 strad 28` | 685 planted, 832 paths | straddles planted: 564 swaps | 0 failures |
| `test_planted.py 22 600 off 28`; `23 400 sat 28` | 184 + 948 planted (off-path switches; saturation), 367 + 1,346 paths | 484 swaps, 44 step-(3) certificates | 0 failures |
| `test_run.py 11 1200 28`; `42 1500 28`; `51 1500 28` | 2,888 + 3,832 + 3,801 critical-run instances (path length up to 19, up to 21 switches, half of them reversed), 11,415 paths | 1,845 step-(3) certificates; 640 holes; hole single sides used 5 times (counted only in `51`); 1,448 swaps; up to 4 sets `N_O[Z]`, 2 disjoint spans | 0 failures |
| `test_run.py 12 600 28 sat` | 1,446 saturated critical-run instances, 1,635 paths | 277 step (3), 81 holes, 220 swaps | 0 failures |
| `test_two.py 41 600 28`; `52 900 28` | 3,194 + 4,742 instances whose rows split into two groups with spans in disjoint halves of `C`, 8,842 paths | 863 step (3), a piercing set H of size 2 and 2 pairwise disjoint spans reached, 204 holes, hole single sides used 4 times (counted only in `52`), 2,460 swaps | 0 failures |
| `families.py 12 6` | `R_L`, its Helly form, `cut(L, k)`, `tflip(L, k)`, `2 <= L <= 12` (165 instances, 22 yes) | `R_L` certificate: step (1) for both types, storage `<= 6`; P2 on all | 0 failures; `decide(1, 1, 8)` rejects the no-variants for `L <= 6`, the full search rejects all 143; `decide` at the proof parameters accepts `R_L` and Helly `R_L`, `L <= 6` |
| `test_t11.py 1 4000` | 4,000 random (70% P2), 48,000 runs of the declaration search (6 random `(K, B, s)` each, lazy and nondeterministic-eager reading of the rule) | 25,162 accepted walks | every accepted walk valid; none on the 1,292 no-instances |

Observed maxima over all runs: storage of a `T`-certificate 10, total storage 13, sets `N_O[Z]` per type 4, single
sides per type 2, pairwise disjoint spans 2 (never 3, as the remark of §2.6 predicts), `|H| = 2`. The bounds of
Theorem 8 (10 sets, 20 single sides, storage 30) are far from reached, as r4-switch.md §6 says; they are proved
bounds, not observed ones. A step-(3) certificate with rows in both directions at once never occurred.

Generators. `planted.py`: planted path with a type word and intended kinds, every P2 requirement met by a private node
(or a shared hub), extra contacts consistent with the kinds, off-path switches, saturation (random memberships added
while the planted path stays shortest). `gen_run.py`: forward zone, run of forward `T`-members, backward zone; cross
pairs of run members and backward `O`-members drawn as a matrix (`p ∈ f(a)`, `a ∈ b(p)`, or both); non-tight
straddles (shortcuts by Lemma 7) rejected before the shortest-path test; `reverse` swaps `s` and `t`, which turns
forward rows into backward rows, so (B0)-(B5) are exercised as often as (F0)-(F5). The diagnostics `diag.py`,
`diag_short.py`, `diag_run.py` show that the planted paths that are not shortest are killed by straddle-type double
swaps and by their two-partner variants (`X_{y_1} X'_p X'_{p'} X_{y_2} .. X_{p_1} X'_x X_{p_2}`), as the theory
predicts.

## 4. Cross-check with the author's code (`crosscheck.py`, the only script importing `r4-switch/`)

`crosscheck.py 1 600` and `2 600`: 1,200 instances (half random P2, half critical-run instances of `gen_run.py`),
1,438 shortest paths. Own and author's `shortest_valid_paths` return the same sets of paths on all; own and author's
brute force agree; the author's `prove.certificate` raised no assertion on any path (maximum storage 7; own maximum on
the same instances 9, because the own procedure follows the text literally and does not prefer swaps); own `search5`
and the author's `admissible_search` agree on all 4,800 random `(K, B)`. 0 mismatches.

## 5. Remarks (none affects the verdict)

1. *Exponent.* With the three-span version of (F4→)/(B4) (§2.6), Theorem 8 gives 6 sets and 12 single sides per type,
   storage 18, `B = 36`, and the running time `O(D^{74})`. The Erdős-Szekeres step can be dropped.
2. *Hypothesis of Theorem 8.* The `T`-part needs only "no `T`-straddle". Corollary 9 is unaffected.
3. *Evidential value of the `decide_full` row of §6.* On instances with at most 6 switches every set of sides of one
   type is a union of at most 20 single sides, and `B = 60 >= D`; so `decide_full` includes `K` = all sides, i.e. an
   exact search, and its agreement with brute force tests the implementation and soundness, not the certificate
   theorem. The certificate-guided checks (the proof's certificate accepted by the search) are what test Theorem 8;
   they were reproduced here independently.
4. *Wording in §7.1 of r4-switch.md.* "Every NP-hardness proof for the open case of DC must therefore use structure that
   the switch model lacks" holds under P ≠ NP (if P = NP, NP-hardness of 2CH + P2 is not excluded); add "unless P = NP".
5. F3 holds for all `a != b` (the distance condition is not needed); harmless.

## 6. Not checked

- §5 (practical variant with declarations, `decide(1, 0/1, 4, 8)`) and its tables: only Theorem 11 (soundness) was
  checked; the failure rates of the small-parameter variant were not re-run.
- §7.2 (ties, `T_L^tie` storage `O(1)`): labelled sketch by the author, not reviewed.
- §7.3 (PC on 2CH + P2) and the PC rows of §6: not re-run.
- The reduction 2CH + P2 = SW + P2 ⊆ open case of DC is taken from `verify/lth.md` §1 (verified there), not re-checked.
- The algorithm with the full parameters `(10, 20, 60)` was run only where it degenerates to an exhaustive search
  (remark 3); on larger instances only the existence and acceptance of the proof's certificate (of the enumerated
  shape) was checked, which is what the proof of Theorem 10 uses.
