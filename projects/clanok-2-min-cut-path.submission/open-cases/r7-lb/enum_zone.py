"""Agent r7-lb (2026-10-31): exhaustive search of the pure tournament zones E^k F^k (r7-lb.md Section 3.3).

usage: python enum_zone.py K LOG [AA] [BB] [PART NPARTS]
Every 0/1 matrix M of cross contacts (a_i b_j: EE if M[i][j] = 1, FF if 0); same-type pairs: a_i a_j = AA (default FF),
b_i b_j = BB (default EE); no extra switches, no relations.  zone.zone_genome builds the genome, design.build the
instance, lbcore.mincost the exact least single-term cost (minimum over all minimal pairs).  Records the distribution
of the cost, the number of minimal pairs and saves the first instance of every new maximum cost.
"""
import sys
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore
import zone

lbcore.WORK_CAP = 200000


def main():
    K = int(sys.argv[1])
    logp = sys.argv[2]
    aa = sys.argv[3] if len(sys.argv) > 3 else "FF"
    bb = sys.argv[4] if len(sys.argv) > 4 else "EE"
    part = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    nparts = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    os.makedirs(os.path.dirname(os.path.abspath(logp)), exist_ok=True)
    f = open(logp, "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        f.write(s + "\n")
        f.flush()
    say("enum_zone K %d aa %s bb %s part %d/%d pid %d" % (K, aa, bb, part, nparts, os.getpid()))
    t0 = time.time()
    hist = Counter()
    pairhist = Counter()
    best = -1
    n = K * K
    for code in range(part, 1 << n, nparts):
        M = [["E" if (code >> (i * K + j)) & 1 else "F" for j in range(K)] for i in range(K)]
        g = zone.zone_genome(K, M, aa=aa, bb=bb)
        I = design.build(g)
        if I is None:
            hist["invalid"] += 1
            continue
        pairs = lbcore.valid_pairs(I, state_cap=300000)
        if not pairs:
            hist["no"] += 1
            continue
        try:
            r = lbcore.mincost(I, cap=10, pairs=pairs)
        except RuntimeError:
            hist["workcap"] += 1
            continue
        c = r["total"] if isinstance(r["total"], int) else 99
        hist["cost%d" % c] += 1
        pairhist[(c, min(len(pairs), 5))] += 1
        if c > best:
            best = c
            design.save_genome(g, logp + ".max%d.json" % c, dict(code=code, cost=c, npairs=len(pairs)))
            lbcore.dump(I, logp + ".max%d-inst.json" % c, dict(code=code, cost=c, npairs=len(pairs)))
            say("  code %d new max cost %d npairs %d term %s (%.0fs)" % (code, c, len(pairs),
                                                                       (r["kind"], r["T"], r["Tp"], r["anchors"], r["flips"]), time.time() - t0))
    say("SUMMARY " + " ".join("%s:%d" % kv for kv in sorted(hist.items())) + " (%.0fs)" % (time.time() - t0))
    say("by (cost, min(npairs,5)): " + " ".join("%s:%d" % (k, v) for k, v in sorted(pairhist.items())))


if __name__ == "__main__":
    main()
