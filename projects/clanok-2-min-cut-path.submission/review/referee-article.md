# Referee report on projects/clanok-2-min-cut-path/main.tex, Sections 1 to 4

Scope, as changed by the coordinator: `sec:introduction`, `sec:preliminaries`, `sec:dt-diameter-three` and `sec:squares` only.
Sections 5 and 6 are being rewritten and get a separate review, so this report gives no verdict on them.
Findings are referred to by label, because main.tex is being edited in parallel.
Classes: G = gap or false statement in the mathematics; E = error that is easily repaired; M = minor.

Text judged: main.tex of 2026-10-31 20:06.
Sections 1 and 2 and `cor:dt-consequences` were re-read in that version.
Sections 3 and 4 were read in the earlier version; a line comparison shows that they differ from the draft files only in five lines (a label rename, the citation sentence in `thm:dt-hardness`, and the sentence in `cor:dt-consequences`(c) that no longer says "by the proof of").

## Overall verdict

Sections 2, 3 and 4 prove what they state.
No gap and no false statement was found in any proof of these sections: every step of `sec:dt-diameter-three` and `sec:squares` follows, the hypotheses of the cited lemmas are satisfied and the cross-references point to the right statements.
So the article proves, as written, that `PathInMinCut` and the question cp = c are NP-complete on graphs of diameter three for pairs at distance two, with the consequences of `cor:dt-consequences`, and that pairs of DC_2 with c <= 2 are solved in linear time and pairs with d = 1 by one minimum cut.
`thm:main` reduces correctly to these results and `thm:pa-open-case`, so it stands or falls with the rewritten Sections 5 and 6.
Three easily repaired errors remain, E1 and E2 in the summary text of Section 1 and E3 in the attribution of `lem:basic-bounds`, and none of them affects a proof.

Counts: G = 0, E = 3, M = 8.

## G: gaps or false statements in the mathematics

None.

## E: errors that are easily repaired

**E1. `sec:results`, item 2: the wording is false if read literally.**
The item says that cp = d if and only if "some square contains a path that lies on a shortest u-v path and separates two terminals of the square".
`thm:characterization` is stronger on both sides: the path joins an entering terminal x to a leaving terminal y, and it must separate the other two, alpha from beta.
Counterexample to the wording, in DC_2: vertices u, v, a, b, c, d, w, y, z and edges ua, ub, ay, yc, aw, wc, wb, wd, bz, zd, cv, dv.
Here c(u,v) = 2, d(u,v) = 4 and cp(u,v) = 5.
The only minimum cuts are {ua, ub} and {cv, dv}, so the middle square is {a, b, c, d, w, y, z} with entering terminals a, b and leaving terminals c, d.
The path a, w, c lies on the shortest path u, a, w, c, v, and in the square without its edges the components are {a, y, c} and {w, b, d, z}, so it separates the terminals a and b.
No shortest path is separating, because b and d stay connected for this path and the other five shortest paths fail in the same way.
Checked by brute force as well.
Repair: "... if and only if some square contains a path from an entering to a leaving terminal that lies on a shortest u-v path and separates the other entering terminal from the other leaving terminal".

**E2. `sec:results`, item 3, and the abstract: pairs with d = 1 and c >= 3 are forgotten.**
Item 3 says that the pairs of DC_2 that item 2 leaves have d = 2 and c >= 3, and the abstract says "The remaining pairs have d(u,v) = 2 and c(u,v) >= 3".
Item 2 treats c <= 2 only, so it also leaves adjacent pairs with c >= 3, for example any two vertices of K_4.
The sentence "Items 2 and 3 together give our main result" inherits this.
The proof of `thm:main` and the text after `prop:easy-pairs` are correct.
Repair: in item 3, "A pair with d(u,v) = 1 is solved by one minimum cut (`prop:easy-pairs`(i), `cor:class-pairs`), and the other pairs of DC_2 that item 2 leaves have d = 2 and c >= 3"; in the abstract, "The remaining pairs, apart from adjacent ones, have ...".

