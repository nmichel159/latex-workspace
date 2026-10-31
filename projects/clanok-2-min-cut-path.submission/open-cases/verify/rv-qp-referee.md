# Referee report on `qp-proof.md` (round 6c)

Status: reading complete; computations in progress (see §4), 2026-10-28 (agent qp-referee). Working file of AI agents;
not read by the author; nothing here is in the manuscript.
Object: `open-cases/qp-proof.md`, version of 2026-10-28 11:06 (809 lines), read as a whole from the first page to the
last, as a journal referee would. Earlier reviews were not assumed: every proof was re-derived line by line, and every
spot check below runs on own code (`verify/rv-qp-referee/`); code of `verify/rv-r6-core/` is imported only to
generate switch-form instances, and `verify/equivalence/graphs8.g6` is read only as a list of graphs.
Labels: holds, holds with repair, gap, false.

## 0. Verdict

**`qp-proof.md` proves its main theorem.** Every numbered statement holds; the proofs are complete and use only
the definitions, the max-flow min-cut theorem (to compute `c`, `Q` and the preorder) and von Neumann's minimax
theorem (for finite games, applied under its hypotheses: both strategy sets non-empty). The reduction from graphs
(Theorem 13(a) of `theory-dc.md`) is not cited but proved in full in §2 (Lemmas 2.1-2.8, Theorem 2.9) and can be
checked line by line; I re-derived it and found no gap. The time bound `2^{O(log^3 n)}` and the complexity
consequences (in NP and in QP; NP-hard only if NP ⊆ QP; not NP-hard if ETH holds) are right.

Overall: **holds with repair**. The repairs (§2) are of wording, notation and precision; none changes a statement or
a proof step: one term defined twice with two meanings ("real edges"), switches called "E-members" without a
definition, the notation `X_a` for the member of a switch used without a definition, a misleading parenthesis in
Corollary 7.2(b), and the form of ETH in Corollary 7.2(c). No mathematical gap was found.

## 1. Verdict per numbered statement

| Statement | Verdict | Note |
|---|---|---|
| Def. 1.1 (cuts, cut-paths) | holds | agrees with `knowledge/research/min-cut-path.md` §1 (cut-path = edge set containing a path and a cut) |
| Def. 1.2 (DC, open case) | holds | DC requires connectedness, as `DC_2` of article 2 |
| Lemma 1.3 | holds | (a) `δ(S) ⊆ C` and minimality; (b) triangle inequality; (c) `C ⊆ F`, `|C| >= c = |F|` |
| Lemma 1.4 (uncrossing) | holds | identity re-checked edge type by edge type (`IX, IY, XO, YO`: 1/1; `IO`: 2/2; `XY`: 2/0+2) |
| Def. 1.5 (preorders) | holds | the two transitivity facts and the trichotomy re-derived |
| Def. 1.6 (ZZ, P2) | holds with repair | R1: "real edges" here are the elements of `R`; in Lemma 2.4 the same italic term means all edges of `K[Q]` |
| Def. 1.7 (general switch form) | holds | private nodes of distinct middle edges are automatically distinct (each lies in exactly two labelled sides) |
| Def. 1.8 (mode vectors, valid paths) | holds with repair | R3: the notation `X_w` (member of the switch `w`) used in Lemma 4.4 is not defined |
| Lemma 2.1 (bridges) | holds | (∗) shows a path meets a bridge at most once and only between the two sides; (b) both directions of "minimum cut" |
| Lemma 2.2 | holds | the counts `|J| + #{i : y_i ∈ S}` and `|J| + #{i : y_i ∉ S}` are exact; `e_1 ≠ e_2` because a path visits a vertex once |
| Lemma 2.3 (ears) | holds | (∗∗) needs `K` bridgeless (Lemma 2.1(d)); ears with `p = p'` or `a = a'` are covered |
| Lemma 2.4 (`H`) | holds with repair | R1 (terminology). Proof complete: (b) is an injection of ear edges of `δ_H(S ∩ Q)` into distinct `E[Y]` |
| Def. 2.5 | holds | |
| Lemma 2.6 | holds | uses Lemma 1.4 with multiplicities; `w(S_1 − S_2, S_2 − S_1) = 0` kills every edge of `H` between `x ∥ y` |
| Lemma 2.7 | holds | "some minimum cut contains `y`" is correctly derived from `v ∉ D`; `C(y) = ↓y` |
| Lemma 2.8 (P2) | holds | the four comparability combinations are exhausted; ties `z ~ x` excluded |
| Theorem 2.9 (reduction) | holds | chain Lemma 1.3(c) → 2.1(c) → 1.3(a) → 2.4(d) → 2.7; the flow formula for `<=` (time part) re-derived for `x`, `y` in all positions |
| Construction 3.1 | holds | the four kinds are exhaustive (`a ∈ [v]` or `b ∈ [u]` impossible) |
| Lemma 3.2 | holds | |
| Lemma 3.3 | holds | (i) bijection; (iii), (iv) per down-set; `w_i = w_{i+1}` needs no argument and is correctly excluded |
| Lemma 3.4 | holds | (b) needs `s ≠ t` (with `s = t` no side is needed to connect); the dropping argument for repeated sides is right also when `j = r` |
| Def. 4.1 | holds with repair | R2: `A`, `B` are sets of switches, defined through "E-members"/"F-members", which Def. 1.8 defines as sides |
| Lemma 4.2 | holds | (a) the choice of `a` with least `|↓a|` is correct with ties; (e) uses only that sub-sequences of members are valid |
| Lemma 4.3 | holds | the spliced walk is itself a valid path (members vs `Z_i` by 4.2(d)) |
| Lemma 4.4 | holds | Case 1a actually gives `[ℓ − 3, ℓ + 3]` (remark O3); the dual via the reversed instance re-checked item by item (`A^op = B`, `E#^op = F#`, `NE^op = NF`, conflict pairs unchanged) |
| Lemma 4.5 | holds | the hypotheses `F_x ≠ ∅`, `E_y ≠ ∅` are not used (remark O4) |
| Def. 5.1 (terms) | holds | every `D(τ)` is a down-set |
| Lemma 5.2 (one level) | holds | claim, trivial cases, both game cases and the case `m = 1` re-derived; every property of the fixed outcome uses only its covering properties |
| Theorem 5.3 | holds | `c <= ⌊log m⌋` continue steps, so `j <= k`; induction `D_1 ∩ .. ∩ D_i ∩ Up ⊆ ↑A^(i+1)` correct |
| Def. 6.1 (IDESC) | holds | |
| Theorem 6.2 | holds | soundness, completeness, count `2k (2^{k+1}(m+1)^{10k})^k (m+1)^N` and `log count <= 1 + 2ℓ + 2ℓ(2ℓ+1) + 45ℓ^3` re-derived |
| Theorem 7.1 (main theorem) | holds | sizes `m + 2 <= n`, `ν, σ <= n + n^2`; `poly(n) <= 2^{O(log^3 n)}` as `log n >= 1` |
| Corollary 7.2 | holds with repair | R4 (parenthesis in (b)), R5 (form of ETH and the cost of deleting repeated clauses in (c)) |

