"""Run rigid_pc variants for one L (cut and tflip), for larger L in the background.
Usage: python rigid_pc_big.py L"""
import sys
from rigid_pc import rigid_named, run
L = int(sys.argv[1])
for k in range(1, L):
    run("cut(%d,%d)" % (L, k), rigid_named(L, drop_y=k))
for k in range(1, L):
    run("tflip(%d,%d)" % (L, k), rigid_named(L, t_in_flip=k))
