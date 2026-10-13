"""Exactness of the AC / PC relaxations of the path-position CSP (zz.py) on several families of ZZ instances.
Families: rand (random order + P2 completion), pi / plant (Pi-instances of theory-dc-scripts/pi.py, converted by
Theorem 13(a)), sw (switch model with P2), noP2 (random orders without P2, control).
For every AC false positive, PC is run.  The smallest false positive of each kind is printed.
Usage: python test_relax2.py SEED COUNT"""
import os
import sys
import random
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "theory-dc-scripts")))
import zz  # noqa: E402
import pi  # noqa: E402
import sw2  # noqa: E402


def make(fam, rng):
    if fam == "rand":
        return zz.random_zz(rng, rng.randint(8, 12), rng.choice([0.1, 0.2, 0.3]), rng.choice([0.15, 0.3, 0.5]),
                            prefer_uv=rng.choice([0.0, 0.2]))
    if fam == "noP2":
        return zz.random_zz(rng, rng.randint(8, 12), rng.choice([0.1, 0.2, 0.3]), rng.choice([0.15, 0.3, 0.5]),
                            p2=False)
    if fam == "pi":
        inst = pi.random_instance(rng, rng.randint(7, 11), rng.choice([0.3, 0.45]), rng.choice([0.1, 0.2]))
        return zz.from_pi(inst)
    if fam == "plant":
        inst = None
        while inst is None:
            q = rng.randint(8, 12)
            inst = pi.planted_instance(rng, q, rng.randint(1, (q - 2) // 2), 0.4, 0.15, 0.1)
        return zz.from_pi(inst)
    if fam == "sw":
        while True:
            inst = sw2.random_inst(rng, rng.randint(2, 4), rng.randint(2, 4), rng.randint(3, 6),
                                   rng.choice([0.1, 0.2]), 3, 3)
            if sw2.p2(inst[3], inst[4]):
                return zz.from_sw(*inst)
    raise ValueError(fam)


def one(args):
    fam, seed = args
    rng = random.Random(seed)
    z = make(fam, rng)
    if fam != "noP2":
        assert not z.p2_bad()
    ex, _ = zz.exact(z)
    ac = zz.ac_answer(z)
    if ex and not ac:
        return fam, seed, z.n, ex, ac, None, "AC-WRONG"
    pc = None
    if ac and not ex:
        pc = zz.pc_answer(z)
    return fam, seed, z.n, ex, ac, pc, None


if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    fams = ["rand", "pi", "plant", "sw", "noP2"]
    jobs = [(f, seed0 * 1000003 + i) for i in range(count) for f in fams]
    st = {}
    first = {}
    with Pool(30) as pool:
        for fam, seed, n, ex, ac, pc, err in pool.imap_unordered(one, jobs, chunksize=4):
            key = (fam, "yes" if ex else "no", "AC+" if ac else "AC-", "" if pc is None else ("PC+" if pc else "PC-"))
            st[key] = st.get(key, 0) + 1
            if err:
                print("ERROR", fam, seed, err)
            if ac and not ex:
                k2 = (fam, pc)
                if k2 not in first or n < first[k2][0]:
                    first[k2] = (n, seed)
    for k in sorted(st):
        print(k, st[k])
    for k2 in sorted(first, key=str):
        print("smallest false positive", k2, first[k2])
