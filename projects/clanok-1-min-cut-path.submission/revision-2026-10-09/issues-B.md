# Issues in Section 3 (frag-B-3.tex), not applied

Numbering in the revised build: Definitions 3.1-3.4, Lemmas 3.5 (`lem:chain-paths`), 3.6 (`lem:synchronization`),
3.7 (`lem:clause-threads`), 3.8 (`lem:separating`), Theorem 3.9 (`thm:ssp-np-complete`), Theorem 3.10 (`thm:mcp-np-complete`).

## Result of the mathematical check

I checked every step of Section 3. The reduction is correct: Lemma 3.5 (shortest paths), both synchronization
arguments (all four sign combinations of each pair), the clause-thread criterion, direction (a), direction (b), the
counts (2n+3m links, 2n+7m threads), Lambda = O(n+m), O((n+m)^2) edges, both NP-membership arguments and the
SSP -> Min Cut-Path reduction. The only real gap was the completeness of the separation argument in (b) (a walk
"starting at u" with cases whose exhaustiveness and repetition along clause threads were left to the reader), plus
the unstated dead-end degree argument; both are closed in Lemma 3.8 by justification only (see changes-B.md, "Made
explicit"). Facts checked for the closure: for tau(x_i)=true the threads [(I+),(T-)], [(I-),(T+)], [(I+),(L-),(T+)],
[(I-),(L+),(T-)] give exactly the edges T_i°v; uI_i°; none; uI_i° and T_i°v of Gamma; for false the roles swap.

## Items

1. [S] **n, m clash.** Section 2 sets n = |V|, m = |E| globally; Section 3 (l. "Throughout this section ...") reuses
   them for variables and clauses, and "Lambda = O(n+m)", "O((n+m)^2) edges" read like bounds in the graph size.
   Proposal (editor A decides on Section 2): keep the override and write in the running-time paragraph
   "polynomial in $n+m$, the number of variables and clauses". Alternative: variables $N$, clauses $M$ in Section 3.

2. [S] **C / C_k / \mathcal{C}.** C is a cut in Definition 2.1 and Lemma 2.4; C_k is a clause and \mathcal{C} the
   clause set here. Proposal: clauses $D_1,\dots,D_m$, set $\mathcal{D}$ (Section 3 and Algorithm 1 only), or keep C
   for clauses and note nothing (cuts do not appear in 3.1).

3. [S] **I_i, T_i, L_{j,k}, K_i vs I, J, K, L of Section 4.** Section 4 uses I, J, K, L for the parts of the
   decomposition (Lemma 4.2). The symbols are local to their sections, so no formula is ambiguous, but a reader of
   Section 4 sees the same letters with another meaning. Proposal: keep; or rename the links of Section 3 to
   $A_i$ (initialization), $Z_i$ (terminal), $B_{j,k}$ (literal).

4. [S] **Index i in Thread.** Thread(u,v,[(K_1,sigma_1),...,(K_t,sigma_t)]) and the hit criterion "for some $i$,
   the path $P$ traverses the path of $K_i$ with the sign $\sigma_i$" reuse i, the variable index. Proposal:
   index $r$: "$(K_1,\sigma_1),\dots,(K_t,\sigma_t)$ ... for some $r \in \{1,\dots,t\}$, the path of $K_r$ with the
   sign $\sigma_r$" (also in the Thread bullet: "$\sigma_r \in \{+,-\}$ ... through $K_r$").

5. [S] **k: threshold vs clause index.** The Min Cut-Path decision box and Theorem 3.10 use k for the threshold;
   k indexes clauses in 3.1. Proposal: threshold $b$: "and an integer $b$" / "$|F| \le b$" / "$b := d_G(u,v)$".

6. [S] **F vs S.** The decision box and Theorem 3.10 call a cut-path F; Definition 2.1 and the rest of the paper
   use S. Proposal: replace F by S in the box and in the proof of Theorem 3.10 (6 occurrences).

7. [M] **Definition 3.1, item 2 is vacuous.** Any two distinct vertices of a cycle split it into two internally
   disjoint paths. Proposal (ready to paste):
   `A \emph{$(p,q)$-chain link} is a cycle $L \subseteq G$ through $p$ and $q$ whose two $p$--$q$ paths have equal length.`
   (keeps items 1 and 3; drops item 2; this is a restatement, so only with the owner's approval).

8. [S] **Definition 3.1, last sentence** ("When a chain link is used inside a chain, its boundary vertices are
   exactly p and q ...") speaks of a chain and its single edges before Definition 3.2 and is a usage note, not part
   of the definition. Proposal: move it after Definition 3.2 as: "In a chain, the single edges $H_i$ and $H_{i+1}$
   are attached to the chain link $L_i$ exactly at its vertices $q_i$ and $p_{i+1}$."

9. [S] **Definition 3.2, last sentence** ("Every u-v path in a chain traverses all single edges and, in each
   chain link, either its positive or its negative path") is a statement inside a definition, without a reason.
   Proposal: move it after the definition with its reason: "By item 4, every single edge $H_i$ is a bridge of the
   chain and $L_i$ meets the rest of the chain only in $q_i$ and $p_{i+1}$; hence every $u$--$v$ path in a chain
   traverses all single edges and, in each chain link, either its positive or its negative path."

10. [M] **Definition 3.3, item 2 is circular.** "P is edge-disjoint from every other thread" defines a thread
    through other threads. It is a property of a family. Proposal:
    `A \emph{family of threads} is a set of $u$--$v$ paths in $G$ such that each of them shares at most one edge with each chain link and no single edge of the chain, and any two of them are edge-disjoint and share only the vertices $u$ and $v$; its members are called \emph{threads}.`

11. [M] **Definitions 3.3 and 3.4 disagree on what a thread is.** 3.3: a finished u-v path; 3.4: "a thread not
    yet passing through L" that is "extended" step by step. In addition, Definition 3.4 is applied to "a chain link",
    but after one threading the link's two paths no longer have equal length (Definition 3.1, item 3) until
    Calibrate; and the step "Extend P" does not say which connecting paths are attached to z_1 and z_2 (needed for
    "the two connecting paths that end at this crossing edge" in Lemma 3.8). Proposal: describe the final object
    statically after Algorithm 1: "The thread created by $\textsc{Thread}(u,v,[(K_1,\sigma_1),\dots,(K_t,\sigma_t)])$
    consists of its $t$ crossing edges $z_1^{r}z_2^{r}$, $r=1,\dots,t$, and of $t+1$ connecting paths, from $u$ to
    $z_1^{1}$, from $z_2^{r}$ to $z_1^{r+1}$ for $r<t$, and from $z_2^{t}$ to $v$"; and in Definition 3.4 replace
    "chain link" by "cycle obtained from a chain link by threading" (or note that equal lengths are restored by
    Calibrate).

12. [S] **L_{j,k,i} vs L_{j,k}.** i is determined by (j,k). Proposal: write $L_{j,k}$ everywhere (list of link
    types, Figures 5 and 8 captions, Algorithm 1 lines 6, 13-14, Lemmas 3.6-3.8) and "where $x_i$ is the variable
    of the $j$-th literal of $C_k$" where i is needed. Figures 5 and 8 show the label $L_{j,k,i}$, so they would
    need redrawing; otherwise keep both and leave as is.

13. [M] **Calibrate vs running time: "at least Lambda" vs "has Lambda edges"; initial length unspecified.**
    Thread does not state the initial length of a connecting path; Calibrate subdivides "until it has at least
    Lambda edges", the running-time paragraph "until it has Lambda edges". Both are consistent if connecting paths
    are created with at most Lambda edges. Proposal: in the Thread bullet "... by $t+1$ new, internally
    vertex-disjoint paths of one edge each" and in Calibrate "until it has exactly $\Lambda$ edges"
    (Lemma 3.5 needs only "at least").

14. [S] **Rephrased sentence after the SSP box.** The new text "a solution is a single shortest u-v path, that
    is, a cut-path of size d(u,v) (see the proof of Theorem 3.10)" uses a fact proved only in 3.2 (forward
    reference). If the owner prefers no forward reference, revert to the original sentence
    "Unlike \MinCutPath, \SSP{} is not an optimization problem, which makes the reduction from \ThreeSAT{} more direct."

15. [C] **Possible strengthening: maximum degree three.** Checked: in G every vertex other than u and v has
    degree at most three (chain-link ends p, q: one single edge and two cycle edges; end-vertices of a crossing
    edge: two chain-link edges and one connecting-path edge; all other vertices: degree two). New claim; proposal
    only, as a sentence after Theorem 3.9:
    `The proof shows more: \SSP{} remains NP-complete for graphs in which every vertex other than $u$ and $v$ has degree at most three.`
    (Theorem 3.10 then gives the same for Min Cut-Path.)

16. [C] **SSP asks whether cp(u,v) = d(u,v).** By Lemma 2.4, cp(u,v) >= d(u,v); the proof of Theorem 3.10 shows
    that a cut-path of size d(u,v) is exactly a separating shortest path. Hence SSP is the question
    "cp(u,v) = d(u,v)?", and it is NP-complete to decide whether the lower bound d(u,v) of Lemma 2.4 is attained.
    New claim; proposal only, as a corollary after Theorem 3.10:
    `\begin{corollary} It is NP-complete to decide, given a graph $G$ and vertices $u,v$, whether $\cp(u,v) = d(u,v)$. \end{corollary}`
    `\begin{proof} By Lemma~\ref{lem:basic-bounds}, $\cp(u,v) \ge d(u,v)$, and by the proof of Theorem~\ref{thm:mcp-np-complete}, $\cp(u,v) = d(u,v)$ holds if and only if $G$ contains a separating shortest $u$--$v$ path. Theorem~\ref{thm:ssp-np-complete} completes the proof. \end{proof}`

17. [S] **Theorem 3.10, "We may assume ..."** repeats the global assumption of Section 2 (u and v lie in one
    component). Also, a many-one reduction must output an instance in every case. Proposal: replace by
    "If $u$ and $v$ lie in different components, the answer is negative, and the reduction outputs a fixed negative instance (for example, $G$ with $k := 0$)." or delete, relying on Section 2.

18. [S] **Theorem 3.10, "We define $G' := G$"** introduces a second name for the same graph. Proposal: delete
    G' and write "We ask whether $G$ admits a cut-path of size at most $k$" (also "suppose that $G$ has a cut-path").

19. [S] **Theorem 3.10, "All conditions can be tested in polynomial time."** repeats the first sentence of the
    paragraph. Proposal: delete.

20. [S] **Theorem 3.10, Conclusion, "(by polynomial verification)"** repeats the Membership paragraph. Proposal:
    "Since \MinCutPath{} is in NP, it is NP-complete."

21. [S] **Introductory sentences of 3.1.1** ("The reduction ... is built from gadgets and basic operations on them.
    The construction consists of two parts: ...") are an announcement plus a two-item list (review 4.2). Proposal:
    "The construction has two parts, the \emph{chain} (base structure) and the \emph{threads} threaded through it (Figure~\ref{fig:chain-threads})."

22. [S] **Chain link described twice.** The sentence before Definition 3.1 says what the definition says
    (review 4.2). Proposal: keep only the definition, or keep the sentence as intuition (current state).

23. [S] **Counts in the list of link types.** "The total number of ... chain links is n / n / 3m" three times and the
    sum after the list. Proposal: delete the three sentences and keep "In total, the construction contains $2n+3m$
    chain links." (also writes 2n+3m in the order used in Algorithm 1).

24. [S] **Thread-type list vs lemmas.** The sentences "Threads of this type force every separating shortest path
    ..." and "It encodes the clause ..." state results before their proofs; I added pointers to Lemmas 3.5-3.7.
    Proposal: replace them by what the threads do structurally (e.g., "This thread is hit by a chain path unless the
    path uses the negative path of $I_i$ and the positive path of $T_i$"), keeping the lemma pointers.

25. [S] **Section 3.2 as a corollary.** Review 5: with item 16, Theorem 3.10 could be stated as a corollary with a
    three-line proof. Restructuring; proposal only.

26. [S] **Length.** With only fragment B revised (others original), the document grows from 15 to 17 pages: about
    one page from the auxiliary multigraph argument and the lemma statements, and half a page because Figures 7-9
    now stand together after the list. Moving Figures 7-9 back into the list items would save a few lines.
