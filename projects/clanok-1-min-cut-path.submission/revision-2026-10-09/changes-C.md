# Changes in frag-C-4-5.tex (editor C, 2026-10-09)

Words (wc -w): 1606 before, about 2300 after. All labels, citations and references unchanged; integrated test build 16 pages (original fragments A, B, D), no errors.

## Language
- Sec. 4 intro: "it either is incident ... or not:" -> "it is either incident ... or not." (no colon lead-in to the lemma).
- Before Lemma 4.3: the argument moved into the proof; one sentence of intuition left ("the vertices that are not incident to the cut lie on at most one side of it").
- Before Lemma 4.4: "We also need the following general fact about ..." -> "The next lemma holds in every graph; it concerns the intersection of a cut and a path."
- Lemma 4.2: "Then, there exists" -> "Then there exists".
- Theorems 4.5 and 5.1: "the value of the minimum cut-path ... is [display]" -> "a minimum cut-path ... has [display] edges".
- Proof of 4.5: "Assume for contradiction that cp != c+1. Then cp = c" -> "Suppose, for a contradiction, that cp = c; by the bounds above, this is the only alternative to cp = c+1." Same opening "Suppose, for a contradiction," in the proof of 5.1.
- Proof of 4.5: "length at least 3" / "length at least three" -> "at least three edges" in both places.
- Proof of 4.5: "We now estimate the size of the cut C: ... where the estimate is obtained by counting ..." -> "Counting the edges of C according to their end-vertex in K, we estimate the size of the cut C:"; bullet items rewritten as full sentences (the first starts with "The terms"), content unchanged.
- Proof of 5.1: "This is a contradiction." -> "This contradicts the assumption that P contains a u--v cut."

## Exposition
- Lemma 4.3: the argument that stood before the lemma is now its proof, completed: a path from x in I to y in L contains an edge {a,b} of C with a in J, b in K; a != x and b != y because x, y are not incident to C; so the path has at least three edges, d(x,y) >= 3.
- Proof of 4.5: the explanation of the two "symmetries" split into two named exchanges (names of A_1, A_2 with I<->L, J<->K; u<->v with c, d, cp symmetric and P reversed), each used once.
- Sec. 5 cactus paragraph: the long "Indeed, ..." sentence split into four sentences; the two vertices are named x, y.

## Made explicit
- Proof of 4.5: why the cases are exhaustive (d in {1,2} by diameter two; c >= 1 by connectivity). Same in 5.1 (c in {1,2}, d >= 1).
- Proof of 4.5: why S is a cut: the cut contained in S has at least c = |S| edges, so it is all of S.
- Proof of 4.5: why the minimum cut C is the set of all edges between two sides with u, v on different sides (A = vertex set of the component of u in G \ C; the edges between A and V \ A lie in C and separate u from v; by minimality they are all of C). Checked: correct.
- Proof of 4.5: u is incident to an edge of C (first edge of P), next to the existing statement for v; u in K follows from A_2 = K.
- Proof of 4.5: deg(u,I) = 0 stated at its first appearance, with the reason (an edge from u in A_2 to I in A_1 would lie in C, but I is not incident to C); the term is kept.
- Proof of 4.5: every edge of C has exactly one end in K (C = edges between I u J and K).
- Proof of 4.5: the third vertex of P lies in K because the vertices of P alternate between A_2 and A_1; it differs from u because a path does not repeat vertices; its two counted edges are the second and third edges of P. Remaining vertices of K contribute one edge "by the definition of K".
- Proof of 4.5: deg(u,K) <= |K| - 1 "because u in K is not its own neighbor"; the equality uses V = I u J u K.
- Sec. 5 cactus paragraph: the two vertices: a path of the second cycle whose ends x != y lie on the first cycle and whose edges are not in it; x, y are joined by this path and the two x--y paths along the first cycle. (Chosen instead of "the ends of the shared path", which is correct only when the two cycles meet in a single path.)
- Proof of 5.1: why S is a path (|S| = d and S contains a u--v path of >= d edges).
- Proof of 5.1: a bridge on P would separate u from v (reason for "no edge of P is a bridge").
- Proof of 5.1: P enters Z_1 at u and leaves Z_t at v; consecutive cycles share the vertex where P passes from one to the next (every edge of P lies on one of the cycles), so the other arcs concatenate.

## Formatting
- Proofs of 4.5 and 5.1: the `enumerate` with bold "Case" items replaced by paragraphs `\emph{Case 1: ...}` / `\emph{Case 2: ...}` in both sections; the figure and the itemize no longer sit inside a list item; `\qedhere` removed from 4.5 (proof ends in text), kept in 5.1 (ends in a display).
- Proof of 4.5: the closing chain's two justifications are two sentences.
- Proof of 5.1: cycles renamed C_1..C_t -> Z_1..Z_t (local to this proof; avoids the clash with the cut C and the clauses C_k). Owner may veto (issues-C 10).
- Figure 10: `diameter-two-structure.png` (149 dpi bitmap, width 60 mm) replaced by the vector `diameter-two-structure.pdf` at natural size (59 x 54 mm), drawn in TikZ in the house style (standalone, STIX, red counted edges 1.2 pt). Source: `projects/clanok-1-min-cut-path.submission/figures/diameter-two-structure.tex`. Shows I, J, K (L empty), the I--J edges, u in K, v in J, red: all edges from u to J, the second and third edge of P at its third vertex, one edge at each further vertex of K; dashed: cut edges not counted. The PNG's kink in the path is drawn as P continuing u, y1, x, y2, k, v (y2--k dashed, k--v red), so the drawing agrees with P being contained in C. Caption unchanged (one line).
- PNG moved with `git mv` to `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-png-figures/`. NOTE for the integrator: `projects/clanok-1-min-cut-path/main.tex` still includes the .png until the fragments are merged.

## Citations
- None changed. GodsilRoyle2001 and Mehlhorn2017Certifying kept (issues-C 5, 6). No bib keys to add.
