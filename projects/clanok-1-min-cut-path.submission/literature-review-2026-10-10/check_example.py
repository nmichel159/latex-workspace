"""Brute force on the two graphs of Example 6.3 (Figure 12) of article 1.

For each graph: c(u,v), d(u,v), cp(u,v), all minimum cut-paths, and whether some minimum cut-path
contains a minimum u-v cut / a shortest u-v path.
"""
from itertools import combinations

import networkx as nx


def connected(edges, nodes, a, b):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return nx.has_path(g, a, b)


def analyse(name, edges, u="u", v="v"):
    edges = [tuple(sorted(e)) for e in edges]
    nodes = sorted({x for e in edges for x in e})
    g = nx.Graph(edges)
    d = nx.shortest_path_length(g, u, v)
    eset = set(edges)

    def is_cut(s):
        return not connected(eset - set(s), nodes, u, v)

    def has_path(s):
        return connected(s, nodes, u, v)

    c = min(k for k in range(1, len(edges) + 1) if any(is_cut(s) for s in combinations(edges, k)))
    min_cuts = [set(s) for s in combinations(edges, c) if is_cut(s)]
    shortest = [set(tuple(sorted(p)) for p in zip(path, path[1:])) for path in nx.all_shortest_paths(g, u, v)]
    cp = min(k for k in range(1, len(edges) + 1)
             if any(is_cut(s) and has_path(s) for s in combinations(edges, k)))
    optima = [set(s) for s in combinations(edges, cp) if is_cut(s) and has_path(s)]
    with_min_cut = [s for s in optima if any(mc <= s for mc in min_cuts)]
    with_shortest = [s for s in optima if any(p <= s for p in shortest)]
    print(f"{name}: c = {c}, d = {d}, cp = {cp}, c + d - 1 = {c + d - 1}")
    print(f"  minimum cuts: {len(min_cuts)}, shortest paths: {len(shortest)}, minimum cut-paths: {len(optima)}")
    print(f"  minimum cut-paths that contain a minimum cut: {len(with_min_cut)}")
    print(f"  minimum cut-paths that contain a shortest path: {len(with_shortest)}")
    for s in optima:
        print("   ", sorted(s))


left = [("t", "a"), ("t", "v"), ("u", "s"), ("s", "b"), ("u", "a"), ("a", "b"), ("b", "v")]
right = left + [("a", "v"), ("u", "b")]
analyse("left graph", left)
analyse("right graph", right)
