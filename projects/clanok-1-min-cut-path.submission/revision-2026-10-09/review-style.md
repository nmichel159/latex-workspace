# Style review of the revised article 1 (2026-10-09)

Reviewed: `projects/clanok-1-min-cut-path/main.tex` (1204 lines), against the original
`archives/removed-from-projects/clanok-1-min-cut-path/main-before-preserving-revision-2026-10-09.tex`.
Rules: `knowledge/writing/academic-style.md`, `knowledge/writing/math-writing.md`, `SPEC.md`.
Line numbers refer to the revised `main.tex`. No proposal removes original mathematical content; deletions
are proposed only for text the revision added (marked "added"). [MERGE] = two passages say the same thing;
the integrator decides whether to merge (no argument is lost in the proposed text).

Overall: the revision reads as plain mathematical English. No dash constructions, no *crucial / notably /
leverage / delve*-type vocabulary, no "not only ... but also", no "Formally:". The remaining problems are
(1) Lemma 3.8 (`lem:separating`) is still hard to navigate: the original walk text and the new $\Gamma$ text
run side by side; (2) several 7-11-sentence paragraphs; (3) inconsistent run-in headings and case labels;
(4) a few calques and awkward sentences; (5) about 17 *i.e.* / *that is*.

## 1. `check-text.ps1` hits (9), judged

| Line | Hit | Verdict |
|---|---|---|
| 146, 150, 159 | "citation is not a noun" | False positive: the authors are named before `\cite` (*Abhinav et al.~\cite{...} proved*). Keep. |
| 150, 162, 1182 | "Vital" | False positive: problem name *Shortest Path Most Vital Edges* / "most vital edges". Keep. |
| 164 | "To the best of our knowledge" | Allowed: once in the paper, backed by the logged searches of 2026-10-07 and 2026-10-09 (`knowledge/literature/searches.md`). But fix the referent, see 2.3. |
| 691 | "exhaustive" | False positive (cases of a proof are exhaustive in the logical sense). Keep. |
| 938 | "Moreover," | Valid: the sentence is added and redundant; delete it (see 5.6). |

No `[long]` hits were reported, but a manual count (math counted as one word) finds sentences of 40-46 words; see §4.

## 2. Wording: announcements, filler, pairs, AI-like phrasing

2.1. **l. 109** (abstract, added "secured") - paired adjectives for rhythm.
- Quote: "uses one of the chosen, secured edges."
- Replace: "uses one of the secured edges."

2.2. **l. 134** (added) - repeats l. 133 (the cut makes every other route use a selected edge) in other words;
the paragraph has 7 sentences. Delete:
"The selected edges are the links that we secure; a route through one of them is closed to the adversary."
If the "secure" motivation should stay, merge it into l. 133 instead:
"The path carries the communication, and the cut guarantees that every other route between the two servers uses at least one of the selected edges, which are secured against the adversary."

2.3. **l. 164** - after four paragraphs on other problems (Network Diversion, matching cut, ...), "the problem" has no
clear referent.
- Replace: "To the best of our knowledge, \MinCutPath{} has not been studied before."

2.4. **l. 161-162** - missing comma after an introductory phrase; "As for" is a calque (SK *ako pre*), meaning "as with".
Problem names are set inconsistently: `\textsc{Network Diversion}` at l. 155 but "network diversion" here;
"matching cut" names both the edge set (l. 157, defined term) and the decision problem.
- Replace l. 161: "In \textsc{Network Diversion} and \textsc{Matching Cut}, the cut alone carries the condition, whereas in a cut-path the cut must fit into few edges together with a path."
- Replace l. 162: "As with \textsc{Shortest Path Most Vital Edges} and \textsc{Matching Cut}, graphs of diameter two form a polynomial case of \MinCutPath{} (Theorem~\ref{thm:diameter-two})."
- l. 158: "Deciding whether a graph has a matching cut is polynomial on graphs of diameter two" -> "Deciding whether a graph has a matching cut is solvable in polynomial time on graphs of diameter two".
- l. 1182: "finding the most vital edges for shortest paths and finding a matching cut are NP-hard" may stay (verbal phrasing).

