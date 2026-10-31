"""rv-r6-chain, link L3: F0 and "valid path exists iff some down-set connects s and t" in the general switch form,
with ties and empty sides, checked exhaustively on random ZZ + P2 instances (own SF of rvc_lib).

usage: python rvc_l3.py SEED COUNT NMMIN NMMAX
For every instance (P2 required): all down-sets D of the switch preorder; for each D that connects s and t, a
shortest walk of picked sides is built and checked to be a valid path (distinct switches, consecutive sides meet,
s in the first, t in the last, no conflict pair E_w, F_z with w <= z).  All valid paths with at most RMAX sides
are enumerated (DFS, own); for each P: L = down(W_F) is a down-set that picks P and connects; and for every down-set
D: (D picks every member of P) iff (L subset D and D disjoint from Up).  Finally: some D connects iff (s = t or a
valid path exists).  Counted: instances with ties among the switches, with empty sides, with s = t.
"""
import sys
import os
import random
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rvc_lib as L     # noqa: E402
import rvc_src as S     # noqa: E402

RMAX = int(os.environ.get("RVC_RMAX", "6"))


def picked_walk(sf, D):
    """Shortest walk of sides picked by D from s to t (list of sides) or None."""
    sides = [(w, 1) if (D >> w) & 1 else (w, 0) for w in range(sf.m)]
    sides = [X for X in sides if sf.smask(X)]
    start = [X for X in sides if (sf.smask(X) >> sf.s) & 1]
    par = {X: None for X in start}
    dq = deque(start)
    while dq:
        X = dq.popleft()
        if (sf.smask(X) >> sf.t) & 1:
            out = []
            while X is not None:
                out.append(X)
                X = par[X]
            return out[::-1]
        for Y in sides:
            if Y not in par and sf.smask(X) & sf.smask(Y):
                par[Y] = X
                dq.append(Y)
    return None


def is_valid(sf, P):
    if not P:
        return sf.s == sf.t
    if not (sf.smask(P[0]) >> sf.s) & 1 or not (sf.smask(P[-1]) >> sf.t) & 1:
        return False
    if len({w for w, _ in P}) != len(P):
        return False
    for a, b in zip(P, P[1:]):
        if not sf.smask(a) & sf.smask(b):
            return False
    for (w, ty) in P:
        for (z, tz) in P:
            if ty == 0 and tz == 1 and sf.le[w][z]:
                return False
    return True


def valid_paths(sf, rmax, cap=4000):
    out = []
    sides = sf.sides()

    def rec(P, Up, Dn):
        if len(out) >= cap:
            return
        X = P[-1]
        if (sf.smask(X) >> sf.t) & 1:
            out.append(list(P))
        if len(P) >= rmax:
            return
        for Y in sides:
            if Y in P or not sf.smask(X) & sf.smask(Y):
                continue
            w, ty = Y
            if any(w == z for z, _ in P):
                continue
            if ty == 0:
                if (Dn >> w) & 1:
                    continue
                rec(P + [Y], Up | sf.up[w], Dn)
            else:
                if (Up >> w) & 1:
                    continue
                rec(P + [Y], Up, Dn | sf.down[w])

    for X in sides:
        if (sf.smask(X) >> sf.s) & 1:
            w, ty = X
            rec([X], sf.up[w] if ty == 0 else 0, sf.down[w] if ty == 1 else 0)
    return out


def picks(sf, D, P):
    return all(((D >> w) & 1) == ty for w, ty in P)


def main():
    seed, count, a, b = (int(x) for x in sys.argv[1:5])
    rng = random.Random(seed)
    st = Counter()
    for it in range(count):
        zd = S.random_zz(rng, rng.randint(a, b))
        z = L.ZZ(zd["q"], zd["le"], zd["R"], zd["u"], zd["v"])
        if z.p2_bad():
            st["no P2 (skipped)"] += 1
            continue
        try:
            sf = L.SF(z)
        except ValueError:
            st["u ~ v (skipped)"] += 1
            continue
        st["instances"] += 1
        ties = any(sf.cls[i] != (1 << i) for i in range(sf.m))
        empt = any(not sf.E[i] or not sf.F[i] for i in range(sf.m))
        st["with ties"] += ties
        st["with empty sides"] += empt
        st["s = t"] += sf.s == sf.t
        downs = sf.count_downsets()
        st["down-sets"] += len(downs)
        anyc = False
        for D in downs:
            if not sf.is_down(D):
                st["ERROR enumerated set not a down-set"] += 1
            if sf.connects(D):
                anyc = True
                W = picked_walk(sf, D)
                if sf.s == sf.t:
                    continue
                if W is None or not is_valid(sf, W):
                    st["ERROR connecting D without a valid picked path"] += 1
        Ps = valid_paths(sf, RMAX)
        st["valid paths"] += len(Ps)
        for P in Ps:
            if not is_valid(sf, P):
                st["ERROR enumerator"] += 1
            WE = sum(1 << w for w, ty in P if ty == 0)
            WF = sum(1 << w for w, ty in P if ty == 1)
            Up = sf.upclose(WE)
            Ld = sf.downclose(WF)
            if Up & Ld:
                st["ERROR valid path with Up cap L nonempty"] += 1
            if not sf.is_down(Ld) or not picks(sf, Ld, P) or not sf.connects(Ld):
                st["ERROR L does not pick / connect"] += 1
            for D in downs:
                if picks(sf, D, P) != ((Ld & ~D) == 0 and (D & Up) == 0):
                    st["ERROR F0 equivalence"] += 1
                    break
        exists = sf.s == sf.t or bool(Ps) or sf.shortest() is not None
        if anyc != exists:
            st["ERROR yes iff (s = t or valid path)"] += 1
        if anyc and sf.s != sf.t and not any(True for X in sf.sides() if (sf.smask(X) >> sf.s) & 1):
            st["ERROR"] += 1
        st["yes"] += anyc
        if sf.s == sf.t and not any((sf.smask(X) >> sf.s) & 1 for X in sf.sides()):
            st["s = t and no side contains s (no valid path with r >= 1)"] += 1
    print("rvc_l3 seed %d count %d nm %d-%d RMAX %d" % (seed, count, a, b, RMAX))
    for kk in sorted(st):
        print("  %-60s %s" % (kk, st[kk]))


if __name__ == "__main__":
    main()