## 2. Required changes

None of them changes a statement or a proof step; each removes an ambiguity a referee of a journal would object to.
Line numbers refer to the version of 2026-10-28 11:06.

**R1. "Real edges" is defined twice, with two meanings.** Definition 1.6 (lines 116-118) calls the elements of `R`
*real edges*; Lemma 2.4 (line 244) calls all edges of `K[Q]` *real edges*, including the edges between equivalent
elements that Definition 2.5 then removes ("`R` = the real edges of `H` whose ends are not equivalent"). §2 uses the
second meaning, §3 the first, and the proof of Theorem 2.9 (lines 335-337) uses both in one sentence. No step is
wrong (a down-set contains whole classes, so the two meanings agree on the edges with exactly one end in a down-set),
but the reader has to work this out. Change: in Definition 1.6 replace "(*real edges*, written `ab` with `a < b`)"
by "(*`R`-edges*, written `ab` with `a < b`)" and "whose edges are the real edges with exactly one end in `D`" by
"whose edges are the `R`-edges with exactly one end in `D`"; in §3 replace "real edge(s)" by "`R`-edge(s)" (lines
351, 355, 356, 361, 379, 395, 396, 397, 408); keep "real edges" in §2, where Lemma 2.4 defines it.

**R2. `A`, `B` and "E-members" as switches.** Definition 1.8 (line 145) defines the *members* of a valid path as
sides, but Definition 4.1 (lines 446-447) defines `A` as "the set of minimal E-members (E-members with no E-member
strictly below)", and `A`, `B` are used as sets of switches from then on (`↑A`, `a ∈ A`, `E_a`, `dam(a)`); Lemma
4.2(a), (b) (lines 470-479), Lemma 4.4 (line 509) and the proof of Lemma 5.2 also call switches "E-members". Change:
in Definition 1.8, after "`W_E` (`W_F`) is the set of switches whose E-side (F-side) is a member", add "; a switch of
`W_E` (`W_F`) is also called an *E-member* (*F-member*)"; in Definition 4.1 write "`A = {a ∈ W_E : no a' ∈ W_E
satisfies a' < a}` (the *minimal E-members*) and `B = {b ∈ W_F : no b' ∈ W_F satisfies b < b'}` (the *maximal
F-members*)".

**R3. The notation `X_w` for the member of a switch.** In Lemma 4.4 (lines 506-530) `X_a`, `X_x`, `X_z`, `X_{a'}`
denote the member of the switch `a`, `x`, `z`, `a'`, while `X_c`, `X_d`, `X_ℓ` denote the member at position `c`,
`d`, `ℓ` (Definition 1.8 indexes members by positions only). Change: in Definition 1.8 (line 146), after "then
`pos(w)` is the index of that member", add "and we also write `X_w = X_{pos(w)}` for it".

