"""Probe of the Section 5 claim of theory-hardness.md: if c(u,v) <= 3 (in particular in the class
"c(x,y) <= 3 for all pairs"), cp(u,v) = c(u,v) is decided by testing the u-v paths of length 1 and 3:
a path P of odd length lies in a minimum cut iff c_{G-P}(u,v) = c(u,v) - |P| (Lemma 1.3 (c)).

Compared with the exact cp of vexact.cp_bruteforce (enumeration of all vertex sets, no lemma used) on
 (i)  all connected graphs with <= 7 vertices (networkx atlas), all ordered pairs with c(u,v) <= 3;
 (ii) random connected graphs with 9..15 vertices in the class "c(x,y) <= 3 for all pairs" (Gomory-Hu tree),
      all unordered pairs with d(u,v) >= 2.
Run: python -I probe_c3.py
"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import networkx as nx
from vexact import maxflow, cp_bruteforce


def alg_short(G, u, v):
    c, _ = maxflow(G, u, v)
    assert c <= 3
    if G.has_edge(u, v):
        return True
    if c < 3:
        return False  # a path in a minimum cut has odd length <= c, and length 1 is excluded
    for x in G[u]:
        for y in G[v]:
            if x != y and x not in (u, v) and y not in (u, v) and G.has_edge(x, y):
                H = G.copy()
                H.remove_edges_from([(u, x), (x, y), (y, v)])
                c2 = maxflow(H, u, v)[0]
                if c2 == c - 3:
                    return True
    return False


def all_pairs_c_le3(G):
    T = nx.gomory_hu_tree(G)
    return max(d['weight'] for _, _, d in T.edges(data=True)) <= 3


def job_atlas(g):
    out = []
    for u in g:
        for v in g:
            if u == v:
                continue
            c, _ = maxflow(g, u, v)
            if c > 3:
                continue
            cp, cb, d, _ = cp_bruteforce(g, u, v)
            out.append((alg_short(g, u, v) == (cp == cb), d, cp == cb))
    return out


def job_random(seed):
    rnd = random.Random(seed)
    out = []
    tries = 0
    while len(out) < 1 and tries < 200:
        tries += 1
        n = rnd.randint(9, 15)
        p = rnd.uniform(0.18, 0.35)
        G = nx.gnp_random_graph(n, p, seed=rnd.randint(0, 10**9))
        if not nx.is_connected(G):
            continue
        for e in G.edges():
            G.edges[e]['capacity'] = 1
        if not all_pairs_c_le3(G):
            continue
        res = []
        for u, v in itertools.combinations(G.nodes(), 2):
            if G.has_edge(u, v):
                continue
            cp, cb, d, _ = cp_bruteforce(G, u, v)
            res.append((alg_short(G, u, v) == (cp == cb), d, cp == cb, cb))
        out.append((n, G.number_of_edges(), res))
    return out


def main():
    graphs = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 2 and nx.is_connected(g)]
    with Pool(30) as pool:
        r1 = pool.map(job_atlas, graphs, chunksize=8)
        r2 = pool.map(job_random, range(600), chunksize=2)
    flat1 = [x for r in r1 for x in r]
    lines = [f'(i) atlas: ordered pairs with c <= 3: {len(flat1)}, of them cp = c: {sum(x[2] for x in flat1)}, '
             f'with d >= 2 and cp = c: {sum(1 for x in flat1 if x[1] >= 2 and x[2])}, disagreements: {sum(not x[0] for x in flat1)}']
    gs = [g for r in r2 for g in r]
    flat2 = [x for g in gs for x in g[2]]
    lines.append(f'(ii) random graphs in the class c(x,y) <= 3: {len(gs)} graphs (n {min(g[0] for g in gs)}-{max(g[0] for g in gs)}), '
                 f'non-adjacent pairs {len(flat2)}, with cp = c: {sum(x[2] for x in flat2)}, '
                 f'with c = 3 and cp = c: {sum(1 for x in flat2 if x[2] and x[3] == 3)}, disagreements: {sum(not x[0] for x in flat2)}')
    txt = '\n'.join(lines)
    print(txt)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results-probe-c3.txt'), 'w') as fh:
        fh.write(txt + '\n')


if __name__ == '__main__':
    main()
