"""Refined side-set search (gsw.search_refined / decide_refined) on Y_k and Y'_k, plus the plain search on Y'_k,
NG, P2 and uniqueness of Y'_k.
Usage: python test_refined.py KMIN KMAX KD KS S B"""
import sys
import time
from common_r4 import gcert
from yfam import yfam
from xfam import brute
from gsw import GSW, decide_refined
from ng import ng

kmin, kmax, kd, ks, s, B = (int(a) for a in sys.argv[1:7])
for k in range(kmin, kmax + 1):
    for contact in (False, True):
        t0 = time.time()
        I, names, info = yfam(k, contact=contact)
        G = GSW(I)
        nsol = len(brute(info)) if len(info["E"]) <= 15 else None
        st = {}
        r = decide_refined(G, kd, ks, s, B, stats=st)
        plain = G.decide(kd, ks, s, B)
        ngr = ng(I, 2, 0) is not None
        print("%s_%d q=%d P2=%s solutions=%s exact=%s | refined%s=%s (tried %d) | plain=%s | NG(2)=%s | %.1fs"
              % ("Y'" if contact else "Y", k, I.n, I.p2(), nsol, gcert.exact(I), (kd, ks, s, B), r,
                 st.get("tried", 0), plain, ngr, time.time() - t0), flush=True)
