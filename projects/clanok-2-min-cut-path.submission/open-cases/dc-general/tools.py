"""Shared tools of agent DC-general: fast exact solver for 2CHC (branch and bound over class modes), shortest relaxed
zigzag length, AC / PC wrappers with a chosen number of CSP positions L (dc-algorithm/zz.py, pcfast.py, read-only).

PC / AC with fewer positions: a solution of the path-position CSP with L positions pads to L' >= L positions (repeat the
last edge), and the PC-closed network for L lifts to a PC-closed sub-network for L' (position j of L' -> min(j, L)).  So
"PC_L says yes" implies "PC_L' says yes" for L' >= L, in particular for the default L of dc-algorithm (largest odd <= n).
A no-instance with PC_L = yes is therefore a false positive of the dc-algorithm PC test.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
import zz  # noqa: E402
import pcfast  # noqa: E402
from gzz import connected, bits_of, classes  # noqa: E402


def bb_solve(inst):
    """Exact 2CHC answer by branch and bound: classes are fixed one at a time (in order of first contact with the
    component of s); a branch is cut when s and t are disconnected even with both sides of all unfixed classes."""
    N, E, F, cls, s, t = inst
    K = classes(inst)
    members = {c: [i for i in range(len(E)) if cls[i] == c] for c in K}

    def relaxed_ok(modes):
        hyper = []
        for i in range(len(E)):
            m = modes.get(cls[i])
            if m is None:
                hyper.append(E[i])
                hyper.append(F[i])
            else:
                hyper.append(F[i] if m else E[i])
        return connected(hyper, s, t)

    def comp_of_s(modes):
        comp = 1 << s
        hyper = [(F[i] if modes[cls[i]] else E[i]) for i in range(len(E)) if cls[i] in modes]
        changed = True
        while changed:
            changed = False
            for h in hyper:
                if h & comp and h | comp != comp:
                    comp |= h
                    changed = True
        return comp

    def rec(modes):
        if not relaxed_ok(modes):
            return None
        free = [c for c in K if c not in modes]
        if not free:
            return dict(modes)
        comp = comp_of_s(modes)
        if (comp >> t) & 1:
            return dict(modes)
        # pick a free class touching the component of s, else any
        pick = None
        for c in free:
            if any((E[i] | F[i]) & comp for i in members[c]):
                pick = c
                break
        if pick is None:
            pick = free[0]
        for m in (0, 1):
            modes[pick] = m
            r = rec(modes)
            del modes[pick]
            if r is not None:
                return r
        return None

    return rec({})


def shortest_relaxed_L(z):
    """Length of a shortest alternating u-v walk of the ZZ instance (consistency ignored), or None."""
    from collections import deque
    adj = z.adj()
    lt = z.lt
    start = (z.u, 1)   # role 1 = valley
    dist = {start: 0}
    dq = deque([start])
    while dq:
        x, val = dq.popleft()
        for y in adj[x]:
            if val and lt[x][y]:
                st = (y, 0)
                if y == z.v:
                    return dist[(x, val)] + 1
            elif not val and lt[y][x]:
                st = (y, 1)
            else:
                continue
            if st not in dist:
                dist[st] = dist[(x, val)] + 1
                dq.append(st)
    return None


def ac_L(z, L):
    csp = zz.CSP(z, L)
    return zz.arc_consistency(csp, csp.init_domains()) is not None


def pc_L(z, L):
    return pcfast.pc_answer(z, L)