2.5. **l. 704** (added) - announcement.
- Quote: "To find the edges of $\Gamma$ given by these threads, suppose first that $\tau(x_i)=\mathsf{true}$."
- Replace: "Suppose first that $\tau(x_i)=\mathsf{true}$."

2.6. **l. 743** (added) - roadmap triad that the three `\paragraph` headings below already give.
- Quote: "The reduction is Algorithm~\ref{alg:reduction}; we prove its correctness, bound its running time and show that \SSP{} belongs to NP."
- Replace: "The reduction is Algorithm~\ref{alg:reduction}."
  (Optional; the sentence is a permitted strategy sentence, but it says nothing beyond the headings.)

2.7. **l. 871** (added) - text about the text in the second clause.
- Quote: "The next lemma holds in every graph; it concerns the intersection of a cut and a path."
- Replace: "The next lemma holds in every graph."

2.8. **l. 828** - vague "efficiently" (rule 3.3, 3.10).
- Quote: "The first class in which the problem can be solved efficiently consists of the graphs of diameter two"
- Replace: "The first class in which the problem can be solved in polynomial time consists of the graphs of diameter two"

2.9. **l. 1137-1138** (added) - l. 1137 restates Lemma 2.4 and is repeated in the proof (l. 1148, l. 1158).
- Replace both sentences by one: "The diameter bound of Theorem~\ref{thm:random-diameter} and the connectivity bound of Lemma~\ref{lem:connectivity-bounds} keep the ratio $(c(u,v)+d(u,v)-1)/c(u,v)$ below $1+\epsilon$ on almost all inputs."
  ("almost all inputs" carries the mathematical issue already logged as issues-A item 5 / issues-D item 7.)

2.10. Lead-ins of the original that only say "a result follows" (academic-style §9; optional, not mathematical content):
- l. 260 "The following elementary bounds relate $\cp(u, v)$ to the classical quantities $c(u, v)$ and $d(u, v)$." -> delete, or keep as the only sentence before the lemma (acceptable).
- l. 539 "We also introduce the following notational conventions:" -> "We use the following notation:".
- l. 940 "This structure is illustrated in Figure~\ref{fig:diameter-two-structure}." -> "Figure~\ref{fig:diameter-two-structure} shows this structure."
- l. 694 "so this option is blocked immediately" -> "so this option is blocked" ("immediately" is filler).
- l. 356 "the \emph{threads}, which are threaded through the base structure." -> "the \emph{threads}, which are threaded through the chain." (one concept, one word: "base structure" is not used again).

2.11. **l. 988** - *cf.* means "compare", not "see" (academic-style §2).
- Quote: "(cf.~\cite{Mehlhorn2017Certifying})" -> "(see~\cite{Mehlhorn2017Certifying})".

## 3. *i.e.* / *that is* (17 occurrences)

Keep those inside definitions and lemma statements (l. 209, 289, 380, 842) and the ones that give a defining
formula (l. 202, 283, 885). Replace the ones that only add a connective:

| Line | Quote | Replace |
|---|---|---|
| 347 (added) | "a solution is a single shortest $u$--$v$ path, that is, a cut-path of size $d(u,v)$" | "a solution is a single shortest $u$--$v$ path, which is a cut-path of size $d(u,v)$" |
| 643 | "..., it traverses paths of the same sign in all chain links of the block of $x_i$, that is, if and only if it is consistent." | see [MERGE] 5.3 |
| 654 | "with the sign $s(\ell_j)$, i.e., if and only if $\tau$ satisfies the literal $\ell_j$." | "with the sign $s(\ell_j)$, that is, if and only if $\tau$ satisfies the literal $\ell_j$." (keep, or) "with the sign $s(\ell_j)$; this happens if and only if $\tau$ satisfies the literal $\ell_j$." |
| 720 | "that lie on $P$, i.e., to dead ends." | "that lie on $P$, so they are dead ends." |
| 759 | "$P$ is separating, i.e., $G\setminus P$ contains no $u$--$v$ path." | "$P$ is separating, so $G\setminus P$ contains no $u$--$v$ path." |
| 867 | "and at least one edge between $b$ and $y$; that is, it passes through $J$ and $K$ and has at least three edges." | "and at least one edge between $b$ and $y$, so it passes through $J$ and $K$ and has at least three edges." |
| 888 | "an odd number of times, i.e., $|S|$ is odd." | "an odd number of times, so $|S|$ is odd." |
| 1043 | "Dense random graphs, i.e., those with a constant edge probability $p$, have diameter two" | "Random graphs with a constant edge probability $p$, called dense, have diameter two" |
| 1169 | "whose probability tends to one, i.e., it is an average $(1+\epsilon)$-approximation scheme." | "whose probability tends to one, so it is an average $(1+\epsilon)$-approximation scheme." |

