# B2. Path and cut in one set; known structural results (critical literature search, 2026-10-10)

Status: COMPLETE (2026-10-10). Nothing outside this file was changed.

Scope: angles 1-6 of the brief (abstract formulations, classical path-cut relations, cut-plus-connecting-structure
problems, known results the manuscript proves itself, parameterized side, approximation side).
Already searched elsewhere and not repeated here: `knowledge/literature/searches.md` (rows 2026-10-07 to 2026-10-10) and
`projects/clanok-1-min-cut-path.submission/session-2026-10-10/related-work-check.md`.

## 1. Verdict

1. Same problem: not found. No source defines an edge set containing a u-v path and a u-v cut, or asks how much a
   u-v path and a u-v cut can overlap.
2. Equivalent abstract formulation: not found. "Smallest set containing a member of a clutter and a member of its
   blocker" (winning and blocking coalition, path set and cut set at once, transversal containing an edge, common
   implicant of f and its dual) is not studied in any of the six wordings searched.
3. A result of the manuscript IS already known: the first half of `cor:diameter-two-degrees`,
   `c(u,v) = min{deg u, deg v}` for every pair in a graph of diameter at most two. It is a theorem of Fricke,
   Oellermann and Swart (unpublished manuscript, 2000), printed as Theorem 11 in Stuart, Czechoslovak Math. J. 59
   (2009) 623-636, and generalized to digraphs by Hellwig and Volkmann, Ars Combin. 72 (2004) 295-306. Graphs with
   this property are called maximally local-edge-connected. The corollary must be attributed.
4. `lem:empty-i-or-l` and the counting in the proof of the corollary are the standard argument of that literature
   (the two cases in Hellwig and Volkmann's proof). The formula `cp = c + d - 1` in diameter two is not in it.
5. `lem:cactus` (pairwise cut-value at most two iff any two cycles share at most one vertex) is folklore. No source
   states exactly this sentence; Marx and Végh (ACM TALG 2015, Proposition 3.7 of the arXiv version) prove the
   non-trivial direction for 2-edge-connected graphs, and two further sources state neighbouring forms. It should
   be called well known and not counted as a contribution.
6. FPT: no theorem of Marx, O'Sullivan and Razgon contains MIN CUT-PATH as a special case, but their CONNECTED s-t
   CUT (Section 3.3, Theorem 3.7) is solved by the same three steps as the manuscript's proof; the manuscript should
   say that it follows that pattern.
7. Background the Introduction lacks: Menger (edge version), Robacker (`d` = maximum number of disjoint cuts) and
   the length-width inequality `c * d <= |E|` of Moore and Shannon; statements verified in Schrijver's lecture notes
   (Theorem 1.2, Corollary 4.1b), originals by record only.
8. Neighbours a referee may name that the text does not mention: CONNECTED s-t CUT; shortest-path separators
   (Abraham, Gavoille, PODC 2006; vertex version, balanced separation); for "no PTAS", the 1.1377 hardness of
   length-bounded cuts (Baier et al.).
9. The novelty sentence stands for third-party work, with the caveat of the earlier check (the author's own thesis
   and conference abstract). The two attribution gaps (items 3 and 5) are the risk.
10. Not opened: the Hellwig-Volkmann survey text, Hellwig-Volkmann 2004, Moore-Shannon, Lehman, Akbari et al.
    (publisher blocks); the theorem numbers there are `TODO(verify)`.

## 2. Findings per angle

How sources were read: the fetch tool returns PDFs as binary and keeps a copy in its own session cache (outside the
workspace); I read those copies with `pdftotext` to standard output and saved nothing myself. "Read" below always
names the version and the part read.

Order of the subsections: 1, 4 (the one with consequences for the text), 2, 3, 5, 6.

### Angle 1. Abstract formulations under other names: nothing found

Equivalent forms of a cut-path that I searched for (the equivalences are standard blocking duality and are mine, not
quoted from a source):

| Language | A cut-path between u and v is ... |
|---|---|
| Clutters (Edmonds, Fulkerson) | a set containing a member of the clutter of u-v paths and a member of its blocker (the minimal u-v cuts) |
| Hypergraph transversals | a transversal of the hypergraph of u-v paths that contains one of its edges (equally, a set meeting every u-v path and every u-v cut) |
| Simple games | a coalition that is winning and blocking (winning, with a losing complement) in the game whose winning coalitions are the edge sets containing a u-v path |
| Two-terminal reliability | a set of components that is a path set and a cut set at once |
| Monotone Boolean functions | a common implicant of the connectivity function f and of its dual f^d |
| Shannon switching game | an edge set that contains a winning set of Short and a winning set of Cut |
| Matroids (after adding the edge e = uv) | (C - e) union (D - e) for a circuit C and a cocircuit D through e, in the port of the graphic matroid at e |

Result of the searches (log, rows A1-A3): no paper studies the minimum size of such a set, for graphs or for general
clutters, hypergraphs, games or matroids, and none gives a complexity result for it.
- Reliability wording: hits are textbooks and enumeration methods for minimal path sets and minimal cut sets, which
  treat the two families separately (OpenAlex: 59 full-text hits for the phrase "path set and a cut set", the first
  six are enumeration and bounds papers; arXiv: 1 hit, 2607.25103, on path-set attributes, title only).
- Simple games: "winning and blocking" appears in definitions of proper and strong games and in voting-power papers
  (zbMATH: 4 titles, e.g. "Weighted voting procedure having a unique blocker", 2021, DOI
  10.1007/s00182-020-00751-z according to OpenAlex, title only); no minimum-size or complexity question.
- Clutters and blockers: the literature is about packing and covering (ideal and Mengerian clutters, the
  width-length inequality, see angle 2), never about the union of a member and a blocker member. Queries with
  "clutter", "blocker", "union", "self-blocking", "blocking clutter": 0 hits in arXiv and zbMATH.
- Transversals: "transversal containing an edge" has no hits as a studied notion; the complementary notion
  (a transversal containing no edge, i.e. 2-colourability) is classical, which makes the absence credible rather than
  an artefact of wording.
- Matroid ports: 6 arXiv hits, all on secret sharing and lattice path matroids. (In secret sharing a set that is
  authorized for an access structure and for its dual is the same object; I did not search that literature further.)
- Boolean functions: one query; hits are on dualization and self-dual decompositions, not on common implicants.

Assessment: the abstract problem "smallest set containing a member of a clutter and a member of its blocker" appears
to be unstudied. For the manuscript this cuts both ways: no priority problem, and an opportunity for one sentence in
the Introduction or Conclusion that places MIN CUT-PATH in the blocking framework (with [EF70] as the reference for
the path and cut clutters, angle 2). Recommendation: REPORT; optional sentence, no novelty risk found.

### Angle 4. Results the manuscript proves itself

#### 4a. Local edge connectivity in graphs of diameter at most two: KNOWN (2000 / 2004)

The statement of `cor:diameter-two-degrees` (first half: `c(u,v) = min{deg u, deg v}` for every pair in a graph of
diameter at most two) is a known theorem. Graphs with this property are called *maximally local-edge-connected*.

**[Stu09] Stuart 2009 (journal article, open access, read in full: the most convenient citable source).**
- Reference: Jeffrey L. Stuart, The eavesdropping number of a graph, Czechoslovak Mathematical Journal 59(3) (2009)
  623-636, DOI 10.1007/s10587-009-0056-9. Record: Crossref (`api.crossref.org/works/10.1007/s10587-009-0056-9`);
  full text from the Czech Digital Mathematics Library, `http://dml.cz/dmlcz/140505`.
- Read: full text (14 pages).
- Exact statement (Section 4 "Maximally locally connected graphs", p. 627; finite simple undirected graphs): "The
  graph G is called maximally locally connected if lambda(u,v) = min{d(u), d(v)} for all distinct u, v in V(G). In
  [4], Fricke, Oellermann and Swart showed the following result: Theorem 11. If G is a graph with diam(G) <= 2, then
  lambda(u,v) = min{d(u), d(v)} for all pairs of distinct vertices u and v." No proof is given there. [4] is the
  manuscript of 2000; the paper also cites Hellwig's dissertation and Hellwig and Volkmann 2004.
- Also relevant to the Introduction: the paper has the same kind of motivation as the manuscript (Section 1: a spy
  agency must be able to intercept wireline communication between any two centres; the eavesdropping number is the
  maximum over all pairs of the minimum u-v edge cut, i.e. the maximum local edge connectivity). It studies cuts
  only, no path. Lemma 29 there: a graph with at least one edge is a forest iff its eavesdropping number is 1, and
  contains a cycle iff it is at least 2 (the level below `lem:cactus`; the level "at most 2" is not treated).

**[H05] Hellwig, dissertation (states the theorem with attribution and proves the digraph version).**
- Reference: Angelika Hellwig, *Maximally Connected Graphs and Digraphs*, doctoral dissertation, RWTH Aachen
  (Fakultät für Mathematik, Informatik und Naturwissenschaften), referees L. Volkmann and E. Triesch, oral examination
  27.04.2005. 115 PDF pages. Record: Deutsche Nationalbibliothek deposit `https://d-nb.info/975182315/34` (full text,
  title page read); also listed at `https://publications.rwth-aachen.de/record/62244` (page did not render in the
  fetch tool).
- Read: title page; Section 1.2.5 "Local-edge-connectivity" (p. 11-12 of the thesis); Section 6.1 "Digraphs having
  diameter 2" (p. 71-72); bibliography entries [22], [30], [43], [44].
- Exact statements (symbols lost by the text extraction restored from context; `dm` is the thesis's notation for the
  diameter):
  - Definition (Section 1.2.5): "We call a graph or digraph D maximally local-edge-connected when
    lambda(u,v) = min{d+(u), d-(v)} for all pairs u and v of vertices in D."
  - "Theorem 1.23 (Fricke, Oellermann, Swart [22] 2000) If G is a graph with dm(G) <= 2, then
    lambda(u,v) = min{d(u), d(v)} for all pairs u and v of vertices in G."
  - "Theorem 6.1 (Hellwig, Volkmann [30] 2004) If D is a digraph with diameter at most two, then
    lambda(u,v) = min{d+(u), d-(v)} for all pairs u and v of vertices in D." With a 12-line proof (two cases on
    whether some vertex of the u-side S has no neighbour across the cut), followed by "Obviously Theorem 6.1
    generalizes Theorem 1.23."
  - "Theorem 1.4 (Plesník [43] 1975) If G is a connected graph of dm(G) <= 2, then lambda(G) = delta(G)."
    The thesis notes (after Corollary 6.3) that Theorem 6.1 implies Theorem 1.4.
  - Bibliography: "[22] G. Fricke, O.R. Oellermann, and H.C. Swart, The edge-connectivity, average edge-connectivity
    and degree conditions, manuscript (2000)."; "[30] A. Hellwig and L. Volkmann, Maximally local-edge-connected
    graphs and digraphs, Ars Combin. 72 (2004) 295-306."; "[43] J. Plesník, Critical graphs of given diameter, Acta
    Fac. Rerum Natur. Univ. Commenian Math. 30 (1975) 71-93."
