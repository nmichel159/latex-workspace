"""Task B1: graph level.  For small graphs G in DC and pairs (u, v) with d(u, v) = 2, c(u, v) >= 3 the ZZ instance is built exactly as in
def:zz-instance by enumerating the minimum sides.  Asserts lem:zz-sides, lem:zz-q, lem:zz-instance, the theorem thm:zz-reduction (answer,
returned cut, flow characterisation of <=), the agreement of "cp = c" (brute force over minimum cuts and, independently, over all cuts and
paths) with "a valid walk exists" (brute force); then runs the construction of thm:pa-formulas on the instance.

Usage: graph_level.py MODE SEED SECONDS LOG        MODE: atlas (all connected graphs up to 7 vertices), g8 (file of 8-vertex graphs),
random (families with bridges, pendant parts, degree-2 ears, n <= 13).
"""
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zz_core import ClaimFail, Inst, bits, chk  # noqa: E402
from zz_proof import Cfg, Walk, construct  # noqa: E402


class G:
    def __init__(self, n, edges):
        self.n = n
        self.edges = sorted({(min(a, b), max(a, b)) for a, b in edges})
        self.nb = [0] * n
        for a, b in self.edges:
            self.nb[a] |= 1 << b
            self.nb[b] |= 1 << a

    def connected(self):
        seen = 1
        st = [0]
        while st:
            x = st.pop()
            new = self.nb[x] & ~seen
            seen |= new
            st.extend(bits(new))
        return seen == (1 << self.n) - 1

    def dist(self, s):
        d = [None] * self.n
        d[s] = 0
        cur = [s]
        k = 0
        seen = 1 << s
        while cur:
            k += 1
            nxt = []
            for x in cur:
                new = self.nb[x] & ~seen
                seen |= new
                for y in bits(new):
                    d[y] = k
                    nxt.append(y)
            cur = nxt
        return d

    def delta(self, A):
        """number of edges with exactly one end in A"""
        r = 0
        for x in bits(A):
            r += bin(self.nb[x] & ~A).count("1")
        return r

    def delta_edges(self, A):
        return [(a, b) for a, b in self.edges if (A >> a & 1) != (A >> b & 1)]

    def cvalue(self, s, t):
        """Min cut by Ford-Fulkerson on unit capacities."""
        cap = {}
        for a, b in self.edges:
            cap[(a, b)] = 1
            cap[(b, a)] = 1
        flow = 0
        while True:
            par = {s: None}
            st = [s]
            while st and t not in par:
                x = st.pop()
                for y in bits(self.nb[x]):
                    if y not in par and cap[(x, y)] > 0:
                        par[y] = x
                        st.append(y)
            if t not in par:
                return flow
            y = t
            while par[y] is not None:
                x = par[y]
                cap[(x, y)] -= 1
                cap[(y, x)] += 1
                y = x
            flow += 1

    def all_c(self):
        n = self.n
        c = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                c[i][j] = c[j][i] = self.cvalue(i, j)
        return c

    def in_DC(self, c, dd):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if dd[i][j] > 2 and c[i][j] > 2:
                    return False
        return True


def paths_in(edges, s, t):
    """All s-t paths of the edge set, as vertex lists."""
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    out = []
    path = [s]
    seen = {s}

    def rec(x):
        if x == t:
            out.append(list(path))
            return
        for y in adj.get(x, []):
            if y not in seen:
                seen.add(y)
                path.append(y)
                rec(y)
                path.pop()
                seen.discard(y)

    rec(s)
    return out


def has_path(edges, s, t):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen = {s}
    st = [s]
    while st:
        x = st.pop()
        if x == t:
            return True
        for y in adj.get(x, []):
            if y not in seen:
                seen.add(y)
                st.append(y)
    return False


def cp_bruteforce(g, u, v):
    """cp(u, v) over all cuts delta(A) and all u-v paths: |delta(A) union pi|.  Every u-v cut contains some delta(A)."""
    allp = paths_in(g.edges, u, v)
    psets = [frozenset((min(p[i], p[i + 1]), max(p[i], p[i + 1])) for i in range(len(p) - 1)) for p in allp]
    best = 10 ** 9
    uu, vv = 1 << u, 1 << v
    for A in range(1 << g.n):
        if A & uu and not A & vv:
            d = frozenset(g.delta_edges(A))
            if len(d) >= best + 1:
                continue
            for s in psets:
                x = len(d | s)
                if x < best:
                    best = x
    return best


