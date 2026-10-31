"""Proof steps on planted instances (planted.py): the planted shortest path and all other shortest paths.

usage: python test_planted.py seed count mode [workers]
mode: run (critical-run words), strad (straddles planted), sat (run words + saturation), off (off-path switches)
"""
import sys
import json
import random
from multiprocessing import Pool

from planted import gen_planted, is_shortest, saturate
from core import shortest_valid_paths, search5
from proof import check_path, ClaimFailure


def one(args):
    seed, mode = args
    rng = random.Random(seed)
    stats = {}
    res = {"gen": 0, "kept": 0, "paths": 0, "fail": []}
    for _ in range(30):
        res["gen"] += 1
        if mode == "run":
            g = gen_planted(rng, rng.randint(1, 4), rng.randint(1, 6), rng.randint(0, 5), rng.randint(1, 5),
                            zone_T=rng.choice([0, 0, 0.2]), hub=rng.choice([0, 0.3]),
                            p_contact=rng.choice([0.6, 0.8, 0.95]), p_both=rng.choice([0, 0.2]),
                            p_extra=rng.choice([0, 0.1, 0.3]))
        elif mode == "strad":
            g = gen_planted(rng, rng.randint(2, 5), rng.randint(2, 6), rng.randint(0, 4), rng.randint(3, 6),
                            zone_T=0.0, hub=rng.choice([0, 0.3]), p_contact=rng.choice([0.5, 0.8]),
                            p_both=0.1, p_extra=rng.choice([0, 0.1]), straddle=rng.randint(1, 3))
        elif mode == "off":
            g = gen_planted(rng, rng.randint(1, 4), rng.randint(1, 5), rng.randint(0, 4), rng.randint(1, 4),
                            zone_T=rng.choice([0, 0.2]), hub=rng.choice([0, 0.3]), p_contact=0.8, p_both=0.2,
                            p_extra=0.1, off=rng.randint(1, 4), off_dens=rng.choice([0.05, 0.1, 0.2]),
                            straddle=rng.randint(0, 1))
        else:  # sat
            g = gen_planted(rng, rng.randint(1, 4), rng.randint(2, 6), rng.randint(0, 4), rng.randint(2, 5),
                            zone_T=rng.choice([0, 0.2]), hub=rng.choice([0, 0.3]), p_contact=0.7, p_both=0.2,
                            p_extra=0.05, straddle=rng.randint(0, 2))
        if g is None:
            continue
        inst, P, T = g
        if len(P) > 22 or inst.n > 26:
            continue
        if not is_shortest(inst, P):
            continue
        if mode == "sat":
            inst, P, added = saturate(rng, inst, P, rng.randint(10, 60))
        res["kept"] += 1
        L, paths = shortest_valid_paths(inst, limit=30)
        assert L == len(P), (L, len(P))
        cand = [tuple(P)] + [q for q in paths if tuple(q) != tuple(P)]
        for Q in cand:
            res["paths"] += 1
            try:
                check_path(inst, Q, stats)
            except ClaimFailure as e:
                res["fail"].append((str(e.args[0]), inst.to_json(), list(Q)))
    return res, stats


def main():
    seed, count, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    tot = {"gen": 0, "kept": 0, "paths": 0}
    agg = {}
    fails = []
    with Pool(workers) as pool:
        for res, stats in pool.imap_unordered(one, [(seed * 100000 + i, mode) for i in range(count)]):
            for k in tot:
                tot[k] += res[k]
            fails += res["fail"]
            for k, v in stats.items():
                agg[k] = max(agg.get(k, 0), v) if k.startswith("max") else agg.get(k, 0) + v
    print("planted seed=%d tasks=%d (30 attempts each) mode=%s" % (seed, count, mode))
    print("counts", json.dumps(tot))
    print("proof stats", json.dumps(agg, sort_keys=True))
    print("failures", len(fails))
    for f in fails[:10]:
        print(json.dumps(f))


if __name__ == "__main__":
    main()
