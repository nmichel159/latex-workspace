"""Agent r7-lb (round 7): exact minimum cost of a single connecting GDESC term.

Instances: general switch form as verify/rv-r6-core/zzl.SW (imported read-only; reviewed library).
A term (qp-proof.md Definition 5.1, with anchors in both kinds as in r5-core.md Section 8.2):
  E-term (T, T', Y, Phi): U = union NE(E#_x) (x in T), Pi = down(Y) + union over T' of (down(x) - [x]),
          Gamma = (Enon - U - Pi) | Phi, D = M - up(Gamma).
  F-term dually (zzl.term_D, kind 'F').
Cost of a term = |T| + |Y| + |Phi|  (tools + anchors + flips).  Flips are ARBITRARY switches here (the restricted
variant Phi inside U of qp-proof.md Definition 6.1 is handled by brute force only, see brute_mincost).

Exact method (mincost):
 (1) D connects s and t iff L_P <= D <= M - Up_P for some valid path P (qp-proof Lemma 3.4); only the pair
     (L_P, Up_P) matters, and only the inclusion-minimal pairs.  valid_pairs() enumerates them by a search over
     states (side, Up, Dn) of valid walks with dominance pruning (a walk with repeated sides contains a valid path
     with smaller closures, so walks give the same minimal pairs).
 (2) For an E-term and a pair (L, Up): L <= D iff Gamma misses L; D misses Up iff every minimal element of Up lies
     above an element of Gamma.  Columns C = L & Enon must lie in U | Pi (each column needs an object: an
     unflagged tool whose star catches it, a flagged tool whose star or pivot contains it, or an anchor above it).
     WLOG every object covers a column (dropping an object that covers no needed column only adds generators
     outside L).  Then the flips are a minimum hitting set: each minimal element a of Up not above a generator of
     Enon - (U | Pi) needs a flip phi <= a with phi outside L.
 (3) F-terms = E-terms of the reversed instance (qp-proof Lemma 4.4, dual part): same nodes, order reversed,
     E and F exchanged, middle edges reversed; its mode vectors are complements and its pairs are (Up, L).
Every term found is rebuilt with zzl.term_D on the ORIGINAL instance and tested with I.connects (verified=True).
"""
import os
import sys
import json
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in (os.path.join(OC, "verify", "rv-r6-core"), os.path.join(OC, "r5-core")):
    if _d not in sys.path:
        sys.path.append(_d)

from zzl import SW, bits, popcount, term_D  # noqa: E402

WORK_CAP = None      # optional bound on DFS nodes per e_term call (searches set it; RuntimeError when exceeded)


# ------------------------------------------------------------------------------------------------ conversion, io

def from_gen(G):
    """r5-core gcore.Gen -> zzl.SW (G.medge: private node -> (y, x) with y < x)."""
    me = [(int(y), int(x), int(p)) for p, (y, x) in G.medge.items()]
    return SW(G.m, [list(map(bool, r)) for r in G.le], G.E, G.F, G.s, G.t, G.N, me)


def reverse(I):
    m = I.m
    le = [[I.le[j][i] for j in range(m)] for i in range(m)]
    me = [(v, z, p) for (z, v, p) in I.me]
    return SW(m, le, I.F, I.E, I.s, I.t, I.nn, me)


def dump(I, path, extra=None):
    d = {"m": I.m, "le": [[int(b) for b in row] for row in I.le], "E": [hex(x) for x in I.E],
         "F": [hex(x) for x in I.F], "s": I.s, "t": I.t, "nn": I.nn, "me": [list(e) for e in I.me],
         "extra": extra or {}}
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    conv = lambda x: int(x, 16) if isinstance(x, str) else int(x)
    if "medge" in d:                      # r5-core format (hunt_single.save)
        E = [int(x) for x in d["E"]]
        F = [int(x) for x in d["F"]]
        me = [(int(v[0]), int(v[1]), int(p)) for p, v in d["medge"].items()]
        I = SW(len(E), [[bool(b) for b in row] for row in d["le"]], E, F, d["s"], d["t"], d["N"], me)
        return I, d.get("extra", {})
    I = SW(d["m"], [[bool(b) for b in row] for row in d["le"]], [conv(x) for x in d["E"]],
           [conv(x) for x in d["F"]], d["s"], d["t"], d["nn"], [tuple(e) for e in d["me"]])
    return I, d.get("extra", {})


