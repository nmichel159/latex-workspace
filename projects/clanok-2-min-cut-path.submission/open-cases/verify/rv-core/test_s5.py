"""Section 5 (and Lemma G of 3.2) of r5-core.md on random general instances with P2, with the reviewer's own code.

For every shortest valid path P of every yes-instance:
  LG   Lemma G: random U (unions of NE of random centres, or random sets); E- and F-descriptions with the flips of
       Lemma G give L <= D <= Q - Up and connect;
  E1   B0 = B, no centre, no flip (and dually A0 = A);
  E2   every pair b1, b2 in B with |pos| distance >= 5 (>= 3 when the instance has no middle edges):
         out-empty claim (with contracted centres), description as written (contracted centres, Phi = f*),
         repair R1 (Phi = A & U), repair R2 (hat centres E_b + F_v, v < b, F_v & E_b != 0, uncontracted, Phi = f*);
  F2   the dual of E2;
  S52  Prop. 5.2': random A1 <= A, B0 <= B with B <= down(B0) | U (down(a) - [a]); D picks every member;
       also with B0 an arbitrary set of switches (hypothesis B0 <= L dropped), to show the hypothesis is needed;
  FA   facts (a), (b) of the proof of 5.2.
usage: python test_s5.py SEED COUNT RMIN RMAX EXTRA [style] [nomiddle]
"""
import sys
import random
from collections import Counter
from gen import gen
from sw import path_data, describe, contracted_sets, NE, NF, bits, enon, fnon


def fstarA(G, pd, b):
    r = 0
    for a in bits(pd["A"]):
        Xa = G.E[a]
        if Xa & G.E[b] or any(G.strict_lt(v, b) and G.F[v] & G.E[b] and G.F[v] & Xa for v in range(G.m)):
            r |= 1 << a
    return r


def fstarB(G, pd, a):
    r = 0
    for b in bits(pd["B"]):
        Xb = G.F[b]
        if Xb & G.F[a] or any(G.strict_lt(a, v) and G.E[v] & G.F[a] and G.E[v] & Xb for v in range(G.m)):
            r |= 1 << b
    return r


def hatE(G, b):
    Z = G.E[b]
    for v in range(G.m):
        if G.strict_lt(v, b) and G.F[v] & G.E[b]:
            Z |= G.F[v]
    return Z


def hatF(G, a):
    Z = G.F[a]
    for v in range(G.m):
        if G.strict_lt(a, v) and G.E[v] & G.F[a]:
            Z |= G.E[v]
    return Z


def picks_all(G, D, pd):
    return D is not None and (pd["L"] & ~D) == 0 and (pd["Up"] & D) == 0


