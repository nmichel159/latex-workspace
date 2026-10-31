"""Diagnostics for the planted generator: why instances are discarded and where Theorem 8 stops for the planted T.

usage: python diag.py seed count k m1 m2 l p_contact p_extra
"""
import sys
import random
from collections import Counter
from planted import gen_planted, is_shortest
from core import shortest_valid_paths
from proof import Ctx, theorem8, straddles, check_path, ClaimFailure


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    k, m1, m2, l = map(int, sys.argv[3:7])
    pc, pe = float(sys.argv[7]), float(sys.argv[8])
    rng = random.Random(seed)
    cnt = Counter()
    for _ in range(count):
        g = gen_planted(rng, k, m1, m2, l, T=0, p_contact=pc, p_both=float(sys.argv[9]) if len(sys.argv) > 9 else 0.0, p_extra=pe)
        if g is None:
            cnt["none"] += 1
            continue
        inst, P, T = g
        L, sp = shortest_valid_paths(inst, limit=1, maxlen=len(P))
        if L < len(P):
            cnt["shortcut"] += 1
            continue
        ctx = Ctx(inst, P)
        if straddles(ctx, T):
            cnt["straddle"] += 1
        st = {}
        try:
            check_path(inst, P, st)
            Zs, singles, step = theorem8(ctx, T, {}) if not straddles(ctx, T) else (None, None, 's')
        except ClaimFailure as e:
            cnt["FAIL " + str(e.args[0][0])] += 1
            continue
        cnt["step %s" % step] += 1
        if step == 1:
            fs = [len(ctx.f(a)) for a in ctx.members(T)]
            cnt["min|f| %d" % min(fs)] += 1
    print(dict(cnt))


if __name__ == "__main__":
    main()
