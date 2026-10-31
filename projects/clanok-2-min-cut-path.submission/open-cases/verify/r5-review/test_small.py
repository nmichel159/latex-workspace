"""Checks of r4-general.md §3: Example MW2 (and its 8-element version), Lemma Sub (exhaustive over the down-sets of
random ZZ + P2 instances, every edge subdivided), Lemma Mon (random augmentations).  Own code only.
Usage: python test_small.py SEED COUNT"""
import random
import sys
from collections import Counter
from zzlib import Inst, bits
from gswlib import random_zz_p2


def mw2(with_a=True, extra=None):
    # u=0; z=1, z'=2 tied to u; p=3 < w=4 < x=5, w < y=6, x < a=7; v=8
    names = ["u", "z", "z'", "p", "w", "x", "y", "a", "v"]
    n = 9
    rel = [(0, i) for i in range(n)] + [(i, 8) for i in range(n)] + [(1, 0), (2, 0)]
    rel += [(3, 4), (4, 5), (4, 6), (5, 7)]
    R = [(0, 3), (1, 3), (1, 5), (4, 5), (4, 6), (2, 6), (2, 8), (0, 7), (5, 7), (7, 8), (6, 8)]
    if not with_a:
        R = [e for e in R if 7 not in e]
    if extra == "bottom":
        names.append("b")
        n += 1
        rel += [(9, 0), (0, 9), (9, 8)]
        R += [(9, 5), (9, 6)]
    elif extra == "top":
        names.append("tau")
        n += 1
        rel += [(9, 8), (8, 9), (0, 9)]
        R += [(5, 9), (6, 9)]
    I = Inst(n, rel, R, 0, 8, names)
    if not with_a:
        # delete the element a = 7 by making it an isolated element tied to nothing: rebuild without it
        keep = [i for i in range(n) if i != 7]
        ren = {x: i for i, x in enumerate(keep)}
        rel2 = [(ren[a], ren[b]) for a in keep for b in keep if I.le(a, b)]
        R2 = [(ren[a], ren[b]) for a, b in I.R]
        I = Inst(len(keep), rel2, R2, ren[0], ren[8], [names[i] for i in keep])
    return I


def solutions(I):
    return [D for D in I.downsets() if I.connected_in_GD(D)]


def show(I, D):
    return "{" + ",".join(I.names[x] for x in bits(D)) + "}"


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    print("== Example MW2 ==")
    for with_a in (True, False):
        for extra in (None, "bottom", "top"):
            I = mw2(with_a, extra)
            sols = solutions(I)
            inc = [(I.names[a], I.names[b]) for a, b in I.incomparable_pairs()]
            print("with a=%s extra=%s: |Q|=%d axioms %s, P2 failures %s, incomparable pairs %s, solutions %d %s" % (
                with_a, extra, I.n, I.check() or "ok", I.p2_failures(), inc, len(sols),
                [show(I, D) for D in sols[:3]]))
    print("== Lemma Sub ==")
    st = Counter()
    for it in range(count):
        I = random_zz_p2(rng, rng.randint(3, 8), rng.randint(0, 2), rng.randint(0, 2), rng.choice((0.2, 0.4)),
                         rng.choice((0.0, 0.3)), rng.choice((0.2, 0.4)))
        if I is None:
            continue
        Ds = I.downsets()
        for e in I.R:
            y, x = e if I.lt(e[0], e[1]) else (e[1], e[0])
            n = I.n
            be, te = n, n + 1
            rel = [(a, b) for a in range(n) for b in range(n) if I.le(a, b)]
            rel += [(be, I.u), (I.u, be), (te, I.v), (I.v, te), (be, te)]
            rel += [(be, z) for z in range(n)] + [(z, te) for z in range(n)]
            R = [f for f in I.R if f != e] + [(y, te), (be, te), (be, x)]
            J = Inst(n + 2, rel, R, I.u, I.v)
            assert not J.check(), J.check()
            Ds2 = J.downsets()
            mapped = sorted(D | (1 << be) for D in Ds)
            if sorted(Ds2) != mapped:
                st["bijection_fail"] += 1
            for D in Ds:
                if I.connected_in_GD(D) != J.connected_in_GD(D | (1 << be)):
                    st["answer_fail"] += 1
            pred = all(I.has_witness(a, b, forbid_edge=frozenset(e)) for a, b in I.incomparable_pairs())
            if pred != (not J.p2_failures()):
                st["p2_iff_fail"] += 1
            st["edges"] += 1
            st["middle_edges"] += int(not I.le(y, I.u) and not I.le(I.v, x))
            st["p2_kept"] += int(pred)
        st["instances"] += 1
    print(dict(st))
    print("== Lemma Mon ==")
    st = Counter()
    for it in range(count):
        I = random_zz_p2(rng, rng.randint(3, 8), rng.randint(0, 2), rng.randint(0, 2), rng.choice((0.2, 0.4)),
                         rng.choice((0.0, 0.3)), rng.choice((0.2, 0.4)))
        if I is None:
            continue
        n = I.n
        rel = [(a, b) for a in range(n) for b in range(n) if I.le(a, b)]
        R = list(I.R)
        k = rng.randint(1, 3)
        for j in range(k):
            x = n + j
            a = rng.randrange(n)
            b = rng.choice([z for z in range(n) if I.le(a, z)])
            rel += [(z, x) for z in range(n) if I.le(z, a)] + [(x, z) for z in range(n) if I.le(b, z)]
            rel += [(I.u, x), (x, I.v)]
        J0 = Inst(n + k, rel, [], I.u, I.v)
        cand = [(p, q) for p in range(n + k) for q in range(n + k) if J0.lt(p, q) and {p, q} != {I.u, I.v}]
        Rs = set(R)
        for p, q in cand:
            if (p, q) not in Rs and rng.random() < 0.2:
                Rs.add((p, q))
        J = Inst(n + k, rel, sorted(Rs), I.u, I.v)
        if J.check():
            st["bad_aug"] += 1
            continue
        same = all(I.le(p, q) == J.le(p, q) for p in range(n) for q in range(n))
        if not same:
            st["order_changed_skip"] += 1
            continue
        for D in I.downsets():
            if I.connected_in_GD(D):
                D2 = 0
                for z in bits(D):
                    D2 |= J.down[z]
                ok = J.is_downset(D2) and (D2 & ((1 << n) - 1)) == D and not (D2 >> I.v) & 1
                ok = ok and J.connected_in_GD(D2)
                st["solutions_checked"] += 1
                if not ok:
                    st["mon_fail"] += 1
        st["instances"] += 1
    print(dict(st))


if __name__ == "__main__":
    main()
