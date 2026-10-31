"""T3 (r4-hard.md section 6), graph level.  For named formulas: build I (pendants), realise it as a graph by
theory-dc.md Theorem 13(b) (own code), and check independently:
  (1) every non-element vertex has degree 2 (so c <= 2 for every pair containing it);
  (2) every pair of element vertices has distance <= 3 (BFS); d(u, v) = 2;
  (3) c(u, v) = N (own Dinic max-flow);
  (4) minimum cuts = down-sets: for every element y, the residual closure of {u, y} meets the elements exactly in
      {u} + down(y) and misses v; the closure of {u} is {u} plus ear vertices only;
  (5) the cut formula |delta(A)| = N + 2 #(inversions) for random element sets A (ears placed optimally), computed
      directly from the edge list;
  (6) answer: exact search for a u-v walk inside one minimum cut (graphlib.pimc_search, uses only the flow) equals
      satisfiability; for a yes-answer, the found walk is re-checked with a fresh max-flow between its even and
      odd vertices (value c);
  (7) the graph is not in DC: some element pair at distance 3 has c >= 3 (own max-flow).
Usage: python t3_graph.py SEED"""
import random
import sys
import time
from t3lib import from_sat, add_pendants, satisfiable
from graphlib import realise, Flow, Graph, cut_size, pimc_search

FORMULAS = [
    (1, [[1]]),
    (1, [[1], [-1]]),
    (2, [[1, 2]]),
    (2, [[1], [-1, 2]]),
    (2, [[1, 2], [-1], [-2]]),
    (2, [[1, -2], [-1, 2], [1, 2]]),
    (2, [[1, 2], [-1, 2], [1, -2], [-1, -2]]),
    (3, [[1, 2, 3], [-1, -2], [-3]]),
    (3, [[1, -2], [2, -3], [3, -1], [1, 2, 3]]),
    (3, [[1, -2], [2, -3], [3, -1], [-1, -2, -3], [1, 2, 3]]),
]


def flow_sets(G, S, T):
    """Dinic on a capacitated digraph built from G with super terminals (capacities = degrees)."""
    from collections import deque
    nv = G.nv + 2
    s, t = G.nv, G.nv + 1
    head = [[] for _ in range(nv)]
    to, cap = [], []

    def arc(a, b, c1, c2):
        head[a].append(len(to)); to.append(b); cap.append(c1)
        head[b].append(len(to)); to.append(a); cap.append(c2)
    for a, b in G.edges:
        arc(a, b, 1, 1)
    for x in S:
        arc(s, x, len(G.adj[x]) + 1, 0)
    for x in T:
        arc(x, t, len(G.adj[x]) + 1, 0)
    total = 0
    while True:
        level = [-1] * nv
        level[s] = 0
        q = deque([s])
        while q:
            x = q.popleft()
            for e in head[x]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[x] + 1
                    q.append(to[e])
        if level[t] < 0:
            return total
        it = [0] * nv

        def dfs(x, f):
            if x == t:
                return f
            while it[x] < len(head[x]):
                e = head[x][it[x]]
                y = to[e]
                if cap[e] > 0 and level[y] == level[x] + 1:
                    d = dfs(y, min(f, cap[e]))
                    if d:
                        cap[e] -= d
                        cap[e ^ 1] += d
                        return d
                it[x] += 1
            return 0
        while True:
            f = dfs(s, 1 << 30)
            if not f:
                break
            total += f


def main():
    seed = int(sys.argv[1])
    rng = random.Random(seed)
    sys.setrecursionlimit(100000)
    for nv, clauses in FORMULAS:
        t0 = time.time()
        I0 = from_sat(nv, clauses)
        I = add_pendants(I0)
        G, N, ears = realise(I)
        n = I.n
        u, v = I.u, I.v
        out = []
        # (1)
        assert all(len(G.adj[w]) == 2 for w, p, s in ears)
        assert G.nv == n + len(ears)
        # (2)
        maxd = 0
        far = []
        for x in range(n):
            dist = G.bfs(x)
            for y in range(n):
                if y != x:
                    assert dist[y] > 0
                    maxd = max(maxd, dist[y])
                    if dist[y] == 3 and x < y:
                        far.append((x, y))
        duv = G.bfs(u)[v]
        # (3)
        F = Flow(G)
        c = F.maxflow(u, v)
        # (4)
        elmask = (1 << n) - 1
        ok4 = True
        Cu = F.closure([u])
        if Cu & elmask != 1 << u:
            ok4 = False
        for y in range(n):
            if y == v:
                continue
            C = F.closure([u, y])
            want = (1 << u) | I.down[y]
            if (C & elmask) != want or (C >> v) & 1:
                ok4 = False
                out.append("closure mismatch at %s" % I.names[y])
        # (5) random element sets with optimal ears
        ok5 = True
        for _ in range(300):
            A = 1 << u
            for x in range(n):
                if x not in (u, v) and rng.random() < 0.5:
                    A |= 1 << x
            inv = sum(1 for a in range(n) for b in range(n) if I.lt(a, b) and not (A >> a) & 1 and (A >> b) & 1)
            real = sum(1 for a, b in G.edges if a < n and b < n and ((A >> a) & 1) != ((A >> b) & 1))
            earc = sum(1 for w, p, s in ears if ((A >> p) & 1) != ((A >> s) & 1))
            # direct: place ear vertices optimally, count all crossing edges
            Afull = A
            for w, p, s in ears:
                if (A >> p) & 1 and (A >> s) & 1:
                    Afull |= 1 << w
                elif ((A >> p) & 1) != ((A >> s) & 1) and (A >> p) & 1:
                    Afull |= 1 << w
            direct = cut_size(G, Afull)
            if not (direct == real + earc == N + 2 * inv):
                ok5 = False
        # (6)
        ans, states, walk = pimc_search(G, F, u, v, c)
        sat = satisfiable(nv, clauses)
        ok6 = ans == sat
        if ans:
            ev = walk[0::2]
            od = walk[1::2]
            assert all(x < n for x in walk), "walk uses an ear vertex"
            val = flow_sets(G, ev, od)
            ok6 = ok6 and val == c
            out.append("walk " + " ".join(I.names[x] for x in walk) + " (flow even/odd = %d)" % val)
        # (7)
        notdc = None
        rng.shuffle(far)
        for x, y in far[:40]:
            Fx = Flow(G)
            cxy = Fx.maxflow(x, y)
            if cxy >= 3:
                notdc = (I.names[x], I.names[y], cxy)
                break
        print("formula nv=%d %s: |Q|=%d (pendants %d), vertices %d, ears %d, N=%d; max element distance %d, "
              "d(u,v)=%d, c(u,v)=%d, closures ok=%s, cut formula ok=%s, PIMC=%s (states %d), SAT=%s, ok=%s; "
              "non-DC witness %s; %.1fs" % (nv, clauses, n, len(I.pendants), G.nv, len(ears), N, maxd, duv, c, ok4,
                                           ok5, ans, states, sat, ok6, notdc, time.time() - t0))
        for line in out:
            print("   ", line)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
