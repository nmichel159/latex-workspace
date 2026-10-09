# Issues in frag-C-4-5.tex (editor C, 2026-10-09)

Tags: [M] possible mathematical error or gap, [C] change that would alter a claim, [D] deletion or restructuring, [S] other.
Checked step by step: Lemma 4.3 (proof now in the text), Lemma 4.4, the count in the proof of Theorem 4.5, Theorem 5.1.
The count is correct for simple graphs: |C| = sum over K of deg(k, J) >= deg(u,J) + 2 + (|K|-2) >= deg(u) + 1 > c(u,v).
The two parked counterexamples were re-checked by brute force (cut, distance and cp of every pair): both confirmed.

1. [D] **Lemma 4.2 (`lem:cut-decomposition`) is a definition.** I, J, K, L are defined by incidence to C; existence and uniqueness are immediate and the lemma has no proof. Kept as a lemma (owner's instruction). Proposal:
   ```latex
   \begin{definition}[Decomposition induced by a cut]
   \label{lem:cut-decomposition}
   Let $G = (V, E)$ be a graph, and let $C$ be the set of all edges between two sets $A_1$ and $A_2$ with $V = A_1 \cup A_2$ and $A_1 \cap A_2 = \emptyset$.
   Let $J$ and $K$ be the vertices of $A_1$ and $A_2$, respectively, that are incident to an edge of $C$, and let $I = A_1 \setminus J$ and $L = A_2 \setminus K$.
   \end{definition}
   ```
   Also: the items use `\forall`, `\exists`, `\nexists` in a sentence (math-writing.md §2); the proposal avoids them.

2. [M] **Lemma 4.4 (`lem:odd-intersection`) holds only for an edge boundary.** The statement says "a cut that divides G into two sets A_1 and A_2"; only the parenthesis of Lemma 4.2 says that this means "C is the set of all edges between A_1 and A_2". For a cut in the sense of Section 2 (an edge set whose removal separates u from v) the lemma is false: add to a minimum cut one edge of P lying inside a side. The proof uses the edge-boundary property ("every other edge of P stays on the same side"). The use in Theorem 4.5 is correct, because C is a minimum cut and hence an edge boundary (now made explicit in the proof). Proposal, second sentence of Lemma 4.4:
   ```latex
   Let $C$ be the set of all edges between two sets $A_1$ and $A_2$ with $V = A_1 \cup A_2$, $A_1 \cap A_2 = \emptyset$, $u \in A_1$ and $v \in A_2$, and let $P$ be a path that connects $u$ and $v$.
   ```
   Same wording for the hypothesis of Lemma 4.3 (there it is implied by the reference to Lemma 4.2).

3. [M] **Simple graphs.** Proof of Theorem 4.5: "deg(u,K) <= |K| - 1" and "deg(u) >= c(u,v) because the edges incident to u form a cut" use that deg counts both neighbors and edges, i.e., no parallel edges (Section 2 defines deg(x,S) as a number of neighbors and says only "undirected and finite"). With parallel edges, the number of edges at u can exceed deg(u), and the step deg(u) + 1 >= c(u,v) + 1 fails as written. Proposal: Section 2 says "simple" (editor A's issue), or the theorem says "Let $G = (V, E)$ be a simple graph of diameter two". Theorem 5.1 does not need it.

4. [S] **"connected" in Theorem 4.5 is redundant**: by Definition 4.1, d(x,y) <= 2 for all pairs, so G is connected. Kept (owner's instruction); the proof now uses it once (c(u,v) >= 1), which also follows from diameter two. Proposal: "Let $G = (V, E)$ be a graph of diameter two" (would be a change of wording of the statement only).

5. [C] **`GodsilRoyle2001` ("a class studied in algebraic graph theory") is loose**: a whole book cited for a side remark; `knowledge/literature/` has no reading note on it (the `.bib` status line verifies only the metadata). Kept. Proposal: either name what the book treats with a verified location, e.g. "... studied in algebraic graph theory, for instance as strongly regular graphs~\cite[Chapter~10]{GodsilRoyle2001}" (TODO(verify) the chapter in the printed book before use), or drop the clause (deletion: owner).

6. [C] **"cf.~\cite{Mehlhorn2017Certifying}" for the cactus structure is loose.** The paper is on certifying 3-edge-connectivity (Algorithmica 77(2), 2017; `.bib` status VERIFIED for metadata only); `knowledge/literature/` has no reading note on it, so nothing backs that it states "graphs with c(x,y) <= 2 for all pairs are cacti". Kept. Proposal: write a reading note for a source that states this characterization (TODO(verify): a textbook or a paper on cacti and 2-edge-connectivity) and cite it with a location, or drop "(cf. ...)" and rely on the article's own argument (issue 7).

7. [M] **Cactus paragraph: the argument proves less than the claim.** The claim: "any two [cycles or edges] share at most one vertex, an articulation point". The argument ("Indeed, ...") only excludes two cycles sharing an edge. Missing: two edge-disjoint cycles sharing two vertices x != y give four edge-disjoint x--y paths, so c(x,y) >= 4. Not made into a lemma, because a lemma would expose this gap. Proposal (after the sentence "Separating $x$ from $y$ would require ..."):
   ```latex
   Similarly, two edge-disjoint cycles cannot share two vertices $x \neq y$: they would contain four edge-disjoint $x$--$y$ paths.
   ```
   With that sentence the paragraph can become `\begin{lemma} Let $G$ be a connected graph with $c(x,y) \leq 2$ for all distinct $x, y \in V$. Then any two distinct cycles of $G$ share at most one vertex. \end{lemma}` with the paragraph as its proof. The proof of Theorem 5.1 uses only "every edge lies on at most one cycle" and the next item.

8. [M] **Theorem 5.1: P meets each cycle in one arc.** "P passes through a sequence of cycles Z_1, ..., Z_t, and in each cycle Z_i it follows one of the two arcs" assumes that P never leaves a cycle and returns to it later; "the other arc ... is edge-disjoint from P" uses the same. True in a cactus, not stated. Proposal (after the sentence about the sequence of cycles):
   ```latex
   The path $P$ does not return to a cycle $Z_i$ after leaving it: otherwise the part of $P$ from the vertex where it leaves $Z_i$ to the next vertex of $Z_i$ on $P$, together with an arc of $Z_i$, would be a cycle that shares an edge with $Z_i$.
   ```
   (Makes the step explicit; I did not apply it because it adds an argument, not a clause.)

9. [S] **Theorem 5.1: shortness of P is not used.** The proof shows that no u--v path P with c(u,v) = 2 in such a graph contains a u--v cut; |P| = d(u,v) is never used. Saying so would clarify the argument. Proposal (after "so the graph $G \setminus P$ contains no $u$--$v$ path."): "The argument below uses only that $P$ is a $u$--$v$ path." Owner decides (it is a remark, not a new result).

10. [S] **Notation C_1..C_t (applied, local).** In the proof of Theorem 5.1 the cycles were C_1, ..., C_t, clashing with the cut C (Sections 2, 4) and the clauses C_k (Section 3). Renamed to Z_1, ..., Z_t inside this proof only (logged in changes-C). Veto: revert the five occurrences.

11. [S] **The formula fails in the union class (parked counterexamples; proposal only).** Graphs in which every pair x, y has d(x,y) <= 2 or c(x,y) <= 2 (MT, Definition 37) contain pairs with cp(u,v) < c(u,v) + d(u,v) - 1. Both graphs have vertices t, a, v, u, b, s and edges ta, tv, au, ab, vb, us, sb; graph (b) also has av and ub. Checked by brute force: (a) c = 2, d = 3, cp = 3; (b) c = 3, d = 2, cp = 3; both satisfy the class condition. Drawings: `figures/counterexample-cut-two.tex`, `figures/counterexample-distance-two.tex`. Proposal, as the last paragraph of Section 5 (or in the conclusion):
   ```latex
   The formula does not extend to graphs in which every two vertices $x, y$ satisfy $d(x,y) \leq 2$ or $c(x,y) \leq 2$.
   In the graph with vertices $t, a, v, u, b, s$ and edges $ta$, $tv$, $au$, $ab$, $vb$, $us$, $sb$, the path $u, a, b, v$ is a shortest path whose removal separates $u$ from $v$, so $\cp(u,v) = 3 < c(u,v) + d(u,v) - 1 = 4$.
   ```
   The owner parked this on 2026-10-09; not applied.

12. [S] **Remark 4.6 and the sentence after the proof of 5.1** (review §6, §7): the remark is used in Sections 5 and 6 like a corollary; a corollary "If cp = c + d - 1, then the union of any minimum cut and any shortest path is a minimum cut-path; this holds in graphs of diameter two and in graphs with c(x,y) <= 2 for all pairs" would replace both. Restructuring: owner decides; not applied.

13. [S] **Lemma 4.3's intuition sentence** before the lemma ("the vertices that are not incident to the cut lie on at most one side of it") is new wording replacing the moved argument; delete it if the owner prefers the lemma to follow Lemma 4.2 directly.
