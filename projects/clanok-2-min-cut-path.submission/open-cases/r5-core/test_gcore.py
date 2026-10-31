"""Self-test of gcore.py and first lemma checks.

For random general ZZ + P2 instances (gcert.random_inst and mixed.random_instance, as in r4-general/test_core.py):
  * Gen.brute (down-set enumeration) == gcert.exact (ZZ walk search of dc-general) == Gen.shortest is not None;
  * round trip Gen -> gcert.Inst -> exact answer unchanged;
  * Lemma W (window lemma) on every shortest valid path: every allowed side (E_z with z not in Dn, F_z with z not in
    Up) meets members only within 3 consecutive positions;
  * Lemma F2' (minimal E-members a, b at distance >= 3 have meeting partners or an upper middle witness), and the
    dual for maximal F-members.
Usage: python test_gcore.py SEED COUNT NMIN NMAX
"""
import sys
import random
import time
from collections import Counter
import gcore
from gcore import Gen, from_inst, to_inst, PathInfo, bits
import gcert
import mixed
from common_r4 import from_zz


def gen_instance(rng, nmin, nmax, it):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        I = from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                          p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))
    return I


def upper_mid_witness(G, a, b):
    """Is there y > a, b with private middle-edge nodes in F_a & E_y and F_b & E_y?"""
    ups = {}
    for z, (y, x) in G.medge.items():
        ups.setdefault(y, set()).add(x)
    return bool(ups.get(a, set()) & ups.get(b, set()))


def lower_mid_witness(G, a, b):
    lows = {}
    for z, (y, x) in G.medge.items():
        lows.setdefault(x, set()).add(y)
    return bool(lows.get(a, set()) & lows.get(b, set()))


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        I = gen_instance(rng, nmin, nmax, it)
        if not I.p2():
            continue
        st["P2"] += 1
        G, G0 = from_inst(I)
        ex = gcert.exact(I)
        L, path = G.shortest()
        assert (L is not None) == ex, "shortest vs exact"
        if G.m <= 16:
            br = bool(G.brute())
            assert br == ex, "brute vs exact"
            st["brute checked"] += 1
        I2, _ = to_inst(G)
        assert gcert.exact(I2) == ex, "round trip"
        if G.p2_bad():
            st["switch-form P2 fails (node merge)"] += 1
        if not ex:
            continue
        st["yes"] += 1
        assert G.is_valid_walk(path)
        paths = G.all_shortest(limit=200, length=L)
        st["paths"] += len(paths)
        for P in paths:
            assert G.is_valid_walk(P)
            pi = PathInfo(G, P)
            for i in pi.allowed:
                if i in P:
                    continue
                c = pi.contacts(i)
                if c and max(c) - min(c) > 2:
                    st["LEMMA W FAILS"] += 1
                    print("W fails", gcert.describe(I), P, i, c)
            # F2' for minimal E-members, dual for maximal F-members
            mins = pi.minimal_E()
            for x in range(len(mins)):
                for y in range(x + 1, len(mins)):
                    a, b = mins[x], mins[y]
                    if abs(a - b) < 3:
                        continue
                    wa, wb = pi.sw[a], pi.sw[b]
                    assert not G.comparable(wa, wb)
                    if G.F[wa] & G.F[wb]:
                        st["F2' partners meet"] += 1
                    elif upper_mid_witness(G, wa, wb):
                        st["F2' upper middle witness"] += 1
                    else:
                        st["F2' FAILS"] += 1
                        print("F2' fails", gcert.describe(I), P, a, b)
            maxs = pi.maximal_F()
            for x in range(len(maxs)):
                for y in range(x + 1, len(maxs)):
                    a, b = maxs[x], maxs[y]
                    if abs(a - b) < 3:
                        continue
                    wa, wb = pi.sw[a], pi.sw[b]
                    assert not G.comparable(wa, wb)
                    if G.E[wa] & G.E[wb]:
                        st["F2'd partners meet"] += 1
                    elif lower_mid_witness(G, wa, wb):
                        st["F2'd lower middle witness"] += 1
                    else:
                        st["F2'd FAILS"] += 1
                        print("F2'd fails", gcert.describe(I), P, a, b)
    print("seed %d count %d n %d-%d %.0fs: %s" % (seed, count, nmin, nmax, time.time() - t0, dict(st)))


if __name__ == "__main__":
    main()
