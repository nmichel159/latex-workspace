# Referee report on the mathematical body of article 2 (`drafts/core.tex`)

Reviewed: `drafts/core.tex` as saved 2026-10-12 18:04 (808 lines; all line numbers refer to this file).
Method: every definition, statement and proof read line by line and re-derived; the degenerate cases of the
brief tried on each statement; every statement of Sections 2-6 tested by an implementation written from the
text (`review/scripts/`, independent of `checks/` except for one cross-check of `cp`).
Not read: anything under `open-cases/`.

## Verdict

1. No mathematical error: all statements of Sections 2-7 are true as written and their proofs are sound, including
   every degenerate case of the brief (coinciding terminals, one-vertex squares, `k = 2`, `S_1`, `S_k`, `d = 1`).
2. One gap (G1): the proof of the linear-time theorem never says how `p_1`, `p_2` come out of the augmentations.
   The two augmenting paths are in general not edge-disjoint; the text has this only in a LaTeX comment.
3. Three places can mislead a careful reader (U1 candidate rule, U2 promise `G in DC`, U3 unattributed standard
   structure); the rest are small precision points with a fix each.
4. The change from directed distances to distances in `G` in the characterization is correct; the proof covers the
   case where `p` is only a part of the trace (explicit 19-vertex instance, point d).
5. As a referee I would ask first for (a) the attribution of Section 3 to the known structure of minimum cuts,
   (b) a version of the algorithm that does not depend on an unverified promise, (c) the fix of G1.

## Findings

Severity: ERROR (false statement), GAP (true statement, incomplete proof), UNCLEAR (wording that admits a wrong
reading), MINOR (precision). There is no ERROR.