def run_pair(g, c_all, dd, u, v, st, rng, deep=True):
    """All checks for the instance (g, u, v) of the open case."""
    n = g.n
    c = c_all[u][v]
    V = (1 << n) - 1
    uu, vv = 1 << u, 1 << v
    rest = V & ~uu & ~vv
    # all sides
    minsides = []
    x = rest
    subs = [0]
    for b in bits(rest):
        subs += [s | 1 << b for s in subs]
    for s in subs:
        A = s | uu
        if g.delta(A) == c:
            minsides.append(A)
    chk(minsides, "a minimum side exists")
    st["pairs"] += 1
    # lem:zz-sides(a)
    msset = set(minsides)
    for A in minsides[:60]:
        for B in minsides[:60]:
            chk((A & B) in msset and (A | B) in msset, "lem:zz-sides(a): A cap B, A cup B minimum sides")
            for a, b in g.edges:
                x1, x2 = 1 << a, 1 << b
                if (x1 & A & ~B and x2 & B & ~A) or (x2 & A & ~B and x1 & B & ~A):
                    raise ClaimFail("lem:zz-sides(a): edge between A - B and B - A")
    # lem:zz-sides(b): all sets Y with at most two boundary edges
    Ys = [s for s in subs if s and g.delta(s) <= 2]
    st["Y sets"] += len(Ys)
    for Y in Ys:
        for A in minsides[:40]:
            k = sum(1 for a, b in g.delta_edges(A) if (Y >> a & 1) or (Y >> b & 1))
            chk(k <= 1, "lem:zz-sides(b): k <= 1")
            if k == 1:
                st["sides(b) k = 1"] += 1
                chk(g.delta(A & ~Y) == c and g.delta(A | Y) == c, "lem:zz-sides(b): A - Y and A + Y are minimum sides")
    # Q
    Q = [u] + [x for x in range(n) if x != u and c_all[u][x] >= 3]
    Qm = sum(1 << x for x in Q)
    chk(Qm >> v & 1, "v in Q")
    st["outside Q vertices"] += n - len(Q)
    if len(Q) < n:
        st["pairs with vertices outside Q"] += 1
    # lem:zz-q
    for x in range(n):
        if x not in Q:
            chk(any(Y >> x & 1 and Y & Qm == 0 and g.delta(Y) <= 2 for Y in Ys), "lem:zz-q(a)")
    for i, x in enumerate(Q):
        for y in Q[i + 1:]:
            chk(c_all[x][y] >= 3 and dd[x][y] <= 2, "lem:zz-q(b)")
    # lem:zz-q(c), and the answer by brute force over minimum cuts
    ans_min = False
    for A in minsides:
        de = g.delta_edges(A)
        if has_path(de, u, v):
            ans_min = True
            for p in paths_in(de, u, v):
                chk(all(Qm >> y & 1 for y in p), "lem:zz-q(c): a vertex outside Q on the path")
            st["min sides with a path"] += 1
    # def:zz-instance
    idx = {x: i for i, x in enumerate(Q)}
    m = len(Q)
    up = [0] * m
    for x in Q:
        for y in Q:
            ok = all((A >> x & 1) or not (A >> y & 1) for A in minsides)
            if ok:
                up[idx[x]] |= 1 << idx[y]
    # flow characterisation of <= in the proof of thm:zz-reduction (brute force minimum)
    for x in Q:
        for y in Q:
            if x == y or x == u or y == v:
                chk(up[idx[x]] >> idx[y] & 1, "x <= y for x = u or y = v")
                continue
            best = 10 ** 9
            for s in subs:
                A = s | uu
                if A >> y & 1 and not A >> x & 1:
                    best = min(best, g.delta(A))
            chk((best > c) == bool(up[idx[x]] >> idx[y] & 1), "the flow test of <=")
    # R
    tie = lambda x, y: bool(up[idx[x]] >> idx[y] & 1 and up[idx[y]] >> idx[x] & 1)
    leq = lambda x, y: bool(up[idx[x]] >> idx[y] & 1)
    edges = []
    for a, b in g.edges:
        if Qm >> a & 1 and Qm >> b & 1 and not tie(a, b):
            if leq(a, b):
                edges.append((idx[a], idx[b]))
            elif leq(b, a):
                edges.append((idx[b], idx[a]))
            else:
                raise ClaimFail("lem:zz-instance(a): adjacent incomparable elements")
    # lem:zz-instance(a)
    I = Inst(m, up, edges, idx[u], idx[v], [str(x) for x in Q])
    I.validate()
    # lem:zz-instance(b)
    trace = {sum(1 << idx[x] for x in Q if A >> x & 1) for A in minsides}
    dsets = I.downsets()
    chk(trace == dsets, "lem:zz-instance(b): A cap Q are exactly the down-sets with u and not v")
    st["down-sets"] += len(dsets)
    # lem:zz-instance(c), with the common neighbours
    chk(I.p2(), "lem:zz-instance(c): P2")
    for i, x in enumerate(Q):
        for y in Q[i + 1:]:
            cn = g.nb[x] & g.nb[y]
            out = cn & ~Qm
            if I.inc(idx[x], idx[y]):
                st["incomparable pairs"] += 1
                chk(not g.nb[x] >> y & 1, "incomparable adjacent")
                chk(cn != 0, "common neighbour")
                chk(out == 0, "lem:zz-instance(c): common neighbour outside Q for an incomparable pair")
            elif out:
                st["comparable pairs with a common neighbour outside Q"] += 1
    # the two answers
    yes = any(I.connected_in_GD(D) for D in dsets)
    chk(yes == ans_min, "thm:zz-reduction: yes-instance iff some minimum cut contains a path")
    w = I.shortest_walk()
    chk((w is not None) == yes, "lem:zz-valid(c): valid walk iff yes-instance")
    # cross-check of the solver against the down-sets
    dmin = None
    for D in dsets:
        k = I.dist_in_GD(D)
        if k is not None and (dmin is None or k < dmin):
            dmin = k
    if yes:
        chk(len(w) - 1 == dmin, "solver against down-sets")
    # returned cut: for each connecting D, the least boundary between D and Q - D
    for D in dsets:
        if I.connected_in_GD(D):
            must = sum(1 << Q[i] for i in bits(D))
            forb = Qm & ~must
            best, bestS = 10 ** 9, None
            for s in subs:
                A = s | uu
                if A & must == must and A & forb == 0:
                    z = g.delta(A)
                    if z < best:
                        best, bestS = z, A
            chk(best == c, "thm:zz-reduction: least boundary is c")
            chk(has_path(g.delta_edges(bestS), u, v), "thm:zz-reduction: delta(A) contains a path")
            st["returned cuts checked"] += 1
    # cp itself
    if deep:
        cpv = cp_bruteforce(g, u, v)
        chk(cpv in (c, c + 1), "prop:easy-pairs(iv)")
        chk((cpv == c) == yes, "cp = c iff yes-instance")
        st["cp brute force"] += 1
    # the construction
    if yes:
        st["yes pairs"] += 1
        cfg = Cfg()
        wl = Walk(I, w)
        construct(wl, cfg, rng, st)
        construct(Walk(I, w[::-1]), cfg, rng, st)
        J = I.reversed_instance()
        J.validate()
        chk(J.p2(), "reversed instance: P2")
        construct(Walk(J, w), cfg, rng, st)
        construct(Walk(J, w[::-1]), cfg, rng, st)
    else:
        st["no pairs"] += 1


