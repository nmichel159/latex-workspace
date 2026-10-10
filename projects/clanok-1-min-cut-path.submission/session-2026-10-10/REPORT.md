# Article 1, session of 2026-10-10: report for the author

Brief: `../NEXT-TASK.md`. Manuscript: `projects/clanok-1-min-cut-path/main.tex`. State before the session: commit
`03b6a69`. Nothing was committed in this session (the workspace rule "do not commit unless asked" was enforced by the
permission mode); `git diff 03b6a69` shows every change.

## Result

- Build: 17 pages (before: 17), no undefined references or citations, BibTeX without warnings; the only overfull box
  is the class's own at `\maketitle`. Words (rough count of the source): 8336 -> 8409.
- `package-project.ps1 -Template els-cas -Flat -KeepComments`: `Verdict: PASS` (one advisory finding: no AI declaration).
- `check-text.ps1`: 7 findings, all judged false positives (problem name "Most Vital Edges" three times, authors named
  before `\cite` three times, the one logged novelty sentence). `check-bib.ps1`: 2 recommendations (no issue number in
  Crossref for two journal entries).
- Phase B (computation): no statement of Sections 2-5 failed. Scripts, logs and a summary: `../checks/README.md`.

## What changed in the manuscript

| Place | Change |
|---|---|
| Section 1 | Matching Cut sentence without the symbol `d` ("every fixed diameter at least three"). The comparison with Shortest Path Most Vital Edges now says "with unit edge lengths" (the source proves the diameter results only for unit lengths; for arbitrary lengths the problem is NP-hard on complete graphs). |
| Section 2 | "Most statements concern a graph `G = (V, E)` and two distinct vertices" (`G`, `V` were not introduced). |
| Section 3 | Lemma 3.5: the proof says at its start what it shows; connecting paths have "exactly `Λ`" edges everywhere (as in `Calibrate`). Theorem 3.9: one plan sentence. Figures 5 and 8: labels `L_{j,k}` instead of `L_{j,k,i}` (the text has two indices since 2026-10-09). |
| Section 4 | Proof of Theorem 4.5: the count of the cut edges is one display with three groups (i)-(iii); `deg(u, I)` no longer appears in the estimate (it was 0; the reason now stands before the count). Figure 10 marks the groups (i)-(iii); caption on one line. |
| Section 5 | The cactus argument is Lemma 5.1 with a proof environment (same sentences). Theorem 5.1 is now Theorem 5.2; its proof cites the lemma at the two places where it is used. |
| Section 6 | Citations with verified locations: Theorem 6.2 cites Chung and Lu only; Theorem 6.3 cites Bollobás, p. 169 (Frieze-Karoński has no such theorem); Chernoff bound: Frieze-Karoński, Eq. (21.19); coupling: Section 1.1. Lemma 6.4: bound variable `x` instead of `v`. |
| Section 7 | The diameter-three question is split in two sentences and restricted to unit edge lengths for Most Vital Edges. |

Old figure PDFs: `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-10-figure-10/` and `2026-10-10-figure-labels/`.

## Decisions for the author

Recommendation first. The list is kept as it was written, with the numbers of the morning build.

**Status (2026-10-10, later):** the author approved the recommendations ("súhlasím"). Applied: 1 (b, c, e, f; a and d
are "keep"), 2 (a, b), 3, 4, 5, 6, 7, 8 (the bound of Chung and Lu is cited without a theorem number until the journal
PDF confirms "Theorem 4"), 9, 10. Wording differences from the proposals below: Definition 4.2 keeps the author's
four items, written in words; Definition 3.3 keeps two items (at most one edge in each link; no single edge);
Theorem 6.1 cites Frieze-Karonski, Exercise 1.4.8, for the known fact and has its proof. New numbering: Corollary
2.4, Definition 2.5, Definition 3.5, Lemmas 3.6-3.9, Theorems 3.10, 3.11, Corollary 3.12, Definition 4.2. Build:
18 pages; packager `Verdict: PASS`. Still open: 11 (title, keywords, novelty sentence, AI declaration, funding),
12 (`url` of `Frieze2016`, optional citation of Baier et al.), the theorem number in the journal version of Chung
and Lu.

