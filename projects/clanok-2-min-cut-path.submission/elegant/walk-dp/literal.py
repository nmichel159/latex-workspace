"""Fixing a literal keeps P2.  x in D: the down-closure of x moves into the class of u.  x not in D: the up-closure of x moves into the class of v.  Edges that stop being strict are removed.

Proof that P2 stays (see the report): let p, q be incomparable in the new order.  Then neither lies in the moved set, the order on the rest is unchanged, so they were incomparable before.  A lower
witness z of p, q stays a lower witness: z < p, q still holds if z moved (it is now in the class of u and p, q are not), and otherwise nothing changed.  An upper witness z satisfies p, q < z; if z had
moved (x in D case), then p, q <= z <= x would have moved too.  The other literal is dual.
"""
from wd import Inst, bits


def fix_low(I, x):
    """x in D.  Returns a new Inst (same element numbers)."""
    M = I.DN[x] | I.CL[I.u]
    if M >> I.v & 1:
        return None
    up = list(I.UP)
    for y in bits(M):
        up[y] = I.ALL
    # elements outside M keep their up-sets, minus nothing: M is a down-set, so no outside element is below an element of M
    edges = {(a, b) for a, b in I.edges if not (M >> a & 1 and M >> b & 1)}
    J = Inst(I.m, up, edges, I.u, I.v, I.names)
    return J


def fix_high(I, x):
    """x not in D."""
    M = I.UP[x] | I.CL[I.v]
    if M >> I.u & 1:
        return None
    up = list(I.UP)
    for y in range(I.m):
        if M >> y & 1:
            up[y] = M
        else:
            up[y] |= M
    edges = {(a, b) for a, b in I.edges if not (M >> a & 1 and M >> b & 1)}
    J = Inst(I.m, up, edges, I.u, I.v, I.names)
    return J
