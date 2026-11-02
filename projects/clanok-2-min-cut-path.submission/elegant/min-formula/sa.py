"""Adversarial search for instances with a large least formula.
Usage: sa.py SEED SECONDS RMIN RMAX LOG [STRICT_ATOMS=1] [START.json]
Score: 100 * free cost + pureF + pureE (free cost exact up to the cap of the front).  Moves: gen.mutate, insertion and deletion of a core element.
P stays a shortest walk (exact solver), P2 holds by construction and is asserted.  The best design goes to LOG.best.json.
"""
import json
import math
import random
import sys
import time

from gen import Abs, dump_json, mutate, rand_abs
from mf_core import Measure


def evaluate(d, strict_atoms=True, cap=400, budget=60000, maxcost=12):
    I, P = d.build()
    if not I.p2():
        return None
    try:
        if I.shortest_walk(bound=len(P) - 1, budget=budget) is not None:
            return None
    except Exception:
        return None
    M = Measure(I, P, strict_atoms=strict_atoms)
    rf, re = M.pure()
    fr = M.free(maxcost=maxcost, cap=cap)
    cost = fr["cost"] if fr["cost"] is not None else maxcost + 1
    pf = rf[0] if rf[0] is not None else 21
    pe = re[0] if re[0] is not None else 21
    return dict(score=100 * cost + pf + pe, cost=cost, pf=pf, pe=pe, exact=fr["exact"], tree=M.fmt(fr["tree"]) if fr["tree"] else None, nb=M.nb, na=M.na, m=I.m, q=len(P) - 1)


def structural(d, rng):
    """Insert or delete a core element."""
    r = len(d.word)
    if rng.random() < 0.5 and r < 40:
        p = rng.randint(0, r)
        t = rng.choice("EF")
        mp = lambda x: x + 1 if x >= p else x
        nd = Abs(d.word[:p] + [t] + d.word[p:])
        cls = [c + 1 for c in d.cls]
        nd.cls = cls[:p] + [0] + cls[p:]
        nd.strict = {(x + 1, y + 1) for x, y in d.strict}
        nd.mA = {(mp(x), mp(y)) for x, y in d.mA}
        nd.mB = {(mp(x), mp(y)) for x, y in d.mB}
        if t == "E":
            for f in nd.F():
                c = rng.random()
                if c < 0.3:
                    nd.strict.add((nd.cls[f], nd.cls[p]))
                elif c < 0.65:
                    nd.mA.add((p, f))
                else:
                    nd.mB.add((f, p))
        else:
            for e in nd.E():
                c = rng.random()
                if c < 0.3:
                    nd.strict.add((nd.cls[p], nd.cls[e]))
                elif c < 0.65:
                    nd.mA.add((e, p))
                else:
                    nd.mB.add((p, e))
        return nd
    if r <= 6:
        return None
    p = rng.randrange(r)
    mp = lambda x: x - 1 if x > p else x
    nd = Abs(d.word[:p] + d.word[p + 1:])
    nd.cls = d.cls[:p] + d.cls[p + 1:]
    nd.strict = set(d.strict)
    nd.mA = {(mp(x), mp(y)) for x, y in d.mA if x != p and y != p}
    nd.mB = {(mp(x), mp(y)) for x, y in d.mB if x != p and y != p}
    return nd


def main():
    seed, secs, rmin, rmax, log = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    strict_atoms = (len(sys.argv) <= 6 or sys.argv[6] != "0")
    start = sys.argv[7] if len(sys.argv) > 7 else None
    rng = random.Random(seed)
    t0 = time.time()
    best = None
    bestd = None
    hist = {}
    lg = open(log, "w", encoding="utf-8")
    iters = 0
    while time.time() - t0 < secs:
        # restart
        if start:
            d = Abs.from_json(json.load(open(start, encoding="utf-8")))
        else:
            for _ in range(2000):
                d = rand_abs(rng, r=rng.randint(rmin, rmax), pstrict=rng.choice([0.2, 0.4, 0.6, 0.8]), pA=rng.choice([0.3, 0.5, 0.7]))
                ev = evaluate(d, strict_atoms)
                if ev is not None:
                    break
            else:
                continue
        ev = evaluate(d, strict_atoms)
        if ev is None:
            continue
        cur, curev = d, ev
        T = 30.0
        stall = 0
        while time.time() - t0 < secs and stall < 3000:
            iters += 1
            T = max(2.0, T * 0.9995)
            if rng.random() < 0.08:
                d2 = structural(cur, rng)
                if d2 is None or len(d2.word) > rmax + 10:
                    continue
            else:
                d2 = cur.copy()
                for _ in range(rng.choice([1, 1, 1, 2, 3])):
                    mutate(d2, rng)
            ev2 = evaluate(d2, strict_atoms)
            if ev2 is None:
                stall += 1
                continue
            dl = ev2["score"] - curev["score"]
            if dl >= 0 or rng.random() < math.exp(dl / T):
                cur, curev = d2, ev2
            if best is None or ev2["score"] > best["score"]:
                best, bestd = ev2, d2.copy()
                stall = 0
                print("t %.0f it %d best" % (time.time() - t0, iters), {k: best[k] for k in best}, "word", "".join(bestd.word), "classes", len(set(bestd.cls)), file=lg, flush=True)
                dump_json(bestd, log + ".best.json", **{k: best[k] for k in best})
            else:
                stall += 1
            hist[ev2["cost"]] = hist.get(ev2["cost"], 0) + 1
        print("t %.0f restart it %d hist %s" % (time.time() - t0, iters, sorted(hist.items())), file=lg, flush=True)
    print("end it", iters, "hist", sorted(hist.items()), file=lg, flush=True)


if __name__ == "__main__":
    main()