**E3. `lem:basic-bounds`: the locator does not cover two of the three clauses.**
The lemma is attributed to [Lemma 2.3 and Corollary 3.12] of article 1 and now has no proof here.
The bounds are the statement of Lemma 2.3.
The clause on the union of a minimum cut and a shortest path is only in the proof of Lemma 2.3.
The equivalence "cp = d if and only if a separating shortest path exists" is not the statement of Corollary 3.12, which is the NP-completeness of the question cp = d; it is the first sentence of the proof of that corollary, which refers to the proof of Theorem 3.11.
The facts are correct and are there, so only the locator is wrong.
The clauses are used in `cor:dt-consequences`(c), `thm:characterization` and the opening of `sec:separating`.
Repair, in order of preference: state the two clauses in Lemma 2.3 of article 1 (this shifts no number), or cite "[Lemma 2.3 and its proof, and the proof of Theorem 3.11]", or keep the three-line proof here.

## M: minor points

**M1. `sec:structure`, the sentence "Throughout this section and `sec:separating`, we assume c(u,v) = 2".**
It is a leftover from the time these were sections: "this section" is now `sec:squares`, which contains `sec:separating` and also `sec:algorithm`, where c = 1 is treated too.
Repair: "Throughout `sec:structure` and `sec:separating`".

**M2. `sec:techniques`, paragraph 2: "the two terminals that R does not use".**
The vertices alpha_i, beta_i are the end of the other entering edge and of the other leaving edge; alpha_1 = u lies on R, and R can pass through alpha_i inside the square.
Repair: "the two terminals at the edges of the square that R does not use".

**M3. Abstract: "separates two prescribed vertices of the subgraph".**
This is not false, but the vertices are determined by the ends of the path, as E1 shows.
Repair: "joins two of its four terminals and separates the other two".

**M4. `Michel2026MinCutPath` is a bibliography entry with the note "Manuscript".**
It now carries `lem:basic-bounds`, half of `lem:minimum-cuts` and five further cited numbers.
Before submission it needs a public version (arXiv or journal status), and the numbers must be rechecked against that version.

**M5. `sec:thesis`: "every statement has a complete proof"; `sec:structure`: "to keep the paper self-contained".**
Both were written before the results of article 1 were delegated.
Repair: "every statement on the decomposition has a complete proof"; the second sentence can stay if it is read as applying to the listed lemmas, or become "We include their proofs".

**M6. `rem:dt-bounded-cut-value`: "the question" has no antecedent in the remark.**
Repair: "whether cp(u,v) = c(u,v) is decided in polynomial time for pairs with c(u,v) <= k".

**M7. `rem:bridges` is never referenced.**
Its content is proved again in Section 5 as `lem:zz-bridges` in the current text.
Repair: when Section 5 is final, delete the remark, or keep one statement and cite it.

**M8. Notation inside Sections 1 to 4.**
Each use is local and I found no real ambiguity, but these letters are overloaded:

- s and t: vertices of G_a, the tail in the proof of `lem:orientation`(iii), the count s(A) in `lem:dt-cuts`, terminals in `thm:structure`(v);
- c_i and d_i are terminals next to the functions c(,) and d(,), in `alg:cut-two` in the same lines;
- H: subgraph in `sec:cut-paths`, H_tau in `lem:dt-cut-graphs`, the flow digraph in the proof of `thm:linear-time`;
- m: m(A,B) in `lem:uncrossing`, the number of clauses, the index in `def:decomposition`, and m_i in the running time;
- x_i: variables in Section 3, entry vertices in `sec:separating`; L: number of literals, and links L_m; p: number of variables, paths p_j, and the path p of `thm:characterization`.

Repair: at least rename the tail in `lem:orientation` and s(A), and rename the flow digraph; decide on H, Q, D, M and m after the rewrite, because Section 5 uses them too.

## Dependencies on the rewrite (not findings)

These places describe the old Sections 5 and 6 and must be rechecked after the rewrite: the last three sentences of the abstract; `sec:results` item 3 (the bound n^71 and `thm:pa-open-case`); `sec:techniques` paragraph 3 (`thm:zz-reduction`, `thm:pa-formulas`, A_P, B_P, 71); `sec:thesis` (last sentence); the proof of `thm:main`; the sentences after `prop:easy-pairs`.

