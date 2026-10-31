"""Closure-based mode descriptions (CDESC) for the general switch form (r5-core.md Section 3).

A *description* on the E-side with centres Z_1..Z_f (sides or single nodes) and a flip set Phi:
    U    = union of the switch sets NE(Z_i) = {w : E_w != 0 and E_w meets Z_i}
    G    = (Enon - U) symmetric-difference Phi,         Enon = {w : E_w != 0}
    D    = Q - up(G)                                     (a down-set; switches of D are in F-mode)
On the F-side:  U' = union of NF(Z_i) = {w : F_w != 0, F_w meets Z_i},  G' = (Fnon - U') xor Phi,  D = down(G').
The description *succeeds* if D connects s and t.  Every success is a genuine solution (soundness is trivial: a
concrete order-consistent mode vector is tested).

Guided cost (completeness side).  For a valid path P with E-members W_E, F-members W_F, L = down(W_F), Up = up(W_E),
A = minimal elements of W_E, B = maximal elements of W_F, every down-set D with L <= D <= Q - Up picks all members of P.
E-side, given U:  out = L & Enon - U  (members of L that G would wrongly contain),
                  G1  = (Enon - U) - L,  in = {a in A : no element of G1 below a};
flipping out of G the set `out` and into G the set `in` gives D with L <= D <= Q - Up, so
cost_E(P, U) = |out| + |in| flips suffice.  F-side dually.  The guided cost is an upper bound for the least flip
number of a successful description; `decide` is the exact (exponential in f, e) enumeration.
"""
import itertools
from gcore import bits, popcount


def centre_sets(G, typ, nodes=True):
    """Distinct switch masks N_typ(Z) for Z over all sides (and single nodes if `nodes`).  typ 0 = E, 1 = F."""
    m = G.m
    side_mask = G.E if typ == 0 else G.F
    out = {}
    cents = [(("side", i), G.mask(i)) for i in G.sides]
    if nodes:
        cents += [(("node", x), 1 << x) for x in range(G.N)]
    for name, zm in cents:
        S = 0
        for w in range(m):
            if side_mask[w] and side_mask[w] & zm:
                S |= 1 << w
        if S and S not in out:
            out[S] = name
    return out


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


def path_data(G, P):
    WE = sum(1 << (i >> 1) for i in P if not i & 1)
    WF = sum(1 << (i >> 1) for i in P if i & 1)
    Up = up_closure(G, WE)
    L = down_closure(G, WF)
    assert not (Up & L)
    A = 0
    for a in bits(WE):
        # a minimal in W_E: no b in W_E strictly below a
        if not any(b != a and G.le[b][a] and not G.le[a][b] for b in bits(WE)):
            A |= 1 << a
    B = 0
    for b in bits(WF):
        if not any(c != b and G.le[b][c] and not G.le[c][b] for c in bits(WF)):
            B |= 1 << b
    return WE, WF, Up, L, A, B


def enon(G):
    return sum(1 << w for w in range(G.m) if G.E[w])


def fnon(G):
    return sum(1 << w for w in range(G.m) if G.F[w])


def cost_E(G, pd, U, En):
    WE, WF, Up, L, A, B = pd
    out = L & En & ~U
    G1 = (En & ~U) & ~L
    inn = 0
    for a in bits(A):
        if not (G.dn[a] & G1):
            inn |= 1 << a
    return popcount(out) + popcount(inn), out, inn


def cost_F(G, pd, U, Fn):
    WE, WF, Up, L, A, B = pd
    out = Up & Fn & ~U
    G1 = (Fn & ~U) & ~Up
    inn = 0
    for b in bits(B):
        if not (G.up[b] & G1):
            inn |= 1 << b
    return popcount(out) + popcount(inn), out, inn


def guided(G, P, fmax=2, nodes=True, cs=None):
    """Least flip cost over unions of <= fmax centre sets, both sides.  Returns dict f -> (cost, side, centres)."""
    pd = path_data(G, P)
    En, Fn = enon(G), fnon(G)
    if cs is None:
        cs = (centre_sets(G, 0, nodes), centre_sets(G, 1, nodes))
    res = {}
    for f in range(fmax + 1):
        best = None
        for side, (sets, costf, nonm) in enumerate(((cs[0], cost_E, En), (cs[1], cost_F, Fn))):
            keys = list(sets.keys())
            for combo in itertools.combinations(keys, f):
                U = 0
                for S in combo:
                    U |= S
                c = costf(G, pd, U, nonm)[0]
                if best is None or c < best[0]:
                    best = (c, "EF"[side], tuple(sets[S] for S in combo))
        res[f] = best
    return res


def connects_D(G, D):
    return G.connects(D)


def decide(G, fmax=1, emax=1, nodes=True, flip_pool=None, want=False):
    """Exact enumeration of descriptions with <= fmax centres and <= emax flips, both sides.  Sound.
    flip_pool: switches allowed in flips (default all)."""
    if G.s == G.t:
        return (True, None) if want else True
    En, Fn = enon(G), fnon(G)
    pool = list(range(G.m)) if flip_pool is None else list(flip_pool)
    full = (1 << G.m) - 1
    seen = set()
    for side in (0, 1):
        sets = centre_sets(G, side, nodes)
        keys = list(sets.keys())
        for f in range(fmax + 1):
            for combo in itertools.combinations(keys, f):
                U = 0
                for S in combo:
                    U |= S
                base = (En if side == 0 else Fn) & ~U
                for e in range(emax + 1):
                    for Phi in itertools.combinations(pool, e):
                        Gm = base
                        for w in Phi:
                            Gm ^= 1 << w
                        if side == 0:
                            D = full & ~up_closure(G, Gm)
                        else:
                            D = down_closure(G, Gm)
                        if D in seen:
                            continue
                        seen.add(D)
                        if G.connects(D):
                            if want:
                                return True, (side, tuple(sets[S] for S in combo), Phi, D)
                            return True
    return (False, None) if want else False
