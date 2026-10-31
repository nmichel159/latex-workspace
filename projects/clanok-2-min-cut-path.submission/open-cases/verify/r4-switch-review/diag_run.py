"""Shortcut patterns that kill gen_run instances (diagnostic only).

usage: python diag_run.py seed count m nl two_spans
"""
import sys
import random
from collections import Counter
from gen_run import gen_run
from core import shortest_valid_paths


def main():
    seed, count, m, nl, two = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed)
    pat = Counter()
    kept = 0
    for _ in range(count):
        g = gen_run(rng, ['O', 'O'], m, ['O'] * nl, T=0, pM=0.6, pB=0.2, two_spans=bool(two))
        if g is None:
            pat['pre'] += 1
            continue
        inst, P, T = g
        L, sp = shortest_valid_paths(inst, limit=1, maxlen=len(P))
        if L == len(P):
            kept += 1
            continue
        Q = sp[0]
        posof = {inst.swof[x]: a for a, x in enumerate(P, 1)}
        desc = []
        for y in Q:
            a = posof.get(inst.swof[y])
            desc.append('off' if a is None else ('X%d' % a if y == P[a - 1] else "X'%d" % a))
        # compress: show only the replaced parts
        pat[' '.join(desc)] += 1
    print('kept', kept)
    for d, c in pat.most_common(15):
        print(c, '|', d)


if __name__ == "__main__":
    main()
