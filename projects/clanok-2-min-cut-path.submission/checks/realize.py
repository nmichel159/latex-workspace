"""End-to-end check on real graphs of DC: a planted ZZ instance that reaches Shape A or Shape B is realised by a graph G; the instance of def:zz-instance is computed
back from G by one maximum flow (residual reachability, Picard-Queyranne) and compared with the planted one; then the formula of thm:pa-formulas gives D, and a minimum
side A with A cap Q = D yields delta(A), which must be a minimum u-v cut containing a u-v path.

Realisation: the elements of Q are vertices, every edge ab of R is an edge, every other pair x <= y gets an ear x, w, y (w of degree two; both directions for tied
pairs), and ears from u to x and from x to v balance every element and give it at least three edge-disjoint paths to u.  Oriented from lower to upper, the graph
is balanced, so the sets with no entering arc are exactly the minimum sides.  This argument is not used by the check, which recomputes everything from G.

Usage: realize.py SEED COUNT LOG
"""
import os
import random
import sys
import time
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from zz_core import bits, chk  # noqa: E402
from zz_design import BASES, zipper  # noqa: E402
from zz_proof import Cfg, Walk, construct  # noqa: E402
import zz_proof  # noqa: E402


class Flow:
    """Dinic on an undirected unit graph."""

    def __init__(self, n):
        self.n = n
        self.head = [[] for _ in range(n)]
        self.to = []
        self.cap = []

    def add(self, a, b):
        self.head[a].append(len(self.to))
        self.to.append(b)
        self.cap.append(1)
        self.head[b].append(len(self.to))
        self.to.append(a)
        self.cap.append(1)

    def maxflow(self, s, t):
        total = 0
        n = self.n
        while True:
            level = [-1] * n
            level[s] = 0
            dq = deque([s])
            while dq:
                x = dq.popleft()
                for e in self.head[x]:
                    y = self.to[e]
                    if self.cap[e] > 0 and level[y] < 0:
                        level[y] = level[x] + 1
                        dq.append(y)
            if level[t] < 0:
                return total
            it = [0] * n
            # iterative blocking flow, unit capacities
            while True:
                path = []
                x = s
                while x != t:
                    adv = False
                    while it[x] < len(self.head[x]):
                        e = self.head[x][it[x]]
                        y = self.to[e]
                        if self.cap[e] > 0 and level[y] == level[x] + 1:
                            path.append(e)
                            x = y
                            adv = True
                            break
                        it[x] += 1
                    if not adv:
                        if x == s:
                            break
                        level[x] = -1
                        e = path.pop()
                        x = self.to[e ^ 1]
                        it[x] += 1
                if x != t:
                    break
                for e in path:
                    self.cap[e] -= 1
                    self.cap[e ^ 1] += 1
                total += 1

    def reach(self, starts):
        seen = bytearray(self.n)
        st = list(starts)
        for s in st:
            seen[s] = 1
        while st:
            x = st.pop()
            for e in self.head[x]:
                y = self.to[e]
                if self.cap[e] > 0 and not seen[y]:
                    seen[y] = 1
                    st.append(y)
        return seen


def realize(I):
    m = I.m
    edges = set()
    n = [m]
    ins = [0] * m
    outs = [0] * m

    def ear(x, y):
        w = n[0]
        n[0] += 1
        edges.add((x, w))
        edges.add((w, y))
        outs[x] += 1
        ins[y] += 1

    for a, b in I.edges:
        edges.add((a, b))
        outs[a] += 1
        ins[b] += 1
    for x in range(m):
        for y in bits(I.UP[x]):
            if x != y and (x, y) not in I.edges:
                ear(x, y)
    for x in range(m):
        if x not in (I.u, I.v):
            for _ in range(3):
                ear(I.u, x)
                ear(x, I.v)
            d = outs[x] - ins[x]
            for _ in range(max(d, 0)):
                ear(I.u, x)
            for _ in range(max(-d, 0)):
                ear(x, I.v)
    return n[0], edges


