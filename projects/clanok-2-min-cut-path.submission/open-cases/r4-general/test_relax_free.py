"""Does dropping the order relations between free switches (after propagation) change the answer?
For random general instances: prune, contract the fixed sides (as in Theorem R) but ignore the comparabilities among
the free switches; solve the contracted 2CH instance by brute force; compare with the exact answer.  A change can
only turn a no-instance into a yes-instance (dropping relations adds mode vectors).
Usage: python test_relax_free.py SEED COUNT NMIN NMAX"""
import os
import sys
import random
from collections import Counter
from common_r4 import OC, gcert, from_zz, bits
from gsw import GSW, prune
import mixed
sys.path.insert(0, os.path.join(OC, "r4-switch"))
import sw as rsw   # noqa: E402

seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
rng = random.Random(seed)
st = Counter()
examples = []


def contract_ignoring_order(G, fixed):
    free = [w for w in range(G.m) if w not in fixed]
    par = list(range(G.N))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for w, mo in fixed.items():
        bl = bits(G.F[w] if mo else G.E[w])
        for x in bl[1:]:
            ra, rb = find(bl[0]), find(x)
            if ra != rb:
                par[ra] = rb
    roots = {}
    for x in range(G.N):
        roots.setdefault(find(x), len(roots))

    def remap(m):
        out = 0
        for x in bits(m):
            out |= 1 << roots[find(x)]
        return out
    return (len(roots), [remap(G.E[w]) for w in free], [remap(G.F[w]) for w in free], roots[find(G.s)],
            roots[find(G.t)]), free


for it in range(count):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        I = from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                          p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))
    if not I.p2():
        continue
    ex = gcert.exact(I)
    G = GSW(I)
    fixed, dead = prune(G)
    if dead is None:
        st["refuted by propagation"] += 1
        continue
    free = [w for w in range(G.m) if w not in fixed]
    comp = any(G.le[a][b] or G.le[b][a] for i, a in enumerate(free) for b in free[i + 1:])
    if not comp:
        st["no free comparabilities"] += 1
        continue
    inst, free = contract_ignoring_order(G, fixed)
    if len(free) > 16:
        st["too many free"] += 1
        continue
    rel = rsw.brute(inst) is not None
    st[("core", ex, rel)] += 1
    if rel != ex and len(examples) < 3:
        examples.append(gcert.describe(I))
print("seed %d: %s" % (seed, dict(st)))
for e in examples:
    print("  answer changed:", e)