Notation found here: l. 289 "its running time is $O(P(n))$ for some polynomial $P(n)$" - $P$ is a path everywhere
else. Replace: "its running time is $O(q(n))$ for some polynomial $q$."

## 4. Sentences over about 40 words

Counted with math as one word; sentences of 36-38 words (l. 587, 620, 654, 757, 856, 867, 885, 1023, 1181, 1185)
are acceptable and not listed.

4.1. **l. 173** (41, added)
- Replace: "Let $n$ be the number of vertices and let $\alpha > 1$. For edge probabilities $p \geq \alpha \log n / n$, we show that the union of a minimum cut and a shortest path is within a factor of $1+\epsilon$ of the optimum on almost all inputs (Theorem~\ref{thm:approximation-scheme})."

4.2. **l. 593** (41, added)
- Replace: "Hence the subdivided $4$-cycles are again chain links, and the chain in $G$ is a $u$--$v$ chain in the sense of Definition~\ref{def:chain}. Every $u$--$v$ path of this chain has exactly $\Lambda$ edges, and every connecting path has at least $\Lambda$ edges."

4.3. **l. 599** (40)
- Replace: "A thread shares only its crossing edges with the chain. Hence a chain path $P$ hits a thread created by $\textsc{Thread}(u,v,[(K_1,\sigma_1),\dots,(K_t,\sigma_t)])$ if and only if, for some $i$, the path $P$ traverses the path of $K_i$ with the sign $\sigma_i$."
  (Index $i$ also clashes with the variable index; issues-B item 4 proposes $r$.)

4.4. **l. 636 and l. 638** (638: 46 words). "The first thread", "one of the two threads" are vague; the bullets at l. 708-711 already name the
threads by their lists. Use the same names here:
- l. 636: "Indeed, the thread $[(I_i,+),(T_i,-)]$ requires the positive path in $I_i$ or the negative path in $T_i$, and the thread $[(I_i,-),(T_i,+)]$ requires the negative path in $I_i$ or the positive path in $T_i$."
- l. 638: "Indeed, the thread $[(I_i,+),(L_{j,k,i},-),(T_i,+)]$ is hit exactly when $P$ uses the positive path in $I_i$ or $T_i$ or the negative path in $L_{j,k,i}$. The thread $[(I_i,-),(L_{j,k,i},+),(T_i,-)]$ is hit exactly when $P$ uses the negative path in $I_i$ or $T_i$ or the positive path in $L_{j,k,i}$."

4.5. **l. 678** (40, added)
- Replace: "An end of a connecting path is \emph{open} if it is $u$, $v$, or an end-vertex of a crossing edge not on $P$. An open end of the last kind lies on $K^{\circ}$, where $K$ is the chain link of its crossing edge."

4.6. **l. 701** (42)
- Replace: "The threads that cross this unused path are one 2-synchronization thread and one 3-synchronization thread for each literal chain link $L_{j,k,i}$. The next crossing edge of the 2-synchronization thread is in $T_i$, that of the 3-synchronization thread of $L_{j,k,i}$ is in $L_{j,k,i}$, and all these next crossing edges lie on $P$."

4.7. **l. 720** (42)
- Replace: "Apart from the clause thread, this unused path is crossed only by a 3-synchronization thread. The two connecting paths of this thread that start there lead to crossing edges in $I_i$ and $T_i$ that lie on $P$, so they are dead ends."

4.8. **l. 723** (38, added; "all under $\tau$" dangles at the end)
- Replace: "Hence, with all literals evaluated under $\tau$, the four connecting paths of the clause thread give the edge $uL_{1,k}^{\circ}$ if $\ell_1$ is false, the edge $L_{j,k}^{\circ}L_{j+1,k}^{\circ}$ if $\ell_j$ and $\ell_{j+1}$ are false ($j=1,2$), and the edge $L_{3,k}^{\circ}v$ if $\ell_3$ is false."

