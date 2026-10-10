# ChungLu2001

| | |
|---|---|
| Paper | Chung, Lu: *The Diameter of Sparse Random Graphs*. Advances in Applied Mathematics 26(4), 2001, 257-279. DOI 10.1006/aama.2001.0720 |
| Key | `ChungLu2001` |
| Reading status | parts read 2026-10-09 in the authors' PDF (fanchung.ucsd.edu/dia.pdf, 22 pages): abstract, Section 1 with the table of ranges, statements of Theorems 1-6 (Section 4, p. 15), proof of Theorem 4. Journal version not reachable (ScienceDirect refused the request) |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 5b |

## What the paper does

- Diameter of G(n, p) for np > 1 up to np of order log n; for a disconnected graph the diameter is that of its largest component.
- Theorem 4: if p >= c log n / n for a constant c, then almost surely ceil(log(cn/11)/log(np)) <= diam(G(n,p)) <= ceil(log((33c^2/400) n log n)/log(np)) + 2 floor(1/c) + 2.
- Theorem 5: if log n > np -> infinity, then almost surely diam = (1 + o(1)) log n / log(np). Theorems 2, 3: concentration on two values for c > 8, three for c > 2.
- "Almost surely" means with probability tending to one (definitions from Bollobas's book, Section 1).

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| diam G(n, p) <= log n / log log n w.h.p. for p = alpha log n / n | Theorem 4 with c = alpha > 1 | article 1, Section 7 (Theorem 7.2) | alpha > 1 constant, so floor(1/alpha) = 0 |

Derivation for the article: with c = alpha > 1 the upper bound is at most (log n + log log n + O(1))/(log log n + log alpha) + 3 = log n/(log log n + log alpha) + O(1). Since log alpha > 0, log n/log log n - log n/(log log n + log alpha) tends to infinity, so diam <= log n/log log n for all large n.

## Difference from our work

Used as a tool only.

## Doubts and open questions

- The theorem number is from the authors' PDF; compare with the journal version before writing `\cite[Theorem~4]{ChungLu2001}`.
