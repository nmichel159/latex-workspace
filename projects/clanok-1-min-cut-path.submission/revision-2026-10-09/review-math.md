# Adversarial mathematical review of the preserving revision (2026-10-09)

Revised file: `projects/clanok-1-min-cut-path/main.tex` (line numbers below refer to it, 1204 lines).
Original: `archives/removed-from-projects/clanok-1-min-cut-path/main-before-preserving-revision-2026-10-09.tex`.
Build checked from `outputs/clanok-1-min-cut-path/main.aux` (built 17:05): no undefined references; 19 pages
(original 15).

Tags: [ERR] introduced by the revision, must fix; [GAP] gap; [PRE] pre-existing and not in `issues-{A,B,C,D}.md`;
[OK-NOTE] minor. Items already in the editors' issue files are not repeated.

## 1. Preservation audit

Result: **nothing mathematical is missing or weakened.** Every original statement environment, proof, proof step,
procedure, figure and citation is present; all original labels exist; Algorithm 1 is byte-identical
(`algorithmic` block diffed). Changes of claims: one (item E3 below, Theorem 6.6 coupling), not logged.

| Original item | Revised location | Status |
|---|---|---|
| Abstract (all sentences) | 108-114 | kept; c, d defined before the formula; "secured" added (109) |
| Intro: motivation, classical work, contributions, section map | 130-141, 164-185 | kept; "duality" -> "max-flow min-cut theorem" (139); new related-work paragraphs 143-162 and proof outline 175-180 |
| Notation paragraph (n, m, d, c, component assumption, path = edge set, G \ P, deg(x,S)) | 190-202 | kept; "u-v cut" now defined (196) |
| Def. cut-path / cut-paths / cp value (2.1-2.3), Fig. 1 | 204-239, 216-221 | kept (wording only) |
| "minimum cut-path" term | 243 | kept; new 241-242: E in CP(u,v), minimum exists (true, made explicit) |
| Problem box (optimization) | 245-258 | identical |
| Lemma 2.4 + proof | 262-279 | kept; equal-bounds step made explicit (277), correct |
| Def. 2.5 + lead-in | 281-303 | kept |
| Sec. 3 lead-in, 3-SAT box, Cook citation, n/m override, two-step plan | 305-329 | kept |
| SSP box; "not an optimization problem" remark | 334-348 | kept; remark expanded (see E1) |
| Gadget intro, two-part list, Fig. 2 | 352-365 | kept |
| Def. 3.1 chain link, Fig. 3; Def. 3.2 chain, Fig. 4 | 370-418 | identical statements |
| Three link types, count 3m+2n, Fig. 5 | 420-447 | kept (count sentence now before Fig. 5) |
| Def. 3.3 thread, Def. 3.4 threading, Fig. 6 | 452-484 | identical |
| Three thread types + Figs. 7-9 | 486-520 | kept; figures moved after the list; lemma pointers added |
| Aux. procedures BuildChain/Thread/Calibrate, notation O_i, s(l) | 527-550 | identical |
| "Reduction from 3-SAT" paragraph, Algorithm 1 | 524-525, 552-585 | kept, Algorithm identical |
| "In words ..." + calibration sentence | 587-593 | kept; 589, 593 made explicit (true) |
| Correctness: chain paths, "hits", hit criterion | 597-599 | identical |
| "Shortest paths" paragraph | Lemma 3.5 `lem:chain-paths` 609-624 | all four steps kept, two justifications added (620, 622), correct |
| "Synchronization" paragraph (both bullets), "consistent", tau | 601-607, Lemma 3.6 `lem:synchronization` 626-644 | all kept; converse made explicit (640-642), correct |
| "Clause threads" paragraph | Lemma 3.7 `lem:clause-threads` 646-657 | kept; 655 made explicit, correct |
| Two-way correspondence (a), (b) | proof of Thm 3.9, 746-760 | kept |
| (b) separation argument: G \ P, unused paths, dead ends, three cases, conclusion | Lemma 3.8 `lem:separating` 659-735 | all original sentences kept verbatim (668-674, 693-702, 716-720, 733-734); auxiliary multigraph Gamma added |
| Thm 3.9 statement | 737-740 | identical (now after the lemmas) |
| Running time, membership in NP | 762-772 | kept ("requires" -> "adds") |
| Sec. 3.2, decision box, Thm 3.10 + proof | 775-821 | kept; BFS sentence added (803); "BFS or DFS" -> "BFS" |
| "decision NP-complete hence optimization NP-hard" | 823 | moved after the proof |
| Sec. 4 lead-in, GodsilRoyle cite, Def. 4.1, decomposition lead-in | 828-838 | kept |
| Lemma 4.2 | 840-850 | identical |
| Sentence "I or L is empty: otherwise ... passes through J and K" | proof of Lemma 4.3, 863-869 | turned into a proof; every step kept (867) |
| Lemma 4.3, Lemma 4.4 + proof | 854-889 | identical statements and proof |
| Thm 4.5 + proof (two cases, estimate, three bullets, final chain), Fig. 10 | 893-975 | all steps kept; several made explicit (905-906, 921, 924-928, 933-938, 949, 954, 960-961, 967, 972); figure redrawn (see N5) |
| Remark 4.6 | 977-981 | identical |
| Sec. 5 cactus paragraph, Thm 5.1 + proof, closing sentence | 986-1034 | kept; cycles C_i -> Z_i; 990-991, 1018, 1022, 1024-1026 made explicit |
| Sec. 6 opening, Thm 6.1, dense paragraph, sparse paragraph, Thms 6.2, 6.3 | 1039-1078 | kept; w.h.p. defined; ChungLu2001 added to Thm 6.2 |
| Lemma 6.4 + proof | 1080-1103 | kept; 1099, 1101 made explicit, correct |
| Lemma 6.5 + proof (three displays) | 1105-1135 | kept; 1119 made explicit |
| Paragraph before Thm 6.6 | 1137-1138 | rewritten, same content |
| Thm 6.6 + proof | 1140-1170 | kept; coupling sentence narrowed (E3); ratio display gains a (c+d-1)/c step |
| Conclusion, four open directions | 1175-1192 | kept as questions; new diameter-three question (1182) |
| Acknowledgments | 1197 | titles "Prof. RNDr. ... CSc." removed (N6) |