1. **Symbols.**
   - (a) Clauses `C_k` and cut `C`: keep (no cut occurs in Section 3.1).
   - (b) Threshold `k` of the decision version -> `b` (decision box, proof of Theorem 3.10); `k` is the clause index and
     `t` the number of links of a thread.
   - (c) Cut-path always `S`: `F` -> `S` in the decision box and in Theorem 3.10; in the proof of Lemma 4.4 write
     `C \cap P` instead of naming it `S`; `\deg(x, S)` -> `\deg(x, W)` (in the proof of Theorem 4.5 the letter `S` is the
     cut-path a few lines earlier).
   - (d) Parts `I, J, K, L` of Section 4: keep (the links always carry an index). Alternative: `N_1, B_1, B_2, N_2` and a
     redrawn Figure 10.
   - (e) Algorithm `A` of Definition 2.4 -> `\mathrm{ALG}` (pairs with `\OPT`; the sides stay `A_1, A_2`); `I(n)` ->
     `\mathcal{I}(n)`.
   - (f) New: the index `r` of `Thread` (`K_r`, `\sigma_r`, "for some `r`") clashes with the number `r` of chain links
     (Definition 3.2, `BuildChain(u,v,r)`, same list of procedures). Proposal: index `h`.
   - Left as they are: `n` (variables in Section 3, vertices elsewhere; declared), `p, q` (ends of a chain link) vs. `p`
     (edge probability), `x_i` vs. `x`.
2. **New statements.** (a) After Lemma 2.3, yes:
   `\begin{corollary} Let $C$ be a minimum $u$--$v$ cut and $P$ a shortest $u$--$v$ path. Then $|C \cup P| \leq 2\cp(u,v) - 1$. \end{corollary}`
   with the proof `$|C \cup P| \leq c(u,v) + d(u,v) - 1 \leq 2\max\{c(u,v), d(u,v)\} - 1 \leq 2\cp(u,v) - 1$`.
   (b) After Theorem 3.10, yes: `It is NP-complete to decide whether $\cp(u,v) = d(u,v)$.` (the proof of Theorem 3.10
   shows that this holds iff a separating shortest path exists). (c) "Every vertex other than `u`, `v` has degree at
   most three": true (checked), but not recommended, because `u` and `v` have unbounded degree.
3. **Definition 2.4 vs. Theorem 6.6.** State what the proof shows and keep the scheme as a consequence:
   `Let $\alpha > 1$ and $p \geq \alpha \log n / n$, and let $\beta_1$ be the constant of Lemma~\ref{lem:degree-bounds}. Then, with high probability, every two distinct vertices $u, v$ of $G(n,p)$, every minimum $u$--$v$ cut $C$ and every shortest $u$--$v$ path $P$ satisfy $|C \cup P| \leq \bigl(1 + 1/(\beta_1 \log\log n)\bigr)\,\cp(u,v)$. In particular, for every $\epsilon > 0$, the algorithm that returns $C \cup P$ is an average $(1+\epsilon)$-approximation scheme.`
   Definition 2.4, item 3, with a probability instead of a ratio of counts: `for a given probability distribution on $I(n)$, the probability that a random input lies in $I_A^{\mathrm{opt}}(n)$ tends to one as $n \to \infty$`. The abstract and
   the introduction then say "with high probability" instead of "on almost all inputs".
4. **Definitions 3.3 and 3.4.** Keep both. Definition 3.3: item 2 ("edge-disjoint from every other thread") defines
   a thread through other threads; move it out as a sentence about the construction: `Any two threads of the construction are edge-disjoint and share only the vertices $u$ and $v$.` Definition 3.4: "let `P` be a thread under
   construction that does not yet pass through `L`".
5. **Lemma 4.2 as a definition** (it has no proof), same number and label:
   `Let $J$ and $K$ be the sets of vertices of $A_1$ and $A_2$, respectively, that are incident to an edge of $C$, and let $I = A_1 \setminus J$ and $L = A_2 \setminus K$.`
6. **Chain path, hits, consistent** (first paragraphs of Section 3.1.3): one `definition` environment, yes; the four
   lemmas refer to these terms.
7. **Theorem 6.1** (constant `p`, diameter two): no numbered statement was found in Bollobás (Theorem 10.10 with
   monotonicity implies it) or in Frieze-Karoński (only Exercise 1.4.8). Recommended: a proof of five lines, as in the
   version of the section you accepted on 2026-10-09: two fixed vertices have no common neighbor with probability
   `(1 - p^2)^{n-2}`; the union bound over fewer than `n^2` pairs gives `n^2 (1 - p^2)^{n-2} \to 0`; the graph is
   complete with probability `p^{n(n-1)/2} \to 0`.
8. **Theorem 6.2** is derived from Theorem 4 of Chung and Lu, not stated there. Recommended: one sentence after the
   theorem: `For $\alpha > 1$, Theorem~4 of~\cite{ChungLu2001} gives $\diam(G) \leq \lceil \log((33\alpha^2/400)\, n \log n) / \log(\alpha \log n) \rceil + 2$ with high probability, which is at most $\log n / \log\log n$ for all sufficiently large $n$.`
   "Theorem 4" is the number in two authors' PDFs; the journal PDF could not be opened (robot check). Please open
   https://www.sciencedirect.com/science/article/pii/S0196885801907201 and confirm the number.