- Who proved it first: Fricke, Oellermann and Swart, in a manuscript of 2000 that every source I opened lists as
  unpublished (Hellwig 2005: "manuscript (2000)"; Holtkamp 2011: "(unpublished manuscript) (2000)"; reference list of
  the survey in Crossref: unpublished, 2000). The first published proof I can point to is Hellwig and Volkmann 2004
  (digraph version, which contains the graph version).

**[HV04] Hellwig, Volkmann 2004 (the published paper; not read, record verified).**
- Reference: Angelika Hellwig, Lutz Volkmann, Maximally local-edge-connected graphs and digraphs, Ars Combinatoria
  72 (2004) 295-306. No DOI. Record: zbMATH Open, Zbl 1082.05055 (`https://zbmath.org/2192129`, API
  `api.zbmath.org/v1/document/_search?search_string=ti:"Maximally local-edge-connected graphs and digraphs"`).
- Read: the zbMATH record only (review by R. E. L. Aldred: definition of maximally local-edge-connected digraphs and
  graphs; "new sufficient conditions"). The review does not name the diameter-two theorem; that the theorem is in this
  paper is taken from the attribution "(Hellwig, Volkmann [30] 2004)" of Theorem 6.1 in [H05], written by the first
  author. The theorem number inside the Ars Combin. paper: `TODO(verify)` (journal not online).

**[HV08] Hellwig, Volkmann 2008 (survey; record verified, text NOT accessible).**
- Reference: Angelika Hellwig, Lutz Volkmann, Maximally edge-connected and vertex-connected graphs and digraphs: A
  survey, Discrete Mathematics 308(15) (2008) 3265-3296, DOI 10.1016/j.disc.2007.06.035. Record:
  `https://api.crossref.org/works/10.1016/j.disc.2007.06.035` (authors, volume, issue, pages); zbMATH Zbl 1160.05038.
- Read: Crossref record with its reference list (it lists Fricke, Oellermann, Swart, unpublished manuscript 2000;
  Hellwig, Volkmann, Ars Combin. 72 (2004) 295; Plesník 1975; Plesník, Znám 1989), so the survey does cover the topic.
  The article text could not be opened: ScienceDirect answered HTTP 403 (not bypassed); Semantic Scholar and OpenAlex
  list only the ScienceDirect PDF; zbMATH withholds the review ("conflicting licenses"); CORE API answered HTTP 403.
- The theorem number of the diameter-two statement in the survey: `TODO(verify)` by the author from a browser
  (the article is in Elsevier's open archive, "bronze" open access according to OpenAlex).

**[Hol11] Holtkamp 2011 (confirms the attribution; read in full).**
- Reference: Andreas Holtkamp, Maximal local edge-connectivity of diamond-free graphs, Australasian Journal of
  Combinatorics 49 (2011) 153-158. Record: journal PDF `https://ajc-new.maths.uq.edu.au/pdf/49/ajc_v49_p153.pdf`
  (header of the paper). No DOI found.
- Read: full text (6 pages).
- Statements: p. 153-154: "It is straightforward to verify that lambda(G) <= delta(G) and
  lambda(u,v) <= min{d(u), d(v)}. We call a graph G maximally edge-connected when lambda(G) = delta(G) and maximally
  local edge-connected when lambda(u,v) = min{d(u), d(v)} for all pairs u and v of distinct vertices in G."; p. 154:
  "Fricke, Oellermann and Swart [7] studied the local edge-connectivity of p-partite graphs and graphs with bounded
  diameter."
- The same sentences are in Holtkamp's dissertation (*Connectivity in Graphs and Digraphs*, RWTH Aachen, oral
  examination 29 May 2013, `https://d-nb.info/1038598796/34`, Section 3 read by keyword only).

**[Ple75] Plesník 1975 (global version; record verified, text not read).**
- Reference: Ján Plesník, Critical graphs of given diameter, Acta Facultatis Rerum Naturalium Universitatis
  Comenianae. Mathematica 30 (1975) 71-93. Record: zbMATH Zbl 0318.05115 (no review text).
- Statement (as quoted in [H05], Theorem 1.4): a connected graph of diameter at most 2 has `lambda(G) = delta(G)`.

