"""Generate all graphs on 8 vertices up to isomorphism (own code): extend every 7-vertex graph of the
networkx atlas by a vertex with every neighbourhood, bucket by an invariant, keep one graph per
isomorphism class (VF2 test inside a bucket). Writes graphs8.g6 (graph6, one per line).
Expected count: 12346 (OEIS A000088), connected 11117 (A001349)."""
import sys, time
import networkx as nx
from networkx.generators.atlas import graph_atlas_g

OUT = sys.argv[1] if len(sys.argv) > 1 else "graphs8.g6"
t0 = time.time()
atlas7 = [g for g in graph_atlas_g() if g.number_of_nodes() == 7]
assert len(atlas7) == 1044, len(atlas7)
buckets = {}
reps = []
for g7 in atlas7:
    for S in range(128):
        g = nx.Graph(g7)
        g.add_node(7)
        for i in range(7):
            if (S >> i) & 1:
                g.add_edge(i, 7)
        key = (tuple(sorted(d for _, d in g.degree())),
               nx.weisfeiler_lehman_graph_hash(g, iterations=3))
        lst = buckets.setdefault(key, [])
        if any(nx.is_isomorphic(g, h) for h in lst):
            continue
        lst.append(g)
        reps.append(g)
conn = sum(1 for g in reps if nx.is_connected(g))
with open(OUT, "wb") as f:
    for g in reps:
        f.write(nx.to_graph6_bytes(g, header=False))
print("graphs on 8 vertices:", len(reps), "connected:", conn, "time %.1fs" % (time.time() - t0))
