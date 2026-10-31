"""Hypothesis H2 on saturated switch-model instances: for every shortest valid path P, h2(P) = least over types T and
pairs u, b of T-members with |u - b| >= 3 of |f(u) ∪ f(b)| (f as in r4-switch §4); h2 = 0 if some type has no
such pair (then at most 3 classes of that type... in the switch model: all members of that type within 2 positions).
Also h1(P) = least |f(a)| over all members.  Usage: python hyp_h2_sat.py SEED COUNT LMIN LMAX"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r4-switch"))
import sw  # noqa: E402
import saturate  # noqa: E402
import prove  # noqa: E402


def h2_of(pp):
    best = None
    for T in (0, 1):
        mem = [a for a in range(pp.r) if pp.typ[a] == T]
        pairs = [(u, b) for u in mem for b in mem if b >= u + 3]
        if not pairs:
            return 0
        for u, b in pairs:
            v = len(set(pp.f(u)) | set(pp.f(b)))
            if best is None or v < best:
                best = v
    return best


if __name__ == "__main__":
    seed, count, lmin, lmax = (int(x) for x in sys.argv[1:5])
    rng = random.Random(seed)
    hist = {}
    worst = None
    t0 = time.time()
    n = 0
    for it in range(count):
        L = rng.randint(lmin, lmax)
        word = "".join(rng.choice("EF") for _ in range(L))
        inst, P0 = saturate.saturate(rng, word, 0.3)
        if inst is None:
            continue
        n += 1
        Ls, paths = sw.shortest_valid_paths(inst, limit=30)
        for P in paths:
            pp = prove.Path(inst, list(P))
            v = h2_of(pp)
            hist[v] = hist.get(v, 0) + 1
            if worst is None or v > worst[0]:
                worst = (v, word, P, sw.fmt(inst))
    print("seed", seed, "instances", n, "h2 histogram", dict(sorted(hist.items())), "worst", worst[:2],
          "%.1fs" % (time.time() - t0), flush=True)
    print("worst instance:", worst[3] if worst else None)
