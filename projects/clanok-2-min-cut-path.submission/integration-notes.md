# Article 2 - integration notes (2026-10-12)

Written by the integration step. `projects/clanok-2-min-cut-path/main.tex` = the template's sample with the
preamble additions, the new front matter, Section 1, Sections 2 to 7 from `drafts/core.tex`, Section 8 and the back
matter. Project notes with status, checks and open items: `projects/clanok-2-min-cut-path.md`.
Statement numbers are those of the compiled PDF. Sections 1 to 7 describe the first pass (23 pages); Section 8
describes the referee pass of the same day (24 pages), which changed statements and proofs on the coordinator's
decision. Line numbers in Section 8 are those of `main.tex` after the referee pass.

## 1. Changes in the body relative to `drafts/core.tex` (first pass)

No statement and no proof was changed in the first pass (the referee pass did: Section 8). The draft's first
comment line was dropped.

| Place (label) | Draft | Manuscript | Reason |
|---|---|---|---|
| Section 2.1, second sentence | - | "Notions that are not defined here follow [Diestel]." | textbook for standard notions (`paper-structure.md` §7) |
| Section 2.1, problem sentence | `\cite{Michel2026MinCutPath}` | `\cite{Michel2025MinCutPath}` | the problem is introduced in the thesis |
| `lem:basic-bounds` | head `[Lemma 2.3 and Corollary 3.12 of article 1]` | head `[Basic bounds]`; sentence before the lemma: the two bounds are those of Claim 7 of the thesis, "we include the short proof" | attribution, not a dependency; the equivalence with a separating shortest path is proved in the text and is attributed to nobody |
| after `lem:uncrossing` | `% CITE: submodularity` | comment removed, sentence kept without a citation | no verified source in `related-work.md`; see §3 |
| `def:class` | head `[The class DC_2]` | head `[The class DC_2, [thesis, Definition 37]]` | the class is the thesis's |
| Section 2.2, cactus sentence | `\cite[Lemma 6.1]{article 1}` | sentence without citation, then "This characterization is folklore (one direction is proved in [thesis, Claim 17], both in [article 1, Lemma 6.1])." | folklore (`related-work.md` 3.4); the thesis has one direction only |
| after the proof of `prop:class` | - | "The equivalence classes of Proposition 4 are called 3-edge-connected components in [Mehlhorn et al.], where they are computed in linear time." | `related-work.md` 0.5, 3.5 |
| before `fig:graph-classes` | formula cited from article 1, Theorems 5.5 and 6.2; "The formula fails in DC_2." | thesis, Theorems 15 and 18; "The formula fails in DC_2, as the two graphs of [thesis, Figure 3.3] show (Example 1)." | thesis has both; attribution of the counterexamples |
| Section 3, first paragraph | one sentence, then the standing assumption | four sentences added after the first: the structure is known (Picard and Queyranne; strip of Dinitz and Vainshtein, see Baswana and Pandey; pointer to Section 1.1); Lemmas 6 to 8 and Theorem 9(i)-(iv) describe it for cut-value two in the explicit form used later; proofs kept for self-containedness; Theorem 9(v) "corresponds to" the contraction of the classes of `c >= 3` in the cactus of the 2-edge cuts (Mehlhorn et al.) | `related-work.md` 0.1-0.3, verdict (ii); the verb "corresponds to" because the derivation of 2.2 there is in no source and not proved in the text |
| Section 3, Menger | `% CITE` | `\cite[Corollary~3.3.5]{Diestel2025}` | A1 |
| `fig:square-decomposition` caption | "... and the edges of F, directed from tail to head" | "... and the directed edges of F" | the caption ran into a second line |
| before `lem:residual` | `% CITE` | two sentences: for a directed network both statements are due to Picard and Queyranne; "We prove them for the graph D, in which every edge outside p_1 u p_2 has both arcs." | A3 and item 0.4 |
| proof of `thm:linear-time`, first step | `% CITE` | "... augmentations of the algorithm of Ford and Fulkerson [Erickson, Section 10.4]" | A2 |
| proof of `thm:linear-time`, running time | `% CITE` | breadth-first search [Erickson, Section 8.4], strong components [Tarjan] | A4 |
| proof of `cor:class-pairs` | `% CITE` | new last sentence: "A minimum u-v cut is computed in polynomial time by a maximum flow [Erickson, Sections 10.3 and 10.4]." | A2 |
| `rem:coarser` | key `Michel2025Thesis` (twice) | key `Michel2025MinCutPath` | the entry's real key |
| Section 7, last paragraph | "In a graph of diameter two, no minimum u-v cut contains a u-v path if d(u,v) = 2 [article 1, Theorem 5.5]." | "In a graph of diameter two, a pair with d(u,v) = 2 has cp(u,v) = c(u,v) + 1 [thesis, Theorem 15], so no minimum u-v cut contains a u-v path." | thesis has the theorem; the wording now says what the source states (the consequence is Proposition 18) |

