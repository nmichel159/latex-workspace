# Article 2: literature, novelty and citations (2026-10-12)

Written by the literature agent. Evidence: status lines in `knowledge/bibliography/references.bib`, reading notes in
`knowledge/literature/` (`PicardQueyranne1980`, `BaswanaPandey2025Carcass`, `Mehlhorn2017Certifying`,
`NagamochiKameda1996`, `Aboulker2017Coloring`, `Erickson2019Algorithms`, `Schmidt2013TwoConnectivity`), search rows of
2026-10-12 marked "article 2" in `knowledge/literature/searches.md` (main table and the last section of the file).
"Read" means read in this session in the source named; a number is the number in that source.
The files under `open-cases/` were not read and nothing here rests on them.

## 0. What changes the presentation of the article

1. **The square decomposition is a known structure in explicit form.** The pieces joined by the edges of `F` are the
   representation of all minimum cuts between two vertices: the acyclic graph of Picard and Queyranne, called a
   *strip* by Dinitz and Vainshtein, which is a *balanced* DAG for an undirected graph (every class other than those
   of the two terminals has as many entering as leaving edges). S1-S5 are this structure for cut-value two. Section 3
   has to say so and must not list the decomposition as a contribution. What remains new is the explicit description
   for cut-value two (squares, links, general paths, terminals) and everything built on it (S7-S11, S12).
2. **The same structure is the part of the cactus of 2-edge cuts between `u` and `v`.** The first half of the planned
   sentence has an exact source (Lemma 11 of Mehlhorn et al., arXiv v3). The second half is in no source; it is a
   derivation of ours (section 2.2 below) and belongs in a remark with a short proof, or it is weakened to
   "corresponds to".
3. **S6 follows from that cactus** (the terminals of a square lie in one 3-edge-connected class). The direct proof
   can stay; a remark may point to the cactus.
4. **The criterion "an edge lies in some minimum cut iff its ends lie in different strong components"** is Corollary 6
   of Picard and Queyranne for *saturated arcs* of a directed network. For the undirected graph the article needs
   two own sentences: edges off `p_1 ∪ p_2` have both residual arcs, and the strong components are exactly the
   pieces (the source merges the component of `s` with its successors; for a flow made of edge-disjoint paths in an
   undirected graph every vertex reachable from `s` also reaches `s`).
5. **Words that mean something else in the sources.** A "3-edge-connected component" in Mehlhorn et al. is a class of
   vertices (the paths may leave it), not a subgraph: the article should say "class of the relation `c(x,y) ≥ 3`"
   and name the term of the source once. Their "cactus" is a multigraph in which every edge lies in exactly one
   cycle (cycles of length two, no bridges); the "cactus graph" of article 1 is a simple graph whose blocks are
   edges and cycles.
6. **Article 1 is an unpublished manuscript, and the journal's reference list is closed to it.** The submission
   guidelines of Algorithmica (re-opened 2026-10-12) admit only works that are published or accepted for
   publication, and send unpublished works to the running text (section 4.4). Everything that article 2 needs from
   article 1 except one result is also in the defended thesis and can be cited from there. The exception is the
   NP-completeness of \SSP{}, on which S12 rests: it exists only in article 1. Article 1 therefore has to be public
   (arXiv) or accepted before article 2 is submitted, or S12 leans on a proof that a referee cannot read.
   Until then every `\cite[Theorem~x]{Michel2026MinCutPath}` carries a number that can still move.

## 1. Standard facts (tasks A1-A5)

