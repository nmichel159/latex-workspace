"""Adversarial hill climbing against Hypothesis H2 (agent r5-classes, third run).

H2: in a shortest valid path some type T has two T-members u, b of different classes, |u - b| >= 3, with
|err(u) | err(b)| small (costs.h2).  Hill climbing on planted paths (plant.Planted) with singleton or given classes:
moves add or remove links (partner -> member contacts, partner-partner links), keeping P2 and the planted path
shortest (exact check); objective: maximise costs.h2, then the least |f|.

usage: python hunt_h2.py SEED RUNS R STEPS [KCLS] [log]
  KCLS = 0: singleton classes (switch model); KCLS = k > 0: positions get random classes among k per type.
"""
import random
import sys
import ccore as C
import plant
import costs


def random_classes(rng, typ, k):
    if k <= 0:
        return list(range(len(typ)))
    cls = []
    for ty in typ:
        cls.append(ty * 1000 + rng.randrange(k))
    return cls


PRAND = 0.2


def start(rng, r, kcls):
    for _ in range(200):
        W = "".join(rng.choice("EF") for _ in range(r))
        if abs(W.count("E") - W.count("F")) > max(2, r // 4):
            continue
        typ = [0 if ch == "E" else 1 for ch in W]
        cls = random_classes(rng, typ, kcls)
        pl = plant.base_word(W, cls, forward=True)
        # randomise directions of opposite-type pairs (only with probability 0.2 per pair)
        for L in list(pl.links):
            if rng.random() > PRAND:
                continue
            u, tu, v, tv = L
            if L in pl.struct:
                continue
            if pl.typ[u] != pl.typ[v] and rng.random() < 0.5:
                # replace X'_u ∩ X_v by X_u ∩ X'_v (or conversely)
                pl.remove_link(L)
                if tu == 1 - pl.typ[u]:
                    pl.add_link(u, pl.typ[u], v, 1 - pl.typ[v])
                else:
                    pl.add_link(u, 1 - pl.typ[u], v, pl.typ[v])
        I, P = pl.realise()
        if C.p2_ok(I) and pl.shortest_ok(I, P):
            return pl
    return None


def score(pl):
    I, P = pl.realise()
    fs = costs.f_sets(I, P)
    return (costs.h2(I, P), min(len(x) for x in fs), sum(len(x) for x in fs)), I, P


def mutate(rng, pl):
    q = pl.copy()
    r = q.r
    mv = rng.random()
    if mv < 0.45:
        a, c = rng.randrange(r), rng.randrange(r)
        if a == c:
            return None
        if not q.add_link(a, 1 - q.typ[a], c, q.typ[c]):
            return None
    elif mv < 0.6:
        a, c = rng.randrange(r), rng.randrange(r)
        if abs(a - c) < 2:
            return None
        if not q.add_link(a, 1 - q.typ[a], c, 1 - q.typ[c]):
            return None
    else:
        cand = [L for L in q.links if L not in q.struct]
        if not cand:
            return None
        L = rng.choice(cand)
        q.remove_link(L)
        miss = q.p2_pairs_missing()
        for (u, v) in miss:
            # repair with the other orientation of an opposite-type pair, or a partner-partner link
            if q.typ[u] != q.typ[v]:
                if rng.random() < 0.5:
                    q.add_link(u, 1 - q.typ[u], v, q.typ[v])
                else:
                    q.add_link(v, 1 - q.typ[v], u, q.typ[u])
            else:
                q.add_link(u, 1 - q.typ[u], v, 1 - q.typ[v])
    return q


def hill(seed, r, steps, kcls, log=None):
    rng = random.Random(seed)
    pl = start(rng, r, kcls)
    if pl is None:
        return None
    best, I, P = score(pl)
    for it in range(steps):
        q = mutate(rng, pl)
        if q is None:
            continue
        sc, I2, P2_ = score(q)
        if sc < best:
            continue
        if not C.p2_ok(I2):
            continue
        if not q.shortest_ok(I2, P2_):
            continue
        pl, best = q, sc
        if log and it % 500 == 0:
            print("   it", it, best, flush=True)
    return pl, best


if __name__ == "__main__":
    seed, runs, r, steps = (int(x) for x in sys.argv[1:5])
    kcls = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    if len(sys.argv) > 6:
        PRAND = float(sys.argv[6])
    hist = {}
    top = None
    for i in range(runs):
        res = hill(seed * 1000 + i, r, steps, kcls)
        if res is None:
            print("run", i, "start failed", flush=True)
            continue
        pl, best = res
        hist[best[0]] = hist.get(best[0], 0) + 1
        I, P = pl.realise()
        print("run", i, "h2", best[0], "min|f|", best[1], "sum|f|", best[2], "types",
              "".join("EF"[x] for x in pl.typ), "classes", pl.cls if kcls else "single", flush=True)
        if top is None or best > top[0]:
            top = (best, pl.typ, pl.cls, sorted(pl.links))
    print("histogram of h2:", hist)
    print("top:", top)
