"""Task B2: planted direct instances with hill climbing.  Every instance: validated, P2 asserted, P verified shortest by the exact solver; the proof is
run on P, on P reversed, on the reversed instance and on both.  Moves keep P2 and keep P shortest; rejected moves are counted.

Usage: run_planted.py SEED BASE SECONDS MOVES LOG      BASE as in zz_design.BASES.
Moves on the design: added contacts, removed strict pairs, ties, private witnesses, attacks (a class of highs put into the stars of several classes
of lows).  Moves on the instance: arbitrary edges, removed edges, added and removed relations (highs above highs, lows below lows), elements lifted out of
the class of u or lowered out of the class of v, new off-walk elements between two comparable elements; P2 is repaired by private top or bottom witnesses.
"""
import json
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from zz_core import Budget, ClaimFail, Inst, bits  # noqa: E402
from zz_design import BASES, near_move  # noqa: E402
from zz_proof import Cfg, Stage0, Walk, construct, general_claim  # noqa: E402

BUDGET = 60_000


# ----------------------------------------------------------------- design moves
def design_move(d, rng):
    if d.info.get("local") and rng.random() < 0.8:
        return near_move(d, rng)
    Apos = d.info["Apos"]
    Bpos = [z for pr in d.info["H"] for z in pr]
    r = len(d.word)
    kind = rng.choice(["addS", "addT", "unstrict", "tieA", "tieH", "wit", "attack", "attack", "addTcore", "addScore"])
    if kind == "addS":
        d.S[rng.choice(Apos)].add(rng.choice([p for p in range(1, r + 1) if d.word[p - 1] == "F"]))
    elif kind == "addScore":
        d.S[rng.choice(Apos)].add(rng.choice(Bpos))
    elif kind == "addT":
        d.T[rng.choice(Bpos)].add(rng.choice([p for p in range(1, r + 1) if d.word[p - 1] == "E"]))
    elif kind == "addTcore":
        d.T[rng.choice(Bpos)].add(rng.choice(Apos))
    elif kind == "unstrict":
        pairs = [(b, a) for a in Apos for b in Bpos if d.is_strict(b, a)]
        if not pairs:
            return "none"
        b, a = rng.choice(pairs)
        d.unset_strict(b, a)
        bs = [p for p in Bpos if d.cls[p - 1] == d.cls[b - 1]]
        aa = [p for p in Apos if d.cls[p - 1] == d.cls[a - 1]]
        for x in bs:
            for y in aa:
                if x not in d.S[y] and y not in d.T[x]:
                    d.S[y].add(x)
    elif kind == "tieA":
        x, y = rng.sample(Apos, 2)
        d.tie(x, y)
    elif kind == "tieH":
        x, y = rng.sample(Bpos, 2)
        d.tie(x, y)
    elif kind == "wit":
        if rng.random() < 0.5:
            a = rng.choice(Apos)
            q = [g for g in d.S[a] if (a, g) not in d.wS]
            if not q:
                return "none"
            d.wS.add((a, rng.choice(q)))
        else:
            b = rng.choice(Bpos)
            q = [g for g in d.T[b] if (b, g) not in d.wT]
            if not q:
                return "none"
            d.wT.add((b, rng.choice(q)))
    elif kind == "attack":
        a = rng.choice(Apos)
        aa = [p for p in Apos if d.cls[p - 1] == d.cls[a - 1]]
        for _ in range(rng.randint(2, 4)):
            b = rng.choice(Bpos)
            bs = [p for p in Bpos if d.cls[p - 1] == d.cls[b - 1]]
            for x in bs:
                d.T[x] |= set(aa)
    return kind


# ----------------------------------------------------------------- instance moves
def add_element(up, m, dnset, upset):
    """New element o with down-set dnset + o and up-set upset + o."""
    o = m
    b = 1 << o
    up = list(up)
    for z in bits(dnset):
        up[z] |= b
    up.append(upset | b)
    return up, m + 1, o


def repair_p2(up, edges, m, u, v, rng, cap):
    """P2 repair by private witnesses tied with v or with u."""
    edges = set(edges)
    for _ in range(60):
        I = Inst(m, up, edges, u, v)
        viol = I.p2_violations()
        if not viol:
            return up, edges, m
        if m + len(viol) > cap or len(viol) > 25:
            return None
        CLv = I.CL[v]
        CLu = I.CL[u]
        for x, y in viol:
            if rng.random() < 0.5:
                up, m, o = add_element(up, m, (1 << m) - 1, CLv)
                CLv |= 1 << o
                edges.add((x, o))
                edges.add((y, o))
            else:
                up, m, o = add_element(up, m, CLu, (1 << m) - 1)
                CLu |= 1 << o
                edges.add((o, x))
                edges.add((o, y))
    return None


