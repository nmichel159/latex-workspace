"""Stronger forms of the single-generator criterion on planted Pi-instances.
 S2: for every witness cut A: some cl(u,x) that is a witness lies inside A, or some V - co-cl(v,y) that is a
     witness contains A.
 S3: for every witness cut A and every shortest real u-v path P inside delta(A): the even vertices of P lie in
     cl(u,x) for one even x with cl(u,x) avoiding the odd vertices, or dually.
 S3any: for every witness cut A some path P inside delta(A) has the property of S3.
Usage: python test_S.py SEED COUNT QMIN QMAX"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dctools, pi
from dctools import mcp
from explore_pi import gen_cuts, co_cut

def has(inst, A):
    return A is not None and pi.real_cut_path(inst, A) is not None

def real_paths_in_cut(inst, A, maxlen=None):
    q = inst.q
    edges = [(a, b) for a, b in inst.real_edges() if ((A >> a) ^ (A >> b)) & 1]
    g = mcp.Gr(q, edges)
    return [list(vs) for vs, es in mcp.simple_paths(g, inst.u, inst.v, maxlen=maxlen, limit=20000)]

def single_ok(inst, reach, P):
    ev, od = P[0::2], P[1::2]
    oddmask = sum(1 << y for y in od)
    for x in ev:
        A = gen_cuts(inst, reach, [x])
        if A is not None and all((A >> e) & 1 for e in ev) and not (A & oddmask):
            return True
    evmask = sum(1 << x for x in ev)
    for y in od:
        A = co_cut(inst, reach, [y])
        if A is not None and (A & evmask) == evmask and not any((A >> o) & 1 for o in od):
            return True
    return False

seed, count, qmin, qmax = map(int, sys.argv[1:5])
rng = random.Random(seed)
st = {"yes": 0, "wcuts": 0, "S2": 0, "S3": 0, "S3any": 0}
ex = {}
for it in range(count):
    q = rng.randint(qmin, qmax)
    k = rng.randint(1, 4)
    inst = pi.planted_instance(rng, q, k, rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
    if inst is None or not inst.dist_ok():
        continue
    try:
        res = pi.answer(inst, limit=100000)
    except RuntimeError:
        continue
    if res["c"] < 3 or not res["yes"]:
        continue
    st["yes"] += 1
    reach = res["reach"]
    U = [gen_cuts(inst, reach, [x]) for x in range(q)]
    U = [A for A in U if A is not None and has(inst, A)]
    Vv = [co_cut(inst, reach, [y]) for y in range(q)]
    Vv = [A for A in Vv if A is not None and has(inst, A)]
    for A in res["cuts"]:
        p = pi.real_cut_path(inst, A)
        if p is None:
            continue
        st["wcuts"] += 1
        s2 = any((X & ~A) == 0 for X in U) or any((A & ~X) == 0 for X in Vv)
        if not s2:
            st["S2"] += 1; ex.setdefault("S2", (inst, A))
        L = len(p) - 1
        paths = real_paths_in_cut(inst, A)
        short = [P for P in paths if len(P) - 1 == L]
        if not all(single_ok(inst, reach, P) for P in short):
            st["S3"] += 1; ex.setdefault("S3", (inst, A))
        if not any(single_ok(inst, reach, P) for P in paths):
            st["S3any"] += 1; ex.setdefault("S3any", (inst, A))
print("seed", seed, st)
for name, (inst, A) in sorted(ex.items()):
    print("  %s: q=%d real=%s ears=%s A=%s" % (name, inst.q, inst.real_edges(), inst.ears(), [x for x in range(inst.q) if (A >> x) & 1]))
