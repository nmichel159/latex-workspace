"""Singleton PC on the hub instance H(2,2) for growing CSP length L (more slack).
Usage: python spc_slack.py L1 [L2 ...]"""
import sys
import time
import hubimp
import variants

if __name__ == "__main__":
    for strict in (False,):
        z, names = hubimp.hubimp(2, 2, strict=strict)
        for L in map(int, sys.argv[1:]):
            t0 = time.time()
            print("H(2,2) %s L=%d: SPC %s %.0fs" % ("strict" if strict else "classes", L, variants.spc(z, L),
                                                   time.time() - t0), flush=True)
