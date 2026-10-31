"""Hypothesis H on saturated switch-model instances (r4-switch/saturate.py, read-only import): for every shortest
valid path P, the least |f(a)| over all members a (f(a) = members of the other type meeting the partner of a), and
the least over each type.  Records the maximum over instances of these minima.
Usage: python hyp_h_sat.py SEED COUNT LMIN LMAX"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r4-switch"))
import sw  # noqa: E402
import saturate  # noqa: E402
import prove  # noqa: E402

seed, count, lmin, lmax = (int(x) for x in sys.argv[1:5])
rng = random.Random(seed)
hist = {}
hist_type = {}
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
        fs = [len(pp.f(a)) if pp.pid[a] is not None else 0 for a in range(pp.r)]
        m_all = min(fs)
        per = []
        for T in (0, 1):
            v = [fs[a] for a in range(pp.r) if pp.typ[a] == T]
            per.append(min(v) if v else -1)
        hist[m_all] = hist.get(m_all, 0) + 1
        key = tuple(sorted(per))
        hist_type[key] = hist_type.get(key, 0) + 1
        if worst is None or m_all > worst[0]:
            worst = (m_all, per, word, P)
print("seed", seed, "instances", n, "min|f| over all members:", dict(sorted(hist.items())),
      "per-type minima (sorted):", dict(sorted(hist_type.items())), "worst", worst[:3], "%.1fs" % (time.time() - t0))
