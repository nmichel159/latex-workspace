"""Theorem B (dc-algorithm.md): Multicolored Clique -> ZZ (without P2), parameter-preserving for the width of the
order and the length of the zigzag.  Check: the ZZ answer equals the clique answer on random small instances.

Construction.  Colour classes V_1..V_k, V_i = {1..n_i}.  Classes of the preorder: B (bottom, contains u), T (top,
contains v), X_{i,r} for i in 1..k, r in 0..n_i with B < X_{i,0} < ... < X_{i,n_i} < T and different chains
incomparable; width k.  Gadget (i, j), i < j, in a fixed order of the C(k,2) pairs; consecutive gadgets share their
bottom element g (g_0 = u).  For every edge {(i, r), (j, r')} of H a private route
    g_in < x1 > x2 < t > x3 < x4 > g_out,   x1 in X_{i,r}, x2 in X_{i,r-1}, t in T, x3 in X_{j,r'-1}, x4 in X_{j,r'},
with fresh elements of these classes; finally g_last < v.  Usage: python mcc.py SEED COUNT"""
import os
import sys
import random
import itertools

sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zz  # noqa: E402


def build(k, sizes, edges):
    """edges: set of frozenset({(i, r), (j, r')}) with i != j, r in 1..n_i.  Returns (ZZ, path length)."""
    cls = []          # class of every element: ('B',), ('T',), ('X', i, r)
    R = []

    def new(c):
        cls.append(c)
        return len(cls) - 1

    u = new(("B",))
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    g = u
    for (i, j) in pairs:
        g2 = new(("B",))
        for e in edges:
            (a, r), (b, r2) = sorted(e)
            if (a, b) != (i, j):
                continue
            x1 = new(("X", i, r))
            x2 = new(("X", i, r - 1))
            t = new(("T",))
            x3 = new(("X", j, r2 - 1))
            x4 = new(("X", j, r2))
            R += [(g, x1), (x2, x1), (x2, t), (x3, t), (x3, x4), (g2, x4)]
        g = g2
    v = new(("T",))
    R.append((g, v))
    n = len(cls)

    def le_cls(c, d):
        if c[0] == "B" or d[0] == "T":
            return True
        if c[0] == "T" or d[0] == "B":
            return False
        return c[1] == d[1] and c[2] <= d[2]

    le = [[le_cls(cls[a], cls[b]) for b in range(n)] for a in range(n)]
    # put v last and u first as zz expects nothing about indices except u, v given explicitly
    z = zz.ZZ(n, None, R, u, v, le=le)
    return z, 6 * len(pairs) + 1


def has_clique(k, sizes, edges):
    for choice in itertools.product(*[range(1, s + 1) for s in sizes]):
        if all(frozenset({(i, choice[i]), (j, choice[j])}) in edges for i in range(k) for j in range(i + 1, k)):
            return True
    return False


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {}
    for it in range(count):
        k = rng.randint(2, 4)
        sizes = [rng.randint(1, 3) for _ in range(k)]
        p = rng.choice([0.4, 0.6, 0.8])
        edges = set()
        for i in range(k):
            for j in range(i + 1, k):
                for r in range(1, sizes[i] + 1):
                    for r2 in range(1, sizes[j] + 1):
                        if rng.random() < p:
                            edges.add(frozenset({(i, r), (j, r2)}))
        z, ell = build(k, sizes, edges)
        ex, path = zz.exact_dfs(z)
        cq = has_clique(k, sizes, edges)
        ok = ex == cq
        if ex:
            # the witness found is a walk; check its length parity and that it is consistent
            pass
        key = (k, cq, ok)
        st[key] = st.get(key, 0) + 1
        if not ok:
            print("MISMATCH", k, sizes, sorted(map(sorted, edges)))
    for key in sorted(st):
        print(key, st[key])