9. **3-SAT citation.** Cook 1971 and Karp 1972 state the form with at most three literals; the article uses exactly
   three. Recommended: `\ThreeSAT{} is NP-complete~\cite{Cook1971Complexity,Karp1972Reducibility}; a clause with fewer than three literals is padded by repeating one of its literals.` (The reduction was checked on clauses with repeated
   literals.) `Karp1972Reducibility` is verified in the canonical `.bib` and would be copied to the project.
10. **Conclusion, last question.** For a fixed `k`, deciding `\cp(u,v) \leq k` is polynomial (try all sets of at most
    `k` edges), so "instances in which `\cp(u,v)` equals a fixed constant" cannot be where the hardness lies. Proposal:
    ask whether the problem is fixed-parameter tractable in `\cp(u,v)`.
11. **Front matter and submission.** Title (keep, or "The Min Cut-Path Problem: NP-Completeness and Polynomial
    Cases"); keywords; the novelty sentence: the search of 2026-10-10 again found no work by others, but your thesis
    record and the CSGT 2026 abstract are found by search engines, so say it in the cover letter at least; AI
    declaration (model and version); funding sentence. Highlights are drafted in `../highlights.txt` (five lines, at
    most 78 characters).
12. **Bibliography.** `Frieze2016` carries a `url` to the authors' PDF of 2026, whose numbering differs from the
    printed book the entry describes (Chernoff bound: (21.19) in print, (34.19) in the PDF). Recommended: drop the `url`.
    Optional citation: Baier et al. 2010 (ACM Trans. Algorithms 7(1)) for the term "length-bounded edge cut"
    (`related-work-check.md`, section 2.2); needs a reading note first.

## Noticed, not changed

- Introduction: "small cuts and edge connectivity~\cite{Mehlhorn2017Certifying} have been studied in detail" is broader
  than the paper (certifying 3-edge-connectivity); "Paths and cuts are related by the max-flow min-cut theorem" (the
  theorem relates flows and cuts). Conclusion: the duality sentence holds for connected plane graphs and has no source.
  Proposed wordings: `related-work-check.md`, Part 1.
- `V(G)` is used twice (Lemma 6.4, proof of Lemma 6.5); both could be written with `\delta(G)`.
- Proof of Theorem 3.9, part (b): "it hits every thread (Lemmas 3.6 and 3.7)" is not needed, Lemma 3.8 gives the claim.
- Lemma 4.2 writes `\forall`, `\exists`, `\nexists` inside list items (decision 5 removes them).
- Still open from before: Theorem 6.3 rests on a remark in Bollobás's book that credits Bollobás and Thomason (1985);
  that chapter was not read (`sources-section-6.md`, Q3).

## Files of this session

- `sources-section-6.md`: sources and locations for Section 6 and for 3-SAT (agent report, with what stays unverified).
- `related-work-check.md`: every related-work sentence against its reading note; the repeated novelty search.
- `referee-report.md`: independent referee-style review of the PDF (see "Referee review" below).
- `../checks/`: scripts and logs of the computational checks.
- Knowledge base: `knowledge/bibliography/references.bib` (comment lines of `Bollobas2001`, `Frieze2016`, `ChungLu2001`,
  `Karp1972Reducibility`), `knowledge/literature/searches.md` (14 rows of 2026-10-10),
  `knowledge/literature/Bazgan2019MostVital.md`, `knowledge/research/min-cut-path.md` (numbers, computational results).

## Referee review (2026-10-10, afternoon)

Independent review in the role of a DAM referee: `referee-report.md` (it covers the 18-page version with the approved
decisions; line numbers are those of that version). Verdict of the reviewer: **major revision, borderline minor**; no
error in the mathematics, no blocker. The recommendation is driven by passages that assert instead of justify, by
missing examples and by results that are easy to add.

### Applied (reasons made explicit, wording; no new result)

| Finding | Change in `main.tex` |
|---|---|
| M1 | `d(x,y)`, `c(x,y)` for any two distinct vertices, `d = \infty` without a path (one sentence in Section 2). |
| M2 | `G \setminus F` for any edge set; after Definition 2.1: a set `S` is a cut-path iff it contains a `u`-`v` path and `G \setminus S` has no `u`-`v` path. |
| M5 | 3-SAT box: "exactly three literals, not necessarily distinct". |
| M6 | After Definition 3.3: the word thread refers from then on to the paths created by `Thread`. |
| M7, P3(a) | New paragraph "The construction is well defined" (a threading always finds an edge; the links between the first threading and `Calibrate`; ends of crossing edges; the order in which a thread visits its links; independence of the free choices). |
| M8 | Proof of Lemma 3.9: two sentences with the reasons for "`Q` starts ..., ends ..., passes ..."; the sign of a crossing edge is defined in item (a). |
| M9 | Proof of Theorem 3.11: `b := d(u,v)` is defined because `u`, `v` lie in one component (Section 2). |
| M12 | Proof of Theorem 4.5: the second renaming is justified by the symmetry of `C`, `P` and `P \subseteq C`; "`V` is partitioned". |
| M13 | Proof of Theorem 5.2: the cycles `Z_1, ..., Z_t` are defined before they are used; they are pairwise distinct; the arcs form a walk that contains a path. |
| M14 | After Theorem 6.2: Chung and Lu measure the diameter of a disconnected graph on its largest component; `G` is connected with high probability (Lemma 6.5). |
| M15(b) | Theorem 6.6: "for an arbitrary choice of the two distinct vertices `u, v`". |
| P3(d), P7 | Table 1 lead-in agrees with its caption; "As with ...", "is hit exactly when", "let `\tau` be its truth assignment", "By Lemma 3.7", present tense in the proof of Lemma 5.1. |

Build after these changes: 18 pages, no undefined references; `check-text.ps1` 8 findings (false positives as
before); packager, full run: `Verdict: PASS`. Not committed.

### For the author to decide (content; nothing applied)

Recommendation first.

1. **S2, example with `cp < c + d - 1`: yes.** The two parked graphs show that the upper bound of Lemma 2.3 can be
   strict, that the hypotheses of Theorems 4.5 and 5.2 cannot be weakened to the pair `u, v` alone, and that the formula
   fails in the class the Conclusion calls "a natural candidate". The computation of today adds: they are the only such
   graphs with at most six vertices. Place: after Theorem 5.2; one figure, three sentences; one clause in the
   Conclusion ("but the formula does not hold in it").
2. **S3, corollary for diameter two: yes.** `c(u,v) = \min\{\deg(u), \deg(v)\}`, hence
   `\cp(u,v) = \min\{\deg(u), \deg(v)\} + d(u,v) - 1` and a linear-time algorithm without a minimum-cut computation
   (Theorem 16 of the master's thesis; statement and proof: `referee-report.md`, S3). The classical theorem on
   diameter two (edge connectivity equals minimum degree; attributed to Plesnik 1975) is TODO(verify) before it is cited.
3. **S4, name the class of Section 5: yes.** A connected graph has `c(x,y) <= 2` for all pairs iff it is a cactus
   (checked on all graphs with at most seven vertices); say "cactus graphs" in the abstract, the introduction and the
   section title. The converse direction needs Menger's theorem with a source.
4. **S1, S9, abstract and introduction: yes.** Say that in both classes the upper bound of Lemma 2.3 is attained;
   replace "above the connectivity threshold" by "with edge probability at least `\alpha \log n / n`, `\alpha > 1`"
   (the abstract promises more than Theorem 6.6 proves); name the intermediate problem.
5. **S6, discussion and open questions: yes, one sentence each.** The reformulation
   `\cp(u,v) = \min_P (|P| + c_{G \setminus P}(u,v))` after Definition 2.2; in the Conclusion: approximation below
   factor two (the reduction gives no gap), the complexity of deciding `\cp(u,v) = c(u,v)`, bounded `c(u,v)` or
   `d(u,v)`; drop the question about experiments.
6. **S5, degree at most three: the reviewer disagrees with decision 2(c).** One sentence that says what the
   reduction gives (degree at most three outside `u, v`; `c(u,v)` and `d(u,v)` unbounded) answers the question about
   restricted classes. Recommended now: add the sentence.
7. **M3, M4, M10, M11 (minor).** Corollary 2.4 in the sharper form `|C \cup P| \leq \cp + \min\{c, d\} - 1`;
   Definition 2.5 with one item instead of items 2 and 3; "diameter at most two" in the statements; the decomposition
   of Definition 4.2 named after the pair `(A_1, A_2)`. Recommended: M10 yes, the others as you prefer.
8. **S8(b), claim in the introduction.** "We settle its complexity and prove its basic structural properties" ->
   "We prove that it is NP-complete and identify two graph classes in which the union of a minimum cut and a shortest
   path is optimal." Recommended: yes.
9. **Presentation (P1, P2, P3(b,c,e), P4-P6, P8-P10).** The author's notation `\ell[0]`, `\ell[1]` and Algorithm 1
   were left alone (the reviewer proposes `L_{j,k}` and a first line that creates `u`, `v`); the term "edge boundary"
   for the second meaning of "cut"; statements of Theorems 4.5 and 5.2 as "Then `\cp(u,v) = c(u,v) + d(u,v) - 1`.";
   repeated sentences; the empty "ORCID(s):" line; pages 2, 6, 7, 8 end with empty space because of the `[H]` floats;
   Figures 7, 8 and 10 rely on colour only; the keyword "average-case approximation".
