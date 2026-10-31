"""Dead mates added to a planted path (agent r5-classes, third run).

A *dead T-mate* of the class of a member a (type T) is a new switch m in cls(a) whose O-side Z_m meets no O-member
of P and whose T-side Z'_m meets the partner X'_q of every O-member q (P2 with q by the T-sides); P2 with every
T-member b of another class by Z_m meeting X'_b; dead mates of the same type and different classes meet in their
T-sides (a T-blob, their O-sides stay pairwise disjoint); a dead T-mate and a dead O-mate meet in a random one of
their two same-type pairs.  window: optional list of members whose sides the T-side Z'_m also meets.

add_dead(pl, a, window=()) -> switch index;  finish(pl, rng) adds the P2 links between dead mates.
"""
import random
import sys
import ccore as C
import plant
import costs
import fastdesc


def add_dead(pl, a, window=()):
    T = pl.typ[a]
    O = 1 - T
    m = pl.add_switch(pl.cls[a], mtyp=T)
    for q in range(pl.r):
        if pl.typ[q] == O:
            pl.add_link(m, T, q, T)          # Z'_m meets X'_q (both type T)
        elif pl.cls[q] != pl.cls[a]:
            pl.add_link(m, O, q, O)          # Z_m meets X'_b (both type O)
    for w in window:
        pl.add_link(m, T, w, pl.typ[w])      # Z'_m meets the member X_w (must be type T to count)
    return m


def finish(pl, rng):
    mates = sorted(pl.mtyp)
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            m1, m2 = mates[i], mates[j]
            if pl.cls[m1] == pl.cls[m2]:
                continue
            t1, t2 = pl.mtyp[m1], pl.mtyp[m2]
            if t1 == t2:
                pl.add_link(m1, t1, m2, t1)  # T-blob
            else:
                ty = rng.randrange(2)
                pl.add_link(m1, ty, m2, ty)


if __name__ == "__main__":
    import ast
    src = sys.argv[1]
    k = int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    txt = open(src).read()
    top = txt.split("top:")[1].strip()
    obj = ast.literal_eval(top)
    best, typ, cls, links = obj[0], obj[1], obj[2], obj[3]
    pl = plant.Planted(typ, cls)
    for L in links:
        pl.links.add(tuple(L))
    I, P = pl.realise()
    print("base: P2", C.p2_ok(I), "shortest", pl.shortest_ok(I, P), "guided(2,1)", fastdesc.guided(I, P, 2, 1))
    fs = costs.f_sets(I, P)
    Es = [a for a in range(pl.r) if typ[a] == 0]
    Fs = [a for a in range(pl.r) if typ[a] == 1]
    # dead mates for k E-classes and k F-classes (distinct classes)
    for a in Es[:k]:
        add_dead(pl, a)
    for a in Fs[:k]:
        add_dead(pl, a)
    finish(pl, rng)
    I, P = pl.realise()
    print("with dead mates: P2", C.p2_ok(I), "shortest", pl.shortest_ok(I, P), "classes", I.k, "switches", I.n)
    for f, g in ((1, 0), (1, 1), (2, 0), (2, 1)):
        print(" guided", f, g, fastdesc.guided(I, P, f, g, want=True), flush=True)
    if I.k <= 18:
        import cdesc2
        sols = cdesc2.solutions_masks(I)
        print(" solutions", len(sols), "exact desc(1,1)", cdesc2.desc_cost(I, 1, 1, sols))