def inst_move(I, P, rng, cap=520):
    """Returns (kind, new instance) or (kind, None)."""
    m, u, v = I.m, I.u, I.v
    Pset = set(P)
    Pedges = set()
    Wk = Walk(I, P)
    for i in range(len(P) - 1):
        lo, hi = (P[i], P[i + 1]) if Wk.labels[i] == "L" else (P[i + 1], P[i])
        Pedges.add((lo, hi))
    core = [x for x in range(m) if not I.tied(x, u) and not I.tied(x, v)]
    up = list(I.UP)
    edges = set(I.edges)
    kind = rng.choice(["edge", "edge", "rmedge", "rel", "relH", "relL", "unrel", "lift", "lower", "off", "off", "xg", "star", "star"])
    if kind == "star":
        # direct attack on (star): contacts that would make an interval between alpha and beta miss Pos[a] and Pos[h]; the solver must reject
        if len(Wk.A) <= 3 or len(Wk.B) <= 3 or m + 2 > cap:
            return kind, None
        S0 = Stage0(Wk, Cfg(), rng)
        Rl, Cl = list(bits(S0.R0)), list(bits(S0.C0))
        if not Rl or not Cl:
            return kind, None
        found = None
        for _ in range(40):
            a, h = rng.choice(Rl), rng.choice(Cl)
            if I.leq(h, a):
                continue
            Z = set(Wk.Pos(a)) | set(Wk.Pos(h))
            al, be = rng.choice(Rl), rng.choice(Cl)
            lo, hi = sorted((Wk.pos[al], Wk.pos[be]))
            if any(lo <= z <= hi for z in Z):
                continue
            found = (a, h, al, be)
            break
        if found is None:
            return kind, None
        a, h, al, be = found
        up, m, t = add_element(up, m, I.CL[u], (1 << m) - 1)
        edges.add((t, al))
        edges.add((t, h))
        up, m, w = add_element(up, m, (1 << m) - 1, I.CL[v])
        edges.add((be, w))
        edges.add((a, w))
    elif kind == "xg":
        # an off-walk element above a far high and with a common lower neighbour with two highs at distance 2: a small set of A_P in MB(x)
        idx = [i for i in range(1, len(P) - 1) if Wk.labels[i] == "L"]
        highs = list(bits(Wk.highs))
        if not idx or not highs or m >= cap:
            return kind, None
        i = rng.choice(idx)
        t = P[i]
        e = rng.choice(highs)
        if I.tied(e, v):
            return kind, None
        up, m2, o = add_element(up, m, I.DN[e] | I.DN[t], I.CL[v])
        edges.add((t, o))
        m = m2
    elif kind == "edge":
        pool = core if core and rng.random() < 0.8 else list(range(m))
        x = rng.choice(pool)
        ab = list(bits(I.USTR[x] & ~I.HI[x]))
        if not ab:
            return kind, None
        y = rng.choice(ab)
        if core and rng.random() < 0.6:
            ab2 = [t for t in ab if t in set(core)]
            if ab2:
                y = rng.choice(ab2)
        edges.add((x, y))
    elif kind == "rmedge":
        non = [e for e in edges if e not in Pedges]
        if not non:
            return kind, None
        edges.discard(rng.choice(non))
    elif kind in ("rel", "relH", "relL"):
        if kind == "rel":
            pool = core
        elif kind == "relH":
            pool = [x for x in core if Wk.highs >> x & 1]
        else:
            pool = [x for x in core if Wk.lows >> x & 1]
        if len(pool) < 2:
            return kind, None
        x, y = rng.sample(pool, 2)
        if not I.inc(x, y):
            return kind, None
        for p in bits(I.DN[x]):
            up[p] |= I.UP[y]
        # edges must stay strict; checked below
    elif kind == "unrel":
        pool = core
        if not pool:
            return kind, None
        x = rng.choice(pool)
        ab = [y for y in bits(I.USTR[x]) if y in set(core) and I.USTR[x] & I.DSTR[y] == 0]
        if not ab:
            return kind, None
        y = rng.choice(ab)
        for xx in bits(I.CL[x]):
            up[xx] &= ~I.CL[y]
        edges = {(a, b) for a, b in edges if not (I.tied(a, x) and I.tied(b, y))}
        if not Pedges <= edges:
            return kind, None
    elif kind == "lift":
        pool = [x for x in bits(I.CL[u]) if x != u]
        if not pool:
            return kind, None
        x = rng.choice(pool)
        up[x] &= ~(I.CL[u] & ~(1 << x))
    elif kind == "lower":
        pool = [x for x in bits(I.CL[v]) if x != v]
        if not pool:
            return kind, None
        x = rng.choice(pool)
        for z in bits(I.CL[v]):
            if z != x:
                up[z] &= ~(1 << x)
    elif kind == "off":
        if not core:
            return kind, None
        if m >= cap:
            return kind, None
        x = rng.choice(core + [u])
        ab = list(bits(I.USTR[x] & ((1 << m) - 1)))
        if not ab:
            return kind, None
        y = rng.choice(ab)
        up, m2, o = add_element(up, m, I.DN[x], I.UP[y])
        # random edges of the new element
        Itmp = Inst(m2, up, edges, u, v)
        low = list(bits(Itmp.DSTR[o]))
        high = list(bits(Itmp.USTR[o]))
        rng.shuffle(low)
        rng.shuffle(high)
        for z in low[:rng.randint(0, 2)]:
            edges.add((z, o))
        for z in high[:rng.randint(0, 2)]:
            edges.add((o, z))
        m = m2
    # strictness of all edges and validity of P
    Itmp = Inst(m, up, edges, u, v)
    for a, b in edges:
        if not Itmp.lt(a, b):
            return kind, None
    if not Itmp.lt(u, v):
        return kind, None
    if not Itmp.is_valid_walk(P):
        return kind, None
    rp = repair_p2(up, edges, m, u, v, rng, cap)
    if rp is None:
        return kind, None
    up, edges, m = rp
    J = Inst(m, up, edges, u, v)
    J.validate()
    return kind, J


