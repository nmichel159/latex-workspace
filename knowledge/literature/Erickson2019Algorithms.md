# Erickson2019Algorithms

| | |
|---|---|
| Paper | Erickson: *Algorithms*. 1st paperback edition, 2019. ISBN 978-1-792-64483-2. <https://jeffe.cs.illinois.edu/teaching/algorithms/> (free electronic edition, CC BY 4.0) |
| Key | `Erickson2019Algorithms` |
| Reading status | parts, read 2026-10-12 in the chapter PDFs of the book's page: copyright page; Sections 6.5, 6.6; Section 8.4; Sections 10.3, 10.4 (beginning). Page and section numbers were read from rendered pages (the text layer garbles the numerals) |
| Full text | - (open access at the author's page) |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md); article 2, Section 5 (standard algorithms) |

## What the paper does

A textbook of algorithms. Statements used:

- Section 6.5: strong components of a directed graph are the classes of mutual reachability. Section 6.6, "Strong Components in Linear Time", p. 240: the algorithm of Kosaraju and Sharir labels the strong components in `O(V + E)` time; Tarjan's algorithm follows on the next page.
- Section 8.4, "Unweighted Graphs: Breadth-First Search", p. 281: breadth-first search runs in `O(V + E)` time; Theorem 8.2: when it ends, `dist(v)` is the length of a shortest path from `s` to `v`.
- Section 10.3, p. 331, "The Maxflow-Mincut Theorem": in every flow network the value of a maximum `(s,t)`-flow equals the capacity of a minimum `(s,t)`-cut.
- Section 10.4, "Ford and Fulkerson's augmenting-path algorithm", p. 334: Integrality Theorem; with integer capacities the algorithm halts after at most `|f*|` iterations, each augmenting path is found by a search of the residual graph in `O(E)` time, so the running time is `O(E |f*|)`.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| `V`, `E` also for the numbers of vertices and edges | `\|V\|`, `\|E\|` | |
| flow network: directed graph with capacities, reduced (at most one edge between two vertices) | undirected graph, every edge of capacity one | an undirected edge is two opposite arcs; the reduction of p. 331 subdivides one of them |
| strong component | strongly connected component | |
| `O(E)` for one search of the residual graph | `O(\|V\| + \|E\|)` | the book writes `O(E)`; a graph with isolated vertices needs `O(\|V\| + \|E\|)`, which is what the article states |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| two augmentations give a flow of value two in linear time | Section 10.4, p. 334 | article 2, S11 (the paths `p_1`, `p_2`) | integer capacities; `\|f*\| = 2` |
| max-flow min-cut theorem | Section 10.3, p. 331 | article 2, S11, if a citation is wanted beside Menger's theorem | |
| distances from one vertex by breadth-first search | Section 8.4, p. 281, Theorem 8.2 | article 2, S8, S11 (`λ^-`, `λ^+`) | unweighted, also for directed graphs |
| strong components in linear time | Section 6.6, p. 240 | article 2, S11 (computation of `F`), beside `Tarjan1972DFS` | |

## Difference from our work

Textbook source for standard algorithms; no relation to the problem.

## Doubts and open questions

- The book is self-published: the copyright page names no publisher, so the canonical entry is a `@misc` with the url. Algorithmica's guide has an example type "Online document"; whether the journal accepts the book in this form is open. `Cormen2022` is the alternative, but the section numbers of its 4th edition were not seen first-hand.
- The book has no statement on the structure of all minimum cuts.
