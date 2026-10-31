"""NG on the known hard families and on the instances of r4-search (read-only).

Usage: python test_ng_families.py [budget] [s]
For every instance: q, |R|, P2, exact answer (gcert.exact), NG result (side, pins, number of down-sets tried), and a
re-check of the returned down-set.
"""
import os
import sys
import time
import glob
from common_r4 import OC, gcert, from_zz, load_json, check_solution, exact
import families
import ladder
import hubimp
from ng import ng

budget = int(sys.argv[1]) if len(sys.argv) > 1 else 2
s = int(sys.argv[2]) if len(sys.argv) > 2 else 0


def run(name, I, known=None):
    t0 = time.time()
    p2 = I.p2()
    ex = exact(I) if known is None else known
    st = {}
    r = ng(I, budget, s, stats=st)
    ok = None
    if r is not None:
        ok = check_solution(I, r[1])
    desc = "-" if r is None else "%s pins Gamma=%s Pi=%s Y=%s" % (r[0], r[3][0], r[3][1], r[3][2])
    flag = ""
    if r is not None and not ok:
        flag = "  <-- INVALID"
    if r is None and ex:
        flag = "  (NG fails)"
    if r is not None and not ex:
        flag = "  <-- UNSOUND"
    print("%-28s q=%3d |R|=%3d P2=%-5s exact=%-5s NG=%-5s tried=%6d %6.1fs %s%s"
          % (name, I.n, len(I.R), p2, ex, r is not None, st.get("tried", 0), time.time() - t0, desc, flag),
          flush=True)


def main():
    print("NG budget=%d s=%d" % (budget, s))
    for L in range(2, 9):
        for m in ("tie", "oneway"):
            I, names, info = families.tic_rigid(L, m)
            run("T_%d^%s" % (L, m), I, known=True if L >= 7 else None)
    for L in range(2, 9):
        for helly in (True, False):
            I, names, info = families.rigid(L, None, helly)
            run("R_%d %s" % (L, "helly" if helly else "2CH"), I, known=True if L >= 7 else None)
        for m in ("tie", "oneway"):
            I, names, info = families.rigid(L, m, True)
            run("R_%d helly mates %s" % (L, m), I, known=True if L >= 6 else None)
    for k in range(2, 7):
        for hubs in (False, True):
            z, path, A, B = ladder.ladder(k, hubs)
            run("K(%d)%s" % (k, " hubs" if hubs else ""), from_zz(z))
    for m, mp in [(1, 1), (2, 2), (2, 3)]:
        for strict in (False, True):
            z, names = hubimp.hubimp(m, mp, strict=strict)
            run("H(%d,%d) %s" % (m, mp, "po" if strict else "classes"), from_zz(z), known=False)
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        I, d = load_json(f)
        run(os.path.basename(f)[:-5], I, known=True if I.n > 30 else None)


if __name__ == "__main__":
    main()