| Id | Severity | Location | Problem | Fix |
|---|---|---|---|---|
| G1 | GAP | proof of `thm:linear-time`, l. 660-663 (also `alg:cut-two` l. 627) | "it yields two edge-disjoint `u`-`v` paths" is unexplained. The second augmenting path can traverse an edge of the first backwards (in `G_a` with first path `u,a,b,v` it must: the second is `u,s,b,a,t,v`), the net flow can contain a cycle, and a walk read from the flow need not be a path, while `lem:orientation` to `lem:residual` need paths. The decomposition is mentioned only in the `% CITE` comment. | Replacement text R1 below. |
| U1 | UNCLEAR | `alg:cut-two` l. 638; proof l. 680, 693 | "a neighbor of `x` or of `y` on `q`" can be read as "a vertex of `q` adjacent to `x` in `G`". Then "`q` contains at most two neighbors of `x`" is false and the number of candidates is not bounded (cost `deg(x)` searches). The proof means the edges of `q` at `x` and `y`. | R2 below. |
| U2 | UNCLEAR | `alg:cut-two` l. 624, `thm:linear-time` l. 656, l. 700-701 | The algorithm takes `G in DC` as a promise and never checks it; outside the class it silently returns `d + 1` with a cut-path that need not be minimum (`checks/README.md`: 111 of 4789 instances). The text does not say what happens then, nor that membership is not tested. The promise can be removed at no cost: if line 632 gives `l >= 3` for `x != y`, the pair `x, y` certifies `G notin DC`; otherwise the answer is right in every graph. | R3 below (a strengthening, verified by script: `ALG3`). |
| U3 | UNCLEAR | Section 3 opening l. 185-190; `lem:residual` l. 592; `prop:class` l. 109 | Three statements are proved as if new: (1) `thm:structure`(i)-(iv) is the Picard-Queyranne / strip structure of all minimum cuts for value two (`related-work.md` 0.1); (2) `lem:residual`(i) is the Picard-Queyranne theorem (only a `% CITE` comment); (3) "`c(x,y) >= 3` is an equivalence relation" is the standard notion of 3-edge-connected classes (no comment at all). A referee reads silence as a claim of novelty. | One sentence at each place: R4 below. Sources: those verified in `related-work.md`, not checked by me. |
| M1 | MINOR | `lem:basic-bounds` l. 34 | Corollary 3.12 of article 1 states NP-completeness of deciding `cp = d`; the equivalence with a separating shortest path is in its proof (and in the proof of Theorem 3.11). | `\begin{lemma}[{\cite[Lemma~2.3 and the proof of Corollary~3.12]{Michel2026MinCutPath}}]` |
| M2 | MINOR | `thm:hardness` l. 757 | "at least three pairwise edge-disjoint `u`-`v` paths, the threads": article 1 gives `2n + 7m` threads, which is 2 for the formula with one variable and no clause. | `For a formula with at least one clause, the graph constructed in that reduction is connected and contains $2n + 7m \geq 9$ pairwise edge-disjoint $u$--$v$ paths, the threads.` |
| M3 | MINOR | l. 807 | Theorem 5.5 of article 1 states `cp = c + d - 1`; the sentence is its consequence through `prop:open-pairs` (or a step of its proof). | `In a graph of diameter two, $\cp(u, v) = c(u, v) + 1$ for every pair with $d(u, v) = 2$~\cite[Theorem~5.5]{Michel2026MinCutPath}, so by \cref{prop:open-pairs} no minimum $u$--$v$ cut contains a $u$--$v$ path.` |
| M4 | MINOR | l. 745 | "a square can be an arbitrary graph": the construction gives every connected graph `G` with `c_G(u,v) >= 3` as the square, with terminals `u,u,v,v`; for `c_G(u,v) = 2` the graph is split (said in l. 783). | `Without the bound on the distances between terminals, every connected graph $G$ with $c_G(u, v) \geq 3$ occurs as a square with the terminals $u, u, v, v$, and deciding ...` |
| M5 | MINOR | proof of `thm:structure`(v) l. 357-358 | `|δ(B)| <= 2` is stated without a reason (the lemma on minimum cuts is stated for `u, v` only). | Insert after l. 357: `Every edge with exactly one end in $B$ belongs to this cut.` |
| M6 | MINOR | proof of `cor:two-edges` l. 583 | "it contains all edges of the path in `S_i`" has no reason. | `..., and it contains all edges of the path in $S_i$, because an edge of a path joins two consecutive vertices of the path.` |
| M7 | MINOR | l. 563-565 | The directed form of the characterization is asserted in one sentence. | Add: `Indeed, by \cref{prop:lengths} the equation holds if and only if some shortest $u$--$v$ path contains $g$ and $h$ and has the trace $p$ in $S_i$, and for such a path $\alpha_i = \alpha$ and $\beta_i = \beta$, so \cref{lem:criterion} applies.` |
| M8 | MINOR | running time l. 688-697 | The representation is not named, and the cost of "marking the neighbors of `x` and of `y`" and of the test `xy in E` is bounded by `n_i + m_i` only because a vertex of `S_i` has at most four edges outside `S_i`. | `The graph is given by adjacency lists.` and `A vertex of $S_i$ is an end of at most four edges outside $S_i$, the edges that enter or leave $S_i$, so its neighbors are marked in $O(m_i + 1)$ time.` |
| M9 | MINOR | `lem:criterion` l. 451, `prop:lengths` l. 536 | The statements rely on the section-wide hypothesis `c(u,v) = 2` (l. 186); quoted alone they are incomplete. `thm:structure`, `thm:characterization`, `lem:residual`, `cor:two-edges` restate it. | Start `lem:criterion` with `Let $c(u, v) = 2$, and let $R$ be a $u$--$v$ path.` |
| M10 | MINOR | notation, l. 290-292, 476-477 | `c_i`, `d_i` are vertices while `c(·,·)`, `d(·,·)` are the cut-value and the distance; both occur in the statement of `thm:characterization`. `m` is an index (l. 293), `m(A,B)` (l. 77) and `m_i` (l. 691); `s`, `t` are vertices of `G_a`, two terminals (l. 356) and tail and head (l. 532). No clash makes a statement ambiguous, but `d(d_i, v)` is one substitution away. | If the notation of the thesis may change: leaving terminals `a_i'`, `b_i'`. Otherwise leave. |
| M11 | MINOR | l. 66, 370, 605 | "leaves", "enters" are defined for edges of `F` and pieces (l. 218) and are used informally for a path or an edge and an arbitrary vertex set. | l. 66: `no edge of $G \setminus C$ has exactly one end in $A'$`; l. 370: `this path contains at least two edges of $\delta(W \cap B)$`; l. 605: keep. |
| M12 | MINOR | `thm:linear-time` proof l. 660-665 vs. `alg:cut-two` l. 627 | The paths are computed in the first step of the proof and again in line 2 of the algorithm; "residual graph" in l. 662 is that of the current flow, not the digraph `D` of l. 588. | In R1: line 2 uses the paths of the first step; say "the residual graph of the current flow". |