def check_instance(I, P, cfg, rng, st, log):
    t0 = time.time()
    I.validate()
    chk(I.p2(), "P2")
    chk(I.shortest_walk(bound=len(P) - 1, budget=200000) is None, "P shortest")
    n, edges = realize(I)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    m = I.m
    # G in DC: elements of Q at distance <= 2, others of degree 2
    nbsets = [set(adj[x]) for x in range(m)]
    for x in range(m):
        for y in range(x + 1, m):
            chk(y in nbsets[x] or nbsets[x] & nbsets[y], "two elements of Q at distance greater than two")
    for x in range(m, n):
        chk(len(adj[x]) == 2, "ear vertex")
    chk(I.v not in nbsets[I.u] and nbsets[I.u] & nbsets[I.v], "d(u, v) = 2")
    F = Flow(n)
    for a, b in edges:
        F.add(a, b)
    c = F.maxflow(I.u, I.v)
    chk(c >= 3, "c(u, v) >= 3")
    # the set Q: three edge-disjoint paths to u, for the vertices of degree at least three
    for x in range(m):
        if x != I.u:
            G3 = Flow(n)
            # only the vertices near u and x are relevant, a full search is fast enough for three augmentations
            G3.head = F.head
            G3.to = F.to
            G3.cap = [1] * len(F.cap)
            for _ in range(3):
                par = {x: None}
                dq = deque([x])
                while dq and I.u not in par:
                    z = dq.popleft()
                    for e in G3.head[z]:
                        y = G3.to[e]
                        if G3.cap[e] > 0 and y not in par:
                            par[y] = e
                            dq.append(y)
                chk(I.u in par, "c(u, x) >= 3 for x in Q")
                z = I.u
                while par[z] is not None:
                    e = par[z]
                    G3.cap[e] -= 1
                    G3.cap[e ^ 1] += 1
                    z = G3.to[e ^ 1]
    # the preorder by residual reachability: y in a minimum side forces every vertex reachable from y
    base = F.reach([I.u])
    chk(not base[I.v], "maximum flow")
    for y in range(m):
        rc = F.reach([y])
        for x in range(m):
            leq = bool(base[x] or rc[x] or rc[I.v])
            chk(leq == I.leq(x, y), "the preorder of G differs from the planted preorder")
    # R
    R2 = set()
    for a, b in edges:
        if a < m and b < m and not I.tied(a, b):
            R2.add((a, b) if I.lt(a, b) else (b, a))
    chk(R2 == set(I.edges), "R of G differs from the planted R")
    st["instances realised"] += 1
    st["max n"] = max(st["max n"], n)
    st["max c"] = max(st["max c"], c)
    # the formula, the side, the cut
    stc = Counter()
    captured = []
    orig_final = zz_proof.final

    def final2(w, D, label, s):
        orig_final(w, D, label, s)
        captured.append((D, label))

    zz_proof.final = final2
    try:
        construct(Walk(I, P), cfg, rng, stc)
    finally:
        zz_proof.final = orig_final
    for D, label in captured:
        st["D: " + label] += 1
        Qin = [x for x in bits(D)]
        Qout = [x for x in range(m) if not D >> x & 1]
        S = F.reach(Qin)
        for x in Qout:
            chk(not S[x], "no minimum side with this trace")
        size = 0
        cutadj = {}
        for a, b in edges:
            if S[a] != S[b]:
                size += 1
                cutadj.setdefault(a, []).append(b)
                cutadj.setdefault(b, []).append(a)
        chk(size == c, "delta(A) is not a minimum cut")
        seen = {I.u}
        stack = [I.u]
        while stack:
            z = stack.pop()
            for y in cutadj.get(z, []):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        chk(I.v in seen, "delta(A) contains no u-v path")
        st["minimum cut-paths verified: " + label] += 1
    print("m", m, "n", n, "c", c, "q", len(P) - 1, "exits", [x[1] for x in captured], "time", round(time.time() - t0, 1), file=log, flush=True)


def main():
    seed, count, logf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    st = Counter()
    cfg = Cfg()
    with open(logf, "w", encoding="utf-8") as log:
        for k in range(count):
            kind = k % 6
            if kind == 0:
                d = zipper(rng.randint(13, 16), rng.randint(14, 18), naux=5, buf=1, end=1)     # Shape B
            elif kind == 1:
                p, q = rng.randint(13, 16), rng.randint(11, 14)
                keep = set(rng.sample(range(q), 5))
                d = zipper(p, q, naux=5, buf=1, end=1, seed_strict=lambda i, j: j not in keep)   # Shape A
            else:
                d = BASES[["stair", "ties", "mix", "cross"][kind - 2]](rng)
            I, P = d.build()
            check_instance(I, P, cfg, rng, st, log)
        for key in sorted(st):
            print(key, st[key], file=log)
        print("FAILURES: none (a failure stops the run with an exception)", file=log)


if __name__ == "__main__":
    main()
