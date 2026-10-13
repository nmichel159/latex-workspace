"""Exhaustive check of Theorem 13(b) for tiny instances: every preorder on q <= QMAX labelled elements with
u = 0 least and v = q-1 greatest, every R (subset of the strict pairs, uv excluded).
For every instance: N <= 3 implies no consistent zigzag. For every instance with P2 and N >= 3: realise
(M = N + 1 and M = 1), check d = 2, c = N, DC, and PIMC of G(Pi) (prefix search) = ZZ answer.
Usage: python exhaustive_b.py QMAX [workers]"""
import sys, time, itertools
from collections import Counter
from multiprocessing import Pool
from eqcore import (adj_masks, leq, lt, check_P2, zz_dfs, zz_downsets, realise, Flow, bfs_dist, in_class_flow,
                    pimc_flow_dfs)


def preorders(q):
    u, v = 0, q - 1
    free = [(x, y) for x in range(q) for y in range(q) if x != y and x != u and y != v]
    for bits in range(1 << len(free)):
        rel = [[x == y for y in range(q)] for x in range(q)]
        for x in range(q):
            rel[u][x] = True
            rel[x][v] = True
        for i, (x, y) in enumerate(free):
            if (bits >> i) & 1:
                rel[x][y] = True
        ok = True
        for x in range(q):
            for y in range(q):
                if rel[x][y]:
                    for z in range(q):
                        if rel[y][z] and not rel[x][z]:
                            ok = False
                            break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            down = [sum(1 << x for x in range(q) if rel[x][y]) for y in range(q)]
            yield down


def work(args):
    q, down = args
    u, v = 0, q - 1
    st = Counter()
    viol = []
    pairs = [(a, b) for a in range(q) for b in range(q) if a != b and lt(down, a, b) and {a, b} != {u, v}]
    N = len(pairs) + (1 if lt(down, u, v) else 0)
    for mask in range(1 << len(pairs)):
        R = [(min(a, b), max(a, b)) for i, (a, b) in enumerate(pairs) if (mask >> i) & 1]
        Radj = adj_masks(q, R)
        z1, _ = zz_dfs(q, down, Radj, u, v)
        z2, _ = zz_downsets(q, down, Radj, u, v)
        if z1 != z2:
            viol.append(("solvers disagree", q, down, R))
        st["instances"] += 1
        if N <= 3:
            st["N<=3 instances"] += 1
            if z1:
                viol.append(("N<=3 yes-instance", q, down, R))
            continue
        if check_P2(q, down, Radj):
            continue
        st["P2 instances with N>=4" if N >= 4 else "P2 instances with N=3"] += 1
        st["P2 yes" if z1 else "P2 no"] += 1
        for M in (None, 1):
            n, edges, N2, info = realise(q, down, R, u, v, M=M)
            F = Flow(n, edges)
            c = F.conn(u, v)
            if c != N2:
                viol.append(("c != N", M, q, down, R))
            if bfs_dist(adj_masks(n, edges), u)[v] != 2:
                viol.append(("d != 2", M, q, down, R))
            if not in_class_flow(n, edges, 2):
                viol.append(("not DC", M, q, down, R))
            pans, _, _ = pimc_flow_dfs(n, edges, u, v, c=c)
            if pans != z1:
                viol.append(("PIMC != ZZ", M, q, down, R, pans, z1))
    return st, viol


if __name__ == "__main__":
    qmax = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    t0 = time.time()
    items = []
    for q in range(2, qmax + 1):
        ps = list(preorders(q))
        print("q = %d: %d preorders with u least, v greatest" % (q, len(ps)))
        items += [(q, d) for d in ps]
    total = Counter()
    viol = []
    with Pool(workers) as pool:
        for st, vi in pool.imap_unordered(work, items, chunksize=1):
            total.update(st)
            viol.extend(vi)
    for k in sorted(total):
        print("%-30s %d" % (k, total[k]))
    print("violations:", len(viol))
    for x in viol[:20]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
