"""Hill climbing against Hypothesis P (r4-classes.md §2.1) with classes.

State: a planted instance (r5-classes/plant.Planted) whose planted path is a shortest valid path, P2 holding.
Moves: add a link (partner of a meets member c; or partners of a, b meet), remove a non-structural link (if P2 stays
true), or move a member to another class of its type (if P2 can be kept: the move is rejected if P2 fails).
Objective: least hErr over the shortest valid paths, then hErr of the planted path, then the sum of |f|; a move is accepted if the planted path stays a
shortest valid path and the objective does not decrease (ties accepted with probability 1/2).
Note: hP is evaluated on the planted path only; at the end hP is evaluated on every shortest valid path.
Usage: python climbp.py SEED RUNS LMIN LMAX KCLS STEPS"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import ccore as C  # noqa: E402
import plant  # noqa: E402
import satc  # noqa: E402


def objective(pl):
    """(least hP over the shortest valid paths (at most 30 enumerated), hP of the planted path, sum of |f|)"""
    I, P = pl.realise()
    f = satc.fsets(I, P)
    Ls, paths = C.shortest_valid_paths(I, limit=30)
    return (min(satc.hErr(I, Q) for Q in paths), satc.hErr(I, P), sum(len(x) for x in f))


def p2_ok_pl(pl):
    return not pl.p2_pairs_missing()


def climb(rng, pl, kcls, steps):
    cur = objective(pl)
    r = pl.r
    for st in range(steps):
        new = pl.copy()
        mv = rng.random()
        if mv < 0.55:
            a = rng.randrange(r)
            if rng.random() < 0.7:
                c = rng.randrange(r)
                if c == a:
                    continue
                new.add_link(a, 1 - new.typ[a], c, new.typ[c])
            else:
                b = rng.randrange(r)
                if abs(b - a) < 2:
                    continue
                new.add_link(a, 1 - new.typ[a], b, 1 - new.typ[b])
        elif mv < 0.85:
            nonstruct = [L for L in new.links if L not in new.struct]
            if not nonstruct:
                continue
            L = rng.choice(nonstruct)
            new.remove_link(L)
            if not p2_ok_pl(new):
                continue
        else:
            a = rng.randrange(r)
            t = new.typ[a]
            new.cls[a] = ("EF"[t], rng.randrange(kcls))
            if not p2_ok_pl(new):
                # repair P2 by partner-partner links for same-type far pairs, forward contacts otherwise
                for (u, v) in new.p2_pairs_missing():
                    if new.typ[u] == new.typ[v] and u < r and v < r and abs(u - v) >= 2:
                        new.add_link(u, 1 - new.typ[u], v, 1 - new.typ[v])
                    elif u < r and v < r and new.typ[u] != new.typ[v]:
                        x, y = (u, v) if u < v else (v, u)
                        new.add_link(x, 1 - new.typ[x], y, new.typ[y])
                if not p2_ok_pl(new):
                    continue
        if not new.shortest_ok():
            continue
        ob = objective(new)
        if ob > cur or (ob == cur and rng.random() < 0.5):
            pl, cur = new, ob
    return pl, cur


if __name__ == "__main__":
    seed, runs, lmin, lmax, kcls, steps = (int(x) for x in sys.argv[1:7])
    rng = random.Random(seed)
    t0 = time.time()
    best = None
    for run in range(runs):
        L = rng.randint(lmin, lmax)
        word = "".join(rng.choice("EF") for _ in range(L))
        pl = satc.saturate(rng, word, kcls)
        if pl is None:
            print("run", run, "start failed", flush=True)
            continue
        pl, cur = climb(rng, pl, kcls, steps)
        I, P0 = pl.realise()
        Ls, paths = C.shortest_valid_paths(I, limit=50)
        allh = [satc.hErr(I, P) for P in paths]
        print("run", run, "word", word, "planted hErr", cur, "min hErr over shortest paths", min(allh), "max", max(allh),
              "classes", [pl.cls[a] for a in range(pl.r)], "%.0fs" % (time.time() - t0), flush=True)
        if best is None or min(allh) > best[0]:
            best = (min(allh), word, [pl.cls[a] for a in range(pl.r)], sorted(pl.links))
    print("best:", best, flush=True)