def run_graph(g, st, rng, deep=True):
    if not g.connected():
        return 0
    c_all = g.all_c()
    dd = [g.dist(i) for i in range(g.n)]
    if not g.in_DC(c_all, dd):
        st["graphs not in DC"] += 1
        return 0
    st["graphs in DC"] += 1
    k = 0
    for u in range(g.n):
        for v in range(g.n):
            if u != v and dd[u][v] == 2 and c_all[u][v] >= 3:
                run_pair(g, c_all, dd, u, v, st, rng, deep)
                k += 1
    if k:
        st["graphs with an open pair"] += 1
    return k


# ---------------------------------------------------------------- families
def rand_core(rng, n):
    """A connected graph of small diameter on n vertices."""
    p = rng.uniform(0.25, 0.8)
    while True:
        e = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        g = G(n, e)
        if g.connected():
            return e


def planted_core(rng, n):
    """A partition A, B of the core with a planted crossing path: the crossing edges form few, the rest is dense."""
    k = rng.randint(2, n - 2)
    A = list(range(k))
    B = list(range(k, n))
    e = []
    for S in (A, B):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if rng.random() < 0.85:
                    e.append((S[i], S[j]))
    # crossing edges: zigzag
    a0 = 0
    b0 = n - 1
    seq = [a0]
    side = 1
    used = {a0, b0}
    for _ in range(rng.choice([1, 2, 3])):
        pool = [x for x in (B if side else A) if x not in used]
        if not pool:
            break
        y = rng.choice(pool)
        used.add(y)
        seq.append(y)
        side = 1 - side
    if side == 1:
        seq.append(b0)
    else:
        pool = [x for x in A if x not in used]
        if pool:
            y = rng.choice(pool)
            seq += [y, b0]
    e += [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    for _ in range(rng.randint(0, 3)):
        e.append((rng.choice(A), rng.choice(B)))
    return e


def add_parts(rng, n, e, budget):
    """Bridges, pendant trees, degree-2 ears, short cycles attached at one vertex."""
    e = list(e)
    while n < budget:
        kind = rng.choice(["ear", "ear", "ear", "ear2", "pend", "cyc", "bridge"])
        x, y = rng.randrange(n), rng.randrange(n)
        if kind == "ear" and x != y:
            e += [(x, n), (n, y)]
            n += 1
        elif kind == "ear2" and x != y and n + 2 <= budget:
            e += [(x, n), (n, n + 1), (n + 1, y)]
            n += 2
        elif kind == "pend":
            e.append((x, n))
            n += 1
        elif kind == "cyc" and n + 2 <= budget:
            e += [(x, n), (n, n + 1), (n + 1, x)]
            n += 2
        elif kind == "bridge" and n + 2 <= budget:
            e += [(x, n), (n, n + 1)]
            n += 2
        else:
            if rng.random() < 0.3:
                break
    return n, e


def random_graph(rng):
    kind = rng.choice(["core", "planted", "planted", "ears", "ears"])
    nmax = rng.choice([8, 9, 10, 11, 12, 13])
    if kind == "core":
        n = rng.randint(5, min(nmax, 10))
        return G(n, rand_core(rng, n))
    n0 = rng.randint(4, min(nmax - 1, 9))
    e = planted_core(rng, n0) if kind in ("planted", "ears") and rng.random() < 0.7 else rand_core(rng, n0)
    n, e = add_parts(rng, n0, e, nmax)
    return G(n, e)


def from_g6(line):
    data = [ord(c) - 63 for c in line]
    n = data[0]
    bitsl = []
    for d in data[1:]:
        for i in range(5, -1, -1):
            bitsl.append(d >> i & 1)
    e = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bitsl[k]:
                e.append((i, j))
            k += 1
    return G(n, e)


def main():
    mode, seed, secs, logf = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    fails = []
    done = 0

    def one(g, deep=True):
        nonlocal done
        try:
            run_graph(g, st, rng, deep)
        except ClaimFail as ex:
            fails.append((g.n, g.edges, str(ex)))
        done += 1

    if mode == "atlas":
        from networkx.generators.atlas import graph_atlas_g
        for H in graph_atlas_g():
            if H.number_of_nodes() >= 3 and H.number_of_edges() >= 3:
                one(G(H.number_of_nodes(), list(H.edges())))
            if time.time() - t0 > secs:
                st["time limit reached"] += 1
                break
    elif mode == "g8":
        path = sys.argv[5]
        with open(path) as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        k = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        i0 = int(sys.argv[7]) if len(sys.argv) > 7 else 0
        for ln in lines[i0::k]:
            one(from_g6(ln), deep=False)
            if time.time() - t0 > secs:
                st["time limit reached"] += 1
                break
    else:
        while time.time() - t0 < secs:
            one(random_graph(rng), deep=rng.random() < 0.2)
    with open(logf, "w", encoding="utf-8") as lg:
        print("mode", mode, "seed", seed, "graphs", done, "time", round(time.time() - t0, 1), file=lg)
        for k in sorted(st):
            print(k, st[k], file=lg)
        print("FAILURES:", fails[:5] if fails else "none", file=lg)


if __name__ == "__main__":
    main()
