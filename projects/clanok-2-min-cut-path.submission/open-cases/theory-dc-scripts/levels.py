"""Candidate canonical cuts: unions of levels of the minimum-cut order.
 height(x) = length of the longest chain of classes from the bottom class to the class of x; depth from the top.
 Candidates: {x : height(x) <= h} and {x : depth(x) > h}, for all h (both are minimum cuts).
Test: in every yes-instance, is some candidate a witness?  Usage: python levels.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def classes(inst, reach):
    q = inst.q; u, v = inst.u, inst.v
    full = (1 << q) - 1
    down = []
    for x in range(q):
        if (reach[x] >> v) & 1:
            down.append(full)                 # top: every minimum cut containing x ... none; treat as top
        else:
            down.append(reach[u] | reach[x])
    return down

def level_cuts(inst, reach):
    q = inst.q; u, v = inst.u, inst.v
    down = classes(inst, reach)
    geq = [[bool((down[x] >> y) & 1) for y in range(q)] for x in range(q)]
    # strict order between classes
    def gt(x, y):
        return geq[x][y] and not geq[y][x]
    # heights by longest chain (q small: memoised DFS)
    import functools
    @functools.lru_cache(None)
    def height(x):
        return max([height(y) + 1 for y in range(q) if gt(x, y)], default=0)
    @functools.lru_cache(None)
    def depth(x):
        return max([depth(y) + 1 for y in range(q) if gt(y, x)], default=0)
    H = [height(x) for x in range(q)]
    Dp = [depth(x) for x in range(q)]
    cands = set()
    for h in range(q + 1):
        A = sum(1 << x for x in range(q) if H[x] <= h)
        if (A >> u) & 1 and not (A >> v) & 1:
            cands.add(A)
        A = sum(1 << x for x in range(q) if Dp[x] > h)
        if (A >> u) & 1 and not (A >> v) & 1:
            cands.add(A)
    return cands

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"yes": 0, "fail": 0, "notmin": 0}
    ex = None
    for it in range(count):
        q = rng.randint(6, 12)
        if rng.random() < 0.7:
            inst = pi.planted_instance(rng, q, rng.randint(1, 4), rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
        else:
            inst = pi.random_instance(rng, q, rng.uniform(0.2, 0.7), rng.uniform(0.0, 0.3), max_mult=rng.randint(1, 3))
        if inst is None or not inst.dist_ok():
            continue
        try:
            res = pi.answer(inst, limit=50000)
        except RuntimeError:
            continue
        if res["c"] < 3 or not res["yes"]:
            continue
        st["yes"] += 1
        cands = level_cuts(inst, res["reach"])
        cutset = set(res["cuts"])
        st["notmin"] += sum(1 for A in cands if A not in cutset)
        if not any(A in cutset and pi.real_cut_path(inst, A) is not None for A in cands):
            st["fail"] += 1
            if ex is None or inst.q < ex.q:
                ex = inst
    print("seed", seed, st)
    if ex:
        print("  smallest failure: q=%d real=%s ears=%s" % (ex.q, ex.real_edges(), ex.ears()))
