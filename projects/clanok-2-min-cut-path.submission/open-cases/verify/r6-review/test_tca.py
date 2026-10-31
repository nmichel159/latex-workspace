"""Checks of r5-core.md: CDESC soundness (§3.1), Lemma G (§3.2), ADESC soundness (§5.1), Theorem 5.2 (E1), (E2),
(F1), (F2) step by step, Proposition 5.2'.

usage: python test_tca.py MODE SEED COUNT [rmin rmax]
  MODE rand  : rand_general (m 3..8)
  MODE plant : planted_general (r in rmin..rmax)
Failures are stored with the instance and the path in runs/tca-MODE-SEED.json.
"""
import itertools
import json
import random
import sys

from glib import (bits, popcount, brute, is_downset, connects, all_shortest, shortest_len, e_desc, f_desc, NE, NF,
                  anchored_e, anchored_f, contract_map, cmask, cdesc, p2_violations)
from gen_g import rand_general, planted_general

STATS = {}
FAIL = []


def bump(k, v=1):
    STATS[k] = STATS.get(k, 0) + v


def fail(name, G, extra=None):
    bump("FAIL " + name)
    if sum(1 for f in FAIL if f["check"] == name) < 5:
        FAIL.append({"check": name, "inst": G.to_json(), "extra": extra})


def members(G, P):
    WE = WF = 0
    pos = {}
    for a, i in enumerate(P):
        w = i >> 1
        pos[w] = a
        if i & 1:
            WF |= 1 << w
        else:
            WE |= 1 << w
    return WE, WF, pos


def minimal_E(G, WE):
    A = 0
    for a in bits(WE):
        if all(G.le[a][x] for x in bits(G.dn[a] & WE)):
            A |= 1 << a
    return A


def maximal_F(G, WF):
    B = 0
    for b in bits(WF):
        if all(G.le[x][b] for x in bits(G.up[b] & WF)):
            B |= 1 << b
    return B


def picks(G, D, P):
    """D picks every member of P"""
    for i in P:
        w = i >> 1
        if bool((D >> w) & 1) != bool(i & 1):
            return False
    return True


def fstar_A(G, P, A, b):
    """f*_A(b) as defined in r5-core §5.2: a in A with X_a meeting E_b, or meeting F_v for a switch v < b with
    F_v & E_b != 0"""
    out = 0
    vs = [v for v in range(G.m) if G.lt(v, b) and (G.F[v] & G.E[b])]
    for a in bits(A):
        Xa = G.E[a]
        if Xa & G.E[b] or any(Xa & G.F[v] for v in vs):
            out |= 1 << a
    return out


def fstar_B(G, P, B, a):
    out = 0
    vs = [v for v in range(G.m) if G.lt(a, v) and (G.E[v] & G.F[a])]
    for b in bits(B):
        Xb = G.F[b]
        if Xb & G.F[a] or any(Xb & G.E[v] for v in vs):
            out |= 1 << b
    return out


