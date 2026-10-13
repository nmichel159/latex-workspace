"""Planted yes-instances of Problem Pi; statistics and the single-generator criterion.
Usage: python explore_planted.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
from explore_pi import criterion_single

seed = int(sys.argv[1]); count = int(sys.argv[2])
rng = random.Random(seed)
st = {"inst": 0, "yes": 0, "no": 0, "crit_fail": 0}
lens = {}
fails = []
for it in range(count):
    q = rng.randint(6, 13)
    k = rng.randint(1, 3)
    inst = pi.planted_instance(rng, q, k, rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.2), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
    if inst is None or not inst.dist_ok():
        continue
    res = pi.answer(inst, limit=50000)
    if res["c"] < 3:
        continue
    st["inst"] += 1
    if res["yes"]:
        st["yes"] += 1
        lens[res["minlen"]] = lens.get(res["minlen"], 0) + 1
        if not criterion_single(inst, res):
            st["crit_fail"] += 1
            fails.append((inst, res))
    else:
        st["no"] += 1
print(st, dict(sorted(lens.items())))
for inst, res in fails[:3]:
    print("FAIL q=%d u=%d v=%d c=%d real=%s ears=%s ncuts=%d nyes=%d minlen=%s" % (inst.q, inst.u, inst.v, res["c"], inst.real_edges(), inst.ears(), res["ncuts"], res["nyes"], res["minlen"]))
