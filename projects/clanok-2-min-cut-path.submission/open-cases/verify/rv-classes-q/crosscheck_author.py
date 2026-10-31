"""Cross-check with the author's code (r5-classes/ccore.py, imported read-only; the only script of this review that
imports r5-classes/): brute force, the sets of all shortest valid paths, P2, and the class search of A5.

usage: python crosscheck_author.py SEED COUNT
Random instances with classes (70% with P2 repair) and planted incremental instances; asserted: same P2 verdict,
same yes/no, same shortest length and the same set of shortest valid paths (limit 200), and for 4 random (K, B):
both searches accept or both reject (same admissibility rule: stored (class, type) pairs, at most B of them).
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "..", "r5-classes"))

from qcore import Inst  # noqa: E402
from qchecks import class_search, walk_ok  # noqa: E402
from qgen import random_instance  # noqa: E402
from qgen2 import incremental, word_of  # noqa: E402
import ccore  # noqa: E402  (r5-classes/ccore.py, the author's code)


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "p2": 0, "yes": 0, "paths": 0, "search": 0, "mismatch": 0}
    for it in range(count):
        if rng.random() < 0.8:
            I = random_instance(rng, rng.randint(3, 9), rng.randint(1, 9), rng.randint(1, 7),
                                rng.choice([0.2, 0.3, 0.45]), rng.choice([0.2, 0.3, 0.45]),
                                fresh=rng.random(), p2=rng.random() < 0.7)
        else:
            rr = rng.randint(4, 9)
            out = incremental(rng, rr, 3, 3, mates=1, offc=1, word=word_of(rng, rr, "blocks"))
            if out is None:
                continue
            I = out[0]
        A = ccore.Inst(I.N, I.s, I.t, [(E, F) for E, F in I.sw], list(I.cl))
        st["inst"] += 1
        mism = []
        if I.p2() != ccore.p2_ok(A):
            mism.append("p2")
        st["p2"] += I.p2()
        yes = I.brute()
        if yes != (ccore.brute(A) is not None):
            mism.append("brute")
        r1, P1 = I.shortest_paths_dfs(limit=200)
        r2, P2 = ccore.shortest_valid_paths(A, limit=200)
        if r1 != r2:
            mism.append(("length", r1, r2))
        elif r1 is not None and len(P1) < 200 and len(P2) < 200 and sorted(P1) != sorted(map(tuple, P2)):
            mism.append("path sets")
        if yes:
            st["yes"] += 1
            st["paths"] += len(P1)
        for _ in range(4):
            K = 0
            pK = rng.random()
            for x in I.sides:
                if rng.random() < pK:
                    K |= 1 << x
            B = rng.randint(0, 4)
            W1 = class_search(I, K, B, count_classes=True)
            W2 = ccore.csearch(A, [x for x in I.sides if (K >> x) & 1], B)
            st["search"] += 1
            if (W1 is None) != (W2 is None):
                mism.append(("search", K, B))
            if W1 is not None and not walk_ok(I, W1):
                mism.append("own walk invalid")
            if W2 is not None and not walk_ok(I, list(W2)):
                mism.append("author walk invalid")
        if mism:
            st["mismatch"] += 1
            print("MISMATCH", mism, json.dumps(I.to_json()), flush=True)
    print(json.dumps(st), flush=True)


if __name__ == "__main__":
    main()