### R1 (for G1): replacement of l. 660-663

```latex
The algorithm first computes, by at most three augmentations, a flow from $u$ to $v$ of value at most three in which every edge of $G$ carries at most one unit.
% CITE: augmenting paths (Ford and Fulkerson).
Each augmentation is a search in the residual graph of the current flow and takes $O(|V| + |E|)$ time.
The first augmentation succeeds because $G$ is connected.
The cut-value $c(u, v)$ is one if the second augmentation fails, two if the third one fails, and at least three otherwise.
Let $c(u, v) = 2$.
The two augmenting paths need not be edge-disjoint, because the second one can traverse an edge of the first one backwards, which cancels the flow on this edge.
The paths $p_1$ and $p_2$ are therefore read from the flow of value two.
Let $H$ be the directed graph formed by the edges that carry flow, each directed along the flow.
In $H$, the vertex $u$ has two more leaving than entering arcs, the vertex $v$ has two more entering than leaving arcs, and every other vertex has as many entering as leaving arcs.
No arc of $H$ leaves the set $X$ of the vertices that can be reached from $u$, so the vertices of $X$ have in total at most as many leaving as entering arcs, and hence $v \in X$.
A search in $H$ therefore finds a $u$--$v$ path $p_1$.
After the removal of the arcs of $p_1$, the same argument with one in place of two gives a $u$--$v$ path $p_2$.
The paths $p_1$ and $p_2$ are edge-disjoint paths of $G$, and the arcs of $H$ that remain form cycles and are not used.
Line~\ref{line:paths} of \cref{alg:cut-two} takes these two paths.
```

### R2 (for U1)

Line 638:

```latex
\State $\mathcal{P} \gets$ the set of the paths $x, w, y$ of $S_i$ such that $xw$ or $wy$ is an edge of $q$ \label{line:candidates}
```

Line 680: `..., so it contains the edge $xw$ or the edge $wy$.`

Line 693:

```latex
The path $q$ has at most two edges at $x$ and at most two edges at $y$, so $\mathcal{P}$ has at most four members.
Whether $x, w, y$ is a path of $S_i$ is decided for each of these vertices $w$ after marking the neighbors of $x$ and of $y$.
```

### R3 (for U2): the algorithm without the promise

In `alg:cut-two`, input "a connected graph `G`", and after l. 632:

```latex
        \If{$\ell \geq 3$}
            \State mark the pair $x, y$ \Comment{$c(x, y) \geq 3$ and $d(x, y) \geq 3$}
        \EndIf
```

and before the last line: `if a pair is marked, return it together with $R \cup C$`.
Statement:

```latex
There is an algorithm that, given a connected graph $G = (V, E)$ and two distinct vertices $u, v$ of $G$, decides in $O(|V| + |E|)$ time whether $c(u, v) \leq 2$.
If so, it returns $\cp(u, v)$ and a minimum cut-path between $u$ and $v$, or it returns two vertices $x, y$ with $c(x, y) \geq 3$ and $d(x, y) \geq 3$ and a cut-path with $d(u, v) + 1 \leq \cp(u, v) + 1$ edges.
The second outcome does not occur for $G \in \DC$.
```

Proof (two sentences added to the correctness part):

```latex
A path returned in line~\ref{line:found} is a separating shortest $u$--$v$ path in every graph.
If line~\ref{line:length} gives $\ell \geq 3$ for two terminals $x \neq y$, then $d(x, y) \geq \ell \geq 3$ because $d(u, v) \leq d(u, x) + d(x, y) + d(y, v)$, and $c(x, y) \geq 3$ by \cref{thm:structure}(v).
If it gives $\ell \leq 2$ for all of them, every path $p$ with (i) and (ii) has $|p| = \ell \leq 2$, and the algorithm finds one.
```

