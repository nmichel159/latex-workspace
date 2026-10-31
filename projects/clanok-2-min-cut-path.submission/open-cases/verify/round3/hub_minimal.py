"""dc-algorithm.md §6.5 (minimality of H(2,2)), own check (agent verify-round3): every deletion of one element other
than u, v, or of one real edge, that keeps P2 and the answer "no": does PC (L = largest odd <= q) still pass?
Usage: python hub_minimal.py version"""
import sys

import numpy as np

from hub3 import hub
from r3core import Inst


def delete_element(inst, x):
    keep = [y for y in range(inst.q) if y != x]
    pos = {y: i for i, y in enumerate(keep)}
    le = inst.le[np.ix_(keep, keep)]
    R = [(pos[a], pos[b]) for (a, b) in inst.R if a != x and b != x]
    return Inst(len(keep), le, R, pos[inst.u], pos[inst.v], names=[inst.names[y] for y in keep])


if __name__ == "__main__":
    ver = sys.argv[1]
    H = hub(2, 2, ver)
    res = []
    for x in range(H.q):
        if x in (H.u, H.v):
            continue
        I = delete_element(H, x)
        res.append(("element " + H.names[x], I))
    for e in H.R:
        I = Inst(H.q, H.le, [f for f in H.R if f != e], H.u, H.v, names=H.names)
        res.append(("edge %s-%s" % (H.names[e[0]], H.names[e[1]]), I))
    survivors = []
    for name, I in res:
        I.check()
        p2 = I.p2()
        ans = I.solve_downsets()[0] if p2 else None
        L = I.q if I.q % 2 == 1 else I.q - 1
        pc = I.pc(L) if (p2 and not ans) else None
        print("%-26s P2=%s answer=%s PC(L=%d)=%s" % (name, p2, ans, L, pc), flush=True)
        if p2 and not ans and pc:
            survivors.append(name)
    print("deletions keeping P2, answer no and PC yes:", survivors)
