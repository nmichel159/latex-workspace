"""Proof steps on random 2CH + P2 instances (random sides, P2 repaired with existing or private nodes).

usage: python test_random.py seed count [maxN] [maxn]
"""
import sys
import json
import random
from core import random_instance, p2_repair, p2, brute_force, shortest_valid_paths, search5
from proof import check_path, ClaimFailure


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    maxN = int(sys.argv[3]) if len(sys.argv) > 3 else 9
    maxn = int(sys.argv[4]) if len(sys.argv) > 4 else 9
    rng = random.Random(seed)
    tot = {"inst": 0, "yes": 0, "no": 0, "paths": 0, "fail": 0, "maxr": 0}
    stats = {}
    for it in range(count):
        N = rng.randint(4, maxN)
        n = rng.randint(2, maxn)
        inst = random_instance(rng, N, n, rng.choice([0.12, 0.2, 0.3]))
        inst = p2_repair(inst, rng, fresh=rng.random() < 0.5)
        assert p2(inst)
        tot["inst"] += 1
        L, paths = shortest_valid_paths(inst, limit=200)
        if n <= 12:
            assert (L is not None) == brute_force(inst)
        if L is None:
            tot["no"] += 1
            for _ in range(4):
                K = {y for y in range(inst.D) if rng.random() < 0.6}
                if search5(inst, K, rng.randint(0, inst.D)) is not None:
                    tot["fail"] += 1
                    print("accepted no-instance", json.dumps(inst.to_json()))
            continue
        tot["yes"] += 1
        tot["maxr"] = max(tot["maxr"], L)
        for P in paths:
            tot["paths"] += 1
            try:
                check_path(inst, P, stats)
            except ClaimFailure as e:
                tot["fail"] += 1
                print("FAIL", e.args[0], json.dumps(inst.to_json()), list(P))
    print(json.dumps(tot))
    print(json.dumps(stats, sort_keys=True))


if __name__ == "__main__":
    main()
