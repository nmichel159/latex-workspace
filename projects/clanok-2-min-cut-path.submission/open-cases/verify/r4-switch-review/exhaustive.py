"""Exhaustive check on all 2CH + P2 instances with N nodes (s = 0, t = 1) and n switches (multisets of switches,
each side any subset of the nodes, including empty).

For each P2 instance: brute force (mode vectors) = existence of a valid path (own path search); every shortest
valid path is passed to proof.check_path (all claims, certificate of Corollary 9 accepted by the search); on
no-instances the search of Theorem 5 is run with several sets K (all K when D <= 6) and must reject; on a sample of
yes-instances the algorithm alg.decide is run with the parameters of the proof's certificate and must accept.

usage: python exhaustive.py N n [workers] [decide_every]
"""
import sys
import json
import random
from itertools import combinations_with_replacement
from multiprocessing import Pool

from core import Inst, brute_force, shortest_valid_paths, search5, is_valid_walk
from proof import check_path, ClaimFailure
from alg import decide


def masks_to_sets(N, code):
    M = 1 << N
    E, F = code % M, code // M
    return ({x for x in range(N) if E >> x & 1}, {x for x in range(N) if F >> x & 1})


def p2_codes(N, codes):
    M = 1 << N
    for i in range(len(codes)):
        Ei, Fi = codes[i] % M, codes[i] // M
        for j in range(i + 1, len(codes)):
            Ej, Fj = codes[j] % M, codes[j] // M
            if not (Ei & Ej) and not (Fi & Fj):
                return False
    return True


def work(args):
    N, n, first, decide_every = args
    M = 4 ** N
    rng = random.Random(1000 * N + 17 * n + first)
    st = {"inst": 0, "p2": 0, "yes": 0, "no": 0, "paths": 0, "fail": [], "soundK": 0, "decide": 0}
    stats = {}
    for rest in combinations_with_replacement(range(first, M), n - 1):
        codes = (first,) + rest
        st["inst"] += 1
        if not p2_codes(N, codes):
            continue
        st["p2"] += 1
        inst = Inst(N, 0, 1, [masks_to_sets(N, c) for c in codes])
        ans = brute_force(inst)
        L, paths = shortest_valid_paths(inst)
        if (L is not None) != ans:
            st["fail"].append(("solver mismatch", inst.to_json()))
            continue
        if not ans:
            st["no"] += 1
            D = inst.D
            if D <= 6:
                Ks = [frozenset(y for y in range(D) if m >> y & 1) for m in range(1 << D)]
                Bs = [0, 1, 2, D]
            else:
                Ks = [frozenset(y for y in range(D) if rng.random() < 0.5) for _ in range(6)] + [frozenset(range(D))]
                Bs = [1, D]
            for K in Ks:
                for B in Bs:
                    st["soundK"] += 1
                    if search5(inst, K, B) is not None:
                        st["fail"].append(("search accepted a no-instance", inst.to_json(), sorted(K), B))
            continue
        st["yes"] += 1
        need_params = None
        for P in paths:
            st["paths"] += 1
            try:
                out = check_path(inst, P, stats)
            except ClaimFailure as e:
                st["fail"].append(("claim", str(e.args[0]), inst.to_json(), list(P)))
                continue
            c9 = out["cor9"]
            if c9[0] == "swap":
                prm = (1, 2, c9[1])
            else:
                prm = (max(c9[2], c9[4]), max(c9[3], c9[5]), c9[1])
            if need_params is None:
                need_params = prm
        if decide_every and need_params and st["yes"] % decide_every == 0:
            st["decide"] += 1
            kd, ks, B = need_params
            if not decide(inst, kd, ks, B):
                st["fail"].append(("decide rejected yes-instance at proof parameters", inst.to_json(), need_params))
    return st, stats


def main():
    N, n = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    decide_every = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    M = 4 ** N
    tasks = [(N, n, f, decide_every) for f in range(M)]
    tot = {"inst": 0, "p2": 0, "yes": 0, "no": 0, "paths": 0, "soundK": 0, "decide": 0}
    fails = []
    agg = {}
    with Pool(workers) as pool:
        for st, stats in pool.imap_unordered(work, tasks, chunksize=1):
            for k in tot:
                tot[k] += st[k]
            fails += st["fail"]
            for k, v in stats.items():
                if k.startswith("max"):
                    agg[k] = max(agg.get(k, 0), v)
                else:
                    agg[k] = agg.get(k, 0) + v
    print("exhaustive N=%d n=%d" % (N, n))
    print("counts", json.dumps(tot))
    print("proof stats", json.dumps(agg, sort_keys=True))
    print("failures", len(fails))
    for f in fails[:20]:
        print(json.dumps(f))


if __name__ == "__main__":
    main()