def check_E2(G, P, WE, WF, pos, A, B, b1, b2, dual=False):
    """(E2) for the anchors b1, b2 (in the dual reading: F-description with E-anchors b1, b2 = a1, a2)."""
    L = G.dnc(WF)
    Up = G.upc(WE)
    tag = "F2" if dual else "E2"
    B0 = (1 << b1) | (1 << b2)
    if not dual:
        dB = G.dnc(B0)
        root = contract_map(G, [G.F[v] for v in bits(dB) if G.F[v]])
        c1, c2 = cmask(G, root, G.E[b1]), cmask(G, root, G.E[b2])
        U = sum(1 << y for y in range(G.m) if G.E[y] and (cmask(G, root, G.E[y]) & (c1 | c2)))
        Phi = fstar_A(G, P, A, b1) | fstar_A(G, P, A, b2)
        # the core claim: out = 0
        out = (L & ~dB) & G.Enon & ~U
        if out:
            fail(tag + "-out", G, [P, b1, b2, sorted(bits(out))])
        D = anchored_e(G, B0, 0, U, Phi)
        ok = D is not None and picks(G, D, P)
        bump(tag + " tested")
        if not ok:
            fail(tag + "-desc", G, [P, b1, b2, None if D is None else sorted(bits(D)), sorted(bits(Phi)),
                                     sorted(bits(U))])
            if D is not None and not connects(G, D):
                fail(tag + "-desc-noconnect", G, [P, b1, b2])
        if A & U & ~Phi:
            bump(tag + " A&U not in Phi")
        # repair (a): Phi = A & U
        Da = anchored_e(G, B0, 0, U, A & U)
        if Da is None or not picks(G, Da, P):
            fail(tag + "-repair-a", G, [P, b1, b2])
        # repair (b): uncontracted two-step centre, Phi = f*
        Ub = NE(G, G.E[b1]) | NE(G, G.E[b2])
        for bb in (b1, b2):
            for v in range(G.m):
                if G.lt(v, bb) and (G.F[v] & G.E[bb]):
                    Ub |= NE(G, G.F[v])
        if (A & Ub) != Phi:
            fail(tag + "-repair-b-phi", G, [P, b1, b2])
        Db = anchored_e(G, B0, 0, Ub, Phi)
        if Db is None or not picks(G, Db, P):
            fail(tag + "-repair-b", G, [P, b1, b2])
        bump(tag + " |Phi|", popcount(Phi))
        bump(tag + " |A&U|", popcount(A & U))
    else:
        a1, a2 = b1, b2
        A0 = B0
        uA = G.upc(A0)
        root = contract_map(G, [G.E[v] for v in bits(uA) if G.E[v]])
        c1, c2 = cmask(G, root, G.F[a1]), cmask(G, root, G.F[a2])
        U = sum(1 << y for y in range(G.m) if G.F[y] and (cmask(G, root, G.F[y]) & (c1 | c2)))
        Phi = fstar_B(G, P, B, a1) | fstar_B(G, P, B, a2)
        out = (Up & ~uA) & G.Fnon & ~U
        if out:
            fail(tag + "-out", G, [P, a1, a2, sorted(bits(out))])
        D = anchored_f(G, A0, 0, U, Phi)
        ok = D is not None and picks(G, D, P)
        bump(tag + " tested")
        if not ok:
            fail(tag + "-desc", G, [P, a1, a2, None if D is None else sorted(bits(D)), sorted(bits(Phi)),
                                     sorted(bits(U))])
            if D is not None and not connects(G, D):
                fail(tag + "-desc-noconnect", G, [P, a1, a2])
        if B & U & ~Phi:
            bump(tag + " B&U not in Phi")
        Da = anchored_f(G, A0, 0, U, B & U)
        if Da is None or not picks(G, Da, P):
            fail(tag + "-repair-a", G, [P, a1, a2])
        Ub = NF(G, G.F[a1]) | NF(G, G.F[a2])
        for aa in (a1, a2):
            for v in range(G.m):
                if G.lt(aa, v) and (G.E[v] & G.F[aa]):
                    Ub |= NF(G, G.E[v])
        if (B & Ub) != Phi:
            fail(tag + "-repair-b-phi", G, [P, a1, a2])
        Db = anchored_f(G, A0, 0, Ub, Phi)
        if Db is None or not picks(G, Db, P):
            fail(tag + "-repair-b", G, [P, a1, a2])


