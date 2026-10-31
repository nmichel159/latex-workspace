"""Checks of Lemma M1, Proposition M, Lemmas S1, S2 and Theorem T (r5-hard.md Section 2) on random planted instances.

Generator (own code): a planted path of r members with a random type word; consecutive member sides share a node;
s in the first, t in the last member side.  Mates: up-mates above random E-members, down-mates below random F-members,
free switches; random strict relations a < b only between chain types (F, F), (F, E), (E, E) (E = E-members and
up-mates, F = F-members and down-mates), so that no E-typed switch lies below an F-typed one and the planted path stays
valid; free switches get random relations consistent with this.  Random extra nodes on random sides; random middle
edges on comparable pairs; then P2 is completed pair by pair (fresh node on both E-sides or both F-sides, or a middle
witness through an existing common lower or upper neighbour).  All shortest valid paths are recomputed.
On every shortest valid path with no ties among its members:
  M1: for x in N_F, a in A: x in up(a), or x in NF(F#a), or a in S_x; |window(S_x)| <= 9;
  PropM: for every pair a1, a2 in A not both in one S_x (x in N_F) the description of Proposition M picks the path;
         dually for B;
  S1: for a in A and c < pos(a) < d in C(a): d - c <= 4;
  S2: a, a' in A at distance >= 3 are linked, and c < p < p' < d in C(a) | C(a') gives d - c <= 6.
Usage: python test_zone.py SEED COUNT RMIN RMAX
"""
import sys
import random
import time
from collections import Counter
import hlib
from hlib import Inst, bits, popcount
from gstar import Stars, Skel
import gdesc


