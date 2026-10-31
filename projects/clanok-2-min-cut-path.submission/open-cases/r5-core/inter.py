"""Intersections of GDESC terms (r5-core.md Section 8): the constructive proof of Lemma 8.1 / Theorem 8.2.

levels(G, P) runs the proof of Theorem 8.2 on a shortest valid path P of a gcore.Gen G:
  residue A' = A (minimal E-members); at every level
    rows R = up(A') & Fnon, columns C = NE (switch masks), k = floor(log2 m) + 1, N = ceil(2 k ln m),
    theta = |A'| / (2k); a row x is light iff |A' & strict_down(x)| <= theta;
    covE(x) = (NEstar[x] | strict_down(x) if light) & C,  covF(y) = (NFstar[y] | strict_up(y) if y in B) & R;
    the duality claim (light x: y in covE(x) or x in covF(y)) is checked for every pair;
    v = value of the game (rows R, columns C, payoff [y in covE(x)]) by LP;
    v >= 1/2: least cover of C by the covE (ILP), must be <= k; E-term with pivots on the light tools, flips A' & U;
              new residue A'' = A' & D(term) (subset of A' - G), must have |A' - G| <= |A'| / 2;
    v <  1/2: least cover of the light rows by the covF (ILP), must be <= k, least set of anchors in A' lying
              strictly below every heavy row (ILP), must be <= N; F-term with strict anchors on tools in B, flips B & U'.
  The intersection of the term down-sets must contain L, miss Up and connect s, t.
Every violated claim of the proof is appended to res['errors'] (must stay empty).

min_single(G, P): the least damage of a single E-term with at most k tools (any pivots) covering NE, by ILP, and
whether a single F-term (light rows by <= k F-tools, heavy rows by anchors) exists; used to see when intersections are
really needed.
"""
import math
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from gcore import bits, popcount
import gstar
from gstar import Stars, Skel, strict_down, strict_up
import gdesc


def up_closure(G, S):
    r = 0
    for w in bits(S):
        r |= G.up[w]
    return r


def game_value(rows, cols, cov):
    """Value of the zero-sum game: row player picks x in rows, column player y in cols, payoff 1 iff y in cov[x]
    (cov[x] a bit mask over switches).  Returns (v, p) with p the optimal row strategy (dict)."""
    nr, nc = len(rows), len(cols)
    M = np.zeros((nr, nc))
    for i, x in enumerate(rows):
        for j, y in enumerate(cols):
            if (cov[x] >> y) & 1:
                M[i, j] = 1.0
    # variables p_1..p_nr, v ; maximise v  <=>  minimise -v
    c = np.zeros(nr + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-M.T, np.ones((nc, 1))])      # v - sum_i p_i M[i,j] <= 0
    b_ub = np.zeros(nc)
    A_eq = np.zeros((1, nr + 1))
    A_eq[0, :nr] = 1.0
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * nr + [(None, None)],
                method="highs")
    assert r.success, r.message
    return -r.fun, {x: r.x[i] for i, x in enumerate(rows)}


def column_strategy(rows, cols, cov):
    """Optimal column strategy q of the game of game_value (column player minimises)."""
    nr, nc = len(rows), len(cols)
    M = np.zeros((nr, nc))
    for i, x in enumerate(rows):
        for j, y in enumerate(cols):
            if (cov[x] >> y) & 1:
                M[i, j] = 1.0
    c = np.zeros(nc + 1)
    c[-1] = 1.0
    A_ub = np.hstack([M, -np.ones((nr, 1))])        # sum_j q_j M[i,j] - w <= 0
    A_eq = np.zeros((1, nc + 1))
    A_eq[0, :nc] = 1.0
    r = linprog(c, A_ub=A_ub, b_ub=np.zeros(nr), A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * nc + [(None, None)],
                method="highs")
    assert r.success, r.message
    return r.fun, {y: max(0.0, r.x[j]) for j, y in enumerate(cols)}


