"""Adversarial hill climbing against the proof of Theorem 8.2 (r5-core.md Section 8.4).

usage: python hill_inter.py SEED RESTARTS STEPS NMIN NMAX
State: a rigid word W = (EF)^n, sets S_i (E-positions below x_i), T_j (F-positions above y_j), the probability
p_xy and the witness options of rgen.rdesign, and the generator seed.  Mutations: add/remove an element of some S_i
or T_j, add/remove an x or a y, change an option or the seed.  Objective (maximised) on the shortest valid paths
(at most 4): (largest number of levels used by inter.levels in ILP or sample mode, largest kappa of the bad pairs,
number of paths without a single term of the proof's kind).  Every evaluated path is checked by inter.levels
(every claim of the proof); a failure is printed with the state and counted.
"""
import sys
import random
import time
from collections import Counter
import gstar
import inter
from rgen import rdesign


def build(st):
    rng = random.Random(st["gseed"])
    return rdesign(rng, st["W"], st["S"], st["T"], p_xy=st["pxy"], p_low=st["plow"], p_up=st["pup"],
                   p_contact=st["pc"])


def evaluate(st, cnt):
    G = build(st)
    if G.p2_bad():
        cnt["P2 FAILS"] += 1
        return None
    Lsh, _ = G.shortest()
    if not Lsh:
        return None
    St = gstar.Stars(G)
    best = (0, 0, 0)
    lev_max, kap_max, nos = 0, 0, 0
    for P in G.all_shortest(limit=4, length=Lsh):
        K = gstar.Skel(G, P)
        for mode in ("ilp", "sample"):
            res = inter.levels(G, P, St, K, rng=random.Random(st["gseed"] + 7) if mode == "sample" else None)
            cnt["paths checked"] += 1
            if res["errors"]:
                cnt["ERRORS"] += 1
                print("ERROR %s state=%s %s" % (mode, st, res["errors"][:3]), flush=True)
            lev_max = max(lev_max, res["nlev"])
        _, cl = gstar.classify(G, P, St, K)
        kap_max = max(kap_max, gstar.min_vertex_cover_bip(cl["bad"]) if cl["bad"] else 0)
        ms = inter.min_single(G, P, St, K)
        nos += not (ms["edmg"] == 0 or ms["fone"])
    return (lev_max, kap_max, nos)


def mutate(rng, st, Epos, Fpos):
    s = dict(st)
    s["S"] = [list(x) for x in st["S"]]
    s["T"] = [list(x) for x in st["T"]]
    r = rng.random()
    if r < 0.3 and s["S"]:
        S = rng.choice(s["S"])
        a = rng.choice(Epos)
        if a in S and len(S) > 1:
            S.remove(a)
        elif a not in S:
            S.append(a)
    elif r < 0.6 and s["T"]:
        T = rng.choice(s["T"])
        b = rng.choice(Fpos)
        if b in T and len(T) > 1:
            T.remove(b)
        elif b not in T:
            T.append(b)
    elif r < 0.7:
        if rng.random() < 0.5 and len(s["S"]) < 8:
            s["S"].append(rng.sample(Epos, 1))
        elif len(s["S"]) > 1:
            s["S"].pop(rng.randrange(len(s["S"])))
    elif r < 0.8:
        if rng.random() < 0.5 and len(s["T"]) < 8:
            s["T"].append(rng.sample(Fpos, 1))
        elif len(s["T"]) > 1:
            s["T"].pop(rng.randrange(len(s["T"])))
    elif r < 0.9:
        key = rng.choice(["pxy", "plow", "pup", "pc"])
        s[key] = rng.choice([0.0, 0.3, 0.5, 0.7, 1.0])
    else:
        s["gseed"] = rng.randrange(10 ** 6)
    return s


def main():
    seed, restarts, steps, nmin, nmax = (int(a) for a in sys.argv[1:6])
    rng = random.Random(seed)
    cnt = Counter()
    t0 = time.time()
    overall = None
    for rs in range(restarts):
        n = rng.randint(nmin, nmax)
        W = "EF" * n
        Epos = [p for p in range(1, 2 * n + 1) if W[p - 1] == "E"]
        Fpos = [p for p in range(1, 2 * n + 1) if W[p - 1] == "F"]
        st = dict(W=W, S=[rng.sample(Epos, rng.randint(1, 2)) for _ in range(rng.randint(2, 5))],
                  T=[rng.sample(Fpos, rng.randint(1, 2)) for _ in range(rng.randint(2, 5))],
                  pxy=1.0, plow=0.5, pup=0.5, pc=0.0, gseed=rng.randrange(10 ** 6))
        val = evaluate(st, cnt)
        while val is None:
            st["gseed"] = rng.randrange(10 ** 6)
            val = evaluate(st, cnt)
        for step in range(steps):
            s2 = mutate(rng, st, Epos, Fpos)
            v2 = evaluate(s2, cnt)
            cnt["evaluations"] += 1
            if v2 is not None and v2 >= val:
                st, val = s2, v2
        cnt["restarts"] += 1
        print("restart %d n=%d best (levels, kappa, paths without single proof-term) = %s (%.0fs)" % (
            rs, n, val, time.time() - t0), flush=True)
        if overall is None or val > overall[0]:
            overall = (val, st)
    print("hill_inter seed %d restarts %d steps %d n %d-%d (%.0fs)" % (seed, restarts, steps, nmin, nmax,
                                                                     time.time() - t0))
    for kk in sorted(cnt):
        print("  %-25s %s" % (kk, cnt[kk]))
    print("  best overall:", overall[0])
    print("  state:", overall[1])


if __name__ == "__main__":
    main()
