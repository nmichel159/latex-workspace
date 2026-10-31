"""Run the constructive proof (prove.certificate) on every shortest valid path of many instances.
Families: random P2 instances (sw.random_p2_instance, sw.p2_repair_existing), planted words with random
orientations and extra contacts (gen.planted), rigid R_L, A14, the 18-element alternating instance.
Records the largest numbers of dominators, singletons and the storage; any AssertionError is a failure of a proof
step and is printed with the instance.
Usage: python test_prove.py SEED COUNT [MODE]   (MODE: random | repair | planted | all)"""
import sys
import random
import time
import json

import sw
import gen
import prove

A14 = [7, [5, 12, 24, 16, 4, 20], [16, 32, 48, 48, 96, 66], 0, 1]
A18 = [7, [5, 40, 24, 32, 96, 32], [22, 12, 18, 48, 2, 66], 0, 1]


def gen_instance(rng, mode):
    if mode == "random":
        return sw.random_p2_instance(rng, rng.randint(3, 7), rng.randint(3, 9), rng.uniform(0.1, 0.4),
                                     rng.uniform(0.1, 0.4))
    if mode == "repair":
        N = rng.randint(4, 9)
        n = rng.randint(3, 10)
        E = [sum(1 << x for x in range(N) if rng.random() < 0.25) for _ in range(n)]
        F = [sum(1 << x for x in range(N) if rng.random() < 0.25) for _ in range(n)]
        return sw.p2_repair_existing(rng, (N, E, F, 0, 1), p_new=rng.uniform(0.1, 0.6))
    if mode == "planted":
        L = rng.randint(4, 11)
        word = "".join(rng.choice("EF") for _ in range(L))
        po = rng.random()
        inst, P = gen.planted(word, rng, lambda p, q: "f" if rng.random() < po else "b",
                              rng.uniform(0, 0.3), rng.uniform(0, 0.3))
        return inst
    raise ValueError(mode)


def run_one(inst, stats, label=""):
    L, paths = sw.shortest_valid_paths(inst, limit=200)
    if L is None:
        stats["no"] += 1
        return
    stats["yes"] += 1
    for P in paths:
        try:
            Pu, certs, st, info = prove.certificate(inst, P)
        except AssertionError as ex:
            stats["fail"] += 1
            print("FAIL", label, repr(ex), sw.fmt(inst), "P=", P, flush=True)
            continue
        nd = max(len(certs[T][0]) for T in (0, 1))
        ns = max(len([x for x in certs[T][1] if x is not None]) for T in (0, 1))
        stats["paths"] += 1
        stats["maxdom"] = max(stats["maxdom"], nd)
        stats["maxsing"] = max(stats["maxsing"], ns)
        stats["maxstore"] = max(stats["maxstore"], st)
        key = info.split(" ")[0] if info.startswith("swap") else "direct"
        stats[key] = stats.get(key, 0) + 1
        if "rows" in info:
            stats["badcase"] = stats.get("badcase", 0) + 1


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else "all"
    rng = random.Random(seed)
    stats = dict(yes=0, no=0, paths=0, fail=0, maxdom=0, maxsing=0, maxstore=0)
    t0 = time.time()
    if mode in ("all", "families"):
        for L in range(2, 13):
            inst, P = gen.rigid(L)
            run_one(inst, stats, "R_%d" % L)
        run_one(tuple(A14), stats, "A14")
        run_one(tuple(A18), stats, "A18")
    modes = ["random", "repair", "planted"] if mode in ("all", "families") else [mode]
    for it in range(count):
        m = modes[it % len(modes)]
        inst = gen_instance(rng, m)
        if len(inst[1]) > 14:
            continue
        run_one(inst, stats, m)
    print("seed", seed, "count", count, "mode", mode, stats, "%.1fs" % (time.time() - t0), flush=True)
