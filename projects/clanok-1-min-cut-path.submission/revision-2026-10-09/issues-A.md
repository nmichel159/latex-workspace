# Issues in fragment A (front matter, Sections 1-2): not applied

Tags: [M] possible mathematical error or gap, [C] change that would alter a claim, [D] proposed deletion or
substantial restructuring, [S] other suggestion. "Section 2" = `sec:fundamentals`.

1. [C] **Novelty sentence vs. the master's thesis** (Introduction, "To the best of our knowledge, the problem has not
   been studied before."). Kept as instructed; it is backed by searches.md (2026-10-07, 2026-10-09), but the author's
   master's thesis (Charles University, 2025) studied Min Cut-Path, and the 2026-10-09 search also found the author's
   CSGT 2026 abstract. DAM's submission form asks about prior publication. Proposal, if the author changes his mind:
   "\MinCutPath{} was introduced in the author's master's thesis~\cite{...}; Theorems~\ref{thm:ssp-np-complete} and
   \ref{thm:mcp-np-complete} [and whichever else is new] are new." At least declare the thesis and the abstract in
   the cover letter.

2. [M] **Two meanings of "cut".** Section 2 (now with the added sentence) and Definition 2.1 use "u-v cut" = any edge
   set whose removal leaves no u-v path. Section 4 (Lemmas 4.2-4.4, proof of Theorem 4.5) uses "cut" = the set of all
   edges between two sides A_1, A_2. Lemma 4.4 (odd intersection) is false for the first meaning (add to delta(A) an
   edge inside A_1 that lies on P). The proof of Theorem 4.5 is fine because a minimum u-v cut is always of the
   second kind, but this is never said. Proposal for Section 2, after the sentence defining a u-v cut:
   "For a vertex set $A \subseteq V$, let $\delta(A)$ denote the set of edges with exactly one end-vertex in $A$.
   If $u \in A$ and $v \notin A$, then $\delta(A)$ is a $u$--$v$ cut, and every minimum $u$--$v$ cut is of this form;
   hence $c(u,v) = \min\{|\delta(A)| : u \in A,\ v \notin A\}$."
   and in Section 4 write "a cut $C = \delta(A_1)$" in Lemmas 4.2-4.4. (The claim "every minimum u-v cut is of this
   form" is standard: a minimal u-v cut equals delta of the component of u after its removal; a one-line proof can be
   added.)

