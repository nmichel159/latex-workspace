# B1. Path-removal side: critical literature search for Min Cut-Path / Separating Shortest Path

Date: 2026-10-10. Status: COMPLETE (angles 1-6).

Scope: angles 1-6 of the brief (disjoint paths with one shortest path, forward citations of the closest papers,
path interdiction, nearby notions, status of Network Diversion and of two preprints, DBLP).
Queries already logged in `knowledge/literature/searches.md` (2026-10-07 to 2026-10-10) were not repeated.
Nothing but this file was written. No downloaded file was saved: PDFs were read from memory (stream to a text extractor).
Everything below is paraphrase; theorem numbers are those of the version named under "Read".

Notation used here: for a shortest u-v path P let r(P) = lambda_{G - E(P)}(u,v), the number of edge-disjoint u-v paths
left after the edges of P are deleted. SSP asks whether r(P) = 0 for some shortest P.

## 1. Verdict

1. The same problem was not found. No paper defines an edge set containing a u-v path and a u-v cut, and no paper asks for a
   shortest path whose edge removal separates its endpoints. No equivalent formulation was found either.
2. No theorem found implies or contradicts a result of the manuscript (NP-completeness, no PTAS, diameter two, cactus,
   G(n,p), FPT).
3. A mirror problem exists and the manuscript does not cite it: "is there a shortest path P with r(P) >= 1?" (a shortest path
   with an edge-disjoint counterpart). It is NP-complete. A referee from the disjoint-paths or survivable-routing side will
   see SSP as its twin, so it has to be named and separated in the Introduction.
