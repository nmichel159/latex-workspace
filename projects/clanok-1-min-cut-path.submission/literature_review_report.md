# Min Cut-Path Problem: literature review report (2026-10-10)

Manuscript: `projects/clanok-1-min-cut-path/main.tex` (article 1, target Discrete Applied Mathematics).
Changed by this review: the Abstract, Section 1, two new entries in `references.bib`. Sections 2-9 are unchanged.
Working files of the review (full query logs, per-paper blocks): `literature-review-2026-10-10/A-bib-audit.md`,
`B1-path-removal.md`, `B2-path-and-cut.md`, beside this report.

## 1. Result in ten lines

1. **Same problem: not found**, under this name or in any equivalent form (set containing a path and a cut;
   shortest path that is a cut; `min_P (|P| + c_{G - P}(u,v))`; clutter and blocker; path set and cut set; winning and
   blocking coalition). The only hits are the author's own master's thesis and CSGT 2026 abstract.
2. **One statement of the manuscript is a known theorem and was not attributed:** `c(u,v) = min{deg u, deg v}` in
   graphs of diameter at most two (first half of Corollary 5.7) is due to Fricke, Oellermann and Swart (2000,
   unpublished), printed as Theorem 11 in Stuart (2009). Now attributed in the Introduction; a sentence for
   Section 5 is proposed in section 7.
3. **Lemma 6.1 (cactus graphs) is folklore.** The Introduction now says so; it is not counted as a contribution.
4. **Bibliography:** all 20 entries were compared field by field with primary records; 18 agree, 2 differ in a
   documented way (article number of Marx et al.; year of Frieze and Karoński). No entry had to be corrected.
5. **Section 8 (fixed-parameter tractability): no error found.** One gap of rigor (the function `f` is called
   computable in the definition and the proof does not say why it is) and one missing remark on the model of the
   proof; both with a proposed sentence in section 6. Not applied.
6. **Added references (3):** `Stuart2009Eavesdropping`, `Baier2010LengthBounded`, `EilamTzoreff1998Disjoint` (a
   mirror problem published in Discrete Applied Mathematics that the manuscript did not mention). No reference
   removed.
7. **Novelty sentence** now reads "has not been studied by other authors"; the thesis is still not cited (author's
   decision of 2026-10-09). This is the main literature-related risk (section 9).
8. The random-graph theorem follows from two cited bounds and `cp >= c`; the Introduction now says so.
9. The FPT proof uses the treewidth reduction of Marx, O'Sullivan and Razgon and meets the obstacle they meet for
   connected separators; the Introduction now says so.
10. Not searched: DBLP (bot check), Google Scholar, MathSciNet. Several publisher pages refused access; what rests
    on a preprint or an author's copy is marked.

## 2. Scope, date and method

- Date of all searches: 2026-10-10. Earlier logged searches (2026-10-07 to 2026-10-10, about 80 queries) are in
  `knowledge/literature/searches.md`; they were not repeated. New queries of this review: the log tables of the
  three working files (copied into `knowledge/literature/searches.md`).
- Sources: Crossref, DataCite, OpenAlex and arXiv APIs, zbMATH Open, DROPS, DML-CZ, publisher catalog pages, authors'
  pages, web search. Refused or bot-checked, not bypassed: ACM Digital Library, ScienceDirect, Wiley, Taylor and
  Francis, SpringerLink (login redirect), DBLP, CORE, MIT Press.
- New angles of this review: (a) the bibliography, entry by entry; (b) paths whose removal separates or keeps
  connectivity, disjoint paths one of which is shortest, path interdiction, forward citations of the closest
  papers; (c) abstract formulations (clutters and blockers, simple games, reliability, matroid ports), classical
  relations between `c` and `d`, cuts with a connecting structure, and results the manuscript proves itself.
- A statement about a paper below rests on the text named with it. "Record only" means that the bibliographic
  record was verified and the text was not read.

## 3. Bibliography audit (20 entries before the review)

All 20 entries are cited, none is missing, none is duplicated, and every project entry equals the canonical one.
Details per entry: `A-bib-audit.md`, section 2.

