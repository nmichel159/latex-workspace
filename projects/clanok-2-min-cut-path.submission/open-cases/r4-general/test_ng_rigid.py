"""NG on the rigid family R_L of dc-hardness.md (2CH form without t in the flip sides), L = LMIN..LMAX.
Usage: python test_ng_rigid.py LMIN LMAX BUDGET"""
import sys
import time
from common_r4 import check_solution
import families
from ng import ng

lmin, lmax, budget = (int(a) for a in sys.argv[1:4])
for L in range(lmin, lmax + 1):
    I, names, info = families.rigid(L, None, False)
    t0 = time.time()
    st = {}
    r = ng(I, budget, 0, stats=st)
    ok = r is not None and check_solution(I, r[1])
    pins = "-" if r is None else "%s Pi=%s Y=%s" % (r[0], [names[p] for p in r[3][1]], [names[y] for y in r[3][2]])
    print("R_%d 2CH q=%d budget=%d NG=%s valid=%s tried=%d %.1fs %s"
          % (L, I.n, budget, r is not None, ok, st.get("tried", 0), time.time() - t0, pins), flush=True)