def sample_cover(rng, items, sets, dist, k, tries=3000):
    """Draw k keys from dist (dict key -> prob) until the union of their sets covers items; None if no success."""
    keys = list(dist)
    w = [dist[x] for x in keys]
    if sum(w) <= 0:
        return None
    need = sum(1 << it for it in items)
    for _ in range(tries):
        ch = rng.choices(keys, weights=w, k=k)
        u = 0
        for x in ch:
            u |= sets[x]
        if u & need == need:
            return sorted(set(ch))
    return None


def min_cover(items, sets, timeout=30):
    """Least number of sets (dict key -> bit mask) covering all items (list of ints).  Returns (size, keys) or
    (None, None) if impossible."""
    if not items:
        return 0, []
    keys = [kk for kk in sets if sets[kk]]
    for it in items:
        if not any((sets[kk] >> it) & 1 for kk in keys):
            return None, None
    A_ = np.zeros((len(items), len(keys)))
    for j, kk in enumerate(keys):
        for i, it in enumerate(items):
            if (sets[kk] >> it) & 1:
                A_[i, j] = 1.0
    r = milp(np.ones(len(keys)), constraints=LinearConstraint(A_, lb=np.ones(len(items)), ub=np.inf),
             integrality=np.ones(len(keys)), bounds=Bounds(0, 1), options={"time_limit": timeout})
    if not r.success:
        return None, None
    xs = np.round(r.x).astype(int)
    chosen = [keys[j] for j in range(len(keys)) if xs[j]]
    return len(chosen), chosen


def params(m):
    k = int(math.floor(math.log2(m))) + 1 if m >= 1 else 1
    N = int(math.ceil(2 * k * math.log(m))) if m > 1 else 0
    return k, N


def level_data(G, St, K, Ares, kth=None):
    """Rows, columns, light/heavy split and coverage masks of one level with residue Ares (mask)."""
    m = G.m
    k, N = params(m)
    fnon = gdesc.fnon(G)
    R = up_closure(G, Ares) & fnon
    C = K.NE
    nA = popcount(Ares)
    theta = nA / (2.0 * (kth or k))
    sdown = {x: strict_down(G, x) for x in range(m)}
    sup = {y: strict_up(G, y) for y in range(m)}
    dam = {x: Ares & sdown[x] for x in bits(R)}
    light = {x: popcount(dam[x]) <= theta for x in bits(R)}
    covE = {x: (St.NEstar[x] | (sdown[x] if light[x] else 0)) & C for x in bits(R)}
    covF = {y: (St.NFstar[y] | (sup[y] if (K.B >> y) & 1 else 0)) & R for y in bits(C)}
    return dict(R=R, C=C, nA=nA, theta=theta, dam=dam, light=light, covE=covE, covF=covF, k=k, N=N)