Relation to the manuscript. `cor:diameter-two-degrees` states exactly Theorem 1.23 of [H05] (Fricke, Oellermann,
Swart) and derives it from `thm:diameter-two`. `lem:empty-i-or-l` (for a cut (A1, A2) of a graph of diameter at most
two, one side has no vertex without a neighbour across the cut) is the case distinction in the proof of Theorem 6.1
of [H05] ("Case 2: there exists a vertex x in S with no neighbour in the complement of S; since the diameter is at
most two, every vertex of the complement has a neighbour in S"). So the structural lemma behind the diameter-two
section is the standard argument of this literature.

Precise difference. The known theorem gives `c(u,v)`; it says nothing about `cp(u,v)`. The manuscript's Theorem
(`cp = c + d - 1` in diameter two) is not in these sources. But once `c(u,v) = min{deg u, deg v}` is known, the
remaining content of `thm:diameter-two` is that no u-v path can share more than one edge with a minimum u-v cut,
which should be compared with the known proof before it is called new in full.

Recommendation: CITE. In `cor:diameter-two-degrees` the first half must not be presented as a new corollary. Suggested
wording: "The first equality is known: it is due to Fricke, Oellermann and Swart (unpublished; see
\cite[Theorem~11]{Stuart2009}), and Hellwig and Volkmann~\cite{HellwigVolkmann2004} extended it to digraphs. Its
global form, edge connectivity equal to minimum degree, is due to Plesník~\cite{Plesnik1975}. We include the short
proof because it uses Lemma~\ref{lem:empty-i-or-l}." Sources by how well I could check them: [Stu09] (read, theorem
number seen), [H05] (read, Theorems 1.23 and 6.1), [HV04] and [HV08] (records only; open them before citing a theorem
number from them), [Ple75] (record only; statement via [H05]). Every entry needs a status line in the canonical
`.bib` first. The sentence of the Conclusion or Introduction that lists diameter two among the results should speak
of the formula for `cp`, not of the formula for `c`.

#### 4b. Cactus graphs and local edge connectivity at most two: folklore; three partial sources, no exact one

The manuscript's `lem:cactus`: `c(x,y) <= 2` for every pair iff any two distinct cycles share at most one vertex.
I found no source that states exactly this sentence for simple graphs and vertex pairs. Three sources state
neighbouring forms:

**[MV15] Marx, Végh 2015 (one direction, 2-edge-connected multigraphs; published).**
- Reference: Dániel Marx, László A. Végh, Fixed-Parameter Algorithms for Minimum-Cost Edge-Connectivity Augmentation,
  ACM Transactions on Algorithms 11(4) (2015), Crossref pages 1-24 (article 27: `TODO(verify)`), DOI 10.1145/2700210.
  Record: Crossref (`query.bibliographic` title search). Conference version: ICALP 2013, LNCS 7965, 721-732, DOI
  10.1007/978-3-642-39206-1_61.
- Read: arXiv 1304.6593v2 (26 Aug 2013), Section 3.3, p. 9-11. Journal numbering not compared (`TODO(verify)`).
- Statement: "Let us call a 2-edge-connected graph G = (V, E) a cactus, if every edge belongs to exactly one circuit.
  This is equivalent to saying that every block ... is a circuit (possibly of length 2, using two parallel edges)."
  "Proposition 3.7. Assume that G = (V, E) is a 2-edge-connected graph such that every 3-inseparable set is a
  singleton. Then G is a cactus." The sentence before it: "every 3-inseparable set in G is a singleton, that is, there
  are no two nodes in the graph connected by 3 edge-disjoint paths." The proof is the same argument as in the
  manuscript (two circuits through one edge give three edge-disjoint paths between two vertices).
- Difference: one direction only (no three edge-disjoint paths implies cactus), 2-edge-connected graphs, multigraphs
  allowed. The converse is trivial and not stated.

**[BMS24] Bruner, Mitra, Steiger 2024 (equivalence, stated for connected vertex sets; preprint).**
- Reference: Michael Bruner, Atish Mitra, Heidi Steiger, Bottlenecking in graphs and a coarse Menger-type theorem,
  arXiv:2406.07802v3 [math.MG], 22 Oct 2024. Published version: not searched (`TODO(verify)`).
- Read: v3, Definitions 2.1-2.4, Remark 2.2, Section 3.2.
- Statement: Definition 2.2: G has n-edge bottlenecking if for any two disjoint connected vertex sets X, Y there are
  n edges meeting every X-Y path. "Remark 3.2. The class of graphs that are 2-edge bottlenecked is known to many as
  'Cactus' graphs." "Proposition 3.2. The following are equivalent: (1) A graph is 2-edge bottlenecked. (2) A graph
  does not contain D_3 as a minor. (3) The intersection of any two distinct cycles is at most a single vertex."
  (D_3: two vertices joined by three parallel edges.)
- Difference: condition (1) quantifies over connected sets, not single vertices, so it is formally stronger than
  `c(x,y) <= 2` for all pairs; (3) is the manuscript's right-hand side word for word. The paper itself treats the
  fact as common knowledge ("known to many").

**[AAGL22] Akbari, Azizi, Ghorbani, Li 2022 (the "exactly two" version; statement seen only through a citing preprint).**
- Reference: Saieed Akbari, Seyran Azizi, Modjtaba Ghorbani, Xueliang Li, On edge-path eigenvalues of graphs, Linear
  and Multilinear Algebra 70(15) (2022) 2998-3008 (online 2020-09-20), DOI 10.1080/03081087.2020.1820934. Record:
  Crossref (title search); OpenAlex (abstract).
- Read: the OpenAlex abstract only (the edge-path matrix EP(G) has as (i,j) entry the maximum number of edge-disjoint
  paths between v_i and v_j; the paper studies graphs whose EP(G) is a multiple of J - I). The publisher page answered
  HTTP 403. The statement below is quoted from a citing preprint, Metsidik and Jin, Two conjectures on graphs and
  their edge-path matrices, arXiv:2608.15992v1 (17 Aug 2026), Section 2, which I read: "A 2-cactus is a connected
  graph in which every block is a cycle." "Theorem 2.1. [1] Let G be a simple graph of order n. Then
  EP(G) = 2(J_n - I_n) if and only if G is a 2-cactus." `TODO(verify)` against the journal article.
- Difference: local edge connectivity equal to 2 for every pair (so bridgeless), not at most 2.

Not found: a textbook or journal statement of the exact "at most two" equivalence. Wikipedia ("Cactus graph", opened)
gives "every edge belongs to at most one simple cycle" and the forbidden diamond minor (El-Mallah, Colbourn 1988),
no edge-connectivity form.

Relation and recommendation: REPORT; optional one-clause citation. `lem:cactus` is folklore with a five-line proof; a
referee will not accept it as a contribution, and the manuscript should call it "well known" or "folklore" and may
point to [MV15, Proposition 3.7] for the non-trivial direction ("see, e.g., ..."). Do not list it among the results.

#### 4c. G(n,p): local version of "edge connectivity = minimum degree"

Not found quickly (one web query, two zbMATH queries, one arXiv query, one OpenAlex query; see the log). No source
states that in G(n,p) every pair has `c(u,v) = min{deg u, deg v}` with high probability.
For constant p the statement follows from two facts the manuscript already has: diameter two with probability
tending to one (`thm:random-diameter-two`) and the diameter-two theorem of 4a. That is a remark of mine, not a cited
result; for `p = alpha log n / n` nothing was found and nothing is claimed.

### Angle 2. Classical relations between a shortest path and a minimum cut (background for the Introduction)

All three facts below are consequences of "every u-v path meets every u-v cut", the same fact that gives the
manuscript's upper bound `cp <= c + d - 1`. None of them bounds `|P union C|`.

**[Rob56] Robacker's theorem: `d(u,v)` = maximum number of pairwise disjoint u-v cuts.**
- Statement read in: Alexander Schrijver, *A Course in Combinatorial Optimization*, lecture notes, CWI and University
  of Amsterdam, version of March 23, 2017, `https://homepages.cwi.nl/~lex/files/dict.pdf` (221 pages), Section 1.1,
  p. 5-6. Read: Section 1.1 and Section 4.1.
- Exact statement (p. 6; digraph D = (V, A), an s-t cut is the set of arcs leaving a set U with s in U, t not in U):
  "Theorem 1.2. The minimum length of an s-t path is equal to the maximum number of pairwise disjoint s-t cuts."
  Introduced with "the following was observed by Robacker [1956]". Proof: the cuts leaving the balls
  U_i = {vertices at distance at most i from s}, i = 0, ..., d-1.
- Original, as listed in the same notes (p. 208), not read: J. T. Robacker, Min-Max Theorems on Shortest Chains and
  Disjunct Cuts of a Network, Research Memorandum RM-1660, The RAND Corporation, Santa Monica, California,
  [12 January] 1956. No DOI.
