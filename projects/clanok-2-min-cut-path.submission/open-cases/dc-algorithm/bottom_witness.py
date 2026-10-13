"""Theorem F' check: ZZ instances in which every two incomparable elements have a common real neighbour equivalent
to u ("bottom witnesses"), or dually equivalent to v.  Algorithm: for every set A of at most two elements, take
D_A = Q - up(A + {v}) (dual: D_A = down(A + {u})) and search the cut graph of D_A for a u-v path.
Compared with zz.exact_dfs and zz.exact (all down-sets) on random instances, plus a count of the minimal peaks of a
shortest path in the witness cut (the theorem says at most two) and of PC answers on the no-instances.
Usage: python bottom_witness.py SEED COUNT"""
import sys
import random
from collections import deque
import zz
import pcfast


def random_instance(rng, dual=False):
    nb = rng.randint(1, 3)            # elements equivalent to u: 0..nb-1
    nm = rng.randint(2, 9)            # middle elements
    nt = rng.randint(1, 3)            # elements equivalent to v (v = last)
    n = nb + nm + nt
    M = list(range(nb, nb + nm))
    T = list(range(nb + nm, n))
    p = rng.choice([0.1, 0.25, 0.4])
    perm = M[:]
    rng.shuffle(perm)
    less = set()
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < p:
                less.add((perm[i], perm[j]))
    lt = zz.closure(n, less | {(b, x) for b in range(nb) for x in M + T} | {(x, t) for x in M for t in T})
    le = [[lt[a][b] or a == b for b in range(n)] for a in range(n)]
    for a in range(nb):
        for b in range(nb):
            le[a][b] = True
    for a in T:
        for b in T:
            le[a][b] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    u, v = 0, n - 1
    strict = [(a, b) for a in range(n) for b in range(n) if le[a][b] and not le[b][a] and (a, b) != (u, v)]
    pr = rng.choice([0.15, 0.3, 0.5])
    R = {e for e in strict if rng.random() < pr}
    W = T if dual else list(range(nb))
    adj = [set() for _ in range(n)]
    for a, b in R:
        adj[a].add(b)
        adj[b].add(a)
    for x in M:
        for y in M:
            if x < y and not le[x][y] and not le[y][x] and not (adj[x] & adj[y] & set(W)):
                w = rng.choice(W)
                for z in (x, y):
                    e = (z, w) if dual else (w, z)
                    R.add(e)
                    adj[e[0]].add(e[1])
                    adj[e[1]].add(e[0])
    return zz.ZZ(n, None, sorted(R), u, v, le=le)


def path_in(z, D, adj):
    par = {z.u: None}
    dq = deque([z.u])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in par and (x in D) != (y in D):
                par[y] = x
                dq.append(y)
    if z.v not in par:
        return None
    p = [z.v]
    while par[p[-1]] is not None:
        p.append(par[p[-1]])
    return p[::-1]


def algo(z, dual=False):
    n, le = z.n, z.le
    adj = z.adj()
    for A in [()] + [(a,) for a in range(n)] + [(a, b) for a in range(n) for b in range(a + 1, n)]:
        if dual:
            gens = list(A) + [z.u]
            D = {x for x in range(n) if any(le[x][g] for g in gens)}
        else:
            gens = list(A) + [z.v]
            D = {x for x in range(n) if not any(le[g][x] for g in gens)}
        if z.u not in D or z.v in D:
            continue
        if path_in(z, D, adj) is not None:
            return True
    return False


def bottom_witness_ok(z, dual=False):
    n, le = z.n, z.le
    adj = z.adj()
    W = {w for w in range(n) if le[w][z.v] and le[z.v][w]} if dual else {w for w in range(n) if le[w][z.u] and le[z.u][w]}
    return all(adj[x] & adj[y] & W for x in range(n) for y in range(x + 1, n) if not le[x][y] and not le[y][x])


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    stats = {"instances": 0, "yes": 0, "mismatch": 0, "pc_fp": 0, "ac_fp": 0, "no": 0, "dual": 0}
    for it in range(count):
        dual = rng.random() < 0.5
        z = random_instance(rng, dual)
        assert bottom_witness_ok(z, dual) and not z.p2_bad()
        ex = zz.exact_dfs(z)[0]
        ex2 = zz.exact(z)[0]
        a = algo(z, dual)
        stats["instances"] += 1
        stats["dual"] += dual
        stats["yes"] += ex
        if not (ex == ex2 == a):
            stats["mismatch"] += 1
            print("MISMATCH", it, ex, ex2, a, flush=True)
        if not ex:
            stats["no"] += 1
            if zz.ac_answer(z):
                stats["ac_fp"] += 1
                if pcfast.pc_answer(z):
                    stats["pc_fp"] += 1
    print(seed, stats, flush=True)