def levels(G, P, St=None, K=None, maxlev=64, rng=None, kth=None):
    """rng given: the covers are drawn as in the proof (k independent draws from the optimal strategies, anchors
    uniformly from A'), with all light tools pivoted; otherwise least covers by ILP."""
    if St is None:
        St = Stars(G)
    if K is None:
        K = Skel(G, P)
    m = G.m
    k, N = params(m)
    res = dict(errors=[], levels=[], k=k, N=N)
    Ares = K.A
    terms = []
    D = (1 << m) - 1
    lev = 0
    while True:
        lev += 1
        if lev > maxlev:
            res["errors"].append("too many levels")
            break
        if not Ares:
            # only possible at level 1 with A empty: trivial F-term
            T = dict(kind=1, tools=[], flags=[], anchors=[], flips=0)
            Dt = gdesc.describe(G, St, 1, [], [], [], 0)
            terms.append(T)
            D &= Dt
            res["levels"].append(dict(case="noA"))
            break
        ld = level_data(G, St, K, Ares, kth)
        R, C = ld["R"], ld["C"]
        info = dict(nA=ld["nA"], R=popcount(R), C=popcount(C),
                    heavy=sum(1 for x in bits(R) if not ld["light"][x]))
        # duality claim for light rows
        for x in bits(R):
            if not ld["light"][x]:
                continue
            for y in bits(C):
                if not ((ld["covE"][x] >> y) & 1) and not ((ld["covF"][y] >> x) & 1):
                    res["errors"].append("duality fails lev %d x %d y %d" % (lev, x, y))
        if not C:
            Dt = gdesc.describe(G, St, 0, [], [], [], 0)
            info["case"] = "C0"
            final = True
            newA = 0
        elif not R:
            Dt = gdesc.describe(G, St, 1, [], [], [], 0)
            info["case"] = "R0"
            final = True
            newA = 0
        else:
            v, p = game_value(bits(R), bits(C), ld["covE"])
            info["v"] = round(v, 4)
            if v >= 0.5 - 1e-9:
                chosen = sample_cover(rng, bits(C), ld["covE"], p, k) if rng is not None else None
                if chosen is not None:
                    size = len(chosen)
                    info["sampled"] = True
                else:
                    if rng is not None:
                        res["sample failures"] = res.get("sample failures", 0) + 1
                    size, chosen = min_cover(bits(C), ld["covE"])
                if size is None or size > k:
                    res["errors"].append("E-cover %s > k=%d at lev %d (v=%.3f)" % (size, k, lev, v))
                    if size is None:
                        break
                T = list(chosen)
                flags = [x for x in T if ld["light"][x]]
                U = 0
                for x in T:
                    U |= St.NEstar[x]
                Phi = Ares & U
                if popcount(Phi) > 9 * len(T):
                    res["errors"].append("flips %d > 9 * tools at lev %d" % (popcount(Phi), lev))
                Dt = gdesc.describe(G, St, 0, T, flags, [], Phi)
                # generators, for the damage bound of the proof
                Sx = 0
                for x in flags:
                    Sx |= strict_down(G, x)
                Gen_ = (gdesc.enon(G) & ~U & ~Sx) | Phi
                dmg = Ares & ~Gen_
                if 2 * popcount(dmg) > ld["nA"]:
                    res["errors"].append("damage %d > |A'|/2 = %.1f at lev %d" % (popcount(dmg), ld["nA"] / 2, lev))
                newA = Ares & Dt
                if newA & ~dmg:
                    res["errors"].append("A' & D not inside A' - G at lev %d" % lev)
                info.update(case="E", tools=len(T), pivots=len(flags), flips=popcount(Phi), damage=popcount(dmg),
                            newA=popcount(newA))
                final = newA == 0
            else:
                lightrows = [x for x in bits(R) if ld["light"][x]]
                heavyrows = [x for x in bits(R) if not ld["light"][x]]
                lr = sum(1 << x for x in lightrows)
                sets = {y: ld["covF"][y] & lr for y in bits(C)}
                chosen = None
                if rng is not None and lightrows:
                    w_, q = column_strategy(bits(R), bits(C), ld["covE"])
                    chosen = sample_cover(rng, lightrows, sets, q, k)
                    if chosen is None:
                        res["sample failures"] = res.get("sample failures", 0) + 1
                if chosen is not None:
                    size = len(chosen)
                else:
                    size, chosen = min_cover(lightrows, sets)
                if size is None or size > k:
                    res["errors"].append("F-cover %s > k=%d at lev %d (v=%.3f)" % (size, k, lev, v))
                    if size is None:
                        break
                hsets = {a: sum(1 << x for x in heavyrows if (ld["dam"][x] >> a) & 1) for a in bits(Ares)}
                hchosen = None
                if rng is not None and heavyrows:
                    hchosen = sample_cover(rng, heavyrows, hsets, {a: 1.0 for a in bits(Ares)}, N)
                    if hchosen is None:
                        res["sample failures"] = res.get("sample failures", 0) + 1
                if hchosen is not None:
                    hsize = len(hchosen)
                else:
                    hsize, hchosen = min_cover(heavyrows, hsets)
                if hsize is None or hsize > N:
                    res["errors"].append("anchors %s > N=%d at lev %d" % (hsize, N, lev))
                    if hsize is None:
                        break
                T = list(chosen)
                flags = [y for y in T if (K.B >> y) & 1]
                U2 = 0
                for y in T:
                    U2 |= St.NFstar[y]
                Phi = K.B & U2
                if popcount(Phi) > 9 * len(T):
                    res["errors"].append("F flips %d > 9 * tools at lev %d" % (popcount(Phi), lev))
                Dt = gdesc.describe(G, St, 1, T, flags, list(hchosen), Phi)
                info.update(case="F", tools=len(T), anchors=hsize, flips=popcount(Phi))
                final = True
                newA = 0
                if Dt & up_closure(G, Ares):
                    res["errors"].append("F-term meets up(A') at lev %d" % lev)
        if K.L & ~Dt:
            res["errors"].append("term misses part of L at lev %d" % lev)
        if not final and (Dt & up_closure(G, Ares) & ~up_closure(G, newA)):
            res["errors"].append("D & up(A') not inside up(A'') at lev %d" % lev)
        D &= Dt
        res["levels"].append(info)
        if final:
            break
        if newA == Ares:
            res["errors"].append("no progress at lev %d" % lev)
            break
        Ares = newA
    res["nlev"] = len(res["levels"])
    res["picks"] = (K.L & ~D) == 0 and (K.Up & D) == 0
    res["connects"] = G.connects(D)
    if not res["picks"]:
        res["errors"].append("final D does not pick P")
    if not res["connects"]:
        res["errors"].append("final D does not connect")
    if res["nlev"] > k:
        res["errors"].append("levels %d > k = %d" % (res["nlev"], k))
    res["D"] = D
    return res


