# Adversarial verification of dc-hardness.md (agent verify-LTH)

Status: in progress, 2026-10-13. Scripts and result files: `verify/lth/` (own code: `core.py`, `families.py`,
`satenc.py` written from the definitions in dc-hardness.md and theory-dc.md; the other agent's scripts were read only
after these were finished and imported only for the cross-check of §9 and for the formula encoder of §8.3).
Targets: dc-hardness.md Lemma D, Theorem L (a), (b), Theorem T, Theorem H with its remarks, "Consequences for a
hardness proof", and the claims that 2CH + P2, SW + P2 and TIC are special cases of the open case of DC.

Verdict labels as in `verify/equivalence.md`: **holds** (every step read and justified; exact checks agree),
**holds, repair given** (a step is missing or a statement is imprecise; a complete replacement is written here),
**gap** (not justified, no repair), **false** (counterexample).

## 1. Special cases: TIC ⊆ 2CH + P2 = SW + P2 ⊆ ZZ + P2 ⊆ open case of DC — holds, repair given

dc-hardness.md asserts the two conversions in one sentence each (Section 2, `swlib.to_zz`) and relies on
theory-dc.md Theorem 13(b). The steps that are not written there:

*From 2CH to ZZ.* Let `(N, s, t, (E_w, F_w))` be a 2CH instance with `s != t` (`s = t` is a trivial yes-instance and
is mapped to a fixed yes-instance). Elements: `b_x`, `t_x` for every node `x`, `e_w` for every switch. Preorder: all
`b_x` equivalent (least class, `u = b_s`), all `t_x` equivalent (greatest class, `v = t_t`), the `e_w` pairwise
incomparable, `b < e < t`. `R = {b_x t_x} ∪ {b_x e_w : x ∈ E_w} ∪ {e_w t_x : x ∈ F_w}`; `{u, v} ∉ R` because `s != t`.
1. *Consistency is automatic.* A valley is a `b` or an `e`, a peak a `t` or an `e`. Bottoms lie below and tops above
   every other class, and distinct switches are incomparable, so "valley `>=` peak" forces valley = peak = `e_w`,
   impossible on a path. Hence the consistent zigzags are exactly the alternating `u`-`v` paths of `(Q, R)`.
2. *Zigzag to mode vector.* `R` has no `e`-`e` edge and its only `b`-`t` edges are `b_x t_x`, so the path consists of
   blocks of elements of one node separated by single switch elements; a switch used as a peak has two bottom
   neighbours on the path, `b_x`, `b_y` with `x, y ∈ E_w` (pick `E_w`), a valley switch two top neighbours (pick
   `F_w`); each switch occurs once. The blocks form a sequence of picked sides from `s` to `t`.
3. *Mode vector to zigzag.* Take a shortest sequence `X_1 .. X_r` of picked sides and nodes
   `s = z_0, z_1, .., z_{r-1}, z_r = t` with `z_{a-1}, z_a ∈ X_a`; the `z_a` are distinct (a repeat shortens the
   sequence). Enter node `z_a` through `b` if `X_a` is an `E`-side and through `t` otherwise, leave it likewise for
   `X_{a+1}`, and use the edge `b_{z_a} t_{z_a}` when entry and exit differ. Every `R`-edge joins a lower and a
   higher element, so the path alternates, starts at `u` as a valley and ends at `v` as a peak; it is simple
   because the nodes are distinct and each switch is used once.
4. *P2.* The incomparable pairs are the pairs of distinct switches; a common `R`-neighbour below both is a `b_x`
   with `x ∈ E_w ∩ E_v`, above both a `t_x` with `x ∈ F_w ∩ F_v`. So ZZ-P2 ⇔ 2CH-P2. There are at least four strict
   pairs (`b_s, b_t < t_s, t_t`), so Theorem 13(b) applies and gives a graph of DC with the same answer.
*SW and 2CH.* The SW model of theory-dc.md is exactly a ZZ instance of this three-level shape except that a node may
carry several bottoms and tops (a component of the bottom-top edges). Contracting each component to a node keeps the
answer (a component is connected and bipartite, so a path can pass from any entry element to any exit element with
the right parity) and maps SW-P2 to 2CH-P2 (a common element gives a common component); the converse uses the
construction above (one bottom and one top per node). So 2CH + P2 and SW + P2 are the same problem up to this
linear-size translation.
*TIC.* Spans sharing a junction cover the union of their edges, so `0` and `K` are connected through picked spans iff
every edge `(j-1, j)` lies in a picked span; TIC is 2CH + P2 on the nodes `0..K`.

Checked (`test_zz.py`, §9): ZZ answer (own DFS for a consistent zigzag) = 2CH brute force, ZZ-P2 = 2CH-P2, valid
preorder; and on small instances the graph of Theorem 13(b) (`M = 1`) has `c(u,v) = ` number of strict pairs,
`d(u,v) = 2`, lies in DC, and "some minimum cut contains a `u`-`v` path" (all paths tested by Lemma 6 of theory-dc.md
with max-flow) = 2CH answer.

