"""Show the shortcuts that kill planted instances, in path-position language.

usage: python diag_short.py seed count k m1 m2 l p_contact p_both
"""
import sys
import random
from collections import Counter
from planted import gen_planted
from core import shortest_valid_paths


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    k, m1, m2, l = map(int, sys.argv[3:7])
    pc, pb = float(sys.argv[7]), float(sys.argv[8])
    rng = random.Random(seed)
    pat = Counter()
    for _ in range(count):
        g = gen_planted(rng, k, m1, m2, l, T=0, p_contact=pc, p_both=pb, p_extra=0.0)
        if g is None:
            continue
        inst, P, T = g
        L, sp = shortest_valid_paths(inst, limit=1, maxlen=len(P))
        if L == len(P):
            continue
        Q = sp[0]
        posof = {inst.swof[x]: a for a, x in enumerate(P, 1)}
        word = ''.join('EF'[inst.typ[x]] for x in P)
        desc = []
        for y in Q:
            a = posof.get(inst.swof[y])
            if a is None:
                desc.append('off')
            elif y == P[a - 1]:
                desc.append('X%d' % a)
            else:
                desc.append("X'%d" % a)
        pat[(word, ' '.join(desc))] += 1
    for (w, d), c in pat.most_common(12):
        print(c, w, '|', d)


if __name__ == "__main__":
    main()
