"""Acceptance rate and hardness of planted instances (development helper).
usage: python try_planted.py SEED COUNT r nTc nOc mates [p_live] [p_contact] [local_only]"""
import random
import sys
import time

from qcore import kq
from qchecks import full_covers
from qgen import planted


def main():
    seed, count, r, nTc, nOc, mates = map(int, sys.argv[1:7])
    p_live = float(sys.argv[7]) if len(sys.argv) > 7 else 0.2
    p_contact = float(sys.argv[8]) if len(sys.argv) > 8 else 0.3
    local = bool(int(sys.argv[9])) if len(sys.argv) > 9 else False
    rng = random.Random(seed)
    acc = 0
    t0 = time.time()
    for it in range(count):
        I, P = planted(rng, r, nTc, nOc, T=0, mates=mates, p_live=p_live, p_contact=p_contact, local_only=local)
        assert I.p2(), I.p2_violations()[:3]
        L, paths = I.shortest_paths_dfs(limit=200, maxlen=r)
        ok = L == r and P in paths
        if ok:
            acc += 1
            hO, hT = full_covers(I, list(P), 0)
            print(it, "ok n=%d c=%d k=%d paths=%d hO=%s hT=%s" % (I.n, I.c, kq(I.n), len(paths), hO, hT), flush=True)
        else:
            print(it, "rejected L=%s" % L, flush=True)
    print("accepted", acc, "of", count, "time %.1f" % (time.time() - t0))


if __name__ == "__main__":
    main()