**R4. Corollary 7.2(b), the parenthesis (lines 739-740).** "If OPEN-DC is NP-hard under polynomial-time many-one or
Turing reductions (by (a), equivalently NP-complete under many-one reductions)" reads as if NP-hardness under Turing
reductions were equivalent to NP-completeness under many-one reductions, which is not known. Change to: "(b) If
OPEN-DC is NP-hard under polynomial-time Turing reductions, in particular if it is NP-hard under many-one reductions
(by (a), the same as NP-complete under many-one reductions), then NP ⊆ QP."

**R5. Corollary 7.2(c), the form of ETH (lines 760-763).** ETH is stated as "no algorithm decides 3-SAT on formulas
with `n_v` variables in time `O(2^{ε n_v})`", and the proof charges the deletion of repeated clauses as `poly(n_v)`.
The deletion takes time polynomial in the size `s_0` of the given formula, which is not bounded by any function of
`n_v` (with ETH in the literal form above, a formula with many repeated clauses cannot even be read in time
`O(2^{ε n_v})`). Change: state ETH with a factor polynomial in the input size, "there is `ε > 0` such that no
algorithm decides 3-SAT in time `2^{ε n_v} · s_0^{O(1)}`, where `s_0` is the size of the formula", and write the
bound of the proof as "`poly(s_0) + 2^{O((log s)^3)} = s_0^{O(1)} · 2^{O((log n_v)^3)}`, which is
`2^{ε n_v} · s_0^{O(1)}`". The conclusion is unchanged. The form of ETH is a statement about the literature: the
write-up must cite it from a checked source (TODO(verify)), not from memory.

## 3. Optional remarks

- **O1 (header, lines 3-5).** "every part reviewed": the routes that §9 items 2, 3 and 5 and the reversed instance of
  Lemma 4.4 describe were new in the assembly and reviewed first here (they hold). Update the line after this report.
- **O2 (why the decision settles the open case).** The main theorem decides `cp = c`; the reader should be told that
  this computes `cp`, since `d(u,v) = 2` gives `c <= cp <= c + 1` (article 2, Proposition 5; one line: for a minimum
  cut `S` and a common neighbour `w` of `u`, `v`, the edge `wv` (if `w ∈ S`) or `uw` (if `w ∉ S`) lies in `δ(S)`, and
  adding the other edge of the path `u w v` gives a cut-path with `c + 1` edges). Checked on all 121 588 pairs (§4).
- **O3 (Lemma 4.4, Case 1a, line 519).** The three types give `[ℓ, ℓ + 2]`, `[ℓ − 1, ℓ + 3]` and `[ℓ − 3, ℓ + 3]`,
  so `pos(a) ∈ [ℓ − 3, ℓ + 3]`, 7 positions; "`[ℓ − 3, ℓ + 5]`, an interval of 9 positions" is true but does not
  follow the case analysis just given, and a reader will look for the missing case. The Note after the lemma (5
  positions) is right; I re-derived the pairwise bounds (`(i)/(i)` 2, `(i)/(ii)` 3, `(ii)/(ii)` 4, Case 2 `[e − 2,
  e + 2]`, Case 1b 4). Largest span found in the computations: 5.
- **O4 (Lemma 4.5).** The hypotheses `F_x ≠ ∅`, `E_y ≠ ∅` are not used: each of the four cases of P2 gives the
  membership directly. Checked without them on every instance of §4. They may stay (Lemma 5.2 applies the lemma to
  rows and columns only), or be dropped.
- **O5 (overloaded letters).** `c` is the cut value (§2), a position (Lemmas 4.2(e), 4.3, 4.4), the number of
  continue steps (Theorem 5.3) and a subset size (Theorem 6.2); `s` is a terminal and the input size (Corollary
  7.2); `A`, `B` are vertex sets in Lemma 2.4 (`A(B)`) and the minimal and maximal members from Definition 4.1 on.
  Each use is local; renaming `c` in Theorems 5.3 and 6.2 costs nothing.
- **O6 (Theorem 6.2, line 715).** Union-find is not linear; a breadth-first search on the incidence graph of the
  nodes and the picked sides takes `O(ν + σ + m)`. Irrelevant for the bound.
- **O7 (Corollary 7.2(b), line 753).** "runs in time at most `s^a`" holds for `s >= 2`; add it.
- **O8 (Definition 1.7).** Distinct middle edges have distinct private nodes (each private node lies in exactly two
  labelled sides); in the abstract form a private node may even be `s` or `t`. Nothing in the proof depends on it;
  one sentence would spare the reader the check.
- **O9 (Lemma 3.4(b)).** The hypothesis `s ≠ t` is needed (with `s = t` a mode vector connects without any side);
  the proof is right as written.

## 4. Computations

(in progress)
