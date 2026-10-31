"""Checks of r4-hard.md Lemma 1.1, Lemmas 2.1-2.3, Proposition 2.4 (typed instances) and Lemma 4.3 (hub lemma) with
own code, exhaustive over all down-sets of random instances.
Usage: python r4hard_lemmas.py SEED COUNT"""
import random
import sys
from collections import Counter, deque
from zzlib import Inst, bits
from gswlib import random_zz_p2


def random_typed(rng, nv, npk, nb, nt, p_ord, p_edge, p_wit, harmless):
    """u = 0 in Vt, v = 1 in Pt; Vt = {0} + 2..nv, Pt = {1} + ...; witnesses: bottoms (tied to u) and tops (tied to
    v).  Main edges x < y, x in Vt, y in Pt.  harmless: bottoms adjacent to Vt only, tops to Pt only."""
    Vt = [0] + list(range(2, 2 + nv))
    Pt = [1] + list(range(2 + nv, 2 + nv + npk))
    nonw = Vt + Pt
    bots = list(range(2 + nv + npk, 2 + nv + npk + nb))
    tops = list(range(2 + nv + npk + nb, 2 + nv + npk + nb + nt))
    n = 2 + nv + npk + nb + nt
    rel = [(0, x) for x in range(n)] + [(x, 1) for x in range(n)]
    for b in bots:
        rel += [(b, 0), (0, b)]
    for t in tops:
        rel += [(t, 1), (1, t)]
    mids = Vt[1:] + Pt[1:]
    perm = list(mids)
    rng.shuffle(perm)
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < p_ord:
                rel.append((perm[i], perm[j]))
    I0 = Inst(n, rel, [], 0, 1)
    R = []
    for x in Vt:
        for y in Pt:
            if I0.lt(x, y) and (x, y) != (0, 1) and rng.random() < p_edge:
                R.append((x, y))
    for b in bots:
        for x in (Vt[1:] if harmless else mids):
            if rng.random() < p_wit:
                R.append((b, x))
    for t in tops:
        for y in (Pt[1:] if harmless else mids):
            if rng.random() < p_wit:
                R.append((y, t))
    I = Inst(n, rel, R, 0, 1)
    I.Vt, I.Pt, I.W = set(Vt), set(Pt), set(bots + tops)
    I.bots, I.tops = set(bots), set(tops)
    return I


def live(I, D, x):
    return ((D >> x) & 1) == 1 if x in I.Vt else ((D >> x) & 1) == 0


