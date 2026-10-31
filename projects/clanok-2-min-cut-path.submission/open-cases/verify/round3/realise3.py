"""Graph form of a ZZ instance (theory-dc.md Theorem 13(b)) and independent graph checks (agent verify-round3).

G(Pi): vertices Q; for every strict pair a < b: the edge ab if {a, b} in R, otherwise an ear vertex joined to a and b;
for every strict pair a < b an ear (new vertex) joined to u and a if a != u, and one joined to b and v if b != v;
M ear vertices inside every pair of equivalent elements.
Checks on the graph only (no use of ZZ theory): simple, d(u, v), c(u, v) by max flow, DC membership (every pair has
d <= 2 or c <= 2) through the 3-edge-connected components and, as a cross-check, a Gomory-Hu tree; and PIMC
("some minimum u-v cut contains a u-v path") by a depth-first search over simple paths from u in which every prefix
x_0 .. x_k must be separable (even-indexed vertices with u, odd-indexed with v) by a cut of value c(u, v).
Usage: python realise3.py m mp version [gomoryhu]"""
import sys
import time
from collections import deque

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow


def realise(inst, M=1):
    G = nx.Graph()
    q = inst.q
    G.add_nodes_from(range(q))
    nxt = [q]
    Rs = set(inst.R)

    def ear(a, b):
        w = nxt[0]
        nxt[0] += 1
        G.add_edge(a, w)
        G.add_edge(w, b)

    N = 0
    for a in range(q):
        for b in range(q):
            if inst.lt(a, b):
                N += 1
                if (a, b) in Rs:
                    assert not G.has_edge(a, b)
                    G.add_edge(a, b)
                else:
                    ear(a, b)
                if a != inst.u:
                    ear(inst.u, a)
                if b != inst.v:
                    ear(b, inst.v)
    for a in range(q):
        for b in range(a + 1, q):
            if inst.eq(a, b):
                for _ in range(M):
                    ear(a, b)
    return G, N


class Flow:
    """Max flow on an undirected unit-capacity graph with super terminals (scipy, Dinic)."""

    def __init__(self, G):
        self.n = G.number_of_nodes()
        self.nodes = list(G.nodes())
        assert self.nodes == list(range(self.n))
        rows, cols = [], []
        for (a, b) in G.edges():
            rows += [a, b]
            cols += [b, a]
        self.rows = np.array(rows, dtype=np.int32)
        self.cols = np.array(cols, dtype=np.int32)

    def value(self, S, T):
        n = self.n
        s, t = n, n + 1
        big = 10 ** 6
        r = list(self.rows) + [s] * len(S) + list(T)
        c = list(self.cols) + list(S) + [t] * len(T)
        cap = [1] * len(self.rows) + [big] * (len(S) + len(T))
        A = csr_matrix((np.array(cap, dtype=np.int32), (np.array(r, dtype=np.int32), np.array(c, dtype=np.int32))),
                       shape=(n + 2, n + 2))
        A.sum_duplicates()
        return maximum_flow(A, s, t, method='dinic').flow_value


def pimc_search(G, u, v, c, flow, limit=10 ** 7):
    """DFS over simple paths from u; prefix test by max flow. Returns (path or None, number of flow tests)."""
    tests = [0]
    path = [u]
    on = {u}

    def ok(P):
        tests[0] += 1
        ev = [P[i] for i in range(0, len(P), 2)]
        od = [P[i] for i in range(1, len(P), 2)]
        if v not in od:
            od = od + [v]
        if v in ev:
            return False
        return flow.value(ev, od) == c

    def rec():
        if tests[0] > limit:
            raise RuntimeError("limit")
        x = path[-1]
        for y in G[x]:
            if y in on:
                continue
            if y == v and len(path) % 2 == 0:
                continue
            path.append(y)
            if ok(path):
                if y == v:
                    return True
                on.add(y)
                if rec():
                    return True
                on.discard(y)
            path.pop()
        return False

    if rec():
        return list(path), tests[0]
    return None, tests[0]


def dc_check(G, gomoryhu=False):
    """Return (in_DC, #pairs with d >= 3 and c >= 3) via 3-edge-connected components; optional Gomory-Hu cross-check."""
    dist = dict(nx.all_pairs_shortest_path_length(G))
    comps = list(nx.k_edge_components(G, k=3))
    comp_of = {}
    for i, C in enumerate(comps):
        for x in C:
            comp_of[x] = i
    bad = 0
    nodes = list(G.nodes())
    for i, x in enumerate(nodes):
        for y in nodes[i + 1:]:
            if comp_of[x] == comp_of[y] and dist[x].get(y, 10 ** 9) >= 3:
                bad += 1
    gh_bad = None
    if gomoryhu:
        H = G.copy()
        nx.set_edge_attributes(H, 1, 'capacity')
        T = nx.gomory_hu_tree(H)
        # c(x, y) = min edge weight on the tree path
        gh_bad = 0
        mism = 0
        for x in nodes:
            # BFS on the tree computing the minimum weight to every node
            mn = {x: 10 ** 9}
            dq = deque([x])
            while dq:
                a = dq.popleft()
                for b in T[a]:
                    if b not in mn:
                        mn[b] = min(mn[a], T[a][b]['weight'])
                        dq.append(b)
            for y in nodes:
                if y <= x:
                    continue
                cxy = mn[y]
                if (cxy >= 3) != (comp_of[x] == comp_of[y]):
                    mism += 1
                if cxy >= 3 and dist[x].get(y, 10 ** 9) >= 3:
                    gh_bad += 1
        gh_bad = (gh_bad, mism)
    return bad == 0, bad, gh_bad, len(comps)


if __name__ == "__main__":
    from hub3 import hub
    m, mp, ver = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    gh = len(sys.argv) > 4 and sys.argv[4] == 'gomoryhu'
    H = hub(m, mp, ver)
    t0 = time.time()
    G, N = realise(H, M=1)
    simple = not any(a == b for a, b in G.edges())
    print("H(%d,%d) %s: G(Pi) has %d vertices, %d edges, N = %d strict pairs, simple %s, multi-edge-free (nx.Graph)"
          % (m, mp, ver, G.number_of_nodes(), G.number_of_edges(), N, simple), flush=True)
    d = nx.shortest_path_length(G, H.u, H.v)
    fl = Flow(G)
    c = fl.value([H.u], [H.v])
    print("  d(u,v) = %d, c(u,v) = %d" % (d, c), flush=True)
    ok, bad, ghb, ncomp = dc_check(G, gomoryhu=gh)
    print("  DC: %s (pairs at distance >= 3 inside a 3-edge-connected component: %d; components: %d; Gomory-Hu: %s)"
          % (ok, bad, ncomp, ghb), flush=True)
    P, tests = pimc_search(G, H.u, H.v, c, fl)
    print("  PIMC search: %s after %d flow tests (%.0fs)" % ("path " + str(P) if P else "no path", tests,
                                                              time.time() - t0), flush=True)
