"""Structure of shortest witnesses (over all minimum cuts) in Pi-instances.
For each yes-instance take every shortest witness path P (minimum length over all minimum cuts) and test
 H1: any two incomparable evens (x_i, x_j, |i-j| >= 4) are both real neighbours of u;
 H2: any two incomparable odds (|i-j| >= 4) are both real neighbours of v;
 H3: every common real neighbour of two incomparable evens lies in cl(u, E_P).
Preorder: x >= y iff every minimum cut containing x contains y, i.e. y in cl(u) + reach[x].
Usage: python shortest_struct.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
from locality_path import all_paths, consistent

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {"yes": 0, "long": 0, "H1": 0, "H2": 0, "H3": 0, "pairsE": 0, "pairsO": 0}
ex = {}
for it in range(count):
    q = rng.randint(6, 12)
    inst = pi.planted_instance(rng, q, rng.randint(2, 4), rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
    if inst is None or not inst.dist_ok():
        continue
    try:
        res = pi.answer(inst, limit=50000)
    except RuntimeError:
        continue
    if res["c"] < 3 or not res["yes"]:
        continue
    st["yes"] += 1
    reach = res["reach"]
    u, v = inst.u, inst.v
    full = (1 << q) - 1
    down = [reach[u] | reach[x] for x in range(q)]          # cl(u, x)
    def geq(x, y):
        return (down[x] >> y) & 1 or (reach[x] >> v) & 1      # top elements are above everything
    paths = [P for P in all_paths(inst, reach, 99, maxlen=15) if consistent(reach, P)]
    L = min(len(P) for P in paths)
    short = [P for P in paths if len(P) == L]
    if L - 1 < 5:
        continue
    st["long"] += 1
    for P in short:
        ev, od = P[0::2], P[1::2]
        clE = 0
        for x in ev:
            clE |= down[x]
        for idx_a in range(len(P)):
            for idx_b in range(idx_a + 4, len(P), 2):
                a, b = P[idx_a], P[idx_b]
                if geq(a, b) or geq(b, a):
                    continue
                if idx_a % 2 == 0:
                    st["pairsE"] += 1
                    if not (inst.R[u][a] or a == u) or not (inst.R[u][b] or b == u):
                        st["H1"] += 1; ex.setdefault("H1", (inst, P, a, b))
                    for w in range(q):
                        if inst.R[a][w] and inst.R[b][w] and not (clE >> w) & 1:
                            st["H3"] += 1; ex.setdefault("H3", (inst, P, a, b))
                            break
                else:
                    st["pairsO"] += 1
                    if not (inst.R[v][a] or a == v) or not (inst.R[v][b] or b == v):
                        st["H2"] += 1; ex.setdefault("H2", (inst, P, a, b))
print("seed", seed, st)
for k, (inst, P, a, b) in sorted(ex.items()):
    print("  %s: P=%s pair=%s q=%d real=%s ears=%s" % (k, P, (a, b), inst.q, inst.real_edges(), inst.ears()))
