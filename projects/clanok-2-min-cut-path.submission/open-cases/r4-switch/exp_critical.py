"""Experiment: 'critical run' instances.  Word F^a E^m F^b.  Cross pairs (F before, E in run) use forward contacts of
the F-partner; cross pairs (E in run, F after) use a forward contact of the run partner (prob. PF) or a backward
contact of the F-partner; extra forward contacts of run partners to later run members with prob. PX.
For each instance: P2, number of solutions, least certificate storage (k = 1..3), side-CSP PC on the no-variants
obtained by deleting one node from one side (when P2 survives).
Usage: python exp_critical.py SEED COUNT A M B PF PX"""
import sys
import random
import time

import sw
import gen
import certcost

seed, count = int(sys.argv[1]), int(sys.argv[2])
A, M, B = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
PF, PX = float(sys.argv[6]), float(sys.argv[7])
rng = random.Random(seed)
word = "F" * A + "E" * M + "F" * B
L = len(word)
t0 = time.time()
stats = {}
pcstat = {}
for it in range(count):
    def orient(p, q):
        if word[p - 1] == "F" and word[q - 1] == "E":
            return "f"
        if word[p - 1] == "E" and word[q - 1] == "F":
            return "f" if rng.random() < PF else "b"
        return "f"
    extra = []
    for p in range(A + 1, A + M + 1):
        for q in range(p + 2, A + M + 1):
            if rng.random() < PX:
                extra.append(("fh", p, q))
    inst, P = gen.planted(word, None, orient, extra=extra)
    assert sw.p2_ok(inst)
    sols = sw.all_solutions(inst)
    c = certcost.cost(inst, P, 3) if len(sols) == 1 else None
    key = (len(sols), tuple((c[k][0] if c[k] else None) for k in (1, 2, 3)) if c else None)
    stats[key] = stats.get(key, 0) + 1
    # no-variants
    N, E, F, s, t = inst
    for w in range(L):
        for typ in (0, 1):
            Sx = E if typ == 0 else F
            for x in sw.bits(Sx[w]):
                E2, F2 = list(E), list(F)
                if typ == 0:
                    E2[w] &= ~(1 << x)
                else:
                    F2[w] &= ~(1 << x)
                inst2 = (N, E2, F2, s, t)
                if not sw.p2_ok(inst2):
                    continue
                if sw.brute(inst2) is not None:
                    continue
                pc = sw.pc_side(inst2)
                pcstat[pc] = pcstat.get(pc, 0) + 1
                if pc:
                    print("PC FALSE POSITIVE", sw.fmt(inst2), flush=True)
print("seed", seed, "word", word, "PF", PF, "PX", PX)
for k in sorted(stats, key=str):
    print("  (#solutions, storage k=1,2,3)", k, stats[k])
print("  no-variants: PC answer counts", pcstat)
print("%.1fs" % (time.time() - t0))
