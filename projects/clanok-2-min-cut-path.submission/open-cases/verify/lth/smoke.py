"""Smoke tests of the own library on R_L (agent verify-LTH)."""
import sys
import time
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *
from families import *

maxL = int(sys.argv[1]) if len(sys.argv) > 1 else 8
for L in range(2, maxL + 1):
    t0 = time.time()
    inst, names = rigid_2ch(L)
    ok, sols = brute_2ch(inst, all_solutions=True)
    print("2CH R_%d: P2=%s unique-alternating=%s #sol=%d (%.1fs)" % (
        L, p2_2ch(inst), sols == [alternating_modes(L)], len(sols), time.time() - t0), flush=True)
for L in range(2, maxL + 1):
    t0 = time.time()
    K, sw = rigid_tic(L)
    ok, sols = brute_tic(K, sw, all_solutions=True)
    print("TIC R_%d: P2=%s unique-alternating=%s T=%s (%.1fs)" % (
        L, p2_tic(sw), sols == [alternating_modes(L)], tic_T(K, sw), time.time() - t0), flush=True)