# ----------------------------------------------------------------- driver
def dump(I, P, msg, path):
    data = dict(m=I.m, up=[hex(x) for x in I.UP], edges=sorted(I.edges), u=I.u, v=I.v, P=P, fail=msg)
    if os.path.exists(os.path.dirname(path)) and len(os.listdir(os.path.dirname(path))) < 12:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)


def test_all(I, P, cfg, rng, st, fails, tag, seed, base):
    J = I.reversed_instance()
    for nm, K, Q in (("id", I, P), ("rev", I, P[::-1]), ("op", J, P), ("oprev", J, P[::-1])):
        try:
            ex = construct(Walk(K, Q), cfg, rng, st)
            st["exit %s %s" % (nm, ex)] += 1
            general_claim(Walk(K, Q), cfg, rng, st)
        except ClaimFail as e:
            fails.append((tag, nm, str(e)))
            os.makedirs(os.path.join(HERE, "runs", "ce"), exist_ok=True)
            dump(K, Q, str(e), os.path.join(HERE, "runs", "ce", "%s-%d-%d.json" % (base, seed, len(fails))))


def main():
    seed, base, secs, moves, logf = int(sys.argv[1]), sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    st = Counter()
    acc, rej = Counter(), Counter()
    fails = []
    cfg = Cfg()
    t0 = time.time()
    rounds = 0
    while time.time() - t0 < secs:
        rounds += 1
        d = BASES[base](rng)
        I, P = d.build()
        I.validate()
        if not I.p2():
            st["base: P2 fails (dropped)"] += 1
            continue
        if I.shortest_walk(bound=len(P) - 1, budget=BUDGET) is not None:
            st["base: planted walk not shortest (dropped)"] += 1
            continue
        st["base instances verified"] += 1
        test_all(I, P, cfg, rng, st, fails, "base", seed, base)
        # design moves
        na = 0
        for mv in range(moves):
            if time.time() - t0 > secs:
                break
            d2 = d.copy()
            kind = design_move(d2, rng)
            if kind == "none":
                continue
            I2, P2 = d2.build()
            if not I2.p2():
                rej["D " + kind + " (P2)"] += 1
                continue
            try:
                if I2.shortest_walk(bound=len(P2) - 1, budget=BUDGET) is not None:
                    rej["D " + kind] += 1
                    continue
            except Budget:
                rej["D " + kind + " (budget)"] += 1
                continue
            acc["D " + kind] += 1
            d, I, P = d2, I2, P2
            na += 1
            if na % 6 == 0:
                test_all(I, P, cfg, rng, st, fails, "dmove", seed, base)
        test_all(I, P, cfg, rng, st, fails, "dsat", seed, base)
        # instance moves
        na = 0
        for mv in range(moves):
            if time.time() - t0 > secs:
                break
            try:
                kind, J = inst_move(I, P, rng)
            except ClaimFail as e:
                fails.append(("inst_move", "id", str(e)))
                continue
            if J is None:
                rej["I " + kind + " (invalid)"] += 1
                continue
            try:
                if J.shortest_walk(bound=len(P) - 1, budget=BUDGET) is not None:
                    rej["I " + kind] += 1
                    continue
            except Budget:
                rej["I " + kind + " (budget)"] += 1
                continue
            acc["I " + kind] += 1
            I = J
            na += 1
            if na % 6 == 0:
                test_all(I, P, cfg, rng, st, fails, "imove", seed, base)
        test_all(I, P, cfg, rng, st, fails, "isat", seed, base)
        # other shortest walks
        try:
            others = I.all_shortest(len(P) - 1, cap=8)
        except RecursionError:
            others = []
        for Q in others:
            if Q != P:
                st["other shortest walks"] += 1
                test_all(I, Q, cfg, rng, st, fails, "other", seed, base)
    with open(logf, "w", encoding="utf-8") as lg:
        print("base", base, "seed", seed, "rounds", rounds, "time", round(time.time() - t0, 1), file=lg)
        print("accepted", dict(acc), file=lg)
        print("rejected", dict(rej), file=lg)
        for k in sorted(st):
            print(k, st[k], file=lg)
        print("FAILURES:", fails[:8] if fails else "none", file=lg)


if __name__ == "__main__":
    main()