## 2. Lemma D — holds

Every step was re-derived. Remarks: (a) the hypothesis quantifies over `s`-`X` paths through sides of *both* modes,
which is what makes the prefix argument work; (b) the case "`X` contains `s`" is covered (the one-side path `X` does
not use `Y'`, so the hypothesis fails, as it should); (c) the converse direction (connected in `I0` ⇒ connected in
`I`) is monotonicity: sides only grow. The application to `R_L` is right: in `I0` the side graph of the non-empty
sides is the path `h_1 .. h_L`, and the flip sides are empty.
Checked (`test_D.py`): random backbones with guarded connectors, all mode vectors (§9).

What Lemma D does **not** give: table row D says the mechanism "protects a connector **only when** the partner of
one of its sides is a separator". Lemma D is a sufficient condition; necessity is argued only in the sketch of
Section 3. Verdict for that clause: **gap** (it is labeled sketch in the body, but the table presents it next to
"Lemma D proved").

## 3. Theorem L(a) — holds, repair given

Re-derived: `E_w ∩ E_v != ∅ ⇒ |x_w - x_v| <= l`; if `|x_w - x_v| > 2l` then `F_w, F_v` are non-empty (P2), meet,
and every `r` with a non-empty `E_r` has `|x_r - x_w| > l` or `|x_r - x_v| > l`, hence `F_r` meets `F_w` or `F_v`;
a switch with `E_r = ∅` has `F_r` meeting `F_w` by P2 (this case is not mentioned in the proof but is immediate).
So every non-empty `F`-side lies in `[y_w - 2l, y_w + 3l]`. Otherwise all `x_w` are within `2l` and every non-empty
`E`-side lies in `3l + 1` positions. The shortest-sequence count (`z_a` distinct, every concentrated side has a
neighbouring `z` in `W`, at most `|W| + 1` such sides) and the search are right; the search is sound for every `S`.
Repairs (none changes the theorem):
1. Running time: one connectivity test costs `O(N + Σ|X|) = O(N + n(l+1)k)` (union-find over the picked sides, each
   of at most `(l+1)k` nodes), not `O(N)`; the bound is `O(n^{(5l+1)k+1} (N + nkl))`.
2. The layout need not be given: run the search with `S` in `E`-mode (rest `F`) and in `F`-mode (rest `E`) for all
   `|S| <= (5l+1)k + 1`; soundness holds for every `S`, completeness by the lemma.
3. The summary sentence "every geometric encoding (bounded reach, ...)" must say bounded reach **and** bounded width:
   with unbounded width every instance has a layout of reach 0 (all nodes at one position).
Checked (`test_La.py`, §9).

## 4. Theorem L(b) — holds

The 3-SAT variant: the cyclic clauses `(¬x^a ∨ x^{a+1})` force all copies equal, and each copy then occurs once in
its original clause, once positively and once negatively, so twice with the sign of its original occurrence and once
with the other (variables with one occurrence are kept; the case `q = 1`, where the cyclic clause would be a
tautology, is not mentioned but needs no copies). The encoding: conflict edge `d_ac` is covered only by `E_a` and
`E_c`, a clause edge only by the `F`-spans of its literals; both directions of the proof are right. Width 1, reach 2.
Checked (`test_Lb.py`, §9).

## 5. Theorem T — holds

Steps filled in (asserted without proof in dc-hardness.md):
- *Minimal covers are chains.* In a minimal cover no span contains another (it would be redundant), so sorting by
  left end gives strictly increasing left and right ends. The edge `(right(I_a), right(I_a) + 1)` (`a < r`) is
  covered by some `I_b` with `left(I_b) <= right(I_a) < right(I_b)`, so `b > a` and `left(I_{a+1}) <= right(I_a)`.
  If `left(I_{a+2}) <= right(I_a)`, every edge of `I_{a+1}` lies in `I_a` or in `I_{a+2}`, so `I_{a+1}` is redundant.
  Spans of length 0 never occur in a minimal cover with `K >= 1`.
- *Two members of one group come from distinct switches* (same type; the mode vector picks one side per switch), so
  their disjointness and P2 make the partners meet; a group with two members has non-empty partners.
- *Soundness of the BFS with merged states*: condition (i) is local to a member, and (ii) compares a new member only
  with stored members; since every member containing a `φ` junction is stored, (ii) holds for the whole chain, and the
  argument "both `X` and its partner contain a `φ` junction" excludes two sides of one switch. Hence every accepted
  chain is picked by one mode vector and covers the line.
- *State bound*: the chain conditions (enforced through the stored previous span) put every junction in at most two
  members, so at most 8 stored spans; `O(n^{10})` states and `O(n)` transitions per guess, `(K + 2)^4` guesses.
  (Junctions with the same membership in all spans are interchangeable, so the guesses can be restricted to one
  junction per class; with spans given by endpoints the bound is `O(n^4 · n^{11})` without `K`.)
