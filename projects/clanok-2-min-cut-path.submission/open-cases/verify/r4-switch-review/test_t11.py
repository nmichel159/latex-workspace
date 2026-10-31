"""Soundness of the search with declarations (Theorem 11 of r4-switch.md), own implementation.

State (Y, St, Dc).  Y may be appended iff Y not in Dc, partner(Y) not in St, and partner(Y) empty, or in K, or in Dc,
or (Y not in K and |Dc| < s; then partner(Y) is added to Dc).  If Y in K it is added to St (|St| <= B).
Both readings of the rule are tested: 'lazy' declares only when no other alternative applies, 'eager' declares
whenever Y not in K and |Dc| < s (even if partner(Y) is in K or already in Dc).
Every accepted walk must be a valid walk, and no-instances must be rejected.

usage: python test_t11.py seed count
"""
import sys
import json
import random
from collections import deque
from core import random_instance, p2_repair, brute_force, is_valid_walk


def search11(inst, K, B, s, eager=False):
    K = frozenset(K)
    par = {}
    q = deque()

    def moves(y, St, Dc):
        out = []
        if y in Dc:
            return out
        p = inst.partner[y]
        if p is not None and p in St:
            return out
        nSt = St | {y} if y in K else St
        if len(nSt) > B:
            return out
        plain = p is None or p in K or p in Dc
        if plain and not (eager and y not in K and len(Dc) < s and p is not None):
            out.append((y, nSt, Dc))
        if p is not None and y not in K and len(Dc) < s and (eager or not plain):
            out.append((y, nSt, Dc | {p}))
        if eager and plain and p is not None and y not in K and len(Dc) < s:
            out.append((y, nSt, Dc))
        return out

    for y in range(inst.D):
        if inst.has_s[y]:
            for st in moves(y, frozenset(), frozenset()):
                if st not in par:
                    par[st] = None
                    q.append(st)
    while q:
        st = q.popleft()
        y, St, Dc = st
        if inst.has_t[y]:
            walk = []
            cur = st
            while cur is not None:
                walk.append(cur[0])
                cur = par[cur]
            return walk[::-1]
        for z in [y] + inst.nbrs[y]:
            for nst in moves(z, St, Dc):
                if nst not in par:
                    par[nst] = st
                    q.append(nst)
    return None


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    tot = {"inst": 0, "no": 0, "runs": 0, "accepted": 0, "fail": 0}
    for _ in range(count):
        inst = random_instance(rng, rng.randint(4, 8), rng.randint(2, 7), rng.choice([0.15, 0.25, 0.35]))
        if rng.random() < 0.7:
            inst = p2_repair(inst, rng, fresh=rng.random() < 0.5)
        bf = brute_force(inst)
        tot["inst"] += 1
        tot["no"] += (not bf)
        for _ in range(6):
            K = {y for y in range(inst.D) if rng.random() < rng.choice([0.2, 0.5, 0.8])}
            B, s = rng.randint(0, 4), rng.randint(0, 4)
            for eager in (False, True):
                tot["runs"] += 1
                W = search11(inst, K, B, s, eager)
                if W is not None:
                    tot["accepted"] += 1
                    if not is_valid_walk(inst, W) or not bf:
                        tot["fail"] += 1
                        print("FAIL", json.dumps(inst.to_json()), sorted(K), B, s, eager, W)
    print("test_t11 seed=%d count=%d" % (seed, count))
    print(json.dumps(tot))


if __name__ == "__main__":
    main()
