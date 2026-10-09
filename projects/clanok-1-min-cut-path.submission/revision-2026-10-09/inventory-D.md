# Inventory of fragment D (Sections 6-7, Acknowledgments), before editing

Line numbers refer to `frag-D-6-7.tex` as received (2026-10-09).

| # | Item | Label | Lines (before) | Content |
|---|---|---|---|---|
| 1 | section | `sec:random-graphs` | 1-2 | Erdős–Rényi Graphs |
| 2 | paragraph: model, base of log, dense case cited | - | 4-7 | cites `Bollobas2001` |
| 3 | theorem (Theorem 6.1) | `thm:random-diameter-two` | 9-16 | G(n,1/alpha) has diameter two, limit display; cites `Bollobas2001` |
| 4 | paragraph: dense-case consequence | - | 18-19 | refs `thm:diameter-two`, `rem:algorithm` |
| 5 | paragraph: sparse setting | - | 22-23 | cites `Bollobas2001,Frieze2016` |
| 6 | theorem (Theorem 6.2, Diameter) | `thm:random-diameter` | 26-32 | diam <= log n / log log n, limit display |
| 7 | theorem (Theorem 6.3, Connectivity) | `thm:random-connectivity` | 35-42 | k-edge-connected, k = delta(G); cites `Frieze2016` |
| 8 | lemma (Lemma 6.4, Degree Bounds) | `lem:degree-bounds` | 46-53 | beta_1 log n <= deg <= beta_2 log n |
| 9 | proof of Lemma 6.4 | - | 55-67 | binomial, h(a), Chernoff display (two tails), choice of a_1, a_2, union bound, beta_1 = a_1 alpha/2, beta_2 = 2 a_2 alpha; cites `Frieze2016` |
| 10 | lemma (Lemma 6.5) | `lem:connectivity-bounds` | 70-79 | beta_1 log n <= c(u,v) <= beta_2 log n |
| 11 | proof of Lemma 6.5 | - | 82-100 | three displays: lower chain, upper bound deg(u), combined |
| 12 | paragraph before Theorem 6.6 | - | 104-105 | announcement of the theorem |
| 13 | theorem (Theorem 6.6) | `thm:approximation-scheme` | 107-111 | average (1+eps)-approximation scheme, p >= alpha log n / n |
| 14 | proof of Theorem 6.6 | - | 113-137 | polynomial time (cites `Cormen2022`), Lemma 2.4, monotonicity + coupling, displays d <= diam <= ..., c >= beta_1 log n; c <= cp = OPT; ratio display; limit argument |
| 15 | section | `sec:conclusion` | 139-140 | Conclusion |
| 16 | paragraph: summary of results | - | 142-144 | |
| 17 | open direction 1: further classes; class "diam or cut 2" sentence | - | 146-148 | |
| 18 | open direction 2: planar graphs | - | 150-152 | cites `itai1979maximum,henzinger1997faster` |
| 19 | open direction 3: experiments | - | 154-155 | |
| 20 | open direction 4: fixed cp(u,v) | - | 157 | |
| 21 | section*: Acknowledgments | - | 160-162 | Martin Loebl |

Displays: 12 (lines 13-15, 29-31, 38-40, 50-52, 59-63, 76-78, 85-87, 92-94, 97-99, 120-124, 126-128, 132-134).
Citations: Bollobas2001 (x3), Frieze2016 (x3), Cormen2022, itai1979maximum, henzinger1997faster.