New mathematical claims introduced (quoted; all true unless flagged):
241-242 "Hence $E \in \CP(u,v)$, and the minimum ... exists"; 589 "Every thread passes through at least two chain
links"; 593 "the subdivided 4-cycles are again chain links ..."; 671 "each end-vertex of a crossing edge has degree
three in $G$"; 677-735 the multigraph Gamma and its edge list; 924-927 "The cut $C$ is the set of all edges between
two sides"; 990 "the second cycle contains a path whose ends $x \neq y$ lie on the first cycle" (G1); 1022 "A bridge
of $G$ on the path $P$ would separate $u$ from $v$"; 347 (E1, imprecise); 1182 diameter three is "the smallest
diameter" for SP-MVE and Matching Cut (backed by the reading notes, correct); 143-162 related-work statements
(checked against the reading notes; E2).

## 2. Mathematical check

### Section 3 (lines 595-773): correct

- Lemma 3.5 (609-624): correct. Every non-chain u-v path contains a whole connecting path (internal vertices have
  degree 2 and are not u, v) whose other end is a crossing-edge vertex, so |Q| >= Lambda + 1.
- Lemma 3.6 (626-644): correct; both bullets checked for all four sign combinations.
- Lemma 3.7 (646-657): correct; the clause thread is threaded with sign s(l_j), consistency gives sign(tau(x_i)).
- Lemma 3.8 (659-735): correct. Checked: degree-one argument for crossing-edge ends on P (671-672); vertex
  disjointness of distinct unused paths (Def. 3.2 item 4: L_i and L_{i+1} are separated by H_{i+1}); the reduction
  of a u-v path of G \ P to a u-v walk in Gamma (681-687); the edge list for tau(x_i) = true for all four
  synchronization threads (708-711) and its sign reversal; the clause-thread edges (723); the shortest-walk argument
  (729-732): I_i° has only u, T_i° only v as neighbour, literal nodes are joined only along one clause, so the only
  possible walk is u L_{1,k}° L_{2,k}° L_{3,k}° v, which needs all three literals false. No circularity: Lemma 3.8
  uses Lemma 3.5 (proof) and Lemma 3.7 (proof), not Theorem 3.9.
- Theorem 3.9 (742-773): (a) uses Lemmas 3.5-3.7 and the sentence 601-602; (b) uses 3.5, 3.6, 3.7, 3.8. Counts
  2n+3m links, 2n+7m threads, Lambda = O(n+m), O((n+m)^2) correct.
- Theorem 3.10: correct.

### Section 4

- Lemma 4.3 new proof (863-869): correct (the x..a and b..y segments are disjoint and non-empty).
- Theorem 4.5 proof (903-975): correct for simple graphs (simplicity already in issues A4/C3). The new 924-928
  argument is right (a subset of C of size >= |C| is C). The exchange argument (933-937) is valid: with
  A_1 := component of u, if L = ∅ then the second exchange (u <-> v) gives u in A_2; if I = ∅ the first exchange
  does. The count |C| = sum over K of deg(k, A_1) >= deg(u,J) + 2 + (|K|-2) >= deg(u) + 1 checked; |K| >= 2 holds
  (u and the third vertex of P).

