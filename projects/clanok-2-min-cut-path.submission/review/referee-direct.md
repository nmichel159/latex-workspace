# Referee report on the direct proof (Sections sec:zz-zigzag and sec:pa-polynomial of main.tex)

Status: finished, 2026-11-02. **Verdict: the text proves that the open case is solvable in time n^31 n^O(1). No G and no E; five minor remarks.** Details in Section 7.
Nothing of this review is running any more.
Working file of an AI referee; not read by the author; not in the manuscript. Scripts and logs: `../checks/`, `../checks/runs/`. Places are cited by label.
Classification: G = gap or false statement, E = error that is easily repaired, M = minor.

## 1. Findings

No finding of class G or E.

| No. | Class | Place | Finding | Proposed repair |
|---|---|---|---|---|
| M1 | M | intro of sec:pa-polynomial | The sentence on duality names the exchange of dn/up, MB/MA, L_P/U_P, but the dual statements also use A_P <-> B_P and (in lem:pa-atoms) C <-> C'. True, not stated. | After the definition of A_P, B_P or at lem:pa-atoms(b): "and it exchanges A_P and B_P, and C and C'". |
| M2 | M | proof of thm:pa-formulas, first two sentences; intro | "contacts" and "far pairs" are used without a definition. | Say once: a far pair is two elements of A_P or of B_P at distance at least six; C(a), C'(b) are the contacts. |
| M3 | M | def:pa-atoms | "elements x_1, ..., x_8" also introduces the F-formula, which uses six. | None needed, or "x_1, ..., x_6" for F. |
| M4 | M | thm:pa-formulas against lem:pa-atoms, lem:pa-two | S(a), T(b) (position sets) next to the formula sets S, S'; a_1, a_2 have three different meanings in lem:pa-atoms, lem:pa-two and Stage 1. Unambiguous in context. | Optional renaming. |
| M5 | M | Case l* < sigma*, r* < tau* | "With the corresponding tie-breaks" hides one line: the first and the last by position exchange, and FR, ER are symmetric in their two arguments. Correct (asserted by the harness). | Optional half sentence. |

## 2. Task A: line-by-line check

Fixed: the text of main.tex; each row was re-derived by hand. "OK" means statement and proof hold as written.

### 2.1 Section sec:zz-preorders

| Statement | Check |
|---|---|
| def:zz-preorder | Facts on down-sets and `x <= y < z` => `x < z`: OK. |
| def:zz-zz | `R` strict; `G_D` for down-sets with `u in D`, `v not in D`. MB(x) may contain x (if x has a lower neighbour), which is harmless below: every use of MB allows it. OK. |
| def:zz-valid | Since u <= x <= v, a valid walk has u only as a low and v only as a high. Reversal keeps labels and validity. The ends with their labels are part of the definition, so "either order" costs nothing. OK. |
| lem:zz-valid(a) | `h <= x <= l` against validity; u is a low so in D; v is a high so outside D; each step of P is an edge with lower end in D and upper end outside, so an edge of G_D. OK. |
| (b) | The end of an edge of G_D in D is the lower end. Alternation, `u` low, `v` high, validity through `l in D` => `h in D`. OK. |
| (c) | (b); (a) with D = L_P, which lies in Q - U_P by the first part. OK. |
| (d) | No element both low and high (`h <= h`), so i, j have one label, j - i is even. Removal keeps the alternation; the ends are kept (j = q gives x_i = x_q; i = 0 and j = q would give u = v). Validity is inherited. OK. |

### 2.2 Section sec:zz-reduction

