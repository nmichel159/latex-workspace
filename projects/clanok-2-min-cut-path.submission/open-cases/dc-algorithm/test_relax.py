"""Are arc consistency (AC) or path consistency (PC) of the path-position CSP (zz.py) exact on ZZ instances,
with and without P2?  AC/PC are necessary conditions; a false positive is an instance where the relaxation says
'yes' and the exact answer is 'no'.  Prints the first (smallest n) false positive per class.
Usage: python test_relax.py SEED COUNT [pc]"""
import os
import sys
import random
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402


def one(args):
    seed, p2, do_pc = args
    rng = random.Random(seed)
    n = rng.randint(5, 10)
    z = zz.random_zz(rng, n, rng.choice([0.1, 0.2, 0.35]), rng.choice([0.2, 0.4, 0.6]),
                     prefer_uv=rng.choice([0.0, 0.3]), p2=p2)
    if p2:
        assert not z.p2_bad()
    ex, wit = zz.exact(z)
    ac = zz.ac_answer(z)
    pc = zz.pc_answer(z) if (do_pc and ac and not ex) else None
    if ex:
        assert ac
    return seed, p2, n, ex, ac, pc, (z.n, [r[:] for r in z.lt], z.R) if (ac and not ex) else None


if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    do_pc = len(sys.argv) > 3
    jobs = [(seed0 * 1000003 + i, p2, do_pc) for i in range(count) for p2 in (True, False)]
    st = {}
    first = {}
    with Pool(30) as pool:
        for seed, p2, n, ex, ac, pc, inst in pool.imap_unordered(one, jobs, chunksize=16):
            key = ("P2" if p2 else "noP2", "yes" if ex else "no", "AC-yes" if ac else "AC-no",
                   "" if pc is None else ("PC-yes" if pc else "PC-no"))
            st[key] = st.get(key, 0) + 1
            if inst is not None:
                k2 = (p2, pc)
                if k2 not in first or n < first[k2][0]:
                    first[k2] = (n, seed, inst)
    for k in sorted(st):
        print(k, st[k])
    for k2, (n, seed, inst) in sorted(first.items(), key=str):
        nn, lt, R = inst
        rel = [(a, b) for a in range(nn) for b in range(nn) if lt[a][b]]
        print("first false positive", k2, "n =", n, "seed", seed)
        print("   order:", rel)
        print("   R:", R)
