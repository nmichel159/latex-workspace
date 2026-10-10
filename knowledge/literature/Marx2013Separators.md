# Marx2013Separators

| | |
|---|---|
| Paper | Marx, O'Sullivan, Razgon: *Finding small separators in linear time via treewidth reduction*. ACM Transactions on Algorithms 9(4), 2013, 1-35. DOI 10.1145/2500119; arXiv:1110.4765 |
| Key | `Marx2013Separators` |
| Reading status | parts read 2026-10-10 in the preprint arXiv:1110.4765v1 (the only arXiv version): Sections 1, 2 and 3.1-3.3. The journal text was not compared, so every number below is the preprint's. The statements used in article 1 were compared once more with the text of the preprint on 2026-10-10 (second pass): they match |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), sections 3 and 5b |

## What the paper does

- For two vertices `s`, `t` and an integer `k`, all inclusion-minimal `s`-`t` vertex separators with at most `k`
  vertices lie in a vertex set whose torso has treewidth bounded by a function of `k`; the set is found in linear
  time for fixed `k`. Constrained separation problems are then solved on the torso with Courcelle's theorem.
- Definition of FPT with a computable `f` (Section 1, p. 1). Tree decompositions, brambles, Theorem 2.1
  (bramble number = treewidth + 1), Theorem 2.2 (Courcelle: a property expressed by an MSO formula `phi` is
  recognized in time `f_phi(tw(G)) (|E(G)| + |V(G)|)`), with the remark that it extends to graphs with vertex and
  edge labels (Section 2.1).
- Definition 2.3: an `s`-`t` separator is a vertex set disjoint from `{s, t}` with `s`, `t` in different components
  of `G \ S`; minimal = inclusion-minimal. If `s`, `t` are adjacent, no separator exists.
- Definition 2.5: `torso(G, C)` has vertex set `C`; `a`, `b` are adjacent if `ab` is an edge of `G` or `G` has an
  `a`-`b` path with all internal vertices outside `C`.
- Proposition 2.7: for `a, b` in `C` and `S` a subset of `C`, `S` separates `a` and `b` in `torso(G, C)` iff in `G`.
- Corollary 2.10: `tw(torso(G, C u X)) <= tw(torso(G, C)) + |X|`.
- Lemma 2.11: with `l` the minimum size of an `s`-`t` separator and `e = k - l`, a set `C'` that contains every
  minimal `s`-`t` separator of size at most `k`, is disjoint from `{s, t}` and has `bn(torso(G, C')) <= g(l, e)`
  is computed in time `f(l, e) (|E(G)| + |V(G)|)`. Remark 2.13: adding `s`, `t` increases the treewidth by at
  most 2. Remark 2.14: `g(l, e) = 2^O(el)`, and an exponential bound is necessary (hypercube).
- Theorem 2.15 (treewidth reduction theorem): a graph `G*` of treewidth `h(k, |T|)` that has the same minimal
  separators of size at most `k` between the terminals `T` and induces the same graph on them.
- Section 3.3: a connected `s`-`t` separator of size at most `k` is found in linear FPT time; the solution is not
  inside `C'`, so `C'` is enlarged by small trees through the components of `G \ C'` (Lemma 3.6, Theorem 3.7).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| vertex separators, `G \ S` deletes vertices | edge cuts, `G \ F` removes edges | we pass to the graph `G'` in which every edge is subdivided by a vertex `z_e`; an edge cut `F` becomes the separator `{z_e : e in F}` |
| bound on the bramble number `bn` | treewidth | `bn = tw + 1` (their Theorem 2.1) |
| parameters `l` and `e = k - l` | one parameter `k` (`= b`) | `l <= k`, so the bounds are functions of `k` |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| set `D` with all minimal separators of size at most `k`, torso of bounded treewidth | Lemma 2.11, Remark 2.13 | article 1, Section 8 "Fixed-Parameter Tractability", Lemma `lem:treewidth-reduction` (8.2) | `s`, `t` non-adjacent; a separator of size at most `k` exists (so `e >= 0`); `l > 0` in their Lemma 2.4, which holds when `s`, `t` lie in one component |
| separation by subsets of `D` is the same in the torso and in the graph | Proposition 2.7 | same lemma, item (c) | the separator is a subset of `D` |
| Courcelle's theorem for graphs with vertex labels | Theorem 2.2 and the paragraph after it | proof of Theorem `thm:fpt` | property expressed in MSO with vertex and vertex-set variables |
| definition of FPT | Section 1, p. 1 | Section "Fixed-Parameter Tractability" | - |

## Difference from our work

Their constrained cut problems put the condition on the separator alone; a cut-path also contains a `u`-`v` path
whose edges outside the cut lie anywhere in the graph, so we add to the torso the lengths of the shortcuts through
the removed components.

## Doubts and open questions

- Numbers are from arXiv v1. Checked 2026-10-10: arXiv has this one version only, and the first author's
  manuscript in journal format (cs.bme.hu/~dmarx/papers/marx-tw-reduction-talg.pdf, dated 2012-10-26) has the same
  numbers for Section 2.1, Theorem 2.2 and the remark on labeled graphs, Definition 2.5, Proposition 2.7,
  Lemma 2.11, Remark 2.13, Theorem 2.15 and Section 3.3. The copy-edited ACM text could not be opened (HTTP 403):
  compare once from a library account. Article number 30 (author's publication list); Crossref has pages 1-35.
- Theorem 2.2 does not say that `f_phi` is computable, and the definition of FPT on p. 1 asks for a computable `f`.
  A source with a computable bound: Cygan et al., *Parameterized Algorithms* (Springer 2015), Theorem 7.11 (read
  2026-10-10 in the authors' free PDF; not in the bibliography). Article 1, Theorem 8.4, does not argue
  computability (proposal in `projects/clanok-1-min-cut-path.submission/literature_review_report.md`, section 6).
- The original source of Courcelle's theorem is not in our bibliography (their [13] is Courcelle's chapter in the
  Handbook of Theoretical Computer Science, vol. B, 1990, not read by us).
- Their Section 3.3 handles a connected vertex separator; an edge version of it is not what we need (the path of a
  cut-path may use edges outside the cut), so our proof does not follow from Theorem 3.7.
