"""Generalized closure descriptions GDESC (r5-core.md Section 6): sibling-star centres, anchors, strict anchors, flips.

E-description with tool switches T (each with a flag 'strict anchor'), F-anchors Y0 and flip-in set Phi:
    U = union over x in T of NE(Estar(x))
    S = union over y in Y0 of down(y)  united with  union over flagged x in T of (down(x) - [x])
    G = ((Enon - U - S) | Phi),   D = Q - up(G)
F-description dually (U' from Fstar, S' from up-sets, D = down(G')).
Every tested D is a down-set, so an accepting run is sound for all parameters.
Guided cost of a valid path P (completeness side): an ILP over the cheap tools of gstar.cheap_tools that covers all
needed items and pays one flip for every minimal E-member (maximal F-member) caught by a chosen centre; the solution
is turned into an explicit description and verified to pick every member of P.
"""
import itertools
from gcore import bits, popcount
import gstar
from gstar import Stars, Skel, strict_down, strict_up


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


def enon(G):
    return sum(1 << w for w in range(G.m) if G.E[w])


def fnon(G):
    return sum(1 << w for w in range(G.m) if G.F[w])


def describe(G, St, kind, T, flags, Y0, Phi):
    """kind 0: E-description, kind 1: F-description.  T: list of tool switches, flags: set of flagged tools,
    Y0: list of anchor switches, Phi: switch mask of flips (added to the generators).  Returns D (mask)."""
    full = (1 << G.m) - 1
    if kind == 0:
        U = 0
        for x in T:
            U |= St.NEstar[x]
        Sx = 0
        for y in Y0:
            Sx |= G.dn[y]
        for x in flags:
            Sx |= strict_down(G, x)
        gen = (enon(G) & ~U & ~Sx) | Phi
        return full & ~up_closure(G, gen)
    U = 0
    for y in T:
        U |= St.NFstar[y]
    Sx = 0
    for x in Y0:
        Sx |= G.up[x]
    for y in flags:
        Sx |= strict_up(G, y)
    gen = (fnon(G) & ~U & ~Sx) | Phi
    return down_closure(G, gen)


def picks(G, K, D):
    return (K.L & ~D) == 0 and (K.Up & D) == 0


def guided(G, P, St=None, K=None, weights=(1, 1, 1), timeout=20):
    """Least weighted cost (tools, anchors, flips) of a GDESC description picking P, both kinds, by ILP.
    Returns dict with 'cost', 'kind', 'tools', 'flagged', 'anchors', 'flips', 'verified'."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    import numpy as np
    if St is None:
        St = Stars(G)
    if K is None:
        K = Skel(G, P)
    best = None
    for kind in (0, 1):
        items = bits(K.NE if kind == 0 else K.NF)
        ext = K.A if kind == 0 else K.B            # extremal members that a centre may catch
        tools = gstar.cheap_tools(G, St, K, kind, anchors=True)
        # variables: one per tool, one per extremal member (flip)
        exts = bits(ext)
        nt, nx = len(tools), len(exts)
        if not items:
            cand = dict(cost=0, kind=kind, tools=[], flagged=[], anchors=[], flips=[])
        else:
            nv = nt + nx
            c = np.zeros(nv)
            rows, lbs = [], []
            for j, (mask, lab) in enumerate(tools):
                c[j] = weights[0] if lab[0] in ("E", "F") else weights[1]
            for i in range(nx):
                c[nt + i] = weights[2]
            for it in items:
                row = np.zeros(nv)
                for j, (mask, lab) in enumerate(tools):
                    if (mask >> it) & 1:
                        row[j] = 1
                rows.append(row)
                lbs.append(1)
            # flip_a >= tool_j whenever the centre of tool j catches a
            for j, (mask, lab) in enumerate(tools):
                if lab[0] not in ("E", "F"):
                    continue
                w = lab[1]
                caught = (St.NEstar[w] if kind == 0 else St.NFstar[w]) & ext
                for i, a in enumerate(exts):
                    if (caught >> a) & 1:
                        row = np.zeros(nv)
                        row[nt + i] = 1
                        row[j] = -1
                        rows.append(row)
                        lbs.append(0)
            Amat = np.array(rows)
            r = milp(c, constraints=LinearConstraint(Amat, lb=np.array(lbs), ub=np.inf),
                     integrality=np.ones(nv), bounds=Bounds(0, 1), options={"time_limit": timeout})
            if not r.success:
                continue
            xs = np.round(r.x).astype(int)
            chosen = [tools[j][1] for j in range(nt) if xs[j]]
            flips = [exts[i] for i in range(nx) if xs[nt + i]]
            cand = dict(cost=int(round(r.fun)), kind=kind,
                        tools=[lab[1] for lab in chosen if lab[0] in ("E", "F")],
                        anchors=[lab[1] for lab in chosen if lab[0] == "anc"], flips=flips)
            cand["flagged"] = [w for w in cand["tools"] if ((K.A if kind == 0 else K.B) >> w) & 1]
        D = describe(G, St, kind, cand["tools"], cand["flagged"], cand["anchors"], sum(1 << a for a in cand["flips"]))
        cand["verified"] = picks(G, K, D) and G.connects(D)
        if best is None or cand["cost"] < best["cost"]:
            best = cand
    return best


def decide(G, k=1, a=1, e=2, St=None, want=False):
    """Exhaustive GDESC with <= k tools (any switches, any flags), <= a anchors, <= e flips (flips drawn from the
    switches caught by the chosen centres, the only ones Theorem 6.5 needs).  Sound."""
    if G.s == G.t:
        return (True, None) if want else True
    if St is None:
        St = Stars(G)
    m = G.m
    seen = set()
    for kind in (0, 1):
        for kk in range(k + 1):
            for T in itertools.combinations(range(m), kk):
                caught = 0
                for x in T:
                    caught |= St.NEstar[x] if kind == 0 else St.NFstar[x]
                for nfl in range(len(T) + 1):
                    for flags in itertools.combinations(T, nfl):
                        for na in range(a + 1):
                            for Y0 in itertools.combinations(range(m), na):
                                for ne in range(e + 1):
                                    for Phi in itertools.combinations(bits(caught), ne):
                                        ph = sum(1 << w for w in Phi)
                                        D = describe(G, St, kind, list(T), list(flags), list(Y0), ph)
                                        if D in seen:
                                            continue
                                        seen.add(D)
                                        if G.connects(D):
                                            if want:
                                                return True, (kind, T, flags, Y0, Phi, D)
                                            return True
    return (False, None) if want else False
