"""Adversarial hill climbing against DESC (agent r5-classes, third run).

Planted paths with classes (plant.Planted): start from a forward word structure (rigid, shortest) with random
multi-position classes; moves add/remove links among members, partners and mates, add/remove mates (switches of a
class of P that are not on P, with random P2 links to every switch of another class).  Kept: P2 and the planted
path shortest (exact).  Objective: the guided DESC cost of the planted path (fastdesc), lexicographically
(cost with f=2, g=1; cost with f=1, g=1).

usage: python hunt_desc.py SEED RUNS R KCLS STEPS [maxmates]
"""
import random
import sys
import ccore as C
import plant
import fastdesc


def start(rng, r, kcls):
    for _ in range(100):
        W = "".join(rng.choice("EF") for _ in range(r))
        if W.count("E") < 3 or W.count("F") < 3:
            continue
        typ = [0 if ch == "E" else 1 for ch in W]
        cls = [ty * 1000 + rng.randrange(kcls) for ty in typ] if kcls > 0 else list(range(r))
        # no two consecutive positions of one class
        if any(cls[a] == cls[a + 1] for a in range(r - 1)):
            continue
        pl = plant.base_word(W, cls, forward=True)
        I, P = pl.realise()
        if C.p2_ok(I) and pl.shortest_ok(I, P):
            return pl
    return None


def repair_p2(rng, q):
    for (u, v) in q.p2_pairs_missing():
        ty = rng.randrange(2)
        q.add_link(u, ty, v, ty)


def add_mate(rng, q):
    a = rng.randrange(q.r)
    cl = q.cls[a]
    m = q.add_switch(cl, mtyp=q.typ[a])
    for v in range(q.n - 1):
        if q.cls[v] != cl:
            ty = rng.randrange(2)
            q.add_link(m, ty, v, ty)
    return m


def remove_switch(q, m):
    """remove switch m (a mate, m >= r) and renumber"""
    newlinks = set()
    for (u, tu, v, tv) in q.links:
        if u == m or v == m:
            continue
        u2 = u - 1 if u > m else u
        v2 = v - 1 if v > m else v
        newlinks.add(plant.Planted.canon(u2, tu, v2, tv))
    q.links = newlinks
    del q.cls[m]
    q.n -= 1
    q.mtyp = {(k - 1 if k > m else k): t for k, t in q.mtyp.items() if k != m}


def mutate(rng, pl, maxmates):
    q = pl.copy()
    r, n = q.r, q.n
    mv = rng.random()
    if mv < 0.30:
        a, c = rng.randrange(r), rng.randrange(r)
        if a == c:
            return None
        if not q.add_link(a, 1 - q.typ[a], c, q.typ[c]):
            return None
    elif mv < 0.38:
        a, c = rng.randrange(r), rng.randrange(r)
        if abs(a - c) < 2:
            return None
        if not q.add_link(a, 1 - q.typ[a], c, 1 - q.typ[c]):
            return None
    elif mv < 0.62:
        cand = [L for L in q.links if L not in q.struct]
        if not cand:
            return None
        q.remove_link(rng.choice(cand))
        repair_p2(rng, q)
    elif mv < 0.72:
        if n - r >= maxmates:
            return None
        add_mate(rng, q)
    elif mv < 0.77:
        if n == r:
            return None
        remove_switch(q, rng.randrange(r, n))
    else:
        if n == r:
            return None
        m = rng.randrange(r, n)
        v = rng.randrange(n)
        if v == m:
            return None
        if not q.add_link(m, rng.randrange(2), v, rng.randrange(2)):
            return None
    return q


def evaluate(q):
    I, P = q.realise()
    if not C.p2_ok(I):
        return None, I, P
    if not q.shortest_ok(I, P):
        return None, I, P
    pr = fastdesc.Prep(I, P)
    return (pr.guided(2, 1), pr.guided(1, 1)), I, P


def hill(seed, r, kcls, steps, maxmates, log=None):
    rng = random.Random(seed)
    pl = start(rng, r, kcls)
    if pl is None:
        return None
    best, I, P = evaluate(pl)
    for it in range(steps):
        q = mutate(rng, pl, maxmates)
        if q is None:
            continue
        sc, I2, P2_ = evaluate(q)
        if sc is None or sc < best:
            continue
        pl, best = q, sc
        if log and it % 200 == 0:
            print("   it", it, best, "mates", pl.n - pl.r, flush=True)
    return pl, best


if __name__ == "__main__":
    seed, runs, r, kcls, steps = (int(x) for x in sys.argv[1:6])
    maxmates = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    hist = {}
    top = None
    for i in range(runs):
        res = hill(seed * 1000 + i, r, kcls, steps, maxmates, log=True)
        if res is None:
            print("run", i, "start failed", flush=True)
            continue
        pl, best = res
        hist[best] = hist.get(best, 0) + 1
        print("run", i, "cost", best, "mates", pl.n - pl.r, "types", "".join("EF"[x] for x in pl.typ),
              "cls", pl.cls, flush=True)
        if top is None or best > top[0]:
            top = (best, pl.typ, pl.cls, sorted(pl.links))
    print("histogram:", hist)
    print("top:", top)