`cor:two-edges` is then needed only for the last sentence of the statement.
Why this matters to a referee: a 3-edge-connected graph lies in `DC` iff it has diameter at most two, so recognizing
`DC` contains recognizing diameter two on such graphs; I know no linear-time algorithm for that
(`TODO(verify)`: conditional lower bounds for distinguishing diameter 2 from 3; from memory, not a verified source).
The paper should say that membership is not tested, or use the version above, which does not need it.

### R4 (for U3)

Opening of Section 3, after l. 190 (keys as verified in `related-work.md`, to be re-checked by the integrator):

```latex
The structure of all minimum $u$--$v$ cuts is known: they are the sets closed in the residual graph of a maximum flow~\cite{PicardQueyranne1980}.
For $c(u, v) = 2$ this structure is a chain, and we describe it and prove its properties directly, because \cref{sec:separating,sec:algorithm} use the terminals of the squares.
```

Before `lem:residual`: turn the `% CITE` comment into a citation and say `Statement (i) is the theorem of Picard
and Queyranne for the flow of value two; we give the short proof for undirected graphs.`
In `prop:class`: `The classes are the 3-edge-connected components of $G$ in the sense of~\cite{Mehlhorn2017Certifying}.`

## Outcome for the points a-m

**a. Lemma on minimum cuts.** Correct (two components, `C = δ(A)`, uniqueness of `A`, parity). The third-component
argument is complete: the edge at `Y'` joins two components of `G \ C`, hence lies in `C = δ(A)`, hence joins `A` to
`Y'`, so `δ(Y)` is a smaller cut. Its "use for `s`, `t`" in `thm:structure`(v) is not a use of the lemma: the proof
needs only `δ(B) ⊆` (the removed cut), which holds trivially but is not said (M5). Checked: by hand; `misc.py`
(`MINCUT-*`, all graphs with at most 6 vertices, all pairs, all cut-values, uniqueness over all sets `A`).

**b. Square decomposition.** (i) `A_1 ∪ A_2` is the right set for the entering edges and `B_1 ∩ B_2` for the leaving
ones (the tails of `g_j` lie in `A_j`, the heads in `S_i`, which is disjoint from both `A_j` by `lem:pieces`(i));
`g_1 ≠ g_2` because `p_1`, `p_2` are edge-disjoint; `i ≥ 2` gives `u ∉ S_i`. (iii) Uniqueness is right: a general
path is determined by its first edge, it cannot stop at a link and cannot pass a square; every edge of `F` and every
link lies between exactly one pair of consecutive squares on exactly one `p_j`. (v) All cases hold: the swap of
`s, t` with `B, V \ B` keeps `s ∈ B`, `t ∉ B`, `|δ(B)| ≤ 2` (connectedness of `B` is not used afterwards);
`s ∉ {u, v}` makes `s` a head of an entering edge (`i ≥ 2`) or a tail of a leaving edge (`i < k`); for `W = V \ A`
the lemma on uncrossing applies to arbitrary sets and `|δ(W)| = 2`; `z ∉ B` gives `m(W,B) ≥ 1`; `z ∈ B` gives
`|δ(W ∩ B)| ≥ 2` because `z ∉ {u, v}` lies on `p_1` or `p_2`. Checked: by hand; `statements.py` (`STR1`-`STR5`,
`DEG`, `PIE`; `STR5`: 38758 pairs of terminals, no failure; a mutation to `c ≥ 4` fails).

**c. Separation criterion.** Both directions correct. When both entering edges have the same head, `α_i = x_i`,
and the first vertex of `Q` in `S_i` is still the head of the edge of `Q`, which is the entering edge not on `R`;
nothing breaks. For `r = 0` the general path is one edge not on `R`. Checked: by hand; `CRI` on every `u`-`v` path
(323680 paths for the full decomposition); the mutation "`x_i` for `α_i`" fails.

**d. Characterization.** Correct. A walk with `d(u,v)` edges is a path. For `α_i ≠ α` necessarily
`(x_i, α_i) = (α, x)`, and the part of the trace before `x` joins `α` to `x` without an edge of `p`; the same at
the end. I tried to break it: graph `H1` (`attack_characterization.py`, 19 vertices, full decomposition) has the
witness `(x, α) = (x, A)`, `p = x,w,y` with `d(u,x) = 2` attained only through `α = A`; a second witness `p = A,x,w`
ends before the leaving terminal that the path uses. In both the walk of the proof is a separating shortest path
and `cp = d = 5`. In the class this case cannot occur for the full decomposition (a trace has at most two edges and
a one-edge `p` would give a one-edge `u`-`v` cut), so the change of the blueprint matters only outside the class and
for coarser decompositions (36 such witnesses among the chains). `x = α`, `i = 1`, `i = k`: trivial cases, fine.
Checked: `CHA` (cp = d iff a witness exists), `CHA+` (every choice of `R_x`, `R_y`), mutations of (i) and (ii) fail.