# ------------------------------------------------------------------------------------------------ valid pairs

def valid_pairs(I, state_cap=2_000_000):
    """Inclusion-minimal pairs (L, Up) = (down(W_F), up(W_E)) over all valid walks from s to t.
    Returns a list of (L, Up) masks; [] if no valid walk; None if s == t (every D connects).
    Raises RuntimeError when more than state_cap states are generated."""
    if I.s == I.t:
        return None
    m = I.m
    sides = [(w, ty) for w in range(m) for ty in (0, 1) if (I.F[w] if ty else I.E[w])]
    sn = {sd: (I.F[sd[0]] if sd[1] else I.E[sd[0]]) for sd in sides}
    nbr = {sd: [o for o in sides if o != sd and sn[sd] & sn[o]] for sd in sides}
    front = {sd: [] for sd in sides}       # non-dominated (Up, Dn) per side

    def add(sd, Up, Dn):
        lst = front[sd]
        for (u, d) in lst:
            if (u & ~Up) == 0 and (d & ~Dn) == 0:
                return False
        lst[:] = [(u, d) for (u, d) in lst if not ((Up & ~u) == 0 and (Dn & ~d) == 0)]
        lst.append((Up, Dn))
        return True

    stack = []
    for sd in sides:
        if (sn[sd] >> I.s) & 1:
            w, ty = sd
            if ty == 0:
                st = (I.up[w], 0)
            else:
                st = (0, I.dn[w])
            if add(sd, *st):
                stack.append((sd,) + st)
    count = 0
    while stack:
        sd, Up, Dn = stack.pop()
        if (Up, Dn) not in front[sd]:
            continue                       # dominated meanwhile
        count += 1
        if count > state_cap:
            raise RuntimeError("valid_pairs: state cap exceeded")
        for o in nbr[sd]:
            w, ty = o
            if ty == 0:
                if (Dn >> w) & 1:
                    continue
                nU, nD = Up | I.up[w], Dn
            else:
                if (Up >> w) & 1:
                    continue
                nU, nD = Up, Dn | I.dn[w]
            if add(o, nU, nD):
                stack.append((o, nU, nD))
    goal = []
    for sd in sides:
        if (sn[sd] >> I.t) & 1:
            for (u, d) in front[sd]:
                goal.append((d, u))        # (L, Up)
    out = []
    for (L, Up) in sorted(set(goal), key=lambda p: (popcount(p[0]) + popcount(p[1]))):
        if any((l2 & ~L) == 0 and (u2 & ~Up) == 0 for (l2, u2) in out):
            continue
        out.append((L, Up))
    return out


# ------------------------------------------------------------------------------------------------ E-term cost

def _hitting(I, Z, budget, Lm):
    """Minimum flips: a list of switches phi (outside Lm), each z in Z above some phi; len <= budget or None."""
    if not Z:
        return []
    if budget <= 0:
        return None
    Zm = 0
    for z in Z:
        Zm |= 1 << z
    best_a, best_c = None, None
    for a in Z:
        c = I.dn[a] & ~Lm
        if best_c is None or popcount(c) < popcount(best_c):
            best_a, best_c = a, c
    cands = []
    for phi in bits(best_c):
        cov = I.up[phi] & Zm
        cands.append((cov, phi))
    # dominance: keep candidates with inclusion-maximal cover
    cands.sort(key=lambda c: -popcount(c[0]))
    keep = []
    for cov, phi in cands:
        if any((cov & ~k) == 0 for k, _ in keep):
            continue
        keep.append((cov, phi))
    for cov, phi in keep:
        rest = [z for z in Z if not (cov >> z) & 1]
        r = _hitting(I, rest, budget - 1, Lm)
        if r is not None:
            return [phi] + r
    return None


