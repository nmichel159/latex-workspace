"""Checks of Section 3 of r4-general.md.

1. Subdivision lemma: for random general ZZ + P2 instances and every R-edge y < x between two middle elements, the
   instance with the edge replaced by y - t_e - b_e - x (b_e ~ u, t_e ~ v new) has the same answer; P2 is kept iff the
   edge is not needed as a witness edge.
2. The 8-element example MW (a middle witness that no bottom witness can replace).
3. Search for instances in which a pair with only middle witnesses can be given neither a new bottom nor a new top
   witness without changing the answer.
Usage: python test_reductions.py SEED COUNT
"""
import sys
import random
from common_r4 import gcert, make, bits
import mixed
from common_r4 import from_zz

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)


def add_elements(I, nb, nt, newR):
    """New instance: I plus nb elements ~ u and nt elements ~ v (appended), plus edges newR (indices may refer to the
    new elements n, n+1, ...)."""
    n = I.n
    n2 = n + nb + nt
    newB = list(range(n, n + nb))
    newT = list(range(n + nb, n2))
    le = [[False] * n2 for _ in range(n2)]
    for a in range(n):
        for b in range(n):
            le[a][b] = I.le[a][b]
    for x in newB:
        for b in range(n2):
            le[x][b] = True
        for a in range(n):
            if I.le[a][I.u]:
                le[a][x] = True
    for x in newT:
        for a in range(n2):
            le[a][x] = True
        for b in range(n):
            if I.le[I.v][b]:
                le[x][b] = True
    for x in newB:
        for y in newB:
            le[x][y] = True
    for x in newT:
        for y in newT:
            le[x][y] = True
    R = list(I.R) + list(newR)
    return gcert.Inst(n2, le, R, I.u, I.v)


def subdivide(I, e):
    y, x = e
    J0 = gcert.Inst(I.n, I.le, [f for f in I.R if f != e], I.u, I.v)
    n = I.n
    b, t = n, n + 1
    return add_elements(J0, 1, 1, [(y, t), (b, t), (b, x)])


def middle_mask(I):
    return ((1 << I.n) - 1) & ~I.B & ~I.T


def check_sub():
    tested = kept = 0
    for it in range(count):
        I = gcert.random_inst(rng)
        if not I.p2():
            continue
        M = middle_mask(I)
        ex = gcert.exact(I)
        for e in I.R:
            if (M >> e[0]) & 1 and (M >> e[1]) & 1:
                J = subdivide(I, e)
                tested += 1
                if J.p2():
                    kept += 1
                ex2 = gcert.exact(J)
                if ex2 != ex:
                    print("SUBDIVISION CHANGED THE ANSWER", gcert.describe(I), e)
                    return
    print("subdivision: %d middle-middle edges subdivided, answer kept in all, P2 kept in %d" % (tested, kept))


def mw_example():
    # u=0, z=1, z'=2 (~u); p=3, w=4, x=5, y=6 (p < w < x, w < y); v=7
    n = 8
    le = [[a == b for b in range(n)] for a in range(n)]
    for a in (0, 1, 2):
        for b in range(n):
            le[a][b] = True
    for a in range(n):
        le[a][7] = True
    for a, b in ((3, 4), (4, 5), (4, 6), (3, 5), (3, 6)):
        le[a][b] = True
    R = [(0, 3), (1, 3), (1, 5), (4, 5), (4, 6), (2, 6), (2, 7)]
    I = gcert.Inst(n, le, R, 0, 7)
    Ib = add_elements(I, 1, 0, [(8, 5), (8, 6)])
    It = add_elements(I, 0, 1, [(5, 8), (6, 8)])
    print("MW example: P2 %s, answer %s; with a new bottom witness of x, y: P2 %s, answer %s; with a new top witness:"
          " P2 %s, answer %s" % (I.p2(), gcert.exact(I), Ib.p2(), gcert.exact(Ib), It.p2(), gcert.exact(It)))
    # MW2: add a = 7 with x < a < v and edges u-a, a-x, a-v, y-v: neither replacement keeps the answer
    n = 9
    le = [[a == b for b in range(n)] for a in range(n)]
    for a in (0, 1, 2):
        for b in range(n):
            le[a][b] = True
    for a in range(n):
        le[a][8] = True
    for a, b in ((3, 4), (4, 5), (4, 6), (3, 5), (3, 6), (5, 7), (4, 7), (3, 7)):
        le[a][b] = True
    R = [(0, 3), (1, 3), (1, 5), (4, 5), (4, 6), (2, 6), (2, 8), (0, 7), (5, 7), (7, 8), (6, 8)]
    I = gcert.Inst(n, le, R, 0, 8)
    print("MW2 (u=0; z, z' = 1, 2 ~ u; p=3 < w=4 < x=5, y=6; x < a=7; v=8): P2 %s, answer %s, common neighbours of x,"
          " y: below %s, above %s" % (I.p2(), gcert.exact(I), bits(I.lo[5] & I.lo[6]), bits(I.hi[5] & I.hi[6])))
    Ib = add_elements(I, 1, 0, [(9, 5), (9, 6)])
    It = add_elements(I, 0, 1, [(5, 9), (6, 9)])
    print("   with a new bottom witness of x, y: P2 %s, answer %s; with a new top witness: P2 %s, answer %s"
          % (Ib.p2(), gcert.exact(Ib, True), It.p2(), gcert.exact(It, True)))


def hunt_both():
    found = 0
    tried = 0
    for it in range(count):
        mode = rng.choice(["lower", "upper", "mixed"])
        I = from_zz(mixed.random_instance(rng, mode))
        if not I.p2():
            continue
        ex = gcert.exact(I)
        n = I.n
        for x in range(n):
            for y in range(x + 1, n):
                if I.le[x][y] or I.le[y][x]:
                    continue
                low = I.lo[x] & I.lo[y]
                up = I.hi[x] & I.hi[y]
                bt = (low & I.B) or (up & I.T)
                if bt or not (low | up):
                    continue
                # only middle witnesses
                tried += 1
                Ib = add_elements(I, 1, 0, [(n, x), (n, y)])
                It = add_elements(I, 0, 1, [(x, n), (y, n)])
                eb, et = gcert.exact(Ib), gcert.exact(It)
                if eb != ex and et != ex:
                    found += 1
                    if found <= 3:
                        print("pair", (x, y), "answer", ex, "bottom ->", eb, "top ->", et, ":", gcert.describe(I))
    print("pairs with only middle witnesses tested: %d; pairs where both replacements change the answer: %d"
          % (tried, found))


if __name__ == "__main__":
    mw_example()
    check_sub()
    hunt_both()
