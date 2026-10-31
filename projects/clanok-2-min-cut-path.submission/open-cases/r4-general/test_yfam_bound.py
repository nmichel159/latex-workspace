"""Theorem Y check: the generalized side-set search with parameters (kd, ks, s, B) rejects Y_k when
kd + ks + s < k and B < k, and accepts once B >= k (with one dominator and one declaration).
Usage: python test_yfam_bound.py K KD KS S B"""
import sys
import time
import common_r4  # noqa: F401
from yfam import yfam
from gsw import GSW

k, kd, ks, s, B = (int(a) for a in sys.argv[1:6])
t0 = time.time()
I, names, info = yfam(k)
G = GSW(I)
st = {}
r = G.decide(kd, ks, s, B, stats=st)
print("Y_%d q=%d switches=%d sides=%d params=(%d,%d,%d,%d) accepted=%s K-pairs tried=%d %.1fs"
      % (k, I.n, G.m, len(G.sides), kd, ks, s, B, r, st.get("tried", 0), time.time() - t0), flush=True)
