"""Hypothesis: if a witness exists, every minimum cut with the largest number of real cut edges (or some) is a
witness.  Usage: python maxcut_hyp.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def nreal(inst, A):
    return sum(1 for a, b in inst.real_edges() if ((A >> a) ^ (A >> b)) & 1)

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {"yes": 0, "some_max_fails": 0, "all_max_fail": 0}
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
    best = max(nreal(inst, A) for A in res["cuts"])
    tops = [A for A in res["cuts"] if nreal(inst, A) == best]
    good = [pi.real_cut_path(inst, A) is not None for A in tops]
    if not all(good):
        st["some_max_fails"] += 1
    if not any(good):
        st["all_max_fail"] += 1
        if ex is None or inst.q < ex.q:
            ex = inst
print("seed", seed, st)
if ex:
    print("  smallest: q=%d real=%s ears=%s" % (ex.q, ex.real_edges(), ex.ears()))