def planted(rng, r, n_up, n_down, n_free, p_rel, p_side, p_med, p_mid_wit, p_back=0.1):
    I = Inst()
    word = [rng.choice("EF") for _ in range(r)]
    mem = ["p%d" % i for i in range(r)]
    for i in range(r):
        I.switch(mem[i])

    def addside(w, ty, nd):
        (I.addE if ty == "E" else I.addF)(w, nd)

    addside(mem[0], word[0], "s")
    addside(mem[r - 1], word[r - 1], "t")
    for i in range(r - 1):
        addside(mem[i], word[i], ("c", i))
        addside(mem[i + 1], word[i + 1], ("c", i))
    ups = ["u%d" % i for i in range(n_up)]
    downs = ["d%d" % i for i in range(n_down)]
    frees = ["f%d" % i for i in range(n_free)]
    for w in ups + downs + frees:
        I.switch(w)
    Em = [mem[i] for i in range(r) if word[i] == "E"]
    Fm = [mem[i] for i in range(r) if word[i] == "F"]
    ctype = {}
    for i in range(r):
        ctype[mem[i]] = word[i]
    for x in ups:
        ctype[x] = "E"
        if Em:
            I.less(rng.choice(Em), x)
    for y in downs:
        ctype[y] = "F"
        if Fm:
            I.less(y, rng.choice(Fm))
    for f in frees:
        ctype[f] = rng.choice("EF")
    allsw = list(I.swnames)
    # a random linear extension: F-typed before E-typed is not required, but every mate relation must agree with it
    order = allsw[:]
    rng.shuffle(order)
    for _ in range(len(order) ** 2):
        changed = False
        for (a, b) in list(I.lt):
            ia, ib = order.index(I.swnames[a]), order.index(I.swnames[b])
            if ia > ib:
                order[ia], order[ib] = order[ib], order[ia]
                changed = True
        if not changed:
            break
    rank = {w: i for i, w in enumerate(order)}
    if any(rank[I.swnames[a]] > rank[I.swnames[b]] for (a, b) in I.lt):
        raise ValueError("no linear extension found")
    for a in allsw:
        for b in allsw:
            if a == b or rank[a] > rank[b]:
                continue
            if (ctype[a], ctype[b]) in (("F", "F"), ("F", "E"), ("E", "E")) and rng.random() < p_rel:
                I.less(a, b)
    G0 = I.build()
    le = G0.le
    idx = I.sw
    # random extra nodes on random partner sides (non-path sides), each node in two sides
    nextra = int(p_side * len(allsw) * 2)

    def nonpath_side(w):
        if w in ctype and w.startswith("p"):
            return "F" if ctype[w] == "E" else "E"
        return rng.choice("EF")
    for k in range(nextra):
        w1, w2 = rng.sample(allsw, 2)
        addside(w1, nonpath_side(w1), ("x", k))
        addside(w2, nonpath_side(w2), ("x", k))
    # random middle edges on comparable pairs
    def pathty(w):
        return word[int(w[1:])] if w.startswith("p") else None

    def joins_paths(y, x):          # the private node of y - x lies in F_y and E_x
        return pathty(y) == "F" and pathty(x) == "E"
    for a in allsw:
        for b in allsw:
            if a != b and le[idx[a]][idx[b]] and not le[idx[b]][idx[a]] and rng.random() < p_med \
                    and not joins_paths(a, b):
                I.edge(a, b)
    # P2 completion
    G = I.build()
    for (a, b) in G.p2_bad():
        wa, wb = G.names[a], G.names[b]
        done = False
        if rng.random() < p_mid_wit:
            # lower or upper common neighbour in the order (not necessarily adjacent yet)
            cands = [z for z in range(G.m) if z not in (a, b) and
                     ((G.le[z][a] and G.le[z][b] and not G.le[a][z] and not G.le[b][z]) or
                      (G.le[a][z] and G.le[b][z] and not G.le[z][a] and not G.le[z][b]))]
            cands = [z for z in cands if not (joins_paths(G.names[z], wa) or joins_paths(G.names[z], wb) or
                                              joins_paths(wa, G.names[z]) or joins_paths(wb, G.names[z]))]
            if cands:
                z = rng.choice(cands)
                wz = G.names[z]
                if G.le[z][a]:
                    I.edge(wz, wa)
                    I.edge(wz, wb)
                else:
                    I.edge(wa, wz)
                    I.edge(wb, wz)
                done = True
        if not done:
            # prefer the type for which neither side is a member's path side
            pa = word[int(wa[1:])] if wa.startswith("p") else None
            pb = word[int(wb[1:])] if wb.startswith("p") else None
            opts = [ty for ty in "EF" if ty != pa and ty != pb]
            if opts:
                ty = rng.choice(opts)
            else:
                # opposite-type members: forward pattern of R_L (earlier partner meets later path side), sometimes back
                ia, ib = int(wa[1:]), int(wb[1:])
                later = pb if ia < ib else pa
                earlier = pa if ia < ib else pb
                ty = later if rng.random() > p_back else earlier
            addside(wa, ty, ("p2", wa, wb))
            addside(wb, ty, ("p2", wa, wb))
    G = I.build()
    return G


def C_of(G, S, K, P, a):
    """contact positions of F_a and of E_z, z upper middle neighbour of a"""
    p = K.pos[a]
    sides = [G.F[a]] + [G.E[z] for z in S.umn[a]]
    out = set()
    for c, i in enumerate(P):
        if c == p:
            continue
        mk = G.mask(i)
        if any(mk & sd for sd in sides):
            out.add(c)
    return out


