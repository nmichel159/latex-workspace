"""Control: AC / PC of the path-position CSP on the 3-SAT reduction of theory-dc.md Theorem 13(c) (no P2).
Usage: python sat_relax.py SEED COUNT"""
import sys, random, itertools, os
from multiprocessing import Pool
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zz

def one(seed):
    rng = random.Random(seed)
    nv = rng.randint(2, 3); m = rng.randint(3, 6)
    cls = [[rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))] for _ in range(m)]
    sat = any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in cls)
              for a in itertools.product([False, True], repeat=nv))
    z, names = zz.from_sat(nv, cls)
    L = 2 * nv + 2 * m + 5
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z, L)
    pc = zz.pc_answer(z, L) if ac and not ex else None
    return seed, sat, ex, ac, pc, (nv, cls)

if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    st = {}; ex_fp = None
    with Pool(30) as pool:
        for seed, sat, ex, ac, pc, f in pool.imap_unordered(one, [seed0 * 100003 + i for i in range(count)]):
            k = ("sat" if sat else "unsat", "zz-yes" if ex else "zz-no", "AC+" if ac else "AC-",
                 "" if pc is None else ("PC+" if pc else "PC-"))
            st[k] = st.get(k, 0) + 1
            if pc and (ex_fp is None or len(f[1]) < len(ex_fp[1])):
                ex_fp = f
    for k in sorted(st): print(k, st[k])
    print("smallest PC false positive (formula):", ex_fp)