**e. Lengths.** Correct. `A`, `S_i`, `V \ (A ∪ B)` are pairwise disjoint; `R^-` stays in `A` and `R^+` outside
`A ∪ B` because no directed path enters `A` or `B`; `h ∉ δ(A)` since a leaving edge of `S_i` is not an entering
edge. Checked: `LEN-ii` against the brute-force minimum over all paths, including existence (342348 triples);
`LAM` for the directed form of the theorem.

**f. Corollary "two edges".** Proved; the missing half-sentence is M6 (an edge of a path with both ends in `S_i`
joins consecutive vertices of the path, which are consecutive in the trace).

**g. Residual-graph lemma.** Both parts correct, including "closed sets give cuts of size exactly two" and
`u ∈ A`, `v ∉ A` in (ii). The lemma is stated for the fixed edge-disjoint paths `p_1`, `p_2` and is explicit about
it ("the flow that sends one unit along `p_1` and one along `p_2`"): nothing to change in l. 587-618. The lemma
does not say and need not say where the paths come from; the proof of the theorem must (G1).
`flow_paths.py`: on 16 of 13350 ordered pairs the two breadth-first augmenting paths share an edge (the same count
as `checks/README.md`); cancellation is forced whenever the first augmenting path is a separating path, in
particular a separating shortest path, the positive instances of the paper (26 pairs). Checked: `RES-i` for all
sets `A` with `u ∈ A`, `v ∉ A` (4.9 million sets), `RES-ii`.

**h. Algorithm and linear time.** Correct modulo G1, U1. Details: `l ≤ d(x,y)` by the triangle inequality, so
`l = 2` with `x`, `y` adjacent cannot occur, `l ≤ 0` admits no path between distinct `x, y`, and `l ≥ 3` cannot
occur in the class (and certifies non-membership, R3). The conditions `x ≠ y`, `α ≠ β` skip no witness (a path
with (ii) has an edge and separates `α` from `β`). Both return lines give minimum cut-paths (`R ∪ C` has `d + 1`
edges since `R` has one edge of the minimum cut `C`; `k ≥ 2` makes `C` exist). Every line is linear: an edge lies
in `S_i` iff both ends carry the label of `S_i`; the neighbors of `x`, `y` on `q` are read off `q`; adjacency
tests cost `O(m_i + 1)` (M8). "Three augmentations decide `c ∈ {1, 2, ≥ 3}`": right. The promise `G ∈ DC` is used
only through `cor:two-edges`; the theorem is true as a promise statement but see U2. Checked: `ALG-star`,
`ALG3`, `ALG-returns-a-cut-path`, `ALG-at-most-4-candidates` for both readings of U1; `algorithm_examples.py`.

**i. Coarser decompositions.** Confirmed. With `F'` the union of a nonempty family, every proof step of
`lem:orientation`, `lem:pieces`, `lem:degrees`, `thm:structure`(i)-(iv), `lem:criterion`, `thm:characterization`
uses a minimum cut that is either a member of the family (chosen for an edge of `F'`) or the cut of the two
entering or leaving edges of a square, which lies in `F'`; `lem:pieces`(i) is applied to no other cut. (v) uses the
cuts `δ(B)`, `δ(W ∪ B)`, which need not lie in `F'`. Checked: all nonempty sub-families when there are at most 6
minimum cuts, sampled otherwise (22382 + 72402 + 4754 decompositions): no failure of the primed tests; (v) fails
for 228870 pairs of terminals, as the remark says. `prop:lengths` also holds for `F'` (not claimed).

