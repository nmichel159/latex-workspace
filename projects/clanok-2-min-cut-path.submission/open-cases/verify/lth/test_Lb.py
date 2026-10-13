"""Theorem L(b) of dc-hardness.md (agent verify-LTH): the 3-SAT variant is equisatisfiable and has the stated
occurrence pattern; the two-choice interval cover encoding (width 1, reach <= 2, no P2) is coverable iff the
formula is satisfiable. Usage: python test_Lb.py <seed> <count>"""
import sys
import random

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import brute_tic, p2_tic
from satenc import *

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"formulas": 0, "sat": 0, "unsat": 0, "viol": 0, "maxswitches": 0, "p2": 0, "exhaustive_small": 0}
    for it in range(count):
        nv = rng.randint(1, 4); nc = rng.randint(1, 6)
        cl = rand_cnf(rng, nv, nc)
        v2, c2 = to_variant(nv, cl)
        nocc = sum(len(c) for c in c2)
        if nocc > 15:
            continue
        st["formulas"] += 1
        s1 = sat_brute(nv, cl)
        s2 = sat_brute(v2, c2)
        ok_var = variant_ok(v2, c2)
        K, sw, occs = encode_tic(v2, c2)
        reach = max(sp[1] - sp[0] for pair in sw for sp in pair if sp is not None)
        cov, _ = brute_tic(K, sw)
        st["maxswitches"] = max(st["maxswitches"], len(sw))
        st["p2"] += p2_tic(sw)
        st["sat" if s1 else "unsat"] += 1
        if s1 != s2 or not ok_var or reach > 2 or cov != s1:
            st["viol"] += 1
            print("VIOLATION", nv, cl, v2, c2, s1, s2, ok_var, reach, cov)
    print(st)
    print("violations:", st["viol"])