### Section 5

- Theorem 5.1: the added 1018, 1022, 1024-1026 are correct; the remaining gap (P returning to a cycle) is issue C8.

### Section 6

- Lemmas 6.4, 6.5, Theorem 6.6: correct; the added steps 1099, 1101, 1119, 1165 are right.

### Cross-references

Every `\ref` has a target and points to the right object (checked all; numbering in the build: Lemmas 3.5-3.8,
Theorems 3.9, 3.10, 4.5, 5.1, 6.1, 6.6). The introduction uses only `\ref` (168-173), so its numbers are right.
`Definition~\ref{def:chain}, item~4` (683) is the right item. The only textual pointer is "Case~3" (732), see N2.
SPEC.md still says "Theorem 3.5" for `thm:ssp-np-complete`; it is 3.9 (no effect on the text).

## 3. Findings

**E1 [ERR] line 347** "a solution is a single shortest $u$--$v$ path, that is, a cut-path of size $d(u,v)$".
A shortest u-v path is a cut-path only when it is separating; "that is" equates two different things. (Issue B14
flags only the forward reference.) Fix:
`Unlike \MinCutPath, \SSP{} is not an optimization problem: a solution is a separating shortest $u$--$v$ path, that is, a cut-path with $d(u,v)$ edges (see the proof of Theorem~\ref{thm:mcp-np-complete}).`

**E2 [ERR] line 155** "\textsc{Network Diversion} asks for a minimal $u$--$v$ cut that contains a prescribed edge."
Without the size bound the stated problem is not the one of Bentert et al. (reading note: remove at most k edges;
equivalently a minimal s-t cut of size at most k+1 containing b), and as written it is easy (an edge lies in some
minimal u-v cut iff it lies on some u-v path). Fix:
`\textsc{Network Diversion} asks, for a prescribed edge $b$ and an integer $k$, for a minimal $u$--$v$ cut with at most $k+1$ edges that contains $b$.`

**E3 [ERR] (record) line 1151** The coupling sentence now transfers only "the lower bound $c(u,v) \geq \beta_1 \log n$
of Lemma 6.5"; the original transferred both bounds of Lemma 6.5. The change is mathematically right (the upper
bound is not monotone) but it changes a claim, is not in `changes-D.md`, and `issues-D.md` item 1 says it is not
applied. Fix: log it in `changes-D.md` ("Made explicit / corrected: only the increasing properties are transferred")
and mark issues-D item 1 as applied, for the owner's approval; keep the text.

**G1 [GAP] line 990** "Then the second cycle contains a path whose ends $x \neq y$ lie on the first cycle and whose
edges do not belong to the first cycle." Asserted without reason. Fix (append):
`To find it, take an edge of the second cycle that is not on the first and follow the second cycle from it in both directions up to the first vertex of the first cycle; the two vertices reached are distinct, because the second cycle contains both ends of the shared edge.`

**N1 [OK-NOTE] line 683** "$u$, $v$ lie only on single edges of the chain": u and v also lie on connecting paths.
Fix: `and, among the subgraphs of the chain, $u$ and $v$ lie only on $H_1$ and $H_{r+1}$.`

**N2 [OK-NOTE] line 732** "by Case~3": the enumerated items (692-724) are not called cases in the text. Fix:
`by item~3 (clause threads)` or label the item and use `\ref`.

**N3 [OK-NOTE] lines 928-936** A_1 is first fixed as the component of u (928), and then the "exchanges" may put u in
A_2. Valid, but a reader may stumble. Optional fix for 928: `We denote the two sides by $A_1$ and $A_2$ in either order.`

**N4 [OK-NOTE] line 170** the class of Theorem 5.1 is stated without "connected"; the theorem assumes it (harmless:
u and v lie in one component by Section 2, and the component inherits the hypothesis). Optional: "in connected graphs in which ...".

**N5 [OK-NOTE] Figure 10** redrawn (PNG -> TikZ PDF). The original drew the end of P with a bend that was not a
vertex; the new drawing reads it as P = u, y1, x, y2, k, v (odd length, all edges in C, counts match the three
bullets). Correct, but it is an interpretation; the author should confirm.

**N6 [OK-NOTE] line 1197** academic titles of M. Loebl removed; owner to confirm (DAM style allows either).

**N7 [OK-NOTE] length** 19 pages vs 15 (SPEC: "about the same or slightly longer"); issue B26 explains 2 of the 4.

No [PRE] findings beyond the editors' issue files. The editors' issues checked and found right: A2, A4, A5, B7,
B10, B11, B13, C2, C3, C7, C8, D1, D3, D4, D7, D10. None is wrong, except that D1 is in fact applied (E3).