def run(seed, count, rmin, rmax, extra, style, middle):
    rng = random.Random(seed)
    C = Counter()
    examples = []
    for it in range(count):
        r = rng.randint(rmin, rmax)
        G = gen(rng, r, extra, style=style, middle=middle, p_rel=rng.choice([0.05, 0.15, 0.3]),
                n_extra_nodes=rng.randint(0, 6), p_medge=rng.choice([0, 0.1, 0.3]))
        if G.p2_violations():
            C["p2-fail(generator bug)"] += 1
            continue
        Lsp, paths = G.shortest_valid_paths()
        if Lsp is None:
            C["no-instances"] += 1
            continue
        C["yes-instances"] += 1
        hasmid = bool(G.medges)
        dmin = 5 if hasmid else 3
        full = (1 << G.m) - 1
        En, Fn = enon(G), fnon(G)
        for P in paths[:20]:
            C["paths"] += 1
            pd = path_data(G, P)
            WE, WF, Up, L, A, B, pos = pd["WE"], pd["WF"], pd["Up"], pd["L"], pd["A"], pd["B"], pd["pos"]
            onP = WE | WF
            # ---- facts (a), (b)
            for y in bits(L & ~onP):
                if G.F[y]:
                    win = [pos[c] for c in bits(onP) if G.side[P[pos[c] - 1]] & G.F[y]]
                    C["FA-a tested"] += 1
                    if win and max(win) - min(win) > 2:
                        C["FA-a VIOLATED"] += 1
            # ---- Lemma G, random U
            for _ in range(4):
                if rng.random() < 0.5:
                    U = 0
                    for _ in range(rng.randint(0, 2)):
                        Z = rng.choice([G.side[i] for i in range(2 * G.m) if G.side[i]] + [1 << rng.randrange(G.N)])
                        U |= NE(G, Z)
                else:
                    U = rng.getrandbits(G.m)
                out = L & En & ~U
                G1 = (En & ~U) & ~L
                inn = sum(1 << a for a in bits(A) if not (G.dnc(1 << a) & G1))
                D = describe(G, "E", 0, 0, U, out | inn)
                C["LG-E tested"] += 1
                if not (picks_all(G, D, pd) and G.connects(D)):
                    C["LG-E FAILED"] += 1
                Uf = U if rng.random() < 0.5 else rng.getrandbits(G.m)
                outf = Up & Fn & ~Uf
                G1f = (Fn & ~Uf) & ~Up
                innf = sum(1 << b for b in bits(B) if not (G.upc(1 << b) & G1f))
                D = describe(G, "F", 0, 0, Uf, outf | innf)
                C["LG-F tested"] += 1
                if not (picks_all(G, D, pd) and G.connects(D)):
                    C["LG-F FAILED"] += 1
            # ---- E1 / F1
            D = describe(G, "E", B, 0, 0, 0)
            C["E1 tested"] += 1
            if not (picks_all(G, D, pd) and G.connects(D)):
                C["E1 FAILED"] += 1
            D = describe(G, "F", 0, A, 0, 0)
            C["F1 tested"] += 1
            if not (picks_all(G, D, pd) and G.connects(D)):
                C["F1 FAILED"] += 1
            # ---- E2
            Bl = list(bits(B))
            for i in range(len(Bl)):
                for j in range(i + 1, len(Bl)):
                    b1, b2 = Bl[i], Bl[j]
                    if abs(pos[b1] - pos[b2]) < dmin:
                        continue
                    C["E2 pairs"] += 1
                    B0 = (1 << b1) | (1 << b2)
                    dB = G.dnc(B0)
                    Ec, Fc, mp = contracted_sets(G, [G.F[v] for v in bits(dB)])
                    U = NE(G, Ec[b1], Ec) | NE(G, Ec[b2], Ec)
                    if (L & En & ~U) & ~dB:
                        C["E2 out-nonempty (claim violated)"] += 1
                        examples.append(("E2-out", seed, it))
                    Phi = fstarA(G, pd, b1) | fstarA(G, pd, b2)
                    D = describe(G, "E", B0, 0, U, Phi)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["E2 as written FAILED"] += 1
                        if len(examples) < 30:
                            examples.append(("E2-written", seed, it, G.names[b1], G.names[b2]))
                    D = describe(G, "E", B0, 0, U, A & U)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["E2 repair R1 (Phi = A&U) FAILED"] += 1
                    C["E2 |A&U| - |f*| sum"] += bin(A & U).count("1") - bin(Phi).count("1")
                    Uh = NE(G, hatE(G, b1)) | NE(G, hatE(G, b2))
                    if (L & En & ~Uh) & ~dB:
                        C["E2 R2 out-nonempty"] += 1
                    D = describe(G, "E", B0, 0, Uh, Phi)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["E2 repair R2 (hat centres, Phi=f*) FAILED"] += 1
                    if (A & Uh) != Phi:
                        C["E2 R2: A&U_hat != f*"] += 1
                    if not hasmid:
                        U0 = NE(G, G.E[b1]) | NE(G, G.E[b2])
                        fA = sum(1 << a for a in bits(A) if G.E[a] & (G.E[b1] | G.E[b2]))
                        C["E2 no-middle pairs"] += 1
                        if fA != Phi:
                            C["E2 no-middle: f_A != f*"] += 1
                        D = describe(G, "E", B0, 0, U0, fA)
                        if not (picks_all(G, D, pd) and G.connects(D)):
                            C["E2 no-middle uncontracted, Phi=f_A FAILED"] += 1
            # ---- F2
            Al = list(bits(A))
            for i in range(len(Al)):
                for j in range(i + 1, len(Al)):
                    a1, a2 = Al[i], Al[j]
                    if abs(pos[a1] - pos[a2]) < dmin:
                        continue
                    C["F2 pairs"] += 1
                    A0 = (1 << a1) | (1 << a2)
                    uA = G.upc(A0)
                    Ec, Fc, mp = contracted_sets(G, [G.E[v] for v in bits(uA)])
                    U = NF(G, Fc[a1], Fc) | NF(G, Fc[a2], Fc)
                    if (Up & Fn & ~U) & ~uA:
                        C["F2 out-nonempty (claim violated)"] += 1
                    Phi = fstarB(G, pd, a1) | fstarB(G, pd, a2)
                    D = describe(G, "F", 0, A0, U, Phi)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["F2 as written FAILED"] += 1
                    D = describe(G, "F", 0, A0, U, B & U)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["F2 repair R1 FAILED"] += 1
                    Uh = NF(G, hatF(G, a1)) | NF(G, hatF(G, a2))
                    D = describe(G, "F", 0, A0, Uh, Phi)
                    if not (picks_all(G, D, pd) and G.connects(D)):
                        C["F2 repair R2 FAILED"] += 1
            # ---- Prop 5.2'
            for _ in range(3):
                A1 = rng.getrandbits(G.m) & A
                B0 = rng.getrandbits(G.m) & B
                D = G.dnc(B0)
                for a in bits(A1):
                    cls = G.dn[a] & G.up[a]
                    D |= G.dn[a] & ~cls
                if B & ~D:
                    continue
                C["S52 tested"] += 1
                if not (picks_all(G, D, pd) and G.connects(D)):
                    C["S52 FAILED"] += 1
                B0x = rng.getrandbits(G.m)
                Dx = G.dnc(B0x)
                for a in bits(A1):
                    cls = G.dn[a] & G.up[a]
                    Dx |= G.dn[a] & ~cls
                if not (B & ~Dx):
                    C["S52 arbitrary-B0 tested"] += 1
                    if not picks_all(G, Dx, pd):
                        C["S52 arbitrary-B0 fails (hypothesis needed)"] += 1
    for k in sorted(C):
        print("%-48s %d" % (k, C[k]))
    for e in examples[:30]:
        print("example", e)


if __name__ == "__main__":
    a = sys.argv
    run(int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6] if len(a) > 6 else "flip",
        not (len(a) > 7 and a[7] == "nomiddle"))
