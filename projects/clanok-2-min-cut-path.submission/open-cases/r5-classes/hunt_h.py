"""Adversarial hill climbing against Hypothesis H (switch model; agent r5-classes, third run).

H: every shortest valid path of a 2CH + P2 instance has a member u with |f(u)| <= c (f(u) = members of the other
type meeting the partner X'_u).  Then DESC(1, 2, c) decides 2CH + P2 (r5-classes.md section 5).
Start: forward structure R(W) for a balanced random word W (rigid, shortest).  Moves: add a contact
(X'_a meets X_c) or a partner-partner link, remove a non-structural link (P2 repaired by the opposite contact or a
partner-partner link), all kept only if P2 holds and the planted path stays shortest (exact check).
Objective: (min_u |f(u)|, second smallest |f|, sum |f|), maximised.

usage: python hunt_h.py SEED RUNS R STEPS
"""
import random
import sys
import ccore as C
import plant
import costs


def start(rng, r):
    while True:
        W = "".join(rng.choice("EF") for _ in range(r))
        if abs(W.count("E") - W.count("F")) <= max(2, r // 4):
            break
    pl = plant.base_word(W, None, forward=True)
    return pl


def score(I, P):
    fs = sorted(len(x) for x in costs.f_sets(I, P))
    return (fs[0], fs[1], sum(fs))


def mutate(rng, pl):
    q = pl.copy()
    r = q.r
    mv = rng.random()
    if mv < 0.5:
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
        q.remove_link(rng.choice(cand))
        for (u, v) in q.p2_pairs_missing():
            if q.typ[u] != q.typ[v]:
                if rng.random() < 0.5:
                    q.add_link(u, 1 - q.typ[u], v, q.typ[v])
                else:
                    q.add_link(v, 1 - q.typ[v], u, q.typ[u])
            else:
                q.add_link(u, 1 - q.typ[u], v, 1 - q.typ[v])
    return q


def hill(seed, r, steps):
    rng = random.Random(seed)
    pl = start(rng, r)
    I, P = pl.realise()
    assert C.p2_ok(I) and pl.shortest_ok(I, P)
    best = score(I, P)
    for it in range(steps):
        q = mutate(rng, pl)
        if q is None:
            continue
        I2, P2_ = q.realise()
        sc = score(I2, P2_)
        if sc < best:
            continue
        if not C.p2_ok(I2) or not q.shortest_ok(I2, P2_):
            continue
        pl, best = q, sc
    return pl, best


if __name__ == "__main__":
    seed, runs, r, steps = (int(x) for x in sys.argv[1:5])
    hist = {}
    top = None
    for i in range(runs):
        pl, best = hill(seed * 1000 + i, r, steps)
        hist[best[0]] = hist.get(best[0], 0) + 1
        print("run", i, "min|f|", best[0], "second", best[1], "sum", best[2], "types",
              "".join("EF"[x] for x in pl.typ), flush=True)
        if top is None or best > top[0]:
            top = (best, pl.typ, sorted(L for L in pl.links if L not in pl.struct))
    print("histogram of min|f|:", hist)
    print("top:", top)
