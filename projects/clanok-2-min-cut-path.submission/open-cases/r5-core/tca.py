"""Two cheap anchors (TCA), r5-core.md Section 5.

For a valid path P (list of side ids of a gcore.Gen):
  A = minimal E-members (no E-member strictly below), B = maximal F-members (no F-member strictly above);
  fA(b) = minimal E-members a with X_a meeting E_b (b in B);  fB(a) = maximal F-members b with X_b meeting F_a.
  costE(P) = 0 if |B| <= 3 (anchor all of B), else min over b1, b2 in B with |pos b1 - pos b2| >= 3 of
             |fA(b1) | fA(b2)|;  costF(P) dually.  tca(P) = min(costE, costF).
The *description check* evaluates the anchored description of the minimising pair exactly (adesc guided costs with
anchors {b1, b2} and centres E_b1, E_b2): with node witnesses only its cost equals the union bound (Proposition
5.2); middle witnesses can leave elements of L uncovered (out != 0).
"""
import itertools
from gcore import bits, popcount
import cdesc
import adesc


def skeleton(G, P):
    pos = {}
    for a, i in enumerate(P):
        pos[i >> 1] = a
    WE = [i >> 1 for i in P if not i & 1]
    WF = [i >> 1 for i in P if i & 1]
    A = [w for w in WE if not any(v != w and G.le[v][w] and not G.le[w][v] for v in WE)]
    B = [w for w in WF if not any(v != w and G.le[w][v] and not G.le[v][w] for v in WF)]
    return pos, A, B


def contacts(G, P):
    pos, A, B = skeleton(G, P)
    fA = {b: frozenset(a for a in A if G.E[a] & G.E[b]) for b in B}
    fB = {a: frozenset(b for b in B if G.F[b] & G.F[a]) for a in A}
    return pos, A, B, fA, fB


def side_cost(pos, X, fX, dist=3):
    """(cost, pair) for one side: X = skeleton members of the anchor type, fX their contact sets.  If the positions
    of X lie in an interval of length < dist, all of X are anchors (cost 0)."""
    if not X or max(pos[x] for x in X) - min(pos[x] for x in X) < dist:
        return 0, tuple(X)
    best = None
    for b1, b2 in itertools.combinations(X, 2):
        if abs(pos[b1] - pos[b2]) < dist:
            continue
        c = len(fX[b1] | fX[b2])
        if best is None or c < best[0]:
            best = (c, (b1, b2))
    return best


def tca_path(G, P, check=True, dist=3):
    pos, A, B, fA, fB = contacts(G, P)
    cE = side_cost(pos, B, fA, dist)
    cF = side_cost(pos, A, fB, dist)
    res = {"costE": cE, "costF": cF, "A": len(A), "B": len(B)}
    if check:
        pd = cdesc.path_data(G, P)
        En, Fn = cdesc.enon(G), cdesc.fnon(G)
        # E-side check
        b = cE[1]
        B0 = sum(1 << w for w in b)
        U = 0
        if len(b) == 2 and set(b) != set(B):
            for w in b:
                U |= cdesc_ne(G, G.E[w])
        c, out, inn = adesc.guided_cost_E(G, pd, B0, 0, U, En)
        res["checkE"] = (c, popcount(out), popcount(inn))
        a = cF[1]
        A0 = sum(1 << w for w in a)
        U = 0
        if len(a) == 2 and set(a) != set(A):
            for w in a:
                U |= cdesc_nf(G, G.F[w])
        c, out, inn = adesc.guided_cost_F(G, pd, 0, A0, U, Fn)
        res["checkF"] = (c, popcount(out), popcount(inn))
    res["tca"] = min(cE[0], cF[0])
    return res


def cdesc_ne(G, zm):
    S = 0
    for w in range(G.m):
        if G.E[w] and G.E[w] & zm:
            S |= 1 << w
    return S


def cdesc_nf(G, zm):
    S = 0
    for w in range(G.m):
        if G.F[w] and G.F[w] & zm:
            S |= 1 << w
    return S


def from_core(inst):
    """verify/r4-switch-review core.Inst (2CH) -> gcore.Gen with the trivial order."""
    from gcore import Gen
    m = inst.n
    E = [sum(1 << x for x in inst.sw[w][0]) for w in range(m)]
    F = [sum(1 << x for x in inst.sw[w][1]) for w in range(m)]
    le = [[a == b for b in range(m)] for a in range(m)]
    return Gen(inst.N, E, F, le, inst.s, inst.t)