4.9. **l. 1151** (40)
- Replace: "The diameter bound of Theorem~\ref{thm:random-diameter} and the lower bound $c(u,v) \geq \beta_1 \log n$ of Lemma~\ref{lem:connectivity-bounds} are stated for $p = \alpha \log n / n$. By the standard coupling of the random graphs $G(n,p)$ for different edge probabilities (see, e.g.,~\cite{Frieze2016}), they remain valid for every $p \geq \alpha \log n / n$."

## 5. Paragraphs and proof structure

### 5.1 Lemma 3.8 (`lem:separating`, l. 659-735): how to make it navigable

Current state. The proof has four run-in parts (`\emph{The graph $G \setminus P$.}`, `\emph{The auxiliary
multigraph $\Gamma$.}`, `\emph{The edges of $\Gamma$.}`, `\emph{Conclusion.}`). Inside "The edges of $\Gamma$" each
case first repeats the original "walk from $u$" text (l. 694, 698-702, 717-720) and then gives the new $\Gamma$ text
(l. 695, 704-714, 722-723). The reader meets the same facts twice in two vocabularies ("unused path of $I_i$" vs
"$I_i^{\circ}$", "leads back to $u$ or to a dead end" vs "gives only the edge $uI_i^{\circ}$"). The proof has no
strategy sentence (math-writing §5), and l. 732 cites "Case~3" although the items are not called cases.

Proposal (no argument removed):

(a) **Strategy sentence** after l. 666 (new, one sentence):
"We contract the parts of $G \setminus P$ that a $u$--$v$ path can use into an auxiliary multigraph $\Gamma$ and show that $\Gamma$ has no $u$--$v$ walk."

(b) **Numbered steps** with the same markup as the proofs of Theorems 3.9 and 3.10 (`\paragraph`):
- l. 668 `\emph{The graph $G \setminus P$.}` -> `\paragraph{Step 1: the graph $G \setminus P$.}`
- l. 676 `\emph{The auxiliary multigraph $\Gamma$.}` -> `\paragraph{Step 2: the multigraph $\Gamma$.}`
- l. 681 (start of the walk claim; keep the text) -> `\paragraph{Step 3: a $u$--$v$ path in $G \setminus P$ gives a $u$--$v$ walk in $\Gamma$.}`
- l. 689 `\emph{The edges of $\Gamma$.}` -> `\paragraph{Step 4: the edges of $\Gamma$.}`
- l. 726 `\emph{Conclusion.}` -> `\paragraph{Step 5: $\Gamma$ has no $u$--$v$ walk.}`
  Then l. 681 can start directly with the claim (it is already a statement), and the heading names it.
  (Alternative: Steps 3 and 5 as `claim` environments; this renumbers Theorem 3.9 and later items, so the
  `\paragraph` version is safer.)

(c) **Case labels** that match the reference at l. 732 ("by Case~3") and the case style of Sections 4-5:
- l. 693 `\item \emph{Using a chain edge.}` -> `\item \emph{Case 1: a chain edge.}`
- l. 697 `\item \emph{Using a synchronization thread.}` -> `\item \emph{Case 2: a synchronization thread.}`
- l. 716 `\item \emph{Using a clause thread.}` -> `\item \emph{Case 3: a clause thread.}`

(d) **Split long blocks**: Case 2 (l. 698-714, 6 sentences + a 4-item list + 2 sentences) already has a blank
line at l. 703; keep it. Step 5 (l. 727-734, 8 sentences): blank line after l. 728, so that "what $\Gamma$ looks
like" and "why a walk cannot exist" are separate paragraphs. Step 1 (l. 669-674, 6 sentences) and Step 3
(l. 682-687, 6 sentences after the claim) are at the limit and can stay.

(e) **[MERGE] candidates** (same fact stated twice; the integrator judges):

