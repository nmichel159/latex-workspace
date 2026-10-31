"""Python wrapper of h1.js (Theorem H search, t = 1, same semantics as dc-hardness/helly2ch.helly_solve).
A persistent node process; falls back to helly2ch.helly_solve for instances with more than 30 sides.
Self-test: python h1fast.py SEED COUNT  (compares with helly2ch.helly_solve on random 2CH + P2 instances and R_L)."""
import os
import sys
import json
import subprocess
import atexit
from common import HERE, bits
import helly2ch

_proc = None


def _worker():
    global _proc
    if _proc is None or _proc.poll() is not None:
        _proc = subprocess.Popen(["node", os.path.join(HERE, "h1.js")], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, text=True, bufsize=1)
        atexit.register(_close)
    return _proc


def _close():
    global _proc
    if _proc is not None and _proc.poll() is None:
        _proc.stdin.close()
        _proc.wait(timeout=10)


def nsides(sw):
    N, E, F, s, t = sw
    return sum(1 for m in E if m) + sum(1 for m in F if m)


def h1(sw):
    N, E, F, s, t = sw
    if nsides(sw) > 30:
        return bool(helly2ch.helly_solve(sw))
    p = _worker()
    d = {"N": N, "s": s, "t": t, "E": [bits(m) for m in E], "F": [bits(m) for m in F]}
    p.stdin.write(json.dumps(d) + "\n")
    p.stdin.flush()
    out = json.loads(p.stdout.readline())
    if "error" in out:
        raise RuntimeError(out["error"])
    return bool(out["h1"])


if __name__ == "__main__":
    import random
    import time
    import twoch
    import known
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    agree = dis = 0
    yes = 0
    for it in range(count):
        sw = twoch.random_p2_instance(rng, rng.randint(3, 6), rng.randint(2, 8), rng.uniform(0.1, 0.4),
                                      rng.uniform(0.1, 0.4))
        if sw[0] > 10:
            continue
        a = h1(sw)
        b = bool(helly2ch.helly_solve(sw))
        if a == b:
            agree += 1
        else:
            dis += 1
            print("DISAGREE", sw, a, b, flush=True)
        yes += a
    print("random: agree %d disagree %d (h1 yes %d)" % (agree, dis, yes), flush=True)
    for L in range(2, 10):
        for hel in (False, True):
            name, z, names, sw = known.rigid_2ch(L, hel)
            t0 = time.time()
            a = h1(sw)
            t1 = time.time()
            b = bool(helly2ch.helly_solve(sw)) if L <= 8 else None
            t2 = time.time()
            print("%s: fast %s (%.2fs) helly2ch %s (%.2fs)" % (name, a, t1 - t0, b, t2 - t1), flush=True)
