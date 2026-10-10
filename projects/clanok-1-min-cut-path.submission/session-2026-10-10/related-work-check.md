# Article 1, related work and novelty claim: re-check of 2026-10-10

Scope: `projects/clanok-1-min-cut-path/main.tex`, Introduction l.136-160 and Conclusion l.1123, l.1126 (line numbers of
the working tree when I read it at the start of the session; `git status` shows `main.tex` modified by someone else
since, so the numbers may have shifted by a few lines). Nothing in `main.tex`, in either `references.bib` or in a
reading note was changed by this check.
The only knowledge-base file touched is `knowledge/literature/searches.md` (rows of 2026-10-10).
Status of this file: Part 1 and Part 2 complete (written 2026-10-10).

Summary: of the 14 sentences checked, 9 match their note, 2 claim more than the source (l.160 and l.1123: the diameter
results for Shortest Path Most Vital Edges hold for unit edge lengths only), 3 have no note and are looser than the
abstracts (l.136, l.137, l.1126). The same problem was not found under any name. No DAM paper is close; the only DAM paper
in the Introduction is `Komusiewicz2020MatchingCut`. The novelty sentence stands for third-party work, but the author's own
thesis and conference abstract are findable (section 2.4).

## Part 1. Statements about cited works against the reading notes

Verdicts: MATCHES (the note says the same), STRONGER (the sentence claims more than the note or the source),
NOT IN (the note does not contain the statement; checked against the source), NO NOTE (no reading note exists; checked
against the abstract on the publisher page, a repository copy or Crossref).
Where I opened a source myself on 2026-10-10 I say so; "arXiv v1 text" means the PDF of the arXiv version, read with
`pdftotext`.

