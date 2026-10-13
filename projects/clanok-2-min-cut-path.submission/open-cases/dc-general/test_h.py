"""Tests of the certificate searches of hsearch.py against brute force.

Usage: python test_h.py notie SEED COUNT     2CH + P2 (every class a singleton): node and clique families
       python test_h.py tie SEED COUNT       2CHC + P2 (ties): naive condition (i) vs (i-tie), node and clique families
Every 'yes' of a search is re-checked as a consistent walk (with the class constraint), so unsoundness is reported.
"""
import sys
import random
import time
import gzz
import hsearch


def gen(rng, ties):
    while True:
        N = rng.randint(3, 7)
        n = rng.randint(2, 7)
        ncls = rng.randint(2, max(2, n - 1)) if ties else n
        inst = gzz.random_inst(rng, N, n, ncls, rng.uniform(0.1, 0.4), rng.uniform(0.1, 0.4), p2=True,
                               newnode=rng.choice([0.2, 0.5, 0.8]), maxN=14)
        if not ties:
            inst = (inst[0], inst[1], inst[2], list(range(n)), inst[4], inst[5])
            inst = gzz.repair(rng, inst, 0.5, 14)
        if gzz.p2_ok(inst):
            return inst


def main():
    mode, seed, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    ties = mode == "tie"
    variants = [("node", True), ("clique", True), ("u-clique", True)] + (
        [("node", False), ("clique", False)] if ties else [])
    st = {}
    first_bad = {}
    t0 = time.time()
    for it in range(count):
        inst = gen(rng, ties)
        ex = gzz.brute(inst) is not None
        for kind, tie_cond in variants:
            if kind.startswith("u-"):
                w, K = hsearch.solve_union(inst, kind=kind[2:], q=4, ties=tie_cond)
            else:
                w, K = hsearch.solve(inst, kind=kind, ties=tie_cond)
            got = w is not None
            valid = got and hsearch.walk_consistent(inst, w, ties=True)
            key = (kind, "i-tie" if tie_cond else "i")
            d = st.setdefault(key, {"yes-found": 0, "yes-missed": 0, "no-correct": 0, "unsound": 0})
            if got and not valid:
                d["unsound"] += 1
                if key not in first_bad:
                    first_bad[key] = (gzz.fmt(inst), w)
            elif ex and got:
                d["yes-found"] += 1
            elif ex and not got:
                d["yes-missed"] += 1
                first_bad.setdefault(key + ("missed",), gzz.fmt(inst))
            elif not ex and not got:
                d["no-correct"] += 1
            else:
                d["unsound"] += 1   # valid walk although brute force says no: would be a bug
                first_bad.setdefault(key + ("bug",), gzz.fmt(inst))
    for k, v in st.items():
        print(k, v)
    for k, v in first_bad.items():
        print("example", k, v)
    print("%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
