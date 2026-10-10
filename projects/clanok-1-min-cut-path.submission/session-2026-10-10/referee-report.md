# Referee report: "Min Cut-Path Problem" (article 1), for Discrete Applied Mathematics

Independent, adversarial review written on 2026-10-10. Read-only: nothing but this file was written.
Status of this file: complete (Parts 1-4), finished 09:38.

## Version reviewed, and a warning about numbering

- The manuscript changed while I was reading it. I first read `main.tex` of 09:11 (1151 lines, PDF 17 pages); at
  09:25:00 the file was replaced (1196 lines, PDF 18 pages, built 09:25:02). **This report is about the 09:25
  version.** A copy of exactly what I reviewed is in `tmp/referee-2026-10-10/main-snapshot.tex` and
  `main-snapshot.pdf`; all line numbers (`L...`) refer to it.
- Statement numbers are those of the 18-page PDF. They differ from the 17-page PDF: old Definition 2.4 = new 2.5
  (new Corollary 2.4 before it); new Definition 3.5 (chain path, hitting, consistency); old Lemmas 3.5-3.8 = new
  Lemmas 3.6-3.9; old Theorems 3.9, 3.10 = new Theorems 3.10, 3.11 (new Corollary 3.12 after them); old Lemma 4.2 =
  new Definition 4.2. Sections 5 and 6 keep their numbers.
- What "checked" means below: I re-derived the argument by hand from the text. I ran no computation and no build.
  I did not open any cited source; where a finding depends on a source I say what it rests on.
- Severity: BLOCKER = wrong or unproved as written; SHOULD FIX = a referee will insist; MINOR = polish.

**Result of Part 1 in one line: no BLOCKER in the 09:25 version; every statement of Sections 2-6 is proved by an
argument that I could follow to the end, with six places (M6, M7, M8, M9, M12, M14) where the text asserts what it
should justify or cites what it should adapt.** The one BLOCKER of the 09:11 version (the theorem on random graphs
claimed a property defined by counting inputs, its proof gave a statement about `G(n,p)`) is repaired by the new
Definition 2.5, item 3, and the new statement of Theorem 6.6.

---

## Part 1. Mathematics, statement by statement

### Section 2

**M1 (MINOR). L194-199, Preliminaries.** `d` and `c` are defined only for the distinguished pair `u, v`, but
are used for arbitrary pairs (`d(x,y)` in Definition 4.1 L832, `c(x,y)` in Lemma 5.1 L981, Theorem 5.2 L997,
Lemma 6.5 L1129), and `d` has no value when no path exists, which Definition 4.1 needs ("diameter two implies
connected", L900).
Fix, replacing L195-197:
`For two vertices $x, y$ of $G$, the distance $d(x, y)$ is the length of a shortest $x$--$y$ path, and $d(x, y) = \infty$ if there is none. For distinct $x, y$, a set of edges whose removal leaves no $x$--$y$ path is a \emph{cut separating $x$ and $y$}, or an \emph{$x$--$y$ cut}; $c(x, y)$ denotes the minimum size of an $x$--$y$ cut, and we call it the \emph{cut-value} of $x$ and $y$.`

**M2 (MINOR). L204-212, Definition 2.1; L202.** The set `C` in the definition is superfluous: with the paper's
notion of a cut (any edge set whose removal separates), every superset of a cut is a cut, so `S` is a cut-path
iff `S` contains a `u`-`v` path and `G \ S` has no `u`-`v` path. The paper uses exactly this equivalence without
stating it: L802 ("`S` contains a cut, [hence] `G \ P` contains no path"), L807 (the NP certificate is checked by
testing `G \ S`), L1020. Also `G \ F` is defined for paths only (L202) but used for `G \ S` (L807) and `G \ C` (L920).
Fix, one sentence after L212:
`Every superset of a $u$--$v$ cut is a $u$--$v$ cut; hence a set $S \subseteq E$ is a cut-path if and only if $S$ contains a $u$--$v$ path and $G \setminus S$ contains no $u$--$v$ path.`
and L202: `For a set $F \subseteq E$, we denote by $G \setminus F$ the graph obtained from $G$ by removing all edges of $F$.`

**Definition 2.2, L223-234; Lemma 2.3, L248-265.** Checked, no finding.

**M3 (MINOR). L267-280, Corollary 2.4.** Correct, but weaker than what its own one-line proof gives, and the
stronger form is re-derived in the proof of Theorem 6.6 (L1158-1159).
Fix: state `$|C \cup P| \leq \cp(u, v) + \min\{c(u, v), d(u, v)\} - 1 \leq 2\cp(u, v) - 1$` with the proof
`$|C \cup P| \leq c(u,v) + d(u,v) - 1 = \max\{c(u,v), d(u,v)\} + \min\{c(u,v), d(u,v)\} - 1$, and $\min\{c(u,v), d(u,v)\} \leq \max\{c(u,v), d(u,v)\} \leq \cp(u,v)$ by Lemma~\ref{lem:basic-bounds}.`
Theorem 6.6 then needs only "`d(u,v) = o(c(u,v))` for all pairs".

**M4 (MINOR). L286-303, Definition 2.5.** After today's change the definition and Theorem 6.6 agree (checked:
items 1-3 follow from the first claim of Theorem 6.6 with `I^opt(n)` = the inputs on which the ratio is below
`1+eps`). What remains: (a) item 2 alone holds for every algorithm (take the empty set); only item 3 has content,
so the three items say `P(ALG(X) < (1+eps) OPT(X)) -> 1` and nothing else; (b) "a given probability distribution on
`I(n)`" is one distribution for each `n`, and it is part of the notion, not of the algorithm; (c) `OPT(X)` is
undefined for an input whose `u, v` lie in different components (no cut-path exists), so `I(n)` must be the inputs
that satisfy L199; (d) the maximization branch is never used.
Fix, replacing items 2 and 3 by one item (the definition stays):
`\item For every $n$, the input $X$ is drawn from a given probability distribution on $\mathcal{I}(n)$, and the value $\ALG(X)$ of the solution computed by $\ALG$ satisfies $\lim_{n \to \infty} \mathbb{P}\bigl(\ALG(X) < (1+\epsilon)\,\OPT(X)\bigr) = 1$ for a minimization problem (and $\OPT(X) < (1+\epsilon)\,\ALG(X)$ for a maximization problem).`

