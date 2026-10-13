"""E2: search all connected graphs with <= 7 vertices (networkx atlas) for a pair u, v with d(u,v) >= 3,
cp(u,v) < c + d - 1, and a minimum cut C and a shortest path P with |C + P| = cp (so "some union of a minimum
cut and a shortest path is a minimum cut-path" holds while cp != c + d - 1).
Run: python -I probe_e2_min.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from vexact import cp_bruteforce


def main():
    npairs = 0
    found = []
    for g in nx.graph_atlas_g():
        if g.number_of_nodes() < 2 or not nx.is_connected(g):
            continue
        for u in g:
            for v in g:
                if u >= v or nx.shortest_path_length(g, u, v) < 3:
                    continue
                d = nx.shortest_path_length(g, u, v)
                cp, c, _, mc = cp_bruteforce(g, u, v)
                if cp >= c + d - 1:
                    continue
                npairs += 1
                for A in mc:
                    C = {frozenset(e) for e in g.edges() if (e[0] in A) != (e[1] in A)}
                    for p in nx.all_shortest_paths(g, u, v):
                        if len(C | {frozenset(e) for e in zip(p, p[1:])}) == cp:
                            found.append((sorted(g.edges()), u, v))
    txt = (f'graphs <= 7 vertices: pairs with d >= 3 and cp < c + d - 1: {npairs}; '
           f'of them with a minimum cut + shortest path of size cp: {len(found)}')
    print(txt)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results-probe-e2-min.txt'), 'w') as fh:
        fh.write(txt + '\n')


if __name__ == '__main__':
    main()
