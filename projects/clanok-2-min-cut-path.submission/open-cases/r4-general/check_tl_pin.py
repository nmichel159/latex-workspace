"""Check of §2.3 item 6: for T_L^tie and T_L^one the single pin Pi = {top of junction L} (with Gamma empty and
Y a set of at most two valley-capable lower neighbours of the pin) gives a solution down-set."""
import itertools
import common_r4  # noqa: F401
from common_r4 import gcert, bits, check_solution
import families
from ng import d_of

for L in range(2, 11):
    for m in ("tie", "oneway"):
        I, names, info = families.tic_rigid(L, m)
        pin = names.index(("t", L))
        NM = I.lo[pin]
        cands = [x for x in bits(NM) if I.hi[x] and not (I.B >> x) & 1]
        ok = None
        for a in range(0, 3):
            for Y in itertools.combinations(cands, a):
                D = d_of(I, 0, [pin], list(Y))
                if check_solution(I, D):
                    ok = [names[y] for y in Y]
                    break
            if ok is not None:
                break
        print("T_%d^%s pin t_%d: %s" % (L, m, L, "solution with Y = %s" % ok if ok is not None else "FAILS"))