def e_term(I, Lm, Upm, budget, tmax=None):
    """An E-term of cost <= budget with L <= D, D & Up = 0, at most tmax tools; returns
    (T, Tp, anchors_list, flips_list) or None.  Exact (complete) by the WLOG argument of the module doc."""
    m = I.m
    C = Lm & I.enon
    minUp = [a for a in bits(Upm) if not (I.sdn[a] & Upm)]
    minUpm = sum(1 << a for a in minUp)
    Rel = I.enon & ~Lm & I.dnc(minUpm)
    objs = []                              # (cov, rem, kind, x); kind 0 tool, 1 flagged tool, 2 anchor
    for x in range(m):
        for kind, rem in ((0, I.NEs[x]), (1, I.NEs[x] | I.sdn[x]), (2, I.dn[x])):
            cov = rem & C
            if cov:
                objs.append((cov, rem, kind, x))
    # dominance: o2 removed if some o1 covers at least as much and removes no more relevant generators,
    # and (o1 is an anchor or o2 is a tool) so that the tool budget is respected
    objs.sort(key=lambda o: (-popcount(o[0]), popcount(o[1] & Rel), o[2] == 2 and 0 or 1))
    keep = []
    for o in objs:
        dom = False
        for k in keep:
            if (o[0] & ~k[0]) == 0 and (k[1] & Rel & ~o[1]) == 0 and (k[2] == 2 or o[2] != 2):
                dom = True
                break
        if not dom:
            keep.append(o)
    opts = {}
    for c in bits(C):
        opts[c] = [o for o in keep if (o[0] >> c) & 1]
        if not opts[c]:
            return None                    # cannot happen: the anchor at c covers c
    failed = set()

    work = [0]

    def dfs(covered, R, bud, ntools, chosen):
        key = (covered, R & Rel, bud, ntools)
        if key in failed:
            return None
        work[0] += 1
        if WORK_CAP is not None and work[0] > WORK_CAP:
            raise RuntimeError("e_term: work cap exceeded")
        if covered == C:
            Gam = I.enon & ~R
            Z = [a for a in minUp if not (I.dn[a] & Gam)]
            fl = _hitting(I, Z, bud, Lm)
            if fl is not None:
                return list(chosen), fl
            failed.add(key)
            return None
        if bud <= 0:
            failed.add(key)
            return None
        unc = C & ~covered
        best = None
        for c in bits(unc):
            oc = opts[c]
            if best is None or len(oc) < len(best):
                best = oc
        for o in best:
            if o[2] != 2 and tmax is not None and ntools >= tmax:
                continue
            chosen.append(o)
            r = dfs(covered | o[0], R | o[1], bud - 1, ntools + (o[2] != 2), chosen)
            chosen.pop()
            if r is not None:
                return r
        failed.add(key)
        return None

    r = dfs(0, 0, budget, 0, [])
    if r is None:
        return None
    chosen, fl = r
    T, Tp, anc = [], [], []
    for (cov, rem, kind, x) in chosen:
        if kind == 2:
            anc.append(x)
        else:
            if x in T:                     # the same switch twice as a tool: merge (flag if either flagged)
                if kind == 1 and x not in Tp:
                    Tp.append(x)
                continue
            T.append(x)
            if kind == 1:
                Tp.append(x)
    return T, Tp, anc, fl


# ------------------------------------------------------------------------------------------------ main routine

def verify_term(I, kind, T, Tp, anc, fl):
    am = sum(1 << a for a in anc)
    ph = sum(1 << f for f in fl)
    D, U, S, Gm = term_D(I, kind, list(T), list(Tp), am, ph)
    return I.connects(D)


