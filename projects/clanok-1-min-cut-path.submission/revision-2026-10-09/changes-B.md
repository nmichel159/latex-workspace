# Changes in frag-B-3.tex (Section 3)

## Structure (Exposition)
- New outline: 3 intro + 3-SAT box + plan; 3.1 SSP box; 3.1.1 Gadgets (unchanged order); 3.1.2 The Construction (`sec:reduction-construction`); 3.1.3 Correctness of the Reduction (`sec:reduction-correctness`): prose definitions, Lemmas `lem:chain-paths`, `lem:synchronization`, `lem:clause-threads`, `lem:separating`, then Theorem `thm:ssp-np-complete` with its proof; 3.2 unchanged in content.
- Old subsubsection "NP-completeness of SSP" became 3.1.2 "The Construction"; its intro sentence kept (with a reference to the theorem) and the proof's "Reduction from 3-SAT" paragraph (two sentences) moved there.
- Algorithm 1 moved out of the proof into 3.1.2, after the procedures and the notation, under a new run-in heading "The graph of the reduction" (one sentence: G, u, v denote its output).
- "In words" paragraph kept after Algorithm 1; its calibration sentence now under the run-in heading "Lengths after the calibration".
- Theorem 3.x moved from before the proof's construction to the end of 3.1.3; its proof keeps (a)/(b), running time, membership in NP and now cites the four lemmas.
- Old proof paragraphs "Correctness" (chain path, hits, hit criterion), "Synchronization" (necessity of hitting every thread; definition of consistent; tau) moved to the prose before the lemmas.
- "Shortest paths" paragraph became Lemma `lem:chain-paths` with proof; "Synchronization of variable gadgets" became Lemma `lem:synchronization` (both bullets kept verbatim); "Clause threads" became Lemma `lem:clause-threads`; the separating argument of (b) became Lemma `lem:separating`.
- Lemma `lem:separating`: original sentences (unused path, dead ends, crossing edges, three cases with every original sentence) kept; added the auxiliary multigraph Gamma (nodes u, v, unused paths K°; edges = connecting paths with two open ends), the reduction "u-v path in G\P => u-v walk in Gamma", the edge list of Gamma per case, and a conclusion that makes the case analysis complete.
- Figures 7-9 moved out of the `enumerate` of thread types to directly after it (no longer indented with the list); each item still cites its figure.
- Thread-type items: each "force/encodes" sentence now ends with a pointer to the lemma that proves it.
- 3.2: "The decision version is NP-complete, and hence the optimization version is NP-hard." moved after the proof (kept verbatim).

## Language
- Section intro: "starting from the 3-SAT problem" -> "by a reduction from the 3-SAT problem"; plan: "this problem" -> "SSP".
- "Unlike Min Cut-Path, SSP is not an optimization problem, which makes the reduction ... more direct" -> two sentences: a solution is a single shortest path, i.e., a cut-path of size d(u,v) (see the proof of Theorem `thm:mcp-np-complete`); "This makes the reduction from 3-SAT more direct." (The equivalence is proved in 3.2; no new claim. Flagged in issues-B #14.)
- Proof of Theorem 3.x: "We first describe the reduction, then prove its correctness, and finally ..." -> "The reduction is Algorithm 1; we prove its correctness, bound its running time and show that SSP belongs to NP."
- "We now show that the constructed instance ... is equivalent" -> "The constructed instance ... is equivalent ...:"; "We complete the proof by establishing the equivalence" merged into it.
- (a) "one can extract a satisfying assignment" -> "a satisfying assignment ... can be extracted from P"; (b) "one can construct" -> "can be constructed from it".
- "It remains to show that P is separating" -> in Lemma `lem:separating`: "By Lemma 3.5, P is a shortest u-v path, so we have to show that G\P contains no u-v path."
- Running time: "It remains to show that the reduction runs in polynomial time." -> "The reduction runs in polynomial time."; "requires O((n+m)^2) edges" -> "adds".
- 3.2 intro: "We now reduce SSP to Min Cut-Path" -> "The second step reduces SSP to Min Cut-Path".
- 3.2 membership: "(e.g., by BFS or DFS)" -> "(e.g., by breadth-first search)".
- Long sentences split (check-text): end-vertex degree sentence; connecting-path sentence in the Gamma claim.

## Made explicit
- Lemma `lem:chain-paths`: every u-v path using only chain edges is a chain path (Definition 3.2); edges outside the chain are connecting-path edges; internal vertices of connecting paths have degree two (Thread creates them new and internally disjoint, Calibrate adds degree-two vertices); Q contains a whole connecting path because u, v are not internal vertices of one; every thread has at least two crossing edges, so no connecting path joins u and v directly.
- 3.1.2 "In words": "Every thread passes through at least two chain links, so it has at least two crossing edges."
- 3.1.2 "Lengths after the calibration": the subdivided 4-cycles are again chain links, the chain in G is a u-v chain (Definition 3.2), its u-v paths have Lambda edges, connecting paths at least Lambda.
- Lemma `lem:synchronization`: the block of x_i consists of I_i, the L_{j,k,i} with (j,k) in O_i, and T_i; both directions of "hits all sync threads iff consistent" spelled out from the two bullets.
- Lemma `lem:clause-threads`: why "traverses the path of sign s(l_j)" equals "tau satisfies l_j".
- Prose before the lemmas: "consistent chain path of tau" named (the sentence of (b) defining it is kept in (b) too).
- Lemma `lem:separating`: why the connecting paths at a crossing edge on P are dead ends (degree three -> one, not u or v).
- Lemma `lem:separating`: completeness of the case analysis (Gamma; cases exhaustive because every edge is a chain edge or a connecting-path edge and every thread is a synchronization or a clause thread; per-thread edge list for tau(x_i)=true, symmetric for false; walk argument in the conclusion).
- Theorem 3.x proof (a): "by Lemma ..." references; (b) now cites Lemma `lem:separating`.
- 3.2 Reduction: "The threshold k is computed by breadth-first search, so the reduction runs in polynomial time." (the Conclusion already claims polynomial time).
- 3.2 proof starts with a sentence ("We reduce SSP to the decision version of Min Cut-Path and use Theorem 3.x.") so that "Proof." does not attach to a heading.

## Formatting
- Figures 3, 4, 6 now cited before they appear ("Figure 3 shows a chain link." etc.).
- Lemma environments named in brackets: Shortest paths, Synchronization, Clause threads, Separation.
- Proof of Theorem 3.x and of Theorem 3.10 use `\paragraph{...}` for their headings (3.2 previously `\textbf`).
- Steps inside the proof of Lemma `lem:separating` are run-in `\emph` headings (The graph G\P; The auxiliary multigraph Gamma; The edges of Gamma; Conclusion).
- "The total number of ... chain links is ..." split to one sentence per line; the total 3m+2n moved directly after the list, before the figure sentence.
- Blank-line clutter between environments removed.

## Citations
- None added or changed. No bib keys to add.
