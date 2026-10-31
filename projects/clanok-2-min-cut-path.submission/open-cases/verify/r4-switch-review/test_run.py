"""Proof steps on critical-run instances (gen_run.py) and their reversals; optional saturation.

usage: python test_run.py seed tasks [workers] [sat]
Each task makes 40 attempts with random zone words, run length, matrix densities, hubs, off-path switches.
"""
import sys
import json
import random
from multiprocessing import Pool

from gen_run import gen_run
from planted import is_shortest, saturate
from core import shortest_valid_paths
from proof import check_path, ClaimFailure, Ctx, theorem8, straddles


def one(args):
    seed, sat = args
    rng = random.Random(seed)
    stats = {}
    res = {"gen": 0, "pre": 0, "kept": 0, "paths": 0, "planted_step3": 0, "fail": []}
    for _ in range(40):
        res["gen"] += 1
        kw = [rng.choice('OOOT') for _ in range(rng.randint(0, 4))]
        lw = [rng.choice('OOOOT') for _ in range(rng.randint(4, 9))]
        m = rng.randint(1, 6)
        g = gen_run(rng, kw, m, lw, hub=rng.choice([0, 0, 0.3]), pM=rng.choice([0.5, 0.65, 0.8]),
                    pB=rng.choice([0.1, 0.25]), p_extra=rng.choice([0, 0, 0.03]), reverse=rng.random() < 0.5,
                    off=rng.choice([0, 0, 1, 2]), off_dens=rng.choice([0.03, 0.08]),
                    two_spans=rng.random() < 0.3)
        if g is None:
            continue
        res["pre"] += 1
        inst, P, T = g
        if not is_shortest(inst, P):
            continue
        if sat:
            inst, P, _ = saturate(rng, inst, P, rng.randint(5, 30))
        res["kept"] += 1
        ctx = Ctx(inst, P)
        if not straddles(ctx, T):
            try:
                _, _, step = theorem8(ctx, T, {})
                if step == 3:
                    res["planted_step3"] += 1
            except ClaimFailure:
                pass
        L, paths = shortest_valid_paths(inst, limit=20)
        assert L == len(P)
        for Q in [tuple(P)] + [q for q in paths if tuple(q) != tuple(P)]:
            res["paths"] += 1
            try:
                check_path(inst, Q, stats)
            except ClaimFailure as e:
                res["fail"].append((str(e.args[0]), inst.to_json(), list(Q)))
    return res, stats


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    sat = len(sys.argv) > 4 and sys.argv[4] == 'sat'
    tot = {"gen": 0, "pre": 0, "kept": 0, "paths": 0, "planted_step3": 0}
    agg, fails = {}, []
    with Pool(workers) as pool:
        for res, stats in pool.imap_unordered(one, [(seed * 100000 + i, sat) for i in range(count)]):
            for k in tot:
                tot[k] += res[k]
            fails += res["fail"]
            for k, v in stats.items():
                agg[k] = max(agg.get(k, 0), v) if k.startswith("max") else agg.get(k, 0) + v
    print("test_run seed=%d tasks=%d sat=%s" % (seed, count, sat))
    print("counts", json.dumps(tot))
    print("proof stats", json.dumps(agg, sort_keys=True))
    print("failures", len(fails))
    for f in fails[:10]:
        print(json.dumps(f))


if __name__ == "__main__":
    main()
