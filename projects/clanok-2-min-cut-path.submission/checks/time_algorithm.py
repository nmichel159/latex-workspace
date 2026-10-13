"""Running time of algorithm.py (S11) on long chains of squares: evidence for the linear bound, not a proof.

Chains of k squares (2-edge-connected squares with at most five vertices, random terminals, pairs of general paths with
links) have c(u,v) = 2 by construction.  For each k the algorithm is timed in a fresh Python process (best of 5 runs,
Python's garbage collector switched off, because its cost grows with the number of live objects and would hide the
behavior of the algorithm itself; the speed of a long-lived process also drifts with the state of its memory
allocator, which is why every size gets its own process).  The algorithm normally stops at the first path it finds;
here it examines every square (exhaustive=True), the worst case.  The exponent is the slope of log(time) against
log(n + m) between the smallest and the largest instance (1 = linear).  The numbers depend on the machine.

Run:  python time_algorithm.py
Output: results-timing.txt
"""

import gc
import json
import math
import os
import random
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ROBUST = ["K1", "K3", "C4", "K4-e", "K4", "C5", "W4", "K23"]


def one(k):
    from mcp import Gr
    import algorithm
    import chains
    rng = random.Random(7)
    B, u, v, _ = chains.build_chain(rng, k, lambda r: chains.NAMED[r.choice(ROBUST)], crossing=0.2)
    g = Gr(B.n, B.edges)
    res = algorithm.solve(g, u, v, exhaustive=True)
    assert res is not None and res["c"] == 2, "the timing instance must have c(u,v) = 2"
    best = 1e9
    for _ in range(5):
        gc.disable()
        t = time.perf_counter()
        algorithm.solve(g, u, v, exhaustive=True)
        best = min(best, time.perf_counter() - t)
        gc.enable()
    print(json.dumps(dict(k=k, n=g.n, m=g.m, seconds=best, squares=len(res["squares"]), c=res["c"],
                          plus_one=res["cp"] != res["d"])))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--one":
        one(int(sys.argv[2]))
        return
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    out("time_algorithm.py: algorithm.solve on chains of k squares (fresh process per size, garbage collector off, best of 5 runs)")
    out("%8s %10s %10s %12s %20s   %s" % ("k", "vertices", "edges", "seconds", "microseconds/(n+m)", "result"))
    rows = []
    for k in (500, 1000, 2000, 4000, 8000, 16000, 32000):
        p = subprocess.run([sys.executable, "-B", os.path.join(HERE, "time_algorithm.py"), "--one", str(k)],
                           capture_output=True, text=True, check=True)
        r = json.loads(p.stdout.strip().splitlines()[-1])
        rows.append((r["n"] + r["m"], r["seconds"]))
        out("%8d %10d %10d %12.3f %20.2f   c = %d, %d squares, cp = d%s" % (
            k, r["n"], r["m"], r["seconds"], 1e6 * r["seconds"] / (r["n"] + r["m"]), r["c"], r["squares"], " + 1" if r["plus_one"] else ""))
    slope = math.log(rows[-1][1] / rows[0][1]) / math.log(rows[-1][0] / rows[0][0])
    out("")
    out("exponent between the smallest and the largest instance: %.2f" % slope)
    with open(os.path.join(HERE, "results-timing.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
