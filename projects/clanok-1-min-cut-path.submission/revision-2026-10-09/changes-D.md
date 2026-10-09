# Changes in fragment D (Section 6, Section 7, Acknowledgments)

Numbering: Theorem 6.1 = `thm:random-diameter-two`, 6.2 = `thm:random-diameter`, 6.3 = `thm:random-connectivity`,
Lemma 6.4 = `lem:degree-bounds`, Lemma 6.5 = `lem:connectivity-bounds`, Theorem 6.6 = `thm:approximation-scheme`.
All environments, proofs, displays, labels and citations of the inventory are present (see end of file).

## Language
- Section 6, opening paragraph: one sentence defines "with high probability" (probability tending to one as n -> infinity), SPEC §3.
- Prose "with probability tending to one" -> "with high probability": dense-case sentence before Thm 6.1, proof of Lemma 6.4, proof of Lemma 6.5, proof of Thm 6.6, Conclusion par. 1. Displayed limits in statements unchanged; "probability tends to one" in the last sentence of the proof of Thm 6.6 kept (it matches Definition 2.5).
- Proof of Thm 6.6: "can only decrease the distances and can only increase the values c(u,v)" -> "cannot increase the distances and cannot decrease the values c(u,v)".
- Proof of Lemma 6.5: "In this case," -> "Suppose that both events hold." ; "This cut need not be a minimum one, but it gives the upper bound" -> "A minimum u--v cut has at most as many edges as this cut, so"; "Combining these two inequalities, we obtain" -> "Hence".
- Proof of Thm 6.6: "Combining these inequalities, we obtain" -> "Hence".
- Sparse-setting paragraph: "We state two known results ... and prove two consequences for the degrees and for the values c(u,v)" -> "For such graphs, we use two known results, on the diameter and on the edge connectivity [cites]. We also bound the degrees (Lemma 6.4) and the values c(u,v) (Lemma 6.5)." (Lemma 6.4 is not a consequence of Theorems 6.2-6.3, so "consequences" was inaccurate.)
- Lead-in before Lemma 6.5: "The next lemma bounds the values c(u,v)." -> "The edge connectivity of Theorem 6.3 and the degree bounds of Lemma 6.4 bound the values c(u,v)." (says what is used).
- Statements of Thms 6.2, 6.3: "Then:" -> "Then" (the display completes the sentence).
- Conclusion: list made parallel; every item is now a question: "The first is to find further graph classes ..." -> "First, in which further graph classes can the problem be solved in polynomial time?"; "The second question concerns planar graphs. ... Whether this duality helps to solve MCP is open." -> "Second, does duality help to solve MCP on planar graphs?" + the unchanged explanation sentence with both citations; "Third, this work is purely theoretical." -> "Third, how do algorithms for MCP behave on average? This work is purely theoretical." + the experiments sentence ("would answer this question and could guide the design of heuristics"); "Finally, graphs with a fixed value of cp(u,v) deserve a closer study, which may clarify ..." -> "Finally, what is the structure of the instances (G,u,v) in which cp(u,v) equals a fixed constant? A closer study of them may clarify ...".
- Conclusion par. 1: "in sparser ones" -> "in sparser ones with p >= alpha log n / n, alpha > 1" (the hypothesis of Thm 6.6, no new claim).
- Acknowledgments: "Prof.~RNDr.~Martin Loebl,~CSc." -> "Martin Loebl"; content unchanged.

## Exposition
- Paragraph before Thm 6.6: announcement ("These results allow us to estimate ...", "so this simple algorithm is an average (1+eps)-approximation scheme") replaced by its information: "By Lemma 2.4 and its proof, the union of a minimum u--v cut and a shortest u--v path has at most c+d-1 edges, and every cut-path has at least c(u,v) edges. The diameter bound of Theorem 6.2 and the connectivity bound of Lemma 6.5 keep the ratio of these two numbers below 1+eps on almost all inputs."
- The five repeated settings "Let G(n,p) be ... alpha > 1" kept in every statement (statements stay self-contained); the setting is also fixed once in the sparse-setting sentence.
- Dense-case consequence kept as text (corollary proposed in issues-D.md, item 9).
- Class "diam or cut 2" sentence kept verbatim.

## Made explicit
- Proof of Lemma 6.4: why both tails are o(1/n): "because exp(-mu h(a_i)) = n^{-(1-o(1)) alpha h(a_i)} and alpha h(a_i) > 1 for i = 1, 2" (the original asserted o(1/n) without the computation).
- Proof of Lemma 6.4: "Since mu = (1 - 1/n) alpha log n, we have alpha log n / 2 <= mu <= alpha log n for n >= 2." (justifies beta_1 = a_1 alpha/2, beta_2 = 2 a_2 alpha).
- Proof of Lemma 6.5: "Since G is delta(G)-edge-connected, every cut separating two distinct vertices has at least delta(G) edges." (justifies the middle inequality min c(x,y) >= min deg(z)).
- Proof of Thm 6.6: "By Lemma 2.4" -> "By the proof of Lemma 2.4" for |S| <= c+d-1 (the statement of Lemma 2.4 bounds cp, its proof bounds |C u P|; same as Remark 4.6).
- Proof of Thm 6.6, ratio display: the intermediate step (c+d-1)/c inserted before (c+d)/c, so the display starts from the bound actually proved; display split into two aligned lines (align*), otherwise unchanged.