def check_path(G, S, P, st):
    K = Skel(G, P)
    ws = [i >> 1 for i in P]
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            if G.le[ws[i]][ws[j]] and G.le[ws[j]][ws[i]]:
                st["paths with member ties (skipped)"] += 1
                return
    st["paths checked"] += 1
    A = bits(K.A)
    B = bits(K.B)
    pos = K.pos
    # M1
    Sx = {}
    for x in bits(K.NF):
        sx = [a for a in A if (S.NEstar[x] >> a) & 1]
        Sx[x] = sx
        if sx:
            span = max(pos[a] for a in sx) - min(pos[a] for a in sx)
            st["max span S_x"] = max(st["max span S_x"], span)
            assert span <= 8, "S_x span"
        for a in A:
            ok = (G.up[a] >> x) & 1 or (S.NFstar[a] >> x) & 1 or a in sx
            assert ok, "M1 fails"
            st["M1 pairs"] += 1
    Sy = {}
    for y in bits(K.NE):
        sy = [b for b in B if (S.NFstar[y] >> b) & 1]
        Sy[y] = sy
        if sy:
            assert max(pos[b] for b in sy) - min(pos[b] for b in sy) <= 8, "S_y span"
        for b in B:
            ok = (G.dn[b] >> y) & 1 or (S.NEstar[b] >> y) & 1 or b in sy
            assert ok, "M1 dual fails"
    # Prop M
    for i, a1 in enumerate(A):
        for a2 in A[i + 1:]:
            if any(a1 in Sx[x] and a2 in Sx[x] for x in Sx):
                continue
            D = hlib.describe_M(G, S, K, a1, a2, 1)
            assert gdesc.picks(G, K, D), "Prop M (F) fails"
            st["PropM F pairs"] += 1
            if abs(pos[a1] - pos[a2]) >= 9:
                st["PropM F pairs at distance >= 9"] += 1
    for i, b1 in enumerate(B):
        for b2 in B[i + 1:]:
            if any(b1 in Sy[y] and b2 in Sy[y] for y in Sy):
                continue
            D = hlib.describe_M(G, S, K, b1, b2, 0)
            assert gdesc.picks(G, K, D), "Prop M (E) fails"
            st["PropM E pairs"] += 1
    # S1, S2
    C = {a: C_of(G, S, K, P, a) for a in A}
    for a in A:
        p = pos[a]
        lo = [c for c in C[a] if c < p]
        hi = [d for d in C[a] if d > p]
        if lo and hi:
            st["S1 straddles"] += 1
            st["S1 max"] = max(st["S1 max"], max(hi) - min(lo))
            assert max(hi) - min(lo) <= 4, "S1"
    for a in A:
        for a2 in A:
            p, p2 = pos[a], pos[a2]
            if p2 - p < 3:
                continue
            linked = bool(G.F[a] & G.F[a2]) or bool(S.umn[a] & S.umn[a2])
            assert linked, "S2(a)"
            U = C[a] | C[a2]
            lo = [c for c in U if c < p]
            hi = [d for d in U if d > p2]
            if lo and hi:
                st["S2 straddles"] += 1
                st["S2 max"] = max(st["S2 max"], max(hi) - min(lo))
                assert max(hi) - min(lo) <= 6, "S2(b)"
    st["max |A|"] = max(st["max |A|"], len(A))
    st["max r"] = max(st["max r"], len(P))


def main():
    seed, count, rmin, rmax = (int(a) for a in sys.argv[1:5])
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        r = rng.randint(rmin, rmax)
        try:
            G = planted(rng, r, rng.randint(0, 4), rng.randint(0, 4), rng.randint(0, 3), rng.choice([0.1, 0.25, 0.4]),
                        rng.choice([0.0, 0.1, 0.3]), rng.choice([0.0, 0.2, 0.5]), rng.choice([0.0, 0.5, 1.0]),
                        rng.choice([0.0, 0.05, 0.2]))
        except ValueError:
            st["order with a tie (skipped)"] += 1
            continue
        if G.p2_bad():
            st["P2 not completed"] += 1
            continue
        st["instances"] += 1
        L, P0 = G.shortest()
        if L is None:
            st["no-instances"] += 1
            continue
        S = Stars(G)
        for P in G.all_shortest(limit=30, length=L):
            check_path(G, S, P, st)
    print("seed %d count %d r in [%d, %d]: %s  (%.1fs)" % (seed, count, rmin, rmax, dict(st), time.time() - t0))


if __name__ == "__main__":
    main()
