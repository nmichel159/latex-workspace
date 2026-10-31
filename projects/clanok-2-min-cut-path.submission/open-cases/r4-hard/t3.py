"""Theorem T3 (r4-hard.md, Section 6): with P2 weakened to 'one-sided' witnesses (distance <= 3 in the realised
graph) the open-case question is NP-complete.

Construction: the 3-SAT instance of theory-dc.md Theorem 13(c) (dc-algorithm/zz.from_sat, imported read-only),
plus one pendant element b_x for every element x other than u, v: u < b_x < y for every y other than u and the
pendants, the pendants pairwise incomparable, one real edge b_x x.

Checks per formula: order axioms (preorder with least u, greatest v), real edges between strictly comparable
elements, {u, v} not in R, the one-sided condition P3 (every incomparable pair x, y: some R-neighbour of x is
comparable with y, or some R-neighbour of y with x), ZZ answer by two exact solvers (zz.exact_dfs and all
down-sets) against brute-force satisfiability.  Graph level (small formulas): realise with the independent code
verify/equivalence/eqcore.realise, check d(u,v) = 2, c(u,v) = N, every pair of element vertices at distance <= 3,
every ear vertex of degree 2 (so c <= 2 for its pairs), and the PIMC answer by eqcore.pimc_flow_dfs.

Usage: python t3.py SEED COUNT [GRAPH_COUNT]
"""
import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
sys.path.insert(0, os.path.join(HERE, "..", "verify", "equivalence"))
import zz  # noqa: E402
import eqcore  # noqa: E402


def sat(nvars, clauses):
    for bits in itertools.product([False, True], repeat=nvars):
        if all(any((lit > 0) == bits[abs(lit) - 1] for lit in cl) for cl in clauses):
            return True
    return False


def with_pendants(z0):
    """Return a ZZ instance (strict order) = z0 plus pendants."""
    n0, u, v = z0.n, z0.u, z0.v
    base = [x for x in range(n0) if x not in (u, v)]
    n = n0 + len(base)
    pend = {x: n0 + i for i, x in enumerate(base)}
    lt = [[False] * n for _ in range(n)]
    for a in range(n0):
        for b in range(n0):
            lt[a][b] = z0.lt[a][b]
    for x, b in pend.items():
        lt[u][b] = True
        lt[b][v] = True
        for y in range(n0):
            if y != u:
                lt[b][y] = True
    R = list(z0.R) + [(b, x) for x, b in pend.items()]
    return zz.ZZ(n, lt, R, u, v), pend


def check_order(z):
    n, le = z.n, z.le
    for a in range(n):
        assert le[a][a]
        for b in range(n):
            for c in range(n):
                if le[a][b] and le[b][c]:
                    assert le[a][c]
    for x in range(n):
        assert le[z.u][x] and le[x][z.v]
    for a, b in z.R:
        assert z.lt[a][b]
    assert (z.u, z.v) not in z.R


def p3_bad(z):
    A = z.adj()
    le = z.le
    bad = []
    for x in range(z.n):
        for y in range(x + 1, z.n):
            if le[x][y] or le[y][x]:
                continue
            ok = any(le[w][y] or le[y][w] for w in A[x]) or any(le[w][x] or le[x][w] for w in A[y])
            if not ok:
                bad.append((x, y))
    return bad


def graph_check(z):
    q = z.n
    down = [sum(1 << a for a in range(q) if z.le[a][b]) for b in range(q)]
    n, edges, N, info = eqcore.realise(q, down, z.R, z.u, z.v)
    adj = eqcore.adj_masks(n, edges)
    deg = [eqcore.popcount(a) for a in adj]
    # distances from every element vertex
    far = 0
    for x in range(q):
        dist = eqcore.bfs_dist(adj, x)
        for y in range(q):
            if y != x and (dist[y] == -1 or dist[y] > 3):
                far += 1
    ears_ok = all(deg[w] == 2 for w in range(q, n))
    du = eqcore.bfs_dist(adj, z.u)[z.v]
    F = eqcore.Flow(n, edges)
    c = F.conn(z.u, z.v)
    ans, path, nodes = eqcore.pimc_flow_dfs(n, edges, z.u, z.v, c=c)
    return dict(n=n, m=len(edges), N=N, c=c, d=du, far=far, ears_ok=ears_ok, pimc=ans)


def random_formula(rng):
    nv = rng.randint(1, 3)
    m = rng.randint(1, 4)
    cls = []
    for _ in range(m):
        k = rng.randint(1, 3)
        vs = rng.sample(range(1, nv + 1), min(k, nv))
        cls.append([x if rng.random() < 0.5 else -x for x in vs])
    return nv, cls


def main():
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    gcount = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = random.Random(seed)
    stats = dict(yes=0, no=0, mism=0, p3fail=0, p2fail_inst=0)
    for it in range(count):
        nv, cls = random_formula(rng)
        z0, names = zz.from_sat(nv, cls)
        z, pend = with_pendants(z0)
        check_order(z)
        if p3_bad(z):
            stats["p3fail"] += 1
        if z.p2_bad():
            stats["p2fail_inst"] += 1
        s = sat(nv, cls)
        a1, _ = zz.exact_dfs(z)
        q = z.n
        down = [sum(1 << a for a in range(q) if z.le[a][b]) for b in range(q)]
        Radj = [0] * q
        for a, b in z.R:
            Radj[a] |= 1 << b
            Radj[b] |= 1 << a
        a2, _ = eqcore.zz_dfs(q, down, Radj, z.u, z.v)
        if not (a1 == a2 == s):
            stats["mism"] += 1
            print("MISMATCH", nv, cls, s, a1, a2)
        stats["yes" if s else "no"] += 1
    print("seed", seed, "formulas", count, stats)
    # graph level on the smallest formulas
    small = [(1, [[1]]), (1, [[1], [-1]]), (2, [[1, 2]]), (2, [[1], [-1, 2]]), (2, [[1, -2], [-1]]),
             (1, [[-1], [1]])]
    for nv, cls in small[:gcount]:
        z0, names = zz.from_sat(nv, cls)
        z, pend = with_pendants(z0)
        r = graph_check(z)
        print("graph", nv, cls, "sat", sat(nv, cls), r, flush=True)


if __name__ == "__main__":
    main()