## Formatting
- `\mathbb{P}[...]`, `\mathbb{P}\!\left[...\right]` -> round brackets `\mathbb{P}(...)` with `\bigl( \bigr)` / `\left( \right)` (Thms 6.1, 6.2, 6.3, Chernoff display).
- Inline `\frac` -> solidus: `p = 1/\alpha` (Thm 6.1), `p = \alpha \log n / n` (sparse sentence, Thms 6.2, 6.3, 6.6, Lemmas 6.4, 6.5, proof of Thm 6.6 twice). Thm 6.1 display: `G\bigl(n, \tfrac{1}{\alpha}\bigr)` -> `G(n, 1/\alpha)`. Ratio display: `\frac{\frac{\log n}{\log\log n}}{\beta_1\log n}` -> `\frac{\log n / \log \log n}{\beta_1 \log n}`.
- Chernoff display: `e^{-\mu h(a)}` -> `\exp(-\mu h(a))` (DAM style), both tails.
- One sentence per line throughout; blank-line runs reduced to one.

## Citations
- Thm 6.2 (Diameter): `\cite{Bollobas2001}` -> `\cite{Bollobas2001,ChungLu2001}`; no theorem number (journal numbering not verified). Derivation reported in issues-D.md, item 3.
- Sparse-setting sentence: `\cite{Bollobas2001,Frieze2016}` -> `\cite{Bollobas2001,ChungLu2001,Frieze2016}`.
- Proof of Thm 6.6, coupling: "(see, e.g.,~\cite{Frieze2016})" added after "the standard coupling of the random graphs G(n,p) for different edge probabilities" (bib status comment of Frieze2016: coupling (1.3) and monotonicity (1.7) in Sec. 1.1 of the 2026 PDF; no location cited because the printed numbering is not verified).
- Conclusion, first direction: one new question sentence: "Is MCP NP-hard on graphs of diameter three, the smallest diameter for which finding the most vital edges for shortest paths and finding a matching cut are NP-hard~\cite{Bazgan2019MostVital,LeLe2019MatchingCut}?" Backed by the notes: Bazgan2019MostVital (linear time on diameter <= 2 with unit lengths, Proposition 1; NP-hard on split graphs, hence diameter three, Theorem 4, preprint numbering) and LeLe2019MatchingCut (polynomial on diameter two, NP-complete for every fixed diameter d >= 3, Theorem 1). check-text flags "vital" as [ai-tic]: justified, it is the established problem name.
- Kept unchanged: Thm 6.1 `Bollobas2001`; Thm 6.3 `Frieze2016`; Chernoff `Frieze2016` without chapter number; `Cormen2022`; `itai1979maximum,henzinger1997faster`.

## Bib keys to add
Not yet in `projects/clanok-1-min-cut-path/references.bib` (all three VERIFIED in the canonical file):
- `ChungLu2001`
- `Bazgan2019MostVital`
- `LeLe2019MatchingCut`

## Proposals for other sections
- Section 3, `\cite{Cook1971Complexity}` for the NP-completeness of 3-SAT. The status notes do NOT yet justify `\cite{Cook1971Complexity,Karp1972Reducibility}`: the Karp1972Reducibility entry is VERIFIED as a record only, and its comment says "Content not read ... open pp. 85-103 before the citation goes into a manuscript". Cook's content was read: Theorem 2 shows D3 (DNF tautologies with at most three conjuncts per disjunct; complement = 3-CNF satisfiability) is P-reducible (oracle/Turing reducibility) to tautologies, and "NP-complete" does not occur in the paper. So Cook alone supports NP-hardness of 3-SAT only under polynomial-time Turing reductions. Recommendation: add Karp1972Reducibility after its pp. 85-103 have been read (the searches.md log of 2026-10-09 concludes "Cite Cook and Karp", which presupposes that reading); until then keep Cook only, and editor B/the integrator should not add Karp.
- Section 2, Definition 2.5 (`def:approximation-scheme`): see issues-D.md, item 7 (how Thm 6.6 relies on it).

## Inventory check (after editing)
All 21 inventory items present, same order: section `sec:random-graphs`; opening paragraph (+ w.h.p. definition); dense sentence; Thm 6.1; dense-case paragraph; sparse paragraph; Thm 6.2; Thm 6.3; Lemma 6.4 + proof (both tails, beta_2 kept); lead-in; Lemma 6.5 + proof (three displays kept); paragraph before Thm 6.6; Thm 6.6 + proof (coupling, all displays); `sec:conclusion`; summary paragraph; four open directions (class "diam or cut 2" sentence kept); Acknowledgments. All 12 displays present (the ratio display is now `align*`). Labels unchanged. Citations: all original ones kept, plus ChungLu2001 (x2), Frieze2016 (coupling), Bazgan2019MostVital, LeLe2019MatchingCut.
Test build (integrated fragments, entries of the three new keys added only to the scratch copy of references.bib): no errors, no undefined references, 15 pages. The only overfull box (117 pt, line 121 of main.tex, at \maketitle) is outside fragment D.