| Statement | Check |
|---|---|
| lem:zz-sides(a) | Both sets separate u and v, so each boundary has at least c edges; lem:uncrossing gives the sum `2c - 2m`. So `m = 0`, both equal c. OK. |
| **lem:zz-sides(b) (new)** | Count of an edge in `delta(A - Y)` and `delta(A + Y)`: no end in Y: same as in delta(A) in each set; both ends in Y: in neither; one end w in Y, other end y outside: A - Y has w outside, so it counts iff y in A; A + Y has w inside, so it counts iff y not in A; so exactly once. Sum = `2(c - k) + |delta(Y)|`. Y misses u, v, so both sets separate: sum >= 2c. Hence 2k <= |delta(Y)| <= 2 and k <= 1; k = 1 forces both = c (and |delta(Y)| = 2). OK. |
| lem:zz-q(a) | lem:minimum-cuts for the pair x, u gives Y containing x, not u, with `|delta(Y)| = c(x, u) <= 2`. A vertex of Y cap Q is not u, and delta(Y) separates it from u, against c >= 3. OK. |
| (b) | prop:class gives transitivity; G in DC gives d <= 2 because c >= 3. OK. |
| (c) | Y misses u, v as they are in Q. First entering and last leaving edge of the path are two distinct edges of delta(Y); they lie in delta(A) since the path does. Against k <= 1. OK. |
| def:zz-instance, lem:zz-instance(a) | Preorder: immediate. No minimum side contains v, so x <= v vacuously; each contains u. A minimum side exists, so not v <= u. For x || y: `A_1` contains x not y, `A_2` contains y not x, and sides(a) forbids an edge xy. Hence adjacent elements of Q are comparable, and edges of R are strict. OK. |
| (b) | A cap Q is a down-set by definition. Converse: y in D lies in a minimum side, otherwise v <= y gives v in D. `S_y` is a minimum side (finite intersection) with `S_y cap Q = dn y`, union over y in D (nonempty, u in D) is a minimum side with trace D. OK. |
| **(c) (new P2 proof)** | x || y, not adjacent, distinct elements of Q, so d = 2 and z exists. Suppose z not in Q; Y as in lem:zz-q(a); x, y are in Q so outside Y and xz, yz are in delta(Y). A_i contains exactly one of x, y; whichever side z is on, one of xz, yz crosses A_i, so k >= 1, hence k = 1 for i = 1, 2, and `A_1 - Y`, `A_2 + Y` are minimum sides. x is in A_1, not in Y, not in A_2: x in `(A_1 - Y) - (A_2 + Y)`. z is in Y: z in `(A_2 + Y) - (A_1 - Y)`. The edge xz contradicts sides(a). So z in Q, z comparable with both; the chain cases and the tie cases make x, y comparable; so z is strictly below both or strictly above both, and the edges lie in R. OK. Note: the step z in Q uses neither DC nor d(u, v) = 2. |
| **thm:zz-reduction** | Answer forward: path in Q by zz-q(c); each edge has exactly one end in D, so not tied, so in R. Backward: A with trace D by (b); each edge of the path has both ends in Q and one end in D, so one end in A. prop:open-pairs, lem:basic-bounds close it. Time: x <= y for x = u or y = v; otherwise {u, y} and {x, v} are disjoint, the least boundary exceeds c iff no minimum side has y and not x (also for y = u, x = v). **Minimum side by one flow:** every S between D and V - (Q - D) separates u, v, so it has at least c edges; (b) gives such an S with c edges; so the least S is a minimum side with trace D. OK. |

### 2.3 Section sec:pa-polynomial: duality

