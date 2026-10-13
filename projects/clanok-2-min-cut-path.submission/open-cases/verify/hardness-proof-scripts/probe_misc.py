"""Small probes for the wording issues of theory-hardness.md.

(1) Cor. 2.6 (c) glosses "cp = c + d - 1" as "the union of a minimum cut and a shortest path is a minimum cut-path".
    Example with d = 3: A-side u, p, q, y (u-p-y, u-q-y), B-side x, r, s, v (x-r-v, x-s-v), cut edges ux, yx, yv.
(2) Sensitivity of the construction: M = c0 + 1 instead of c0 + 2 (one filler less), and no sync edges.
Run: python -I probe_misc.py
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from vexact import cp_bruteforce, min_cuts_pq, cut_graph, cut_size
import construct


def part1():
    G = nx.Graph([('u', 'p'), ('p', 'y'), ('u', 'q'), ('q', 'y'), ('x', 'r'), ('r', 'v'), ('x', 's'), ('s', 'v'),
                  ('u', 'x'), ('y', 'x'), ('y', 'v')])
    cp, c, d, mc = cp_bruteforce(G, 'u', 'v')
    P = [('u', 'x'), ('x', 'y'), ('y', 'v')]
    C = {frozenset(e) for e in P}  # delta({u,p,q,y})
    A = {'u', 'p', 'q', 'y'}
    print('(1) edges', sorted(tuple(sorted(e)) for e in G.edges()))
    print(f'    c={c} d={d} cp={cp} c+d-1={c+d-1}; |delta(A)|={cut_size(G, A)}; '
          f'shortest path u x y v inside delta(A); |cut U path| = {len(C)}')


def variant(phi, drop_filler=False, no_sync=False):
    G, u, v, info = construct.build(phi)
    if drop_filler:
        f = info['KA'][-1]
        g = info['KB'][-1]
        G.remove_nodes_from([f, g])
    if no_sync:
        G.remove_edges_from(info['sync'])
    _, cuts = min_cuts_pq(G, u, v)
    ans = any(nx.has_path(cut_graph(G, A), u, v) for A in cuts)
    sat = any(construct.satisfies(phi, t) for t in construct.assignments(phi))
    return len(cuts), ans, sat


def part2():
    for phi in ([[1], [-1]], [[1, 2], [1, -2], [-1, 2], [-1, -2]], [[1, 1, 1], [-1, -1, -1]]):
        for df, ns in ((False, False), (True, False), (False, True)):
            n, ans, sat = variant(phi, df, ns)
            print(f'(2) phi={phi} M=c0+{1 if df else 2} sync={"no" if ns else "yes"}: #mincuts={n} answer={ans} sat={sat}')


if __name__ == '__main__':
    part1()
    part2()