| Key | Verdict | Note |
|---|---|---|
| `Bollobas2001`, `Diestel2025`, `Karp1972Reducibility`, `GomoryHu1961`, `henzinger1997faster`, `itai1979maximum`, `Mehlhorn2017Certifying`, `NagamochiKameda1996`, `ChungLu2001`, `Komusiewicz2020MatchingCut`, `LeLe2019MatchingCut`, `Feige1998Threshold`, `Bazgan2019MostVital` | agree | Crossref (and publisher page where it opened) |
| `Abhinav2022NonSeparating`, `Bentert2025NetworkDiversion` | agree | DROPS and DataCite; no journal version found |
| `Mao2021NonSeparating` | agrees | arXiv v3 (2021-02-09), no journal reference, no published version found |
| `Cook1971Complexity` | agrees | capitalization of the printed title not confirmed (Crossref has sentence case) |
| `Cormen2022` | agrees | distributor catalog and Open Library; the MIT Press page refused access |
| `Marx2013Separators` | differs between records | Crossref and OpenAlex: pages 1-35, no article number; the first author's publication list: `9(4):30`. The entry keeps `1--35` (primary record). The bibliography style cannot print an article number |
| `Frieze2016` | differs from Crossref | Crossref and the publisher page: 2015; the imprint page of the book: 2016 (checked 2026-10-10 earlier). Kept. Open: the `url` field points to the authors' PDF of 2026, whose numbering differs from the printed book that the text cites; recommended: delete the `url` field |

Statements cited by number:

| Citation in the text | Checked in | Result |
|---|---|---|
| `\cite[Corollary~3.3.5]{Diestel2025}` (new, Introduction) | author's preview of the 6th edition, Chapter 3 | Corollary 3.3.5 (ii), p. 75: edge version of Menger's theorem |
| `\cite[Theorem~11]{Stuart2009Eavesdropping}` (new, Introduction) | journal text (DML-CZ) | Theorem 11, p. 627 |
| Marx et al.: Section 2.1, Theorem 2.2, Definition 2.5, Proposition 2.7, Lemma 2.11, Remark 2.13 (Section 8) | arXiv v1 (the only arXiv version) and the first author's manuscript in journal format (2012-10-26) | identical numbers in both; the copy-edited ACM text could not be opened |
| `\cite[Proposition~2.1.2]{Feige1998Threshold}` (Section 4) | journal PDF (earlier check of 2026-10-10) | agrees |
| Frieze and Karoński: Exercise 1.4.8, Eq. (21.19), Section 1.1; Bollobás p. 169; Chung and Lu (Section 7) | earlier checks of 2026-10-10 | printed numbering agrees; journal numbering of Chung and Lu's Theorem 4 unverified (not cited by number) |

## 4. Closest related work