def components(I, D):
    par = list(range(I.n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in I.R:
        if ((D >> a) & 1) != ((D >> b) & 1):
            par[find(a)] = find(b)
    return find


def prop14(I):
    """Proposition 14 of theory-dc.md on the instance with the witnesses deleted."""
    Vt, Pt = I.Vt, I.Pt
    main = [(a, b) for a, b in I.R if a not in I.W and b not in I.W]
    adj = {x: [] for x in Vt | Pt}
    for a, b in main:
        adj[a].append(b)
        adj[b].append(a)
    Nset = {y: frozenset(x for x in Vt if I.lt(x, y)) for y in Pt}
    for ys in Pt:
        allowed = set(Nset[ys]) | {y for y in Pt if Nset[y] >= Nset[ys]}
        if 0 not in allowed or 1 not in allowed:
            continue
        seen = {0}
        q = deque([0])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y in allowed and y not in seen:
                    seen.add(y)
                    q.append(y)
        if 1 in seen:
            return True
    return False


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = Counter()
    for it in range(count):
        harmless = rng.random() < 0.7
        I = random_typed(rng, rng.randint(1, 5), rng.randint(1, 5), rng.randint(0, 3), rng.randint(0, 3),
                         rng.choice((0.2, 0.5, 0.8)), rng.choice((0.3, 0.6)), rng.choice((0.3, 0.6)), harmless)
        assert not I.check(), I.check()
        st["inst"] += 1
        Ds = I.downsets()
        for D in Ds:
            st["downsets"] += 1
            # Lemma 1.1 (a): main edge in G_D iff both ends live
            for a, b in I.R:
                if a in I.W or b in I.W:
                    continue
                x, y = (a, b) if I.lt(a, b) else (b, a)
                assert x in I.Vt and y in I.Pt
                inGD = ((D >> x) & 1) == 1 and ((D >> y) & 1) == 0
                if inGD != (live(I, D, x) and live(I, D, y)):
                    st["L11a_fail"] += 1
            # Lemma 1.1 (b): order relations as clauses on liveness
            for a in I.Vt | I.Pt:
                for b in I.Vt | I.Pt:
                    if a != b and I.le(a, b):
                        la, lb = live(I, D, a), live(I, D, b)
                        if a in I.Vt and b in I.Vt:
                            ok = (not lb) or la
                        elif a in I.Pt and b in I.Pt:
                            ok = (not la) or lb
                        elif a in I.Vt:
                            ok = la or lb
                        else:
                            ok = (not la) or (not lb)
                        if not ok:
                            st["L11b_fail"] += 1
            # Lemma 2.1 for bottoms / tops: b adjacent to x in G_D iff x not in D (bottom), iff x in D (top)
            for a, b in I.R:
                for w, x in ((a, b), (b, a)):
                    if w in I.bots:
                        if ((((D >> a) & 1) != ((D >> b) & 1))) != (((D >> x) & 1) == 0):
                            st["L21_fail"] += 1
                    if w in I.tops:
                        if ((((D >> a) & 1) != ((D >> b) & 1))) != (((D >> x) & 1) == 1):
                            st["L21_fail"] += 1
            # Lemma 2.2: a dead Vt element has no main edge in G_D
            for a, b in I.R:
                if a in I.W or b in I.W:
                    continue
                x, y = (a, b) if I.lt(a, b) else (b, a)
                inGD = ((D >> x) & 1) == 1 and ((D >> y) & 1) == 0
                if inGD and (not live(I, D, x) or not live(I, D, y)):
                    st["L22_fail"] += 1
            if harmless:
                find = components(I, D)
                comps_w = {find(w) for w in I.W}
                for x in I.Vt | I.Pt:
                    if live(I, D, x) and find(x) in comps_w:
                        st["L23_fail"] += 1
                # u, v connected in G_D iff connected by main edges between live elements
                par = list(range(I.n))

                def f2(a):
                    while par[a] != a:
                        a = par[a]
                    return a
                for a, b in I.R:
                    if a in I.W or b in I.W:
                        continue
                    if live(I, D, a) and live(I, D, b):
                        par[f2(a)] = f2(b)
                if (find(0) == find(1)) != (f2(0) == f2(1)):
                    st["L23_conn_fail"] += 1
        if harmless:
            # Proposition 2.4 when every Vt element is comparable with every Pt element
            if all(I.comparable(x, y) for x in I.Vt for y in I.Pt):
                st["P24_inst"] += 1
                if prop14(I) != I.zz_brute():
                    st["P24_fail"] += 1
                    print("PROP 2.4 MISMATCH")
    print("typed:", dict(sorted(st.items())))
    # Lemma 4.3 on random ZZ + P2 instances
    st = Counter()
    for it in range(count):
        I = random_zz_p2(rng, rng.randint(4, 10), rng.randint(0, 3), rng.randint(0, 3), rng.choice((0.1, 0.25)),
                         0.0, rng.choice((0.2, 0.4)))
        if I is None:
            continue
        inc = {x: [y for y in range(I.n) if not I.comparable(x, y)] for x in range(I.n)}
        for _ in range(20):
            n = rng.randint(1, 3)
            xs = [x for x in range(I.n) if len(inc[x]) >= n]
            if not xs:
                break
            A = rng.sample(xs, 1)
            # grow A and B greedily into an n x n block of incomparable pairs
            B = []
            cand = list(inc[A[0]])
            rng.shuffle(cand)
            for b in cand:
                if len(B) < n:
                    B.append(b)
            if len(B) < n:
                continue
            Acand = [a for a in range(I.n) if a not in A and all(not I.comparable(a, b) for b in B)]
            rng.shuffle(Acand)
            A += Acand[:n - 1]
            if len(A) < n:
                continue
            st["blocks"] += 1
            need = (n + 1) // 2

            def low(a, b):
                return [w for w in I.adj[a] if w in I.adj[b] and I.lt(w, a) and I.lt(w, b)]

            def upw(a, b):
                return [w for w in I.adj[a] if w in I.adj[b] and I.lt(a, w) and I.lt(b, w)]
            L = any(sum(1 for a in A if low(a, b)) >= need for b in B)
            U = any(sum(1 for b in B if upw(a, b)) >= need for a in A)
            if not (L or U):
                st["L43_fail"] += 1
                print("HUB LEMMA FAILS", A, B)
    print("hub:", dict(sorted(st.items())))


if __name__ == "__main__":
    main()
