"""AC / PC of the path-position CSP on P2 completions of the 3-SAT reduction (theory-dc.md Theorem 13(c)):
the SAT instance plus random common bounding neighbours for every incomparable pair (zz.p2_complete).
Usage: python satp2_relax.py SEED COUNT"""
import sys, random, itertools, os
from multiprocessing import Pool
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zz

def one(seed):
    rng = random.Random(seed)
    nv = rng.randint(2, 3); m = rng.randint(2, 5)
    cls = [[rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))] for _ in range(m)]
    sat = any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in cls)
              for a in itertools.product([False, True], repeat=nv))
    z0, names = zz.from_sat(nv, cls)
    R = zz.p2_complete(rng, z0.n, z0.lt, z0.R, prefer_uv=rng.choice([0.0, 0.5, 0.9]))
    z = zz.ZZ(z0.n, z0.lt, R, z0.u, z0.v)
    assert not z.p2_bad()
    L = min(z.n if z.n % 2 else z.n - 1, 2 * nv + 2 * m + 9)
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z, L)
    pc = zz.pc_answer(z, L) if ac and not ex else None
    if ex and not ac:
        return seed, sat, ex, ac, "L-too-small", None
    return seed, sat, ex, ac, pc, (nv, cls)

if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    st = {}
    with Pool(30) as pool:
        for seed, sat, ex, ac, pc, f in pool.imap_unordered(one, [seed0 * 100003 + i for i in range(count)]):
            k = ("sat" if sat else "unsat", "zz-yes" if ex else "zz-no", "AC+" if ac else "AC-", str(pc))
            st[k] = st.get(k, 0) + 1
    for k in sorted(st): print(k, st[k])