| Related work or problem | Main known results | Relationship to Min Cut-Path | Precise difference | Implication for the novelty claim |
|---|---|---|---|---|
| Non-disconnecting (non-separating) `u`-`v` paths: Mao 2021 (preprint); Abhinav et al., MFCS 2022 | existence NP-hard; shortest one FPT in its length; vertex version W[1]-hard | opposite requirement to Separating Shortest Path | the removal of the path must keep the graph connected; here it must separate `u` from `v` | no overlap; cited |
| Shortest Path Most Vital Edges, length-bounded cuts: Bazgan et al. 2019; Baier et al. 2010 | NP-hard; unit lengths: NP-hard on diameter three, linear on diameter two; minimum length-bounded edge cut NP-hard to approximate within 1.1377 for `L >= 4` | a cut-like set defined through path lengths | destroys the short paths and contains no path | no overlap; cited (Baier et al. added) |
| Network Diversion: Bentert et al. 2025 | minimal cut through a prescribed edge; `O(n log n)` on planar graphs; open on general undirected graphs | cut with prescribed content | one edge is prescribed, not a path; no path in the solution | no overlap; cited |
| Matching Cut: Le and Le 2019; Komusiewicz et al. 2020 | polynomial on diameter two, NP-complete on every fixed diameter at least three | cut with prescribed structure; same diameter frontier | condition on the cut alone | no overlap; cited |
| Treewidth reduction; connected `s`-`t` separators: Marx, O'Sullivan, Razgon 2013 (Section 3.3, Theorem 3.7 of arXiv v1) | all minimal separators of size at most `k` lie in a torso of bounded treewidth; connected separator of size at most `k` in linear FPT time | tool and model of the proof of Theorem 8.4 | vertex set that excludes `s`, `t`, must be connected as a whole and need not contain an `s`-`t` path; no theorem of the paper contains Min Cut-Path | FPT result is new as a statement; the technique is an application with one own step (weighted shortcuts) |
| Maximally local-edge-connected graphs: Fricke, Oellermann, Swart 2000 (unpublished); Hellwig and Volkmann 2004; Stuart 2009, Theorem 11; Plesník 1975 (global form) | diameter at most two implies `lambda(u,v) = min{d(u), d(v)}` for all pairs | equals the first half of Corollary 5.7; Lemma 5.3 is the case distinction of the known proof | says nothing about a path inside a cut or about `cp` | Corollary 5.7 (first half) is not new; Theorem 5.5 (`cp = c + d - 1`) stays new |
| Cactus characterizations: Marx and Végh 2015 (Proposition 3.7 of arXiv v2); Bruner, Mitra, Steiger 2024 (preprint) | no two vertices joined by three edge-disjoint paths, 2-edge-connected: cactus; "2-edge bottlenecked" iff two cycles share at most one vertex | neighbouring forms of Lemma 6.1 | none states exactly Lemma 6.1 | folklore; not a contribution |
| Menger; Robacker 1956; Moore and Shannon 1956 (length-width inequality) | `c` = maximum number of edge-disjoint paths; `d` = maximum number of disjoint cuts; `c d <= \|E\|` | classical links between the two parameters of `max{c,d} <= cp <= c + d - 1` | packing with small overlap, not the union of one path and one cut | background; Menger cited, the other two only reported |
| Blocking clutters: Edmonds and Fulkerson 1970 (record only) | paths and minimal cuts block each other | a cut-path is a member of a clutter plus a member of its blocker | the minimum union is not studied in any wording searched | supports the novelty claim |
| Shortest-path separators: Abraham and Gavoille 2006 | minor-free graphs are split into balanced parts by removing the vertices of `k` shortest paths | a name a referee may connect with Separating Shortest Path | vertex removal, balanced separation, structural result | not cited; one clause possible |
| Largest bond, connected cut: Duarte et al. 2021 | maximization, connectivity required of the sides | cut with a connectivity condition | no path in the cut | no overlap |
| Force Path Cut: Miller et al. 2023 | APX-hard | edges removed around a prescribed path | path is input, removed edges need not separate | no overlap |
| Two disjoint paths, one of them shortest (2D1SP): Eilam-Tzoreff, DAM 1998 | NP-complete for two terminal pairs, vertex- and edge-disjoint, undirected and directed, unit lengths (Claims 1, 3) | mirror of Separating Shortest Path | the removal of a shortest path must leave a second pair connected; here it must separate the ends of the path | no overlap; now cited |
| Min-Min disjoint paths ("shortest path with a disjoint counterpart"): Xu et al. 2006; Guo and Shen 2012, 2013 (abstracts only) | one terminal pair; NP-hard, no constant-factor approximation for general lengths; planar cases | optimization form of the one-pair mirror | asks for a short path that has an edge-disjoint counterpart; Separating Shortest Path asks for a shortest path that has none | no overlap; not cited (full texts not read) |
| Critical Disruption Path: Granata et al. 2013-2023 | integer programming and heuristics | a path removed to damage the network | vertices removed, objective is the largest remaining component | no overlap |
| "Cut paths": Cairo et al., STACS 2023, ACM Trans. Algorithms 2026 | linear-time verification, enumeration | name only | a walk contained in every `u`-`v` walk of a strongly connected digraph | no overlap; possible confusion of names |

### 4.1 Path-removal side (working file `B1-path-removal.md`)

For a shortest `u`-`v` path `P` let `r(P)` be the number of edge-disjoint `u`-`v` paths left after the edges of `P`
are removed. Separating Shortest Path asks whether some shortest `P` has `r(P) = 0`. The literature has the mirror
question, whether some shortest `P` has `r(P) >= 1`:

- **Eilam-Tzoreff, The disjoint shortest paths problem, Discrete Applied Mathematics 85(2) (1998) 113-138**, for two
  terminal pairs (Section 2, Claim 1; pp. 113-120 read by the search subagent). Published in the target journal,
  NP-completeness by a reduction from 3SAT on undirected graphs with unit lengths. Now cited in the Introduction
  with the exact difference.
- **Min-Min disjoint paths** for one pair (Xu, Chen, Xiong, Qiao, He, IEEE/ACM Trans. Netw. 14(1) (2006) 147-158;
  Guo and Shen, Algorithmica 66(3) (2013) 641-653, and Theor. Comput. Sci. 432 (2012) 58-63). Only the abstracts
  were readable, so nothing is cited. `TODO(verify)` in the full texts: hardness for undirected graphs with unit
  lengths, and whether the hard instances ask for a path of length exactly `d(s,t)`.
- The two questions are neither equal nor complementary: a graph can have a shortest path with an edge-disjoint
  counterpart and another one without (six-vertex example in the working file; `TODO(verify)` by the author).
  No reduction between them was found. A by-product of Theorem 3.10 in the language of that literature: deciding
  whether every shortest `u`-`v` path has an edge-disjoint `u`-`v` counterpart is coNP-complete.
- **Non-disconnecting paths:** Hon, Tsai, Yang, Supereulerian Testing on Semi-Eulerian Graphs (CIAC 2025, LNCS,
  316-330, DOI 10.1007/978-3-031-92935-9_20; abstract only) gives a peer-reviewed NP-completeness proof that, by the
  subagent's reading of the abstract, covers the existence of a non-disconnecting path. The manuscript rests this
  fact on Mao's preprint. Not cited: the equivalence has to be read in the paper first.
- **Parameterized mirror:** Cai and Ye (Theor. Comput. Sci. 795 (2019) 275-284; arXiv 1509.05559v1 read): a path of
  length at most `k` with an edge-disjoint counterpart for a second pair is found in FPT time in `k`. Different
  technique; optional citation in Section 8.
- **Forward citations** (2022-2026) of Mao, Abhinav et al., Bazgan et al., Eilam-Tzoreff, Xu et al., Guo and Shen:
  no citing paper asks for a path whose removal separates its ends.
- **Status on 2026-10-10:** Network Diversion on general undirected graphs (edge version) is still stated open
  (Bentert, Fomin, Hauser, Saurabh, Theor. Comput. Sci. 1065 (2026) 115726, read as arXiv 2408.13543v1; Kenig, arXiv
  2511.15849v5 of 2026-10-07). Mao's preprint has no published version; Abhinav et al. has no journal version.

## 5. Originality assessment

**A. The problem.**
The problem was proposed by Martin Loebl (acknowledgments) and first treated in the author's master's thesis (Charles
University, 2025), where NP-hardness was left open. No work by other authors was found, under any name. The
characterization `cp(u,v) = min_P (|P| + c_{G - P}(u,v))` is a two-line observation and was not found in the
literature either. Defensible claim: the problem has not been studied by other authors; the complexity results are
new. Not defensible: "has not been studied before" without the thesis.

**B. Proofs of hardness.**
- The reduction from 3-SAT to Separating Shortest Path (chain of cycles, synchronization and clause threads,
  calibration) follows the usual plan of a 3-SAT reduction (choice gadgets, consistency, clause checking); the
  gadgets and the separation argument (transition graph, Lemma 3.9) are specific to this problem. Nothing similar
  was found for a neighbouring problem. This is the central contribution.
- No PTAS: a gap-preserving reading of the same construction with the bounded-occurrence gap problem of Feige.
  Standard method; the content is Lemma 4.1 (paths that are not chain paths do not help). The constant
  `epsilon_0 = delta/200` is not explicit, because `delta` is not.
- The step from Separating Shortest Path to Min Cut-Path (threshold `b = d(u,v)`) is immediate.

