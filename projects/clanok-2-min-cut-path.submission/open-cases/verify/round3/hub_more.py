"""Other members of the hub family (dc-algorithm.md §6.3, §7): PC at L = largest odd <= q, exact answer, P2,
Theorem F algorithm (agent verify-round3). Usage: python hub_more.py"""
import time
from hub3 import hub

if __name__ == "__main__":
    for (m, mp) in [(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 3)]:
        for ver in ('classes', 'po'):
            t0 = time.time()
            H = hub(m, mp, ver)
            H.check()
            L = H.q if H.q % 2 == 1 else H.q - 1
            ans, D, nd = H.solve_downsets()
            line = "H(%d,%d) %s: q=%d |R|=%d P2=%s downsets=%d answer=%s bottomwit=%s thmF=%s" % (
                m, mp, ver, H.q, len(H.R), H.p2(), nd, ans, H.bottom_witness_ok(), H.thmF()[0])
            if H.q <= 29:
                line += " AC(L=%d)=%s PC(L=%d)=%s" % (L, H.ac(L)[0], L, H.pc(L))
            print(line + " (%.0fs)" % (time.time() - t0), flush=True)
