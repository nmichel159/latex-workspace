"""Counterexample to Theorem 5.2 (E2) of r5-core.md as written, and test of the repair.

Instance: rigid word family R((EF)^n) of r4-general 6 (2CH form, no order, no middle edges) plus one node kap in
E(x_j) & F(x_j) for the F-members j listed in KAP.  P = h_1 .. h_2n is the unique valid path.
For a pair b1 = x_p, b2 = x_q of maximal F-members with q - p >= 5 the E-description of (E2) is evaluated:
B0 = {b1, b2}, centres E_b1, E_b2 in the instance with F_v (v in down(B0)) contracted, Phi = f*_A(b1) | f*_A(b2).
Also evaluated: centres in the uncontracted instance (no middle edges), and the repaired flip set Phi = A & U.

usage: python cex_e2.py n KAP(comma list of positions, or -)
"""
import sys
from fams import rword
from sw import path_data, describe, contracted_sets, NE, bits


def fstar(G, pd, b):
    """f*_A(b): a in A whose path side X_a meets E_b, or meets F_v for some v < b with F_v & E_b != 0."""
    r = 0
    for a in bits(pd["A"]):
        Xa = G.E[a]
        if Xa & G.E[b]:
            r |= 1 << a
            continue
        for v in range(G.m):
            if G.strict_lt(v, b) and G.F[v] & G.E[b] and G.F[v] & Xa:
                r |= 1 << a
                break
    return r


def run(n, kap):
    word = "EF" * n
    G = rword(word, kappa_F=kap)
    print("instance R(%s) with kap at %s: switches %d, nodes %d, P2 violations %d" % (
        word, kap, G.m, G.N, len(G.p2_violations())))
    sols = G.solutions()
    L, paths = G.shortest_valid_paths()
    print("solutions:", len(sols), " shortest valid length:", L, " number of shortest valid paths:", len(paths))
    P = paths[0]
    pd = path_data(G, P)
    names = lambda S: ",".join(G.names[w] for w in bits(S))
    fails = 0
    for p in range(2, 2 * n + 1, 2):
        for q in range(p + 6, 2 * n + 1, 2):     # same parity as p (F-members), distance >= 5
            b1, b2 = G.x[p], G.x[q]
            B0 = (1 << b1) | (1 << b2)
            dB = G.dnc(B0)
            Ec, Fc, mp = contracted_sets(G, [G.F[v] for v in bits(dB)])
            U = NE(G, Ec[b1], Ec) | NE(G, Ec[b2], Ec)
            Phi = fstar(G, pd, b1) | fstar(G, pd, b2)
            D = describe(G, "E", B0, 0, U, Phi)
            ok = D is not None and G.connects(D)
            U0 = NE(G, G.E[b1]) | NE(G, G.E[b2])
            D0 = describe(G, "E", B0, 0, U0, Phi)
            ok0 = D0 is not None and G.connects(D0)
            PhiR = pd["A"] & U
            DR = describe(G, "E", B0, 0, U, PhiR)
            okR = DR is not None and G.connects(DR)
            extra = (pd["A"] & U) & ~Phi
            print("b1=x%d b2=x%d: |Phi|=%d  contracted centres: %s  | uncontracted: %s | Phi = A & U (|.|=%d): %s"
                  "   A&U-Phi = {%s}" % (p, q, bin(Phi).count("1"), "succeeds" if ok else "FAILS (D = {%s})" % names(D),
                                       "succeeds" if ok0 else "FAILS", bin(PhiR).count("1"),
                                       "succeeds" if okR else "FAILS", names(extra)))
            fails += not ok
    print("failures of (E2) as written:", fails)


if __name__ == "__main__":
    n = int(sys.argv[1])
    kap = [] if sys.argv[2] == "-" else [int(x) for x in sys.argv[2].split(",")]
    run(n, kap)
