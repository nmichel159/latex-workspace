"""alg.decide(kd=1, ks=0, s=4, B=8) on R_L for L = LMIN..LMAX (yes-instances with a unique solution); the returned
walk is checked for validity.  Usage: python rigid_ks0.py LMIN LMAX"""
import sys
import gen
import alg
import sw

for L in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    inst, P = gen.rigid(L)
    r = alg.decide(inst, 1, 0, 4, 8, True)
    print(L, "accepted" if r[0] else "rejected", "walk valid" if r[0] and sw.is_valid_walk(inst, r[1][2]) else "", flush=True)