4. Closest work, ranked: (i) Eilam-Tzoreff, DAM 85 (1998): two disjoint paths, one of them shortest (2D1SP), NP-complete on
   undirected unit-length graphs, two terminal pairs, reduction from 3SAT; published in the target journal. (ii) Min-Min
   disjoint paths, "the shortest path with a disjoint counterpart": Xu et al. 2006; Guo and Shen 2012 (TCS), 2013
   (Algorithmica): one terminal pair, NP-hard, no constant-factor approximation. (iii) Radermacher and Rutter 2018: state
   that the one-pair form is NP-hard and that the planar case is open. (iv) Cai and Ye 2016/2019: the mirror
   problem is FPT in the length of the short path. (v) Hon, Tsai, Yang 2025: a peer-reviewed NP-completeness proof for the
   existence of a non-disconnecting path (the statement the manuscript takes from Mao's preprint).
5. Logical relation of SSP to the mirror problem MMS ("some shortest P has r(P) >= 1"): neither the same nor the complement.
   Not-SSP implies MMS, not-MMS implies SSP, and both can hold in one graph (example in Angle 1). No reduction between
   them was found in the literature.
6. Free by-product of the manuscript's theorem in the language of that literature: deciding whether every shortest u-v
   path has an edge-disjoint u-v counterpart (the complement of SSP) is coNP-complete.
7. Name collision: "cut paths" of Cairo et al. (STACS 2023; ACM Trans. Algorithms 22(2), 2026) are a different object
   (a walk contained in every u-v walk of a strongly connected digraph).
8. Other path-removal problems found (Critical Disruption Path, minimum maximal flow, Lovasz path removal) differ in the
   object removed or in the objective; details in Angle 3.
9. Status answers: Network Diversion on general undirected graphs (edge version) is still stated open in the newest sources
   found; Mao's preprint has no published version; Abhinav et al. has no journal version.
10. Not read in full text: Xu et al. 2006 and the Guo-Shen papers (abstracts only). Two points depend on them and are
    marked `TODO(verify)`: whether undirected edge-disjoint Min-Min is hard for unit lengths, and whether the hard instances
    ask for a path of length exactly d(s,t).

## 2. Findings by angle

### Angle 1. Disjoint paths where one path is shortest

#### 1.0 Four predicates and their relation

Fix G, u, v with d = d(u,v) finite, edge-disjoint version, unit lengths.

| Name | Predicate | Where it occurs |
|---|---|---|
| SSP | some shortest P has r(P) = 0 | the manuscript |
| MMS | some shortest P has r(P) >= 1 | Min-Min disjoint paths with the bound d; one-pair form of 2D1SP |
| co-SSP | every shortest P has r(P) >= 1 | not found in the literature |
| co-MMS | every shortest P has r(P) = 0 | not found in the literature |

- co-SSP implies MMS and co-MMS implies SSP (a shortest path exists). So at least one of SSP, MMS holds.
- Only SSP: a path. Only MMS: the 4-cycle with u, v opposite.
- Both: vertices u, a, b, c, e, v; edges ua, ab, bv, ac, cv, ue, eb. Here d = 3 and the shortest paths are u-a-b-v,
  u-a-c-v, u-e-b-v. Removing u-a-b-v leaves no u-v path (r = 0); removing u-a-c-v leaves u-e-b-v (r = 1).
  (Checked by hand; `TODO(verify)` by the author before use.)
- Hence SSP is not MMS and not its complement. The hardness of one does not transfer to the other by complementation.
  I found no reduction between them.
- Survivable-routing wording: a path P with r(P) = 0 in a graph with lambda(u,v) >= 2 is a "trap" for the heuristic that
  routes the active path first. SSP asks whether a shortest path can be a trap; Min-Min asks for the shortest path that is
  not one.

#### 1.1 Eilam-Tzoreff 1998 (closest verified theorem)

- Reference: Tali Eilam-Tzoreff. The disjoint shortest paths problem. Discrete Applied Mathematics 85(2) (1998) 113-138.
  DOI 10.1016/S0166-218X(97)00121-2. Record: Crossref (`api.crossref.org/works/10.1016/s0166-218x(97)00121-2`).
- Read: abstract (CORE API record 41769756 and the PDF); journal PDF pages 113-120 (Sections 1, 2 and the start of 3),
  from the Internet Archive snapshot of 2024-12-05 of `core.ac.uk/download/pdf/82288569.pdf`. Sections 4-5 not read.
- Problem (Section 2), 2D1SP: given a graph with positive edge lengths and two pairs (s1,t1), (s2,t2), are there disjoint
  paths P1 from s1 to t1 and P2 from s2 to t2 such that P1 is a shortest path? Vertex- and edge-disjoint versions, directed
  and undirected.
- Results read: Claim 1: the vertex- and the edge-disjoint version on undirected graphs are NP-complete; the reduction is
  from 3SAT, uses integer lengths and replaces each edge by a path of unit edges, so the claim holds for unit lengths.
  Claim 2 is the correctness of the reduction. Claim 3: the same for directed graphs. Claim 4 (Section 3): k disjoint
  shortest paths, k in the input, NP-complete on planar undirected graphs. Abstract: polynomial algorithm for two disjoint
  shortest paths on undirected graphs with positive lengths.
- Relation to SSP: the mirror question with two terminal pairs. 2D1SP: some shortest s1-t1 path P leaves s2, t2 connected in
  G - E(P). SSP: some shortest u-v path P leaves u, v disconnected in G - E(P).
- Precise difference: (a) connectivity required versus separation required; (b) two different pairs in the reduction
  (the pairs are (y1, y6m) and (d1, a_{m+1})), one pair in SSP; (c) decision problem only, no size objective.
  Neither result implies the other.
- Recommendation: CITE. Introduction, paragraph on non-disconnecting paths: one sentence stating the result and the
  opposite requirement. It is the nearest NP-completeness result on shortest paths and connectivity after their removal,
  it uses a 3SAT reduction on undirected unit-length graphs, and it appeared in DAM.

#### 1.2 Xu, Chen, Xiong, Qiao, He 2006 (Min-Min; the name "disjoint counterpart")

- Reference: Dahai Xu, Yang Chen, Yizhi Xiong, Chunming Qiao, Xin He. On the complexity of and algorithms for finding the
  shortest path with a disjoint counterpart. IEEE/ACM Transactions on Networking 14(1) (2006) 147-158.
  DOI 10.1109/TNET.2005.863451. Record: Crossref. (The lead "Xu, Chen, Xiao, Qiao" was wrong in the third name.)
  Conference version: On finding disjoint paths in single and dual link cost networks, IEEE INFOCOM 2004,
  DOI 10.1109/INFCOM.2004.1354541 (seen in reference lists and a search result only, record not opened: `TODO(verify)`).
- Read: abstract only (OpenAlex copy of the publisher abstract, W2128090945). Full text not accessible.
- Problem: Min-Min: among pairs of disjoint s-t paths, minimise the length of the shorter path (the active path).
- Results (abstract): NP-complete in single-cost and in dual-cost networks; NP-hard to approximate within any factor
  K > 1; heuristic COLE built on "conflicting link sets", introduced for the "trap problem".
  Directed or undirected, link- or node-disjoint, allowed lengths: not in the abstract, `TODO(verify)`.
- Relation: optimisation form of MMS. Min-Min has optimum d(s,t) iff MMS holds.
- Difference: Min-Min wants a short path that does not separate; SSP wants a shortest path that does. Min-Min has general
  lengths (the inapproximability within every factor cannot hold for unit lengths, where the ratio is below n).
- Recommendation: CITE together with 1.3 (one clause: the problem and its name). Source of the term "disjoint counterpart".

#### 1.3 Guo and Shen 2012, 2013 (corrected hardness, planar cases)

- References (records: Crossref):
  - Longkun Guo, Hong Shen. On Finding Min-Min Disjoint Paths. Algorithmica 66(3) (2013) 641-653 (online 2012).
    DOI 10.1007/s00453-012-9656-0.
  - Longkun Guo, Hong Shen. On the complexity of the edge-disjoint min-min problem in planar digraphs. Theoretical Computer
    Science 432 (2012) 58-63. DOI 10.1016/j.tcs.2011.12.009.
  - Conference versions: Hardness of Finding Two Edge-Disjoint Min-Min Paths in Digraphs, FAW-AAIM 2011, LNCS 6681,
    300-307, DOI 10.1007/978-3-642-21204-8_32 (volume number from a repository page, `TODO(verify)`); On the complexity of
    the edge-disjoint min-min problem in undirected graphs, 2011 3rd International Conference on Computer Research and
    Development (ICCRD), 150-154, DOI 10.1109/ICCRD.2011.5764102; A Polynomial Algorithm for the Vertex Disjoint Min-Min
    Problem in Planar Graphs, PAAP 2011, 47-51, DOI 10.1109/PAAP.2011.15.
- Read: abstracts only. Algorithmica: abstract and reference list on the Springer page. TCS: abstract from the University
  of Adelaide repository API (handle 2440/72964) and the CORE API. FAW-AAIM: Springer page. ICCRD, PAAP: OpenAlex.
  No full text (ScienceDirect HTTP 403; CORE download behind a challenge page, not passed; Springer paywall).
- Results (abstracts):
  - Algorithmica: the NP-hardness proof of Bhatia et al. for edge-disjoint Min-Min in undirected graphs is wrong (an
    unsatisfiable 3SAT instance is accepted); a correct NP-hardness proof for undirected graphs; a polynomial algorithm for
    vertex-disjoint Min-Min in planar graphs via st-planar graphs.
  - TCS: edge-disjoint Min-Min is NP-complete in planar digraphs, has no K-approximation for any K > 1 unless P = NP, and
    stays NP-complete when all edge costs are equal.
  - PAAP: vertex-disjoint Min-Min on st-outerplanar graphs in O(|E| + |V| log |V|) time.
- Open after reading the abstracts, `TODO(verify)` in the full texts: (a) is undirected edge-disjoint Min-Min NP-hard for
  unit lengths; (b) does the bound in the hard instances equal d(s,t), that is, do they prove MMS hard.
- Relation and difference: as 1.2. Their planar results concern the mirror problem; they say nothing on SSP or Min Cut-Path
  in planar graphs (the manuscript's open question).
- Recommendation: CITE the Algorithmica paper with 1.2. MENTION the TCS paper in the report only, or in the Conclusion
  beside the planar question if the author wants a contrast ("the mirror problem is hard on planar digraphs").

#### 1.4 Bhatia, Kodialam, Lakshman 2006 (not Min-Min)

- Reference: Randeep Bhatia, Murali Kodialam, T. V. Lakshman. Finding disjoint paths with related path costs. Journal of
  Combinatorial Optimization 12(1-2) (2006) 83-96. DOI 10.1007/s10878-006-8906-y. Record: Crossref.
- Read: abstract and reference list (Springer page).
- Problem: a pair of edge- or node-disjoint paths minimising cost(primary) + alpha * cost(backup), alpha < 1.
  Results: hard to approximate within a factor about (1/alpha)^(1-eps); an O(1/alpha)-approximation.
- Relation: none to SSP beyond the family. The abstract does not mention Min-Min; the proof that Guo and Shen refute is
  inside the paper.
- Recommendation: SKIP.

#### 1.5 Radermacher and Rutter 2018 (the one-pair statement)

- Reference: Marcel Radermacher, Ignaz Rutter. Inserting an Edge into a Geometric Embedding. Graph Drawing and Network
  Visualization (GD 2018), LNCS, 402-415, DOI 10.1007/978-3-030-04414-5_29. Journal version: Computational Geometry 102
  (2022) 101843, DOI 10.1016/j.comgeo.2021.101843. arXiv 1807.11711. Records: Crossref, arXiv API.
- Read: arXiv v1, the related-work passage (p. 6) and the conclusion (p. 12). Journal version not read.
- Statements: Eilam-Tzoreff's result can be modified to show that deciding whether a graph has two edge-disjoint s-t
  paths, one of them shortest, is NP-hard (stated without proof); for planar graphs the complexity of finding two
  edge-disjoint paths with one length minimised is called open (2018).
- Relation: this is MMS, stated for one pair. It is a remark, not a theorem with a proof; the passage does not say which
  edge lengths are meant (the result it modifies is for unit lengths).
- Recommendation: MENTION in the report. Cite only if the Introduction states the one-pair form of the mirror problem and
  needs a source for it next to Xu et al.

#### 1.6 Cai and Ye 2016/2019 (parameterized mirror)

- Reference: Leizhen Cai, Junjie Ye. Finding Two Edge-Disjoint Paths with Length Constraints. WG 2016, LNCS, 62-73,
  DOI 10.1007/978-3-662-53536-3_6. Journal version: Two edge-disjoint paths with length constraints, Theoretical Computer
  Science 795 (2019) 275-284, DOI 10.1016/j.tcs.2019.07.009. arXiv 1509.05559. Records: Crossref, arXiv API.
- Read: arXiv v1, pages 1-4 and the theorem statements (Theorems 1-3, 6, 7, concluding remarks).
- Problem: Edge-Disjoint (L1, L2)-Paths: undirected graph, pairs (s1,t1), (s2,t2), edge-disjoint paths P1, P2 whose lengths
  satisfy constraints "at most k_i", "exactly k_i", "at least k_i" or none.
- Results read: Theorem 2: the case (at most k1, no constraint) is solvable in time O(2.01^{k1^2} m log n), so FPT in k1.
  Theorems 6, 7: no polynomial kernel unless NP is in coNP/poly. Related work: credits Eilam-Tzoreff with NP-completeness of
  the case (at most k1, no constraint) even when k1 = d(s1,t1).
- Relation: the mirror problem ("a path of length at most k with an edge-disjoint counterpart") is FPT in k. The manuscript
  shows Min Cut-Path FPT in the solution size, which bounds the path length too. No overlap in technique (random
  separation on "nearby edges" versus treewidth reduction).
- Recommendation: MENTION; optional citation in the FPT section as the parameterized counterpart on the other side.

#### 1.7 Seen by record only

- Chung-Lun Li, S. Thomas McCormick, David Simchi-Levi. The complexity of finding two disjoint paths with min-max objective
  function. Discrete Applied Mathematics 26(1) (1990) 105-115. DOI 10.1016/0166-218X(90)90024-7. Crossref record; content
  known only from Eilam-Tzoreff's introduction. Min-max of two disjoint s-t paths; no path removal that separates. SKIP.
- Yang, Zheng, Katukam, "Finding Two Disjoint Paths in a Network with Min-Min Objective Function" (2003): a Semantic
  Scholar record without venue or DOI. `TODO(verify)`. Yang, Zheng, Lu (ISAAC 2005, DOI 10.1007/11602613_95) is about the
  "normalized alpha+-MIN-SUM" objective, not Min-Min. SKIP both.
- Shan, Zhang, Chen, Liang, Yang, Zhao. Min-min edge-disjoint path pairs with constraints on common nodes. The Journal of
  Supercomputing 81(5) (2025) article 662, DOI 10.1007/s11227-025-07064-6. Springer abstract read: a heuristic. Shows the
  Min-Min line is active in 2025. SKIP.
- "Trap": the abstract of Xu et al. names the "trap problem". An open text that describes it: Zhao, Zhu, Liu, arXiv
  2303.00527v1 (pp. 1-2, 5, 8-9 read): an active path is found that has no disjoint backup path. Xu, Xiong, Qiao, Li,
  J. Lightwave Technol. 21(11) (2003) 2683-2693 is said to define traps; known from a search summary only, `TODO(verify)`.

### Angle 2. Forward citations 2022-2026

Citing papers found (all sources together):

| Cited paper | Source | Citing papers | Any path whose removal must separate? |
|---|---|---|---|
| Mao, arXiv 2101.03519 | Semantic Scholar (2), Google Scholar (2) | Kobayashi, Nagano, Otachi (arXiv 2202.09718); Abhinav et al. (MFCS 2022) | no |
| Kobayashi, Nagano, Otachi, arXiv 2202.09718 | Semantic Scholar (0), OpenAlex (0), Google Scholar (no count shown) | none listed | - |
| Abhinav et al., MFCS 2022 | Semantic Scholar (1), Google Scholar (3), OpenAlex (0) | Antony et al., arXiv 2307.12073 (title: total domination, CD-coloring; not opened); Hon, Tsai, Yang 2025; Bandopadhyay, Banik, "Parameterized algorithms for constrained graph problems", repository record 2024 (not opened); Finocchi, Italiano, Algorithms and Complexity, Springer 2025 (a book entry, probably the proceedings volume holding Hon et al.) | no |
| Bazgan et al., Networks 2019 | OpenAlex (14), Semantic Scholar (22) | interdiction on trees and interval graphs, length-bounded cuts (Bentert, Heeger, Knop), Preventing small (s,t)-cuts, safety in s-t paths (Cairo et al.), the flow-interdiction survey of Ausiello et al. 2026, Robust Temporal Cut (SAND 2026), Vertex Cover Interdiction (arXiv 2609.24624) | no (titles; three abstracts read) |
| Eilam-Tzoreff, DAM 1998 | OpenAlex (94) | disjoint shortest paths (Lochet; Bentert et al.; Berczi, Kobayashi; Gottschau et al.; Akhmedov; Mari et al.), Cai and Ye, Radermacher and Rutter, Critical Disruption Path 2023, Bachtler et al. (almost disjoint paths) | no |
| Guo, Shen, Algorithmica 2013 | OpenAlex (18) | restricted shortest paths, SRLG-disjoint routing, link-disjoint paths with few common nodes | no |
| Xu et al., TNET 2006 | OpenAlex (62) | survivable routing, Minimum Shared Edges (Omran, Sack, Zarrabi-Zadeh), Guo-Shen papers | no |

No citing paper asks for a path whose removal separates its endpoints.

#### 2.1 Hon, Tsai, Yang 2025 (published hardness for non-disconnecting paths)

- Reference: Wing-Kai Hon, Meng-Tsung Tsai, Ching-Yu Yang. Supereulerian Testing on Semi-Eulerian Graphs. In: Algorithms
  and Complexity (CIAC 2025), LNCS, 316-330, 2025. DOI 10.1007/978-3-031-92935-9_20. Record: Crossref (LNCS volume number
  not in the record, `TODO(verify)`).
- Read: abstract (Springer page). Found as a citing paper of Abhinav et al. (Google Scholar).
- Problem: does G have a spanning Eulerian subgraph. Restated in the abstract: join the odd-degree vertices in pairs by
  edge-disjoint paths whose edge removal does not disconnect G. With exactly two odd-degree vertices s, t this is: is there
  an s-t path P with G - E(P) connected (my reading of the abstract: the removed set is an {s,t}-join, and removing only its
  s-t path keeps a connected spanning subgraph with even degrees).
- Result: NP-complete even for semi-Eulerian graphs; an O(1.362^n) exact algorithm.
- Relation: a peer-reviewed proof that the existence of a non-disconnecting s-t path is NP-complete, on a restricted class.
  The manuscript (l.143 of the 2026-10-10 check) rests this fact on Mao's preprint, whose proof is a sketch.
- Recommendation: CITE beside Mao in the Introduction (after a reading note on the full text confirms the equivalence).

#### 2.2 Cairo et al. 2023/2026 (name collision "cut paths")

- Reference: Massimo Cairo, Shahbaz Khan, Romeo Rizzi, Sebastian Schmidt, Alexandru I. Tomescu, Elia C. Zirondelli. Cut
  Paths and Their Remainder Structure. ACM Transactions on Algorithms 22(2) (2026) 1-30. DOI 10.1145/3790095 (Crossref).
  Conference version: STACS 2023, LIPIcs 254, 17:1-17:17, DOI 10.4230/LIPIcs.STACS.2023.17 (DataCite). arXiv 2210.07530.
- Read: both abstracts (Crossref, arXiv API).
- Definition: in a strongly connected digraph, a cut path is a walk W such that for some u, v every u-v walk contains W as a
  subwalk; it generalises cut arcs (strong bridges). Results: linear-time verification, O(n) maximal cut paths, O(n^2)
  enumeration, applications to safe walks in genome assembly.
- Relation: none in content. Their object is one path lying on all u-v walks; a cut-path of the manuscript is an edge set
  made of a path and a cut. The names differ by a hyphen.
- Recommendation: CITE in one clause where "cut-path" is defined ("not to be confused with ..."). The earlier search log
  listed the arXiv version as unrelated; the 2026 journal publication makes the collision visible to referees.

### Angle 3. Path interdiction, removal of a path

Nothing found under "most vital path", "path blocker", "minimum cut after removing a shortest path" or "residual
connectivity after routing a path" (arXiv, OpenAlex title and abstract phrases, web). Three lines of work remove a path:

#### 3.1 Critical Disruption Path

- References (Crossref): Donatella Granata, Gregory Steeger, Steffen Rebennack. Network interdiction via a Critical
  Disruption Path: Branch-and-Price algorithms. Computers & Operations Research 40(11) (2013) 2689-2702.
  DOI 10.1016/j.cor.2013.04.016. Donatella Granata, Antonino Sgalambro. Network Interdiction through Length-Bounded
  Critical Disruption Paths: a Bi-Objective Approach. Electronic Notes in Discrete Mathematics 52 (2016) 375-382.
  DOI 10.1016/j.endm.2016.03.049. Donatella Granata, Antonino Sgalambro. A hybrid modified-NSGA-II VNS algorithm for the
  Multi-Objective Critical Disruption Path Problem. Computers & Operations Research 160 (2023) 106363.
  DOI 10.1016/j.cor.2023.106363.
- Read: 2016 paper, accepted manuscript (White Rose repository), abstract and introduction; 2023 paper, abstract
  (OpenAlex). 2013 paper not read (no abstract in Crossref or OpenAlex).
- Problem: given s, t, choose a simple s-t path whose removal (vertices: the residual graph is the induced subgraph on the
  remaining vertices) minimises the size of the largest connected component; variants bound the path length, maximise the
  number of components and add path cost.
- Relation: a path chosen for the damage its removal does. Differences: vertices are removed, so s and t disappear and
  nothing is separated from anything in particular; the objective is fragmentation of the whole graph; the path is not
  required to be short in the base problem; the work is MIP and metaheuristics, no complexity theorem seen.
- Recommendation: MENTION in the report; an optional clause in the Introduction's paragraph on interdiction.
  The earlier log knew this problem from a search summary only; the definition is now read in two primary texts.

#### 3.2 Minimum maximal flow (uncontrollable flows)

- References: Jianming Shi, Yoshitsugu Yamamoto. A global optimization method for minimum maximal flow problem. Acta
  Mathematica Vietnamica 22(1) (1997) 271-287 (zbMATH Open record 1140467; not read). Maiko Shigeno, I. Takahashi,
  Y. Yamamoto. Minimum Maximal Flow Problem: An Optimization over the Efficient Set. Journal of Global Optimization 25(4)
  (2003) 425-443, DOI 10.1023/A:1022523615101 (Springer page). Kuan Lu, Shinji Mizuno, Jianming Shi. A mixed integer
  programming approach for the minimum maximal flow. Journal of the Operations Research Society of Japan 61(4) (2018)
  261-271, DOI 10.15807/jorsj.61.261 (Crossref). Le Dung Muu, Jianming Shi. D.C. Optimization Methods for Solving Minimum
  Maximal Network Flow Problem. RIMS Kokyuroku 1349 (2004) 83-93 (data from the PDF footer).
- Read: Lu et al., pages 261-263 (J-STAGE PDF); Muu and Shi, pages 83-85 (RIMS PDF); abstract of Shigeno et al.
- Problem: directed network with capacities; a feasible flow x is maximal if no feasible flow y >= x, y != x exists;
  minimise the flow value over maximal flows. Stated NP-hard, attributed to Shi and Yamamoto 1997 (proof not seen).
  Motivation: flow that cannot be reduced once sent (Iri's "uncontrollable flows"). The introductory example of Muu and Shi
  is a unit-capacity network in which one unit sent along a path through the middle arc blocks the second unit.
- Relation: a u-v path whose edge set is a u-v cut is, in a unit-capacity network, an integral flow of value one that
  cannot be augmented without rerouting. SSP asks whether a shortest path is such a flow.
- Precise difference: real-valued flows on directed networks; the objective is the flow value, not path length plus
  remaining connectivity; maximality as defined also forbids adding flow on a cycle; no shortest-path condition.
  The minimum maximal flow value is not cp(u,v) and "value 1" is not SSP.
- Recommendation: MENTION in the report. A citation is justified only if the Introduction wants the flow interpretation of
  a separating path. `TODO(verify)`: the hardness proof of Shi and Yamamoto, and whether it works for unit capacities and
  integral flows (if it did, it would be a hardness result for "some path is a cut" without the shortest-path condition).

#### 3.3 Path removal in highly connected graphs (Lovasz)

- References (Crossref): Guantao Chen, Ronald J. Gould, Xingxing Yu. Graph Connectivity After Path Removal. Combinatorica
  23(2) (2003) 185-203, DOI 10.1007/s003-0018-z. Ken-ichi Kawarabayashi, Orlando Lee, Xingxing Yu. Non-Separating Paths in
  4-Connected Graphs. Annals of Combinatorics 9(1) (2005) 47-56, DOI 10.1007/s00026-005-0240-4. Ken-ichi Kawarabayashi,
  Orlando Lee, Bruce Reed, Paul Wollan. A weaker version of Lovasz' path removal conjecture. Journal of Combinatorial
  Theory, Series B 98(5) (2008) 972-979, DOI 10.1016/j.jctb.2007.11.003.
- Read: abstracts (Springer pages for the first two; CORE API record for the third).
- Content: Lovasz conjectured (1975) a function f(k) such that every f(k)-connected graph has, for any two vertices, a path
  P between them with G - V(P) k-connected; f(1) = 3 follows from a result of Tutte; f(2) = 4 except for double wheels;
  an edge-removal weakening is proved for induced cycles through a given edge.
- Relation: sufficient conditions for a path whose removal keeps the graph connected. Extremal statements, vertex removal
  in the main conjecture, no shortest-path condition, no algorithmic question.
- Recommendation: SKIP in the article (the manuscript already contrasts with non-disconnecting paths); report only.

#### 3.4 Other

- Giorgio Ausiello, Lorenzo Balzotti, Paolo Giulio Franciosa, Isabella Lari, Andrea Ribichini. Interdiction in network
  maximum flow and related problems: A survey. Computer Science Review 60 (2026) 100867. DOI 10.1016/j.cosrev.2025.100867
  (Crossref). Abstract read (OpenAlex): variants of max-flow interdiction, vitality. A path as the interdicted set is not
  named in the abstract; full text not accessible. A place to check with library access. MENTION.
- Stefanie Gerke, Balazs F. Mezei, Gregory B. Sorkin. Successive shortest paths in complete graphs with random edge
  weights. Random Structures & Algorithms, DOI 10.1002/rsa.20962, arXiv 1911.01151 (volume and pages not looked up).
  Abstract read: in K_n with random weights the k-th shortest path edge-disjoint from the earlier ones costs about
  2k/n + ln n/n. Different model from G(n,p) with unit lengths; no cut. SKIP.

### Angle 4. Notions with nearby names

One line each: definition as read, and why it is not a cut-path.

| Notion | Source read | Definition | Why it differs |
|---|---|---|---|
| Shortest-path separators, k-path separable graphs | Ittai Abraham, Cyril Gavoille. Object location using path separators. PODC 2006, 188-197, DOI 10.1145/1146381.1146411 (abstract). Emilie Diot, Cyril Gavoille. Path Separability of Graphs. FAW 2010, LNCS, 262-273, DOI 10.1007/978-3-642-14553-7_25 (abstract). Emilie Diot, Cyril Gavoille. On the Path Separability of Planar Graphs. Electron. Notes Discrete Math. 34 (2009) 549-552, DOI 10.1016/j.endm.2009.07.091 (HAL abstract). | A graph is k-path separable if removing at most k shortest paths (their vertices), recursively, leaves components of at most half the size; every weighted planar graph is halved by three shortest paths. The planar fact is usually credited to Thorup, J. ACM 51(6) (2004) 993-1024, DOI 10.1145/1039488.1039493; its abstract does not state it, `TODO(verify)`. | Vertices are removed; the separation is balanced and global, not between two given vertices; the paths join arbitrary endpoints and are not u-v paths. |
| Isometric path cover | Mael Dumas, Florent Foucaud, Anthony Perez, Ioan Todinca. On graphs coverable by k shortest paths. SIAM J. Discrete Math. 38(2) (2024) 1840-1862, DOI 10.1137/23M1564511 (arXiv 2206.15088 abstract). | Cover all vertices (or edges) by k shortest paths. | A covering problem; nothing is separated. |
| Geodesic separators | no source | I found no established notion under this name (arXiv phrase searches). | - |
| Separating path systems | Victor Falgas-Ravry, Teeradej Kittipassorn, Daniel Korandi, Shoham Letzter, Bhargav P. Narayanan. Separating path systems. Journal of Combinatorics 5(3) (2014) 335-354, DOI 10.4310/JOC.2014.v5.n3.a4 (arXiv 1311.5051 abstract). | A family of paths that is a separating system of the edge set: the paths distinguish the edges from one another. | "Separating" refers to telling edges apart, not to disconnecting. |
| Secluded paths | Shiri Chechik, M. P. Johnson, Merav Parter, David Peleg. Secluded Connectivity Problems. Algorithmica 79(3) (2017) 708-741, DOI 10.1007/s00453-016-0222-z (abstract). Rene van Bevern, Till Fluschnik, Oxana Yu. Tsidulko. Parameterized algorithms and data reduction for the short secluded s-t-path problem. Networks 75(1) 34-63, DOI 10.1002/net.21904 (abstract; Crossref gives 2019, print year `TODO(verify)`). Max-Jonathan Luckow, Till Fluschnik. On the computational complexity of length- and neighborhood-constrained path problems. Inf. Process. Lett. 156 (2020) 105913, DOI 10.1016/j.ipl.2019.105913 (arXiv 1808.02359 abstract). | An s-t path with few vertices in its closed neighbourhood (exposure); Short Secluded Path bounds the number of path vertices and of neighbours. | The path is paid for together with its neighbourhood, which isolates the path from the rest of the graph; it is a vertex set around the path, not a u-v cut, and u, v lie on the same side. |
| Cut paths | Cairo et al., block 2.2 | A walk contained in every u-v walk. | See 2.2. |
| Non-separating, non-disconnecting paths | already in the manuscript; Chen, Gould, Yu (3.3) use "nonseparating" for G - V(P) connected | Path whose removal keeps the graph connected. | Opposite requirement. |

Recommendation for the Introduction: a sentence excluding path separators and secluded paths is optional; I would not
add more than the "cut paths" clause of 2.2. None of these needs a citation for the mathematics.

### Angle 5. Status in 2026

(i) Network Diversion, general undirected graphs, edge version: still open in every source found.

- Matthias Bentert, Pal Gronas Drange, Fedor V. Fomin, Steinar Simonnes. Planar Network Diversion. SEA 2025, LIPIcs 338,
  6:1-6:14, DOI 10.4230/LIPIcs.SEA.2025.6 (DataCite record opened in this pass; the text was checked by the earlier pass
  of today in arXiv 2502.16714v1, see `session-2026-10-10/related-work-check.md`; I did not reread it).
- Matthias Bentert, Fedor V. Fomin, Fanny Hauser, Saket Saurabh. The parameterized complexity landscape of two-sets
  cut-uncut. Theoretical Computer Science 1065 (2026) 115726, DOI 10.1016/j.tcs.2025.115726 (Crossref). Read: arXiv
  2408.13543v1, pages 3 and 18: the complexity of Network Diversion on undirected graphs is called widely open and is
  repeated as a long-standing open question in the conclusion. Journal text not read.
- Batya Kenig. Connectivity-Preserving Important Separators: A Framework for Cut-Uncut Problems. arXiv 2511.15849v5,
  updated 2026-10-07. Text searched for "diversion" and "open": names network diversion among cut-uncut problems, claims no
  resolution. Its last abstract sentence (an FPT algorithm for a minimum minimal s,t-vertex-separator whose source side
  contains a set A and avoids a set B) is a parameterized result on a vertex version, not a classification.
- arXiv API, newest first, `all:"network diversion"` and `abs:"Network Diversion" AND (abs:cut OR abs:graph)`: nothing
  after 2502.16714. Semantic Scholar lists no paper citing arXiv 2502.16714.
- Conclusion: "state that its complexity on general undirected graphs is open" remains accurate on 2026-10-10. Repeat at
  submission.

(ii) Published versions.

- Mao, Shortest non-separating st-path on chordal graphs: arXiv 2101.03519v3 (2021-02-09), no journal reference or DOI in
  the arXiv record; comment field says it was prepared for ICALP 2021; Semantic Scholar and Google Scholar list arXiv only;
  Crossref title search from 2021 on: no match. No published version found.
- Abhinav, Bandopadhyay, Banik, Kobayashi, Nagano, Otachi, Saurabh: MFCS 2022, LIPIcs 241, 6:1-6:15,
  DOI 10.4230/LIPIcs.MFCS.2022.6 (DataCite). Crossref search restricted to journal articles from 2023 on: no match.
  OpenAlex title phrases "non-separating path", "non-disconnecting": no journal item. No journal version found.
- Kobayashi, Nagano, Otachi, arXiv 2202.09718v1: no journal reference; merged into the MFCS paper.
- New since the earlier check: Hon, Tsai, Yang 2025 (block 2.1) gives a published NP-completeness proof for the existence
  of a non-disconnecting path.

### Angle 6. DBLP

- One request to `https://dblp.org/search/publ/api?q=non-separating%20path&format=json&h=40`: the server answered with the
  bot-check page ("Making sure you're not a bot!", Anubis). Not bypassed; the other four queries were not sent. The mirror
  `dblp.dagstuhl.de` was not tried.
- Substitutes: OpenAlex exact title-phrase search for the five phrases (all returned, see log); Semantic Scholar paper
  search (one phrase answered, four returned HTTP 429 twice).
- From the title-phrase search: "cut-path" in a title gives the author's own thesis record (OpenAlex: "Min Cut-Path",
  Norbert Michel, 2025, National Repository of Grey Literature) and Cairo et al.; "separating shortest path": 0;
  "disjoint counterpart": Xu et al. 2006 and an OFC 2004 paper of Xu, Chen, Qiao; "min-min disjoint": Guo and Shen 2013.

## 3. Comparison table

| Related work or problem | Main known results | Relationship to Min Cut-Path | Precise difference | Implication for the novelty claim |
|---|---|---|---|---|
| Two disjoint paths, one shortest (2D1SP), Eilam-Tzoreff 1998 | NP-complete, vertex- and edge-disjoint, directed and undirected, unit lengths (Claims 1, 3) | mirror of SSP with two terminal pairs | removal of the shortest path must leave the other pair connected; two pairs | none against novelty; must be cited and contrasted (same journal, same style of reduction) |
| Min-Min disjoint paths, Xu et al. 2006; Guo, Shen 2012, 2013 | NP-hard; no K-approximation (general lengths); edge-disjoint: NP-complete on planar digraphs even with equal costs, NP-hard on undirected graphs; vertex-disjoint: polynomial on planar graphs | optimisation form of the mirror problem MMS for one pair | wants a short path with r(P) >= 1; SSP wants a shortest path with r(P) = 0; objective is one path length, not path plus cut | none against novelty; cite as the problem SSP is the opposite of |
| One-pair mirror, Radermacher, Rutter 2018 | stated NP-hard (modification of Eilam-Tzoreff, no proof); planar case open | MMS itself | as above | none; shows the mirror is known to the graph-drawing community |
| Edge-Disjoint (<= k1, any)-Paths, Cai, Ye | FPT in k1, no polynomial kernel | parameterized mirror | as above; parameter is the short path's length | none; FPT of Min Cut-Path in the solution size is a different statement |
| Non-disconnecting / non-separating paths: Mao; Abhinav et al.; Hon, Tsai, Yang 2025 | existence NP-hard (now with a published proof on semi-Eulerian graphs); shortest one FPT in length (edge version), W[1]-hard (vertex version) | opposite requirement, whole graph must stay connected | G - E(P) connected versus no u-v path in G - E(P) | already handled in the Introduction; add the 2025 reference |
| Critical Disruption Path, Granata et al. | MIP, branch-and-price, metaheuristics | a path removed to damage the network | vertex removal; objective is the largest component; no cut between two vertices | none |
| Minimum maximal flow, Shi, Yamamoto and followers | NP-hard (stated); global-optimisation algorithms | a separating path is an integral non-augmentable flow of value one | real flows, directed, objective is the flow value, no shortest-path condition | none; hardness proof unread, see `TODO(verify)` in 3.2 |
| Lovasz path removal | existence of paths whose removal keeps k-connectivity in highly connected graphs | opposite direction, extremal | vertex removal, no algorithmic problem | none |
| Cut paths, Cairo et al. 2023/2026 | linear-time verification, enumeration | name only | a walk lying on all u-v walks in a digraph | none; needs a disambiguating clause |
| Path separators, isometric path cover, separating path systems, secluded paths | various | names only | see Angle 4 | none |
| Network Diversion | polynomial on planar graphs; open on general undirected graphs | cut with a prescribed edge (already cited) | no path in the solution | statement "open" still accurate |

## 4. Search log

All rows: 2026-10-10. Counts are hits reported by the source. "0" rows are searches that found nothing.

| Date | Question | Source | Queries exactly as entered | Found | Conclusion |
|---|---|---|---|---|---|
| 2026-10-10 | Min-Min / shortest path with a disjoint counterpart: definitions, hardness, relation to SSP | web search | *"min-min" disjoint paths problem "shortest path" "disjoint counterpart" NP-complete Xu Chen Xiao Qiao*; *Guo Shen "On Finding Min-Min Disjoint Paths" Algorithmica pdf "edge-disjoint" "planar" NP-complete undirected proof*; *"shortest path with a disjoint counterpart" pdf Xu Chen Xiong Qiao He "conflicting link set" "trap" definition*; *"min-min" disjoint path pair NP-complete undirected "unit" OR "equal" edge costs "edge-disjoint" Guo Shen planar digraphs pdf full text*; *"On finding disjoint paths in single and dual link cost networks" Xu Chen Xiong Qiao He INFOCOM 2004 pdf*; *"Finding disjoint paths with related path costs" Bhatia Kodialam Lakshman pdf "min-min" NP-hard undirected "edge disjoint" approximation*; *Dahai Xu "finding the shortest path with a disjoint counterpart" filetype:pdf "Min-Min" "Theorem 1" NP-complete "link-disjoint" directed undirected*; *Longkun Guo Hong Shen "Min-Min" "edge-disjoint" undirected "NP-complete" "unit" OR "uniform" edge costs open problem planar undirected "edge disjoint Min-Min" later results 2014..2024*; (extended mode) *"Min-Min" "edge-disjoint" "undirected" Guo Shen "3SAT" "shorter path" "zero" OR "cost 0" reduction "NP-hard" "no K-approximation" explanation later paper survey "Min-Min problem is NP-hard" undirected unit weights*; *"trap topology" shortest path first "no disjoint" backup path exists although two disjoint paths exist definition "trap" survivable routing Suurballe "active path first"*; *"avoidable trap" OR "real trap" "active path" "disjoint backup path" definition Xu Xiong Qiao Li "Trap avoidance and protection schemes in networks with shared risk link groups" Journal of Lightwave Technology 2003* | Xu et al. 2006; Guo, Shen 2011-2013; Bhatia et al. 2006; INESC Coimbra report 5/2006 (Gomes, Craveirinha, Jorge; pp. 1-4 read, secondary); patents on trap-free disjoint paths (not opened) | Publisher abstracts opened for every claim used; no full text of Xu et al. or Guo-Shen reachable |
| 2026-10-10 | Two disjoint paths, one of them shortest | web search | *"two disjoint paths" "one of them" OR "one of which" "is a shortest path" NP-complete undirected graph Eilam-Tzoreff "disjoint shortest paths problem"*; *Cai Ye "Finding two edge-disjoint paths with length constraints" abstract parameterized "edge-disjoint" "length at most" one path unconstrained FPT*; *"shortest path" "has no edge-disjoint" OR "without an edge-disjoint" counterpart "every shortest path" graph theory "blocks all" s-t paths "blocking path" OR "bridging path" complexity undirected unit lengths*; *"edge-disjoint" two s-t paths "one of which is a shortest path" OR "one of them is a shortest path" same terminals undirected unweighted polynomial OR NP-complete "shortest path with a disjoint" theorem* | Eilam-Tzoreff 1998; Cai, Ye (arXiv 1509.05559); Radermacher, Rutter (arXiv 1807.11711) | 2D1SP verified in the journal PDF; the one-pair form is a remark in Radermacher and Rutter |
| 2026-10-10 | Same, arXiv | arXiv API (`export.arxiv.org/api/query`, relevance order) | `all:"min-min" AND all:"disjoint paths"` (0); `abs:"disjoint counterpart"` (1, unrelated); `abs:"disjoint paths" AND abs:"shorter path"` (1, unrelated); `abs:"min-min" AND abs:disjoint AND abs:paths` (0); `abs:"disjoint paths" AND abs:"shortest path" AND abs:"one of"` (12); `abs:"edge-disjoint" AND abs:"one of which is a shortest"` (0); `abs:"disjoint" AND abs:"shortest path" AND abs:"min-min"` (0); `abs:"disjoint" AND abs:"shortest path" AND abs:"no disjoint"` (77, first 12 listed); `abs:"two disjoint paths" AND abs:"shortest path" AND abs:"NP-complete"` (0); `abs:"edge-disjoint" AND abs:"shortest path" AND abs:"backup" AND abs:"NP-hard" AND abs:"trap"` (0); `abs:"trap topology" OR abs:"trap topologies" OR abs:"trap problem" AND abs:"disjoint"` (14, physics); `all:"conflicting link set" OR all:"conflict set" AND all:"disjoint path" AND all:"active path"` (0); `abs:"shortest path" AND abs:"edge cut" AND abs:"contains" AND abs:"NP-complete"` (1, unrelated); `ti:"Forcing a unique minimum spanning tree and a unique shortest path"` (1: arXiv 2509.24309, not assessed) | disjoint shortest paths papers (Lochet 1912.10486; Bentert et al. 2007.12502; Pilipczuk et al. 2505.03353; Choudhary et al. 2509.14588); Gerke et al. 1911.01151; Ekim, Farley 2606.27451 (abstract read, unrelated) | The Min-Min literature is not on arXiv; nothing on a shortest path without a disjoint counterpart |
| 2026-10-10 | Bibliographic records and abstracts | Crossref API (`works/<DOI>`, `query.bibliographic`); OpenAlex (`works/<id>`); DataCite API; CORE API v3; University of Adelaide repository API; HAL API; zbMATH Open API; Springer Link pages | Crossref DOIs: 10.1109/tnet.2005.863451; 10.1007/s10878-006-8906-y; 10.1007/s00453-012-9656-0; 10.1016/j.tcs.2011.12.009; 10.1109/iccrd.2011.5764102; 10.1007/978-3-642-21204-8_32; 10.1109/paap.2011.15; 10.1016/s0166-218x(97)00121-2; 10.1016/j.comgeo.2021.101843; 10.1007/978-3-030-04414-5_29; 10.1016/j.tcs.2019.07.009; 10.1007/978-3-662-53536-3_6; 10.1145/3790095; 10.4230/LIPIcs.STACS.2023.17 (404, then DataCite); 10.1016/j.cosrev.2025.100867; 10.15807/jorsj.61.261; 10.1016/j.endm.2009.07.091; 10.1007/s11227-025-07064-6. Crossref text: *On the complexity of and algorithms for finding the shortest path with a disjoint counterpart*; *Bhatia Kodialam Lakshman Finding disjoint paths with related path costs* (first try HTTP 429); *Eilam-Tzoreff The disjoint shortest paths problem Discrete Applied Mathematics 1998*; *Cai Ye Two edge-disjoint paths with length constraints Theoretical Computer Science*; *Yang Zheng Lu Finding two disjoint paths in a network with min-min objective function*; *Network interdiction via a Critical Disruption Path Branch-and-Price algorithms Granata Steeger Rebennack*; *A weaker version of Lovasz path removal conjecture Kawarabayashi Lee Reed Wollan*; *Chen Gould Yu Graph connectivity after path removal Combinatorica*; *Supereulerian Testing on Semi-Eulerian Graphs Hon Tsai Yang*; the eight angle-4 title strings (Thorup; Abraham Gavoille; Diot Gavoille; Chechik Johnson Parter Peleg; van Bevern Fluschnik Tsidulko; Luckow Fluschnik; Falgas-Ravry et al.; isometric path cover Chakraborty et al.). DataCite: 10.4230/LIPIcs.STACS.2023.17; 10.4230/LIPIcs.MFCS.2022.6; 10.4230/LIPIcs.SEA.2025.6. CORE: `doi:"10.1016/j.tcs.2011.12.009"`; `title:"The disjoint shortest paths problem"`; `doi:"10.1016/j.jctb.2007.11.003"`. Adelaide: `server/api/pid/find?id=2440/72964`. HAL: `halId_s:hal-00408228`. zbMATH: `ti:"minimum maximal flow"` (6) | all references of Section 2 | Records verified as stated in each block |
| 2026-10-10 | Forward citations of the closest papers | Semantic Scholar Graph API (`paper/<id>/citations`); OpenAlex (`filter=cites:`); Google Scholar | S2: arXiv:2101.03519 (2); arXiv:2202.09718 (0); DOI:10.4230/LIPIcs.MFCS.2022.6 (1); DOI:10.1002/net.21832 (22); arXiv:1804.09155 (22, same list). OpenAlex cites: W3120639636 (0); W4221149015 (0); W2888538681 (14); W2151715608 (94); W2066450989 (18); W2128090945 (62). Google Scholar: `q="Parameterized Complexity of Non-Separating and Non-Disconnecting Paths and Sets"` (cited by 3, list opened); `q="Shortest non-separating st-path on chordal graphs"` (cited by 2); `q="Finding shortest non-separating and non-disconnecting paths"` (no count shown) | Hon, Tsai, Yang 2025; Cairo et al. (safety, cut paths); Ausiello et al. 2026; Granata, Sgalambro 2023; Cai, Ye; Radermacher, Rutter | No citing paper has a path whose removal must separate |
| 2026-10-10 | Later work on non-separating paths | web search; arXiv API (newest first) | web: *"non-separating" OR "non-disconnecting" "st-path" OR "s-t path" 2024 2025 2026 arXiv cites "Abhinav" "Kobayashi" "Otachi" parameterized path removal connectivity*. arXiv: `all:"non-separating path" OR all:"non-separating paths" OR all:"non-disconnecting paths" OR all:"nonseparating path"` (4); `ti:"Supereulerian" AND ti:"Semi-Eulerian"` (0); `abs:supereulerian AND abs:"semi-eulerian"` (0) | Mao; Kobayashi et al.; Fernandes et al. 1409.4239 (spanning trees with nonseparating paths); Wu 1105.5915 | Nothing new on arXiv after 2022 |
| 2026-10-10 | Path interdiction, removal of a path | arXiv API | `abs:"most vital path"` (0); `abs:"path interdiction" AND abs:"maximum flow"` (0); `abs:"removal of a path" AND abs:"connectivity" AND abs:"s-t"` (0); `abs:"path blocker"` (0); `abs:"removing a shortest path"` (0); `abs:"after removing" AND abs:"shortest path" AND abs:"minimum cut"` (0); `abs:"residual" AND abs:"edge connectivity" AND abs:"shortest path" AND abs:"removal"` (0); `abs:"interdict" AND abs:"path" AND abs:"disconnect" AND abs:"shortest path" AND abs:"attacker chooses a path"` (0); `abs:"shortest path" AND abs:"bridge" AND abs:"every edge" AND abs:"cut" AND abs:"path is a cut"` (0); `ti:"Interdiction" AND ti:"maximum flow" AND ti:survey` (0); `abs:"minimum maximal flow" OR abs:"smallest maximal flow" OR abs:"minimum blocking flow"` (0); `abs:"path removal conjecture" OR ti:"path removal"` (1, unrelated) | - | No arXiv paper on removing a path to cut or to reduce flow |
| 2026-10-10 | Same, OpenAlex free text | OpenAlex (`search=`) | *most vital path*; *path interdiction maximum flow remove a path*; *removal of an s-t path minimizes remaining maximum flow*; *minimum cut after removing a shortest path*; *residual connectivity after routing a path*; *path blocker graph*; *shortest path that is an edge cut*; *trap topology disjoint path active path no backup path exists*; *shortest path with no edge-disjoint alternative path*; *Network interdiction via a Critical Disruption Path: Branch-and-Price algorithms*; *A weaker version of Lovász' path removal conjecture*; *finding two disjoint paths in a network with min-min objective function* | most vital node or edge of a shortest path (Nardelli, Proietti, Widmayer; Malik et al.); Khachiyan et al.; Critical Disruption Path (3 papers); Miller et al. (Force Path Cut); Ma, A note on Lovasz removable path conjecture (J. Comb. 2011, title only); Clow, Haxell, Mohar, A Counterexample to a Conjecture of Lovasz (Combinatorica 2026, title only, not opened) | Only single vital edges or nodes, never a vital path |
| 2026-10-10 | Minimum maximal flow | web search; OpenAlex title phrases; J-STAGE; RIMS; Springer | web: *"minimum maximal flow" problem NP-hard network "maximal flow" not maximum "uncontrollable flow" Iri Shi Yamamoto integral unit capacities edge-disjoint paths*. OpenAlex `title.search`: "minimum maximal flow" (10); "maximal flow problem" (30); "uncontrollable flow" (2: Iri 1998, Comput. Math. Appl., DOI 10.1016/S0898-1221(98)00077-7, title only); "min-max disjoint paths" (2); "maximal set of edge-disjoint paths" (0); "minimum blocking flow" (0) | Shi, Yamamoto 1997; Shigeno et al. 2003; Lu et al. 2018; Muu, Shi 2004; Yamamoto, Zenke 2005, 2007 (records only) | A relative, not the same; hardness proof unread |
| 2026-10-10 | Nearby names (angle 4) | arXiv API; OpenAlex; Springer; HAL | arXiv: `ti:"Secluded Connectivity Problems"` (2); `ti:"isometric path cover"` (0); `abs:"isometric path cover"` (7); `abs:"geodesic" AND abs:"separator" AND abs:"shortest path" AND abs:"balanced"` (1, unrelated); `abs:"shortest path separator" OR abs:"shortest-path separator" OR abs:"shortest path separators"` (6, users of the tool, none defines a new notion); id look-ups 1808.02359, 1311.5051, 2206.15088 | references of the Angle 4 table | Definitions read in abstracts |
| 2026-10-10 | Exact phrases in titles and abstracts (DBLP substitute) | OpenAlex `filter=title.search:"..."`; OpenAlex `filter=abstract.search:"..."` | title: "non-separating path" (2); "nonseparating path" (2); "separating shortest path" (0); "cut-path" (18); "disjoint counterpart" (2); "min-min disjoint" (1); "min-min problem" (9); "separating path" (118); "non-disconnecting" (6); "disconnecting path" (2); "most vital path" (0); "critical disruption path" (3); "Supereulerian Testing on Semi-Eulerian Graphs" (1). abstract: "shortest path whose removal" (1: Diot, Gavoille 2009); "unavoidable shortest path" (0); "shortest path with a disjoint counterpart" (0); "one of them is a shortest path" (5, unrelated); "two disjoint paths one shortest" (0); "disjoint counterpart" (5, unrelated); "path whose removal disconnects" (0); "path whose edges form a cut" (0) | author's thesis record; Cairo et al.; Kawarabayashi, Lee, Yu 2005; Wu 2012; Fernandes et al. 2015; separating path systems (many) | No title or abstract with a separating shortest path |
| 2026-10-10 | Same phrases, DBLP | DBLP publication search API | *non-separating path* | - | Failed: bot-check page (Anubis), HTTP 200 with HTML. Not bypassed; *separating shortest path*, *cut-path*, *disjoint counterpart*, *min-min disjoint paths* not sent |
| 2026-10-10 | Same phrases, Semantic Scholar | Semantic Scholar `paper/search` | *min-min disjoint paths* (answered, 20 listed); *non-separating path*, *separating shortest path*, *cut-path graph*, *shortest path disjoint counterpart* (HTTP 429, two rounds) | Shan et al. 2025; Yang, Zheng, Katukam 2003 (record without venue); Bhaskar et al., ESA 2025 (min-max disjoint paths, title only) | Rate-limited; repeat |
| 2026-10-10 | Network Diversion status 2026 | arXiv API (newest first); Semantic Scholar citations; web search (extended); arXiv PDFs | arXiv: `all:"network diversion"` (38, mostly word-stem noise); `abs:"minimal cut" AND abs:"containing" AND abs:"given edge" OR abs:"cut-uncut" OR abs:"two-sets cut-uncut"` (0); `abs:"Network Diversion" AND (abs:cut OR abs:graph)` (6). S2 citations: arXiv:2502.16714 (0); arXiv:2305.01314 (7); DOI:10.1002/net.21514 (11). web: *"Network Diversion" undirected graphs "NP-hard" OR "polynomial-time" 2026 arXiv "minimal s-t cut" containing edge open problem settled Bentert Drange Fomin*. Text search in arXiv 2511.15849v5 and 2408.13543v1 for *diversion*, *open* | Bentert et al. SEA 2025; Bentert et al. TCS 2026 (arXiv 2408.13543); Kenig arXiv 2511.15849v5 and 2506.03612 (WG 2025); Marin, Watrigant arXiv 2604.26533; Dehaleesan et al. arXiv 2607.03266 (diverse minimum cuts, unrelated) | Still open |
| 2026-10-10 | Published versions of Mao and of Abhinav et al. | arXiv API id look-ups; Semantic Scholar paper records; Crossref with filters; Google Scholar | arXiv ids 2101.03519, 2202.09718. S2: `arXiv:2101.03519`, `DOI:10.4230/LIPIcs.MFCS.2022.6`. Crossref: *Parameterized Complexity of Non-Separating and Non-Disconnecting Paths and Sets* with `from-pub-date:2023-01-01,type:journal-article`; *Shortest non-separating st-path on chordal graphs Mao* with `from-pub-date:2021-01-01`; *Finding shortest non-separating and non-disconnecting paths Kobayashi Nagano Otachi* with `from-pub-date:2022-01-01` | - | None found |
| 2026-10-10 | Open full texts | Internet Archive availability API; CORE; ScienceDirect; Elsevier API; J-STAGE; RIMS; White Rose; arXiv | `archive.org/wayback/available?url=core.ac.uk/download/pdf/82288569.pdf` (snapshot 2024-12-05, read); `...81109985.pdf` (no snapshot); `core.ac.uk/download/81109985.pdf` (challenge page, HTTP 403); `sciencedirect.com/science/article/pii/S0304397511009698` (HTTP 403); `api.elsevier.com/content/article/pii/S0304397511009698` (HTTP 400/429 without key); `link.springer.com/article/10.1007/s00453-012-9656-0` (abstract and references only); `beta.math.ac.vn/uploads/files/9701271.pdf` (no data) | Eilam-Tzoreff 1998 (pp. 113-120); Lu et al. 2018; Muu, Shi 2004; Granata, Sgalambro 2016; arXiv 1509.05559, 1807.11711, 2303.00527, 2408.13543, 2511.15849 | See Limitations |

## 5. Limitations

- Full texts not read: Xu et al. 2006 (IEEE paywall); Guo and Shen, Algorithmica 2013 (paywall), TCS 2012 (open archive at
  ScienceDirect, but HTTP 403 for the fetch tool; the CORE copy sits behind a challenge page that I did not try to pass),
  FAW-AAIM 2011, ICCRD 2011, PAAP 2011; Shi and Yamamoto 1997; Granata, Steeger, Rebennack 2013; the journal versions of
  Radermacher and Rutter, of Cai and Ye and of Bentert, Fomin, Hauser, Saurabh; Ausiello et al. 2026; Hon, Tsai, Yang 2025
  (abstract only). Statements about these rest on publisher or repository abstracts, and say so.
- Eilam-Tzoreff 1998 was read from an Internet Archive snapshot of the CORE copy, pages 113-120 only; figures were not
  legible in the extracted text; Sections 4-5 not read.
- DBLP: bot check again, not bypassed. Semantic Scholar search: rate-limited for four of five phrases. Google Scholar
  answered four requests with a "try again later" banner; its lists may be incomplete.
- OpenAlex shows zero citations for the arXiv and LIPIcs records of Mao, Kobayashi et al. and Abhinav et al.; the forward
  trail for these rests on Semantic Scholar and Google Scholar (2 + 0 + 3 citing items).
- Citing papers were judged by title; abstracts were read for those named in Section 2.
- The six-vertex example in 1.0 and the reading of "supereulerian on semi-Eulerian graphs = non-disconnecting path" in 2.1
  are my own derivations, not statements of a source.
- No text addressed to AI agents was found in any page or PDF opened. The Semantic Scholar API attaches a licence notice
  with an e-mail placeholder to some records; it was ignored.
- Nothing was added to any `.bib` file or reading note. Every citation proposed here still needs a status line in the
  canonical `.bib` and a reading note before it enters the manuscript.
