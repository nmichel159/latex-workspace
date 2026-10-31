"""Critical runs whose rows split into two groups with spans in two disjoint halves of C (gen_run two_spans=True):
targets |H| = 2 and holes in (F5->).  Also reversed paths (backward rows).

usage: python test_two.py seed tasks [workers]
"""
import sys
import json
import random
from multiprocessing import Pool

from gen_run import gen_run
from planted import is_shortest, saturate
from core import shortest_valid_paths
from proof import check_path, ClaimFailure


def one(seed):
    rng = random.Random(seed)
    stats = {}
    res = {"gen": 0, "kept": 0, "paths": 0, "fail": []}
    for _ in range(40):
        res["gen"] += 1
        kw = [rng.choice('OOOT') for _ in range(rng.randint(0, 3))]
        lw = [rng.choice('OOOOOT') for _ in range(rng.randint(6, 10))]
        m = rng.randint(2, 4)
        g = gen_run(rng, kw, m, lw, hub=rng.choice([0, 0.3]), pM=rng.choice([0.6, 0.8, 0.95]),
                    pB=rng.choice([0.0, 0.1, 0.3]), p_extra=rng.choice([0, 0.02]), reverse=rng.random() < 0.5,
                    off=rng.choice([0, 0, 1]), off_dens=0.05, two_spans=True)
        if g is None:
            continue
        inst, P, T = g
        if not is_shortest(inst, P):
            continue
        if rng.random() < 0.3:
            inst, P, _ = saturate(rng, inst, P, rng.randint(5, 20))
        res["kept"] += 1
        L, paths = shortest_valid_paths(inst, limit=10)
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
    tot = {"gen": 0, "kept": 0, "paths": 0}
    agg, fails = {}, []
    with Pool(workers) as pool:
        for res, stats in pool.imap_unordered(one, [seed * 100000 + i for i in range(count)]):
            for k in tot:
                tot[k] += res[k]
            fails += res["fail"]
            for k, v in stats.items():
                agg[k] = max(agg.get(k, 0), v) if k.startswith("max") else agg.get(k, 0) + v
    print("test_two seed=%d tasks=%d" % (seed, count))
    print("counts", json.dumps(tot))
    print("proof stats", json.dumps(agg, sort_keys=True))
    print("failures", len(fails))
    for f in fails[:10]:
        print(json.dumps(f))


if __name__ == "__main__":
    main()
