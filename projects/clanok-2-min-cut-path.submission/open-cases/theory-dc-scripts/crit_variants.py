"""Which canonical minimum cuts suffice?  On planted Pi-instances count failures of
 C0: the two extreme minimum cuts;  C1u: the cuts cl(u, x);  C1v: the complements of the co-closures of (v, y);
 C1: C1u or C1v.  Usage: python crit_variants.py SEED COUNT QMIN QMAX"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
from explore_pi import gen_cuts, co_cut

def has(inst, A):
    return A is not None and pi.real_cut_path(inst, A) is not None

seed, count, qmin, qmax = map(int, sys.argv[1:5])
rng = random.Random(seed)
st = {"yes": 0, "no": 0, "C0": 0, "C1u": 0, "C1v": 0, "C1": 0}
ex = {}
for it in range(count):
    q = rng.randint(qmin, qmax)
    k = rng.randint(1, 4)
    inst = pi.planted_instance(rng, q, k, rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
    if inst is None or not inst.dist_ok():
        continue
    try:
        res = pi.answer(inst, limit=200000)
    except RuntimeError:
        continue
    if res["c"] < 3:
        continue
    if not res["yes"]:
        st["no"] += 1
        continue
    st["yes"] += 1
    reach = res["reach"]
    c0 = has(inst, reach[inst.u]) or has(inst, co_cut(inst, reach, []))
    c1u = any(has(inst, gen_cuts(inst, reach, [x])) for x in range(inst.q))
    c1v = any(has(inst, co_cut(inst, reach, [y])) for y in range(inst.q))
    for name, ok in (("C0", c0), ("C1u", c1u), ("C1v", c1v), ("C1", c1u or c1v)):
        if not ok:
            st[name] += 1
            if name not in ex or inst.q < ex[name][0].q:
                ex[name] = (inst, res)
print("seed", seed, "failures:", st)
for name, (inst, res) in sorted(ex.items()):
    print("  %s smallest failure: q=%d c=%d real=%s ears=%s minlen=%s" % (name, inst.q, res["c"], inst.real_edges(), inst.ears(), res["minlen"]))