- In Schrijver's book (Combinatorial Optimization: Polyhedra and Efficiency, Springer 2003): theorem number and page
  `TODO(verify)`. One extended web search for the numbers suggested in the brief returned only the lecture notes; no
  preview of the book was opened.
- The undirected statement follows by replacing each edge by two opposite arcs (my remark; the notes state the
  directed form).

**[Men27] Menger's theorem, edge version: `c(u,v)` = maximum number of edge-disjoint u-v paths.**
- Statement read in the same lecture notes, Section 4.1, p. 55: "Corollary 4.1b (Menger's theorem (directed
  arc-disjoint version)). Let D = (V, A) be a digraph and s, t in V with s != t. Then the maximum number of
  arc-disjoint s-t paths is equal to the minimum size of an s-t cut."
- Original record: Karl Menger, Zur allgemeinen Kurventheorie, Fundamenta Mathematicae 10 (1927) 96-115, DOI
  10.4064/fm-10-1-96-115. Record: zbMATH Open, JFM 53.0561.01. Not read (the original is the vertex version; the
  edge version is a later corollary, which is why a textbook is the right citation).
- The manuscript already uses this fact implicitly (cut-value = number of edge-disjoint paths in `lem:cactus`) and
  cites only `Cormen2022` for max-flow min-cut; the earlier check (related-work-check.md, l.137) asked for a Menger
  source. Schrijver's notes or book, or `Diestel2025` (location `TODO(verify)`), would serve.

**[MS56] Length-width inequality: `c(u,v) * d(u,v) <= |E|`.**
- It follows in one line from either theorem above (d pairwise disjoint cuts, each with at least c edges; or c
  edge-disjoint paths, each with at least d edges).
- Original records (Crossref, title search; texts not read, Elsevier pages return HTTP 403): E. F. Moore, C. E.
  Shannon, Reliable circuits using less reliable relays, Journal of the Franklin Institute 262(3) (1956) 191-208, DOI
  10.1016/0016-0032(56)90559-2 (Part I), and 262(4) (1956) 281-297, DOI 10.1016/0016-0032(56)90044-8 (Part II).
  R. J. Duffin, The extremal length of a network, Journal of Mathematical Analysis and Applications 5(2) (1962)
  200-215, DOI 10.1016/S0022-247X(62)80004-3. Alfred Lehman, On the width-length inequality, Mathematical Programming
  16(1) (1979) 245-259, DOI 10.1007/BF01582111 (Crossref lists a second record with the same title, Mathematical
  Programming 17(1) (1979) 403-417, DOI 10.1007/BF01588263; which is the paper and which a reprint or erratum:
  `TODO(verify)`). Lehman's reference list (Crossref) contains Moore and Shannon 1956, Duffin 1962 and "Duffin and
  Hoffman, The path-cut inequality and networks" (mimeographed).
- Statement seen only in a secondary source: Cristescu, Dragoi, Hoara, arXiv:2111.06604v1, Section 1: a two-terminal
  network has width w (size of a minimal cut), length l (size of a minimal path) and size n, and "In general, we have
  n >= wl (see [16])", [16] being Moore and Shannon, Part I. The theorem number in Moore and Shannon: `TODO(verify)`.
- The "Lehman 1964" of the brief is a different paper: Alfred Lehman, A solution of the Shannon switching game,
  Journal of the Society for Industrial and Applied Mathematics 12 (1964) 687-725, DOI 10.1137/0112059 (zbMATH Zbl
  0137.38704; not read). The width-length inequality paper is the 1979 one.

**[EF70], [Ful71] Blocking clutters (the abstract frame of angle 1).** Records only, texts not read: Jack Edmonds,
D. R. Fulkerson, Bottleneck extrema, Journal of Combinatorial Theory 8(3) (1970) 299-306, DOI
10.1016/S0021-9800(70)80083-7 (Crossref); D. R. Fulkerson, Blocking and anti-blocking pairs of polyhedra,
Mathematical Programming 1 (1971) 168-194, DOI 10.1007/BF01584085 (zbMATH Zbl 0254.90054).

