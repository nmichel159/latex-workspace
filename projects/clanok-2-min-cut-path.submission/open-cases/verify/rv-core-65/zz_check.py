"""End-to-end check of the private-node model (reviewer rv-core-65): for every ZZ instance with K middle elements (as in
enum_zz.py: every preorder on the middle elements, u least, v greatest, every set R of strict pairs except {u, v}),
the ZZ answer computed from the definition (some down-set D with u in D, v not in D such that the R-edges with exactly
one end in D connect u and v) equals the answer of the general switch form of gsf.from_zz (middle edges as private
nodes of F_z & E_v), and P2 in ZZ form (every incomparable pair has a common R-neighbour strictly below or strictly
above both) equals P2 in switch form.

usage: python zz_check.py K
"""
import sys
import time
from collections import Counter
from gsf import from_zz
from enum_zz import preorders


def zz_answer(q, le, R, u, v):
    # all down-sets of the preorder on q elements containing u and missing v
    elems = list(range(q))
    out = False
    for mask in range(1 << q):
        if not (mask >> u) & 1 or (mask >> v) & 1:
            continue
        ok = True
        for b in elems:
            if (mask >> b) & 1:
                for a in elems:
                    if le[a][b] and not (mask >> a) & 1:
                        ok = False
                        break
            if not ok:
                break
        if not ok:
            continue
        adj = {x: [] for x in elems}
        for a, b in R:
            if ((mask >> a) & 1) != ((mask >> b) & 1):
                adj[a].append(b)
                adj[b].append(a)
        seen = {u}
        stack = [u]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if v in seen:
            return True
    return out


def zz_p2(q, le, R):
    nb = {x: set() for x in range(q)}
    for a, b in R:
        nb[a].add(b)
        nb[b].add(a)
    for x in range(q):
        for y in range(x + 1, q):
            if le[x][y] or le[y][x]:
                continue
            ok = False
            for w in nb[x] & nb[y]:
                if (le[w][x] and not le[x][w] and le[w][y] and not le[y][w]) or \
                   (le[x][w] and not le[w][x] and le[y][w] and not le[w][y]):
                    ok = True
                    break
            if not ok:
                return False
    return True


def main():
    K = int(sys.argv[1])
    q = K + 2
    st = Counter()
    t0 = time.time()
    for lem in preorders(K):
        le = [[False] * q for _ in range(q)]
        for a in range(q):
            le[0][a] = True
            le[a][1] = True
            le[a][a] = True
        for a in range(K):
            for b in range(K):
                le[a + 2][b + 2] = lem[a][b]
        strict = [(0, w) for w in range(2, q)] + [(w, 1) for w in range(2, q)]
        strict += [(a + 2, b + 2) for a in range(K) for b in range(K) if lem[a][b] and not lem[b][a]]
        for mask in range(1 << len(strict)):
            R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
            I = from_zz(q, 0, 1, le, R)
            I.validate()
            st["instances"] += 1
            a1 = zz_answer(q, le, R, 0, 1)
            a2 = I.yes()
            st["yes" if a1 else "no"] += 1
            if a1 != a2:
                st["ZZ ANSWER != SWITCH-FORM ANSWER"] += 1
            p1 = zz_p2(q, le, R)
            p2 = I.p2()
            st["P2" if p1 else "not P2"] += 1
            if p1 != p2:
                st["ZZ P2 != SWITCH-FORM P2"] += 1
    print("zz_check K %d (%.0fs): %s" % (K, time.time() - t0, dict(sorted(st.items()))))


if __name__ == "__main__":
    main()
