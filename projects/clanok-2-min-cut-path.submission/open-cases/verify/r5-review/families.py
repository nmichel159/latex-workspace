"""Own builders (reviewer r5-verify) of the families X_L (r4-general.md §4) and Y_k, Y'_k (§6) in the general switch
form, written from the text, and checks of Proposition X (i), (ii), Theorem Y (i), Proposition Y' (P2, uniqueness),
plus the behaviour of the own forced-exit propagation and the hypothesis of Theorem R on them.
Usage: python families.py LMAX KMAX"""
import sys
from gswlib import SW


class Builder:
    def __init__(self):
        self.nodes = {}
        self.sw = []          # names
        self.E = {}
        self.F = {}
        self.less = []        # (a, b): switch a < switch b

    def node(self, name):
        return self.nodes.setdefault(name, len(self.nodes))

    def switch(self, name):
        self.sw.append(name)
        self.E[name] = set()
        self.F[name] = set()
        return name

    def put(self, name, ty, nodename):
        (self.E if ty == "E" else self.F)[name].add(self.node(nodename))

    def build(self, s="s", t="t"):
        self.node(s)
        self.node(t)
        idx = {nm: i for i, nm in enumerate(self.sw)}
        m = len(self.sw)
        le = [[i == j for j in range(m)] for i in range(m)]
        for a, b in self.less:
            le[idx[a]][idx[b]] = True
        for k in range(m):
            for i in range(m):
                if le[i][k]:
                    for j in range(m):
                        if le[k][j]:
                            le[i][j] = True
        E = [sum(1 << x for x in self.E[nm]) for nm in self.sw]
        F = [sum(1 << x for x in self.F[nm]) for nm in self.sw]
        G = SW(len(self.nodes), E, F, le, self.nodes[s], self.nodes[t])
        G.names = list(self.sw)
        G.idx = idx
        return G


def other(ty):
    return "F" if ty == "E" else "E"


def xfam(L):
    b = Builder()
    path = {k: ("E" if k % 2 == 1 else "F") for k in range(1, L + 1)}
    for k in range(1, L + 1):
        b.switch("x%d" % k)
    def h(k, nd):
        b.put("x%d" % k, path[k], nd)
    def fl(k, nd):
        b.put("x%d" % k, other(path[k]), nd)
    h(1, "s")
    h(L, "t")
    for k in range(1, L):
        h(k, "y%d" % k)
        h(k + 1, "y%d" % k)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                fl(p, "z%d_%d" % (p, q))
                h(q, "z%d_%d" % (p, q))
    for k in range(1, L + 1):
        fl(k, "t")
    for k in range(1, L + 1):
        m = b.switch("m%d" % k)
        if k % 2 == 0:
            b.less.append((m, "x%d" % k))
            for nd in ("n%d" % k, "n'%d" % k):
                b.put(m, "E", nd)
                h(k, nd)
            for j in range(2, L + 1, 2):
                if j != k:
                    b.put(m, "E", "n%d_%d" % (k, j))
                    fl(j, "n%d_%d" % (k, j))
            for i in range(1, L + 1, 2):
                b.put(m, "E", "c%d_%d" % (i, k))
            b.put(m, "F", "t")
        else:
            b.less.append(("x%d" % k, m))
            b.put(m, "E", "t")
            for j in range(2, L + 1, 2):
                b.put(m, "E", "c%d_%d" % (k, j))
            for nd in ("e%d" % k, "e'%d" % k):
                b.put(m, "F", nd)
                h(k, nd)
            for j in range(1, L + 1, 2):
                if j != k:
                    b.put(m, "F", "n'%d_%d" % (k, j))
                    fl(j, "n'%d_%d" % (k, j))
    G = b.build()
    intended = {}
    for k in range(1, L + 1):
        intended["x%d" % k] = 0 if k % 2 == 1 else 1
        intended["m%d" % k] = 1 if k % 2 == 0 else 0
    return G, intended


def yfam(k, contact=False):
    b = Builder()
    path = {j: ("E" if j <= k else "F") for j in range(1, 2 * k + 1)}
    for j in range(1, 2 * k + 1):
        b.switch("x%d" % j)
    def h(j, nd):
        b.put("x%d" % j, path[j], nd)
    def fl(j, nd):
        b.put("x%d" % j, other(path[j]), nd)
    h(1, "s")
    h(2 * k, "t")
    for j in range(1, 2 * k):
        h(j, "y%d" % j)
        h(j + 1, "y%d" % j)
    for p in range(1, 2 * k + 1):
        for q in range(p + 1, 2 * k + 1):
            if path[p] != path[q]:
                fl(p, "z%d_%d" % (p, q))
                h(q, "z%d_%d" % (p, q))
            else:
                fl(p, "w%d_%d" % (p, q))
                fl(q, "w%d_%d" % (p, q))
    for c in range(1, k + 1):
        m = b.switch("m%d" % c)
        b.less.append(("x%d" % c, m))
        for bb in range(1, k + 1):
            if bb != c:
                b.put(m, "F", "f%d_%d" % (c, bb))
                fl(bb, "f%d_%d" % (c, bb))
        for q in range(k + 1, 2 * k + 1):
            b.put(m, "E", "e%d_%d" % (c, q))
            fl(q, "e%d_%d" % (c, q))
        for c2 in range(1, k + 1):
            if c2 != c:
                b.put(m, "E", "g%d_%d" % (min(c, c2), max(c, c2)))
        if contact:
            b.put(m, "F", "p%d" % c)
            h(k + c, "p%d" % c)
    G = b.build()
    intended = {"x%d" % j: (0 if j <= k else 1) for j in range(1, 2 * k + 1)}
    intended.update({"m%d" % c: 0 for c in range(1, k + 1)})
    return G, intended


def p2_incomparable(G):
    bad = []
    for a in range(G.m):
        for c in range(a + 1, G.m):
            if G.le[a][c] or G.le[c][a]:
                continue
            if not (G.E[a] & G.E[c]) and not (G.F[a] & G.F[c]):
                bad.append((G.names[a], G.names[c]))
    return bad


def report(tag, G, intended):
    sols = G.solutions()
    want = [intended[nm] for nm in G.names]
    fixed, status = G.prune()
    free = [G.names[w] for w in range(G.m) if w not in fixed]
    agree = all(intended[G.names[w]] == mo for w, mo in fixed.items())
    print("%s: switches %d, nodes %d, P2 failures %s, solutions %d, unique = intended: %s; propagation fixes %d "
          "(all agree with the solution: %s), free %s" % (tag, G.m, G.N, p2_incomparable(G)[:4], len(sols),
                                                          len(sols) == 1 and sols[0] == want, len(fixed), agree,
                                                          free))
    sys.stdout.flush()


def main():
    LMAX, KMAX = int(sys.argv[1]), int(sys.argv[2])
    for L in range(2, LMAX + 1):
        G, it = xfam(L)
        report("X_%d" % L, G, it)
    for k in range(2, KMAX + 1):
        for contact in (False, True):
            G, it = yfam(k, contact)
            report(("Y'_%d" if contact else "Y_%d") % k, G, it)


if __name__ == "__main__":
    main()
