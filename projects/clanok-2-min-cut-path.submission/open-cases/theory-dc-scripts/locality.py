"""Is the global condition 'no even vertex reaches an odd vertex in R' implied by local conditions?
For each Pi-instance compare the truth with: does a simple alternating real u-v path exist whose pairs
(even, odd) at index distance <= w satisfy 'even does not reach odd'  (w = 1, 3, 5).
Usage: python locality.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def search(inst, reach, w, maxlen=13):
    q = inst.q
    u, v = inst.u, inst.v
    nbr = [[y for y in range(q) if inst.R[x][y]] for x in range(q)]
    path = [u]
    used = [False] * q
    used[u] = True
    def ok(newidx, y):
        for i in range(max(0, newidx - w), newidx):
            if (newidx - i) % 2 == 0:
                continue
            a, b = (path[i], y) if i % 2 == 0 else (y, path[i])   # a even, b odd
            if (reach[a] >> b) & 1:
                return False
        return True
    def rec():
        x = path[-1]
        if x == v:
            return len(path) % 2 == 0
        if len(path) > maxlen:
            return False
        for y in nbr[x]:
            if used[y]:
                continue
            if y == v and len(path) % 2 == 0:
                continue
            if not ok(len(path), y):
                continue
            used[y] = True; path.append(y)
            if rec():
                return True
            path.pop(); used[y] = False
        return False
    return rec()

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {"inst": 0, "yes": 0}
fp = {1: 0, 3: 0, 5: 0}
fn = {1: 0, 3: 0, 5: 0}
ex = {}
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
    truth = res["yes"]
    st["yes"] += truth
    for w in (1, 3, 5):
        loc = search(inst, res["reach"], w)
        if loc and not truth:
            fp[w] += 1
            if w not in ex:
                ex[w] = inst
        if truth and not loc:
            fn[w] += 1
print("seed", seed, st, "false positives by window:", fp, "false negatives:", fn)
for w, inst in sorted(ex.items()):
    print("  w=%d example: q=%d real=%s ears=%s" % (w, inst.q, inst.real_edges(), inst.ears()))
