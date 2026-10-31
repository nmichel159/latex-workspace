"""Smallest side-set parameters (gsw.decide) that solve given instances.
Usage: python min_cert.py FILE.json [FILE.json ...]   (r4-search JSON format)"""
import sys
import time
from common_r4 import load_json, gcert
from gsw import GSW

LADDER = [(1, 0, 2, 6), (1, 1, 4, 8), (2, 0, 4, 8), (2, 1, 4, 10), (2, 2, 6, 12), (3, 2, 6, 14), (3, 3, 8, 16),
          (4, 4, 10, 20)]


def minimal(I, ladder=LADDER):
    G = GSW(I)
    for par in ladder:
        st = {}
        r = G.decide(*par, want_walk=True, stats=st)
        if r[0]:
            return par, r[1]
    return None, None


if __name__ == "__main__":
    for f in sys.argv[1:]:
        I, d = load_json(f)
        t0 = time.time()
        par, cert = minimal(I)
        print("%s q=%d exact=%s minimal params=%s cert=%s %.1fs" % (f.split("/")[-1].split("\\")[-1], I.n,
                                                                  gcert.exact(I), par, cert, time.time() - t0),
              flush=True)