def min_single(G, P, St=None, K=None, timeout=30):
    """Least damage of one E-term with <= k tools (pivots on any tool, flips A & U free) covering NE, and whether
    one F-term in the sense of Lemma 8.1 (light rows by <= k F-tools, heavy rows by <= N anchors) exists, with
    residue A.  Returns dict(edmg=least damage or None, fone=bool)."""
    if St is None:
        St = Stars(G)
    if K is None:
        K = Skel(G, P)
    k, N = params(G.m)
    out = dict(edmg=None, fone=False)
    if not K.A:
        out.update(edmg=0, fone=True)
        return out
    ld = level_data(G, St, K, K.A)
    C, R = bits(ld["C"]), bits(ld["R"])
    if not C:
        out["edmg"] = 0
    else:
        # E-term: tools x in R with or without pivot (two options per row; pivot option allowed for every row)
        opts = []
        for x in R:
            opts.append((x, 0, St.NEstar[x] & ld["C"], 0))
            sd = strict_down(G, x)
            opts.append((x, 1, (St.NEstar[x] | sd) & ld["C"], K.A & sd))
        As = bits(K.A)
        nv = len(opts) + len(As)
        c = np.zeros(nv)
        c[len(opts):] = 1.0
        rows, lb, ub = [], [], []
        for y in C:
            row = np.zeros(nv)
            for j, o in enumerate(opts):
                if (o[2] >> y) & 1:
                    row[j] = 1
            rows.append(row)
            lb.append(1)
            ub.append(np.inf)
        row = np.zeros(nv)
        row[:len(opts)] = 1
        rows.append(row)
        lb.append(0)
        ub.append(k)
        for j, o in enumerate(opts):
            for i, a in enumerate(As):
                if (o[3] >> a) & 1:
                    row = np.zeros(nv)
                    row[len(opts) + i] = 1
                    row[j] = -1
                    rows.append(row)
                    lb.append(0)
                    ub.append(np.inf)
        if all(any((o[2] >> y) & 1 for o in opts) for y in C):
            r = milp(c, constraints=LinearConstraint(np.array(rows), lb=np.array(lb), ub=np.array(ub)),
                     integrality=np.ones(nv), bounds=Bounds(0, 1), options={"time_limit": timeout})
            if r.success:
                out["edmg"] = int(round(r.fun))
    if not R:
        out["fone"] = True
    else:
        lightrows = [x for x in R if ld["light"][x]]
        heavyrows = [x for x in R if not ld["light"][x]]
        lr = sum(1 << x for x in lightrows)
        size, _ = min_cover(lightrows, {y: ld["covF"][y] & lr for y in C})
        hsize, _ = min_cover(heavyrows, {a: sum(1 << x for x in heavyrows if (ld["dam"][x] >> a) & 1)
                                         for a in bits(K.A)})
        out["fone"] = size is not None and size <= k and hsize is not None and hsize <= N
        out["fsize"], out["hsize"] = size, hsize
    return out
