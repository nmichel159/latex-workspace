"""A5: the class search (r4-switch Theorem 5 with Pi(Y) = opposite-type sides of the class of Y and stored
(class, type) pairs) is sound for every K and B; and the completeness analogue: a valid path P with Pi(X) in K for
its members and at most B stored pairs is accepted.

usage: python test_a5.py SEED COUNT
Random P2 instances (and without P2), 6 random (K, B) per instance (both storage counts), plus K = union of
Pi(X) over the members X of a shortest valid path with random extra sides, B = its number of stored pairs.
"""
import json
import random
import sys

from qcore import bits
from qchecks import class_search, walk_ok
from qgen import random_instance
from qgen2 import incremental, word_of


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "runs": 0, "accepted": 0, "no_inst": 0, "compl": 0, "fail": 0}
    for it in range(count):
        if rng.random() < 0.7:
            I = random_instance(rng, rng.randint(3, 9), rng.randint(1, 9), rng.randint(1, 6),
                                rng.choice([0.2, 0.3, 0.45]), rng.choice([0.2, 0.3, 0.45]),
                                fresh=rng.random(), p2=rng.random() < 0.7)
        else:
            rr = rng.randint(4, 8)
            out = incremental(rng, rr, 3, 3, mates=1, offc=1, word=word_of(rng, rr, "blocks"))
            if out is None:
                continue
            I = out[0]
        st["inst"] += 1
        yes = I.brute()
        if not yes:
            st["no_inst"] += 1
        for _ in range(6):
            K = 0
            pK = rng.random()
            for x in I.sides:
                if rng.random() < pK:
                    K |= 1 << x
            B = rng.randint(0, 4)
            W = class_search(I, K, B, count_classes=rng.random() < 0.5)
            st["runs"] += 1
            if W is not None:
                st["accepted"] += 1
                if not walk_ok(I, W) or not yes:
                    st["fail"] += 1
                    print("SOUNDNESS FAIL", json.dumps(I.to_json()), K, B, W, flush=True)
        if yes:
            r, paths = I.shortest_paths_dfs(limit=5)
            for P in paths:
                K = 0
                for x in P:
                    K |= I.Omega[I.cl[x >> 1]][1 - (x & 1)]
                for x in I.sides:
                    if rng.random() < 0.3:
                        K |= 1 << x
                stored = {(I.cl[x >> 1], x & 1) for x in P if (K >> x) & 1}
                W = class_search(I, K, len(stored), count_classes=True)
                st["compl"] += 1
                if W is None or not walk_ok(I, W):
                    st["fail"] += 1
                    print("COMPLETENESS FAIL", json.dumps(I.to_json()), K, P, flush=True)
    print(json.dumps(st), flush=True)


if __name__ == "__main__":
    main()
