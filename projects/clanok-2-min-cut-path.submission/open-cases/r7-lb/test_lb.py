"""Cross-check of lbcore.mincost against brute force (r7-lb.md Section 2).

usage: python test_lb.py SEED COUNT MMIN MMAX [CAP]
Random general switch-form instances with P2 (verify/rv-r6-core/gen8.random_sw, read-only import).  Checks:
  * yes/no: valid_pairs non-empty  <=>  some down-set connects (I.downsets() brute force);
  * every minimal pair (L, Up) comes from a connecting down-set: the down-set L itself misses Up and connects;
  * mincost(I) == brute_mincost(I, CAP) whenever either is <= CAP (brute: every term of total cost <= CAP);
  * the term returned by mincost is verified (term_D + connects on the original instance).
"""
import sys
import random
import time
from collections import Counter
import lbcore
from lbcore import valid_pairs, mincost, brute_mincost
import gen8


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    cap = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        m = rng.randint(mmin, mmax)
        I = gen8.random_sw(rng, m, rng.randint(2, 5), rng.choice([0.15, 0.25, 0.35]), rng.choice([0.2, 0.4, 0.6]),
                           rng.choice([0, 0.1]), rng.choice([0, 0.3, 0.6]))
        if I.s == I.t:
            continue
        brute_yes = any(I.connects(D) for D in I.downsets())
        pairs = valid_pairs(I)
        if bool(pairs) != brute_yes:
            st["YESNO MISMATCH"] += 1
            print("yes/no mismatch it=%d" % it, flush=True)
            continue
        if not brute_yes:
            st["no"] += 1
            continue
        st["yes"] += 1
        for (L, Up) in pairs:
            if (L & Up) or not I.connects(L):
                st["PAIR BAD"] += 1
                print("pair bad it=%d" % it, flush=True)
        r = mincost(I, cap=cap + 2)
        b = brute_mincost(I, cap)
        tot = r["total"]
        if not r.get("verified", False):
            st["NOT VERIFIED"] += 1
            print("not verified it=%d %r" % (it, r), flush=True)
        if isinstance(tot, int) and tot <= cap:
            ok = (b == tot)
        else:
            ok = (b is None)
        if not ok:
            st["COST MISMATCH"] += 1
            print("cost mismatch it=%d m=%d mincost=%r brute=%r" % (it, m, tot, b), flush=True)
        st["cost=%s" % tot] += 1
    print("test_lb seed %d count %d m %d-%d cap %d (%.0fs)" % (seed, count, mmin, mmax, cap, time.time() - t0))
    for k in sorted(st):
        print("  %-20s %d" % (k, st[k]))


if __name__ == "__main__":
    main()
