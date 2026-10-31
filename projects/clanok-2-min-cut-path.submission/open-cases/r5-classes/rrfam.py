"""Round-robin planted paths with multi-position classes (agent r5-classes, third run).

P = (C_1 C_2 .. C_K)^R: K classes, R rounds, class j at positions j, K + j, 2K + j, ...; the type of class j is
given by the word W (length K).  P2: same-type members of different classes at distance >= 2 by partner-partner
links; opposite-type pairs by a contact a -> q (X'_a meets X_q) chosen among the *forward-compatible* ones (the
contact position lies after the first position of the class of the partner), at random (both directions with
probability pboth).  Such instances are rigid (first-flip argument, r5-classes.md section 4.1).

mode 'free': contacts chosen at random among all directions (not necessarily forward-compatible).
"""
import random
import sys
import ccore as C
import plant
import costs


def build(W, R, seed, pboth=0.0, mode="fwd", extra=0.0):
    rng = random.Random(seed)
    K = len(W)
    typ, cls = [], []
    for rd in range(R):
        for j in range(K):
            typ.append(0 if W[j] == "E" else 1)
            cls.append(j)
    r = len(typ)
    pl = plant.Planted(typ, cls)
    first = {}
    for a in range(r):
        first.setdefault(cls[a], a)
    for a in range(r):
        for b in range(a + 1, r):
            if cls[a] == cls[b]:
                continue
            if typ[a] == typ[b]:
                if b >= a + 2:
                    pl.add_link(a, 1 - typ[a], b, 1 - typ[b])
                continue
            # opposite types: candidates a -> b (X'_a meets X_b) and b -> a
            ok_ab = (mode == "free") or b > first[cls[a]]
            ok_ba = (mode == "free") or a > first[cls[b]]
            choices = []
            if ok_ab:
                choices.append((a, b))
            if ok_ba:
                choices.append((b, a))
            assert choices
            if len(choices) == 2 and rng.random() < pboth:
                sel = choices
            else:
                sel = [rng.choice(choices)]
            for (x, y) in sel:
                pl.add_link(x, 1 - typ[x], y, typ[y])
    # optional extra contacts (forward-compatible), any types
    if extra > 0:
        for a in range(r):
            for b in range(r):
                if a != b and abs(a - b) >= 2 and rng.random() < extra:
                    if mode == "free" or b > first[cls[a]]:
                        pl.add_link(a, 1 - typ[a], b, typ[b])
    return pl


if __name__ == "__main__":
    W = sys.argv[1]
    R = int(sys.argv[2])
    seeds = int(sys.argv[3])
    mode = sys.argv[4] if len(sys.argv) > 4 else "fwd"
    pboth = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    for sd in range(1, seeds + 1):
        pl = build(W, R, sd, pboth=pboth, mode=mode)
        I, P = pl.realise()
        p2 = C.p2_ok(I)
        sh = pl.shortest_ok(I, P)
        nsol = len(C.all_solutions(I)) if I.k <= 16 else None
        g10 = costs.desc_guided(I, P, 1, 0, want=True)
        g11 = costs.desc_guided(I, P, 1, 1, want=True)
        g20 = costs.desc_guided(I, P, 2, 0, want=True) if len(I.sides) <= 60 else None
        print("W=%s R=%d seed=%d mode=%s P2=%s shortest=%s classes=%d sides=%d nsol=%s h2=%d desc(1,0)=%s desc(1,1)=%s desc(2,0)=%s" % (
            W, R, sd, mode, p2, sh, I.k, len(I.sides), nsol, costs.h2(I, P), g10, g11, g20), flush=True)