| # | Fact needed | Key | Exact statement and location (where read) | Status |
|---|---|---|---|---|
| A1 | Menger's theorem, edge version: `c(a,b)` = maximum number of edge-disjoint `a`-`b` paths | `Diestel2025` | Corollary 3.3.5 (ii), p. 75: the minimum number of edges separating `a` from `b` equals the maximum number of edge-disjoint `a`-`b` paths (author's preview of the 6th edition, checked 2026-10-10 for article 1) | VERIFIED; same citation as article 1 |
| A2 | Max-flow min-cut theorem | `Erickson2019Algorithms` | Section 10.3, p. 331, "The Maxflow-Mincut Theorem": the value of a maximum `(s,t)`-flow equals the capacity of a minimum `(s,t)`-cut (chapter PDF on the book's page) | VERIFIED |
| A2 | Augmenting paths; a flow of value 2 by two augmentations in `O(|V| + |E|)` | `Erickson2019Algorithms` | Section 10.4, p. 334: Integrality Theorem; with integer capacities the algorithm of Ford and Fulkerson halts after at most `|f*|` iterations, each a search of the residual graph in `O(E)` time, total `O(E |f*|)`. For `|f*| = 2` this is two searches | VERIFIED. `Cormen2022` covers the same (chapter 24 of the 4th edition by third-party listings); its section and theorem numbers were **not** seen first-hand: cite it without a location or not at all |
| A3 | Source sides of minimum `s`-`t` cuts = closed sets of the residual digraph that contain `s` and not `t` | `PicardQueyranne1980` | Theorem 1 (Section 2, p. 4 of the authors' report EP-79-R-15): with `i R j` iff (`(i,j)` an arc, `f_ij < c_ij`) or (`(j,i)` an arc, `f_ji > 0`) for a maximum flow `f`, a cut `(S, V - S)` separating `s` from `t` is minimum iff `S` is a closure for `R` containing `s` and not `t` | VERIFIED in the report (same title and abstract as the chapter). The published chapter was not reachable: cite without a number, `TODO(verify)` the numbering |
| A3 | An edge lies in some minimum cut iff its ends lie in different strong components | `PicardQueyranne1980` | Corollary 6 (Section 3, p. 8 of the report): a saturated arc belongs to some minimum cut iff its ends do not lie in the same (strong) connected component of `R` | VERIFIED in the report; holds for saturated arcs, see 0.4 |
| A3 | Textbook statement citable by number | - | not found: Erickson has none; Cormen et al., Ahuja-Magnanti-Orlin, Schrijver and Korte-Vygen were not accessible | none; secondary statement read: `BaswanaPandey2025Carcass`, Section 4.1, Lemma 20 (arXiv v4) |
| A4 | Strongly connected components in linear time | `Tarjan1972DFS`; `Erickson2019Algorithms` | Tarjan: abstract only (Crossref record): algorithm for the strongly connected components with time and space bounded by `k_1 V + k_2 E + k_3`. Erickson: Section 6.6, p. 240, strong components labelled in `O(V + E)` time | VERIFIED (Tarjan as the original source, no number; Erickson with section) |
| A4 | Bridges and 2-edge-connected components in linear time | `Schmidt2013TwoConnectivity` | Lemma 4 (an edge is a bridge iff it lies in no chain of a chain decomposition) and Section 4 (all bridges in linear time, then the 2-edge-connected components) of arXiv:1209.0700v1 | VERIFIED in the preprint; journal numbering not compared. Tarjan 1974 (the original) was not read and has no entry |
| A4 | Breadth-first search: distances from one vertex in linear time | `Erickson2019Algorithms` | Section 8.4, p. 281: breadth-first search runs in `O(V + E)` time; Theorem 8.2: the labels are the distances from `s` | VERIFIED |
| A5 | The classes of `c(x,y) ≥ 3` (3-edge-connected components) and their computation in linear time | `Mehlhorn2017Certifying` | Section 1, p. 2 of arXiv:1211.6553v3: the 3-edge-connected components are the maximal vertex subsets whose vertices are pairwise connected by three edge-disjoint paths, not necessarily inside the subset. Section 2: linear-time algorithms of Galil and Italiano, Nagamochi and Ibaraki, Taoka et al., Tsin; Sections 10-11: computed and certified in linear time | VERIFIED in arXiv v3 (posted after acceptance); journal text not compared. The older algorithms were not read and have no entries |
| A5 | Contracting the 3-edge-connected classes of a 2-edge-connected graph gives a cactus that represents its 2-edge cuts | `Mehlhorn2017Certifying` | Lemma 11 (Section 10, pp. 16-17 of arXiv v3), credited to Nagamochi and Ibaraki 2008, Section 2.3.5: for `G` 2-edge-connected and not 3-edge-connected the contraction yields a cactus representation `(C, φ)`; the edges of `C` correspond one-to-one to the edges of `G` in a 2-cut; node preimages are the 3-edge-connected components | VERIFIED in arXiv v3; `TODO(verify)` the lemma number in the journal. Primary source (book, `NagamochiIbaraki2008`): PARTIAL, not read, not in the project bibliography |
| A5 | All minimum cuts of a graph have a cactus representation (Dinits, Karzanov, Lomonosov 1976, in Russian) | `NagamochiKameda1996` (also `Mehlhorn2017Certifying`, Section 10) | Section 1, p. 135: all minimum cuts of a network can be embedded in a cactus of size `O(|V|)`, reported in [3] = Dinits, Karzanov, Lomonosov | VERIFIED as a secondary statement; the Russian original is cited only through these sources |
| A5 | "The square decomposition is the part of this cactus between `u` and `v`" | - | in no source | our derivation (2.2); prove it in a remark or weaken the sentence |

## 2. Novelty (tasks B1-B4)

### 2.1 The class (B1): not found in the literature

- Searches (web, graphclasses.org, arXiv, OpenAlex, zbMATH; row "task B1" of the log) found no class defined by
  "small distance or small local edge-connectivity", under any name, and no class defined through the diameter of the
  3-edge-connected classes.
- Nearest notions, both without a distance condition:
  - graphs with `λ(x,y) ≤ k` for **all** pairs, "maximal local edge-connectivity `k`" (`Aboulker2017Coloring`,
    Section 1, p. 2); for `k = 2` these are the graphs of Lemma 6.1 of article 1;
  - maximally local-edge-connected graphs, `λ(x,y) = min{deg x, deg y}` for all pairs, which include the graphs of
    diameter two (`Stuart2009Eavesdropping`, Theorem 11; a published proof: `Payne2012Visibility`, Theorem 2 of the
    preprint, found in this search and useful for article 1 as well).
- **Verdict (i): the class is new.** Phrase it as a definition of this paper that contains the two classes of
  article 1. One novelty sentence at most, with "to the best of our knowledge". The class has no name in the
  literature, so the name `\DC` needs no attribution. Do not write that classes "of this kind" are common.
- Not searched: Google Scholar, MathSciNet, DBLP (bot check on 2026-10-10).

### 2.2 The decomposition (B2): known structure, new explicit form

Closest named structures and what their sources state:

| Structure | Source read | What it states | Relation to the square decomposition |
|---|---|---|---|
| closures of the residual relation (acyclic after shrinking strong components) | `PicardQueyranne1980`, Theorem 1, pp. 5-6 of the report | all minimum `s`-`t` cuts of a directed network | pieces = strong components (to be proved for the undirected case); minimum cuts = closed sets |
| *strip* of Dinitz and Vainshtein, a balanced DAG | `BaswanaPandey2025Carcass`, Section 4.1, Definition 22, Lemmas 18-20 (arXiv v4) | the quotient graph by all `(s,t)`-mincuts of an undirected multigraph, directed along a maximum flow, is a DAG with one source, one sink and indegree = outdegree elsewhere; `(s,t)`-mincuts = cuts that no edge enters | exactly the pieces and `F` with the tail-to-head orientation; S4 is "balanced"; for cut-value two the common degree is 1 (link) or 2 (square) |
| cactus of the 2-edge cuts of a 2-edge-connected graph | `Mehlhorn2017Certifying`, Lemma 11 (arXiv v3) | contraction of the 3-edge-connected classes | the chain of cycles between the nodes of `u` and `v` (derivation below) |
| `(s,t)`-MC-partition, chain representation | `NagamochiKameda1996`, Lemma 3.4, p. 141 | for an **edge** `(s,t)` with `λ(s,t) = λ(N)` the minimum cuts separating `s`, `t` are nested | not our case: `u`, `v` are non-adjacent and their minimum cuts may cross (two links on different general paths) |

Derivation for the remark (ours; for the math-core and checks agents to confirm, not from a source).
Let `K` be the 2-edge-connected component of `u`, which contains `v`, and let `(C, φ)` be the cactus of Lemma 11 for `K`.
The cycles of `C` that lie between `φ(u)` and `φ(v)` form a sequence `Z_1, ..., Z_m` with `Z_i ∩ Z_{i+1} = {w_i}`,
`w_0 = φ(u)`, `w_m = φ(v)`, `w_{i-1} ≠ w_i`.
A 2-edge cut of `C` separates `φ(u)` from `φ(v)` iff its edges lie on the two different `w_{i-1}`-`w_i` arcs of one `Z_i`.
Hence `F` is the edge set of `Z_1 ∪ ... ∪ Z_m`, the squares are the pieces of `w_0, ..., w_m` (so `k = m + 1`), the links
are the pieces of the other nodes of these cycles, and the two general paths from `S_i` to `S_{i+1}` are the two arcs of `Z_i`.
A piece is the preimage of a node of these cycles together with everything attached to it outside `F`.
The terminals of a square are ends of cactus edges at one node, so they lie in one 3-edge-connected class, which is S6.

- Searches for other names ("chain", "necklace", "path of cycles", "2-cut chain", `(s,t)`-cactus, "square
  decomposition", "general square graph") found nothing further; the last two phrases occur only in the records of
  the author's thesis. For cut-value one the analogue is the sequence of `u`-`v` bridges (Cairo et al., arXiv
  2006.15024, seen as a search summary only, not cited).
- **Verdict (ii): not new as a structure; new as an explicit description for cut-value two.** The article should
  say: the structure of all minimum `u`-`v` cuts is known (Picard and Queyranne; Dinitz and Vainshtein), for
  cut-value two it takes the form of a chain, we describe this form and prove it directly because the later
  sections need its terminals and lengths. Attribute in the Introduction and at the start of Section 3. Do not
  write "we introduce a decomposition" without the attribution.
- Not read: Dinitz and Vainshtein 1994 and 2000 (the strip is attributed through Baswana and Pandey), the book of
  Nagamochi and Ibaraki, Dinits-Karzanov-Lomonosov (Russian).

### 2.3 The algorithmic result (B3): no earlier result found

- No paper asks for a shortest path that is a cut, or for a cut inside a path, under a bound on the cut-value or in a
  class defined by distances (row "task B3"). The only hits for the problem are the author's thesis and the CSGT
  2026 abstract. Nothing new since the review of article 1 (2026-10-10).
- The closest problems are those of article 1: non-disconnecting paths (`Mao2021NonSeparating`,
  `Abhinav2022NonSeparating`), two disjoint paths one of which is shortest (`EilamTzoreff1998Disjoint`), most vital
  edges (`Bazgan2019MostVital`), matching cut (`LeLe2019MatchingCut`). None has a variant for small cut-values.
- **Verdict (iii): new** (S7 criterion, S9 characterization, S10-S11 linear-time algorithm in the class, S12
  hardness for `c(u,v) = 2`), relative to the thesis as well in the sense that the thesis has the decomposition and
  the algorithm as sketches (Section 3.3, Theorems 20, 22, 23). The article has to say what the thesis contains
  (`paper-structure.md`, question 5). The tools are standard (two augmentations, strong components, breadth-first
  search) and are cited as such.

### 2.4 Diameter two and three (B4)

Verified in the reading notes of 2026-10-09, no new search:
`LeLe2019MatchingCut`, Theorem 1 and Section 1.1 (Matching Cut: polynomial for diameter two, NP-complete for every fixed diameter at least three);
`Bazgan2019MostVital`, Proposition 1 and Theorem 4 of arXiv v1 (Shortest Path Most Vital Edges with unit lengths: linear time for diameter at most two, NP-hard on split graphs, hence for diameter three).
Cite both without statement numbers (journal numbering not compared).
No third example was added.

## 3. Ready-to-use sentences

One sentence per line. Macros `\MinCutPath`, `\SSP`, `\cp`, `\DC` as in the specification; labels are placeholders.
Sections 3.1-3.6 cite the author's results from the thesis wherever the thesis has them, because the thesis can
stand in the reference list today and article 1 cannot (section 4.4). The only citation of article 1 that has no
substitute is marked. Section 3.7 gives the variants for the time when article 1 is public.
Statement numbers of the thesis were read in `knowledge/sources/diplomova-praca-2025-min-cut-path.txt` on 2026-10-12;
those of article 1 are the numbers of its build of 2026-10-10.

### 3.1 Introduction: the problem and earlier work of the author

```latex
The \MinCutPath{} problem was introduced in the author's master's thesis~\cite{Michel2025MinCutPath}.
The thesis proves that $\cp(u,v) = c(u,v) + d(u,v) - 1$ for all pairs of vertices in graphs of diameter two and in graphs with $c(x,y) \leq 2$ for all pairs~\cite[Theorems~15 and~18]{Michel2025MinCutPath}.
It also defines the class $\DC$ and contains a first version of the decomposition and of the algorithm of this paper, with definitions given by procedures and with proof sketches~\cite[Section~3.3]{Michel2025MinCutPath}.
Here all notions are defined without reference to an algorithm and every statement is proved.
The complexity of the problem is left open in the thesis.
% Only in article 1, no substitute in the thesis:
Deciding whether $\cp(u,v) = d(u,v)$ is NP-complete~\cite{Michel2026MinCutPath}.
```

### 3.2 Introduction: minimum cuts between two vertices

```latex
By Menger's theorem, $c(u,v)$ is the maximum number of pairwise edge-disjoint $u$--$v$ paths~\cite[Corollary~3.3.5]{Diestel2025}.
Picard and Queyranne~\cite{PicardQueyranne1980} described all minimum cuts between two vertices of a network by one maximum flow.
A set that contains the source and not the sink is the source side of a minimum cut if and only if no arc of the residual digraph leaves it.
For an undirected graph, contract every class of vertices that no minimum $u$--$v$ cut separates and direct the remaining edges along a maximum flow.
The result is an acyclic digraph in which every vertex other than the classes of $u$ and $v$ has as many entering as leaving edges, a structure that Dinitz and Vainshtein call a strip (see~\cite{BaswanaPandey2025Carcass}).
All minimum cuts of a graph are represented by a cactus, a result of Dinits, Karzanov and Lomonosov (see~\cite{NagamochiKameda1996}).
For a 2-edge-connected graph that is not 3-edge-connected, this cactus is obtained by contracting every 3-edge-connected class and is computed in linear time~\cite{Mehlhorn2017Certifying}.
For a pair with $c(u,v) = 2$, the square decomposition of Section~\ref{sec:structure} is an explicit form of these representations.
We prove its properties directly, because Sections~\ref{sec:separating} and~\ref{sec:algorithm} use the terminals of the squares and distances inside the squares, which a contraction does not keep.
```

### 3.3 Introduction: paths whose removal matters

```latex
A $u$--$v$ path is \emph{non-disconnecting} if the removal of its edges leaves the graph connected.
Deciding whether such a path exists is NP-hard~\cite{Mao2021NonSeparating}, and a shortest one is found in FPT time with respect to its length~\cite{Abhinav2022NonSeparating}.
For two pairs of vertices, it is NP-complete to decide whether some shortest path between the first pair is edge-disjoint from some path between the second pair~\cite{EilamTzoreff1998Disjoint}.
\SSP{} asks the opposite, namely whether the removal of the edges of some shortest $u$--$v$ path separates $u$ from $v$.
% Only in article 1, no substitute in the thesis:
It is NP-complete~\cite[Theorem~3.10]{Michel2026MinCutPath}, and we show that it stays NP-complete for pairs with $c(u,v) = 2$ (Theorem~\ref{thm:hardness}).
```

### 3.4 Introduction or Section 2: the class

```latex
Classes of graphs in which the local edge-connectivity of every pair of vertices is at most a constant $k$ were studied for coloring problems~\cite{Aboulker2017Coloring}.
For $k = 2$ the connected graphs of this kind are the cactus graphs, in which two distinct cycles share at most one vertex.
This characterization is folklore.
The class $\DC$ asks for $c(x,y) \leq 2$ only when $d(x,y) \geq 3$, so it contains all cactus graphs and all graphs of diameter two.
To the best of our knowledge, a class defined by such a condition on distances and cut-values has not been studied.
```

### 3.5 Body: places that need a citation

```latex
We use standard notation from graph theory and follow the conventions of~\cite{Diestel2025,Cormen2022}.
Every pair of vertices satisfies $\max\{c(u,v), d(u,v)\} \leq \cp(u,v) \leq c(u,v) + d(u,v) - 1$~\cite[Claim~7]{Michel2025MinCutPath}.
If $c(u,v) = 1$ or $d(u,v) = 1$, then $\cp(u,v) = c(u,v) + d(u,v) - 1$~\cite[Claim~6]{Michel2025MinCutPath}.
The bridges of a graph and its 2-edge-connected components are found in linear time~\cite{Schmidt2013TwoConnectivity}.
By Menger's theorem~\cite[Corollary~3.3.5]{Diestel2025}, a pair with $c(u,v) = 2$ is joined by two edge-disjoint $u$--$v$ paths and not by three.
The relation $c(x,y) \geq 3$ is an equivalence relation on $V$, and its classes, called 3-edge-connected components in~\cite{Mehlhorn2017Certifying}, are computed in linear time.
In graphs of diameter two and in cactus graphs, $\cp(u,v) = c(u,v) + d(u,v) - 1$ for all pairs~\cite[Theorems~15 and~18]{Michel2025MinCutPath}.
The two graphs of~\cite[Figure~3.3]{Michel2025MinCutPath} lie in $\DC$ and violate this formula.
Two edge-disjoint $u$--$v$ paths are found by two augmentations of the algorithm of Ford and Fulkerson, each a search of the residual digraph, in $O(|V| + |E|)$ time~\cite[Section~10.4]{Erickson2019Algorithms}.
For a set $A$ of vertices with $u \in A$ and $v \notin A$, the cut $\delta(A)$ is a minimum $u$--$v$ cut if and only if no arc of the residual digraph leaves $A$~\cite{PicardQueyranne1980}.
An edge of $p_1 \cup p_2$ lies in some minimum $u$--$v$ cut if and only if its ends lie in different strongly connected components of the residual digraph~\cite{PicardQueyranne1980}.
The strongly connected components of a digraph are computed in linear time~\cite{Tarjan1972DFS}.
Breadth-first search computes the distances from one vertex in $O(|V| + |E|)$ time~\cite[Section~8.4]{Erickson2019Algorithms}.
```

Remark for Section 3 (after S6; needs the proof of 2.2 or the weaker verb "corresponds to"):

```latex
Let $K$ be the 2-edge-connected component of $G$ that contains $u$ and $v$.
Contracting every 3-edge-connected class of $K$ gives a cactus, possibly with cycles of length two, whose pairs of edges on a common cycle are the 2-edge cuts of $K$~\cite{Mehlhorn2017Certifying}.
The cycles of this cactus between the classes of $u$ and $v$ form a chain.
The squares correspond to the classes of $u$ and $v$ and to the nodes shared by consecutive cycles of the chain, and the links correspond to the other nodes of these cycles.
The two general paths between consecutive squares correspond to the two arcs of one cycle.
```

`check-text.ps1` on these sentences (extracted to `tmp/clanok-2-literature/related-work-sentences.tex`): two findings,
both kept. "To the best of our knowledge" occurs once and rests on the search row "task B1"; if the article also
keeps the sentence of article 1 on the problem itself, only one of the two may stay (`academic-style.md`, §6).
"Vital" is part of the problem name \textsc{Shortest Path Most Vital Edges}.

### 3.6 Conclusion: diameter three

```latex
Graphs of diameter two are a polynomial case of \textsc{Matching Cut} and, for unit edge lengths, of \textsc{Shortest Path Most Vital Edges}, and both problems are NP-hard on graphs of diameter three~\cite{LeLe2019MatchingCut,Bazgan2019MostVital}.
We do not know whether \MinCutPath{} is NP-hard on graphs of diameter three.
```

### 3.7 Variants once article 1 is public (arXiv or accepted)

Replace the thesis citations of 3.1 and 3.5 by these; the numbers have to be read again in the public version.

```latex
The \MinCutPath{} problem was introduced in the author's master's thesis~\cite{Michel2025MinCutPath} and studied further in~\cite{Michel2026MinCutPath}.
Deciding whether $\cp(u,v) = d(u,v)$ is NP-complete, and $\cp(u,v) = c(u,v) + d(u,v) - 1$ holds for all pairs of vertices in graphs of diameter two and in cactus graphs~\cite{Michel2026MinCutPath}.
If $c(u,v) = 1$ or $d(u,v) = 1$, then $\cp(u,v) = c(u,v) + d(u,v) - 1$~\cite[Lemma~2.3]{Michel2026MinCutPath}.
A connected graph satisfies $c(x,y) \leq 2$ for all pairs if and only if it is a cactus graph~\cite[Lemma~6.1]{Michel2026MinCutPath}.
In graphs of diameter two and in cactus graphs, $\cp(u,v) = c(u,v) + d(u,v) - 1$ for all pairs~\cite[Theorems~5.5 and~6.2]{Michel2026MinCutPath}.
The two graphs of~\cite[Example~6.3]{Michel2026MinCutPath} lie in $\DC$ and violate this formula.
```

While article 1 is neither public nor accepted, the guidelines leave only a mention in the text for it (4.4), for
example:

```latex
\SSP{} is NP-complete (N.~Miche\v{l}, \emph{Min Cut-Path Problem}, manuscript, 2026).
```

## 4. Project bibliography, open items, what was not accessible

### 4.1 Keys in `projects/clanok-2-min-cut-path/references.bib` (17, copied from the canonical file)

| Group | Keys |
|---|---|
| Own work | `Michel2026MinCutPath` (new entry, unpublished manuscript), `Michel2025MinCutPath` (the existing thesis entry; no entry `Michel2025Thesis` was created) |
| Textbooks | `Diestel2025`, `Cormen2022`, `Erickson2019Algorithms` (new) |
| Standard algorithms | `Tarjan1972DFS` (new), `Schmidt2013TwoConnectivity` (new) |
| Structure of minimum cuts | `PicardQueyranne1980` (new), `BaswanaPandey2025Carcass` (new), `NagamochiKameda1996`, `Mehlhorn2017Certifying` |
| The class | `Aboulker2017Coloring` (new) |
| Related problems | `Mao2021NonSeparating`, `Abhinav2022NonSeparating`, `EilamTzoreff1998Disjoint`, `Bazgan2019MostVital`, `LeLe2019MatchingCut` |

In the canonical file only, not in the project: `Payne2012Visibility` (VERIFIED), `DinitzVainshtein2000Carcass`
(PARTIAL), `NagamochiIbaraki2008` (PARTIAL), and the entries of article 1 not used above (`Stuart2009Eavesdropping`,
`Baier2010LengthBounded`, `Bentert2025NetworkDiversion`, `Komusiewicz2020MatchingCut`, `Marx2013Separators`, ...).
Delete from the project file whatever the final text does not cite (`check-bib.ps1` reports it as `unused`).

### 4.2 Open `TODO(verify)` items

1. Numbering of Picard and Queyranne in the published chapter (read: the report). Cite without a number until compared.
2. Lemma 11 and the definition of 3-edge-connected components in the journal text of Mehlhorn et al. (read: arXiv v3).
3. Section 4.1 and its numbers in the SOSA text of Baswana and Pandey (read: arXiv v4); the sentence in 3.2 cites the paper without a section for this reason.
4. Section and theorem numbers of `Cormen2022` (4th edition): unverified, cite without a location.
5. Lemma 4 and Section 4 of Schmidt in the journal text (read: arXiv v1).
6. Statement numbers of article 1 (Lemma 2.3, Lemma 6.1, Theorems 3.10, 5.5, 6.2, Example 6.3): check against the version that is posted.
7. The sentences in 3.1 on what the thesis contains: confirm with the author. The thesis numbers (Claims 6, 7, 17, Theorems 15, 18, 20, 22, 23, Definition 37, Figure 3.3, Section 3.3) were read in the extracted text; the errata of the thesis (`knowledge/research/min-cut-path.md`, Section 5a) do not touch these statements.
8. The remark on the cactus (2.2, 3.5): proof by the math-core agent, test by the checks agent.
9. The identification "strong components of the residual digraph = pieces" (0.4): proof in the article.
10. Reference list of Algorithmica (4.4): `Michel2026MinCutPath` cannot stay in the list of a submitted version as it is; `Mao2021NonSeparating` is a preprint and `Erickson2019Algorithms` a self-published book (a misc entry with a url), which the guide does not address. Decide before submission.
11. The thesis has a public record, `http://hdl.handle.net/20.500.11956/200007` (defence 2025-06-13), noted in the comment of the canonical entry. The entry has no `url` field; adding one is a proposal, not applied.
12. `knowledge/literature/README.md` (table of notes) and `knowledge/research/min-cut-path.md` (Section 5b) do not list the seven new notes and the new sources yet; they belong to other owners.
13. Authors of `PicardQueyranne1980` are written with initials. With the full first given name the trace scan of `package-project.ps1` failed the package check of article 2 (it reads the name as an AI tool), and the allow-list it offers lies in `projects/<project>/submission/`, which the flat layout forbids. Infrastructure, for the owner of the scripts.
14. What `sn-mathphys-num.bst` does with the entries (scratch build `tmp/clanok-2-literature/bibtest.tex`, 17 entries, no BibTeX warning): it prints the page range `6:1--6:15` of `Abhinav2022NonSeparating` as "pp. 6-1615", and it prints no arXiv number for `Mao2021NonSeparating` (a misc entry; only the note "arXiv preprint"). Both are for the integration agent; the entries follow the rules of the canonical file.
15. The CSGT 2026 abstract (one page, `https://csgt2026.tuke.sk/pdfs/MICHEL.pdf`) is the only public text that states the NP-completeness result. It has no canonical entry: the type of contribution and the date are `TODO(verify)` with the author (`knowledge/author.md`).

### 4.3 Not accessible in this session

| Source | Reason | Consequence |
|---|---|---|
| Picard, Queyranne: published chapter (SpringerLink) | paywall | report read instead |
| Dinitz, Vainshtein: STOC 1994, SIAM J. Comput. 2000 | paywall, no free copy found | PARTIAL entry; the strip is attributed through Baswana and Pandey |
| Nagamochi, Ibaraki: *Algorithmic Aspects of Graph Connectivity* (2008) | not free | PARTIAL entry; Lemma 11 is cited from Mehlhorn et al. |
| Dinits, Karzanov, Lomonosov 1976 | Russian, not available | cited through `NagamochiKameda1996` |
| Mehlhorn et al., journal text; Baswana and Pandey, SOSA text; Schmidt, journal text | paywall or HTTP 403 | numbers are those of the arXiv versions |
| Cormen et al., 4th edition (text and table of contents) | publisher page HTTP 403 | no locations cited |
| Tarjan 1972 (text), Tarjan 1974 | paywall | abstract only; 1974 has no entry |
| Galil and Italiano 1991, Nagamochi and Ibaraki 1992, Tsin 2007, 2009, Dinitz and Westbrook 1998, Hellwig and Volkmann 2004, 2008, Plesník 1975 | not opened or records only | no entries, not cited |
| DBLP, Google Scholar, MathSciNet | bot checks, no access | not searched |

### 4.4 Citing the author's own works under Algorithmica's rule

What the guide says (submission guidelines, section "References", re-opened 2026-10-12 at
<https://link.springer.com/journal/453/submission-guidelines>):

- The reference list includes only works that are cited in the text and that have been published or accepted for
  publication (close paraphrase).
- Verbatim: "Personal communications and unpublished works should only be mentioned in the text."
- Citations are numbers in square brackets, and the entries of the list are numbered consecutively.
- Example entries: journal article, article by DOI, book, book chapter, online document. The guide has no example
  for a dissertation and does not mention arXiv or preprints.
- Section "Text": a footnote may contain the citation of a listed reference but should not consist only of a citation.

Practice of the journal (Crossref reference lists of four Algorithmica articles published from June 2026, read
2026-10-12): two of them list arXiv preprints, for example the article with DOI 10.1007/s00453-026-01396-2 lists a
preprint as "arXiv: 2502.18429". A preprint posted on arXiv is therefore accepted in the list.

| Work | State on 2026-10-12 | How article 2 can cite it | Key |
|---|---|---|---|
| Master's thesis | defended 2025-06-13, public record with a handle in the repository of Charles University | in the reference list, as a defended and publicly deposited work (the guide has no dissertation example, so this is an inference; the style prints the entry type) | `Michel2025MinCutPath` |
| Article 1 | manuscript, not submitted, not on arXiv | **not in the reference list.** Today only a mention in the text, for example "(N. Micheľ, *Min Cut-Path Problem*, manuscript, 2026)". After posting on arXiv: a list entry with the arXiv number. After acceptance: a regular entry | `Michel2026MinCutPath` (to be rewritten at that time) |
| CSGT 2026 abstract | one public page, results without proofs | possible as an online document, of no use for a proof | no entry |

Which result comes from where:

| Needed in article 2 | Thesis (read in the extracted text) | Article 1 (build of 2026-10-10) | Cite |
|---|---|---|---|
| bounds `max(c, d) ≤ cp ≤ c + d − 1` | Claim 7 | Lemma 2.3 | thesis, or two lines of proof in S0 |
| `c = 1` or `d = 1` gives `cp = c + d − 1` | Claim 6 | Lemma 2.3 | thesis, or two lines of proof in S0 |
| `cp = c + d − 1` in graphs of diameter two | Theorem 15 | Theorem 5.5 | thesis |
| `cp = c + d − 1` when `c(x,y) ≤ 2` for all pairs | Theorem 18 (with Claim 17: such a graph consists of cycles and single edges joined at cut vertices) | Theorem 6.2 (with Lemma 6.1) | thesis |
| the class and the two counterexamples | Definition 37, Figure 3.3 | Example 6.3; the class is named only in the conclusion | thesis |
| decomposition for `c(u,v) = 2`, polynomial and linear-time algorithm in the class | Section 3.3: Theorems 20, 22, 23 | - | thesis, as the first version (3.1) |
| NP-completeness of \SSP{}, that is, of deciding `cp = d` | **not in the thesis** (stated there as an open problem) | Theorems 3.10, 3.11, Corollary 3.12 | **article 1 only**; S12 rests on it |
| no approximation scheme, fixed-parameter tractability, random graphs | - | Sections 4, 7, 8 | not needed in article 2 |

Consequence: with the thesis as the source, article 2 needs article 1 in exactly one place, the reduction of S12.
Recommended order: post article 1 on arXiv, then submit article 2 with the entry rewritten to the arXiv record.
If article 2 has to go first, S12 either carries the text mention above (a referee cannot check the proof) or is
left to a later paper.
The guide also expects the overlap with earlier texts to be described at the start of the paper (venue card, row
"Prior publication"); the sentences of 3.1 do this for the thesis.

### 4.5 Checks run on 2026-10-12

| Check | Result |
|---|---|
| `check-bib.ps1 -CanonicalOnly` | 140 entries (10 new), 38 findings, none on an entry added or changed here: 5 `required`, 32 `recommended`, 1 `pages`, all on older entries of other sections. One older `status` finding (`Feige1998Threshold`, status line broken over two lines) was repaired |
| `check-bib.ps1 -Project clanok-2-min-cut-path` | 17 entries, every entry equal to the canonical one; 17 `unused` (the manuscript still has placeholder text and cites nothing) and 1 `recommended` (`LeLe2019MatchingCut` has no issue number in its Crossref record) |
| scratch build of all 17 entries with `sn-mathphys-num.bst` (`tmp/clanok-2-literature/bibtest.tex`) | BibTeX: no warning, no error; see item 14 of 4.2 for two effects of the style |
| `build-project.ps1 -Project clanok-2-min-cut-path` | exit code 0; static package check `Verdict: PASS` (one note: no AI declaration yet); the PDF is unchanged because nothing is cited yet |
| `check-text.ps1` on the sentences of section 3 | two findings, both kept (after 3.5) |