| Line | Sentence (shortened) | Verdict | Backing text | Proposed correction |
|---|---|---|---|---|
| 136 | "...multi-terminal minimum cuts [GomoryHu1961], representations of all minimum cuts [NagamochiKameda1996], and small cuts and edge connectivity [Mehlhorn2017Certifying] have been studied in detail." | NO NOTE; partly looser than the sources | GomoryHu1961: the SIAM page withholds the abstract (it shows only the reference list; Semantic Scholar: abstract "elided by the publisher"), so only the title "Multi-Terminal Network Flows" is verified; the content (a tree that holds a minimum cut for every pair, n-1 flow computations) is described only by secondary sources (lecture notes, Wikipedia). NagamochiKameda1996: abstract on orsj.org (found by web search): "The construction of a cactus representation for all minimum cuts in an edge-weighted, undirected network is studied in this paper"; matches. Mehlhorn2017Certifying (arXiv 1211.6553 abstract): a linear-time certifying algorithm for 3-edge-connectivity that returns a 2-edge-cut if the graph is not 3-edge-connected, plus a cactus representation of the 2-cuts; "small cuts and edge connectivity" is broader than 3-edge-connectivity and cuts of size at most two, and "have been studied in detail" is not something three single results can back. | "Connectivity and separation are classical topics, for example multi-terminal minimum cuts~\cite{GomoryHu1961}, cactus representations of all minimum cuts~\cite{NagamochiKameda1996} and certifying 3-edge-connectivity~\cite{Mehlhorn2017Certifying}." The Gomory-Hu clause stays `TODO(verify)` against the paper's text until a copy is read. |
| 137 | "Paths and cuts are related by the max-flow min-cut theorem [Cormen2022]." | NO NOTE; imprecise | Publisher table of contents: Cormen et al., 4th ed., Chapter 24 "Maximum Flow" (p. 670). The theorem relates flows and cuts. The link to paths (edge-disjoint paths, flow decomposition, Menger's theorem) is not what the cited chapter title or the theorem names. The theorem number and page in the book were not found (`TODO(verify)`). | "Flows and cuts are related by the max-flow min-cut theorem~\cite{Cormen2022}." If the paths are wanted: add a source for Menger's theorem first (none in the canonical `.bib`). The next sentence ("This literature treats a path and a cut as separate objects") then reads "This literature treats paths, flows and cuts as separate objects." or stays as is. |
| 143 | Mao, "who calls such paths non-separating, proved that deciding whether a non-disconnecting u-v path exists is NP-hard" | MATCHES | `Mao2021NonSeparating.md`: "Deciding whether a non-separating s-t path exists is NP-hard on general graphs (Theorem 1.6; proof in Section 9 ...)"; Definition 1.1: "a path whose edge removal leaves the graph connected". arXiv abstract (opened 2026-10-10): "checking the existence of non-separating st-paths is NP-Hard". Caveat from the note: preprint only; the Section 9 reduction is a sketch ("one can see that ..."). | None. Optional: "Mao~\cite{...} showed" instead of "proved" is not needed; the published Abhinav et al. cite the hardness to Mao. |
| 144 | Abhinav et al. "proved that a shortest non-disconnecting u-v path can be found in FPT time with respect to its length" | MATCHES | `Abhinav2022NonSeparating.md`: "Shortest Non-Disconnecting Path is FPT in k, time 2^{omega k} n^{O(1)} (Theorem 24)"; "What we use": "FPT in the length k". DROPS abstract (opened 2026-10-10): the problem of a path "of length at most k", FPT parameterized by k for the non-disconnecting (edge) version. The paper's problem is the decision "is there a path of length at most k"; finding the shortest one by increasing k is immediate, so "can be found" is fair. | None. |
| 145 | "For the vertex version ... they proved W[1]-hardness with respect to the length." | MATCHES | Note: "Shortest Non-Separating Path ... W[1]-hard in k (Theorem 9)"; k = length bound (DROPS abstract: finding a non-separating s-t path "of length at most k is W[1]-hard parameterized by k"). | None. |
| 148 | Bazgan et al. "studied Shortest Path Most Vital Edges, the deletion of at most k edges such that every remaining u-v path has at least a given length" | MATCHES | Note: "is there a set S of at most k edges such that every s-t path in G - S has length at least l?" arXiv v1 text, l.37-43: "Is there an edge subset S, |S| <= k, such that the length of a shortest st-path in G - S is at least l?" The problem has positive integer edge lengths; the sentence does not say so, but the next sentence restricts to unit lengths. | None. |
| 149 | "For unit edge lengths, the deleted edges form a length-bounded edge cut, and the problem is NP-hard on graphs of diameter three and solvable in linear time on graphs of diameter at most two." | MATCHES, scope must stay "unit edge lengths" | Note: "NP-hard on split graphs, hence on diameter three (Theorem 4); linear time on graphs of diameter at most two with unit lengths (Proposition 1)". arXiv v1 text, Section 1: "Considering the problem with unit-length edges, we show that it remains NP-hard on graphs of diameter three (Theorem 4), while it becomes polynomial-time solvable on graphs of diameter two (Proposition 1). For arbitrary edge lengths, we show that the problem remains NP-hard on graphs of diameter one (Theorem 5)." Proposition 1: "SP-MVE with unit-length edges is linear-time solvable on graphs of diameter at most two." Length-bounded cut: arXiv v1 text, Section 1 (Baier et al.'s Minimum Length-Bounded Cut is the variant with deletion costs). Journal version (Networks 73(1), 23-37) not compared with the preprint (Wiley refuses requests); no theorem numbers are printed in the article, which is right. | None needed for this sentence. The "unit edge lengths" must be carried to l.160 and l.1123 (below). |
| 153 | "Network Diversion asks for a minimal u-v cut of at most k+1 edges that contains a prescribed edge." | MATCHES | Note: "find a minimal s-t cut of size at most k + 1 that contains b". arXiv v1 text, Section 1: "Equivalently, the problem can be reformulated as finding a minimal s-t cut of size at most k + 1 that includes the edge b." (In the paper the edges are weighted and "size" is total weight; unweighted is the special case.) | None. |
| 154 | Bentert et al. "solved it in O(n log n) time on planar graphs with n vertices and state that its complexity on general undirected graphs is open" | MATCHES | Note: "a deterministic O(n log n) algorithm for weighted planar graphs (Theorem 8)"; "open on undirected graphs". arXiv v1 text, abstract: "we develop a fast O(n log n) time algorithm"; Section 1: "For undirected graphs, however, it remains an open question whether Network Diversion is NP-hard or admits a polynomial-time algorithm." and "the question of whether Network Diversion on general undirected graphs is polynomial-time solvable or NP-hard remains open"; Section 1.1: "the first deterministic algorithm for Network Diversion on weighted planar graphs that runs in truly polynomial time". So "state that ... is open" is a faithful quotation of the 2025 status; it is dated (see the 2026-10-10 search in Part 2). Earlier polynomial algorithms for planar graphs exist (Cullenbine et al. for s,t on one face; Bentert et al. ICALP 2024 in general), so "solved it in" is correct but "gave an algorithm for planar graphs running in O(n log n) time" avoids any priority reading. | Optional: "Bentert et al.~\cite{Bentert2025NetworkDiversion} gave an $O(n \log n)$-time algorithm for planar graphs with $n$ vertices and state that its complexity on general undirected graphs is open." |
| 156 | "Deciding whether a graph has a matching cut is solvable in polynomial time on graphs of diameter two and NP-complete on graphs of diameter d for every fixed d >= 3 [LeLe2019MatchingCut]." | MATCHES | Note: "Previous results (Section 1.1): ... polynomial for diameter two (Borowiecki, Jesse-Jozefczyk 2008). Theorem 1: for every fixed d >= 3, Matching Cut is NP-complete on graphs of diameter d. ... Section 4.2: a new O(|V| |E|^2) algorithm for diameter two." arXiv abstract (opened 2026-10-10): known "polynomially solvable for graphs of diameter two"; new: NP-complete "in the class of graphs of diameter d" for any fixed d >= 3. The diameter-two algorithm is in Le and Le (Section 4.2) as well as in the earlier paper, so the citation covers both halves. Definition in l.155 equals the note's. | None. |
| 157 | Komusiewicz et al. "gave kernels, single-exponential FPT algorithms and an exact exponential-time algorithm for this problem" | MATCHES | Note: "kernels for distance to cluster and to clique, single-exponential FPT algorithms, an O*(1.3071^n) randomized algorithm". Accepted version, abstract (opened 2026-10-10): "quadratic-vertex kernel for the parameter distance to cluster and a linear-vertex kernel for the parameter distance to clique", O*(2^dc(G))-time FPT algorithms for distance to cluster and to co-cluster, "improve the running time of the best known branching algorithm ... to O*(1.3071^n)"; Section 4: SAT-based algorithms, deterministic O*(1.328^n) and randomized O*(1.3071^n), and a SAT-free branching algorithm O*(1.3803^n). | None. Optional: "exact exponential-time algorithms". |
| 160 | "As with Shortest Path Most Vital Edges and Matching Cut, graphs of diameter two form a polynomial case of Min Cut-Path (Theorem 4.5)." | STRONGER than the note for Shortest Path Most Vital Edges | The polynomial case is for unit edge lengths only. arXiv v1 text, Section 1: "For arbitrary edge lengths, we show that the problem remains NP-hard on graphs of diameter one (Theorem 5)", and Theorem 5: "SP-MVE remains NP-hard on complete graphs." The note records "linear time on diameter two with unit lengths" but not Theorem 5. For Matching Cut the sentence matches the note (polynomial on diameter two). | "As with Shortest Path Most Vital Edges with unit edge lengths and Matching Cut, graphs of diameter two form a polynomial case of \MinCutPath{} (Theorem~\ref{thm:diameter-two})." |
| 1123 | "Is Min Cut-Path NP-hard on graphs of diameter three, the smallest diameter for which finding the most vital edges for shortest paths and finding a matching cut are NP-hard [Bazgan2019MostVital, LeLe2019MatchingCut]?" | STRONGER than the note for Shortest Path Most Vital Edges | Same facts as l.160: with arbitrary edge lengths Shortest Path Most Vital Edges is NP-hard on complete graphs (diameter one), so three is the smallest diameter only for unit edge lengths. Matching Cut: polynomial on diameter two, NP-complete for every fixed d >= 3 (Le and Le), so three is the smallest diameter there (diameter one is trivial: complete graphs). "Smallest diameter for which ... are NP-hard" also silently needs P != NP. | "Is \MinCutPath{} NP-hard on graphs of diameter three, the diameter at which finding the most vital edges for shortest paths with unit edge lengths and finding a matching cut turn from polynomial-time solvable to NP-hard~\cite{Bazgan2019MostVital,LeLe2019MatchingCut}?" |
| 1126 | "In a planar graph, every minimal edge cut corresponds to a cycle in the dual graph and vice versa, and several problems on cuts and flows can be solved faster in planar graphs than in general ones [itai1979maximum, henzinger1997faster]." | NO NOTE; the second clause is backed by the abstracts, the first clause has no source | Itai and Shiloach, SIAM J. Comput. 8(2), 135-150 (Crossref abstract, opened 2026-10-10): "Efficient algorithms for finding maximum flow in planar networks are presented. These algorithms take advantage of the planarity and are superior to the most efficient algorithms to date. ... If the network is undirected a minimum cut may be found in O(n^2 log n) time." Henzinger et al., JCSS 55(1), 3-23 (ISTA repository abstract, opened 2026-10-10): "We give a linear-time algorithm for single-source shortest paths in planar graphs with nonnegative edge-lengths. Our algorithm also yields a linear-time algorithm for maximum flow in a planar graph" (the quotation stops where my fetch tool cut it; a search-tool paraphrase of the abstract adds "source and sink on the same face", and Itai and Shiloach state the same-face case in their abstract, so I treat the qualifier as probable, not verified). So the title of Henzinger et al. is about shortest paths; its flow result is a by-product, and "faster than in general" is relative to the general algorithms of the time. The duality clause: Bentert et al. (arXiv v1 text, Section 1.1) "based on the correspondence between cuts and cycles in dual graphs" and Cullenbine et al., quoted there: "minimality of the corresponding (s,t)-cut demands a simple cycle". The article cites no source for the duality; the canonical `.bib` has `Diestel2025`, whose theorem on bonds and dual cycles has not been located (`TODO(verify)`: Section 4.6 of the 5th edition, number in the 6th edition). The duality holds for connected plane graphs. | "In a connected planar graph, the minimal edge cuts correspond to the simple cycles of the dual graph~\cite{Diestel2025}, and maximum flows and minimum cuts can be computed faster in planar graphs than in general ones~\cite{itai1979maximum,henzinger1997faster}." Keep `\cite{Diestel2025}` out until the location is checked. |

Count: the table has 14 rows (l.136 and l.137 are separate sentences; l.1123 and l.1126 are in the
Conclusion). 9 MATCH their notes, 2 are STRONGER than the source (l.160, l.1123), 3 have no note and are looser than the
abstracts (l.136, l.137, l.1126; l.1126 is half backed). Sentences that do not match: l.160, l.1123 (wording claims more
than the source) and, for lack of a source or precision, l.136, l.137, l.1126.

- MATCH: l.143, 144, 145, 148, 149 (with its unit-length scope), 153, 154, 156, 157.
- STRONGER than the source: l.160 and l.1123 (both: Shortest Path Most Vital Edges is polynomial on diameter two and
  NP-hard on diameter three only for unit edge lengths).
- NO NOTE and looser than the abstract: l.136 (Mehlhorn et al. is about 3-edge-connectivity; "studied in detail"),
  l.137 (the theorem relates flows and cuts), l.1126 (duality clause without a source).

### Items checked against your list of risky wordings

- "O(n log n) time on planar graphs": correct (weighted planar graphs, any s and t).
- "FPT with respect to its length": correct for the edge version (non-disconnecting); the length is the bound k.
- "W[1]-hardness": correct, vertex version, parameter k = length bound.
- "NP-hard on graphs of diameter three and linear time on diameter at most two": correct only for unit edge lengths;
  the sentence l.149 has the scope, l.160 and l.1123 lose it.
- "state that its complexity on general undirected graphs is open": faithful (arXiv v1, Section 1, twice), dated 2025.
- "the smallest diameter for which ... are NP-hard": see l.1123.

### Proposed addition to the reading note of Bazgan et al. (not applied)

`knowledge/literature/Bazgan2019MostVital.md`, "What the paper does": "For arbitrary positive integer edge lengths
SP-MVE is NP-hard already on complete graphs, so on diameter one (Theorem 5 of arXiv v1). The diameter results
(Theorem 4, Proposition 1) are for unit lengths." The same sentence belongs in `knowledge/research/min-cut-path.md`,
section 5b, row "Shortest Path Most Vital Edges".

### Other sentences of the Introduction that cite a work (not in your list)

- l.146: "Such a path models a private channel whose removal keeps the rest of the network connected". MATCHES the note
  (Abhinav et al., Section 1: a private channel between s and t whose path no other connection uses, the rest of the
  network must stay connected without it). "a cut-path asks for the opposite" is the author's contrast: for a
  non-disconnecting path G - E(P) is connected, for a cut-path S the graph G - S has no u-v path.
- l.150: "Such an edge set destroys all short u-v paths, whereas a cut-path meets every u-v path and contains one of
  them." Own contrast, correct.

## Part 2. Search for the same problem under another name

All queries, entered exactly, are in `knowledge/literature/searches.md` (8 rows dated 2026-10-10). Sources used: web search
(9 queries), web search restricted to sciencedirect.com (4), arXiv API (16 `search_query` searches), OpenAlex (4 free-text
and 19 restricted to DAM, ISSN 0166-218X), zbMATH Open API (12), Crossref (4 free-text and 10 with `filter=issn:0166-218X`).
DBLP failed again (bot-check page instead of results, HTTP 200; not bypassed). Elsevier pages (ScienceDirect, linkinghub)
could not be opened, and Crossref carries no abstracts for the DAM papers below, so their abstracts were read in the arXiv
version, an accepted manuscript or a repository record; each row says which.

### 2.1 Is the same problem found anywhere? No.

Evidence, by source:

- Web search (all wordings of the task list, plus "path-cut", "cut-path", "separating shortest path", "disconnecting path",
  "path whose removal separates", "geodesic cut", "secure path", "bond containing a path"): the only hits for the
  problem itself are the author's own CSGT 2026 abstract (`csgt2026.tuke.sk/pdfs/MICHEL.pdf`) and the master's thesis
  record (`dspace.cuni.cz/handle/20.500.11956/200007`, "Minimalni rez-cesta", Loebl). Everything else is a neighbouring
  problem (below).
- arXiv API: `abs:"separating shortest path"`, `all:"cut containing a path"`, the "edge cut contains a path" and
  "minimum cut and shortest path union" queries, the "secure path" and "geodesic edge cut" queries and three circuit/cocircuit
  queries: 0 hits each. `abs:"cut-path"`: 15 hits in other fields (geometry, robotics, quantum computing, physics; Cairo et al., arXiv 2210.07530,
  "cut paths" in strongly connected digraphs, which are subwalks contained in every u-v walk, not our object).
  `abs:"non-disconnecting path"`: only Kobayashi, Nagano, Otachi (arXiv 2202.09718).
- zbMATH Open: no document with *separating shortest path* or *non-disconnecting path*; *cut-path* in a title gives only
  Hartvigsen and Wagner 1988 (path matrices, Oper. Res. Lett. 7), unrelated; *separating path* gives 14 documents, all on
  separating path systems (families of paths that separate edge pairs), a different notion.
- OpenAlex (free text and restricted to DAM): only the non-separating-path papers already known (Kobayashi et al.,
  Abhinav et al., Wu 2012, Kawarabayashi-Lee-Yu 2005) and unrelated hits.
- Matroid wording (the smallest union of a circuit and a cocircuit that meet in one element, which is what a cut-path
  is, essentially, after adding the edge uv and taking a minimal cut): no paper found; the circuit-cocircuit literature studies intersection sizes
  (Oxley's conjecture), not unions.
- Equivalent form, derived here and not found in any source (`TODO(verify)` by the author, the derivation is two lines):
  `cp(u,v) = min over u-v paths P of ( |P| + c_{G - E(P)}(u,v) )`, because for a fixed path P the cheapest completion is a
  minimum u-v cut of the graph without the edges of P (all other edges cost one). This is "delete a path so that the
  remaining u-v edge connectivity is as small as possible, paying for the path". Searches for that wording (path removal
  that minimizes the maximum flow, "most vital path") found only single most vital edges and k most vital edges
  (Baswana and Bhanja, arXiv 2310.12096, for one edge; a search summary names Wood for the strong NP-hardness of k
  edges, not read), not paths.

Nearest problems found, none of them the same (relation in one line):

| Problem | Source | Relation |
|---|---|---|
| Non-disconnecting / non-separating s-t path | `Mao2021NonSeparating`, `Abhinav2022NonSeparating` | opposite requirement; already in the Introduction |
| Force Path Cut: delete the fewest edges so that a given path becomes a shortest s-t path | Miller et al., ACM TKDD 18(2), 2023 (arXiv 2211.11141); ECML PKDD 2021 (arXiv 2104.03761) | path is input, deleted edges need not separate; adversary motivation like ours |
| Network Diversion | `Bentert2025NetworkDiversion`, Cullenbine et al. 2013 | cut with a prescribed edge; already in the Introduction |
| Connectivity Preserving / Reachability-Preserving Minimum Edge Cut | Duan, Xu, arXiv 1309.6689; Duan et al., arXiv 1412.3359; Duan, arXiv 2606.18225 | a minimum cut that keeps another pair connected: cut and connection in one problem, but the connection must survive the cut (we put the path into the selected set) |
| Critical Disruption Path | Granata, Steeger, Rebennack, Comput. Oper. Res. 40(11), 2013 | remove an s-t path to fragment the network (vertex version, objective is the largest remaining component); abstract known only from a search summary |
| Preventing Small (s,t)-Cuts by Protecting Edges | Grüttemeier, Komusiewicz, Morawietz, Sommer, arXiv 2107.04482 | choose protected edges that meet every small cut; no path |
| Minimum Shared Edges | Fluschnik, Kratsch, Niedermeier, Sorge, arXiv 1602.01739 | p paths sharing few edges; no cut |

### 2.2 Candidates

Abstract source: "A" = arXiv abstract, "C" = Crossref abstract, "R" = repository or accepted manuscript. For none of the DAM
papers was the Elsevier page readable.

| Key proposal | Reference | DOI | Abstract (one sentence) | Relation | Recommendation |
|---|---|---|---|---|---|
| `Baier2010LengthBounded` | Baier, Erlebach, Hall, Köhler, Kolman, Pangrác, Schilling, Skutella: Length-bounded cuts and flows. ACM Trans. Algorithms 7(1), 2010 (Crossref pages 1-27; "7(1):4" in the reference list of Bazgan et al.) | 10.1145/1868237.1868241 | (C) An L-length-bounded edge-cut is an edge set after whose removal no s-t path of length at most L remains; minimum length-bounded cuts are NP-hard to approximate within 1.1377 for L >= 4 (edge case) and the paper compares them with length-bounded flows. | Source of the term "length-bounded edge cut" used in l.149 without a reference. Already read on 2026-10-09 (log), no note, no `.bib` entry. | cite at l.149 (needs the `.bib` entry with status line and a reading note first) |
| `Cullenbine2013NetworkDiversion` | Cullenbine, Wood, Newman: Theoretical and computational advances for network diversion. Networks 62(3), 225-242, 2013 | 10.1002/net.21514 | (C) New NP-completeness proof of Network Diversion on directed graphs, first polynomial-time algorithm for a special topology (s-t planar graphs), a better mixed-integer program; a corollary gives NP-completeness of a vertex-deletion version on undirected graphs. | Original source for the undirected problem and for the s-t planar algorithm; the Bentert et al. introduction (arXiv v1 text) attributes both to it. The vertex-deletion hardness explains why l.154 must say "edge version" if it ever says "open". | mention: cite next to `Bentert2025NetworkDiversion` at l.153 (optional) |
| `Miller2023ForcePathCut` | Miller, Shafi, Ruml, Vorobeychik, Eliassi-Rad, Alfeld: Attacking Shortest Paths by Cutting Edges. ACM Trans. Knowl. Discov. Data 18(2), 2023 (Crossref pages 1-42) | 10.1145/3622941 | (A, 2211.11141) The Force Path Cut problem asks an adversary to remove edges so that a given path becomes the shortest path between its terminals; it is APX-hard and PATHATTACK is a logarithmic-factor approximation. | Edge-removal problem with a prescribed path and an adversary; closest in motivation to the server story of the Introduction, different object. Not assessed in depth. | mention (optional, one clause in the paragraph on cuts with prescribed structure); reading note first |
| `Duan2013ConnectivityPreserving` | Duan, Xu: On the Connectivity Preserving Minimum Cut Problem. arXiv 1309.6689, 2013 (no published version found in OpenAlex) | - | (A) A minimum cut that separates a source from a destination while keeping the source connected to a partner node; hard to approximate for node cuts, polynomial for edge cuts on planar graphs, general edge case open. | The only family I found that asks for a cut and a connecting structure in one problem. | skip for now (preprint; relation is the reverse of ours) |
| `Komusiewicz2020MatchingCut` | Komusiewicz, Kratsch, Le: Matching cut: Kernelization, single-exponential time FPT, and exact exponential algorithms. DAM 283, 2020, 44-58 | 10.1016/j.dam.2019.12.010 | (R, accepted manuscript) Matching Cut has a quadratic-vertex kernel for distance to cluster and a linear-vertex kernel for distance to clique, FPT algorithms O*(2^dc) for distance to cluster and to co-cluster, a branching algorithm of O*(1.3071^n) and no polynomial kernel for treewidth plus cut size plus maximum degree unless NP is in coNP/poly. | Cut with a prescribed structure; the one DAM paper in the Introduction. | keep (already cited) |
| `LoSchmidtThorup2021` | Lo, Schmidt, Thorup: Compact cactus representations of all non-trivial min-cuts. DAM 303, 2021, 296-304 | 10.1016/j.dam.2020.03.046 | (A, 1810.03865v2) A contraction-based sparsifier with O(n/delta) vertices and O(n) edges preserves all non-trivial min-cuts of a simple graph, gives a cactus representation of them with O(n/delta) vertices, and lists all min-cuts in O~(m) + O(n^2/delta) time. | DAM paper on representing all minimum cuts, the topic of the second clause of l.136 (Nagamochi and Kameda); not close to Min Cut-Path. | mention: optional second citation at l.136 to anchor the sentence in DAM |
| `Pan2016Interdiction` | Pan, Schild: Interdiction problems on planar graphs. DAM 198, 2016, 215-231 | 10.1016/j.dam.2015.05.036 | (A, 1305.1407v2) Approximation algorithms and strong NP-completeness for interdiction problems on planar graphs, among them directed shortest path interdiction. | Interdiction of shortest paths (directed, weighted); no cut containing a path. | skip (revisit if the planar question of the Conclusion is expanded) |
| `Hartvigsen1998PlanarMultiterminal` | Hartvigsen: The planar multiterminal cut problem. DAM 85(3), 1998, 203-222 | 10.1016/s0166-218x(98)00036-5 | (OpenAlex copy of the Elsevier abstract) Two structural theorems for optimal solutions of the planar min V'-cut problem, one linking it to Gomory-Hu cut collections, one to a matroid; each gives a simple algorithm. | Planar cut structure; background only for the planar question of the Conclusion. | skip |

Seen by title only in DAM, abstract not read, therefore not proposed: Ito, Kaminski, Paulusma, Thilikos, On disconnected cuts and
separators (DAM 159(13), 2011, 1345-1351, 10.1016/j.dam.2011.04.027; vertex cuts that induce a disconnected graph, a relative
of matching cut); Bonsma, Most balanced minimum cuts (DAM 158(4), 2010, 261-276, 10.1016/j.dam.2009.09.010); Bruglieri,
Maffioli, Ehrgott, Cardinality constrained minimum cut problems (DAM 137(3), 2004, 311-341, 10.1016/s0166-218x(03)00358-5);
Fujita, Kawarabayashi, Note on non-separating and removable cycles in highly connected graphs (DAM 157(2), 2009, 398-399,
10.1016/j.dam.2008.06.012); Shang, Zhang, Super restricted edge-connectivity of graphs with diameter 2 (DAM 161(3), 2013,
445-451, 10.1016/j.dam.2012.08.030; restricted edge-connectivity, not cuts between two given vertices); Zenklusen, Matching
interdiction (DAM 158(15), 2010, 1676-1690, 10.1016/j.dam.2010.06.006); Hoang, Lendl, Wulf, Assistance and interdiction
problems on interval graphs (DAM 340, 2023, 153-170, 10.1016/j.dam.2023.06.046); Dev, Dey, Foucaud, Narayanan, Sulochana,
Monitoring edge-geodetic sets in graphs (DAM 377, 2025, 598-610, 10.1016/j.dam.2025.08.041; OpenAlex abstract: vertex pairs
that detect the removal of an edge by the increase of their distance, NP-hard; about vertex sets, not a cut or a path).

DAM papers genuinely close to Min Cut-Path or Separating Shortest Path: none. Closest in the journal: `Komusiewicz2020MatchingCut`
(cut with a prescribed structure, already cited). For the topics you listed: paths whose removal disconnects or keeps
connectivity (only Fujita and Kawarabayashi on cycles, vertex removal, highly connected graphs, and a matroid paper on
non-separating cocircuits, DAM 156(7), 2008, 1019-1024, 10.1016/j.dam.2007.05.055, neither close); connected cuts, bonds,
d-cuts (none in DAM; they are in TCS, Algorithmica and arXiv); most vital edges and length-bounded cuts (none in DAM; Bazgan et
al. is in Networks, Baier et al. in ACM TALG); edge cuts in diameter-two graphs (only restricted edge-connectivity; the classical
fact is Plesník 1975, "edge connectivity equals minimum degree", strengthened locally by Payne, Pór, Valtr, found through a
search summary only and not needed by the text, since Section 4 proves what it uses); cactus graphs (Section 5 proves its own
lemma, `lem:cactus`).

### 2.3 Proposed optional additions to the Introduction (only if you want them)

Each rests on an abstract I read; none is applied. The first is the only one I would make.

1. l.149, after "length-bounded edge cut": add `~\cite{Baier2010LengthBounded}` (the term is Baier et al.'s).
2. l.153: "\textsc{Network Diversion}~\cite{Cullenbine2013NetworkDiversion} asks for a minimal $u$--$v$ cut of at most $k+1$ edges that contains a prescribed edge."
3. After l.157, one sentence: "\textsc{Force Path Cut} asks for the fewest edges whose removal makes a prescribed path a shortest path between its endpoints~\cite{Miller2023ForcePathCut}; the path is part of the input, and the removed edges need not separate its endpoints." (Needs a reading note and `VERIFIED` entry first.)

### 2.4 Does "To the best of our knowledge, Min Cut-Path has not been studied before." still stand?

Yes for work by other authors, as of 2026-10-10: about 80 queries over six sources found no paper that defines a set of
edges containing a path and a cut, or a shortest path whose edge removal separates its endpoints, under any name; the
log rows of 2026-10-10 satisfy the three-month rule until 2027-01-10. Two cautions:

1. Read literally the sentence is imprecise: the problem was studied before in the author's own master's thesis (Charles University,
   2025) and in the CSGT 2026 abstract, and both are findable by search engines, so a referee will see them. The
   thesis is deliberately not cited in the article (decision of 2026-10-09). This is the author's decision; a wording that
   stays true without citing it is "To the best of our knowledge, no work other than the author's own has studied \MinCutPath{}"
   or, with the citation, "To the best of our knowledge, apart from the author's master's thesis~\cite{...}, \MinCutPath{}
   has not been studied before."
2. The Network Diversion sentence (l.154) is a statement about the state of the art of 2025; no resolution was found in 2026,
   but a result could appear before submission. Repeat the Network Diversion search at submission.

DBLP is the one index not searched; if it is reachable from your machine, run the three queries (*non-separating path*,
*separating shortest path*, *cut-path*) in a browser and add a row.