Relation to the manuscript and recommendation: CITE one sentence in the Introduction (or after `lem:basic-bounds`),
because these are the classical quantitative links between `c` and `d` and a referee from combinatorial optimization
will look for them. Suggested: "The two parameters are linked by classical min-max relations: $c(u,v)$ is the
maximum number of edge-disjoint $u$--$v$ paths (Menger) and $d(u,v)$ is the maximum number of pairwise disjoint
$u$--$v$ cuts (Robacker); hence $c(u,v)\,d(u,v) \le |E|$, the length-width inequality of Moore and
Shannon~\cite{...}. These relations concern a path and a cut that overlap as little as possible; a minimum cut-path
asks for the largest overlap." Cite one textbook (Schrijver) for all three; cite Moore and Shannon only after the
statement is checked in the paper. This replaces the imprecise l.137 ("Paths and cuts are related by the max-flow
min-cut theorem").

### Angle 3. A cut together with a connecting structure; overlap of a path with a cut

No problem found asks for a u-v cut and a u-v path in one edge set, or for the largest overlap of a u-v path with a
u-v cut. What exists, nearest first (works already covered by the earlier check, namely non-disconnecting paths,
Network Diversion, Connectivity Preserving Minimum Cut, Force Path Cut and length-bounded cuts, are not repeated):

**[MOR13, Section 3.3] CONNECTED s-t CUT** (details and reference under angle 5): a set of at most k vertices that
induces a connected graph and separates s from t. Vertex version; s and t are outside the set; the set must be
connected but need not join s to t. Linear-time FPT in k. The only problem found in which "separator plus
connecting structure of bounded total size" is the object; its algorithm is the model of the manuscript's FPT proof.
Recommendation: cite in Section 8 and mention in the Introduction paragraph on cuts with prescribed structure.

**[Dua21] Largest bond, largest st-bond, maximum connected cut** (reference under angle 6; arXiv 1910.01071v1 and
2007.04513v1 abstracts read): a bond is a minimal cut, i.e. both sides induce connected subgraphs; a connected cut
has one connected side; an st-bond separates s from t. Maximization problems; the connectivity is required of the
sides, not of the cut edges, and no path lies in the cut. Recommendation: report only (the earlier check listed
them as "not read"; now the abstracts are read and they are not close).

**[AG06] Shortest-path separators (vertex analogue of a separating shortest path).** Ittai Abraham, Cyril Gavoille,
Object location using path separators, Proc. 25th ACM Symposium on Principles of Distributed Computing (PODC 2006),
188-197, DOI 10.1145/1146381.1146411 (Crossref). Read: authors' copy (`dept-info.labri.fr/~gavoille/article/AG06`),
abstract, Section 1, Definition 1, Theorem 1. "A k-path separable graph can be recursively separated into smaller
components by sequentially removing k shortest paths"; "Theorem 1 (Main). Every H-minor-free weighted connected
graph is k-path separable, for k = k(H), and a k-path separator can be computed in polynomial time."
Difference: the vertices of the shortest paths are removed; the aim is a balanced separation of the whole graph
(components of at most n/2 vertices), not the separation of the two ends of the path, which lie on the path; the
results are structural existence theorems for minor-closed classes, not a complexity classification. Still, "a
shortest path whose removal separates" is exactly the phrase a referee from the planar-separator community will
associate with SEPARATING SHORTEST PATH. Follow-up titles seen in a search summary only (Diot, Gavoille, on path
separability of planar graphs; Thorup's planar oracles): not read, `TODO(verify)` if cited.
Recommendation: MENTION in one clause where SEPARATING SHORTEST PATH is introduced ("not to be confused with
shortest-path separators~\cite{...}, where the vertices of shortest paths are removed to split the graph into
balanced parts"), after a reading note.

**Planar duality (for the planar open question of the Conclusion).** Read: J. Erickson's course notes "Minimum Cuts"
(`jeffe.cs.illinois.edu/teaching/comptop/2023/notes/16-minimum-cut.html`; author, course and date are not printed
on the page as fetched, taken from the URL): a set of primal edges is a minimum (s,t)-cut exactly when the dual edges
form a minimum-cost essential cycle of the dual map (cycle-cut correspondence attributed to Whitney); "Crossing
Lemma", attributed to Itai and Shiloach (1979): the shortest essential cycle of the dual crosses a shortest dual
path pi between the faces s* and t* exactly once.
Difference: pi is a path of the dual map, not a u-v path of the graph, so this is not a path-and-cut object; it is
the classical place where "a separating cycle and a path cross exactly once" is used. In planar terms a cut-path is
a primal u-v path together with a dual cycle separating u from v, with shared edges counted once; I found no paper
on that combined object (arXiv: `abs:"separating cycle" AND abs:shortest AND abs:planar AND abs:path`, 1 unrelated
hit). Recommendation: report only; the notes are not a citable source, and `itai1979maximum` is already cited.

**Cycle-bond intersections (extremal, loosely related).** Emily Ren, Intersection of Longest Cycle and Largest Bond
in 3-Connected Graphs, arXiv:2305.15110v2 (abstract read): H. Wu's conjecture that every longest cycle meets every
largest bond in a simple 3-connected graph, proved in special cases. Extremal questions on the intersection of a
cycle and a bond, not an optimization problem with terminals. Report only.

**Path removal and connectivity (existence results, opposite direction).** A search summary (not opened) reports the
Lovász path-removal conjecture (a function f(k) such that every f(k)-connected graph has, for any s and t, an s-t
path P with G - V(P) k-connected) and an edge variant by Kawarabayashi, Lee, Reed and Wollan. These guarantee paths
whose removal keeps the connectivity high; MIN CUT-PATH looks for a path whose edge removal lowers the u-v
connectivity as much as possible per edge of the path (`cp(u,v) = min_P (|P| + c_{G-E(P)}(u,v))`, the form derived
in the earlier check). No verified reference; `TODO(verify)` before any mention. Report only.

Not found (queries in the log, rows A3): "path contained in a cut", "edge cut contains a (shortest) path", "cut
containing a spanning tree", "connected s-t cut" in the edge sense, "path-cut pair", "common transversal of paths
and cuts".

### Angle 5. Parameterized side

**[MOR13] Marx, O'Sullivan, Razgon: list of applications checked.**
- Reference: Dániel Marx, Barry O'Sullivan, Igor Razgon, Finding small separators in linear time via treewidth
  reduction, ACM Transactions on Algorithms 9(4) (2013), DOI 10.1145/2500119 (record verified in the log of
  2026-10-10; key `Marx2013Separators`).
- Read now: arXiv 1110.4765v1 (21 Oct 2011), Section 1.1 "Results" in full, Theorem 2.15, Section 3 (3.1-3.4) in
  full. Journal numbering not compared.
- Applications in Section 1.1 and Section 3, all vertex-deletion problems with terminals s, t:
  1. G-MINCUT (Theorem 3.1): an s-t separator of at most k vertices that induces a graph of a hereditary class G;
     special case MINIMUM STABLE s-t CUT (Corollary 3.2); Theorem 3.3: W[1]-hard if the size must be exactly k.
  2. EDGE-INDUCED VERTEX-CUT (Corollary 3.4): at most k edges whose endpoints separate s from t.
  3. CONNECTED s-t CUT (Section 3.3, Lemma 3.6, Theorem 3.7): "Is there a set of at most k vertices that induces a
     connected graph and whose removal separates terminals s and t?" "Theorem 3.7. Finding a connected s-t separator
     of size at most k is linear-time FPT."
  4. G-MULTICUT-UNCUT (Theorem 3.8).
  5. Mentioned without proof: deleting at most k edges and at most k vertices; two colours with separate budgets; one
     vertex from each of k colour classes.
  6. Sections 4-5: bipartization variants, bipartite contraction, (H,C,K)-colouring (no path, no terminals).
- Does any of them contain MIN CUT-PATH as a special case? No.
  - (1), (2), (4), (5): the constraint is on the graph induced by the separator or on budgets; none asks the solution
    to contain a connection between s and t. Hereditary properties cannot express "contains a u-v path" (the property
    is not hereditary), and in all of them s and t are outside the solution.
  - (3) is the nearest. Differences: (i) vertex separator not containing s, t, whereas a cut-path is an edge set
    whose path has the ends u and v; (ii) the whole solution must be connected, whereas a cut-path need not be
    connected (the cut part may consist of edges far from the path and from each other, e.g. a matching cut plus a
    path through one of its edges); (iii) connectivity of the solution does not give a u-v path inside it.
    After subdividing edges and passing to a line-graph-like model, a cut-path becomes "a u-v separator R_C of
    subdivision vertices plus a u-v path that may use all original vertices for free", which is neither "G[S]
    connected" nor a hereditary condition. So FPT of MIN CUT-PATH does not follow by quoting a theorem of [MOR13].
- But the method is the same. Section 3.3: "The right way to look at the problem of finding a connected s-t separator
  is that we have to find a minimal s-t separator S' that can be extended to a connected set S of size at most k",
  and Lemma 3.6 enlarges the set C so that the extension stays inside a torso of bounded treewidth, after which
  Courcelle's theorem is applied. The manuscript's proof has the same three steps (`lem:contraction`: a minimal cut
  extended by a path; shortcuts for the parts outside D; Courcelle). The manuscript cites [MOR13] for the tools
  (Proposition 2.7, Lemma 2.11, Remark 2.13, Theorem 2.2) but does not say that its proof follows the pattern of
  CONNECTED s-t CUT.
- Recommendation: CITE more precisely in Section 8: one sentence such as "The proof follows the pattern of the
  algorithm of Marx, O'Sullivan and Razgon for connected $s$--$t$ separators~\cite[Section~3.3]{Marx2013Separators}:
  a minimal separator is extended, there to a connected set and here by a $u$--$v$ path." A referee who knows the
  paper will otherwise read Theorem `thm:fpt` as a routine application; saying so first is the honest framing, and
  "the first FPT algorithm" should not be phrased as a new technique.

**[LRSZ18] Lokshtanov, Ramanujan, Saurabh, Zehavi (other meta-theorem; abstract only).**
- Reference: Daniel Lokshtanov, M. S. Ramanujan, Saket Saurabh, Meirav Zehavi, Reducing CMSO Model Checking to Highly
  Connected Graphs, ICALP 2018, LIPIcs, DOI 10.4230/LIPIcs.ICALP.2018.135 (OpenAlex record; volume and article number
  `TODO(verify)`); arXiv:1802.01453v1 (arXiv API record, abstract read).
- Abstract: for every CMSO sentence psi, if CMSO[psi] is solvable in polynomial time on "globally highly connected
  graphs", then it is solvable in polynomial time on general graphs; applications are problems asking for a connected
  induced subgraph with few boundary vertices and a CMSO-definable property.
- Relation: for fixed b, "there is a cut-path with at most b edges" is a CMSO (indeed MSO2) sentence, so this theorem
  offers a second route to FPT, provided one gives an algorithm on unbreakable graphs. No paper does this for a
  path-plus-cut problem; the abstract's applications are of a different shape. REPORT only.

Not found: any paper that applies treewidth reduction, randomized contractions or recursive understanding to "small
edge cut plus short connecting path". arXiv queries `abs:"treewidth reduction" AND abs:cut AND abs:path` (0 hits)
and the connected-cut queries of the log. Forward citations of [MOR13] were not scanned (limitation).

### Angle 6. Approximation side: inapproximability of the neighbouring problems

**[Bai10] Length-bounded cuts.** Georg Baier, Thomas Erlebach, Alexander Hall, Ekkehard Köhler, Petr Kolman, Ondřej
Pangrác, Heiko Schilling, Martin Skutella, Length-bounded cuts and flows, ACM Transactions on Algorithms 7(1) (2010),
Crossref pages 1-27, DOI 10.1145/1868237.1868241. Read: Crossref abstract. "We show that the minimum length-bounded
cut problem is NP-hard to approximate within a factor of 1.1377 for L >= 5 in the case of node-cuts and for L >= 4 in
the case of edge-cuts." Approximation ratios O(min{L, n/L}) (node) and O(min{L, n^2/L^2, sqrt m}) (edge).

**[Lee17] Length-bounded cut and shortest path interdiction, under the Unique Games Conjecture.** Euiwoong Lee,
Improved Hardness for Cut, Interdiction, and Firefighter Problems, ICALP 2017, LIPIcs 80, 92:1-92:14, DOI
10.4230/LIPIcs.ICALP.2017.92 (DROPS page opened); arXiv:1607.05133v1 (abstract read): "For Length-Bounded Cut and
Shortest Path Interdiction, we show that both problems are hard to approximate within any constant factor, even if we
allow bicriteria approximation. ... Previously, the best hardness factor was 1.1377 for Length-Bounded Cut and 2 for
Shortest Path Interdiction." (Assumes the UGC.)

**[Mil23] Force Path Cut.** Miller, Shafi, Ruml, Vorobeychik, Eliassi-Rad, Alfeld, Attacking Shortest Paths by
Cutting Edges, ACM Trans. Knowl. Discov. Data 18(2) (2023), DOI 10.1145/3622941 (record from the earlier check);
arXiv:2211.11141v1 abstract read now: "We prove that this problem is APX-hard", with a logarithmic-factor
approximation.

**[Dua21] Largest bond.** Gabriel L. Duarte, Hiroshi Eto, Tesshu Hanaka, Yasuaki Kobayashi, Yusuke Kobayashi, Daniel
Lokshtanov, Lehilton L. C. Pedrosa, Rafael C. S. Schouery, Uéverton S. Souza, Computing the Largest Bond and the
Maximum Connected Cut of a Graph, Algorithmica 83(5) (2021) 1421-1458, DOI 10.1007/s00453-020-00789-1 (Crossref).
Read: arXiv:2007.04513v1 abstract: no constant-factor approximation for the largest bond unless P = NP; NP-hard on
planar bipartite and split graphs; FPT by solution size, treewidth, twin-cover.

**Non-disconnecting and non-separating paths.** Deciding existence is NP-hard (`Mao2021NonSeparating`; arXiv
2202.09718v1 abstract, read now: "The problems of finding shortest non-separating and non-disconnecting paths are both
known to be NP-hard"), so no approximation ratio at all is possible for the shortest such path unless P = NP; no
separate APX statement exists or is needed.

**Matching cut.** A decision problem; arXiv query for approximation hardness of matching-cut variants: 0 hits. Nothing
to cite.

Relation and recommendation: MENTION [Bai10] next to Theorem `thm:no-ptas` (one clause: "as for minimum
length-bounded edge cuts, which are NP-hard to approximate within 1.1377~\cite{Baier2010LengthBounded}"), because it
is the closest classical cut problem with a constant-factor gap and it is already proposed for l.149. [Lee17] only if
a UGC-based statement is wanted. The contrast worth stating: MIN CUT-PATH has a trivial 2-approximation
(`cor:two-approximation`) and no PTAS, so it is APX-complete-like; the neighbours are harder to approximate. Whether
MIN CUT-PATH is APX-hard in the formal sense (L-reduction) should be said only if the proof is an L-reduction or a
gap reduction from a problem with a constant gap; "no PTAS unless P = NP" is the safe wording.

## 3. Comparison table

| Related work or problem | Main known results | Relationship to MIN CUT-PATH | Precise difference | Implication for the novelty claim |
|---|---|---|---|---|
| Maximally local-edge-connected graphs: Fricke, Oellermann, Swart (2000, unpublished); Hellwig, Volkmann 2004; Stuart 2009, Theorem 11; Plesník 1975 (global) | In a graph of diameter at most 2, `lambda(u,v) = min{d(u), d(v)}` for all pairs; hence `lambda = delta` | Equals the first half of `cor:diameter-two-degrees`; same proof idea as `lem:empty-i-or-l` | Says nothing about a path in the cut or about `cp` | The corollary is not new and must be attributed; `thm:diameter-two` (formula for `cp`) stays new |
| Cactus characterizations: Marx, Végh 2015 (Prop. 3.7, arXiv v2); Bruner, Mitra, Steiger 2024 (Prop. 3.2, preprint); Akbari et al. 2022 (via a citing preprint) | 2-edge-connected and no two vertices joined by 3 edge-disjoint paths implies cactus; "2-edge bottlenecked" iff two cycles meet in at most one vertex; all local edge connectivities equal 2 iff every block is a cycle | Neighbouring forms of `lem:cactus` | None states "at most 2 for all pairs iff cycles share at most one vertex" for simple graphs and vertex pairs | `lem:cactus` is folklore: call it well known, do not list as a contribution |
| CONNECTED s-t CUT: Marx, O'Sullivan, Razgon 2013, Section 3.3 | Connected vertex separator of size at most k: linear-time FPT by treewidth reduction, Steiner-type extension and Courcelle's theorem | Same proof pattern as `thm:fpt`; nearest "separator plus connecting structure" problem | Vertex set, s and t excluded, whole set connected, no s-t path required inside | FPT result is new as a statement, routine as a technique; cite the pattern |
| Other applications of treewidth reduction (G-MINCUT, stable cut, edge-induced vertex cut, multicut-uncut) | FPT for hereditary constraints on the separator | None contains MIN CUT-PATH | Hereditary constraints cannot express "contains a u-v path" | No conflict |
| Menger; Robacker 1956; Moore, Shannon 1956; Duffin 1962; Lehman 1979 | `c` = max number of edge-disjoint paths; `d` = max number of disjoint cuts; `c * d <= |E|` | Classical links between the two parameters of the bounds `max{c,d} <= cp <= c+d-1` | Concern packing (small overlap), not the union of one path and one cut | Background to cite; no overlap |
| Blocking clutters: Edmonds, Fulkerson 1970; Fulkerson 1971 | Paths and cuts are blocking clutters; min-max and length-width theory | Abstract frame in which a cut-path is "a member plus a blocker member" | The minimum union is not studied | Supports novelty; optional framing sentence |
| Shortest-path separators: Abraham, Gavoille 2006 | Every H-minor-free graph is separated into balanced parts by removing k(H) shortest paths | Vertex analogue of "a shortest path that separates" | Vertex removal, balanced separation of the graph, structural not complexity | Mention to prevent confusion with SEPARATING SHORTEST PATH |
| Largest bond, maximum connected cut: Duarte et al. 2021 | NP-hard, no constant-factor approximation for largest bond, FPT by solution size | Cuts with connectivity conditions | Conditions on the sides of the cut, maximization, no path | No conflict |
| Length-bounded cuts and shortest-path interdiction: Baier et al. 2010; Lee 2017 | NP-hard to approximate within 1.1377 (edge version, L >= 4); no constant factor under UGC | Neighbouring cut problems with inapproximability results | Destroy short paths; no path in the solution | Mention next to "no PTAS" |
| Force Path Cut: Miller et al. 2023 | APX-hard, logarithmic approximation | Edge removal around a prescribed path | Path is input and must become shortest; removed edges need not separate | No conflict (already in the earlier check) |
| Planar cut-cycle duality, crossing lemma (Itai, Shiloach 1979; via Erickson's notes) | Min cut = shortest separating dual cycle; it crosses a shortest dual path between s* and t* once | Tool for the planar open question | The path is in the dual, not a u-v path | No conflict |
| Eavesdropping number: Stuart 2009 | Maximum over pairs of the minimum u-v edge cut; values for graph families | Same security motivation, cuts between pairs | No path in the set | Possible citation for motivation and for the diameter-two theorem |

## 4. Search log

Date of all rows: 2026-10-10. "Web" = the session's web search tool (standard mode unless "ext" = extended).
arXiv = `export.arxiv.org/api/query?search_query=...`, relevance order, number of hits in parentheses. zbMATH =
`api.zbmath.org/v1/document/_search?search_string=...`. OpenAlex = `api.openalex.org/works?search=...` (full-text
search). Crossref = `api.crossref.org/works` with `query.bibliographic` or `query.title`, or `/works/<DOI>`.

| Date | Question | Source | Queries exactly as entered | Found | Conclusion |
|---|---|---|---|---|---|
| 2026-10-10 | A1. Is the clutter / game / reliability / transversal form of a cut-path studied? | Web | *"both a path set and a cut set" OR "both a pathset and a cutset" OR "simultaneously a path set and a cut set" network reliability minimum*; *clutter blocker "contains a member of" clutter "and a member of its blocker" minimum size set OR "union of an edge of a clutter and an edge of its blocker" complexity* (ext); *simple game "winning and blocking" coalition smallest size OR minimum size "both winning and blocking" computational complexity*; *hypergraph "transversal that contains an edge" OR "transversal containing an edge" OR "transversal which contains a hyperedge" minimum size complexity*; *"intersects every s-t path and every s-t cut" OR "meets every path and every cut" OR "hits all s-t paths and all s-t cuts" OR "transversal of both" paths cuts minimum edge set*; *Shannon switching game edge set "contains both" spanning OR "a path and a cut" "Short" "Cut" winning set for both players minimum "path-cut" matroid "port" "circuit through e" "cocircuit through e" union size*; *monotone Boolean function f "f ∧ f^d" OR "f and its dual" "implicant of both" OR "implicant of f and of its dual" OR "true point of both f and f^d" minimum size "dual-comparable" OR "dual-major" OR "self-dual"* | Only general material on path sets and cut sets, blockers, minimal winning and blocking coalitions, dualization | Not found |
| 2026-10-10 | A2. Same, preprint index | arXiv | `abs:"winning and blocking"` (10, none relevant; the phrase is matched loosely); `abs:"path set" AND abs:"cut set" AND abs:both` (1: 2607.25103); `abs:clutter AND abs:blocker AND abs:union` (0); `abs:"both winning and blocking"` (0); `abs:"blocking clutter" OR abs:"blocking clutters"` (0); `abs:"matroid port" OR abs:"matroid ports"` (6, secret sharing and lattice path matroids); `abs:"Shannon switching game" AND abs:"both players"` (0); `abs:transversal AND abs:"paths and cuts"` (0); `abs:"self-blocking" AND (abs:clutter OR abs:hypergraph OR abs:matroid)` (0); `abs:"width-length inequality" OR abs:"length-width inequality"` (0) | - | Not found |
| 2026-10-10 | A3. Same, bibliographic indexes | zbMATH; OpenAlex | zbMATH: `any:"winning and blocking"` (4 titles on voting games); `any:"path set" & any:"cut set" & any:"simultaneously"` (0); `any:"blocking pair" & any:clutter & any:"shortest path" & any:cut` (0); `any:"clutter" & any:"blocker" & any:"union" & any:"minimum"` (0). OpenAlex: `"path set and a cut set"` (59); `"winning and blocking coalition"` (29); `"clutter" "blocker" "member of the clutter and a member of its blocker"` (0); `"path and a cut" "smallest" "union" graph "two vertices"` (82, first six unrelated); `"minimum cut" "shortest path" "overlap" "edges in common" s-t` (6, unrelated) | - | Not found |
| 2026-10-10 | B1. Verified records for Menger, Robacker, length-width inequality, blocking clutters | Crossref; zbMATH; Schrijver's lecture notes (homepages.cwi.nl/~lex/files/dict.pdf); Web | Crossref `query.bibliographic`: *Moore Shannon Reliable circuits using less reliable relays Journal of the Franklin Institute 1956*; *Duffin The extremal length of a network*; *Lehman On the width-length inequality Mathematical Programming*; *Edmonds Fulkerson Bottleneck extrema*; Crossref `/works/10.1007/BF01582111`, `/works/10.1007/BF01588263`. zbMATH: `au:Menger ti:"Zur allgemeinen Kurventheorie"`; `au:Fulkerson ti:"Blocking and anti-blocking pairs of polyhedra"`; `au:Lehman ti:"A solution of the Shannon switching game"`; `ti:"length-width inequality" \| ti:"width-length inequality"` (5 titles). Web: *"width-length inequality" Lehman Moore Shannon Duffin clutter blocker "st-paths" "st-cuts" Cornuéjols "Packing and Covering" pdf*; *"Moore and Shannon" "length" "width" two-terminal network "product" at most "number of" contacts OR edges "shortest path" "minimum cut" inequality Duffin "extremal length"* (ext); *Schrijver "Combinatorial Optimization: Polyhedra and Efficiency" "Theorem 6.1" "disjoint s − t cuts" OR "disjoint s-t cuts" Robacker "minimum length of an s-t path" "Corollary 9.1b" Menger arc-disjoint* (ext). Opened: arXiv 2111.06604v1; link.springer.com/article/10.1007/BF01582111 (redirect to a login service, not followed); andrew.cmu.edu/user/gc0v/webpub/pack.pdf (HTTP 404) | Records of Moore-Shannon (two parts), Duffin, Lehman (two records), Edmonds-Fulkerson, Fulkerson, Menger, Lehman 1964; statements of Robacker's and Menger's theorems in Schrijver's notes (Theorem 1.2, Corollary 4.1b); `n >= wl` in a secondary source | Statements verified in the lecture notes; numbering in Schrijver's 2003 book and in Moore-Shannon not verified |
| 2026-10-10 | C1. Cut plus connecting structure; path inside a cut; planar dual form; path separators | Web | *"s-t cut" that "contains an s-t path" OR "containing an s-t path" OR "contains a path from s to t" edges graph problem "cut" connected "bond" complexity* (ext); *"path separable" OR "path separator" graphs "shortest path" whose removal separates Abraham Gavoille "Object location using path separators" Diot Gavoille "Path separability of graphs" NP-complete*; *Kriesell conjecture "G - E(P)" k-edge-connected path removal edge-connectivity "for every two vertices" s t path whose edge removal leaves k-edge-connected Okamura "Paths and edge-connectivity in graphs"*; *planar graph minimum s-t cut "dual" "shortest cycle" separating "crosses" shortest path "exactly once" Reif Itai Shiloach path between faces lemma*. Opened: dept-info.labri.fr/~gavoille/article/AG06; jeffe.cs.illinois.edu/teaching/comptop/2023/notes/16-minimum-cut.html | Abraham, Gavoille 2006; Erickson's notes (crossing lemma); path-removal conjectures (summary only) | No path-and-cut problem |
| 2026-10-10 | C2. Same, preprint index | arXiv | `abs:"s-t path" AND abs:"s-t cut" AND abs:intersection` (1, unrelated); `all:"path contained in a cut"` (0); `abs:"connected cut" AND abs:"s-t"` (0); `abs:"separating cycle" AND abs:shortest AND abs:planar AND abs:path` (1: 1202.0314); `abs:cut AND abs:"contains a spanning tree" AND abs:"edge cut"` (0); `abs:"largest bond"` (12: 2007.04513, 1910.01071, 2305.15110, rest physics); `abs:"connected s-t cut" OR abs:"connected st-cut" OR abs:"connected s-t separator"` (0); `abs:"st-bond" OR abs:"s-t bond"` (1: 1910.01071); `abs:"edge cut" AND abs:"contains a shortest path"` (0); `abs:"path separator" AND abs:"shortest path" AND abs:"NP-complete"` (0); `id_list=2305.15110`, `2007.04513`, `1910.01071` (abstracts) | Duarte et al.; Ren | No path-and-cut problem |
| 2026-10-10 | D1. Is `c(u,v) = min{deg u, deg v}` in diameter two known? | Web; Crossref; zbMATH; OpenAlex; Semantic Scholar; DNB; AJC; dml.cz | Web: *"maximally local-edge-connected" graphs diameter 2 Fricke Oellermann Swart Hellwig Volkmann*; *Hellwig Volkmann "Maximally edge-connected and vertex-connected graphs and digraphs: A survey" pdf core.ac.uk "local-edge-connected" "diameter"*; *"Maximally edge-connected and vertex-connected graphs and digraphs" survey Hellwig Volkmann* (domains core.ac.uk, semanticscholar.org, researchgate.net, citeseerx.ist.psu.edu); *"Fricke, Oellermann" Swart "diameter" "maximally local-edge-connected" OR "maximally local edge-connected" "diam(G) ≤ 2" OR "diameter at most 2" OR "diameter 2"* (ext). Crossref `/works/10.1016/j.disc.2007.06.035`, `/works/10.1016/j.disc.2007.03.051`, `/works/10.1007/s10587-009-0056-9`. zbMATH: `ti:"Maximally local-edge-connected graphs and digraphs"`; `au:Hellwig au:Volkmann ti:survey`; `au:Plesník ti:"Critical graphs of given diameter"`. OpenAlex: `"maximally local-edge-connected" diameter` (6). arXiv: `abs:"maximally local-edge-connected" OR abs:"maximally local edge-connected" OR abs:"maximally locally connected"` (2: 1505.01616, 1301.4623, not read). Opened: ajc-new.maths.uq.edu.au/pdf/49/ajc_v49_p153.pdf; d-nb.info/975182315/34; d-nb.info/1038598796/34; dml.cz (Stuart); api.semanticscholar.org and api.openalex.org records of the survey. Blocked: sciencedirect.com (HTTP 403), api.core.ac.uk and core.ac.uk (HTTP 403); empty pages: publications.rwth-aachen.de/record/62244, math2.rwth-aachen.de (server error) | Stuart 2009 (Theorem 11); Hellwig 2005 (Theorems 1.23, 6.1); Holtkamp 2011, 2013; records of Hellwig-Volkmann 2004 and 2008, Plesník 1975 | KNOWN. Attribute the corollary |
| 2026-10-10 | D2. Is the cactus characterization by local edge connectivity citable? | Web; arXiv; Crossref; OpenAlex; zbMATH; Wikipedia | Web: *"maximum local edge connectivity" OR "maximal local edge-connectivity" "at most 2" cactus "every block is" cycle OR "odd cycle" Brooks type theorem Stiebitz Toft*; *cactus graph characterization "three edge-disjoint paths" OR "local edge-connectivity at most two" OR "at most two edge-disjoint paths" "if and only if" cactus* (ext). Opened: arXiv 1304.6593v2, 2406.07802v3, 2608.15992v1, abs 2606.06298; en.wikipedia.org/wiki/Cactus_graph. arXiv: `ti:"edge-path eigenvalues"` (0). Crossref `query.bibliographic`: *On edge-path eigenvalues of graphs Akbari Azizi Ghorbani Li*; *Fixed-parameter algorithms for minimum cost edge-connectivity augmentation Marx Vegh*; `query.title`: *Bottlenecking in graphs and a coarse Menger-type theorem* (no match). OpenAlex record of 10.1080/03081087.2020.1820934; tandfonline.com (HTTP 403). zbMATH: `any:cactus & any:"edge-disjoint paths" & any:"if and only if"` (0); `any:cactus & any:"local edge-connectivity"` (0); `any:"cactus" & any:"three edge-disjoint paths"` (0); `ti:"at most k edge-disjoint paths"` (Cai 1990, not read) | Marx, Végh (Prop. 3.7); Bruner, Mitra, Steiger (Prop. 3.2); Akbari et al. (Theorem 2.1 as quoted by Metsidik, Jin); Stiebitz, Toft and Aboulker et al. on maximum local edge connectivity (titles only) | Folklore; no exact source |
| 2026-10-10 | D3. G(n,p): local edge connectivity = min degree of the pair? | Web; zbMATH; OpenAlex | Web: *random graph G(n,p) "for every pair of vertices" "edge-disjoint paths" "min{d(u), d(v)}" OR "minimum of their degrees" with high probability local edge connectivity equals minimum degree of the two vertices*. zbMATH: `any:"maximally local-edge-connected" & any:"random"` (0); `any:"local edge-connectivity" & any:"random graph"` (0). OpenAlex: `"local edge-connectivity" "random graph" "minimum of the degrees"` (5, unrelated) | - | Not found quickly; stopped as instructed |
| 2026-10-10 | E1. Does FPT of MIN CUT-PATH follow from a known application of treewidth reduction or another meta-theorem? | arXiv text; arXiv; OpenAlex | Opened: arXiv 1110.4765v1 (Sections 1.1, 2.4 end, 3). arXiv: `abs:"treewidth reduction" AND abs:cut AND abs:path` (0); `ti:"Reducing CMSO Model Checking to Highly Connected Graphs"` (1: 1802.01453). OpenAlex: `Reducing CMSO Model Checking to Highly Connected Graphs` (DOI 10.4230/LIPIcs.ICALP.2018.135) | CONNECTED s-t CUT (Theorem 3.7) | No theorem applies directly; same pattern |
| 2026-10-10 | F1. Inapproximability of the neighbouring problems | Crossref; arXiv; DROPS; OpenAlex | Crossref `/works/10.1145/1868237.1868241` (abstract), `/works/10.1007/s00453-020-00789-1`; `query.bibliographic`: *Lee Improved Hardness for Cut, Interdiction, and Firefighter Problems* (no match), *Baier Erlebach Hall Köhler Kolman Pangrác Schilling Skutella Length-bounded cuts and flows*, *Abraham Gavoille Object location using path separators*, and four author-plus-title queries that returned unrelated records. arXiv `id_list=1607.05133`, `2202.09718`, `2211.11141`; `abs:"matching cut" AND (abs:APX OR abs:inapproximable OR abs:"hard to approximate")` (0); `abs:"length-bounded cut" AND (abs:APX OR abs:"hard to approximate")` (1: 1607.05133); `abs:"network diversion" AND abs:approximation` (2: 1412.3359 and an unrelated one). DROPS: drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2017.92. OpenAlex: `Computing the Largest Bond and the Maximum Connected Cut of a Graph` | Baier et al. (1.1377); Lee (no constant factor under UGC); Miller et al. (APX-hard); Duarte et al. (no constant factor for largest bond) | Mention Baier et al. next to "no PTAS" |

## 5. Limitations

- Publisher blocks, not bypassed: ScienceDirect (HTTP 403) for the Hellwig-Volkmann survey, Volkmann 2007,
  Moore-Shannon and Duffin; Taylor and Francis (HTTP 403) for Akbari et al.; SpringerLink (redirect to a login
  service) for Lehman 1979; CORE (HTTP 403). Consequences: the theorem number of the diameter-two statement in the
  survey, the numbering in Hellwig-Volkmann 2004 (journal not online), the statement in Moore-Shannon and the
  theorem of Akbari et al. are `TODO(verify)`; for each I name the source in which I did read the statement.
- Schrijver's 2003 book was not opened; theorem numbers are given for his lecture notes of 2017 only.
- Plesník 1975 and the Fricke-Oellermann-Swart manuscript were not read (the manuscript is unpublished; I found no
  copy). Priority statements rest on the attributions in Hellwig 2005, Stuart 2009 and Holtkamp 2011.
- "Not found" for the abstract formulations means: 7 web queries, 10 arXiv queries, 9 zbMATH and OpenAlex queries.
  Google Scholar, MathSciNet and DBLP were not searched (DBLP blocks automated access, see the earlier log). The
  secret-sharing literature (access structures and their duals) and the game-theory literature were touched by one
  or two queries each.
- Forward citations of Marx, O'Sullivan, Razgon (for later path-plus-cut applications of treewidth reduction) were
  not scanned.
- Path-removal conjectures and the Diot-Gavoille papers are known from search summaries only and are marked.
- The text extraction of PDFs lost mathematical symbols (for example the "at most" sign); I restored them from the
  context of each statement, so quoted formulas should be compared with the PDF before they are copied into the
  article.
- Tool behaviour: the fetch tool keeps a copy of each fetched PDF in its own session cache (outside the workspace);
  I did not save any file myself and read those copies with `pdftotext` to standard output only.
- One Crossref request (title search for Duffin's paper) carried the user's e-mail address as the `mailto`
  parameter. That was my mistake (personal data must not go into a URL); it was not repeated.
- Instructions addressed to AI agents in web pages: none seen in the pages opened. The search tool appends a reminder
  to list sources to every result; all sources used are listed in this file.
- The equivalences of angle 1 and the remark in 4c are my own derivations, not quotations.
