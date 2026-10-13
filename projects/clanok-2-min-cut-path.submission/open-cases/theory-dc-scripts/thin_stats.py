"""Statistics on thin sides of minimum cuts of Pi-instances (planted generator):
 T1: for every minimum cut, some side is thin (Lemma 7) -- must never fail;
 T2: on a thin side K with root r every vertex of K - r is W-adjacent to r;
 T3: for witness cuts: is the u-side thin, the v-side thin, both.
Usage: python thin_stats.py SEED COUNT"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {"cuts": 0, "T1fail": 0, "thinsides": 0, "T2fail": 0, "wit": 0, "wit_u_thin": 0, "wit_v_thin": 0, "wit_both": 0}
ex = None
for it in range(count):
    q = rng.randint(6, 12)
    inst = pi.planted_instance(rng, q, rng.randint(1, 3), rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
    if inst is None or not inst.dist_ok():
        continue
    try:
        res = pi.answer(inst, limit=50000)
    except RuntimeError:
        continue
    if res["c"] < 3:
        continue
    W = inst.W
    for A in res["cuts"]:
        st["cuts"] += 1
        side = [x for x in range(q) if (A >> x) & 1]
        other = [x for x in range(q) if not (A >> x) & 1]
        thinA = all(any(W[x][y] for y in other) for x in side)
        thinB = all(any(W[x][y] for y in side) for x in other)
        if not (thinA or thinB):
            st["T1fail"] += 1
        for thin, K, r in ((thinA, side, inst.u), (thinB, other, inst.v)):
            if thin:
                st["thinsides"] += 1
                if any(W[r][x] == 0 for x in K if x != r):
                    st["T2fail"] += 1
                    if ex is None:
                        ex = (inst, side)
        if pi.real_cut_path(inst, A) is not None:
            st["wit"] += 1
            st["wit_u_thin"] += thinA
            st["wit_v_thin"] += thinB
            st["wit_both"] += thinA and thinB
print(st)
if ex:
    inst, side = ex
    print("T2 example: q=%d real=%s ears=%s A=%s" % (inst.q, inst.real_edges(), inst.ears(), side))
