"""Rigid alternating family R_L of 2CH+P2 (= SW+P2) instances.

Switches x_1..x_L.  Path hyperedge h_k of x_k is E if k is odd, F if k is even; Fl(x_k) is the other one.
Nodes: s in h_1, t in h_L; y_k in h_k & h_{k+1} (k = 1..L-1);
z_{pq} in Fl(x_p) & h_q for p < q with q - p odd ('flip points right');
w_{pq} in Fl(x_p) & Fl(x_q) for p < q with q - p even.
Claim: P2 holds and the only connecting mode vector is the alternating one (all switches in path mode), so every
solution has ceil(L/2) E-switches and floor(L/2) F-switches.
Usage: python rigid.py LMAX"""
import sys
from twoch import solve, p2_ok, connected


def rigid(L):
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    path = [0] * (L + 1)
    flip = [0] * (L + 1)
    s = node("s")
    t = node("t")
    path[1] |= 1 << s
    path[L] |= 1 << t
    for k in range(1, L):
        y = node(("y", k))
        path[k] |= 1 << y
        path[k + 1] |= 1 << y
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                z = node(("z", p, q))
                flip[p] |= 1 << z
                path[q] |= 1 << z
            else:
                w = node(("w", p, q))
                flip[p] |= 1 << w
                flip[q] |= 1 << w
    E = [0] * L
    F = [0] * L
    for k in range(1, L + 1):
        if k % 2 == 1:
            E[k - 1], F[k - 1] = path[k], flip[k]
        else:
            F[k - 1], E[k - 1] = path[k], flip[k]
    return (len(nodes), E, F, s, t)


def all_solutions(inst):
    N, E, F, s, t = inst
    n = len(E)
    sols = []
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            sols.append(mask)
    return sols


if __name__ == "__main__":
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for L in range(2, LMAX + 1):
        inst = rigid(L)
        sols = all_solutions(inst)
        alt = sum(1 << (k - 1) for k in range(1, L + 1) if k % 2 == 0)
        print("L=%d nodes=%d P2=%s solutions=%d only-alternating=%s" % (
            L, inst[0], p2_ok(inst[1], inst[2]), len(sols), sols == [alt]), flush=True)
