# Notes: Sections 2 and 4 (W-squares)

Files: `02-prelim.tex` (Section 2), `04-squares.tex` (Section 4). Both are copies of article 2 `main.tex`; text is unchanged
except for the edits below. `check-text.ps1`: no finding except the intended `TODO(check)` in `02-prelim.tex`.

## Section 2 (`02-prelim.tex`, source lines 270-451)

- Added at the top a `% MACROS:` block with `\SSP` (`\textsc{Separating Shortest Path}`); it is used once, in Section 2.1
  ("the \SSP{} problem asks whether $G$ contains such a path"). The integrator drops it if Section 3 defines it as well.
- Proposition `prop:open-pairs` (statement and proof, source lines 1098-1111) moved to the end of Section 2.1, after the
  remark on submodularity. The two sentences that follow it in the source (example $G_b$ and the diameter-two fact of the
  thesis, source lines 1113-1114) came with it. Dropped: the section heading, the two lead-in sentences, and the sentence
  "We do not know a polynomial-time algorithm ..." (open status).
  The $G_b$ sentence points forward to `ex:counterexamples` (Section 2.2); the two sentences can be deleted without loss.
- The sentence on the pairs still to be treated ended with "and `\cref{sec:distance-two}` states what we know about the
  second". The section `sec:distance-two` is no longer in the article, so the clause is deleted and a
  `% TODO(check)` comment asks for a pointer to the sections on pairs at distance two (the integrator or coordinator
  knows the labels of Sections 5 and 6).

## Section 4 (`04-squares.tex`, source lines 453-1047)

- New title `\section{Pairs with Cut-Value at Most Two}` with the new label `sec:squares`; the three sections of
  article 2 became subsections with their titles and labels (`sec:structure`, `sec:separating`, `sec:algorithm`).
  The sentence "Throughout this section and `\cref{sec:separating}`, we assume that $c(u,v) = 2$" now reads with
  "this section" = Section 4.1.
- Removed Proposition 12 (`prop:lengths`) with everything that depends on it: the paragraph that introduces it, the
  directed graph $\vec G$ and the numbers $\lambda^-(e)$, $\lambda^+(e)$, the proposition and its proof, and the three
  closing sentences that restate Theorem `thm:characterization` with condition (i) replaced. Nothing else cites
  `prop:lengths` (checked in the whole of article 2 `main.tex`). The Introduction of article 2 does not cite it either.
- Remark 2 (`rem:coarser`): the sentences that compare with the thesis were deleted: "The thesis ... defines a decomposition
  ...", "The construction starts ...", "It splits a square ...", and the clause "and it is a general square graph in the
  sense of [Definition 40]". Kept: the definition of $F'$, the claims about the lemmas and theorems, the failure of
  (v), the condition on the algorithm, "The square decomposition defined here is the finest of the decompositions of
  this remark. For $G \in \DC$, it satisfies the distance condition by `\cref{thm:structure}(v)`".
- Nothing in Section 4 referred to Theorem 17 (`thm:hardness`) or to the hardness section; the Examples, Remark 2 and all
  figures are kept. The thesis is still cited (`Michel2025MinCutPath`) in Section 2 where the source cites it for a fact
  (Claim 7, Definition 37, Figure 3.3, Theorems 15 and 18, Claim 17); these citations are kept.

## Labels cited but not defined in the two drafts

- `sec:related-work`: cited in Section 4.1 ("the strip of Dinitz and Vainshtein (see ... and `\cref{sec:related-work}`)").
  In article 2 it is the subsection "Related Work" of the Introduction. The coordinator must either define this label in
  the Introduction (Dinitz and Vainshtein strip, Picard and Queyranne, cactus) or the reference is replaced.
- Labels of the other drafts are not cited from Sections 2 and 4. The removed `sec:distance-two` and `prop:lengths`
  are no longer cited anywhere in the two drafts.
- Labels of the two drafts that the Introduction of article 2 cites (all present): `cor:class-pairs`, `cor:two-edges`,
  `ex:counterexamples`, `lem:basic-bounds`, `lem:criterion`, `lem:residual`, `prop:easy-pairs`, `prop:open-pairs`,
  `sec:algorithm`, `sec:class`, `sec:separating`, `sec:structure`, `thm:characterization`, `thm:linear-time`,
  `thm:structure`. The Introduction of article 2 also cites `thm:hardness`, which is not in these drafts (Section 3
  of article 3 carries the hardness result under its own labels).

## Figures used (files in the project folder)

`graph-classes.pdf`, `counterexamples.pdf` (Section 2); `square-decomposition.pdf`, `decomposition-example.pdf`,
`worked-example.pdf`, `square-terminals.pdf` (Section 4). `padding.pdf` (hardness of article 2) is not used here.

## Citation keys used

`Michel2025MinCutPath`, `Michel2026MinCutPath`, `Diestel2025`, `PicardQueyranne1980`, `BaswanaPandey2025Carcass`,
`Mehlhorn2017Certifying`, `Erickson2019Algorithms`, `Tarjan1972DFS`. All are in `references.bib` of the project.
`NagamochiKameda1996` is not cited in these two drafts.

## Unclear or optional

- Three figure captions keep the source punctuation with a semicolon or an explanatory colon
  (`fig:graph-classes`, `fig:counterexamples`, `fig:square-decomposition`); the checker does not flag them. A later tidy
  pass can turn them into one clause each.
- The term "directed path" remains in the proof of `lem:residual` (paths in the digraph $D$); its definition for
  $\vec G$ went with Proposition 12. The usage is the standard one.
- No error or gap was found in the copied statements and proofs; no mathematical `TODO(check)` was needed.
