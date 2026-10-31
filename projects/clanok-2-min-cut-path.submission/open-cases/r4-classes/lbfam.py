"""Lower-bound family LB(K, R, M) for r5-classes descriptions (agent r4-classes).

Round-robin path P = (C_1 .. C_K)^R (K classes, R rounds, class j at positions (j-1) + K*rho, 0-based).
Word 'block' (default): C_1 .. C_{K/2} of type E, the rest of type F; word 'alt': alternating types.
Classes 1..K/2 are *after-choosers*, K/2+1..K *before-choosers*.
Links (private nodes, r5-classes/plant.py conventions):
  - consecutive members meet (structural y-links);
  - same type, different classes, distance >= 2: the partners meet;
  - after-chooser C_j: the partner of every member of C_j meets every member of every opposite-type class C_j', j' > j;
  - before-chooser C_j: the partner of every member of C_j meets every member of every opposite-type class C_j', j' < j;
    (this satisfies P2 for every opposite-type pair, see r4-classes.md);
  - M dead mates per class (r5-classes/deadmates.py: O-side meets the partners of the other-class members of the
    class's type, T-side meets the partners of all opposite-type members; T-blob between dead mates of the same type;
    a random same-type pair between dead mates of opposite types: the mate tournament).
build(K, R, M, seed) -> Planted (r5-classes/plant.py).
"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import plant  # noqa: E402  (read-only import)
import deadmates  # noqa: E402  (read-only import)


def base(K, R, choose=None, word="block"):
    typ, cls = [], []
    for rho in range(R):
        for j in range(K):
            if word == "block":
                typ.append(0 if j < K // 2 else 1)
            else:
                typ.append(0 if j % 2 == 0 else 1)
            cls.append(j)
    pl = plant.Planted(typ, cls)
    r = len(typ)
    if choose is None:
        choose = ["after" if j < K // 2 else "before" for j in range(K)]
    for a in range(r):
        for b in range(a + 2, r):
            if cls[a] != cls[b] and typ[a] == typ[b]:
                pl.add_link(a, 1 - typ[a], b, 1 - typ[b])
    for a in range(r):
        ja = cls[a]
        for b in range(r):
            if b == a or cls[b] == ja or typ[b] == typ[a]:
                continue
            jb = cls[b]
            if (choose[ja] == "after" and jb > ja) or (choose[ja] == "before" and jb < ja):
                pl.add_link(a, 1 - typ[a], b, typ[b])
    return pl


def build(K, R, M, seed, choose=None, word="block"):
    rng = random.Random(seed)
    pl = base(K, R, choose, word)
    first = {}
    for a in range(pl.r):
        first.setdefault(pl.cls[a], a)
    for j in range(K):
        for _ in range(M):
            deadmates.add_dead(pl, first[j])
    deadmates.finish(pl, rng)
    return pl
