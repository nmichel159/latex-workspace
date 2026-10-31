"""Adversarial hill climbing against Theorem Q (and Lemma PP): mutate a planted instance while P2 holds and the
planted path P stays a shortest valid path, maximising an objective on P; every visited accepted instance is
checked with the full proof construction (both types) and Lemma PP on all its shortest valid paths (limit).

usage: python hunt_q.py SEED STEPS START OBJ [start params key=value]
START = band | inc;  OBJ = h (largest number of centres used by the proof, over both types), full (least number
of centres any cover needs, min over the two games, max over the types), phi (largest |Phi| / 3h ratio, then |Phi|),
err (least |Err(u, b)| of Lemma PP over the pairs, max over the types).
Mutations: a fresh node in two random sides (any types), a random existing node added to a random side, a random
non-terminal node removed from a random side (rejected if P2 fails), a P2 pair re-oriented.
"""
import json
import random
import sys
import time

from qcore import Inst, bits, kq
from qchecks import ClaimFailure, check_basic, check_theorem_q, full_covers, check_pp
from qgen2 import band, incremental, word_of, no_shorter


def objective(I, P, obj, st):
    P = list(P)
    if obj == "h":
        return max(check_theorem_q(I, P, T, st)["h"] for T in (0, 1))
    if obj == "phi":
        best = 0.0
        for T in (0, 1):
            o = check_theorem_q(I, P, T, st)
            if o["h"]:
                best = max(best, o["phi"] / (3.0 * o["h"]) + 0.001 * o["phi"])
        return best
    if obj == "full":
        vals = []
        for T in (0, 1):
            hO, hT = full_covers(I, P, T)
            vals.append(min(x for x in (hO, hT, 99) if x is not None))
        return max(v for v in vals if v < 99) if any(v < 99 for v in vals) else 0
    if obj == "err":
        vals = [check_pp(I, P, T, st) for T in (0, 1)]
        vals = [v for v in vals if v is not None]
        return max(vals) if vals else 0
    raise ValueError(obj)


def full_check(I, st, plim=20):
    r, paths = I.shortest_paths_dfs(limit=plim)
    for Q in paths:
        Q = list(Q)
        check_basic(I, Q, st)
        for T in (0, 1):
            o = check_theorem_q(I, Q, T, st)
            st["hmax"] = max(st.get("hmax", 0), o["h"])
            st["phimax"] = max(st.get("phimax", 0), o["phi"])
            check_pp(I, Q, T, st, maxpairs=20)
    st["checked"] = st.get("checked", 0) + 1


def main():
    seed, steps, start, obj = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    par = {"r": 10, "nTc": 3, "nOc": 3, "mT": 6, "mO": 6, "mates": 1, "offc": 0}
    for kv in sys.argv[5:]:
        k, v = kv.split("=")
        par[k] = int(v)
    rng = random.Random(seed)
    while True:
        if start == "band":
            lam = max(1, par["r"] // 2 - 1)
            I, P, _ = band(rng, par["r"], lam, par["nTc"], par["nOc"], par["mT"], par["mO"], offc=par["offc"])
        else:
            out = incremental(rng, par["r"], par["nTc"], par["nOc"], mates=par["mates"], offc=par["offc"],
                              word=word_of(rng, par["r"], "blocks"))
            if out is None:
                continue
            I, P = out
        if no_shorter(I, len(P)) and I.is_valid_path(list(P)):
            break
    N, sw, cl = I.N, [list(x) for x in I.sw], list(I.cl)
    r = len(P)
    st = {}
    cur = objective(I, P, obj, st)
    best = cur
    t0 = time.time()
    acc = 0
    for step in range(steps):
        N2, sw2 = N, [list(x) for x in sw]
        mv = rng.random()
        n = len(sw2)
        if mv < 0.4:
            a, b = rng.sample(range(2 * n), 2)
            x = N2
            N2 += 1
            sw2[a >> 1][a & 1] |= 1 << x
            sw2[b >> 1][b & 1] |= 1 << x
        elif mv < 0.6:
            a = rng.randrange(2 * n)
            x = rng.randrange(2, N2)
            sw2[a >> 1][a & 1] |= 1 << x
        elif mv < 0.9:
            a = rng.randrange(2 * n)
            nodes = [x for x in bits(sw2[a >> 1][a & 1]) if x not in (0, 1)]
            if not nodes:
                continue
            x = rng.choice(nodes)
            sw2[a >> 1][a & 1] &= ~(1 << x)
        else:
            w, v = rng.sample(range(n), 2)
            if cl[w] == cl[v]:
                continue
            for ty in (0, 1):
                common = bits(sw2[w][ty] & sw2[v][ty])
                for x in common:
                    if x not in (0, 1):
                        sw2[w][ty] &= ~(1 << x)
            x = N2
            N2 += 1
            ty = rng.randrange(2)
            sw2[w][ty] |= 1 << x
            sw2[v][ty] |= 1 << x
        J = Inst(N2, 0, 1, sw2, cl)
        if not J.p2() or not J.is_valid_path(list(P)) or not no_shorter(J, r):
            continue
        try:
            val = objective(J, P, obj, st)
        except ClaimFailure as ex:
            print("FAIL in objective", repr(ex), json.dumps(J.to_json()), list(P), flush=True)
            return
        if val >= cur:
            N, sw = N2, sw2
            cur = val
            acc += 1
            if val > best:
                best = val
                try:
                    full_check(J, st)
                except ClaimFailure as ex:
                    print("FAIL", repr(ex), json.dumps(J.to_json()), list(P), flush=True)
                    return
                print("step %d best %s n=%d c=%d k=%d N=%d t=%.0fs" % (step, best, J.n, J.c, kq(J.n), J.N,
                                                                       time.time() - t0), flush=True)
    J = Inst(N, 0, 1, sw, cl)
    full_check(J, st)
    print("final best", best, "accepted moves", acc, "stats", json.dumps(st, sort_keys=True), flush=True)
    print("instance", json.dumps(J.to_json()), "P", list(P), flush=True)


if __name__ == "__main__":
    main()
