"""Re-check every instance stored in runs/*.jsonl (AC false positives of the hunts): exact answer (exact_dfs and,
for n <= 22, all down-sets), P2, AC and PC with the full length L = largest odd number <= n.
Usage: python recheck_acfp.py WORKERS OUTFILE"""
import os
import sys
import glob
import json
import time
from multiprocessing import Pool

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import pcfast  # noqa: E402


def check(args):
    fname, lineno, rec = args
    le = [[bool(x) for x in row] for row in rec["le"]]
    n = rec["n"]
    # records of hunt-sw-seed1-acfp.jsonl carry no u, v: switch model of zz.from_sw, u = 0, v = first top
    u = rec.get("u", 0)
    v = rec.get("v", min(x for x in range(n) if all(le[y][x] for y in range(n))))
    z = zz.ZZ(n, None, [tuple(e) for e in rec["R"]], u, v, le=le)
    t0 = time.time()
    ex = zz.exact_dfs(z)[0]
    ex2 = zz.exact(z)[0] if z.n <= 22 else None
    p2 = not z.p2_bad()
    ac = zz.ac_answer(z)
    pc = pcfast.pc_answer(z) if ac else False
    return (os.path.basename(fname), lineno, rec["mode"], z.n, len(z.R), p2, ex, ex2, ac, pc, time.time() - t0)


if __name__ == "__main__":
    workers, out = int(sys.argv[1]), sys.argv[2]
    jobs = []
    for f in sorted(glob.glob(os.path.join(HERE, "runs", "*.jsonl"))):
        for i, line in enumerate(open(f)):
            jobs.append((f, i, json.loads(line)))
    jobs.sort(key=lambda j: j[2]["n"])
    tally = {}
    with Pool(workers) as pool, open(out, "w") as fo:
        for r in pool.imap_unordered(check, jobs):
            fname, i, mode, n, m, p2, ex, ex2, ac, pc, dt = r
            fo.write("%-26s %3d %-7s n=%3d |R|=%3d P2=%-5s exact=%-5s exact2=%-5s AC=%-5s PC=%-5s %6.1fs\n"
                     % (fname, i, mode, n, m, p2, ex, ex2, ac, pc, dt))
            fo.flush()
            key = (mode, p2, ex, ac, pc)
            tally[key] = tally.get(key, 0) + 1
        fo.write("\nTally (mode, P2, exact, AC, PC): count\n")
        for k in sorted(tally, key=str):
            fo.write("%s: %d\n" % (k, tally[k]))
