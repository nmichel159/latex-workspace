# Notes on `03-diameter-three.tex` (Section 3, W-hard, 2026-10-31)

Draft compiles in a stub wrapper (article class, same macros); the only undefined references are the Section 2 labels
(`prop:open-pairs`, `lem:minimum-cuts`, `lem:basic-bounds`, `prop:easy-pairs`) and the citation key `Michel2026MinCutPath` (not in the stub). `scripts/check-text.ps1`: 2 findings, both intended (see below).

## Statements and labels

| Label | Statement | Source |
|---|---|---|
| `sec:dt-diameter-three` | Section 3 | |
| `sec:dt-construction`, `sec:dt-correctness`, `sec:dt-results` | subsections | |
| `con:dt-graph` (a `definition`) | the graph `G_phi`, `A_tau` | theory-hardness 2.1 |
| `fig:dt-construction` | figure `hardness-construction.pdf` | |
| `lem:dt-forcing` | Lemma (Forcing) | Lemma 2.2 |
| `lem:dt-cuts` | Lemma (Minimum cuts), parts (i), (ii) | Lemma 2.3 |
| `lem:dt-cut-graphs` | Lemma (Cut graphs) | Lemma 2.4 |
| `thm:dt-hardness` | PathInMinCut is NP-complete, also for `d = 2` on diameter three | Theorem 2.5 |
| `cor:dt-consequences` | (a) `cp = c`, (b) decision version, `b = c`, computing `cp`, (c) `cp = c + d - 1` coNP-complete | Corollary 2.6 (a)-(c) |
| `rem:dt-not-in-dc` | `G_phi` not in DC (fillers) | Remark (2), with E1 |
| `rem:dt-bounded-cut-value` | bounded `c(u,v)` is polynomial | Remark (1) |
| `rem:dt-shifted-class` | results hold in "`d <= 3` or `c <= 2`" | Section 5 of the source, verify 1.5 (b) |

Macro needed (block `% MACROS:` at the top): `\PathInMinCut`.
External labels used: `prop:open-pairs`, `lem:minimum-cuts`, `lem:basic-bounds`, `prop:easy-pairs`. Citation:
`Michel2026MinCutPath` once (Theorem 8.4, FPT in the threshold; number as in the current manuscript of article 1).

## Changes against the source

- **Notation follows the figure** `hardness-construction.pdf`: `K_A, K_B, h_k, beta_k, a_1, a_2, b_1, b_2` became
  `K^u, K^v, u_k, v_k, w_1, w_2, z_1, z_2`; `L_k` (levels) became `T_k` (the source also used `L` for the number of
  literals); `M = c0 + 2` became `N`; the number of variables `n` became `p` (`n = |V|` in the article). The edge count
  uses `sum_i (|O_i| - 1) = L - p`; every variable is assumed to occur (the source says "variables that occur").
- **Slip in Lemma 2.4 of the source (not in the verification report).** The proof said "a positive occurrence of `x_i`
  lies in `A_tau` iff `tau(x_i)` is true, a negative one iff `tau(x_i)` is false". This contradicts the definition of
  `A_tau` (the set `O_i` contains occurrence vertices of both polarities and lies on one side as a whole, so every
  occurrence vertex of `x_i` is in `A_tau` iff `tau(x_i)` is true). The list of edges of `H_tau` that follows in the
  source, the report's line-by-line check (1.4) and the figure all use the correct rule. The draft states the correct
  rule and keeps a `% TODO(check)` comment. No result is affected.
- Lemma 2.3: the description of `delta(A)` (rungs, two edges per occurrence vertex, sync edges) is now part of the
  statement (part (i)), because Lemma 2.4 uses it; it was inside the proof in the source. Added "distinct assignments
  give distinct cuts" (verification 1.3).
- `G_phi` is stated to be connected (needed for `prop:open-pairs`).
- NP membership: certificate is the edge set `S` (`|S| = c(u,v)`, no `u`-`v` path in `G - S`, a `u`-`v` path in `S`),
  instead of Corollary 1.4 and Lemma 1.3. `cp = c` iff a minimum cut contains a path is `prop:open-pairs`.
- E1: Remark (2) now says `c(f, f') = c_0` (the source said `M - 1`), justified by "the proofs of the two lemmas apply
  to `f`, `f'` in place of `u`, `v`".
- E2: Corollary (c) has the wording of the report: the union of any minimum cut and any shortest path is a minimum
  cut-path when `cp = c + d - 1` (one-line proof from `lem:basic-bounds`, no reference to Remark 5.6 of article 1), and
  for `d = 2` the converse (a minimum cut meets a path with two edges in exactly one edge, `lem:minimum-cuts`).
- Remark (1): Corollary 1.4 is replaced by the FPT result of article 1 (Theorem 8.4), which the source also names.
- Remark (3) of the source (3-SAT) is in the definition `con:dt-graph`. "3-SAT" is written without a citation (the
  project bibliography has no entry for Cook or Karp; the canonical bibliography has `Cook1971Complexity` and
  `Karp1972Reducibility`, which could be added to the project `.bib` if the author wants a citation).
- `rem:dt-shifted-class` is new in wording only: one sentence from the source's Section 5 table and verify 1.5 (b); drop
  it if the Introduction or Conclusion says the same.

## Left out

- Corollary 2.6 (d) (lengths of paths in minimum cuts, `>= 2m + 1`) and, with it, E3 and the smallest example
  `(x_1) and (x_1)`, as the spec says.
- Section 2.3 (computational check, 399 and 4537 formulas), Lemmas 1.1-1.3 and Corollary 1.4 (Lemma 1.1 is
  `prop:open-pairs`), O5 (Section 3), Sections 4-9 of the source.
- The 8-vertex example of E2 (`d = 3`, a union of a minimum cut and a shortest path is a minimum cut-path but
  `cp != c + d - 1`); the draft states only the direction that holds and the case `d = 2`.
- No worked example with numbers (not in the source; the figure shows `phi = (x_1 or not x_2) and x_2`).

## Figure

`projects/clanok-3-min-cut-path/hardness-construction.pdf` is a drawing of this construction for
`phi = (x_1 or not x_2) and x_2` with the labels `K^u, K^v, u_k, v_k, w_1, w_2, z_1, z_2, o_{k,j}, A_tau`; clique edges
omitted, synchronization edge dotted, red path `u_0 v_0 o_{1,1} v_1 o_{2,1} v_2` in `delta(A_tau)` for
`x_1 = x_2 = true`. The draft uses exactly these labels and the one-line caption states the formula and the red path.
It renders correctly (checked in the stub wrapper).

## Unclear or for the author

- Section 3 uses `m` for the number of clauses, `L` for the number of literals, `p` for the number of variables
  and `N` for the clique size, all local to this section.
- `check-text.ps1` flags `\label{con:dt-graph}` (prefix `con` is not in its list, but the blueprint prescribes it) and
  the intended `TODO(check)` comment.
- The article 1 theorem number in `rem:dt-bounded-cut-value` (8.4) is that of the manuscript at 2026-10-31; update it
  if article 1 is renumbered.
- The definition environment holds the construction (no `construction` environment in the class).
