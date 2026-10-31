"""Anchored closure descriptions (ADESC) for the general switch form (r5-core.md Section 5).

E-side description with F-anchors B0, E-anchors A0, centres Z_1..Z_f and flip set Phi:
    U = union of NE(Z_i)                       (switches whose non-empty E-side meets a centre)
    G = ((Enon - U) - down(B0)) xor Phi,  G := G | A0
    D = Q - up(G)                              (requires down(B0) <= D, i.e. A0 and G avoid down(B0))
F-side dually:
    U' = union of NF(Z_i),  G' = ((Fnon - U') - up(A0)) xor Phi,  G' := G' | B0,  D = down(G')
    (requires up(A0) & D = 0).
Every success is an order-consistent connecting mode vector (D is a down-set): soundness for all parameters.

Guided cost for a valid path P (completeness side).  E-side, for given B0 (F-anchors), A0 (E-anchors), U:
    L = down(W_F), A = minimal E-members,
    out = (L & Enon & ~U) - down(B0)             (elements of L that would be generators)
    G1  = (Enon & ~U) - down(B0) - L
    inn = {a in A : no element of G1 | A0 is <= a}
flipping `out` out of G and `inn` into G gives D with L <= D <= Q - up(W_E) (Lemma G with anchors), so
cost = |out| + |inn| flips suffice.  F-side dually with B = maximal F-members:
    out = (Up & Fnon & ~U') - up(A0),  G1' = (Fnon & ~U') - up(A0) - Up,
    inn = {b in B : no element of G1' | B0 is >= b}.
"""
import itertools
from gcore import bits, popcount
import cdesc


def up_closure(G, S):
    r = 0
    for w in bits(S):
        r |= G.up[w]
    return r


def down_closure(G, S):
    r = 0
    for w in bits(S):
        r |= G.dn[w]
    return r


def describe(G, side, B0, A0, U, Phi):
    """The down-set D of a description (None if the anchors are inconsistent)."""
    full = (1 << G.m) - 1
    En, Fn = cdesc.enon(G), cdesc.fnon(G)
    dB = down_closure(G, B0)
    uA = up_closure(G, A0)
    if dB & uA:
        return None
    if side == 0:
        g = (En & ~U) & ~dB
        g ^= Phi
        g |= A0
        if g & dB:
            return None
        return full & ~up_closure(G, g)
    g = (Fn & ~U) & ~uA
    g ^= Phi
    g |= B0
    if g & uA:
        return None
    return down_closure(G, g)


def path_data(G, P):
    return cdesc.path_data(G, P)


def guided_cost_E(G, pd, B0, A0, U, En):
    WE, WF, Up, L, A, B = pd
    dB = down_closure(G, B0)
    out = (L & En & ~U) & ~dB
    G1 = ((En & ~U) & ~dB) & ~L
    gen = G1 | A0
    inn = 0
    for a in bits(A):
        if not (G.dn[a] & gen):
            inn |= 1 << a
    return popcount(out) + popcount(inn), out, inn


def guided_cost_F(G, pd, B0, A0, U, Fn):
    WE, WF, Up, L, A, B = pd
    uA = up_closure(G, A0)
    out = (Up & Fn & ~U) & ~uA
    G1 = ((Fn & ~U) & ~uA) & ~Up
    gen = G1 | B0
    inn = 0
    for b in bits(B):
        if not (G.up[b] & gen):
            inn |= 1 << b
    return popcount(out) + popcount(inn), out, inn


def subsets(S, kmax):
    el = bits(S)
    for k in range(kmax + 1):
        for c in itertools.combinations(el, k):
            yield sum(1 << x for x in c)


def guided(G, P, fmax=2, amax=2, nodes=True, cs=None, budget=None):
    """Least total parameter count (anchors + centres + flips) of an anchored description of P, both sides.
    Anchors range over B (maximal F-members; E-side) and A (minimal E-members; F-side), at most amax of each kind
    on its natural side and at most 1 of the other kind.  Returns (total, side, B0, A0, centres, flips)."""
    pd = path_data(G, P)
    WE, WF, Up, L, A, B = pd
    En, Fn = cdesc.enon(G), cdesc.fnon(G)
    if cs is None:
        cs = (cdesc.centre_sets(G, 0, nodes), cdesc.centre_sets(G, 1, nodes))
    best = None
    for side in (0, 1):
        sets = cs[side]
        keys = list(sets.keys())
        nat, oth = (B, A) if side == 0 else (A, B)
        for X0 in subsets(nat, amax):
            for Y0 in subsets(oth, 1):
                B0, A0 = (X0, Y0) if side == 0 else (Y0, X0)
                na = popcount(X0) + popcount(Y0)
                if best is not None and na >= best[0]:
                    continue
                for f in range(fmax + 1):
                    if best is not None and na + f >= best[0]:
                        break
                    for combo in itertools.combinations(keys, f):
                        U = 0
                        for S in combo:
                            U |= S
                        if side == 0:
                            c = guided_cost_E(G, pd, B0, A0, U, En)[0]
                        else:
                            c = guided_cost_F(G, pd, B0, A0, U, Fn)[0]
                        tot = na + f + c
                        if best is None or tot < best[0]:
                            best = (tot, "EF"[side], B0, A0, tuple(sets[S] for S in combo), c)
    return best


def decide(G, fmax=1, amax=1, emax=0, nodes=True, want=False, sides=(0, 1)):
    """Exact enumeration of anchored descriptions with <= amax anchors of each kind (any switches), <= fmax
    centres, <= emax flips.  Sound."""
    if G.s == G.t:
        return (True, None) if want else True
    allsw = (1 << G.m) - 1
    seen = set()
    for side in sides:
        sets = cdesc.centre_sets(G, side, nodes)
        keys = list(sets.keys())
        for B0 in subsets(allsw, amax):
            for A0 in subsets(allsw, amax):
                if B0 & A0:
                    continue
                for f in range(fmax + 1):
                    for combo in itertools.combinations(keys, f):
                        U = 0
                        for S in combo:
                            U |= S
                        for e in range(emax + 1):
                            for Phi in itertools.combinations(range(G.m), e):
                                ph = sum(1 << w for w in Phi)
                                D = describe(G, side, B0, A0, U, ph)
                                if D is None or D in seen:
                                    continue
                                seen.add(D)
                                if G.connects(D):
                                    if want:
                                        return True, (side, B0, A0, tuple(sets[S] for S in combo), ph, D)
                                    return True
    return (False, None) if want else False