**C. Structural and algorithmic results.**
- Diameter two: `cp = c + d - 1` is new. The known theorem gives `c(u,v) = min{deg u, deg v}`; the new content is
  that no minimum cut contains a `u`-`v` path when `d(u,v) = 2 <= c(u,v)`. Lemma 5.3 is the standard argument of
  the known proof.
- Cactus graphs: the formula is new and elementary; the characterization (Lemma 6.1) is folklore.
- Example 6.3 shows that the hypotheses cannot be weakened to the pair `u`, `v`; it also shows that a minimum
  cut-path may contain no minimum cut (left graph) or no shortest path (right graph); checked by brute force
  (`literature-review-2026-10-10/check_example.py`).
- Random graphs: for constant `p` the result is "diameter two with high probability" plus Theorem 5.5; for
  `p >= alpha log n / n` it is `|C u P| / cp <= 1 + d/c` with the diameter bound of Chung and Lu and "edge
  connectivity = minimum degree" from Bollobás. A meaningful statement about the problem (hardness is a worst-case
  phenomenon), a short proof from known bounds. Definition 2.5 ("average approximation scheme") is not a standard
  notion; the theorem is already stated as a bound with high probability, which is the form a referee expects.
- FPT: new statement. The technique is an application of treewidth reduction and Courcelle's theorem; the own step
  is the weighted shortcut graph that lets the path leave the torso. No explicit `f(b)`; no running time a
  practitioner could use.

**D. Overall.**
Strongest contributions, in this order: (1) NP-completeness of Separating Shortest Path, that is, of deciding
`cp = d`, on graphs of maximum degree three apart from `u`, `v`; (2) no PTAS; (3) the exact formula and the
linear-time algorithm in diameter two; (4) fixed-parameter tractability in the solution size. Supporting: basic
bounds and the factor two, cactus graphs, random graphs.
The paper is coherent around one question, which the Introduction now states: when is the union of a minimum cut
and a shortest path optimal, and how hard is the problem otherwise.

## 6. Section 8 (penultimate section): check of correctness

Every step was derived again from the text; the cited statements were compared with arXiv:1110.4765v1.

| Item | Verdict |
|---|---|
| `d_C(u,v)` as a distance after contracting `C` | correct (it may be zero) |
| Lemma 8.1 (`cp = min (\|C\| + d_C)` over inclusion-minimal cuts) | correct |
| Remark on `\|E\|^{O(b)}` and the example with `(\|E\|/b)^b` minimal cuts | correct |
| Lemma 8.2 against Marx et al. (Lemma 2.11 with `l <= k`, `e = k - l`; bramble number = treewidth + 1; Remark 2.13; Proposition 2.7) | correct; hypotheses (non-adjacent, same component, a separator of size at most `k`) are the ones the source needs |
| Construction: `G'`, `R_F`, minimal cuts of `G` give minimal separators of `G'`; `D`, `G_D`, `omega`, `G_D^+`; equivalence (8.1) | correct |
| Lemma 8.3, both directions, including the counts `\|M\| <= \|C\| + \|P \ C\|` and `\|F_1 u F_2\| <= \|M\|` | correct |
| Theorem 8.4: running time, treewidth after subdivision, the three monadic second-order conditions | correct |
| `checks/check_fpt_lemmas.py`, run again 2026-10-10 | 142 graphs, 1933 pairs, 35945 constructions, no failure |

Findings, none of them an error in a statement:

1. **Computability of `f`.** The section defines FPT with a computable `f`; the proof of Theorem 8.4 ends with "for
   a function `f` of `b`". Theorem 2.2 of Marx et al. does not say that `f_phi` is computable. A source that does:
   Cygan et al., *Parameterized Algorithms* (Springer 2015, DOI 10.1007/978-3-319-21275-3), Theorem 7.11: time
   `f(||phi||, t) n` for a computable `f`, for a graph with an evaluation of the free variables and a given tree
   decomposition of width `t`; Theorem 7.18 computes a decomposition of width at most `4t + 4` in time
   `O(8^t t^2 n^2)` (read in the authors' free PDF; printed pagination not compared). Proposed sentence at the end
   of the proof: "The function $f$ is computable: the bounds of Lemma~\ref{lem:treewidth-reduction} are given
   explicitly in~\cite{Marx2013Separators}, the formula $\varphi_b$ is constructed from $b$, and the bound of
   Courcelle's theorem is a computable function of the formula and of the treewidth~\cite[Theorem~7.11]{...}."
   Before it is added: check in Marx et al. that the functions of their Lemma 2.11 are explicit
   (Remark 2.14 gives `g = 2^{O(el)}`; the running-time function was not checked), and add the book to the
   bibliography. `TODO(verify)`.
2. **Model of the proof.** The proof has the three steps of the algorithm of Marx et al. for connected separators
   (their Section 3.3: a minimal separator is extended; the extension leaves the torso; Courcelle's theorem). The
   Introduction now says so. Proposed sentence for Section 8, before "We avoid the enumeration": "Marx, O'Sullivan
   and Razgon~\cite{Marx2013Separators} extend a minimal separator to a connected one in the same way; there the
   part is enlarged, here the path is recorded by the shortcuts."
3. **Numbers of the cited statements** are those of arXiv v1 and of the author's manuscript in journal format; the
   copy-edited ACM text could not be opened. Compare once from a library account.
4. **Definition of FPT** is cited to Marx et al. ("see, e.g."); it is on the first page there, with a computable
   `f`. A textbook (Cygan et al., Definition 1.2) is the usual reference; optional.

## 7. Bibliography: changes and proposals

Applied (canonical `knowledge/bibliography/references.bib` first, with status lines; then the project file):

| Entry | Why | Verified in |
|---|---|---|
| `Stuart2009Eavesdropping`: J. L. Stuart, The eavesdropping number of a graph, Czechoslovak Math. J. 59(3) (2009) 623-636, DOI 10.1007/s10587-009-0056-9 | attribution of `c(u,v) = min{deg u, deg v}` in diameter two (its Theorem 11, credited there to Fricke, Oellermann and Swart) | Crossref, DML-CZ record, journal text |
| `Baier2010LengthBounded`: Baier, Erlebach, Hall, Köhler, Kolman, Pangrác, Schilling, Skutella, Length-bounded cuts and flows, ACM Trans. Algorithms 7(1) (2010) 1-27, DOI 10.1145/1868237.1868241 | source of the term "length-bounded edge cut", used before without a reference, and the inapproximability result next to "no PTAS" | Crossref (with abstract), OpenAlex, authors' manuscript of the journal version (Theorem 3.11) |

| `EilamTzoreff1998Disjoint`: T. Eilam-Tzoreff, The disjoint shortest paths problem, Discrete Appl. Math. 85(2) (1998) 113-138, DOI 10.1016/S0166-218X(97)00121-2 | the published problem closest to Separating Shortest Path from the other side (a shortest path whose removal keeps a pair connected) | Crossref, OpenAlex; text pp. 113-120 read by the search subagent (Internet Archive copy); the main session could not re-open it (ScienceDirect captcha): open the article once and confirm Claim 1 |

Corrected or removed: none. Reading notes: `knowledge/literature/Stuart2009Eavesdropping.md`,
`knowledge/literature/Baier2010LengthBounded.md`, `knowledge/literature/EilamTzoreff1998Disjoint.md`.

Proposed, not applied (each is the author's decision):

1. **Section 5, after Corollary 5.7:** "The first equality is known: it is due to Fricke, Oellermann and Swart
   (see~\cite[Theorem~11]{Stuart2009Eavesdropping}); we include a proof because it uses
   Lemma~\ref{lem:empty-i-or-l}." Without it, the body presents a known theorem as a corollary of the paper.
2. **Section 6, before Lemma 6.1:** call the lemma well known ("This characterization is folklore; we include a
   proof."). Optional pointer: Marx and Végh, ACM Trans. Algorithms 11(4) (2015), DOI 10.1145/2700210,
   Proposition 3.7 of arXiv:1304.6593v2 (journal numbering not compared).
3. **The author's master's thesis** (`Michel2025MinCutPath`, verified entry in the canonical file) and the CSGT
   2026 abstract: cite and say what is new. Ready sentence: "The problem was introduced in the author's master's
   thesis~\cite{Michel2025MinCutPath}, which contains the results of Sections~\ref{sec:diameter-two},
   \ref{sec:cut-two} and~\ref{sec:random-graphs} and leaves the complexity open; the results of
   Sections~\ref{sec:np-completeness}, \ref{sec:approximation} and~\ref{sec:fpt} are new." (Check the list of
   sections against the thesis.)
4. **Cygan et al. 2015** for the computable bound in Section 8 (section 6, item 1).
5. **`Frieze2016`:** delete the `url` field (numbering of the linked PDF differs from the cited printed book).
6. **Background not added** (verified only in Schrijver's lecture notes of 2017, Theorem 1.2 and Corollary 4.1b):
   Robacker's theorem and the length-width inequality `c(u,v) d(u,v) <= |E|`. One sentence is possible after
   Lemma 2.3 once a citable source is read.
7. **Shortest-path separators** (Abraham and Gavoille, PODC 2006, DOI 10.1145/1146381.1146411): one clause where
   Separating Shortest Path is defined, if a referee confuses the notions.
8. **Min-Min disjoint paths** (Xu et al. 2006; Guo and Shen 2013) next to Eilam-Tzoreff, once a full text is read;
   **Hon, Tsai, Yang 2025** next to Mao, once the equivalence is read in the paper; a clause that separates
   cut-paths from the **"cut paths" of Cairo et al.** (ACM Trans. Algorithms 22(2) (2026) 1-30, DOI
   10.1145/3790095), where the term is defined.
9. **Keywords:** the two results added on 2026-10-10 are not among them; candidates: "inapproximability",
   "fixed-parameter tractability" (seven keywords are allowed).
10. **Title:** "Min Cut-Path Problem" names no result; a shape: "Min Cut-Path: Hardness, Exact Cases and
   Parameterized Complexity".

## 8. Change log

Abstract (181 -> 213 words, formulas not counted; the journal allows 250):
- states the baseline (the union of a minimum cut and a shortest path, at most `c + d - 1` edges, fewer than
  twice the minimum), which ties the results together;
- the approximation hardness with its constant `epsilon_0`, and the scheme as a consequence;
- "in contrast" for the two classes; `1 + o(1)` for random graphs (as in the Conclusion);
- "the decision version" is fixed-parameter tractable (before: the problem).

Introduction (rewritten, about 550 words longer; statements about cited works are those of the reading notes):
- opens with the definition; the network interpretation is one sentence;
- new second paragraph: why the problem is not the sum of its two polynomial parts (bounds, factor two,
  `|P| + |C| - |P n C|`, the form `min_P`, Example 6.3), and the question of the paper;
- related work by idea: classical path-cut relation (Menger, now with the corollary number; before: "max-flow
  min-cut theorem" cited for paths and cuts), paths whose removal keeps connectivity (with the result of
  Eilam-Tzoreff on two disjoint paths, one of them shortest), cuts that destroy short paths (with Baier et al.),
  cuts with prescribed structure (with the treewidth reduction), then the difference and the novelty sentence;
- "have been studied in detail" and "This literature treats a path and a cut as separate objects" are gone;
- "To the best of our knowledge, \MinCutPath{} has not been studied before" became "neither \MinCutPath{} nor
  \SSP{} has been studied by other authors, under these or other names";
- contributions as a numbered list of four (hardness and approximation hardness; two classes; random graphs;
  parameterized complexity), each with theorem numbers; new in it: the degree bound of the reduction (stated in
  Section 3.1), the interval `1 + epsilon_0` to two, the attribution of `c(u,v) = min{deg u, deg v}`, "folklore"
  for Lemma 6.1, the sources of the random-graph bounds, "no explicit bound on `f`";
- techniques: the paragraph on the reduction is kept; one paragraph each on the approximation hardness and on the
  FPT algorithm (with the relation to connected separators);
- organization: three sentences.

New statement to check (it is in the Introduction only): "A minimum cut-path may contain no minimum cut, or no
shortest path; the two graphs of Example 6.3 show both." Reason: in the left graph `cp = d = 3`, so a minimum
cut-path is a shortest path, and by Lemma 5.4 a minimum cut (two edges) shares exactly one edge with it; in the
right graph `cp = c = 3`, so a minimum cut-path is a minimum cut, and a path inside it has an odd number of edges,
hence three, while `d = 2`.

Bibliography: three entries added (section 7); 23 entries, all cited.

Build: 24 pages (before: 23), no undefined reference or citation, BibTeX without warnings; `check-text.ps1`
11 findings (the eight known false positives and three more of the same kind, "Name~\cite{...} proved");
`check-bib.ps1` 2 recommendations (no issue number in two Crossref records); packager with `-CheckOnly`:
`Verdict: PASS`.

## 9. Critical reviewer assessment

**Strongest contributions.** NP-completeness of deciding `cp(u,v) = d(u,v)` on graphs of maximum degree three
apart from `u` and `v`; the constant-factor inapproximability; the exact value in diameter two with a linear-time
algorithm; fixed-parameter tractability in the solution size.

**Most vulnerable novelty claims.**
1. Corollary 5.7 and Lemma 5.3 in the body: known (maximally local-edge-connected graphs). Attributed in the
   Introduction only.
2. Lemma 6.1: folklore.
3. Theorem 7.6: a short consequence of cited bounds; Definition 2.5 is non-standard.
4. Theorem 8.4: an application of a known technique, without an explicit bound; the computability of `f` is
   asserted by the definition and not argued.

**Literature-related risks.**
1. The master's thesis and the conference abstract are findable and not cited; the article shares results (and,
   by the notes of the workspace, paragraphs) with the thesis. A referee who finds them reads the novelty sentence
   as concealment. This is the first thing to settle.
2. `Mao2021NonSeparating` is a preprint of 2021 without a published version; its hardness proof is a sketch. The
   published paper of Abhinav et al. relies on it, so the citation is acceptable.
3. Numbers cited from Marx et al. were not compared with the copy-edited journal text.
4. The statement that Network Diversion is open on undirected graphs is the state of 2025; repeat the search at
   submission.
5. DBLP, Google Scholar and MathSciNet were not searched.
6. The sentence on Eilam-Tzoreff rests on a subagent's reading of pp. 113-120; the one-pair form of that problem
   (Min-Min disjoint paths) is known to the survivable-routing literature and is not cited, because only abstracts
   were readable. A referee from that side will name it.
7. "Cut paths" is the title term of a 2026 paper in ACM Transactions on Algorithms (Cairo et al.) for a different
   object.

**Does the Introduction make the case?** It now states one question, places the problem between two polynomial
problems and a trivial factor two, names the closest problems with the exact difference, and lists four results
with theorem numbers and their limits. The application remains a one-sentence interpretation; the paper is
theoretical and should not promise more.

**Before submission.**
1. Decide on the thesis citation (section 7, item 3).
2. Add the attribution sentence to Section 5 and "folklore" to Section 6 (items 1, 2).
3. Argue the computability of `f` or weaken the claim (section 6, item 1).
4. The author must read Sections 4 and 8, which were written with an AI assistant, and the AI declaration must
   name them (open items of the project notes).
5. Consider a title that names the results, the two keywords, and whether Definition 2.5 is needed.
6. Open questions a referee may ask about and the Conclusion already lists: complexity of `cp = c`, bounded `c` or
   `d`, diameter three, planar graphs. Not addressed anywhere: weighted and directed versions, the vertex version.

## 10. Limitations

- No search can prove absence. About 80 earlier queries and the queries of the three working files found no
  earlier treatment by other authors; DBLP, Google Scholar and MathSciNet are missing.
- Read only as a record: Hellwig and Volkmann 2004 and 2008, Plesník 1975, Moore and Shannon 1956, Edmonds and
  Fulkerson 1970, the manuscript of Fricke, Oellermann and Swart (unpublished, no copy found).
- Read in a preprint or an author's copy, journal text not compared: Marx et al., Baier et al., Bazgan et al.,
  Marx and Végh.
- One request of a search subagent to Crossref carried the author's e-mail address as a `mailto` parameter
  (`B2-path-and-cut.md`, Limitations). It was not repeated.