- [MERGE] M1, l. 701-702 vs l. 708-711 and l. 714. For $\tau(x_i)=\mathsf{true}$, the bullets for
  $[(I_i,-),(T_i,+)]$ and $[(I_i,-),(L_{j,k,i},+),(T_i,-)]$ list exactly the threads that cross $I_i^{\circ}$ and
  say that their next crossing edges lie on $P$, which is l. 701; l. 714 ("only edges $uI_i^{\circ}$ and
  $T_i^{\circ}v$") is l. 702 in $\Gamma$ language. Proposal that keeps l. 698-702 and ties them to $\Gamma$:
  l. 702 -> "Hence every continuation from $I_i^{\circ}$ leads back to $u$ or to a dead end, so in $\Gamma$ the node $I_i^{\circ}$ is adjacent only to $u$."
  and l. 704 -> "The same check for all synchronization threads of $x_i$ gives their edges of $\Gamma$. Suppose first that $\tau(x_i)=\mathsf{true}$."
  (Do not delete l. 701-702: they are original.)

- [MERGE] M2, l. 718 and l. 722 state the same criterion (a crossing edge of the clause thread lies on $P$ iff its
  literal is true), in the opposite order of dependence. Reorder within Case 3 (no deletion):
  1. l. 717 (unchanged);
  2. l. 722 rephrased as the first fact: "By the proof of Lemma~\ref{lem:clause-threads}, the crossing edge of the clause thread in $L_{j,k}$ lies on $P$ if and only if $\tau$ satisfies $\ell_j$.";
  3. l. 718: "Since $\tau$ satisfies $C_k$, at least one of these crossing edges lies on $P$, so the clause thread itself is interrupted before it reaches $v$.";
  4. l. 719-720 (split as in 4.7);
  5. l. 723 (as in 4.8).

- [MERGE] M3, l. 714 second half ("and no edge at the unused path of a literal chain link") and l. 720 (the
  3-synchronization thread at a literal unused path gives dead ends) say the same. Keep l. 720 (original);
  shorten the added l. 714 to: "In both cases the synchronization threads of $x_i$ give only edges $uI_i^{\circ}$ and $T_i^{\circ}v$."
  (l. 727 restates the consequence for literal nodes anyway.)

- [MERGE] M4, l. 695 (added) repeats l. 669 and l. 682 (single edges lie on $P$; remaining chain edges lie on unused paths).
  Replace l. 695 by: "The other edges of the chain lie on $P$ or on an unused path $K^{\circ}$, which is a node of $\Gamma$, so the chain gives no edge of $\Gamma$."

- [MERGE] M5, l. 733-734: two sentences, both "hence", one idea.
  Replace: "Hence $\Gamma$ contains no $u$--$v$ walk, so all possible continuations from $u$ are blocked in $G\setminus P$, there is no $u$--$v$ path after removing $P$, and $P$ is separating."
  (keeps every clause of the original sentence, archived file l. 645, and the new $\Gamma$ step.)

- Not a merge: l. 685 repeats the dead-end fact of l. 671-672 as a reason; keep it but point back:
  "Both ends of this connecting path are open, since, by Step 1, an end-vertex of a crossing edge on $P$ lies on no $u$--$v$ path of $G \setminus P$."

### 5.2 Theorem 3.9, item (b), l. 757 vs l. 606-607 [MERGE]

l. 606-607 (added) define "the consistent chain path of $\tau$" with the same words that l. 757 (original) repeats.
Replace l. 757 by: "Given a satisfying assignment $\tau$, let $P$ be the consistent chain path of $\tau$: in all chain links of the block of $x_i$, it traverses the positive path if $\tau(x_i)=\mathsf{true}$ and the negative path if $\tau(x_i)=\mathsf{false}$."
(only the phrase "that corresponds to $\tau$" becomes the defined term; the integrator may also cut after "of $\tau$".)

### 5.3 Lemma 3.6 (`lem:synchronization`), l. 640-643 [MERGE]

The added l. 640-642 prove both directions per variable; the original l. 643 then restates the result. Keep both, but
make l. 643 the conclusion instead of a second statement:
"Since this holds for every variable $x_i$, a chain path hits all synchronization threads if and only if it traverses paths of the same sign in all chain links of every block, that is, if and only if it is consistent."

### 5.4 Other long paragraphs (more than about 6 sentences)

| Lines | Sentences | Proposal |
|---|---|---|
| 130-136 (intro, 1st paragraph) | 7 | delete l. 134 (2.2) -> 6 |
| 167-173 (contributions) | 7 | blank line before l. 172 ("Third, ...") |
| 616-623 (proof of Lemma 3.5) | 8 | blank line after l. 619 ("Hence $Q$ contains an edge of some connecting path.") |
| 930-940 (proof of Theorem 4.5) | 11 | blank lines before l. 932 ("Let $I, J, K, L$ ...") and before l. 937 ("Since $A_2 = K \cup L = K$ ..."); delete l. 938 (5.6) |
| 1021-1031 (proof of Theorem 5.1) | 7 + display | blank line before l. 1023 ("The path $P$ therefore passes ...") |
| 1090-1102 (proof of Lemma 6.4) | 9 + display | blank line before l. 1100 ("The union bound ...") |

### 5.5 Proof of Theorem 4.5, l. 933-936: garden-path sentence

"The first exchanges the names $A_1$ and $A_2$" reads first as a noun phrase ("the first exchanges").
- Replace l. 933-935: "Two renamings do not affect the argument. The first swaps the names $A_1$ and $A_2$, and with them $I$ with $L$ and $J$ with $K$. The second swaps $u$ and $v$: the values $c(u, v)$, $d(u, v)$ and $\cp(u, v)$ do not depend on the order of $u$ and $v$, and $P$ read backwards is a $v$--$u$ path."
- l. 936: "By Lemma~\ref{lem:empty-i-or-l} and the first renaming, we may assume that $L = \emptyset$; by the second renaming, we may then assume that $u \in A_2$."

### 5.6 Redundant sentences added by the revision (deletion proposed)

| Line | Added text | Why |
|---|---|---|
| 134 | "The selected edges are the links that we secure; a route through one of them is closed to the adversary." | restates l. 133 (see 2.2) |
| 938 | "Moreover, $u$ is incident to an edge of the cut: the first edge of $P$ belongs to the cut and is incident to $u$." | $u \in K$ (l. 937) already means that $u$ is incident to an edge of $C$ (definition of $K$, Lemma 4.2) |
| 954 vs 972 [MERGE] | "Here $\deg(u, I) = 0$, because ..." | l. 972 (original) uses the same fact; move the added reason there and delete l. 954: l. 972 -> "The equality holds because $V = I \cup J \cup K$ and $u$ has no neighbors in $I$: an edge between $u \in A_2$ and a vertex of $I \subseteq A_1$ would belong to $C$, but no vertex of $I$ is incident to an edge of $C$." |
| 1137 | "By Lemma~\ref{lem:basic-bounds} and its proof, the union ... has at least $c(u,v)$ edges." | repeated in the proof (l. 1148, 1158); see 2.9 |
| 714 (second half) | "and no edge at the unused path of a literal chain link" | see M3 |
| 695 | (shorten) | see M4 |

## 6. Markup, terminology and notation

6.1. **Run-in headings inside proofs are mixed**: `\paragraph{...}` in the proofs of Theorems 3.9 and 3.10
(l. 745, 762, 770, 798, 805, 813, 818), `\emph{...}` in the proof of Lemma 3.8 (l. 668, 676, 689, 726), `\emph{Case n: ...}`
in Theorems 4.5 and 5.1, enumerate items `(a)`, `(b)` in Theorem 3.9. Proposal: `\paragraph` for steps of a proof
(Lemma 3.8 as in 5.1(b)), `\emph{Case n: ...}` for cases (Lemma 3.8 as in 5.1(c)). Items (a)/(b) of Theorem 3.9 may stay.

6.2. **Names of environments: case style.** Existing names are title case (`[Cut-Path]`, `[Basic Bounds]`,
`[Degree Bounds]`, `[Chain Link]`); the four new lemmas use sentence case. Replace:
- l. 609 `\begin{lemma}[Shortest paths]` -> `\begin{lemma}[Shortest Paths]`
- l. 646 `\begin{lemma}[Clause threads]` -> `\begin{lemma}[Clause Threads]`
  (`[Synchronization]`, `[Separation]` are single words.)
- l. 305 section title "NP-completeness of the Min Cut-Path Problem": title case would be "NP-Completeness of the Min Cut-Path Problem" (other titles: "Graphs with Cut-Value at Most Two"). Optional.

6.3. **"literal link" vs "literal chain link"** (one concept, one word, rule 3.9). "literal link" at l. 637, 701, 717,
719 and in the caption at l. 445 ("the initialization link, the literal links, and the terminal link"); "literal chain
link" elsewhere (l. 433-437, 493, 511, 587, 633, 714, 727, 730). Replace "literal link" by "literal chain link" at
l. 637, 701, 717, 719. The caption at l. 445 may keep the short form (one line).

6.4. **Problem names** (academic-style §2: small caps, identical everywhere): see 2.4 (`\textsc{Network Diversion}`,
`\textsc{Matching Cut}` at l. 161-162).

6.5. **$d_G(u,v)$** appears only in the proof of Theorem 3.10 (l. 801, 806, 809); everywhere else $d(u,v)$. Since
$G' := G$, the subscript can go: "set the threshold $k := d(u,v)$". Optional.

6.6. **$\epsilon$ vs $\varepsilon$**: the paper uses `\epsilon` 12 times and never `\varepsilon`; it is consistent.
math-writing §1 prefers `\varepsilon`; change all 12 or none.

6.7. **"cut separating $u$ and $v$" vs "separating $u$ from $v$"**: l. 196 defines "cut separating $u$ and $v$";
the abstract and the introduction (l. 112, 169) say "separating $u$ from $v$". Both are clear; if one form is
wanted, use "separating $u$ from $v$" and change l. 196 and l. 209 ("a cut separating $u$ and $v$") accordingly.

6.8. **Terms defined twice** (original; for information): *threads* (l. 450, `\emph`) and *thread* (Definition 3.3);
*threading* (l. 450) and *threading operation* (Definition 3.4); *chain link* (l. 368 and Definition 3.1). The
`\emph` before the definition environments could become plain text (l. 368 `\emph{chain link}`, l. 450
`\emph{Threads}` / `\emph{threading}` -> no `\emph`), so each term is emphasized once.

6.9. Notation clashes are logged by editor B (issues-B items 1-6, 12) and not repeated here; add l. 289 ($P(n)$ vs
path $P$, see §3).

## 7. Grammar and wording (other)

| Line | Quote | Replace |
|---|---|---|
| 177 | "Its shortest $u$--$v$ paths choose one of the two halves of every cycle" | "The shortest $u$--$v$ paths of the chain choose one of the two halves of every cycle" ("Its" can refer to the reduction) |
| 924 (added) | "The cut $C$ is the set of all edges between two sides with $u$ and $v$ on different sides." | "The cut $C$ is the set of all edges between a vertex set and its complement, with $u$ and $v$ on different sides." |
| 691 | "The following three cases are therefore exhaustive; they also describe all ways in which a path starting at $u$ could progress in $G \setminus P$." | keep; with the case labels of 5.1(c) the reference "Case~3" at l. 732 becomes correct |
| 729 | "let $W$ be a shortest one; it is a path with at least one internal node." | "let $W$ be a shortest one. It is a path, and it has an internal node because no edge of $\Gamma$ joins $u$ and $v$." (makes the reason of l. 728 explicit at the place where it is used; optional) |
| 807 | "its removal disconnects $u$ and $v$" | "its removal disconnects $u$ from $v$" (as everywhere else) |
| 1048 | "converges to 1 as $n \to \infty$" | consistent with l. 1041 would be "tends to one as $n \to \infty$"; optional (theorem statement) |
| 1188-1189 | "This work is purely theoretical. Experiments ... would answer this question and could guide the design of heuristics." | "Experiments on real-world networks and on random instances would answer this question and could guide the design of heuristics." (drop "This work is purely theoretical."; optional, original text) |

## 8. Not found

No dash parentheses (`---`), no *Formally:*, no *crucial / notably / pivotal / leverage / delve / underscore /
robust / seamless*, no *not only ... but also*, no *In summary / Overall*, no future tense for the text, no
contractions, no *thanks to / it holds that*. Captions are one line each. Paragraph-level "Moreover" opens only
l. 938 (proposed for deletion).
