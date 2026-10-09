# Inventory of frag-B-3.tex (Section 3), before editing

Line numbers refer to the original fragment. "Now" column filled in at the end.

| # | Item | Label | Original place | Now |
|---|---|---|---|---|
| 1 | `\section` NP-completeness of the Min Cut-Path Problem | `sec:np-completeness` | l.1 | |
| 2 | problem box 3-SAT | - | l.9-22 | |
| 3 | sentence: 3-SAT NP-complete, cite Cook1971Complexity; n, m override | - | l.25-26 | |
| 4 | two-step plan (3 sentences) | - | l.28-30 | |
| 5 | `\subsection` The Separating Shortest Path Problem | `sec:ssp` | l.33 | |
| 6 | problem box SSP (definition of separating shortest path) | - | l.36-47 | |
| 7 | sentence "Unlike Min Cut-Path, SSP is not an optimization problem ..." | - | l.49 | |
| 8 | `\subsubsection` Gadgets and Basic Operations | - | l.54 | |
| 9 | gadgets intro + 2-item enumerate (base structure / chain; threads) | - | l.56-62 | |
| 10 | Figure chain-threads | `fig:chain-threads` | l.67-72 | |
| 11 | `\paragraph{Chain.}` + intuition sentence for chain link | - | l.75-76 | |
| 12 | Definition Chain Link (3 items + positive/negative path + boundary sentence) | `def:chain-link` | l.79-90 | |
| 13 | Figure chain-link (uncited) | `fig:chain-link` | l.93-98 | |
| 14 | intuition sentence for chain | - | l.102 | |
| 15 | Definition Chain (4 items + "Every u-v path ..." sentence) | `def:chain` | l.104-119 | |
| 16 | Figure chain (uncited) | `fig:chain` | l.121-126 | |
| 17 | list of the three chain-link types (initialization, terminal, literal) with counts n, n, 3m | - | l.130-148 | |
| 18 | sentence: links of one variable consecutive (cites fig:chain-link-types) | - | l.150 | |
| 19 | Figure chain-link-types | `fig:chain-link-types` | l.152-157 | |
| 20 | sentence: 3m+2n chain links in total | - | l.159 | |
| 21 | `\paragraph{Threads and threading.}` + intuition sentence | - | l.161-162 | |
| 22 | Definition Thread (2 items) | `def:thread` | l.164-172 | |
| 23 | intuition sentence for threading | - | l.175 | |
| 24 | Definition Threading (3 steps + positively/negatively threaded + "at the edge e") | `def:threading` | l.177-188 | |
| 25 | Figure threading (uncited) | `fig:threading` | l.190-195 | |
| 26 | list of the three thread types (2-sync, 3-sync, clause), each with a "force/encodes" sentence | - | l.198-233 | |
| 27 | Figure two-synchronization (inside list) | `fig:two-synchronization` | l.205-210 | |
| 28 | Figure three-synchronization (inside list) | `fig:three-synchronization` | l.216-221 | |
| 29 | Figure clause-thread (inside list) | `fig:clause-thread` | l.227-232 | |
| 30 | `\subsubsection` NP-completeness of SSP + intro sentence | - | l.235-236 | |
| 31 | `\paragraph{Auxiliary procedures.}` BuildChain, Thread (+ connecting paths), Calibrate (2 steps, Lambda) | - | l.238-247 | |
| 32 | `\paragraph{Auxiliary notation.}` O_i, sign function s | - | l.249-261 | |
| 33 | Theorem SSP NP-complete | `thm:ssp-np-complete` | l.263-266 | |
| 34 | proof: strategy sentence | - | l.269 | |
| 35 | proof: `\paragraph{Reduction from 3-SAT.}` (2 sentences) | - | l.271-273 | |
| 36 | Algorithm 1 (all 21 lines) | `alg:reduction` | l.276-305 | |
| 37 | "In words" paragraph (3 sentences) | - | l.307-309 | |
| 38 | proof: `\paragraph{Correctness.}` chain path, hits, hit criterion | - | l.311-315 | |
| 39 | proof: `\paragraph{Shortest paths.}` (4 sentences) | - | l.317-321 | |
| 40 | proof: `\paragraph{Synchronization of variable gadgets.}` necessity of hitting, bullet 2-sync, bullet 3-sync, consistent, tau | - | l.323-333 | |
| 41 | proof: `\paragraph{Clause threads.}` (3 sentences) | - | l.335-338 | |
| 42 | proof: `\paragraph{Two-way correspondence.}` (a) 4 sentences | - | l.340-348 | |
| 43 | proof: (b) consistent chain path of tau, unused path, dead ends, crossing-edge facts | - | l.350-359 | |
| 44 | proof: (b) list of 3 cases (chain edge; synchronization thread; clause thread) + conclusion | - | l.360-373 | |
| 45 | proof: `\paragraph{Running time of the reduction.}` (6 sentences) | - | l.376-382 | |
| 46 | proof: `\paragraph{Membership in NP.}` (2 sentences) | - | l.384-386 | |
| 47 | `\subsection` From SSP to Min Cut-Path + intro sentence | `sec:ssp-to-mcp` | l.389-390 | |
| 48 | problem box Min Cut-Path (decision version) | - | l.392-402 | |
| 49 | sentence "The decision version is NP-complete, and hence the optimization version is NP-hard." | - | l.404 | |
| 50 | Theorem Min Cut-Path NP-complete | `thm:mcp-np-complete` | l.406-409 | |
| 51 | proof: Reduction (4 sentences incl. "We may assume", G' := G) | - | l.412-416 | |
| 52 | proof: Correctness (6 sentences) | - | l.418-424 | |
| 53 | proof: Membership in NP (3 sentences) | - | l.426-429 | |
| 54 | proof: Conclusion (2 sentences) | - | l.431-433 | |
