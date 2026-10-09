# Inventory of frag-B-3.tex (Section 3), before editing

Line numbers refer to the original fragment. "Now" column filled in at the end.

| # | Item | Label | Original place | Now |
|---|---|---|---|---|
| 1 | `\section` NP-completeness of the Min Cut-Path Problem | `sec:np-completeness` | l.1 | same |
| 2 | problem box 3-SAT | - | l.9-22 | same |
| 3 | sentence: 3-SAT NP-complete, cite Cook1971Complexity; n, m override | - | l.25-26 | same |
| 4 | two-step plan (3 sentences) | - | l.28-30 | same ("this problem" -> SSP) |
| 5 | `\subsection` The Separating Shortest Path Problem | `sec:ssp` | l.33 | same |
| 6 | problem box SSP (definition of separating shortest path) | - | l.36-47 | same |
| 7 | sentence "Unlike Min Cut-Path, SSP is not an optimization problem ..." | - | l.49 | after SSP box, rephrased into 2 sentences |
| 8 | `\subsubsection` Gadgets and Basic Operations | - | l.54 | 3.1.1, same |
| 9 | gadgets intro + 2-item enumerate (base structure / chain; threads) | - | l.56-62 | 3.1.1, same |
| 10 | Figure chain-threads | `fig:chain-threads` | l.67-72 | 3.1.1 |
| 11 | `\paragraph{Chain.}` + intuition sentence for chain link | - | l.75-76 | 3.1.1 |
| 12 | Definition Chain Link (3 items + positive/negative path + boundary sentence) | `def:chain-link` | l.79-90 | 3.1.1, unchanged |
| 13 | Figure chain-link (uncited) | `fig:chain-link` | l.93-98 | 3.1.1, now cited |
| 14 | intuition sentence for chain | - | l.102 | 3.1.1 |
| 15 | Definition Chain (4 items + "Every u-v path ..." sentence) | `def:chain` | l.104-119 | 3.1.1, unchanged |
| 16 | Figure chain (uncited) | `fig:chain` | l.121-126 | 3.1.1, now cited |
| 17 | list of the three chain-link types (initialization, terminal, literal) with counts n, n, 3m | - | l.130-148 | 3.1.1, same |
| 18 | sentence: links of one variable consecutive (cites fig:chain-link-types) | - | l.150 | 3.1.1, after the total |
| 19 | Figure chain-link-types | `fig:chain-link-types` | l.152-157 | 3.1.1 |
| 20 | sentence: 3m+2n chain links in total | - | l.159 | 3.1.1, directly after the list |
| 21 | `\paragraph{Threads and threading.}` + intuition sentence | - | l.161-162 | 3.1.1 |
| 22 | Definition Thread (2 items) | `def:thread` | l.164-172 | 3.1.1, unchanged |
| 23 | intuition sentence for threading | - | l.175 | 3.1.1 |
| 24 | Definition Threading (3 steps + positively/negatively threaded + "at the edge e") | `def:threading` | l.177-188 | 3.1.1, unchanged |
| 25 | Figure threading (uncited) | `fig:threading` | l.190-195 | 3.1.1, now cited |
| 26 | list of the three thread types (2-sync, 3-sync, clause), each with a "force/encodes" sentence | - | l.198-233 | 3.1.1, + lemma pointers |
| 27 | Figure two-synchronization (inside list) | `fig:two-synchronization` | l.205-210 | 3.1.1, after the list |
| 28 | Figure three-synchronization (inside list) | `fig:three-synchronization` | l.216-221 | 3.1.1, after the list |
| 29 | Figure clause-thread (inside list) | `fig:clause-thread` | l.227-232 | 3.1.1, after the list |
| 30 | `\subsubsection` NP-completeness of SSP + intro sentence | - | l.235-236 | 3.1.2 The Construction (sec:reduction-construction), first sentence |
| 31 | `\paragraph{Auxiliary procedures.}` BuildChain, Thread (+ connecting paths), Calibrate (2 steps, Lambda) | - | l.238-247 | 3.1.2, unchanged |
| 32 | `\paragraph{Auxiliary notation.}` O_i, sign function s | - | l.249-261 | 3.1.2, unchanged |
| 33 | Theorem SSP NP-complete | `thm:ssp-np-complete` | l.263-266 | end of 3.1.3, before its proof |
| 34 | proof: strategy sentence | - | l.269 | proof of Thm 3.9, first sentence (rephrased) |
| 35 | proof: `\paragraph{Reduction from 3-SAT.}` (2 sentences) | - | l.271-273 | 3.1.2, second sentence; 'summarized' -> heading 'The graph of the reduction' |
| 36 | Algorithm 1 (all 21 lines) | `alg:reduction` | l.276-305 | 3.1.2, unchanged, outside the proof |
| 37 | "In words" paragraph (3 sentences) | - | l.307-309 | 3.1.2, after Algorithm 1; last sentence under 'Lengths after the calibration' |
| 38 | proof: `\paragraph{Correctness.}` chain path, hits, hit criterion | - | l.311-315 | 3.1.3 prose before Lemma 3.5 |
| 39 | proof: `\paragraph{Shortest paths.}` (4 sentences) | - | l.317-321 | Lemma 3.5 (lem:chain-paths) + proof |
| 40 | proof: `\paragraph{Synchronization of variable gadgets.}` necessity of hitting, bullet 2-sync, bullet 3-sync, consistent, tau | - | l.323-333 | necessity + consistent + tau: 3.1.3 prose; bullets: proof of Lemma 3.6 (lem:synchronization) |
| 41 | proof: `\paragraph{Clause threads.}` (3 sentences) | - | l.335-338 | Lemma 3.7 (lem:clause-threads) + proof |
| 42 | proof: `\paragraph{Two-way correspondence.}` (a) 4 sentences | - | l.340-348 | proof of Thm 3.9, Correctness (a) |
| 43 | proof: (b) consistent chain path of tau, unused path, dead ends, crossing-edge facts | - | l.350-359 | (b) keeps the tau/P sentence; the rest in proof of Lemma 3.8 (lem:separating), 'The graph G\P' |
| 44 | proof: (b) list of 3 cases (chain edge; synchronization thread; clause thread) + conclusion | - | l.360-373 | proof of Lemma 3.8, 'The edges of Gamma', cases 1-3 (all original sentences) + 'Conclusion' (original final sentence) |
| 45 | proof: `\paragraph{Running time of the reduction.}` (6 sentences) | - | l.376-382 | proof of Thm 3.9, Running time |
| 46 | proof: `\paragraph{Membership in NP.}` (2 sentences) | - | l.384-386 | proof of Thm 3.9, Membership in NP |
| 47 | `\subsection` From SSP to Min Cut-Path + intro sentence | `sec:ssp-to-mcp` | l.389-390 | 3.2, intro rephrased |
| 48 | problem box Min Cut-Path (decision version) | - | l.392-402 | 3.2, unchanged |
| 49 | sentence "The decision version is NP-complete, and hence the optimization version is NP-hard." | - | l.404 | after the proof of Thm 3.10, verbatim |
| 50 | Theorem Min Cut-Path NP-complete | `thm:mcp-np-complete` | l.406-409 | 3.2 |
| 51 | proof: Reduction (4 sentences incl. "We may assume", G' := G) | - | l.412-416 | \paragraph{Reduction.}, all kept + BFS sentence |
| 52 | proof: Correctness (6 sentences) | - | l.418-424 | \paragraph{Correctness.}, unchanged |
| 53 | proof: Membership in NP (3 sentences) | - | l.426-429 | \paragraph{Membership in NP.}, BFS or DFS -> breadth-first search |
| 54 | proof: Conclusion (2 sentences) | - | l.431-433 | \paragraph{Conclusion.}, unchanged |


All 54 items present after the revision (checked 2026-10-09). New: Lemmas 3.5-3.8 with labels lem:chain-paths, lem:synchronization, lem:clause-threads, lem:separating; subsubsection labels sec:reduction-construction, sec:reduction-correctness. All original labels present exactly once.