No counterexample: own implementation (§9) = brute force on all instances, including exhaustive enumeration of every
TIC + P2 instance with small `K` and `n`, switches with an empty side, repeated spans, spans equal to their partner,
spans of length 0, broken rigid families and planted long chains.

## 6. Theorem H and its remarks

**Theorem H — holds.** The proof is that of Theorem T with "chain" replaced by a shortest sequence: `X_a ∩ X_b = ∅`
for `|a - b| >= 2`, every node in at most two members, partners of one group pairwise meeting (distinct switches,
same type, disjoint), pierced by `Φ_g`. Soundness with walks (repetitions allowed): if `X` and its partner `X'` both
occur, (i) at `X` gives `X' ∩ Φ_{g(X)} != ∅` and (i) at `X'` gives `X ∩ Φ_{g(X')} != ∅`, so both are stored and (ii)
fails. In particular a member not meeting `Φ` can never be followed by its partner, so not storing it is safe.
Completeness: the shortest sequence of a solution passes every check (at most two members through each node).

**Remark (2), first part ("the t-search fails on `R_L` for `L > 8t`") — holds.** Every accepted walk belongs to the
unique solution, so it consists of `h`-sides and visits every `h_k`; a node lies in at most two flip sides, so each
`Φ_g` covers the partners of at most `2t` switches, and the four groups cover at most `8t`.

**Remark (2), "the equivalent forms of Section 2 (interval form, or `t` added to every flip side) are Helly" —
false for the second form.** Counterexample (smallest, `L = 5`): in `R_5` with `t` added to every flip side, the
`F`-sides `h_4`, `Fl_1`, `Fl_3` pairwise intersect (`h_4 ∩ Fl_1 = {z_14}`, `h_4 ∩ Fl_3 = {z_34}`,
`Fl_1 ∩ Fl_3 = {w_13, t}`) and have no common node. For `L <= 4` the form is Helly. The conclusion "solved with
`t = 1`" survives for a different reason: all partner families are families of flip sides, all of which contain `t`,
so `Φ_g = {t}` pierces them; Theorem H needs piercing of the partner families only, not the Helly property of all
sides. (The interval form is Helly: intervals.)

**Remark (2), dead sides — holds (proof added).** Setting of Lemma D; let `D_1, .., D_p` be the sides whose nodes
are all connectors, and add `t` to each. Take a shortest sequence of picked sides from `s` to a side containing `t`.
A side `D_i` cannot occur before the last position: its only node of `I0 + t` is `t`, so entering it through an
`I0`-node means the previous side contains `t`. Hence the first consecutive pair sharing only connector nodes, if any,
is preceded by an `s`-`X` path of `I0` and Lemma D's argument applies; if there is none, the sequence (without a final
`D_i`, which would be entered through `t`) lies in `I0`. So the answers do not change.

## 7. Consequences for a hardness proof

**Item 1 — holds, repair given (wording).** What is proved: if a polynomial reduction maps an NP-complete problem to
2CH + P2 and some constant `t` exists such that all but finitely many yes-instances in its image have a solution with
a shortest sequence whose four group partner families are each pierceable by `t` nodes, then P = NP (compose the
reduction with the `t`-search, which is sound on all instances). So, unless P = NP, for every `t` infinitely many
produced yes-instances have, for every solution and every shortest sequence, a group whose partner family has
piercing number `> t`. The text's "for every solution of its yes-instances" reads as a property of every
yes-instance, which is not what is proved; "intervals, subtrees or bounded reach cannot work" needs "unless P = NP"
and "bounded reach and bounded width" (§3).

**Item 2 and the summary ("the remaining room for a hardness proof is non-Helly side families or ties") — gap
(overstatement).** The open case of DC is equivalent to *general* ZZ + P2 (Theorem 13), and SW (= 2CH) is the special
case in which the middle elements form an antichain with real edges only to the bottom and top classes. Besides ties
(two-way implications), general ZZ + P2 has one-way comparabilities between middle elements (`x < y`: "`y` in the
cut ⇒ `x` in the cut"), real edges between comparable middle elements, and bottom/top elements not equivalent to
`u`/`v`. None of Lemma D, L, T, H says anything about these, and they are exactly what the NP-hardness proof of
ZZ without P2 uses (theory-dc.md 13(c): the conflict relations `P_{j,k} < F_i` are one-way comparabilities between
middle elements). Repair of the statement: "through SW + P2 a hardness proof needs non-Helly partner families with
unbounded piercing number; through general ZZ + P2 it may in addition use ties, comparabilities between middle
elements and edges between them, none of which is covered by Theorems L, T, H."

## 8. Other statements checked in passing

(Filled in below.)

## 9. Computations

(Filled in below.)