def check_path(G, P):
    WE, WF, pos = members(G, P)
    L = G.dnc(WF)
    Up = G.upc(WE)
    if L & Up:
        fail("valid path with Up & L", G, [P])
        return
    A = minimal_E(G, WE)
    B = maximal_F(G, WF)
    nomed = not G.medges
    # Lemma G with random U (and its dual)
    for _ in range(3):
        U = sum(1 << w for w in range(G.m) if random.random() < 0.5)
        out = L & G.Enon & ~U
        G1 = (G.Enon & ~U) & ~L
        inn = sum(1 << a for a in bits(A) if not any(G.le[g][a] for g in bits(G1)))
        D = e_desc(G, U, out | inn)
        if not is_downset(G, D) or not picks(G, D, P):
            fail("LemmaG", G, [P, U])
        outF = Up & G.Fnon & ~U
        G1F = (G.Fnon & ~U) & ~Up
        innF = sum(1 << b for b in bits(B) if not any(G.le[b][g] for g in bits(G1F)))
        DF = f_desc(G, U, outF | innF)
        if not is_downset(G, DF) or not picks(G, DF, P):
            fail("LemmaG-dual", G, [P, U])
        bump("LemmaG tested")
    # (E1), (F1)
    pB = [pos[b] for b in bits(B)]
    if pB and max(pB) - min(pB) <= 4:
        D = anchored_e(G, B, 0, 0, 0)
        bump("E1 tested")
        if D is None or not picks(G, D, P):
            fail("E1", G, [P])
    pA = [pos[a] for a in bits(A)]
    if pA and max(pA) - min(pA) <= 4:
        D = anchored_f(G, A, 0, 0, 0)
        bump("F1 tested")
        if D is None or not picks(G, D, P):
            fail("F1", G, [P])
    # (E2), (F2)
    thr = 3 if nomed else 5
    for b1, b2 in itertools.combinations(list(bits(B)), 2):
        if abs(pos[b1] - pos[b2]) >= thr:
            check_E2(G, P, WE, WF, pos, A, B, b1, b2)
    for a1, a2 in itertools.combinations(list(bits(A)), 2):
        if abs(pos[a1] - pos[a2]) >= thr:
            check_E2(G, P, WE, WF, pos, A, B, a1, a2, dual=True)
    # Proposition 5.2'
    for _ in range(2):
        A1 = sum(1 << a for a in bits(A) if random.random() < 0.5)
        strict = 0
        for a in bits(A1):
            strict |= G.dn[a] & ~(G.dn[a] & G.up[a])     # down(a) - [a]
        B0 = B & ~strict
        D = G.dnc(B0) | strict
        bump("5.2' tested")
        if not is_downset(G, D) or not picks(G, D, P):
            fail("5.2'", G, [P, A1])


def check_inst(G, max_paths=60, do_cdesc=False):
    if p2_violations(G):
        bump("skip noP2")
        return
    bump("instances")
    sols = brute(G) if G.m <= 14 else None
    L = shortest_len(G)
    yes = L is not None
    if sols is not None and bool(sols) != yes:
        fail("brute vs shortest", G, None)
    bump("yes" if yes else "no")
    # soundness of CDESC / ADESC-type descriptions: every produced D is a down-set
    for _ in range(3):
        U = sum(1 << w for w in range(G.m) if random.random() < 0.5)
        Phi = sum(1 << w for w in range(G.m) if random.random() < 0.2)
        B0 = sum(1 << w for w in range(G.m) if random.random() < 0.2)
        A0 = sum(1 << w for w in range(G.m) if random.random() < 0.2)
        for D in (e_desc(G, U, Phi), f_desc(G, U, Phi), anchored_e(G, B0, A0, U, Phi), anchored_f(G, A0, B0, U, Phi)):
            if D is None:
                continue
            if not is_downset(G, D):
                fail("desc not downset", G, None)
            if connects(G, D) and not yes:
                fail("desc accepts no-instance", G, None)
    if do_cdesc and not yes:
        if cdesc(G, 1, 1):
            fail("CDESC-sound", G, None)
    if not yes:
        return
    paths = all_shortest(G, cap=max_paths)
    bump("paths", len(paths))
    for P in paths:
        check_path(G, P)


def main():
    mode = sys.argv[1]
    seed = int(sys.argv[2])
    count = int(sys.argv[3])
    random.seed(seed)
    rng = random.Random(seed)
    made = 0
    while made < count:
        if mode == "rand":
            G = rand_general(rng, rng.randint(3, 8), rng.randint(3, 6), dens=rng.choice([0.2, 0.3]),
                             p_rel=rng.choice([0.2, 0.4]), p_tie=rng.choice([0.0, 0.3]), p_med=rng.choice([0.0, 0.3]))
            if G is None:
                bump("gen fail")
                continue
            made += 1
            check_inst(G, do_cdesc=True)
        else:
            rmin = int(sys.argv[4]) if len(sys.argv) > 4 else 6
            rmax = int(sys.argv[5]) if len(sys.argv) > 5 else 12
            r = rng.randint(rmin, rmax)
            g = planted_general(rng, r, rng.randint(0, 5), rng.randint(0, 3 * r), rng.randint(0, r),
                                p_rel=rng.choice([0.15, 0.3, 0.5]), p_tie=rng.choice([0.0, 0.2]))
            if g is None:
                bump("gen fail")
                continue
            made += 1
            G, P = g
            check_inst(G)
    out = {"mode": mode, "seed": seed, "count": count, "stats": STATS, "fails": FAIL}
    print(json.dumps(STATS, indent=1, sort_keys=True))
    with open("runs/tca-%s-%d.json" % (mode, seed), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
