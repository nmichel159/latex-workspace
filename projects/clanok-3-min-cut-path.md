# Article 3 - Min Cut-Path: NP-completeness on diameter three and a polynomial algorithm for distance or cut-value at most two

Status: **first complete version, 2026-10-31**: 44 pages, 17,300 words. `main.tex` is now the source (assembled once by
`projects/clanok-3-min-cut-path.submission/assemble.py` from `drafts/`, with the blueprint `SPEC.md`; notes of each writer in
`drafts/notes-*.md`). Build clean: no undefined reference, no overfull line, 7 figures. Package check `-Template sn-jnl -Flat
-KeepComments -CheckOnly`: `Verdict: PASS`, 1 finding (`[ai-declaration]`). `check-text.ps1`: 4 findings kept (`on the other
side` is meant literally; the logged "to the best of our knowledge"; "Vital" in a problem name; the sample's "Acknowledgements").
`check-bib.ps1`: 1 recommended (no issue number for `LeLe2019MatchingCut`). **Referee of the assembled text running:
`projects/clanok-3-min-cut-path.submission/review/referee-article.md`.** The author has read nothing of it.
Sections: 1 Introduction (with `thm:main`), 2 Preliminaries, 3 NP-completeness on diameter three (`thm:dt-hardness`), 4 Pairs with
cut-value at most two (squares, `thm:linear-time`), 5 Zigzag problem (`thm:zz-reduction`), 6 Polynomial algorithm (`thm:pa-formulas`,
`thm:pa-open-case`: time `n^71 · n^O(1)`), 7 Conclusion. `padding.pdf` retired to `archives/removed-from-projects/clanok-3-min-cut-path/`.

## Intent

| | |
|---|---|
| Type | journal article, theory (graph algorithms) |
| Language | English (American spelling) |
| Author's plan (2026-10-31) | one article: NP-completeness only for diameter three; then "diam or cut 2" is in P by two proofs, the squares for `c <= 2` and ZZ + P2 for `d = 2`, `c >= 3`. First version in order, later improvement and simpler proofs |
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
- Article 1 must be public before submission if the article cites it (as for article 2).
- Everything is AI-written and AI-reviewed so far: the AI-use statement and the author's reading are required before submission.
- The proof of Sections 5 and 6 has been reviewed in parts (`verify/rv-r6-chain.md`, `verify/rv-r7-desc.md`); the assembled text not yet.
