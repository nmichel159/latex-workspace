"""Per-path locality: every simple alternating real u-v path whose (even, odd) pairs at index distance <= w are
consistent ('even does not reach odd' in R) -- is it globally consistent?  Counts violating paths for w = 3, 5.
Usage: python locality_path.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def all_paths(inst, reach, w, maxlen=13, cap=200000):
    q = inst.q; u, v = inst.u, inst.v
    nbr = [[y for y in range(q) if inst.R[x][y]] for x in range(q)]
    path = [u]; used = [False] * q; used[u] = True
    out = []
    def ok(idx, y):
        for i in range(max(0, idx - w), idx):
            if (idx - i) % 2 == 0:
                continue
            a, b = (path[i], y) if i % 2 == 0 else (y, path[i])
            if (reach[a] >> b) & 1:
                return False
        return True
    def rec():
        if len(out) > cap:
            return
        x = path[-1]
        if x == v:
            if len(path) % 2 == 0:
                out.append(list(path))
            return
        if len(path) > maxlen:
            return
        for y in nbr[x]:
            if used[y] or (y == v and len(path) % 2 == 0) or not ok(len(path), y):
                continue
            used[y] = True; path.append(y)
            rec()
            path.pop(); used[y] = False
    rec()
    return out

def consistent(reach, P):
    ev, od = P[0::2], P[1::2]
    return not any((reach[a] >> b) & 1 for a in ev for b in od)

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "paths3": 0, "bad3": 0, "paths5": 0, "bad5": 0}
    ex = None
    for it in range(count):
        q = rng.randint(6, 11)
        if rng.random() < 0.5:
            inst = pi.planted_instance(rng, q, rng.randint(1, 3), rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
        else:
            inst = pi.random_instance(rng, q, rng.uniform(0.2, 0.7), rng.uniform(0.0, 0.3), max_mult=rng.randint(1, 3))
        if inst is None or not inst.dist_ok():
            continue
        try:
            res = pi.answer(inst, limit=50000)
        except RuntimeError:
            continue
        if res["c"] < 3:
            continue
        st["inst"] += 1
        for w in (3, 5):
            for P in all_paths(inst, res["reach"], w):
                st["paths%d" % w] += 1
                if not consistent(res["reach"], P):
                    st["bad%d" % w] += 1
                    if ex is None:
                        ex = (w, inst, P)
    print("seed", seed, st)
    if ex:
        w, inst, P = ex
        print("  w=%d bad path %s: q=%d real=%s ears=%s" % (w, P, inst.q, inst.real_edges(), inst.ears()))