**j. Hardness.** Correct. NP membership: one search for `d(u,v)`, one in `G \ P`; the promise `c(u,v) = 2` is
decidable in polynomial time. Article 1: Theorem 3.10 is the NP-completeness of \SSP; its graphs are connected and
the threads are `2n + 7m` pairwise edge-disjoint `u`-`v` paths (stated after the theorem), see M2. Padding: every
`u'`-`v` path is `u', s_j, u` plus a `u`-`v` path of `G`; distances, cut-value and the equivalence are right. The
decomposition of `G'` is as described for `c_G ≥ 3` and for `c_G = 2`. Checked: `misc.py` `PAD-*` (2836 pairs).

**k. Pairs at distance two.** `prop:open-pairs` is correct for every pair. The sentence on diameter two is a
consequence of Theorem 5.5, not its statement (M3). `G_b`: `δ({u,s,b}) = {ua, ab, bv}`, checked.

**l. Examples.** All stated values recomputed (`examples.py`): 81 claims, 0 mismatches, `cp` by three
computations. The figures `worked-example`, `decomposition-example`, `counterexamples`, `square-terminals`,
`padding`, `square-decomposition` agree with the text.

**m. Terminology and notation.** "trace", "visits", "terminals", the double use of a symbol for a piece and its
vertex set and `S_i \ p` are used consistently with their definitions. Informal "enter/leave" for sets: M11.
Symbol clashes: M10. No statement is used before it is proved; `def:decomposition` rests on `lem:degrees`, which
precedes it.

## Referee's judgment

- **Stated as new but standard:** U3. The body itself makes no novelty claim (no Introduction), but proofs without
  attribution read as one.
- **Missing hypotheses:** none that makes a statement false; M9.
- **Stronger than proved:** nothing. `thm:linear-time` is weaker than what the proof gives (R3).
- **Three points I would raise first:** (1) Section 3 re-derives the known representation of minimum cuts; what is
  new is the criterion, the characterization and the algorithm, and the paper must say so. (2) The main algorithm
  works under a promise that is not known to be testable in linear time; make it robust (R3) and fix G1. (3) The
  class is solved only for pairs with `c ≤ 2`; pairs with `d = 2`, `c ≥ 3` stay open, and the hardness theorem is
  a padding of a result from an unpublished manuscript (`related-work.md` 0.6): title and abstract must not
  promise more.

## Not settled

- The sentences of `rem:coarser` about the thesis (the construction by three transformations, "can stop before all
  edges of `F` are removed"). Definitions 38-40 of the thesis were read in the extracted text and agree with
  "general square graph"; the construction was not checked.
- The literature attributions of R4 and the recognition remark in R3 rest on `related-work.md` and on memory.
- The numbers of article 1 (2.3, 3.10, 3.12, 5.5, 6.1, 6.2) are those of its build of 2026-10-10 and of the
  current source; article 1 is a manuscript and they can move.

## Scripts (`review/scripts/`) and results

| Script | What it does | Result |
|---|---|---|
| `ref.py` | own library: graphs, searches, cut-value, `cp` (two ways), class test, decomposition for a family of minimum cuts | - |
| `examples.py` | every value of the six example graphs | `results-examples.txt`: 81 claims, 0 mismatches |
| `statements.py`, `run_statements.py` | statements of Sections 3-5 in the written form; all sub-families of minimum cuts; algorithm as printed (two readings) | `results-statements.txt`: 11895 instances (7395 pairs on all graphs with 2-7 vertices, 3000 chains, 1500 random graphs), 0 failures; 9 mutations of the checker all detected |
| `misc.py` | preliminaries, bridges, open pairs, padding | `results-misc.txt`: 0 failures |
| `flow_paths.py` | augmenting paths versus edge-disjoint paths; net flow with a cycle; two searches in the net flow | `results-flow-paths.txt` |
| `attack_characterization.py` | graph `H1` and a random search against `thm:characterization` | `results-attack-characterization.txt`: 0 failures |
| `algorithm_examples.py` | printed algorithm on `G_a^+` and on the 21-vertex graph of `checks/README.md` | `results-algorithm-examples.txt`: 3 and 9, as brute force |

Run from `review/scripts/` with `python -B <script>` (`run_statements.py --maxn 7 --chains 3000 --random 1500`).
Limits: exhaustive only up to 7 vertices; chains up to 16 vertices; the tests support the statements, the proofs
were checked by reading.
