"""Parallel version of test_random.py: random 2CH + P2 instances (random sides; P2 repaired with existing or private
nodes), all claims on all shortest valid paths (at most 100 per instance), the search on no-instances with random K.

usage: python test_random_par.py seed tasks per_task maxN maxn [workers]
"""
import sys
import json
import random
from multiprocessing import Pool
from core import random_instance, p2_repair, p2, brute_force, shortest_valid_paths, search5
from proof import check_path, ClaimFailure


def one(args):
    seed, per, maxN, maxn = args
    rng = random.Random(seed)
    tot = {"inst": 0, "yes": 0, "no": 0, "paths": 0, "maxr": 0, "soundK": 0}
    fails = []
    stats = {}
    for _ in range(per):
        N = rng.randint(4, maxN)
        n = rng.randint(2, maxn)
        inst = random_instance(rng, N, n, rng.choice([0.08, 0.12, 0.2, 0.3]))
        inst = p2_repair(inst, rng, fresh=rng.random() < 0.6)
        assert p2(inst)
        tot["inst"] += 1
        L, paths = shortest_valid_paths(inst, limit=100)
        if n <= 11 and (L is not None) != brute_force(inst):
            fails.append(("solver mismatch", inst.to_json()))
        if L is None:
            tot["no"] += 1
            for _ in range(4):
                K = {y for y in range(inst.D) if rng.random() < 0.6}
                tot["soundK"] += 1
                if search5(inst, K, rng.randint(0, inst.D)) is not None:
                    fails.append(("accepted no-instance", inst.to_json()))
            continue
        tot["yes"] += 1
        tot["maxr"] = max(tot["maxr"], L)
        for P in paths:
            tot["paths"] += 1
            try:
                check_path(inst, P, stats)
            except ClaimFailure as e:
                fails.append((str(e.args[0]), inst.to_json(), list(P)))
    return tot, stats, fails


def main():
    seed, tasks, per, maxN, maxn = map(int, sys.argv[1:6])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 24
    tot, agg, fails = {}, {}, []
    with Pool(workers) as pool:
        for t, stats, f in pool.imap_unordered(one, [(seed * 100000 + i, per, maxN, maxn) for i in range(tasks)]):
            for k, v in t.items():
                tot[k] = max(tot.get(k, 0), v) if k == "maxr" else tot.get(k, 0) + v
            fails += f
            for k, v in stats.items():
                agg[k] = max(agg.get(k, 0), v) if k.startswith("max") else agg.get(k, 0) + v
    print("test_random_par seed=%d tasks=%d per=%d maxN=%d maxn=%d" % (seed, tasks, per, maxN, maxn))
    print("counts", json.dumps(tot))
    print("proof stats", json.dumps(agg, sort_keys=True))
    print("failures", len(fails))
    for f in fails[:10]:
        print(json.dumps(f))


if __name__ == "__main__":
    main()