3. [M] **"cut-value" / "minimum cut-value" is never defined.** Used in the title of Section 5 ("Graphs with Cut-Value
   at Most Two"), in its first sentence ("the minimum cut-value of every pair of vertices") and in the conclusion
   ("graphs with minimum cut-value at most two"). The introduction no longer uses it (now "c(x,y) <= 2 for every two
   distinct vertices"). Proposal: either add to Section 2 "We call $c(u,v)$ the \emph{cut-value} of $u$ and $v$." or
   replace the term everywhere: Section 5 title "Graphs with $c(x,y) \leq 2$ for All Pairs" or "Graphs in Which Every
   Two Vertices Are Separated by Two Edges".

4. [M] **"simple" is missing** (Section 2, "All graphs under consideration are undirected and finite, unless otherwise
   stated."). Theorem 4.5 uses deg(u,K) <= |K| - 1, false with parallel edges (and deg(u,S) counts neighbors, not
   edges, so deg(u) = deg(u,J) + deg(u,K) also needs simplicity); the cactus argument of Section 5 ("two distinct
   cycles share an edge", "three edge-disjoint paths") also assumes simple graphs. "unless otherwise stated": nothing
   is stated otherwise. Proposal: "All graphs are finite, simple and undirected."

5. [M] **Definition 2.5 does not fit Theorem 6.6.** Item 3 measures inputs uniformly: |I_opt(n)| / |I(n)| -> 1.
   Theorem 6.6 is about G(n,p) with p = p(n) >= alpha log n / n, which is not the uniform distribution (uniform over
   graphs on n vertices = G(n,1/2)). As stated, Theorem 6.6 does not follow from its proof. Proposal for item 3:
   "Let $\mu_n$ be a probability distribution on $I(n)$. The algorithm is average-case with respect to $(\mu_n)$ if
   $\lim_{n \to \infty} \mu_n\bigl(I_{A}^{\mathrm{opt}}(n)\bigr) = 1$."
   with the remark that the uniform distribution gives the original ratio, and in Theorem 6.6: "... with respect to
   the distribution of $G(n,p)$, for every choice of $u$ and $v$". Also `OPT(x)` is defined twice (sentence before
   the definition and item 2); one can go. A division by OPT(x) = 0 is excluded for Min Cut-Path (cp >= 1) but not in
   general.

6. [S] **Name "scheme"** (Definition 2.5). An approximation scheme is a family of algorithms indexed by epsilon; here
   one algorithm (min cut + shortest path, independent of epsilon) works for every epsilon, so Theorem 6.6 actually
   proves more: the ratio is 1 + 1/(beta_1 log log n). Proposal: name it "average $(1+\epsilon)$-approximation
   algorithm", or state Theorem 6.6 as "asymptotically optimal with high probability".

7. [S] **P(n) vs. path P** (Definition 2.5, item 1). P denotes a path everywhere else. Proposal: "its running time is
   bounded by a polynomial in $n$".

8. [C] **Missing 2-approximation** (after Lemma 2.4; new claim, author decides). Proposal:
   "\begin{corollary}\label{cor:two-approximation} Let $C$ be a minimum $u$--$v$ cut and $P$ a shortest $u$--$v$
   path. Then $|C \cup P| \leq 2\cp(u,v) - 1$. In particular, the union of a minimum cut and a shortest path is a
   polynomial-time $2$-approximation for \MinCutPath{}. \end{corollary}
   \begin{proof} By Lemma~\ref{lem:basic-bounds}, $|C \cup P| \leq c(u,v) + d(u,v) - 1 \leq 2\max\{c(u,v), d(u,v)\} - 1
   \leq 2\cp(u,v) - 1$. \end{proof}"
   (MT has it as Claim 8; research notes, open problem 3, call it "the trivial 2-approximation".)

9. [S] **Remark 4.6 cites "the proof of Lemma 2.4"** for the fact that C ∪ P has at most c + d - 1 edges for every
   minimum cut C and shortest path P. Proposal: put it in the statement of Lemma 2.4:
   "Moreover, for every minimum $u$--$v$ cut $C$ and every shortest $u$--$v$ path $P$, the set $C \cup P$ is a
   cut-path with $|C \cup P| \leq c(u,v) + d(u,v) - 1$."
   and in Remark 4.6 "By Lemma~\ref{lem:basic-bounds}, ...". The proof already proves it (no new argument).

10. [S] **Title** "Min Cut-Path Problem": names the object, not the result; "Min" is an abbreviation. Proposal:
    "The Minimum Cut-Path Problem: NP-Completeness and Polynomial Cases" (shorttitle "The Minimum Cut-Path Problem").

11. [S] **Keywords.** "average-case approximation" is the article's own term (see issue 6); "graph diameter" fine.
    Proposal: NP-completeness; edge cut; shortest path; graph diameter; random graphs; approximation algorithm
    (add "separating path" if DAM allows six or more).

12. [S] **E-mail** `5344553@upjs.sk` is a student-number address. Proposal: the name-based UPJŠ address (or a stable
    one) in `\ead{}`. The PDF also prints an empty "ORCID (s):" line in the first-page footnote: fill in
    `\orcidauthor{...}` or check how the class suppresses it.

13. [S] **Abstract, last sentence**: "for every fixed epsilon > 0" is weaker than what Theorem 6.6's proof gives
    (ratio 1 + 1/(beta_1 log log n)). Optional: "is within a factor $1 + O(1/\log\log n)$ of the optimum".

14. [S] **Problem box** (optimization version): repeats "Let G ... distinct vertices" and "is defined as follows:", and
    has a displayed equation in a table cell. Proposal: "\textbf{Output:} & A minimum cut-path $S^*$ between $u$ and
    $v$ and its size $\cp(u,v) = |S^*|$." (Kept unchanged here, to match the decision box of Section 3.)

15. [S] **Definition 2.1 now overlaps the new sentence** defining "u-v cut": item 1 could read "$C$ is a $u$--$v$ cut,
    and" with the bracket "(i.e., removing $C$ disconnects $u$ from $v$)" dropped. Not applied (deletion).

16. [S] **No example after the definitions.** Figure 1 is schematic. A small concrete graph with a minimum cut-path
    where cp(u,v) < c(u,v) + d(u,v) - 1 (path and cut sharing more than one edge) would show that Lemma 2.4's upper
    bound can be strict; with an example where cp = max{c,d} < c + d - 1 both bounds would be shown not improvable.
    New content; author decides (the MT counterexamples are parked by the author's decision of 2026-10-09).

17. [S] **Connectivity assumption.** Lemma 2.4 and Definition 2.3 rely on the global convention that u and v lie in one
    component (now made explicit after Definition 2.3). The proof of Theorem 3.6 restates it as an assumption "since
    otherwise the answer is negative"; that is consistent (an SSP instance may be disconnected), not an error.

18. [S] **deg(x,S)** is used only in the proof of Theorem 4.5; kept in Section 2 per the brief (Section 2 is meant to
    hold notions used at least twice). Could move to Section 4.

19. [S] **Integration note.** Introduction cites Theorem 6.1 (`thm:random-diameter-two`) as the reason the formula
    applies to dense random graphs; that theorem is a quoted result (Bollobás), not a contribution, which the sentence
    states as a fact, not as "we prove". Related work cites Bazgan et al. without theorem numbers (only the preprint
    was read).

20. [S] **Build note** (not fragment A): the project folder currently has no `diameter-two-structure.png`, and
    frag-C now includes `diameter-two-structure.pdf`, which is not there either; my test builds used the old PNG.
