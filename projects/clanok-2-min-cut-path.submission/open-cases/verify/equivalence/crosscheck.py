"""After the own implementation was finished: cross-check of its primitives against the shared library
checks/mcp.py (imported read-only): cp (own 0-1-BFS formula vs mcp.cp_brute), DC membership, and
PIMC (own) vs "cp == c" (mcp). All connected graphs with <= 7 vertices, all pairs; random DC graphs 9..12.
Usage: python crosscheck.py SEED COUNT"""
import sys, os, random
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "checks"))
import mcp  # noqa: E402
import networkx as nx  # noqa: E402
from networkx.generators.atlas import graph_atlas_g  # noqa: E402
from eqcore import Small, adj_masks, all_dist, cp_brute, pimc_from_cuts, in_class_small  # noqa: E402
from randgraphs import gen_core_ears, gen_planted  # noqa: E402


def compare(n, edges, st, bad):
    g = mcp.Gr(n, edges)
    adj = adj_masks(n, edges)
    sm = Small(n, [(a, b, 1) for a, b in edges])
    dist = all_dist(adj)
    if in_class_small(sm, dist, n, 2) != mcp.in_dc(g)[0]:
        bad.append(("DC differs", n, edges))
    for u in range(n):
        for v in range(u + 1, n):
            c, cuts = sm.min_cuts(u, v)
            mine = cp_brute(sm, adj, u, v)
            theirs = mcp.cp_brute(g, u, v)[0]
            if mine != theirs:
                bad.append(("cp differs", n, edges, u, v, mine, theirs))
            ans, _ = pimc_from_cuts(adj, cuts, u, v)
            if ans != (theirs == c):
                bad.append(("PIMC vs cp == c", n, edges, u, v))
            st["pairs"] += 1


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    st, bad = Counter(), []
    for g in graph_atlas_g():
        n = g.number_of_nodes()
        if 2 <= n <= 7 and nx.is_connected(g):
            compare(n, sorted((min(a, b), max(a, b)) for a, b in g.edges()), st, bad)
            st["atlas graphs"] += 1
    rng = random.Random(seed)
    k = 0
    while k < count:
        g = gen_core_ears(rng, 2, 9, 12) if rng.random() < 0.5 else gen_planted(rng, 2, 9, 12)
        if g is None or not nx.is_connected(nx.Graph(g[1])) or nx.Graph(g[1]).number_of_nodes() != g[0]:
            continue
        compare(g[0], g[1], st, bad)
        k += 1
        st["random graphs"] += 1
    print(dict(st))
    print("disagreements:", len(bad))
    for x in bad[:10]:
        print("  ", x)
