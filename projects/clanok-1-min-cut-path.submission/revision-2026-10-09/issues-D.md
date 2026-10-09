# Issues in fragment D (Section 6, Section 7, Acknowledgments)

Tags: [M] possible mathematical error or gap, [C] change that would alter a claim, [D] proposed deletion or
restructuring, [S] other suggestion. None of these is applied in the text. Numbering of Section 6 as in changes-D.md.

Result of the step-by-step check: Lemma 6.4, Lemma 6.5, the ratio bound and the coupling argument of Theorem 6.6 are
correct, apart from items 1 and 7 (an over-broad sentence and the mismatch with Definition 2.5).

1. [M] **Proof of Thm 6.6, coupling sentence** ("the bounds of Theorem 6.2 and Lemma 6.5 ... remain valid for every
   p >= alpha log n / n"). Too broad: the upper bound c(u,v) <= beta_2 log n of Lemma 6.5 is not monotone and fails
   for larger p (for constant p, c(u,v) is about np). Only the two increasing properties are transferred, and only
   they are used. Proposed text:
   `Hence, by the standard coupling of the random graphs $G(n,p)$ for different edge probabilities (see, e.g.,~\cite{Frieze2016}), the diameter bound of Theorem~\ref{thm:random-diameter} and the lower bound of Lemma~\ref{lem:connectivity-bounds}, which are stated for $p = \alpha \log n / n$, remain valid for every $p \geq \alpha \log n / n$.`
   Optionally add: `Both properties are preserved by adding edges, so their probabilities do not decrease as $p$ grows.`

2. [D] **Unused upper bounds.** beta_2, the upper Chernoff tail (a > 1, a_2) in the proof of Lemma 6.4 and the upper
   half of Lemma 6.5 (c(u,v) <= beta_2 log n, with its proof paragraph and display) are never used: Thm 6.6 needs only
   c(u,v) >= beta_1 log n. Kept, as the owner requires preservation; they could be dropped or marked as not needed
   only on the owner's decision. They are correct.

3. [C] **Thm 6.2 and ChungLu2001 (derivation for the author to check).** Chung and Lu, Theorem 4 (authors' PDF,
   Section 4, p. 15; journal numbering not compared): if p >= c log n / n for a constant c, then almost surely
   diam G(n,p) <= ceil( log((33 c^2/400) n log n) / log(np) ) + 2 floor(1/c) + 2.
   With c = alpha > 1 and p = alpha log n / n: floor(1/alpha) = 0, np = alpha log n, log(np) = log log n + log alpha, so
   diam <= (log n + log log n + O(1)) / (log log n + log alpha) + 3 = log n / (log log n + log alpha) + O(1).
   Since log alpha > 0, log n / log log n - log n / (log log n + log alpha) = (log alpha) log n / (log log n (log log n + log alpha)) -> infinity,
   so diam <= log n / log log n for all large n, w.h.p. Thus Thm 6.2 holds as stated (the review's proposal to weaken
   it to O(log n / log log n) is not needed). Cited as `\cite{Bollobas2001,ChungLu2001}` without a theorem number;
   write `\cite[Theorem~4]{ChungLu2001}` only after comparing the journal numbering. The Bollobas2001 location for
   Thm 6.2 (and for Thm 6.1) is not verified; check it in the book or drop Bollobas2001 from Thm 6.2.

4. [C] **Thm 6.3 statement and source.** "lim P(G is k-edge-connected) = 1, where k = delta(G)": k is a random variable
   inside the probability, which is awkward. Proposed restatement (same claim):
   `Let $G(n, p)$ be an Erdős–Rényi random graph with $p = \alpha \log n / n$, where $\alpha > 1$. Then, with high probability, the edge connectivity of $G$ equals its minimum degree $\delta(G)$.`
   Source not verified first-hand: secondary sources name Bollobas and Thomason (1985) and Section 7.2 of Bollobas2001.
   Frieze2016 (2026 PDF) has Theorem 4.3 for k-connectivity with k fixed, which does not cover k = delta(G) growing
   like log n. Before submission, read the source and either cite it with a location or replace the citation.
   Proof of Lemma 6.5 would then read "with high probability, the edge connectivity of $G(n,p)$ equals $\delta(G)$ and ...".

5. [M] **Thm 6.1, parameter.** p = 1/alpha with alpha > 1 means "constant p in (0,1)"; alpha is then reused with a
   different meaning in p = alpha log n / n. Proposal: `Let $p \in (0,1)$ be a constant and let $G(n,p)$ be ...` and
   in the display `\diam(G(n,p)) = 2`. Also the dense-case sentences say "constant edge probability p" already.

6. [M] **Lemma 6.4: checked, correct.** h(a) = a log a - a + 1 -> 1 as a -> 0 (a log a -> 0), h decreases on (0,1)
   and increases to infinity on (1, infinity); alpha > 1 gives a_1, a_2 with alpha h(a_i) > 1. The Chernoff forms
   P(X <= a mu) <= exp(-mu h(a)) (0<a<1) and P(X >= a mu) <= exp(-mu h(a)) (a>1) are the standard ones
   (h(a) = phi(a-1), phi(x) = (1+x)log(1+x) - x). mu = (1-1/n) alpha log n, so exp(-mu h(a_i)) = n^{-(1-o(1)) alpha h(a_i)} = o(1/n),
   union bound o(1). alpha log n /2 <= mu <= alpha log n for n >= 2, so beta_1 = a_1 alpha/2, beta_2 = 2 a_2 alpha work
   (beta_2 = a_2 alpha would also do). Implicit: p <= 1, true for large n. The made-explicit steps are in changes-D.md.
   Lemma 6.5: correct; the middle inequality uses lambda(G) = min_{x != y} c(x,y) >= delta(G) (made explicit).

7. [M] **Definition 2.5 vs. G(n,p); how Thm 6.6 relies on it.** Definition 2.5 (Section 2, editor A) measures the good
   inputs by counting, |I_A^opt(n)| / |I(n)| -> 1, i.e. uniformly over all inputs of size n. Uniform counting over
   graphs on n vertices is G(n, 1/2), not G(n,p). The last sentence of the proof of Thm 6.6 ("on a set of inputs whose
   probability tends to one, i.e., it is an average (1+eps)-approximation scheme") silently reads the ratio as a
   probability under G(n,p). Also: an input x is (G,u,v); "size n" is not defined (vertices?), and x is never
   introduced in Section 6 (OPT(x) appears only here and in Def. 2.5). The proof does cover all pairs u != v at once,
   so the choice of (u,v) is harmless. Proposal for Def. 2.5 item 3 (editor A's place):
   `In addition, for a given probability distribution on $I(n)$, the algorithm is average-case in the sense that $\lim_{n\to\infty} \mathbb{P}\bigl(x \in I_A^{\mathrm{opt}}(n)\bigr) = 1$, where $x$ is a random input of size $n$.`
   and in Thm 6.6: `... is an average $(1+\epsilon)$-approximation scheme for the \MinCutPath{} problem on the inputs $(G(n,p), u, v)$, $u \neq v$.`
   Alternative that avoids Def. 2.5: item 8.

8. [C] **Thm 6.6, sharper statement (proposal only).** What the proof shows:
   `\begin{theorem}\label{thm:approximation-scheme} Let $\alpha > 1$ and $p \geq \alpha \log n / n$, and let $\beta_1$ be the constant of Lemma~\ref{lem:degree-bounds}. Then, with high probability, every pair of distinct vertices $u, v$ of $G(n,p)$ and every minimum $u$--$v$ cut $C$ and shortest $u$--$v$ path $P$ satisfy \[ |C \cup P| \leq \Bigl(1 + \frac{1}{\beta_1 \log \log n}\Bigr) \cp(u,v). \] In particular, for every $\epsilon > 0$, the algorithm that returns $C \cup P$ is an average $(1+\epsilon)$-approximation scheme.\end{theorem}`
   It is stronger than "for every epsilon" and makes the dependence on Def. 2.5 a one-line consequence.
   Also: the ratio display uses (c+d)/c although Lemma 2.4 gives |S| <= c+d-1; valid (looser). The step (c+d-1)/c was
   made explicit in the display; the sharper bound 1 + (d-1)/c is possible but not needed.

9. [S] **Dense case as a corollary** (gives contribution "Third" of the introduction a number). Proposed text to
   replace the two sentences after Thm 6.1 (keeping them as the proof):
   `\begin{corollary}\label{cor:dense} Let $p \in (0,1)$ be a constant. With high probability, every pair of distinct vertices $u, v$ of $G(n,p)$ satisfies $\cp(u,v) = c(u,v) + d(u,v) - 1$, and the union of a minimum $u$--$v$ cut and a shortest $u$--$v$ path is a minimum cut-path; it is computed in polynomial time.\end{corollary}`
   `\begin{proof} By Theorem~\ref{thm:random-diameter-two}, $G(n,p)$ has diameter two with high probability. The claim follows from Theorem~\ref{thm:diameter-two} and Remark~\ref{rem:algorithm}.\end{proof}`
   (If Thm 6.1 keeps p = 1/alpha, write "Let $\alpha > 1$ and $p = 1/\alpha$".) Note the original phrase "on almost all inputs" has the same Def. 2.5 issue as item 7.

10. [S] **Conclusion, fixed cp(u,v).** For a fixed k, deciding cp(u,v) <= k is polynomial by brute force: try all
    O(m^k) edge sets of size at most k and test each for containing a u--v path and a u--v cut (two BFS runs). So
    "a fixed value of cp(u,v)" is not where hardness can lie; the open question is fixed-parameter tractability in k.
    Proposed text (replacing the last paragraph):
    `Finally, for a fixed $k$, trying all sets of at most $k$ edges decides whether $\cp(u,v) \leq k$ in time $m^{O(k)}$. Is \MinCutPath{} fixed-parameter tractable with respect to $k$, i.e., solvable in time $f(k)\,\mathrm{poly}(n)$?`
    (A new but elementary claim; needs the owner's approval.) The applied wording ("the structure of the instances in
    which cp(u,v) equals a fixed constant") only clarifies the original and adds no claim.

11. [S] **Conclusion, class "diam or cut 2".** The author's material (MT Fig. 3.3; knowledge note, Section 3) has two
    counterexamples in which cp(u,v) != c + d - 1 in this class, so a reader may assume the formula is conjectured
    there. Proposed addition after the class sentence (no figure, per the owner's decision of 2026-10-09):
    `In this class, the formula $\cp(u,v) = c(u,v) + d(u,v) - 1$ fails in general, so a different algorithm is needed.`
    Requires the counterexamples to be stated or cited (the master's thesis is no longer cited); owner decides.

12. [S] **Missing open questions (proposal text, one sentence each; not applied).**
    - Approximation: `By Lemma~\ref{lem:basic-bounds}, the union of a minimum cut and a shortest path has fewer than $2\cp(u,v)$ edges. Is there a polynomial-time approximation with a factor smaller than two, or is the problem APX-hard?` (the first sentence follows from c + d - 1 <= 2 max{c,d} - 1 <= 2 cp - 1).
    - FPT: see item 10 (parameter cp(u,v)); also parameters d(u,v), c(u,v), treewidth.
    - Vertex version: `In the vertex version, the cut consists of vertices; its complexity is open.`
    - Weighted and directed graphs: `For edge weights or directed graphs, Lemma~\ref{lem:basic-bounds} and the results of Sections~4 and~5 need not hold; their complexity is open.` (the "need not hold" part must be checked first; otherwise only "are open").
    - Restricted classes for the reduction: is the problem NP-hard on graphs of bounded maximum degree, on bipartite graphs, on planar graphs (whether the reduction of Section 3 produces such graphs was not checked).
    - Diameter three: applied as one question sentence (changes-D.md, Citations), backed by Bazgan2019MostVital and LeLe2019MatchingCut; the knowledge note adds that the reduction of Section 3 produces graphs of large diameter (not added to the text).

13. [S] **Conclusion, planar duality sentence.** "every minimal edge cut corresponds to a cycle in the dual graph and
    vice versa" holds for connected plane graphs (bonds <-> cycles of the dual). Proposal: "In a connected plane
    graph, ...".

14. [S] **Coordination.** "With high probability" is defined in the opening paragraph of Section 6 (SPEC §3). If
    editor A defines it in Section 2, delete the sentence in Section 6. The Conclusion and the Introduction use the
    term after Section 6 / before it respectively; the Introduction (editor A) may need its own wording.

15. [S] **Lemma 6.5 has no name** while Lemma 6.4 is "Degree Bounds"; proposal `\begin{lemma}[Cut Bounds]`.

16. [S] **Conclusion par. 1** repeats the abstract (review §9); acceptable in a conclusion, kept.
