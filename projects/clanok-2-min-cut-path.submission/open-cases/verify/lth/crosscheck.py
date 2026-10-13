"""Cross-check of the own implementations against the other agent's scripts (imported read-only, only here, after
the own checks were finished): dc-hardness/tic_poly.poly_solve (Theorem T) and dc-hardness/helly2ch.helly_solve
(Theorem H, t = 1), on instances from the own generators. Reference answer: own brute force.
Usage: python crosscheck.py <seed> <count TIC> <count 2CH>"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from core import *
from test_T import gen as gen_tic, FAMS as TFAMS
from test_H import gen as gen_2ch

sys.path.insert(1, os.path.join(HERE, "..", "..", "dc-hardness"))
sys.setrecursionlimit(100000)
import tic_poly  # noqa: E402
import helly2ch  # noqa: E402

if __name__ == "__main__":
    seed, c1, c2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    st = {"tic": 0, "tic_p2": 0, "tic_agree_all": 0, "tic_mismatch": 0, "2ch": 0, "2ch_agree": 0,
          "2ch_mismatch": 0}
    fams = ["rand", "pool", "empty", "zero", "sat", "rigidmut", "hard", "chain"]
    for it in range(c1):
        fam = fams[it % len(fams)]
        K, sw = gen_tic(fam, rng)
        if K > 9 or len(sw) > 9:
            continue
        E = [x[0] for x in sw]; F = [x[1] for x in sw]
        ans = brute_tic(K, sw)[0]
        mine = tic_T(K, sw)
        theirs = tic_poly.poly_solve(K, E, F)[0]
        st["tic"] += 1
        st["tic_p2"] += p2_tic(sw)
        if ans == mine == theirs:
            st["tic_agree_all"] += 1
        else:
            st["tic_mismatch"] += 1
            print("TIC MISMATCH", fam, K, sw, "brute", ans, "own", mine, "agent", theirs, flush=True)
    for it in range(c2):
        fam = ["rand", "tree", "sparse", "hardrand"][it % 4]
        inst = gen_2ch(fam, rng)
        N, s, t, sw = inst
        if N > 7:
            continue
        theirs_inst = (N, [x[0] for x in sw], [x[1] for x in sw], s, t)
        ans = brute_2ch(inst)[0]
        mine = h_search(inst, 1)
        theirs = helly2ch.helly_solve(theirs_inst)
        st["2ch"] += 1
        if mine == bool(theirs):
            st["2ch_agree"] += 1
        else:
            st["2ch_mismatch"] += 1
            print("2CH MISMATCH", fam, inst, "brute", ans, "own", mine, "agent", theirs, flush=True)
    print(st)
    print("violations:", st["tic_mismatch"] + st["2ch_mismatch"])
