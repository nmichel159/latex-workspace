"""Self-test of core.py: the path solver against brute force on random instances (with and without P2), the search
of Theorem 5 with K = all sides and B = D against brute force, and validity of every returned walk.

usage: python selftest.py seed count
"""
import sys
import random
from core import random_instance, p2_repair, p2, brute_force, shortest_valid_paths, search5, is_valid_walk, \
    is_valid_path


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    stats = {"inst": 0, "yes": 0, "p2": 0, "fail": 0}
    for it in range(count):
        N = rng.randint(3, 8)
        n = rng.randint(1, 8)
        inst = random_instance(rng, N, n, rng.choice([0.15, 0.25, 0.4]))
        if rng.random() < 0.6:
            inst = p2_repair(inst, rng, fresh=rng.random() < 0.5)
        stats["inst"] += 1
        stats["p2"] += p2(inst)
        bf = brute_force(inst)
        L, paths = shortest_valid_paths(inst)
        if (L is not None) != bf:
            stats["fail"] += 1
            print("mismatch path solver", inst.to_json())
        for P in paths:
            if not is_valid_path(inst, P) or len(P) != L:
                stats["fail"] += 1
                print("bad path", inst.to_json(), P)
        W = search5(inst, set(range(inst.D)), inst.D)
        if (W is not None) != bf:
            stats["fail"] += 1
            print("mismatch full search", inst.to_json())
        if W is not None and not is_valid_walk(inst, W):
            stats["fail"] += 1
            print("invalid walk", inst.to_json(), W)
        stats["yes"] += bf
        # random K: accepted walks must be valid
        for _ in range(5):
            K = {y for y in range(inst.D) if rng.random() < 0.5}
            B = rng.randint(0, inst.D)
            W = search5(inst, K, B)
            if W is not None and not is_valid_walk(inst, W):
                stats["fail"] += 1
                print("invalid walk random K", inst.to_json(), W)
            if W is not None and not bf:
                stats["fail"] += 1
                print("accepted no-instance", inst.to_json(), sorted(K), B)
    print(stats)


if __name__ == "__main__":
    main()