The reversed instance is an instance of ZZ with P2 (`v <=' x <=' u`, `v <' u`, pairs with exchanged ends, meeting below and above exchange). Exchanging labels maps valid walks of the two
instances bijectively, keeping length and positions, so shortest walks correspond. Then highs' = lows, A'_P = B_P, B'_P = A_P, U'_P = L_P, L'_P = U_P, MB' = MA, MA' = MB, C'' (the C of
the reversed instance) = C'. **FR of the reversed instance:** `FR'(x, x') = dn'(Q - (MA'(x) + MA'(x') + up'x + up'x')) = up(Q - (MB(x) + MB(x') + dn x + dn x')) = Q - ER(x, x')`. So the
dual of lem:pa-atoms(a), "FR' misses U'_P and contains B'_P - (C''(b_1) + C''(b_2))", reads "ER contains L_P and misses A_P - (C'(b_1) + C'(b_2))", which is (b) word for word. Dual of lem:pa-one(a):
"no low' >=' x" is "no high <= x", (b) word for word; dual of lem:pa-basic(b), lem:pa-one(c): likewise. EP has no dual in the text and needs none.

### 2.4 Sections sec:pa-detours, sec:pa-atoms

| Statement | Check |
|---|---|
| lem:pa-basic | Finite strict descent; a down-set containing B_P contains dn B_P; a down-set meeting up A_P contains an element of A_P. (b): `e < a` excluded; `e' < e <= a` gives `e' < a`. OK. |
| lem:pa-one(a) | **Walk:** x_p high, z low (z < a, z < x), x high, z' low, x_p' high; steps are edges with the lower end at the low position; x_0, x_q and their labels are kept, also for p = 0 or p' = q. **Validity:** kept high with kept low: P valid. Kept high with z: `e <= z < a` against a in A_P; with z' likewise. x with z, z': z, z' < x. x with a kept low: kept lows are at positions outside (p, p'), hypothesis. All pairs covered. Length p + 4 + q - p'. x may be on P, equal to a, or equal to v: repetitions are allowed and nothing changes; x tied with u gives MB(x) empty. OK. |
| (b) | Dual. OK. |
| (c) | x not in L_P means no low >= x. Same parity, pairwise distance <= 4: at most three. OK. |
| lem:pa-two | **Walk:** a_1 high; z_1 low; h high; z_2 low; a_2 high, then W, whose end is b_1 low; w_1 high; a low; w_2 high; b_2 low. Reversing W keeps labels and edges. Steps: z_1 < a_1, z_1 < h, z_2 < h, z_2 < a_2, b_1 < w_1, a < w_1, a < w_2, b_2 < w_2. Ends kept. Length p_1 + 4 + (p_3 - p_2) + 4 + (q - p_4). Kept positions are [0, p_1], [p_2, p_3], [p_4, q], disjoint from Z. **Validity:** highs {e, h, w_i}, lows {f, z_j, a}: nine pairs, exactly the items (1)-(9) of the proof, each correct: (2), (4) use lem:pa-basic(b) and Z; (9) is `b_i < w_i <= z_j < h` with h a low. Coincidences (z_1 = z_2, w_1 = w_2, z_i a kept low, w_i a kept high) are allowed and covered by the same pairs. OK. |
| def:pa-atoms, formulas are down-sets | OK. Counts 6 + 19 + 6 = 31, 8 + 16 = 24. |
| lem:pa-atoms(a) | x in Gamma cap U_P: not a_i <= x; x < a_i would give a high below a_i; so x || a_i (the tie is excluded by not a_i <= x); P2 and x not in MA(a_i): meet below. Two elements of A_P cap MB(x) at distance >= 6 with x not in L_P, against one(c). Then dn Gamma misses the up-set U_P. b in B_P outside C(a_1), C(a_2): not in MA(a_i), not in up a_i. OK. |
| (b) | Section 2.3. OK. |
| (c) | y <= b < a gives y in dn a - [a], so dn b misses Gamma. a' in A_P - win(a): not in MB(a); `a' < a` impossible; a' tied with a is not in dn a - [a]; so a' in Gamma. win(a) <= 3 as a is not in L_P. OK. |

### 2.5 Section sec:pa-formulas: thm:pa-formulas

| Step | Check |
|---|---|
| (dagger) | OK. |
| Small sets | Q - up A_P: E-formula with all ER omitted, |S| <= 3; dn B_P: F-formula with all FR and the last term omitted. OK. |
| Stage 0, far pairs | Four elements: four positions of one parity, so first and last differ by >= 6. OK. |
| Thresholds | First four of the sort by l have l >= l*; the far pair has all positions of S at least l*, so b with pos(b) < l* is outside both C and lies in FR_l. r, sigma, tau alike (asserted). With +inf or -inf these statements hold vacuously. OK. |
| E_0, H_0 | 3 + 3 + 6 = 12 each; positions outside the walk give nothing. OK. F* misses U_P, E* contains L_P by (dagger). Exits C_0 empty, R_0 empty: OK. |
| Finite thresholds | l* = +inf or r* = -inf puts all of B_P in FR_l or FR_r; l is never -inf, r never +inf; likewise sigma, tau. l*, r* are positions of elements of B_P (lows), sigma*, tau* of A_P (highs). OK. |
| Classes | E*, F* down-sets and lem:pa-basic(b): classes stay in R_0, C_0. OK. |
| eq:pa-ranges-r, -c | a in R_0: in ER_sigma and ER_tau, so sigma* <= pos(a) <= tau*; a not in E_0 (as up E_0 is removed); parity excludes all but the six listed positions. Index >= 4 in the sorts gives l(a) <= l*, r(a) >= r*. Same for h through FR_l, FR_r, dn H_0. **Margins:** tau* - sigma*, r* - l* >= 12 since the ranges are nonempty; values finite. OK. |
| Orientation | Types differ, so sigma* != l*, tau* != r*; four sign cases, exhaustive. Case sigma* < l*, r* < tau*: Pos[h] inside (sigma*, tau*) inside (sigma(h), tau(h)), span >= 12, every low >= h has its position in Pos[h]: against lem:pa-one(a). Case l* < sigma*, tau* < r*: dual with a, lem:pa-one(b). OK. |
| **Reversal** | P reversed: positions q - p; U_P, L_P, A_P, B_P unchanged; l' = q - r, r' = q - l, sigma' = q - tau, tau' = q - sigma. Non-increasing l' is non-decreasing r etc. First and last by position exchange; FR, ER symmetric; position lists in E_0, H_0 map to themselves: `{q - tau* + i} = q - {tau* - i}`. So E_0, H_0, F*, E*, R_0, C_0 are the same and eq:pa-ranges hold in the new positions. New values give sigma* < l*, tau* < r*. Nothing later refers to the old positions, nor to which end is u (walks have either direction; the lemmas are stated for any shortest valid walk). OK. |
| **(star)** | alpha != beta by type. p_1 = sigma(h) <= sigma*, p_4 = r(a) >= r*. alpha >= sigma* + 6, beta >= l* + 6 > sigma* + 6: p_2 - p_1 >= 6. alpha <= tau* - 6 < r* - 6, beta <= r* - 6: p_4 - p_3 >= 6. Z above sigma*, below r*. All hypotheses of lem:pa-two: the elements at p_1, alpha are in A_P cap MB(h), at p_4, beta in B_P cap MA(a); h not <= a. 12 <= 8 contradiction. OK. |
| Positions of C_0 | Span >= 12, so Pos[h] is not inside (sigma(h), tau(h)) by one(a); types differ from the ends; Pos[h] above sigma* >= sigma(h) by the orientation; so some position exceeds tau(h) >= tau*. OK. |
| Stage 1, at most four classes | S = E_0 + A_kappa, at most 16; every element of A_P in E* is in R_0, so tied with a representative. OK. |
| kappa, tail, a_1, a_2 | Disjoint position sets, distinct last positions; other classes have their last position in the tail; C_0 classes have a position > tau* > p*. Last positions of kappa_1, kappa_4 differ by >= 6. OK. |
| F^1, eq:pa-not-below | |S'| <= 6; last term misses A_P: in S' means in up S', otherwise outside both EP; so F^1 (a down-set) misses U_P. g in a class of C_1: outside FR(a_1, a_2), so in C(a_1) + C(a_2). h < a_i would put h in the last term, as up S' lies in U_P; h ~ a_i impossible. OK. |
| Shape A | S = H_0 + H_1 <= 19, S' <= 6, x_1..x_6: formula form exact. Misses U_P, contains B_P. OK. |
| Shape B | Eight classes, two groups of four: two far pairs in four classes. E-formula with S <= 16, x_1..x_8. Contains L_P. a in A_P cap D: in R_0, not in kappa (up A_kappa removed), so a position in the tail; whole class in D. Lambda has both types, so consecutive alpha (a'' in a class of R_0 in D) and beta (g in a class of C_1). One pair of h's avoids the class of g; a'' in ER gives a'' in C'(h); g in C(a'). a' in R_0, h in C_0, h not <= a'. Interval in the tail misses Pos[a'] (kappa has no tail position); interior misses Lambda, so Pos[h] (class of h is in C_1); alpha is a high; beta not in Pos[h] as positions are unique and the class of h does not contain g. Against (star). OK. |

**Formula uses against def:pa-atoms:** small sets (no atom), F* (FR, FR, dn H_0; third pair and last term omitted), E* (two ER), E* minus up A_kappa, F^1 + dn H_1 (three FR with EP on x_5, x_6), Shape B (four ER): each is an instance of the definition with the stated omissions. Sizes: 19 = 12 + 7, 6 = 3 + 3, 16 = 12 + 4, 31 = 6 + 19 + 6.

**Degenerate cases.** An element tied with v lies in A_P only if all highs are tied with v; then C = empty, l = +inf, and the F* exit applies. Dually for u and B_P. x = u: MB(u) empty; x = v: no low >= v, one(a) holds. z, z_i tied with u and w, w_i tied with v are ordinary lows and highs. Elements z, w may coincide with kept elements of the same label (the opposite label is excluded by the validity items). Off-walk elements tied with a class are removed or kept by the up-set and down-set terms with no effect on the argument, since classes in R_0, C_0 are classes of highs and lows of P. Infinite thresholds are excluded before any use of parity.

### 2.6 Section sec:pa-algorithm

| Statement | Check |
|---|---|
| cor:pa-zz | Values are down-sets; a passing value proves yes. Completeness: lem:zz-valid(c), thm:pa-formulas, lem:zz-valid(a). Tuples over Q and one symbol: (m + 1)^31 and (m + 1)^24. OK. |
| alg:pa-open-case, thm:pa-open-case | thm:zz-reduction, prop:easy-pairs(iv), lem:basic-bounds; m <= n and (n + 1)^31 <= 2^31 n^31. OK. |

### 2.7 Items added by the author during the review

The mathematics of the statements and proofs is unchanged (text re-read after the additions). Checked in addition:

| Item | Check |
|---|---|
| ex:zz-instance | All numbers recomputed by hand and by `checks/example_gb.py`: c = 3, Q = {u, a, b, v}, the five minimum sides, u < b < a < v, R = {ua, ub, ba, av, bv}, the valid walk, D = {u, b}, A = {u, s, b} the only minimum side with this trace, delta(A) = {ua, ab, bv}. OK. |
| tab:pa-exits | 3, 3, 4 + 12 = 16, 4 + 12 = 16, 4 + 16 = 20, 6 + 19 + 6 = 31, 8 + 16 = 24. OK. |
| fig:zz-walk, fig:p2-outside, fig:one-detour, fig:two-detours, fig:positions | Rendered and compared with the text: order of the elements, labels, red parts, position of Y and of the two differences, order sigma(h) <= sigma* < l* < p* < tau* < r* <= r(a), dark part beyond tau*. OK. |

## 3. Answers to the specific questions

- Constructed walks of lem:pa-one, lem:pa-two are walks under def:zz-valid: yes, labels alternate, every consecutive pair is an edge with its lower end at the low position, ends u, v with their labels. Also tested: 3.2 million walks of lem:pa-one and 2,994 of lem:pa-two, both directions of W, passed `is_valid_walk`, which tests def:zz-valid directly (Section 4).
- Parity, bound 3, margins, count 31, sizes 19, 6, 16: correct. The margin 6 is not tight (Section 6).
- FR of the reversed instance is the complement of ER: yes.
- The reversal of the walk preserves everything used later: yes.
- P2 with z outside Q: the argument is correct, and the step does not need DC.

## 4. Task B: computations

Code in `../checks/`: `zz_core.py` (instances, exact solver, atoms), `zz_proof.py` (the proof with asserts), `zz_design.py` (planted bases), `run_planted.py`, `graph_level.py`, `graph_climb.py`, `p2_outside.py`, `realize.py`, `run_tiny.py`, `run_mut.py`, `example_gb.py`, `agg.py`. Failing instances would go to `runs/ce/`, which is empty. All 28 logs with a line `FAILURES:` report `none` (18 planted, 6 graph level, 2 tiny, 1 climb, 1 p2-outside); no error file has content. The logs total 137 KB.

### 4.1 Graph level

`graph_level.py`, `graph_climb.py`: all connected graphs with n <= 7, all 8-vertex graphs, random families with bridges, pendant parts, ears with n <= 13, hill climbing with n <= 12: 313,329 open pairs (3,813 yes), 225,884 of them with vertices outside Q, 295,738 comparable pairs with a common neighbour outside Q, 2,638 incomparable pairs, none with such a neighbour. Asserted: lem:zz-sides, lem:zz-q, lem:zz-instance (preorder, non-adjacency, A cap Q exactly the down-sets, P2), the flow test of <=, the least boundary between D and Q - D, cp = c over minimum cuts and over all cuts and paths, solver against down-sets, thm:pa-formulas on four variants. No failure. Brute force stays at q = 3 (the climb did not reach q = 5 for n <= 12); long walks on graphs come from `realize.py`.

`p2_outside.py`: all graphs with c(u, v) >= 3 of the exhaustive sets and 344,129 random ones, any distance, also outside DC: 523,207 pairs, 3,977 incomparable pairs, no common neighbour outside Q. The attempt to force the case: 774 ears inserted between incomparable elements; the pair always became comparable, as the proof predicts.

`realize.py` (stopped by the interruption after 10 of 12 instances, each of them complete): planted instances realised by real graphs of DC with n up to 171,748, c up to 40,641, q up to 283. The check recomputes from G: distance at most two within Q, c(u, x) >= 3 on Q, the preorder by one maximum flow (residual reachability) and R, all equal to the planted ones; the value of the formula gives a minimum side, whose boundary is a minimum cut containing a u-v path. Exits: Shape B 4, Shape A with C_1 nonempty 5, at most 4 classes 1. So Stage 1 and both Shapes are reached by graphs of DC, not only by abstract instances.

### 4.2 Instance level

18 logs, 1200 s or 900 s each: planted bases B, A, stair, ties, small, mix, cross, allstrict, kappa (zipper layouts adapted from `rv-r7-desc`, written directly: shared E-node = element tied with u, shared F-node = element tied with v), and two (gadgets for lem:pa-two). Each P is verified shortest by the exact solver and each proof run is made on P, P reversed, the reversed instance and both, with random tie-breaks and representatives. Hill climbing keeps P2 and P shortest; moves: contacts, removed strict pairs, ties, private witnesses, arbitrary edges, relations among highs or among lows, elements lifted out of the classes of u and v, off-walk elements.

| Branch reached | Count |
|---|---|
| proof runs | 54,444 (max m 452, max q 311) |
| small A / small B | 42 / 42 |
| C_0 empty, F* | 20,773 |
| R_0 empty, E* | 20,781 |
| R_0, C_0 nonempty | 27,761 |
| orientation direct / reversed | 13,881 / 13,880 |
| orientation cases 1, 2 | never (asserted) |
| R_0 has at most 4 classes | 7,032 |
| **Shape A**, C_1 empty / C_1 nonempty | 14,133 / 3,998 (|C_1| = 7, |S'| = 6, |S| = 18 reached) |
| **Shape B** | 2,598 (375 where one pair alone leaves a class, so the second pair is needed; |S| = 15 reached, C_1 up to 20) |
| (star) | 3.7 million pairs (a, h), 70.5 million quadruples; 2.8 million sampled with exactly one element of Z in the interval |
| direct attack on (star) | 205 instances with contacts added to violate (star): all rejected by the solver, which found a shorter walk, as lem:pa-two predicts |
| general core of Shape B (any far a_1, a_2, any far pairs) | 25,731 tests, 862 with a class of R_0 inside D |
| lem:pa-one | 9.4 million pairs, 3.2 million built walks valid; span 4 and three elements of A_P cap MB(x) occur, so 4 and 3 are tight |
| lem:pa-two on shortest walks | 2,994 tests, each walk built and valid; sum 8 reached 2,158 times, so 8 is tight, with W forward and with W backward (`runs/two-layouts.txt`). A layout with sum 10 is rejected by the solver |
| lem:pa-atoms | more than 7.8 million far pairs, 1.3 million EP |

Limit: lem:pa-two was exercised on shortest walks only in base `two`, which ends in Stage 0. In the Stage 1 families its hypothesis was never met in the tested pairs (at most 250 per run); there the lemma acts through (star) and the attacks above, and it fires on non-shortest walks (Section 4.3).

`run_tiny.py`: 355,475 random tiny P2 instances, not from graphs, solver equal to enumeration of down-sets, 282,969 shortest walks on four variants, 3.5 million random formula values, all down-sets, none connecting on a no-instance. Stage 0 only.

### 4.3 Mutation test

`runs/mut-31.txt` (4 instances per family, four variants, 3 tie-breaks; `runs/mut-21.txt` is the earlier run, in which the two rows marked below had no instances yet):

| Mutation | Fired | Assertion |
|---|---|---|
| none (control) | 0 of 432 | |
| margin 6 -> 2 | 31 of 48 | Positions of C_0, on the purpose-built `margin2` |
| far pair distance 6 -> 2 | 48 of 48 | Stage 0: FR misses U_P; ER contains L_P |
| lem:pa-atoms at distance 2 | 16 of 48 | atoms (a), (b) |
| drop up A_kappa (new instance `kappay`) | 12 of 48 | Shape B: D meets U_P |
| drop the EP term | 6 of 48 | eq:pa-not-below |
| drop h_3, h_4 | 20 of 48 | Shape B: D meets U_P |
| bound of lem:pa-one 4 -> 2 | 48 of 48 | |
| bound of lem:pa-two 8 -> 6 (new base `two`) | 12 of 48 | |
| walk made non-shortest | 15 of 16 | lem:pa-two 14, (star) 1 |
| margin 4 (Section 6, must pass) | 0 of 480 | |
| margin 4 and five classes (Section 6, must pass) | 0 of 336 | |

The runs that do not fire are other instance variants that end at another exit, for instance the reversed instance. So the harness detects each error on instances that reach the place concerned.

### 4.4 Processes of the resumed part (all exited by themselves by 09:44; nothing is running)

| PID | Command | Purpose |
|---|---|---|
| 18100 | `run_planted.py 31 two 900 120 runs/planted2-two-31.txt` | lem:pa-two on shortest walks |
| 16544 | `run_planted.py 32 all 900 40 runs/planted2-all-32.txt` | all bases with the later moves and attacks |
| 30772 | `graph_climb.py 7 900 12 runs/climb-7.txt` | graph level hill climbing |
| 20696 | `run_mut.py 31 4 runs/mut-31.txt` | mutation test |

The six climbs, three local runs and the rest of the first session were killed at the interruption and left no logs; the climb and the base `two` above replace them.

## 5. What is not checked

1. The algorithm of cor:pa-zz is not run: (m + 1)^31 is out of reach. Completeness rests on the construction from a known P, soundness on the formula values being down-sets, which is immediate and sampled.
2. In Shape B the branch "a class of R_0 outside kappa lies inside D" never occurs. That is what the claim says, so the end of its proof is confirmed by hand only, and by the (star) tests and attacks on the step it uses.
3. Planted instances are my designs. Hill climbing leaves their layout essentially in place, and the tiny random instances and the base `two` end at Stage 0, so Stage 1 was reached only from the zipper layouts. No search can exclude a counterexample; the verdict rests on the hand check, with the computations as a test of it.
4. Brute force over minimum sides stops at n = 13 and q = 3. The longer walks on graphs use one maximum flow in place of enumeration.
5. Sections 1 to 4 of main.tex are out of scope. Used from them, and checked: lem:minimum-cuts, lem:uncrossing, prop:class, prop:open-pairs, prop:easy-pairs. lem:basic-bounds is cited from an earlier paper; the two facts used here are immediate: a cut-path contains a cut, and a path shares an edge with every cut that separates its ends.

Figures were read for agreement with the text, not as a typesetting review.

## 6. Further simplifications (none is needed)

1. Margin 4 suffices: if alpha < beta, then pos(a) is outside [alpha, beta], so alpha >= sigma* + 6 or beta <= r* - 6 while the other gap is >= 4; if beta < alpha, both gaps are >= 5. Either way the sum is >= 10 > 8, and the other uses of the margin need only a span > 4. Then |E_0|, |H_0| <= 10. Margin 2 fails (Positions of C_0, Section 4.3).
2. Shape B needs only five classes: with positions c_1 < ... < c_5 the pairs c_1, c_4 and c_2, c_5 are far and use four classes. Then |C_1| <= 4 in Shape A.
3. Together: F-formula 6 + (10 + 4) + 6 = 26 elements, E-formula 8 + (10 + 4) = 22, exponent 26 in place of 31. Passed 336 runs of the harness, reaching Shape B 102 times.
4. One maximum flow gives the whole preorder by residual reachability (used in `realize.py`), in place of one flow per pair in thm:zz-reduction.

## 7. Verdict

**Yes. The new text proves that the open case is solvable in time n^31 n^O(1).** thm:pa-open-case follows from thm:zz-reduction, thm:pa-formulas and cor:pa-zz, and every step holds as written, in particular the items that nobody had reviewed: lem:zz-sides(b), the proof of P2 in lem:zz-instance(c), the minimum side by one flow, walks in either direction, all constants of thm:pa-formulas, and duality through the reversed instance, where FR of the reversed instance is the complement of ER.

Findings: no G, no E, five minor remarks (M1 to M5), none of which touches a proof.

The computations agree: no failure in any run. Stage 1 and both Shapes were actually reached (Shape A with C_1 nonempty 3,998 times, Shape B 2,598 times), also on real graphs of DC, and the mutation test shows that the harness detects errors of the kinds asked about. Their limits are in Section 5. As with any referee report of this kind, this is one reader's check and not a substitute for the author's reading or for external peer review.