### Section 3

**M5 (MINOR). L312, L324, the 3-SAT box.** L324 pads short clauses by repeating a literal, so clauses with
repeated literals are inputs; the box says only "exactly three literals". I checked that nothing in Lemmas 3.7-3.9
needs distinct literals or distinct variables in a clause (`L_{1,k}, L_{2,k}, L_{3,k}` are three different chain
links also when two literals coincide).
Fix, L312: `is a disjunction of exactly three literals, not necessarily distinct, and each literal is either a variable $x_i$ or its negation $\neg x_i$.`

**Definition 3.1, L366-375; Definition 3.2, L386-400.** Checked. L402 ("every `u`-`v` path in a chain traverses all
single edges and one path of each link") is stated without a reason and is used at L591 and L610; one clause
suffices: `because every $H_i$ is a bridge of the chain and $L_i$ meets the rest of the chain only in $q_i$ and $p_{i+1}$`.

**M6 (SHOULD FIX). L437-447, Definition 3.3 (Thread).** Since today the definition is no longer circular, but it
does not define the objects that are called threads afterwards. Items 1-2 are satisfied by `u`-`v` paths that no
call of `Thread` creates. Example, for choices that Definition 3.4 leaves open: two threads with the same first
link are threaded there at adjacent free edges, the first arrives and the second leaves at the two adjacent
end-vertices; the path that follows the first thread from `u` to that link, uses the chain edge between the two
crossing edges and continues along the second thread to `v` shares one edge with each link it meets and no single
edge. For such paths L447 ("any two
threads are edge-disjoint") is false, and "the construction creates `2n+7m` threads" (L758), "hits all
synchronization threads" (Lemma 3.7) and Table 1 mean the created paths only. The proofs never use Definition 3.3;
they use properties of the procedure `Thread`.
Fix, replacing L447:
`Algorithm~\ref{alg:reduction} creates its threads by the procedure \textsc{Thread} described below; from now on, a \emph{thread} is one of these paths. Any two of them are edge-disjoint and share only the vertices $u$ and $v$.`

**M7 (SHOULD FIX). L449-460 (Definition 3.4), L513-520 (procedures), L576-580: the construction is not shown to be
well defined.** I checked each point; all hold, none is in the text.
(a) Step 1 of Definition 3.4 must find a free edge on the path with the requested sign. It always can: each path of a
4-cycle starts with two free edges, and a threading turns one free edge into two free edges and a crossing edge.
(b) From the first threading until `Calibrate`, the two paths of a link differ in length, so the cycle is not a chain
link (Definition 3.1, item 2) and the chain is not a chain (Definition 3.2), although Definition 3.4 and `Thread`
are applied to "a chain link in a `u`-`v` chain"; L579 says only afterwards that they "are again chain links".
(c) Three facts are used later with no reason given (first at L669): the end-vertices of a crossing edge are new
vertices, so distinct crossing edges share no vertex; each of them has degree three in `G`; each is the end of
exactly one connecting path.
(d) The output is not unique (which free edge, which end of a crossing edge a connecting path is attached to, which
edge `Calibrate` subdivides); L539 says "its output".
Fix, one paragraph after L580:
`The construction is well defined. Initially each of the two paths of a chain link has two edges, and a threading replaces one edge that no thread uses by two such edges and a crossing edge; hence step~1 of Definition~\ref{def:threading} always finds an edge on the requested path. Between the first threading and the calibration the two paths of a chain link may differ in length; we still call the cycle a chain link. The end-vertices of a crossing edge are new vertices. Hence distinct crossing edges share no vertex, and each end-vertex of a crossing edge has degree three in $G$: it is incident to two edges of its chain link and is the end of exactly one connecting path. The statements below hold for every choice made in step~1 and in \textsc{Calibrate}.`

**Definition 3.5, L584-599.** Checked, no finding ("block" is defined only in the paragraph "In words", L576).

**Lemma 3.6 (Shortest Paths, old 3.5), L601-617.** Checked, no finding: a `u`-`v` path that is not a chain path
contains an edge outside the chain, hence a whole connecting path (`Lambda` edges, inner vertices of degree two, `u`
and `v` are not inner vertices), and that path has an end that is neither `u` nor `v`, so one more edge follows.
(L615 needs one crossing edge per thread, not two; harmless.)

**Lemma 3.7 (Synchronization, old 3.6), L619-638.** Checked all four sign patterns of `(I_i, T_i)` for the
2-synchronization pair and both signs of `L_{j,k}` for the 3-synchronization pair; no finding. The proof states
the two disjunctions and leaves the four-case check to the reader, which is acceptable.

**Lemma 3.8 (Clause Threads, old 3.7), L640-651.** Checked, no finding.

**M8 (SHOULD FIX). L672-677 and L682, proof of Lemma 3.9 (Separation, old 3.8).** The lemma is correct and the case
analysis at the end is complete; I checked the points raised: `Q` cannot enter `L_{2,k}` or `L_{3,k}` first, because
the connecting paths at `u` are the first connecting paths of the threads, which lead to `I_i` or to `L_{1,k}`
(`Thread` joins `u` to the crossing edge in `K_1`); `Q` cannot revisit, because it is a path (used at L720); `Q`
stays in the three links of `C_k`, because by L712 only connecting paths of the clause thread of `C_k` are usable
there and they lead to `u`, `v` or these links; the middle connecting paths of all synchronization threads are
unusable for every sign pattern of Algorithm 1 (consecutive crossings have opposite signs in one block); Table 1
is consistent with (a), (b) and Algorithm 1 in all six rows.
What is missing is the reason for the sentence on which all of this rests, L677 ("Hence `Q` starts ..., ends ...,
and passes from one usable connecting path to the next along a segment of a single unused path"). It needs three
facts, two of which appear nowhere: the edges of `G \ P` at `u` and `v` are edges of connecting paths (the single
edges `H_1`, `H_{r+1}` lie on `P`); every end-vertex of a crossing edge is the end of exactly one connecting path
(so two connecting paths of `Q` are never consecutive); unused paths of distinct links are vertex-disjoint (L667, so
the chain edges of `Q` between two connecting paths lie in one link). Also "its sign" of a crossing edge (L682)
is not defined.
Fix, replacing L677:
`The edges of $G \setminus P$ at $u$ and at $v$ belong to connecting paths, because the single edges of the chain lie on $P$. Every end-vertex of a crossing edge is the end of exactly one connecting path, and unused paths of distinct chain links are vertex-disjoint. Hence $Q$ starts at $u$ with a usable connecting path, ends at $v$ with a usable connecting path, and between two consecutive connecting paths it follows a segment, with at least one edge, of a single unused path.`
and at L682: `(the sign of a crossing edge is the sign of the path of its chain link on which it lies)`.

**Theorem 3.10 (SSP, old 3.9), L731-767.** Checked, no new finding: both directions; the counts (`2n+7m` threads,
at most `4n+21m` crossing edges, `Lambda = O(n+m)`, `O((n+m)^2)` edges); membership in NP. (L752, "it hits every
thread", is not needed for (b); already noted in the session report.)

**M9 (SHOULD FIX). L793-795, proof of Theorem 3.11 (old 3.10); boxes L242, L340, L778.** The reduction sets
`b := d(u,v)`, which has no value when `u` and `v` lie in different components. Such inputs are excluded only by the
sentence L199, 13 pages earlier; none of the three problem boxes repeats the restriction, and the SSP box (L340)
admits "a graph and two distinct vertices". Formally the proof is complete under L199 (connectivity of `u, v` is
decidable in linear time, so the restricted problems are ordinary decision problems), but a reader of Section 3
sees a reduction that is undefined on some inputs.
Fix (make the boxes self-contained), in the Input rows L242, L340, L778:
`A graph $G = (V,E)$ and two distinct vertices $u, v \in V$ in the same connected component of $G$` (plus `, and an integer $b$` at L778).
Alternative (if the boxes stay as they are and L199 is dropped for Section 3), one sentence at L794: `If $u$ and $v$ lie in different components of $G$, the answer to \SSP{} is no and the reduction outputs a fixed no-instance, for example the path with three vertices, its two ends and $b = 1$; otherwise we set the threshold $b := d(u,v)$ ...`
The rest of the proof is checked (both directions; membership, which uses the equivalence of M2).
Remark: composing with Algorithm 1 gives `b = Lambda` directly, without breadth-first search.

**Corollary 3.12, L815-823.** Checked, no finding.

### Section 4

**M10 (MINOR). L832, L856, L890, L969: "diameter two".** Lemma 4.3, Theorem 4.5 and Remark 4.6 hold verbatim for
diameter at most two (complete graphs fall under Case 1), and the Introduction quotes Bazgan et al. with "diameter at
most two" (L150). Fix: `of diameter at most two` in the statements, the abstract (L113) and L169.

**M11 (MINOR). L836-850, Definition 4.2.** (a) "Cut" here means the set of all edges between the two sides of a
partition, possibly with an empty side, while Section 2 defines a cut as any edge set separating `u` from `v`; the
same switch happens in Lemmas 4.3, 4.4. (b) The four sets depend on the ordered pair `(A_1, A_2)`, not on `C`
("induced by `C`"; in a disconnected graph `C` does not determine the partition). (c) L837-838 say in prose what
the definition says three lines later.
Fix, L842-843: `Let $G = (V, E)$ be a graph, let $A_1, A_2$ be a partition of $V$ into two sets, and let $C$ be the set of all edges between $A_1$ and $A_2$. The \emph{decomposition induced by $(A_1, A_2)$} consists of ...`

**Lemma 4.3, L854-869; Lemma 4.4, L871-886.** Checked, no finding (4.3: take the first edge of `C` on an `x`-`y`
path; 4.4: parity).

**M12 (SHOULD FIX). L919-933, proof of Theorem 4.5.** The proof is correct. I checked: `S = C` and `P` a subset of
`C` (L915-917); `C` is the edge boundary of the component of `u` (L919-922); `|P|` odd, hence at least 3; the count:
the three groups are disjoint because each edge of `C` has exactly one end in `K`, `|K| >= 2`, the third vertex of
`P` is in `K`, differs from `u` and carries the second and third edge of `P`; `deg(u,K) <= |K| - 1`; `u` has no
neighbor in `I`. Figure 10 agrees with the count (in the figure `P` has five edges, six vertices lie in `K`, the
brace (iii) covers `|K| - 2 = 4` of them).
Both renamings are legitimate at once: the first fixes which side is called `A_2`, the second which terminal is
called `u`, and they do not interact. But the text does not say why the second is allowed: it gives "`c`, `d`, `cp`
do not depend on the order of `u` and `v`" (L930), whereas what must be symmetric at that point are the objects
already fixed: `C`, `P` and the assumption that `P` is a subset of `C`. (They are symmetric; `A`, which was defined
through `u` at L920, is no longer used.) The sides are also named twice: "in either order" (L923) and "after
exchanging the names if necessary" (L929). L932 (`v in J`) is not used in the count. L931: "the graph is
partitioned".
Fix, replacing L923 and L928-931 (L925-926 unchanged in between; Lemma 4.4 does not depend on the names):
`By Lemma~\ref{lem:empty-i-or-l}, one of the two sides $A$ and $V \setminus A$ consists only of vertices that are incident to an edge of $C$. We denote this side by $A_2$ and the other side by $A_1$, and we let $I, J, K, L$ be the decomposition induced by $C$ (Definition~\ref{def:cut-decomposition}); thus $L = \emptyset$ and $A_2 = K$. The cut $C$, the path $P$ and the assumption $P \subseteq C$ are symmetric in $u$ and $v$. Hence, after exchanging the names of $u$ and $v$ if necessary, we may assume that $u \in A_2 = K$, so $V$ is partitioned into the three sets $I, J, K$.`
(The by-product of this proof, `c(u,v) = min{deg u, deg v}`, is S3 in Part 2.)

**Remark 4.6, L966-970.** Checked, no finding.

### Section 5

**Lemma 5.1, L979-993.** Checked, no finding. Two steps are implicit and fine: the second cycle has an edge outside
the first (a cycle contained in a cycle equals it), and the two vertices reached are distinct (walking the second
cycle away from that edge in both directions, one direction meets the first cycle no later than one end of the shared
edge, the other no later than the other end).

**M13 (MINOR). L1022-1033, proof of Theorem 5.2.** Correct; three things are used before or without being said.
(a) `Z_1, ..., Z_t` and "the vertex where it enters/leaves `Z_i`" appear (L1026) before the sequence is defined and
before "`P` does not return" (L1027-1028), without which they are ambiguous. (b) L1032 ("the other arc of each
`Z_i` is edge-disjoint from `P`") needs that the `Z_i` are pairwise distinct and that every edge of `P` on `Z_i`
lies on the arc; both follow from L1024 and L1027-1028 but are not drawn. (c) The concatenation of the arcs is a
walk. (d) L1023 calls `G` "the cactus graph" although a cactus has only been described (L977).
Fix, replacing L1026: `Let $Z_1, Z_2, \dots, Z_t$ be the cycles that contain the edges of $P$, in the order in which $P$ traverses them, a cycle being listed again if $P$ comes back to it. In each $Z_i$ the path follows an arc from the vertex where it enters $Z_i$ to the vertex where it leaves $Z_i$.`
after L1028: `Hence the cycles $Z_1, \dots, Z_t$ are pairwise distinct, and the edges of $P$ on $Z_i$ are exactly the edges of this arc.`
and L1032: `... so these arcs form a $u$--$v$ walk in $G \setminus P$, which contains a $u$--$v$ path.`

### Section 6

**Theorem 6.1, L1052-1067 (new proof).** Checked, no finding.

**M14 (SHOULD FIX). L1075-1084, Theorem 6.2, and its use at L1144-1146.** (a) According to the author's own reading
note (`knowledge/literature/ChungLu2001.md`, line 13; I did not open the paper) Chung and Lu define the diameter of a
disconnected graph through its components. Definition 4.1 gives a disconnected graph no finite diameter. So Theorem
6.2, read with Definition 4.1, also asserts that `G` is connected with high probability, which the quoted bound does
not give; and the proof of Theorem 6.6 needs exactly the reading of Definition 4.1, twice: for
`d(u,v) <= diam(G)` for all pairs (L1149), and for monotonicity (L1144: with the component convention, adding an
edge that joins two components can increase the diameter, so the event is not preserved by the coupling). The gap
closes in one sentence, because for `alpha > 1` the graph is connected with high probability (it follows already from
Lemma 6.5: `c(u,v) >= beta_1 log n > 0` for all pairs).
(b) The inequality in L1084 is right: I re-derived that
`log n / log log n - (log n + log log n + O(1)) / (log log n + log alpha) - 3` tends to infinity because `log alpha > 0`.
(c) The proof of Theorem 6.6 needs only `diam(G) = o(log n)`; a statement with slack, for instance
`diam(G) <= 2 log n / log log n`, would not depend on the constants of the source.
Fix, appended to L1084:
`Chung and Lu define the diameter of a disconnected graph through its components; for $\alpha > 1$ the graph $G$ is connected with high probability (see Lemma~\ref{lem:connectivity-bounds}), so their bound holds for $\diam(G)$ in the sense of Definition~\ref{def:diameter}.`

**Theorem 6.3, L1086-1090.** Quoted from a source I did not open; no new finding (the open point, the remark on
p. 169 crediting Bollobas and Thomason, is in `sources-section-6.md`).

**Lemma 6.4, L1092-1113.** Checked, no finding: the Chernoff form (with `t = (1-a) mu` the exponent
`phi(-t/mu)` equals `h(a)`), the choice of `a_1` (continuity of `h` at 0 and `alpha > 1`), the `o(1/n)` claim (the
exponent of `n` tends to `alpha h(a_1) > 1`), the union bound, `beta_1 = a_1 alpha / 2`.

**Lemma 6.5, L1115-1131.** Checked, no finding (the middle inequality of L1129 is an equality on the event
considered).

**M15 (MINOR). L1133-1141, Theorem 6.6 (new statement).** Checked: the first claim is proved (coupling of two
increasing events, given M14), the second follows from Definition 2.5. Remaining: (a) `p` is a function of `n`;
(b) "on the inputs `(G(n,p), u, v)`" does not say how `u, v` are chosen; the proof allows any choice, also one that
depends on the graph, and that is worth saying; (c) the first claim makes the second redundant (this is what remains
of the known issue with the name "scheme").
Fix: L1135 `Let $p = p(n) \geq \alpha \log n / n$ ...`; L1140 `... on the inputs $(G(n,p), u, v)$, for an arbitrary choice of two distinct vertices $u, v$.`

---

## Part 2. Significance and positioning

**Assessment.** The paper introduces a natural problem and has one substantial result, the NP-completeness of
`Separating Shortest Path` and hence of `Min Cut-Path` (Section 3, about 8 of 17 pages; the reduction is not routine,
and Lemma 3.9 needs the `I_i`/`T_i` design so that literal links are never joined to `u` or `v` by a usable path).
The three positive results are light: Section 4 is a one-page counting argument, Section 5 concerns cactus graphs,
Section 6 is Lemma 2.3 plus textbook facts. In all three the algorithm is "any minimum cut together with any
shortest path" and the theorem says that the trivial upper bound of Lemma 2.3 is attained. For a DAM Contribution
this is at the lower end of what is published, acceptable if the paper says plainly what it has and adds the cheap
results and examples that a reader expects (S2-S6). None of the requests below needs new research; each is a few
lines. Statements about related work were checked today against reading notes (`related-work-check.md`); I add only
what that check does not contain.

**S1 (SHOULD FIX). Abstract L113, Introduction L168-170, L836, L975: the positive results are not placed.** Nowhere
before Remark 4.6 does the text say that `c(u,v) + d(u,v) - 1` is the size guaranteed by taking a minimum cut and a
shortest path, so "a minimum cut-path has `c+d-1` edges" reads as a formula found, not as "the trivial bound is
tight". Fix, L170: `In both classes the upper bound of Lemma~\ref{lem:basic-bounds} is attained, so the union of any minimum cut and any shortest path is a minimum cut-path.`
and in the abstract (L113): `..., a minimum cut-path has $c(u,v) + d(u,v) - 1$ edges, the size of the union of a minimum cut and a shortest path.`

**S2 (SHOULD FIX). No example with `cp < c + d - 1`; Conclusion L1174.** The paper never shows that the upper bound
of Lemma 2.3 can be strict, that the hypotheses of Theorems 4.5 and 5.2 are needed, or what happens at diameter
three. Two graphs on six vertices settle all of this (I found the first independently and then saw that both are the
parked figures `counterexample-cut-two.tex` and `counterexample-distance-two.tex`; I checked both by hand):
- `H_1`: edges `ua, ab, bv, us, sb, at, tv`. The path `u-a-b-v` is a shortest `u`-`v` path and a `u`-`v` cut, so
  `cp(u,v) = 3 = d(u,v)`, while `c(u,v) = 2` and `c + d - 1 = 4`. Here `c(a,b) = 3`, so the hypothesis of Theorem 5.2
  cannot be weakened to `c(u,v) <= 2`.
- `H_2 = H_1 + ub + av`: `d(u,v) = 2`, `c(u,v) = 3`, and the same path is a minimum cut, so `cp(u,v) = 3 = c(u,v)`
  while `c + d - 1 = 4`. So the hypothesis of Theorem 4.5 cannot be weakened to `d(u,v) <= 2`.
- Both graphs have diameter three, so Theorem 4.5 fails for diameter three; both lower bounds of Lemma 2.3 are
  attained with the upper bound strict.
- Both graphs belong to the class that L1174 calls "a natural candidate" (every pair at distance at most two or with
  cut-value at most two; in `H_1` the only pair with cut-value three is the adjacent pair `a, b`). So in that class
  the formula fails, and the sentence, placed after "`cp = c + d - 1` in two graph classes", suggests the opposite.
Fix: one example (a figure of `H_1` and `H_2`, already drawn) after Remark 4.6 or after Theorem 5.2, with the three
sentences above, and at L1174: `... it contains both classes treated in this paper, but the formula $\cp(u,v) = c(u,v) + d(u,v) - 1$ does not hold in it (Example~...).`

**S3 (SHOULD FIX). Section 4 and the classical theorem on diameter two.** The count (i), (iii) in the proof of
Theorem 4.5 is the standard proof that a graph of diameter two has edge connectivity equal to its minimum degree
(Plesnik 1975; TODO(verify): I give the attribution from memory, it is also mentioned in `related-work-check.md`
section 2.2 as found but not used). A DAM reader will know this theorem and will see that Section 4 is its local
version plus one edge. The paper should say so, and it should state the by-product, which I checked:
`\begin{corollary} Let $G$ be a graph of diameter at most two and let $u, v$ be two distinct vertices of $G$. Then $c(u,v) = \min\{\deg(u), \deg(v)\}$, and hence $\cp(u,v) = \min\{\deg(u), \deg(v)\} + d(u,v) - 1$. \end{corollary}`
Proof: `The edges incident to $u$ form a $u$--$v$ cut, and so do those incident to $v$; hence $c(u,v) \leq \min\{\deg(u), \deg(v)\}$. Let $C$ be a minimum $u$--$v$ cut. As in the proof of Theorem~\ref{thm:diameter-two}, $C$ is the set of all edges between the two sides of a partition of $V$, and by Lemma~\ref{lem:empty-i-or-l} one side, say $X$, consists only of vertices incident to an edge of $C$. Let $w$ be the one of $u, v$ that lies in $X$. Every edge of $C$ has exactly one end in $X$; the vertex $w$ is the end of $\deg(w, V \setminus X)$ of them, and each of the other $|X| - 1$ vertices of $X$ is the end of at least one. Hence $|C| \geq \deg(w, V \setminus X) + |X| - 1 \geq \deg(w, V \setminus X) + \deg(w, X) = \deg(w)$.`
Consequences worth one sentence each: Remark 4.6 needs no minimum-cut computation (take all edges at the terminal of
smaller degree and, if `u, v` are not adjacent, one more edge of a path of length two: linear time); for constant
`p`, with high probability `cp(u,v) = min{deg u, deg v}` for adjacent and `min{deg u, deg v} + 1` for non-adjacent
pairs of `G(n,p)`.

**S4 (SHOULD FIX). Section 5: the class is the class of cactus graphs, and the paper does not say so.** L977 says
such graphs "have the structure of a cactus graph"; in fact a connected graph has `c(x,y) <= 2` for all pairs if and
only if it is a cactus (checked). Abstract (L113), Introduction (L169), section title and Theorem 5.2 describe a
well-known class by a paraphrase ("every two vertices can be separated by at most two edges"), which hides both the
name and how elementary the result is (on a cactus, `c(u,v) = 1` if a bridge separates `u` from `v`, else 2).
Fix, replacing L977:
`A connected graph has this property if and only if it is a \emph{cactus}, that is, any two of its cycles share at most one vertex. Lemma~\ref{lem:cactus} is one direction. Conversely, by Menger's theorem, $c(x,y) \geq 3$ gives three edge-disjoint $x$--$y$ paths with first edges $e_1, e_2, e_3$; the first and the second contain a cycle through $e_1$ and $e_2$, the first and the third a cycle through $e_1$ and $e_3$, and these two cycles are distinct and share both ends of $e_1$.`
and "cactus graphs" in the abstract, L169 and the title of Section 5. (Menger's theorem needs a source, e.g. the
textbook already cited at L191.)

**S5 (MINOR). Theorem 3.10: a restriction that the reduction gives for free is not stated.** In the constructed
graph every vertex other than `u` and `v` has degree at most three (checked from the construction: link ends and ends
of crossing edges have degree three, all other vertices two; the session's computation confirms it). The session
report (decision 2c) advises against stating it because `u, v` have unbounded degree. I disagree: referees ask
"does hardness survive on restricted classes?", and one sentence answers what is known and what is not:
`In the graph constructed by Algorithm~\ref{alg:reduction}, every vertex other than $u$ and $v$ has degree at most three; $c(u,v) \geq 2n + 7m$, because the threads are edge-disjoint, and $d(u,v) = \Lambda$, so the reduction says nothing about instances with bounded $c(u,v)$ or bounded $d(u,v)$.`

**S6 (SHOULD FIX). What a referee will ask for and the paper does not discuss.**
(a) The reformulation `cp(u,v) = min over u-v paths P of ( |P| + c_{G \ P}(u,v) )` (checked: for a fixed path `P`, a
superset `S` of `P` is a `u`-`v` cut of `G` iff `S \ P` is one of `G \ P`). It is two lines, it explains the problem
("choose the path; the rest is a minimum cut"), and it shows at once that `Separating Shortest Path` asks for a
shortest `P` with `c_{G \ P}(u,v) = 0`. It is in `related-work-check.md` but not in the manuscript.
(b) Approximation. Corollary 2.4 gives factor two. The reduction separates `cp = d` from `cp >= d + 1` with
`d = Lambda` of order `n + m`, so it gives no inapproximability bound. Say so and ask whether a ratio below two or a
PTAS is possible.
(c) The symmetric question to Corollary 3.12: the complexity of deciding `cp(u,v) = c(u,v)`, that is, whether some
minimum `u`-`v` cut contains a `u`-`v` path. I do not see an immediate answer; `H_2` shows the question is not void.
(d) Parameters: besides `b` (L1184-1185), the cases of bounded `c(u,v)` and bounded `d(u,v)` (see S5), which is what
the class of L1174 is about.
(e) L1181-1182 ("how do algorithms behave on average? Experiments ...") is not an open problem of this paper: the
only algorithm in it is `C` union `P`, whose behaviour on random graphs is Theorem 6.6. Cut it or replace it by (b).
Fix: (a) as a sentence after Definition 2.2; (b)-(d) as questions in Section 7, one sentence each.

**S7 (MINOR). Motivation, abstract L109 and L130-133.** The story does not say what the cut is for: the servers
communicate along the secured path, so why must every other route contain a secured edge? As written, an applied
reader cannot tell which attack the cut prevents. Either state the model in one sentence (for example: the secured
edges are the only places where traffic between the two servers is inspected, so they must carry the communication
and meet every route) or keep only the combinatorial description. This is the author's and Prof. Loebl's call; the
present wording invites the question.

**S8 (MINOR). Related work, L137-164.** (a) Four paragraphs describe problems that are relatives by analogy (paths
whose removal does not disconnect, most vital edges, network diversion, matching cut); the two classical facts that
Sections 4 and 5 rest on (S3, S4) are absent. (b) L164 "We settle its complexity and prove its basic structural
properties": the general case is shown NP-complete, everything else is listed as open in Section 7, and the
"structural properties" are Lemma 2.3. Fix:
`We prove that it is NP-complete and identify two graph classes in which the union of a minimum cut and a shortest path is optimal.`
(c) L144: the only source for the NP-hardness of non-disconnecting paths is an arXiv preprint whose proof the reading
note calls a sketch; cite the refereed paper [1] with it.

**S9 (MINOR). Abstract, L108-115.** The results are stated correctly. Two imprecisions: "above the connectivity
threshold" (L114) promises more than Theorem 6.6, which needs `p >= alpha log n / n` with a constant `alpha > 1`
(the proof needs `d(u,v) = o(c(u,v))` for all pairs, which is shown only in that range; nothing is proved for `p`
just above the threshold); and the intermediate problem, the only other named contribution, is missing. Fix:
`In Erd\H{o}s--R\'enyi random graphs with edge probability at least $\alpha \log n / n$, $\alpha > 1$, the union ...`
and `We prove that its decision version is NP-complete, already when the question is whether some shortest $u$--$v$ path is a $u$--$v$ cut.`
(The title is in the list of open decisions; I agree that "Min Cut-Path Problem" alone tells a reader of a table of
contents nothing about the results.)

---

## Part 3. Presentation

Only what is not in the list of open decisions (symbol clashes `C`/`C_k`, `I, J, K, L`/`I_i, L_{j,k}`, `A`/`A_1`;
title; keywords; novelty sentence; declarations; highlights) and not in "Noticed, not changed" of the session report.

**P1 (MINOR). "Cut" has three meanings; "cut-value" is a private term.** L196: any edge set whose removal separates
`u` from `v`. L842, L856, L874: the set of all edges between the two sides of a partition. L1179: "minimal edge cut".
The step from the first to the second is the content of L198 and L919-922. Fix: name the second notion once in
Section 2, `For $A \subseteq V$, the \emph{edge boundary} $\partial A$ is the set of all edges between $A$ and $V \setminus A$`,
and use it in Definition 4.2, Lemmas 4.3-4.4 and L919. L197: the quantity `c(u,v)` is the local edge connectivity of
`u` and `v`; say so once (`the local edge connectivity of $u$ and $v$, which we call their \emph{cut-value}`), since
"cut-value" (also in the title of Section 5) is not a standard term.

**P2 (MINOR). Notation.** (a) `\ell[0]`, `\ell[1]` (L525, 555, 563, 564, 569, 626): zero-based array indexing of a
literal, in a paper where everything else counts from one, used only to write `L_{\ell[0],\ell[1]}`; and a literal is
"identified with its position" (L525) but compared with `x_i` in the sign function (L531). Fix: iterate over
occurrences, `for each occurrence $(j,k)$ of $x_i$` with `L_{j,k}` in lines 8-9 and 16-18 of Algorithm 1, and line 23
as `\textsc{Thread}(u,v,[(L_{1,k},s(\ell_1)),(L_{2,k},s(\ell_2)),(L_{3,k},s(\ell_3))])`, which is how Lemma 3.8 and
Table 1 already write it; L525 can then go. (b) `L` is a generic chain link (L369, L451), `L_i` the `i`-th link of a
chain (L391, L439) and `L_{j,k}` a literal link; `I_i` and `T_i` are also chain links but are not some `L_i`.
(c) The threshold is now `b`, but `k` is still, besides the clause index, a number of edges (L149, L154) and a
diameter bound (L832). (d) `V(G)` at L1097 and L1129, `V` everywhere else.

**P3 (MINOR). Text against figures, algorithm and table.**
(a) Figures 2 and 9 show a thread that visits its links from left to right. `Thread` visits them in the order of
its argument (L515), and for a clause thread this is `L_{1,k}, L_{2,k}, L_{3,k}` (L569), which is in general not
their order along the chain (the variables of the literals decide). Lemma 3.9 and Table 1 use the order of the
thread. One sentence at L577:
`A thread visits its chain links in the order given in the call of \textsc{Thread}; for a clause thread this need not be their order along the chain.`
(b) Algorithm 1, line 2 (L548), uses `u` and `v`, which no line creates. Fix: a first line `\State create two new vertices $u$ and $v$`.
(c) L483: "a separating shortest path exists only if at least one of the three literals is satisfied" names no
assignment and is not what Lemma 3.8 says. Fix:
`It encodes the clause: a consistent chain path hits it only if its truth assignment satisfies at least one of the three literals (Lemma~\ref{lem:clause-threads}).`
(d) Table 1: the caption says "can be usable" (L695), the text "lists all usable connecting paths" (L691), and the
heading "Usable if" (L699) means "if and only if". Fix, L691:
`Table~\ref{tab:usable} lists the remaining connecting paths and the condition under which each of them is usable.`
and the heading `Usable if and only if`.
(e) Figure 10 agrees with the count (M12), but its dashed edges (edges of `C` that are not counted) and the thin
edges between `I` and `J` are not explained; Figures 6-9 use thick segments (crossing edges) and dashed ends
(towards `u` and `v`) without a word. One parenthesis keeps the captions on one line, for example L938:
`The cut $C$ in the proof of Theorem~\ref{thm:diameter-two}: $P$ shaded, counted edges red, the other edges of $C$ dashed`
and L489: `The two 2-synchronization threads of a variable $x_i$ (thick: crossing edges; dashed: towards $u$ and $v$)`.

**P4 (MINOR). Terms used before or without a definition.** "Block" (first in the paragraph "In words", L576, then
inside Definition 3.5, L588). "Sign" of a crossing edge (L682; see M8). "Separating" for a chain path (L595), defined
only for shortest paths (L335) before Lemma 3.6 shows that chain paths are shortest. "Edge connectivity" and
`\delta(G)` (L1073, L1089). "Size `n`" of an instance (L283). "Articulation point", "cactus graph" (L977; see S4).

**P5 (MINOR). Forward references.** L198 sends the reader to a proof in Section 4 for a basic fact about minimum
cuts (the three sentences L920-922 could stand in Section 2 as a lemma, or a textbook could be cited). L346 refers
to the proof of Theorem 3.11. L475, L479, L483 refer to Lemmas 3.6-3.8 before the construction exists. L836 refers
to Remark 4.6. Definition 2.5 (L282-303) is used only in Section 6, 13 pages later.

**P6 (MINOR). Sentences that fail the author's own test ("delete it; did the reader lose anything?").**
L166 ("Our contributions are the following."). L237-238 and L773-774 (the box text repeats the Input row and adds
"cut-paths are defined in Definition 2.1"). L341 ("Does there exist a shortest `u`-`v` path in `G` that is a
separating shortest path?"; shorter: `Does $G$ contain a separating shortest $u$--$v$ path?`). L346 (that
`Separating Shortest Path` "is not an optimization problem" tells nothing; the second half is the first step of the
proof of Theorem 3.11). L350 (the terms "gadgets" and "basic operations" are emphasized and never used again).
L757 and L762 say the same. L809-810 repeat L790. L836-838 repeat Definition 4.2 (M11). L1181-1182 (S6e).

**P7 (MINOR). English.**
- L161 "As for \textsc{Matching Cut} and for ..." reads as "concerning"; write `As with \textsc{Matching Cut} and \textsc{Shortest Path Most Vital Edges} with unit edge lengths, ...`.
- L629 "the thread ... requires the positive path in `I_i` or ..."; write `is hit exactly when $P$ traverses the positive path in $I_i$ or the negative path in $T_i$`, as L631 does.
- L642 "a consistent chain path with the truth assignment `tau`"; write `Let $P$ be a consistent chain path and let $\tau$ be its truth assignment.`
- L891-895 and L998-1002 "a minimum cut-path between `u` and `v` has [displayed equation] edges": an equation is not a number of edges. Write `Then $\cp(u,v) = c(u,v) + d(u,v) - 1$.`
- L931 "the graph is partitioned into the three sets": `$V$ is partitioned`.
- L986-992 mix moods ("shared ... contains ... would then contain ... would require"). Write the indirect proof in the present tense: `Suppose first that two distinct cycles share an edge. Then ... The union of the two cycles then contains ... Separating $x$ from $y$ requires at least three edges, which contradicts $c(x,y) \leq 2$.`
- L745 "By the synchronization property (Lemma 3.7)": `By Lemma~\ref{lem:synchronization}`.
- L1072 calls `p = alpha log n / n` "sparse" and L1049 constant `p` "dense", but Theorem 6.6 covers every
  `p >= alpha log n / n`, dense included; the two labels are not needed.

**P8 (MINOR; the first item is visible on page 1). Layout of the 18-page PDF.**
- Page 1, footnote: the line `ORCID(s):` is printed with nothing after it. Give the ORCID in the optional argument
  after the author's name (key `orcid=`, as in `cas-sc-template.tex`, line 74), or the empty label goes to the referees.
- Pages 2, 6, 7 and 8 end with roughly a sixth to a fifth of the page empty: the `[H]` floats that follow (Figure 1,
  Figure 6, Figure 9, Algorithm 1) do not fit and move to the next page. Figure 9 is thereby separated from Figures
  7-8. The publisher will reset the article, but a referee reads this PDF.
- No text line runs into the margin (log of 09:25: the only overfull box is the class's own at `\maketitle`, plus one
  underfull line in the bibliography).

**P9 (MINOR). DAM guide for authors** (against `knowledge/venues/discrete-applied-mathematics.md`).
- Abstract: about 150 words, stands alone, no references. Complies; content remarks in S1, S9.
- Keywords: five, none with "and"/"of". "average-case approximation" names what the paper no longer claims (the
  result is "with high probability"); `random graphs` or `approximation` is closer.
- Figures: vector PDF, all ten cited in order. Captions: the guide asks that every symbol be explained (P3e). Colour
  is the only cue that tells the two threads apart in Figures 7-8 and marks the "counted edges" in Figure 10; in a
  greyscale print they are lost. Add a second cue (line style) or check them in greyscale. File names are by content
  (`cut-path.pdf`, ...); the guide suggests names that show the order (`Figure_1`, ...).
- Table 1: no vertical rules, caption above, cited. Complies.
- References: alphabetical and numbered, DOIs present. Journal names are written in full (the guide asks for LTWA
  abbreviations; applied at proof, low priority). [16] is an arXiv preprint (S8c). [9] carries a URL to a version of
  the book whose numbering differs from the printed book that is cited (already in the session report).
- Statements still missing in the PDF: declaration of competing interest, funding sentence, AI declaration (known).

**P10 (MINOR). Order of Section 3.1.1.** The three thread types are described in words (L471-484) with what they
"force" before the construction exists; the signs that make these claims true are fixed only in Algorithm 1 two
pages later, and the figures show them without saying that they are part of the definition. One clause at L471 is
enough: `Every thread has one of three types; Algorithm~\ref{alg:reduction} fixes the signs with which they are threaded:`.

---

## Part 4. Verdict

**Recommendation to the editor: major revision.** The mathematics is correct as far as I can verify by hand, and no
result is in doubt; the recommendation is driven by what the paper does not say and by the construction's
definitions, and I would want to see the revised text. An editor who weighs correctness only would call it a minor
revision. I see no ground for rejection: the NP-completeness proof carries the paper.

What drives the recommendation:

1. **The proofs hold; six passages assert instead of justify (M6-M9, M12, M14).** Definition 3.3 does not define the
   threads that are used; the construction is not shown to be well defined; the key sentence of Lemma 3.9 has no
   reason attached; the reduction of Theorem 3.11 relies on an assumption made 13 pages earlier; the two renamings in
   Theorem 4.5 are justified by the wrong symmetry; Theorem 6.2 is quoted under another convention for the diameter.
   Each is repaired by one to five sentences given above.
2. **The positive results are easy and are not placed (S1, S3, S4).** Both polynomial cases say that the trivial
   bound is tight; Section 4 is the local form of a classical theorem on diameter two and yields the closed formula
   `cp(u,v) = min{deg u, deg v} + d(u,v) - 1`, which the paper does not state; the class of Section 5 is the class of
   cactus graphs, which the paper does not name.
3. **No example of strictness, and a misleading open problem (S2).** Two graphs on six vertices, which the author
   already has, show that the bound can be strict, that the hypotheses of both theorems are needed, that diameter
   three fails, and that the formula fails in the class proposed in the Conclusion.
4. **Expected discussion is missing (S6).** The reformulation as "choose a path, then a minimum cut", approximation
   below factor two, the complexity of deciding `cp = c`, and the cases of bounded `c(u,v)` or `d(u,v)`.
5. **Section 6 is now consistent** (the 09:11 mismatch between the definition and the theorem is gone) but it is a
   corollary of Lemma 2.3; with M3, M14 and M15 it should be presented as one.
6. **Known items that a referee will raise independently:** the author's master's thesis and conference abstract on
   the same problem are found by a search and are not mentioned; competing-interest, funding and AI statements are
   absent; the title says nothing about the results; the empty `ORCID(s):` line on page 1 (P8).

Findings by severity. BLOCKER: none. SHOULD FIX: M6, M7, M8, M9, M12, M14, S1, S2, S3, S4, S6. MINOR: M1-M5, M10,
M11, M13, M15, S5, S7-S9, P1-P10.

What I verified myself and what I did not. Verified by hand: every proof step of Sections 2-6 as described in
Part 1; the two examples of S2; the corollary of S3; the equivalence of S4; the degree bound of S5; the formula of
S6(a); the agreement of Figures 7-10, Table 1 and Algorithm 1 with the text. Not verified: any cited source
(Theorems 6.2 and 6.3, the Chernoff bound's equation number, the coupling, the related-work statements; for these I
rely on `sources-section-6.md` and `related-work-check.md`); the attribution to Plesnik in S3 (from memory,
TODO(verify)); the convention of Chung and Lu in M14 (from the author's reading note). Not done: any computation or
build. The manuscript was identical to the reviewed snapshot when this report was finished (compared at the end).