Unchanged citations of article 1: Theorem 3.10 in the proof of `thm:hardness` (no substitute).
Figures are included at natural size as in the draft. `transformations.pdf` is not used.

## 2. Preamble

- Plain route tested first (cleveref after the sample's package block, `\newtheorem{lemma}[theorem]{Lemma}`): the
  build passes, but `\cref` prints "Theorem 6(iii)" for Lemma 6 and "Theorem 5(ii)" for Proposition 5. Cause: the
  class loads hyperref before amsthm, so cleveref cannot tell the environments on a shared counter apart.
- Chosen: `thmtools` + `cleveref`; `theorem` stays the sample's `\newtheorem` line, the sample's `proposition`
  line is commented out, and `proposition`, `lemma`, `corollary` are `\declaretheorem[..., style=thmstyleone,
  sibling=theorem]`. Checked in the PDF: "Lemma 6(iii)", "Proposition 5", "Corollary 13", "Lemmas 6 to 8".
  `thmtools` was already installed; nothing was installed.
- `\RequirePackage{float}` before `\documentclass`: no "destination with the same identifier" message in the log.

## 3. CITE needs of `core-notes.md` §6

| Need | Result |
|---|---|
| submodularity of the cut function | **open**: no verified source. The sentence only names the inequality of Lemma 3, which is proved. Candidate to verify and add: a textbook statement (for example Schrijver, *Combinatorial Optimization*, or Frank, *Connections in Combinatorial Optimization*); neither is in the canonical file |
| Menger, edge version | `Diestel2025`, Corollary 3.3.5 |
| residual graph, minimum cuts as closed sets | `PicardQueyranne1980`, no number (the published chapter was not compared with the report) |
| augmenting paths | `Erickson2019Algorithms`, Section 10.4. The step "a flow of value two decomposes into two edge-disjoint paths in linear time" has no locator of its own (doubt 3 of `core-notes.md`) |
| breadth-first search; strong components | `Erickson2019Algorithms`, Section 8.4; `Tarjan1972DFS` |
| minimum u-v cut in polynomial time | `Erickson2019Algorithms`, Sections 10.3 and 10.4 |

## 4. Bibliography (for the owner of the `.bib` files; nothing was edited)

- **Uncited entries of `projects/clanok-2-min-cut-path/references.bib`** (15 of 17 cited): `Cormen2022` (its
  locations are unverified, and the text needs no second textbook), `Schmidt2013TwoConnectivity` (the article does
  not compute bridges; Remark 1 only uses their definition). Delete both from the project file, or cite them.
- `Abhinav2022NonSeparating`: `sn-mathphys-num.bst` prints the pages `6:1--6:15` as "pp. 6-1615". Fix in the
  entry (for example an article number in `note` and no `pages`), to be tested with this style.
- `Mao2021NonSeparating`: prints "arXiv preprint (2021)" without the number `2101.03519`; the style ignores
  `eprint` of a `@misc` entry. Put the number into `note` or use `howpublished`.
- `Michel2026MinCutPath`: prints "Manuscript (2026)". Algorithmica's list holds only published or accepted works
  (`related-work.md` 4.4): article 1 has to be on arXiv or accepted before submission, and the entry rewritten.
- `Michel2025MinCutPath`: prints "Master's thesis, Charles University, Faculty of Mathematics and Physics, Prague
  (2025)", without the handle of the public record (proposal 11 of `related-work.md` 4.2).
- `LeLe2019MatchingCut`: `check-bib.ps1` finding `recommended` (no issue number in the Crossref record).
- The list is in citation order (default of the style); see "Reference order" in the project notes.

## 5. Locators to re-check before submission

- Article 1: Theorem 3.10 (twice), Lemma 6.1; the question about bounded `c(u,v)` (its conclusion, question 2).
  Numbers agree with `outputs/clanok-1-min-cut-path/main.aux` of 2026-10-12; they can move until article 1 is public.
- Thesis: Section 3.3, Claims 7 and 17, Definitions 37 to 40, Figure 3.3, Theorems 15, 18, 20, 22, 23; all found
  at these numbers in the extracted text (`knowledge/sources/diplomova-praca-2025-min-cut-path.txt`) on 2026-10-12.
- Erickson: Sections 8.4, 10.3, 10.4. Diestel: Corollary 3.3.5.

## 6. Mathematical points noticed while integrating

No error found; the body was read statement by statement against its proofs.

1. **Section 3 attribution.** "The square decomposition is an explicit form of these representations"
   (Section 1.1) and "Statement (v) corresponds to ... the cactus" (Section 3) rest on the literature notes and
   are not proved in the text. That the pieces are exactly the classes of the strip (two vertices of different
   pieces are separated by some minimum cut) follows from Theorem 9(i) and (iv): the entering edges of a square
   are a minimum cut, and so is one edge of each of the two general paths between consecutive squares. This
   argument is not written down in the manuscript. The correspondence with the cactus is the derivation of
   `related-work.md` 2.2, which nobody has proved or tested yet (its item 4.2.8); hence the verb "corresponds".
   If a referee asks, a short remark with these proofs is the answer.
2. **Theorem 17** depends on article 1 in two ways: the NP-completeness of Separating Shortest Path and the fact
   that the graphs of that reduction have at least three edge-disjoint u-v paths (doubt 2 of `core-notes.md`).
3. **Introduction, results item 3** says that Theorem 17 answers "for the cut-value" the question of article 1 on
   bounded `c(u,v)`. Nothing is said about bounded `d(u,v)`, about deciding `cp = c` in general graphs or about
   diameter three.
4. **Conclusion, question 2** uses that in the class with distance bound `k` the paths of Theorem 11 have at most
   `k` edges. This is the argument of Corollary 13 with `k` in place of two (Theorem 9(v) holds in every graph);
   it is stated as a remark to the question, not as a result. Trying all paths with at most `k` edges gives a
   polynomial algorithm for fixed `k`, which is why the question asks for linear time.
5. **Conclusion, question 3**: `d <= cp <= d + 2` for `c = 3`, `d >= 3` is Lemma 1.
6. **Resolved in the referee pass (Section 8, G1); kept as the record of the state before it. How `p_1`, `p_2`
   are obtained (proof of Theorem 15, first step; `main.tex` lines 933-935 of the first pass).** The checks report (`checks/README.md`, "Blueprint", item 2) that `p_1` and `p_2` must be read from
   the net flow, not taken as the two augmenting paths: the second augmenting path cancels flow on an edge of the
   first for 16 of the 13350 pairs with `c = 2` on graphs with at most 7 vertices. The manuscript does not say
   that the augmenting paths are `p_1` and `p_2`, but it does not say how they are obtained either, and the verb
   "yields" can be read that way. The exact sentences (mathematics not changed):

   > The algorithm first searches for three edge-disjoint $u$--$v$ paths by at most three augmentations of the
   > algorithm of Ford and Fulkerson~\cite[Section~10.4]{Erickson2019Algorithms}.
   > Each augmentation is a search in a residual graph and takes $O(|V| + |E|)$ time.
   > This step determines whether $c(u, v)$ is one, two or at least three, and if $c(u, v) = 2$ it yields two
   > edge-disjoint $u$--$v$ paths $p_1$ and $p_2$.

   Also line 2 of Algorithm 1 ("compute two edge-disjoint $u$--$v$ paths $p_1$ and $p_2$", `main.tex` line 900)
   and, in the Introduction, "The squares are computed from two edge-disjoint $u$--$v$ paths" (Section 1.3):
   neither names the augmenting paths. Proposal for the referee pass, not applied: after "at least three" say
   that the edges carrying flow after two augmentations form two edge-disjoint `u`-`v` paths and possibly
   cycles, and that the two paths are extracted from them in linear time (this is doubt 3 of `core-notes.md`;
   no verified locator for the flow decomposition yet). The definition of `D` and Lemma 14 start from two
   edge-disjoint paths and are not affected.
7. **Observation 8 of `core-notes.md` is false** (`checks/README.md`, "Failures": a 21-vertex graph of the class
   with a separating trace and four distinct terminals). The manuscript does not contain it.
8. The other doubts of `core-notes.md` §8 stand as they are (Remark 2 and the thesis's construction; Proposition 12
   not needed for the main line; letters `c_i`, `d_i`, `s`, `t` reused; digit vertex names of `G_1`;
   adjacency-list model).

## 7. Other things noticed, not changed

- `projects/clanok-2-min-cut-path/transformations.pdf` is in the folder and is not read by the build: the full
  package run reports `[unused]`. It belongs to the figures step; retire it to
  `archives/removed-from-projects/clanok-2-min-cut-path/` before the folder is sent (or use it).
- The packager looks for an AI declaration draft in `projects/<project>/submission/`; the draft lies in
  `projects/clanok-2-min-cut-path.submission/ai-declaration.tex`, so its reminder keeps saying "no draft".
- `checks/README.md` (finished after the first integration pass) is the record of the computational checks:
  all 12112 connected graphs with at most 8 vertices, 2953 random chains in the class, the algorithm against
  brute force, 18 mutation tests; no statement of the manuscript failed. It also shows that Algorithm 1 gives
  wrong answers outside the class when an entering and a leaving terminal of a square are at distance greater
  than two (111 of 4789 random instances), which agrees with the sentence after Theorem 15.
- `drafts/related-work.md` 3.6 proposes for the conclusion "We do not know whether Min Cut-Path is NP-hard on
  graphs of diameter three." It was left out on the coordinator's instruction; the Matching Cut and Most Vital
  Edges sentence stands in Section 1.1 without it.

## 8. Referee pass (2026-10-12)

Source: `review/referee-math.md` (no error, one gap G1, three unclear places U1-U3, twelve minor points M1-M12,
each with replacement LaTeX; its line numbers refer to `core.tex`). Its scripts (`review/scripts/`): statements of
Sections 3 to 5 on 11895 instances (7395 pairs on all graphs with 2 to 7 vertices, 3000 chains, 1500 random
graphs), 81 example values, 0 failures; the algorithm without the promise is its test `ALG3`.
Decisions are the coordinator's; the ban on changing statements and proofs was lifted for these findings only.

**Numbering did not change:** no numbered statement was added or removed (Definitions 1-4, Lemmas 1-3, 6-8, 10,
14, Propositions 4, 5, 12, 18, Theorems 9, 11, 15, 17, Corollaries 13, 16, Examples 1-5, Remarks 1-2, Figures 1-7).
Algorithm 1 has 29 lines instead of 22; all its lines are cited by label (`line:record`, `line:union` and
`line:certificate` are new). Pages: 24 (23 before).

| Finding | Place (`main.tex` line) | Before | After |
|---|---|---|---|
| G1, M12 | proof of Theorem 15, first step (950-966) | three sentences: three augmentations, "it yields two edge-disjoint `u`-`v` paths `p_1` and `p_2`" | text R1: a flow of value at most three with at most one unit per edge; the first augmentation succeeds because `G` is connected; `c(u,v)` from the failing augmentation; for `c = 2` the augmenting paths need not be edge-disjoint, so `p_1`, `p_2` are read from the flow: digraph `H` of the edges that carry flow, degree count, reachability argument, two searches, remaining arcs form cycles; "Line 2 of Algorithm 1 takes these two paths"; "the residual graph of the current flow". The citation of Erickson, Section 10.4, stays at the augmentation sentence. Running time: "The paths `p_1` and `p_2` are found by two searches in `H`." |
| U1 (R2) | Algorithm 1, `line:candidates` (921) | "the paths `x, w, y` of `S_i` in which `w` is a neighbor of `x` or of `y` on `q`" | "the paths `x, w, y` of `S_i` such that `xw` or `wy` is an edge of `q`" |
| U1 (R2) | proof of Theorem 15, case `l = 2` | "... so it contains the edge `xw` or the edge `wy`, and `w` is a neighbor of `x` or of `y` on `q`." | "... so it contains the edge `xw` or the edge `wy`." |
| U1 (R2), M8 | proof of Theorem 15, running time (992-1000) | "The path `q` contains at most two neighbors of `x` and at most two neighbors of `y`, so P has at most four members, which are found by marking the neighbors of `x` and of `y`." | "The graph is given by adjacency lists." (first sentence of the part); "The path `q` has at most two edges at `x` and at most two edges at `y`, so P has at most four members. Whether `x, w, y` is a path of `S_i` is decided for each of these vertices `w` after marking the neighbors of `x` and of `y`. A vertex of `S_i` is an end of at most four edges outside `S_i`, the edges that enter or leave `S_i`, so its neighbors are marked in `O(m_i + 1)` time." |
| U1 | Example 5 (1017) | "The only neighbor of `x` or of `y` on `q` is `a`, and ..." | "Its only edge is `ua`, so `w = a`, and ..." |
| U1 | Section 1.3 | "so `w` is a neighbor of `x` or of `y` on `q`" | "so `xw` or `wy` is an edge of `q`" |
| U2 (R3) | Algorithm 1 (900-934) | caption "... for a pair with `c(u,v) = 2` in a graph of DC_2"; input "a graph `G` in DC_2 ..."; output "`cp(u,v)` and a minimum cut-path"; last line returns `d(u,v) + 1` and `R ∪ C` | caption "A minimum cut-path if `c(u,v) = 2`, or two vertices that show `G` not in DC_2"; input "a connected graph `G = (V,E)` and two vertices `u, v` with `c(u,v) = 2`"; output "`cp(u,v)` and a minimum cut-path between `u` and `v`, or two vertices `x, y` with `c(x,y) >= 3` and `d(x,y) >= 3` and a cut-path between `u` and `v` with `d(u,v) + 1` edges"; after `line:length`: "if `l >= 3` then record the pair `x, y`" (`line:record`); at the end: `R`, `C` defined (`line:union`), "if a pair `x, y` is recorded then return `x, y` and `R ∪ C`" (`line:certificate`), "return `d(u,v) + 1` and `R ∪ C`" (`line:not-found`) |
| U2 (R3) | **statement of Theorem 15** (943-948) | "There is an algorithm that, given a graph `G = (V,E)` in DC_2 and two distinct vertices `u, v` of `G`, decides in `O(\|V\| + \|E\|)` time whether `c(u,v) <= 2` and, if so, computes `cp(u,v)` and a minimum cut-path between `u` and `v`." | "There is an algorithm that, given a connected graph `G = (V,E)` and two distinct vertices `u, v` of `G`, decides in `O(\|V\| + \|E\|)` time whether `c(u,v) <= 2`. If so, it returns within the same time `cp(u,v)` and a minimum cut-path between `u` and `v`, or it returns two vertices `x, y` with `c(x,y) >= 3` and `d(x,y) >= 3`, which show that `G` is not in DC_2, and a cut-path between `u` and `v` with `d(u,v) + 1 <= cp(u,v) + 1` edges. The second outcome does not occur for `G` in DC_2." |
| U2 (R3) | proof of Theorem 15, correctness (968-990) | "Suppose now that `cp = d` ... `\|p\| <= 2` by Corollary 13 ... Otherwise `cp = d + 1`, and the algorithm reaches the last line ..." | the three sentences of R3 worked in: a path returned in `line:found` is a minimum cut-path in every connected graph; `l >= 3` for terminals `x != y` gives `d(x,y) >= l >= 3` (triangle inequality) and `c(x,y) >= 3` (Theorem 9(v)), so a recorded pair shows `G` not in DC_2 and none is recorded in the class; if `cp = d` and no pair is recorded, the witness has `l = \|p\|` in `{1, 2}` and is found; reaching `line:not-found` therefore means `cp = d + 1`; `R ∪ C` is a minimum cut-path there and has at most `cp + 1` edges in `line:certificate`. Corollary 13 is no longer used in this proof (the last sentence of the statement follows from Definition 2) |
| U2 | before Theorem 15 | - | "... searches every square for a path `p` as in Theorem 11 with at most two edges"; "The algorithm does not test whether `G` in DC_2." |
| U2 | paragraph after Theorem 15 (1007) | "The proof uses the hypothesis `G` in DC_2 only in Corollary 13. Algorithm 1 is therefore correct for every connected graph and every pair ... such that every entering terminal ... is at distance at most two from every leaving terminal of the same square." | "Algorithm 1 returns `cp(u,v)` and a minimum cut-path whenever no pair is recorded, in particular if every entering terminal of every square is at distance at most two from every leaving terminal of the same square." |
| U2 | proof of Corollary 16 (1030) | "The first statement is Theorem 15, ..." | "The first statement is Theorem 15, whose second outcome does not occur for `G` in DC_2, ..." |
| U2 | Remark 2 | - | not changed: it does not refer to the promise; its distance hypothesis implies that no pair is recorded |
| U2 | abstract (145) | - | one sentence: "On any other graph, the same algorithm returns a minimum cut-path or two vertices whose distance and cut-value are both at least three." |
| U2 | Section 1.2, item 2 (228) | - | one sentence on graphs outside the class; "In a graph of DC_2," added to the sentence on pairs with `d >= 3` |
| U2 | Section 1.2, item 3 (234) | "Hence the hypothesis `G` in DC_2 of the previous item cannot be dropped unless P = NP." | "Hence, unless P = NP, no polynomial-time algorithm computes `cp(u,v)` for all such pairs, and the second outcome of the previous item cannot be avoided." |
| U2 | Section 1.3 (255) | - | one sentence: two terminals between which a trace would need at least three edges have distance and cut-value at least three, and the algorithm returns them if it finds no separating trace with at most two edges |
| U2 | Section 8, first paragraph (1122) | - | one sentence: outside DC_2 the algorithm either still returns a minimum cut-path or returns two terminals at distance at least three |
| U3 (R4) | opening of Section 3 | (first pass) | covered by the first pass, not changed: known structure, Picard and Queyranne and the strip, statements (i)-(iv) describe it for cut-value two, proofs included, statement (v) and the cactus |
| U3 (R4) | before Lemma 14 (869-870) | "For a directed network, the two statements of the following lemma are due to Picard and Queyranne. We prove them for the graph `D`, in which every edge outside `p_1 ∪ p_2` has both arcs." | "For a directed network, statement (i) of the following lemma is the theorem of Picard and Queyranne on the closed sets of the residual graph of a maximum flow, and statement (ii) is their criterion for saturated arcs. We give the short proofs for the flow of value two in the undirected graph `G`, where every edge outside `p_1 ∪ p_2` has both arcs in `D`." (Theorem 1 and Corollary 6 of the report as read in `related-work.md`, no numbers cited) |
| U3 (R4) | after Proposition 4 | (first pass) | covered by the first pass, not changed: the classes are the 3-edge-connected components of Mehlhorn, Neumann and Schmidt |
| M1 | Lemma 1 | (first pass) | already satisfied: the head is "[Basic bounds]", the sentence before the lemma attributes only the two bounds to Claim 7 of the thesis, and the equivalence with a separating shortest path is proved in the lemma and attributed to nobody |
| M2 | proof of Theorem 17 (1063) | "The graphs constructed in that reduction are connected and contain at least three pairwise edge-disjoint `u`-`v` paths, the threads." | "For a formula with `n` variables and `m >= 1` clauses, the graph constructed in that reduction is connected and contains `2n + 7m >= 9` pairwise edge-disjoint `u`-`v` paths, the threads." Count read in article 1 (`main.tex` lines 810 and 823: "the construction creates `2n+7m` threads", "`c(u,v) >= 2n + 7m`, because the threads are edge-disjoint `u`-`v` paths"); that the graph is connected is not a sentence of article 1 (confirmed by the referee's and the checks' computations) |
| M3 | Section 7, last paragraph (1113) | "..., a pair with `d(u,v) = 2` has `cp = c + 1` [thesis, Theorem 15], so no minimum `u`-`v` cut contains a `u`-`v` path." | "..., `cp(u,v) = c(u,v) + 1` for every pair with `d(u,v) = 2` [thesis, Theorem 15], so by Proposition 18 no minimum `u`-`v` cut contains a `u`-`v` path." (thesis kept instead of article 1) |
| M4 | opening of Section 6 (1051) | "... a square can be an arbitrary graph, and deciding whether it contains ..." | "... every connected graph `G` with `c_G(u,v) >= 3` occurs as a square with the terminals `u, u, v, v`, and deciding whether it contains ..."; the same correction in Section 1.3 (260) and in Section 8 |
| M5 | proof of Theorem 9(v) (633) | - | inserted: "Every edge with exactly one end in `B` belongs to this cut." |
| M6 | proof of Corollary 13 (861-862) | "..., and it contains all edges of the path in `S_i`." | new sentence: "It contains all edges of the path in `S_i`, because an edge of a path joins two consecutive vertices of the path." (two sentences, because one was 43 words long) |
| M7 | after Proposition 12 (843) | - | added: "Indeed, by Proposition 12 the equation holds if and only if some shortest `u`-`v` path contains `g` and `h` and has the trace `p` in `S_i`, and for such a path `alpha_i = alpha` and `beta_i = beta`, so Lemma 10 applies." |
| M8 | proof of Theorem 15, running time | see the row U1, M8 | |
| M9 | **statement of Lemma 10** (727) | "Let `R` be a `u`-`v` path." | "Let `c(u,v) = 2`, and let `R` be a `u`-`v` path." |
| M9 | **statement of Proposition 12** (812) | starts with "(i) ..." | starts with "Let `c(u,v) = 2`." (the finding names both statements; its fix names only the lemma) |
| M11 | proof of Lemma 2 (335) | "no edge of `G \ C` leaves `A'`" | "no edge of `G \ C` has exactly one end in `A'`" |
| M11 | proof of Theorem 9(v) (646) | "this path enters and leaves `W ∩ B`, so ..." | "this path contains at least two edges of `delta(W ∩ B)`, so ..." |
| M10 | - | - | **not applied** (coordinator): the terminals keep the names `c_i`, `d_i` of the thesis, which the figures use; recorded in the project notes as a point for the author |

Not added, on the coordinator's instruction: any claim about the complexity of recognizing the class, and any
citation for robust algorithms (the referee's remark on this is from memory).
Nothing in the report could not be applied. Points 2 and 8 of Section 6 above are answered by M2 and M8.
After the pass: build exit 0, 24 pages, no undefined reference, no overfull line, BibTeX clean; `check-text.ps1`
3 findings (the same three); `check-bib.ps1` 3 findings (the same three); packager `-CheckOnly` `Verdict: PASS`.
