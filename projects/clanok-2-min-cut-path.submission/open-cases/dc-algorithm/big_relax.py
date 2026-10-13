"""Large random test of AC / PC exactness on ZZ + P2 (families rand, sw, pi, plant) with the DFS exact solver.
Usage: python big_relax.py SEED COUNT NMIN NMAX"""
import sys, random, os
from multiprocessing import Pool
sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "theory-dc-scripts")))
import zz, pi, sw2

NMIN, NMAX = 10, 14

def make(fam, rng):
    if fam == "rand":
        return zz.random_zz(rng, rng.randint(NMIN, NMAX), rng.choice([0.05, 0.1, 0.2, 0.3]),
                            rng.choice([0.1, 0.2, 0.35]), prefer_uv=rng.choice([0.0, 0.2, 0.5]))
    if fam == "sw":
        while True:
            k = rng.randint(4, 9)
            inst = sw2.random_inst(rng, rng.randint(2, 5), rng.randint(2, 5), k, rng.choice([0.05, 0.1, 0.2]), 3, 3)
            if sw2.p2(inst[3], inst[4]):
                return zz.from_sw(*inst)
    if fam == "pi":
        return zz.from_pi(pi.random_instance(rng, rng.randint(NMIN, NMAX), rng.choice([0.25, 0.35, 0.45]),
                                             rng.choice([0.05, 0.15])))
    if fam == "plant":
        inst = None
        while inst is None:
            q = rng.randint(NMIN, NMAX)
            inst = pi.planted_instance(rng, q, rng.randint(1, (q - 2) // 2), rng.choice([0.2, 0.4]),
                                       rng.choice([0.05, 0.15]), 0.1, support_prob=rng.choice([1.0, 0.7]))
        return zz.from_pi(inst)

def setn(a, b):
    globals().update(NMIN=a, NMAX=b)

def one(args):
    fam, seed = args
    rng = random.Random(seed)
    z = make(fam, rng)
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z)
    if ex and not ac:
        return fam, seed, z.n, "AC-WRONG"
    if ac and not ex:
        pc = zz.pc_answer(z)
        return fam, seed, z.n, "fpAC-PC+" if pc else "fpAC-PC-"
    return fam, seed, z.n, "yes" if ex else "no"

if __name__ == "__main__":
    seed0, count = int(sys.argv[1]), int(sys.argv[2])
    NMIN, NMAX = int(sys.argv[3]), int(sys.argv[4])
    jobs = [(f, seed0 * 1000003 + i) for i in range(count) for f in ("rand", "sw", "pi", "plant")]
    st = {}; ex = {}
    with Pool(31, initializer=setn, initargs=(NMIN, NMAX)) as pool:
        for fam, seed, n, res in pool.imap_unordered(one, jobs, chunksize=4):
            st[(fam, res)] = st.get((fam, res), 0) + 1
            if res.startswith("fpAC-PC+") or res == "AC-WRONG":
                if (fam, res) not in ex or n < ex[(fam, res)][0]:
                    ex[(fam, res)] = (n, seed)
    for k in sorted(st): print(k, st[k])
    for k in sorted(ex): print("example", k, ex[k])
