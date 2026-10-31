"""Final cross-check against the author's code in r4-switch/ (imported read-only, only here).

On random P2 instances and on planted/critical-run instances from this folder's generators:
  - sw.shortest_valid_paths (author) = core.shortest_valid_paths (own): same length and same set of paths;
  - sw.brute (author) = core.brute_force (own) on instances with at most 11 switches;
  - prove.certificate (author) runs without assertion error on every shortest path; its storage is recorded;
  - tsearch.admissible_search (author) and core.search5 (own) agree (accept / reject) on random (K, B).

usage: python crosscheck.py seed count
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = os.path.normpath(os.path.join(HERE, '..', '..', 'r4-switch'))
sys.path.append(AUTHOR)

import sw as asw            # noqa: E402  (author)
import prove as aprove      # noqa: E402  (author)
import tsearch as ats       # noqa: E402  (author)

from core import random_instance, p2_repair, shortest_valid_paths, brute_force, search5  # noqa: E402
from gen_run import gen_run  # noqa: E402
from planted import is_shortest  # noqa: E402
from proof import check_path, ClaimFailure  # noqa: E402


def to_author(inst):
    E = [sum(1 << x for x in e) for e, _ in inst.sw]
    F = [sum(1 << x for x in f) for _, f in inst.sw]
    return (inst.N, E, F, inst.s, inst.t)


def sid(inst, y):
    w, typ = inst.sides[y]
    return 2 * w + typ


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    tot = {"inst": 0, "paths": 0, "path_mismatch": 0, "brute_mismatch": 0, "author_cert_error": 0,
           "search_pairs": 0, "search_mismatch": 0, "own_fail": 0, "author_storage_max": 0, "own_storage_max": 0}
    for it in range(count):
        if it % 2 == 0:
            inst = random_instance(rng, rng.randint(4, 9), rng.randint(2, 8), rng.choice([0.12, 0.2, 0.3]))
            inst = p2_repair(inst, rng, fresh=rng.random() < 0.5)
        else:
            g = None
            while g is None:
                g = gen_run(rng, [rng.choice('OOT') for _ in range(rng.randint(0, 3))], rng.randint(1, 4),
                            [rng.choice('OOOT') for _ in range(rng.randint(4, 8))], pM=0.7, pB=0.2,
                            reverse=rng.random() < 0.5, two_spans=rng.random() < 0.3)
                if g is not None and not is_shortest(g[0], g[1]):
                    g = None
            inst = g[0]
        tot["inst"] += 1
        ai = to_author(inst)
        L, paths = shortest_valid_paths(inst)
        res = asw.shortest_valid_paths(ai)
        aL, apaths = (res if isinstance(res, tuple) else (None, res))
        mine = {tuple(sid(inst, y) for y in P) for P in paths}
        theirs = {tuple(p) for p in (apaths or [])}
        if mine != theirs:
            tot["path_mismatch"] += 1
        if inst.n <= 11 and (asw.brute(ai) is not None) != brute_force(inst):
            tot["brute_mismatch"] += 1
        for P in paths:
            tot["paths"] += 1
            st = {}
            try:
                check_path(inst, P, st)
                tot["own_storage_max"] = max(tot["own_storage_max"], st.get("maxB", 0))
            except ClaimFailure:
                tot["own_fail"] += 1
            try:
                _, _, stor, _ = aprove.certificate(ai, tuple(sid(inst, y) for y in P))
                tot["author_storage_max"] = max(tot["author_storage_max"], stor)
            except AssertionError:
                tot["author_cert_error"] += 1
        for _ in range(4):
            K = {y for y in range(inst.D) if rng.random() < 0.6}
            B = rng.randint(0, 6)
            mine_acc = search5(inst, K, B) is not None
            r = ats.admissible_search(ai, {sid(inst, y) for y in K}, B)
            theirs_acc = bool(r[0]) if isinstance(r, tuple) else bool(r)
            tot["search_pairs"] += 1
            if mine_acc != theirs_acc:
                tot["search_mismatch"] += 1
    print("crosscheck seed=%d count=%d" % (seed, count))
    print(json.dumps(tot))


if __name__ == "__main__":
    main()