## What was checked

**Section 3.** The vertex and edge counts; `lem:dt-forcing`; both parts of `lem:dt-cuts`; both directions of `lem:dt-cut-graphs`, including the anchors that keep false occurrence vertices away from the rungs and the set W for an unsatisfied clause; membership in NP; the distances and d(f,f') = 3 in `thm:dt-hardness`; all parts of `cor:dt-consequences`; `rem:dt-not-in-dc` (c_0 >= 4). `fig:dt-construction` agrees with the definition.

**Section 4.** Line by line: `lem:orientation`, `lem:pieces`, `lem:degrees`, `thm:structure` (i) to (v), `lem:criterion`, `thm:characterization`, `cor:two-edges`, `lem:residual`, `alg:cut-two`, `thm:linear-time` (flow decomposition, correctness, O(|V|+|E|)), `cor:class-pairs`, `rem:coarser`.

**Examples.** Brute force confirms the values stated for G_a, G_b, G_a^+, G_1, G_1' and G_1''; the minimum cuts and terminals of `ex:decomposition` and `ex:worked` were checked by hand. All figures agree with the text.

**Computation.** An independent script builds the decomposition from the definition (F as the union of all minimum cuts) and compares with brute-force cp on 64732 random chain graphs with c = 2 (64652 of them in DC_2; 2359 with cp = d). It tested well-definedness of tails, the degrees of squares and links, `thm:structure`(v), `prop:easy-pairs`(iii), `thm:characterization`, and the loop of `alg:cut-two`, including that nothing is recorded in DC_2. No assertion failed. The script does not touch the linear running time.

**Theorem `thm:main`.** The cases are complete: d = 1 by `cor:class-pairs`; c <= 2 by `thm:linear-time` (c = 1 by `prop:easy-pairs`(ii)); d >= 3 forces c <= 2; what remains is d = 2 and c >= 3.

## Citations of article 1 (projects/clanok-1-min-cut-path/main.tex)

The numbers were read from outputs/clanok-1-min-cut-path/main.aux, which was built after the last edit of that main.tex (2026-10-10).

| Cited in article 3 | Article 1 | Match |
|---|---|---|
| Lemma 2.3 (`sec:introduction`, `lem:basic-bounds`) | Basic Bounds, `lem:basic-bounds` | yes, for the bounds; see E3 for the other clauses |
| Corollary 3.12 (`lem:basic-bounds`) | `cor:lower-bound-attained` | only through its proof; see E3 |
| Theorem 3.10 (`sec:introduction`) | `thm:ssp-np-complete` | yes; the definition of a separating shortest path is the same |
| Lemma 5.4 (`lem:minimum-cuts`) | `lem:odd-intersection` | yes; the same hypotheses |
| Theorem 5.5 (`sec:introduction`, `sec:cut-paths`, `sec:class`) | `thm:diameter-two` | yes |
| Lemma 6.1 (`sec:class`) | `lem:cactus` | yes; article 1 omits connectedness, which article 3 adds in its definition of a cactus |
| Theorem 6.2 (`sec:introduction`, `sec:class`) | `thm:cut-two` | yes |
| Theorem 8.4 (`rem:dt-bounded-cut-value`) | `thm:fpt` | yes |

The first part of `lem:minimum-cuts` (exactly two components, and A unique) rightly stays proved here: article 1 has only the form C = delta(A), inside the proof of its Theorem 5.5.
The thesis locators (Definitions 37 to 40, Theorems 20, 22 and 23, Figure 3.3 with two graphs, Transformations A, B and C) agree with knowledge/sources/diplomova-praca-2025-min-cut-path.txt.
The diameter claims on Matching Cut and SP-MVE in `sec:related-work` agree with the reading notes; the other related-work statements were not checked against their sources.

## Outside the scope

The Declarations still hold the placeholders "Funding: Statement", "Conflict of interest/Competing interests: Statement" and "Author contribution: Statement".
My earlier pass over the previous text of Sections 5 and 6 is superseded by the rewrite and is not reported as a verdict.
