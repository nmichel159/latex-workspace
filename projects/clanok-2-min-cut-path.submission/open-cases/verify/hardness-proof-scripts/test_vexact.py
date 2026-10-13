"""Self-test of vexact.py on all graphs of the networkx atlas (<= 7 vertices), all ordered pairs:
- maxflow value = networkx edge connectivity
- min_cuts_pq = brute-force set of minimum cuts
- cp_bruteforce vs a second brute force: min over u-v paths P of |P| + c_{G-P}(u,v) (all simple paths)
Run: python -I test_vexact.py
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from networkx.algorithms.connectivity import local_edge_connectivity
from vexact import maxflow, min_cuts_pq, cp_bruteforce


def cp_by_paths(G, s, t):
    best = None
    for p in nx.all_simple_paths(G, s, t):
        H = G.copy()
        H.remove_edges_from(zip(p, p[1:]))
        cval = 0 if not nx.has_path(H, s, t) else local_edge_connectivity(H, s, t)
        val = len(p) - 1 + cval
        if best is None or val < best:
            best = val
    return best


def main():
    t0 = time.time()
    graphs = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 2 and nx.is_connected(g)]
    pairs = fails = 0
    for g in graphs:
        n = g.number_of_nodes()
        for s in g:
            for t in g:
                if s == t:
                    continue
                pairs += 1
                val, _ = maxflow(g, s, t)
                c_nx = local_edge_connectivity(g, s, t)
                cpb, c, d, mc = cp_bruteforce(g, s, t)
                _, pq = min_cuts_pq(g, s, t)
                ok = (val == c_nx == c) and set(pq) == set(mc) and len(pq) == len(set(pq))
                if n <= 6:
                    ok = ok and cpb == cp_by_paths(g, s, t)
                if not ok:
                    fails += 1
                    if fails < 5:
                        print('FAIL', list(g.edges()), s, t, val, c_nx, c, cpb)
    print(f'graphs {len(graphs)}, ordered pairs {pairs}, failures {fails}, {time.time()-t0:.0f} s')


if __name__ == '__main__':
    main()
