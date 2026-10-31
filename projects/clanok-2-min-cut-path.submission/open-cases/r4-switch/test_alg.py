"""Check alg.decide against the exact answer (brute force over modes, or sw.exact for larger n).
Families: rigid R_L (L = 2..LMAX) and its broken variants cut(L, k), tflip(L, k) (dc-hardness/rigid_pc.py
definitions, re-implemented in gen.py style here), the Helly form (t added to every flip side), A14, A18, their
one-node no-variants keeping P2, saturated planted instances (saturate.py), random P2 instances.
Usage: python test_alg.py SEED COUNT KD KS S B [families]"""
import sys
import random
import time

import sw
import gen
import alg
import saturate
from test_prove import A14, A18, gen_instance

seed, count = int(sys.argv[1]), int(sys.argv[2])
kd, ks, s, B = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
do_fam = len(sys.argv) > 7 and sys.argv[7] == "families"
rng = random.Random(seed)
stats = {}
t0 = time.time()


def exact(inst):
    if len(inst[1]) <= 16:
        return sw.brute(inst) is not None
    return sw.exact(inst)


def check(inst, label):
    ex = exact(inst)
    a = alg.decide(inst, kd, ks, s, B)
    key = (label.split("(")[0], ex, a)
    stats[key] = stats.get(key, 0) + 1
    if a and not ex:
        print("UNSOUND", label, sw.fmt(inst), flush=True)
    if ex and not a:
        print("INCOMPLETE", label, sw.fmt(inst), flush=True)


if do_fam:
    for L in range(2, 9):
        for lab, inst in gen.rigid_variants(L):
            check(inst, lab)
    for base, nm in ((A14, "A14"), (A18, "A18")):
        inst = tuple(base)
        check(inst, nm)
        N, E, F, s_, t = inst
        for w in range(len(E)):
            for typ in (0, 1):
                S = E if typ == 0 else F
                for x in sw.bits(S[w]):
                    E3, F3 = list(E), list(F)
                    if typ == 0:
                        E3[w] &= ~(1 << x)
                    else:
                        F3[w] &= ~(1 << x)
                    inst3 = (N, E3, F3, s_, t)
                    if sw.p2_ok(inst3):
                        check(inst3, nm + "del")
    print("families done %.1fs" % (time.time() - t0), flush=True)
for it in range(count):
    m = ["random", "repair", "planted", "saturated"][it % 4]
    if m == "saturated":
        L = rng.randint(5, 10)
        word = "".join(rng.choice("EF") for _ in range(L))
        inst, P = saturate.saturate(rng, word, 0.3)
        if inst is None:
            continue
        # also a broken variant: drop one random node of the planted path
        check(inst, "sat")
        N, E, F, s_, t = inst
        w = rng.randrange(len(E))
        typ = P[w] & 1
        S = F if typ else E
        xs = sw.bits(S[w])
        x = rng.choice(xs)
        E3, F3 = list(E), list(F)
        if typ:
            F3[w] &= ~(1 << x)
        else:
            E3[w] &= ~(1 << x)
        inst3 = (N, E3, F3, s_, t)
        if sw.p2_ok(inst3):
            check(inst3, "satdel")
        continue
    inst = gen_instance(rng, m)
    if len(inst[1]) > 12:
        continue
    check(inst, m)
print("seed", seed, "params kd ks s B", kd, ks, s, B, "%.1fs" % (time.time() - t0))
for k in sorted(stats, key=str):
    print("  (family, exact, alg)", k, stats[k])
