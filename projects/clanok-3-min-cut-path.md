# Article 3 - Min Cut-Path: NP-completeness on diameter three and a polynomial algorithm for distance or cut-value at most two

Status: **second version, 2026-10-31**: 35 pages, 12,800 words. `main.tex` is the source; the first version (44 pages, commit `c1c0fc6`) was assembled by
`projects/clanok-3-min-cut-path.submission/assemble.py` from `drafts/`, with the blueprint `SPEC.md`. Do not rerun `assemble.py`. Sections 5 and 6 were then
rewritten directly on the preorder (draft: `drafts/05-06-direct.tex`): no bridge-free graph `K`, no multigraph `H` with ears, no switch form with nodes and sides, and
`n^31 · n^O(1)` instead of `n^71 · n^O(1)`. Results of article 1 are only cited, on the author's request (2026-10-31).
Sections: 1 Introduction (with `thm:main`), 2 Preliminaries, 3 NP-completeness on diameter three (`thm:dt-hardness`), 4 Pairs with cut-value at most two (squares,
`thm:linear-time`), 5 Zigzag problem (`thm:zz-reduction`, `lem:zz-valid`), 6 Polynomial algorithm (`thm:pa-formulas`, `thm:pa-open-case`), 7 Conclusion.
The author has read nothing of it.

Checks: build clean, no undefined reference, no overfull line, 7 figures. Package check `-Template sn-jnl -Flat -KeepComments -CheckOnly`: `Verdict: PASS`, 1 finding
(`[ai-declaration]`). `check-text.ps1`: 3 findings kept (the logged "to the best of our knowledge"; "Vital" in a problem name; the sample's "Acknowledgements").
`check-bib.ps1`: 1 recommended (no issue number for `LeLe2019MatchingCut`).

## Reviews

- Sections 1 to 4: `projects/clanok-3-min-cut-path.submission/review/referee-article.md`: no gap, 3 easily repaired errors and 8 minor points, all applied (M4 is below).
- Sections 5 and 6 as rewritten: `review/referee-direct.md` with programs in `checks/`. **Unfinished at the last stop: first pass by hand with no gap and no error, computations
  not reported yet; until it holds, the rewrite is not a reviewed result.** If it stopped, resume this referee only, reading that file first. The earlier reviews
  (`open-cases/verify/rv-r6-chain.md`, `rv-r7-desc.md`) cover the older form of the proof.

## Next steps

1. Finish `review/referee-direct.md` and apply its findings to `main.tex`.
2. Commit the second version: the working tree holds it uncommitted; the last commit `c1c0fc6` is the first version with 44 pages. Keep `checks/runs/` small.
3. The author reads the article; then shorter proofs and the open points below.

## Intent

| | |
|---|---|
| Type | journal article, theory (graph algorithms) |
| Language | English (American spelling) |
| Author's plan (2026-10-31) | one article: NP-completeness only for diameter three; then "diam or cut 2" is in P by two proofs, the squares for `c <= 2` and ZZ + P2 for `d = 2`, `c >= 3`. First version in order, later improvement and simpler proofs. What is in article 1 is at most cited, never restated with its proof |
| Class | `sn-jnl` (template 3.1), options as article 2; byte-identical `sn-jnl.cls`, `sn-mathphys-num.bst` from `templates/sn-jnl/` |
| Target journal | not decided (article 2 targets Algorithmica) |
| Sources | `projects/clanok-2-min-cut-path/main.tex` (squares; article 2 stays unchanged); `projects/clanok-2-min-cut-path.submission/open-cases/` (`theory-hardness.md`, `qp-proof.md`, `r7-desc.md`, reviews in `verify/`) |

The four answers of `knowledge/writing/paper-structure.md` §1:

| Question | Answer |
|---|---|
| **Main claim** | Min Cut-Path is NP-complete on graphs of diameter three, and solvable in polynomial time on graphs in which every pair has distance or cut-value at most two |
| **Contributions** | (1) NP-completeness on diameter three, already for `d(u,v) = 2`. (2) Linear time for pairs with `c <= 2` (squares). (3) Reduction of pairs with `d = 2`, `c >= 3` to the zigzag problem ZZ + P2. (4) Polynomial algorithm for ZZ + P2 |
| **Closest work** | article 1, article 2, the master's thesis; minimum cuts: Picard and Queyranne (see article 2, Section 1.1) |
| **Reader and venue** | researchers in graph algorithms and connectivity; venue open |

## Open points for the author

- The article overlaps article 2 almost entirely in Sections 2 and 4. What happens to article 2 is the author's decision.
- Article 1 (`Michel2026MinCutPath`, "Manuscript") must be public before submission, because `lem:basic-bounds`, half of `lem:minimum-cuts` and five further results are only cited from it; the numbers (Lemma 2.3, Theorems 3.10, 3.11, 5.5, 6.2, 8.4, Lemmas 5.4, 6.1) must be rechecked against the public version.
- `lem:basic-bounds` cites the proofs of Lemma 2.3 and Theorem 3.11 of article 1, because two of its clauses are not stated there. Stating them in Lemma 2.3 of article 1 would shift no number and allow a plain citation.
- Everything is AI-written and AI-reviewed so far: the AI-use statement and the author's reading are required before submission.
- The Declarations still hold the template's placeholders (Funding, Competing interests, Author contribution).

## Removed from the first version

`rem:bridges`, `rem:coarser`, the last statement of `cor:dt-consequences`(c), `lem:zz-bridges`, `lem:zz-ears`, `lem:zz-multigraph`, the switch form (`def:zz-general`, `def:zz-switch-form`, `lem:zz-answers`), `lem:pa-windows`, `lem:pa-duality`. All of it is in commit `c1c0fc6`.
