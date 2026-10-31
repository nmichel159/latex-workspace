# Notes on Sections 5 and 6 (W-zigzag), 2026-10-31

Drafts: `05-zigzag.tex`, `06-polynomial.tex`. Nothing was built. Checks run: `check-text.ps1` on both (one finding left,
see "Check findings"), a script for brackets, `$` parity, environments and cross-references (all `\cref` targets exist
in these two drafts or in the Section 2 labels `prop:easy-pairs`, `prop:class`, `prop:open-pairs`, `lem:basic-bounds`,
`lem:minimum-cuts`, `lem:uncrossing`).

**No TODO(check) in the drafts.** Every restructured step was re-derived by hand; no error or gap was found in the sources.

**Switch count of the final proof: at most 71** (Shape A: 4 + 28 + 2 + 18 + 19). Other formulas: Shape B 46, the case of at
most ten classes of `R_0` 42, `F^*` and `E^*` 32, small `A_P` or `B_P` 9.

## Statements

Section 5 (`sec:zz-zigzag`): `def:zz-preorder`, `def:zz-zz`, `def:zz-general`, `def:zz-valid`, `lem:zz-bridges`, `lem:zz-paths-in-q`,
`lem:zz-ears`, `lem:zz-multigraph`, `lem:zz-uncrossing`, `def:zz-instance`, `lem:zz-incomparable`, `lem:zz-down-sets`, `lem:zz-p2`,
`thm:zz-reduction`, `con:zz-switch-form`, `lem:zz-switch-form`, `lem:zz-answers`, `lem:zz-valid`.

Section 6 (`sec:pa-polynomial`): `def:pa-objects`, `lem:pa-basic`, `lem:pa-windows`, `lem:pa-stars`, `lem:pa-duality`, `def:pa-atoms`,
`lem:pa-atoms`, `lem:pa-walks`, `lem:pa-two-jumps`, `lem:pa-one-jump`, `def:pa-formulas`, `thm:pa-formulas`, `cor:pa-switch-form`,
`alg:pa-open-case`, `thm:pa-open-case`. Equations: `eq:pa-ranges-r`, `eq:pa-ranges-c`, `eq:pa-not-below`.

## Deviations from the sources

Restructuring required by the blueprint, re-derived in full:
1. Theorem B: `κ` = the first ten classes of `R_0` by last position; Case II, Shapes A', B', `F_κ` deleted; 𝓚 holds classes of `R_0`
   only; the exit "at most ten classes of `R_0`" is added (`rv-r7-desc.md` §3). The second alternative of the Shape B claim is gone,
   since `κ` holds no class of `C_0`.
2. Of Proposition C only one half of (a) is used and written ("every class of `C_0` has a position greater than `v^*`", paragraph
   "Positions of `C_0`"). The rest of Proposition C is not needed once Case II is deleted.
3. Repair of Corollary B1 (`rv-r7-desc.md` §2.6): instead of "allow every role to be empty", all exits are listed. `def:pa-formulas` has
   six formulas T1-T6, written with `↓S` and `M \ ↑S`; `thm:pa-formulas` says "one of them". T1, T2 are the small exits, T3 is `F^*`, T4
   covers `E^*` and the exit of item 1, T5 is Shape A, T6 is Shape B.
4. Chains and the conflict list of Lemma X moved into the text before Lemma G and into its proof (nine numbered items). Lemma J is
   stated after Lemma G and cites items of the list.
5. New `lem:pa-walks` holds the "Counting" step of Lemma X, and `lem:zz-valid`(b) (Lemma 3.4(b)) is strengthened to "a valid path with at
   most `h` members" for this. The proof is the one of Lemma 3.4(b).

Not requested explicitly, my decisions (each can be undone):
6. Atom `FP(h)` and Lemma R(c) are omitted: after the deletion of Case II nothing uses them. `lem:pa-atoms`(c) is now the `EP(a)` fact of
   `r7-desc.md` §3.
7. Not carried over because nothing uses them: `N_E`, `N_F` (Definition 4.1), the Note after Lemma 4.4, the parenthesis on the consistent
   zigzag in Definition 1.6 (replaced by one sentence on the name ZZ).
8. Lemma 1.3 and Lemma 1.4 are not restated. (a) is `lem:minimum-cuts`, (c) is `prop:open-pairs`, (b) is the transitivity in `prop:class`
   applied to `K` (used in `lem:zz-paths-in-q`(c)). Lemma 1.4: the identity is cited from the proof of `lem:uncrossing`, which counts per edge,
   and its consequences are the new `lem:zz-uncrossing` for the multigraph `H`, without weights, since all weights were 1. `c_H` is defined in
   the statement of `lem:zz-multigraph`.
9. `thm:pa-open-case` adds, as the blueprint asks, the construction of a minimum cut-path: lifting (Theorem 2.9, Lemmas 2.4, 2.7, proof of
   Lemma 3.3) and, in the no-case, `C ∪ π` by the argument of `lem:basic-bounds`.
10. Time in `cor:pa-switch-form`: `(m + 1)^{71}`, tuples over `M` and one symbol for an empty role; a graph search replaces union-find, so
    that `O(ν + σ + m)` is exact.

Renamings (clashes): path length `r` to `q` (clash with `r(a)`); positions `c, d` to `p, p'` (clash with cut-value and distance); `ρ, γ` in (★)
to `α, β` (clash with the private node `ρ`); `Enon`, `Fnon` to `M_E`, `M_F`; chain sides `Z_i` to `Y_i`; `Z ⊆ Ω` to `O`; `X` in Lemma 2.2 to `Y`;
`C(y)` in Lemma 2.7 to `S_y`; `c` to `c_K(u,v)`; `win`, `ℓ`, `e` inside Lemma 4.4 to `I`, `p_0`; "equivalent" to "tied" everywhere; plus the renamings of
SPEC §3 (`A_P`, `B_P`, `U_P`, `L_P`, `ℓ^*`, `r^*`, `u^*`, `v^*`, also in Section 5).

## Unclear or for later

- The term "open case" stays, as in the blueprint (`thm:pa-open-case` is titled "The open case"). In an article that solves it, "pairs at distance two" may read
  better; the integrator can rename.
- The hypotheses `F_x ≠ ∅`, `E_y ≠ ∅` of `lem:pa-duality` are not used by its proof (each case of P2 supplies the node). Kept as in the source.
- `E-member` and `F-member` denote switches in Section 6 (`def:pa-objects`); the proofs of `lem:zz-valid` in Section 5 say "F-member `F_w`" for the side, which is clear from context.
- `lem:pa-stars` keeps nine positions, though the proof gives five (`verify/rv-core-65.md` §2.3); with five, the distance `>= 9` of far pairs, and hence the thresholds and the exponent, could drop later.

## Check findings

- `05-zigzag.tex`: `[latex] \label{con:zz-switch-form}` (prefix not in the script's list). Justified: SPEC §2 prescribes `con:`. The construction is typeset as a `definition`, since the class has no construction environment, so `\cref` prints "Definition".
- `06-polynomial.tex`: none.

## Macros for the preamble

Listed in the `% MACROS:` block at the top of each draft: `\dn`, `\upp`, `\LMN`, `\UMN`, `\pos`, `\nodeof`, `\pk` (Section 5); `\NE`, `\NF`, `\Pos`, `\win`, `\FR`, `\ER`, `\EP` (Section 6). None occurs in `sn-jnl.cls`.