def mincost(I, cap=12, tmax=None, pairs=None, Irev=None):
    """Exact minimum total cost (tools + anchors + flips, arbitrary flips) of a single connecting term.
    Returns dict(total, kind, T, Tp, anchors, flips, verified, npairs) or dict(total=None) if no-instance,
    total = '>cap' if none of cost <= cap exists."""
    if I.s == I.t:
        return dict(total=0, kind=None, T=[], Tp=[], anchors=[], flips=[], verified=True, npairs=0)
    if pairs is None:
        pairs = valid_pairs(I)
    if not pairs:
        return dict(total=None)
    if Irev is None:
        Irev = reverse(I)
    for c in range(0, cap + 1):
        for (L, Up) in pairs:
            for kind, J, Lm, Um in (("E", I, L, Up), ("F", Irev, Up, L)):
                r = e_term(J, Lm, Um, c, tmax)
                if r is not None:
                    T, Tp, anc, fl = r
                    cost = len(T) + len(anc) + len(fl)
                    ok = verify_term(I, kind, T, Tp, anc, fl)
                    return dict(total=cost, kind=kind, T=T, Tp=Tp, anchors=anc, flips=fl, verified=ok,
                                npairs=len(pairs), pair=(L, Up))
    return dict(total=">%d" % cap, npairs=len(pairs))


def profile(I, tmaxs=(0, 1, 2, 3), cap=12, pairs=None):
    """For each tool bound t: the least anchors + flips of a connecting term with at most t tools."""
    if pairs is None:
        pairs = valid_pairs(I)
    Irev = reverse(I)
    out = {}
    for t in tmaxs:
        r = mincost(I, cap=cap, tmax=t, pairs=pairs, Irev=Irev)
        tot = r["total"]
        out[t] = (None if not isinstance(tot, int) else tot - len(r["T"]), r.get("T"))
    return out


# ------------------------------------------------------------------------------------------------ brute force

def brute_mincost(I, cap=3, restricted=False):
    """Independent check: enumerate every term (both kinds, tools, flag patterns, anchors, flips) with
    tools + anchors + flips <= cap (flips arbitrary, or inside U if restricted) and test I.connects(D) directly.
    Returns the least total cost or None (no term of cost <= cap)."""
    if I.s == I.t:
        return 0
    m = I.m
    sw = list(range(m))
    for c in range(0, cap + 1):
        for t in range(0, c + 1):
            for T in itertools.combinations(sw, t):
                for kind in ("E", "F"):
                    U = 0
                    for x in T:
                        U |= I.NEs[x] if kind == "E" else I.NFs[x]
                    fsrc = list(bits(U)) if restricted else sw
                    for fl in range(1 << t):
                        Tp = [T[i] for i in range(t) if (fl >> i) & 1]
                        for a in range(0, c - t + 1):
                            f = c - t - a
                            for anc in itertools.combinations(sw, a):
                                am = sum(1 << x for x in anc)
                                for ph in itertools.combinations(fsrc, f):
                                    D = term_D(I, kind, list(T), Tp, am, sum(1 << x for x in ph))[0]
                                    if I.connects(D):
                                        return c
    return None


def is_yes(I):
    if I.s == I.t:
        return True
    return bool(valid_pairs(I))


# ------------------------------------------------------------------------------------------------ counting

def count_terms(I, c, limit=None):
    """Number of connecting terms of total cost exactly c (both kinds; objects: tool, flagged tool, anchor, flip;
    a switch is not both a plain and a flagged tool).  Brute force; for c <= 3 and small m."""
    m = I.m
    objs = [(k, x) for x in range(m) for k in ("T", "P", "A", "X")]
    cnt = 0
    for kind in ("E", "F"):
        for combo in itertools.combinations(objs, c):
            T, Tp, anc, ph = [], [], 0, 0
            seen = set()
            bad = False
            for (k, x) in combo:
                if k in ("T", "P"):
                    if x in seen:
                        bad = True
                        break
                    seen.add(x)
                    T.append(x)
                    if k == "P":
                        Tp.append(x)
                elif k == "A":
                    anc |= 1 << x
                else:
                    ph |= 1 << x
            if bad:
                continue
            D = term_D(I, kind, T, Tp, anc, ph)[0]
            if I.connects(D):
                cnt += 1
                if limit is not None and cnt >= limit:
                    return cnt
    return cnt
