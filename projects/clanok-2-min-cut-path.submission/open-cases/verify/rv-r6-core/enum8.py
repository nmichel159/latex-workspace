"""Exhaustive check of r5-core.md Section 8 on all ZZ instances with K middle elements (own enumerator).

Instances (the convention of verify/rv-core-65.md Section 3.1, re-implemented): elements u = 0, v = 1 and K middle
elements; every preorder on the middle elements (as relation matrices), u strictly below and v strictly above every
middle element; every set R of strict pairs except {u, v}.

Per instance: P2 from the ZZ definition (own) = P2 of the own switch form; for every down-set of the middle elements
the ZZ graph G_D (definition) and the picked hypergraph of the switch form agree on u-v / s-t connectivity; yes iff
some down-set connects iff a valid path exists.  Per shortest valid path of a yes-instance: Lemma 6.3 bound, and
the proof of Theorem 8.2 (proof8.levels) in modes 'proof' and 'stress' with every claim checked; the final
intersection is also tested in the ZZ graph.  IDESC with all terms (both kinds, <= k tools, every flag pattern,
flips inside the caught switches, anchors) on every instance of the part when K <= 3, on a deterministic sample
otherwise: every term gives a down-set; on yes-instances some intersection of the Theorem 8.2 form connects; on
no-instances no term connects (and hence no intersection).

usage: python enum8.py K PART NPARTS [IDESC_EVERY] [LOG]
"""
import sys
import time
import itertools
from collections import Counter
from zzl import zz_to_sw, zz_connects, zz_p2, all_shortest_valid_paths, Skel, bits, popcount, term_D, kparam
import proof8


def preorders(K):
    pairs = [(a, b) for a in range(K) for b in range(K) if a != b]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[a == b for b in range(K)] for a in range(K)]
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                le[a][b] = True
        ok = all(not (le[a][b] and le[b][c]) or le[a][c] for a in range(K) for b in range(K) for c in range(K))
        if ok:
            out.append(le)
    return out


def all_terms(I, k, N, anchors_ok=True):
    """Yield (kind, T, Tp, anchors_mask, Phi, D) for every term of IDESC with <= k tools, every flag pattern,
    every flip set inside U (size <= 9k), and anchor sets of size <= N (anchors of the kind's opposite type:
    F-anchors Y0 for E-terms, E-anchors X0 for F-terms; any switches)."""
    m = I.m
    sw = list(range(m))
    anc_sets = [0]
    if anchors_ok:
        anc_sets = []
        for r in range(0, min(N, m) + 1):
            for c in itertools.combinations(sw, r):
                anc_sets.append(sum(1 << a for a in c))
    for kind in ("E", "F"):
        for t in range(0, min(k, m) + 1):
            for T in itertools.combinations(sw, t):
                U = 0
                for x in T:
                    U |= I.NEs[x] if kind == "E" else I.NFs[x]
                Ul = list(bits(U))
                for fl in range(1 << t):
                    Tp = [T[i] for i in range(t) if (fl >> i) & 1]
                    for anc in anc_sets:
                        for r in range(0, min(9 * k, len(Ul)) + 1):
                            for ph in itertools.combinations(Ul, r):
                                Phi = sum(1 << a for a in ph)
                                D, U2, S, G = term_D(I, kind, list(T), Tp, anc, Phi)
                                yield kind, T, Tp, anc, Phi, D


def idesc_check(I, isyes, st, zzconn):
    m = I.m
    k, N = kparam(m)
    free = set()      # D of anchor-free terms
    anch = set()      # D of F-terms with E-anchors (<= N)
    anyD = set()
    for kind, T, Tp, anc, Phi, D in all_terms(I, k, N):
        st["idesc terms"] += 1
        if not I.is_down(D):
            st["IDESC TERM NOT A DOWN-SET FAIL"] += 1
        anyD.add(D)
        if anc == 0:
            free.add(D)
        elif kind == "F" and popcount(anc) <= N:
            anch.add(D)
    # intersections of <= k terms of the Theorem 8.2 form: <= k-1 anchor-free terms and one last term
    # (anchor-free or anchored F-term)
    lastset = free | anch
    reach = {I.full}
    for _ in range(k - 1):
        reach = reach | {a & b for a in reach for b in free}
    form_ok = any(I.connects(a & b) for a in reach for b in lastset)
    single_ok = any(I.connects(D) for D in anyD)
    # intersections of <= k terms of any kind (IDESC as defined, anchors anywhere, here not limited in total)
    if isyes:
        st["idesc yes"] += 1
        if not form_ok:
            st["IDESC MISSES A YES-INSTANCE (THM 8.2 FORM) FAIL"] += 1
        if single_ok:
            st["idesc yes: single term suffices"] += 1
    else:
        st["idesc no"] += 1
        for D in anyD:
            if I.connects(D):
                st["IDESC TERM CONNECTS ON A NO-INSTANCE FAIL"] += 1
            if zzconn(D):
                st["IDESC TERM CONNECTS IN ZZ ON A NO-INSTANCE FAIL"] += 1


def main():
    K = int(sys.argv[1])
    part, nparts = int(sys.argv[2]), int(sys.argv[3])
    every = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    logp = sys.argv[5] if len(sys.argv) > 5 else None
    q = K + 2
    st = Counter()
    t0 = time.time()
    pres = preorders(K)
    st["preorders"] = len(pres)
    logf = open(logp, "a", encoding="utf-8") if logp else None

    def out(s):
        print(s, flush=True)
        if logf:
            logf.write(s + "\n")
            logf.flush()
    import os
    out("enum8 K=%d part %d/%d idesc_every=%d preorders=%d pid=%d" % (K, part, nparts, every, len(pres), os.getpid()))
    inst_id = 0
    for pi, lem in enumerate(pres):
        if pi % nparts != part:
            continue
        le = [[False] * q for _ in range(q)]
        for a in range(q):
            le[0][a] = True
            le[a][1] = True
            le[a][a] = True
        for a in range(K):
            for b in range(K):
                le[a + 2][b + 2] = lem[a][b]
        strict = [(0, w) for w in range(2, q)] + [(w, 1) for w in range(2, q)]
        strict += [(a + 2, b + 2) for a in range(K) for b in range(K) if lem[a][b] and not lem[b][a]]
        for mask in range(1 << len(strict)):
            R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
            st["instances"] += 1
            inst_id += 1
            p2z = zz_p2(q, le, R)
            I, mid = zz_to_sw(q, 0, 1, le, R)
            p2s = I.p2_switch()
            if p2z != p2s:
                st["P2 ZZ != P2 SWITCH FAIL"] += 1
            if not p2z:
                continue
            st["P2 instances"] += 1
            bott = sum(1 << a for a in range(q) if le[a][0])

            def zzconn(D, mid=mid, bott=bott, R=R):
                Df = bott
                for i in bits(D):
                    Df |= 1 << mid[i]
                return zz_connects(q, 0, 1, R, Df)
            yes = False
            for D in I.downsets():
                a = I.connects(D)
                b = zzconn(D)
                if a != b:
                    st["SWITCH FORM != ZZ ON A DOWN-SET FAIL"] += 1
                yes = yes or b
            r, paths = all_shortest_valid_paths(I)
            if yes != (r is not None):
                st["VALID PATH EXISTS != YES FAIL"] += 1
            if yes:
                st["yes"] += 1
            else:
                st["no"] += 1
            if yes:
                st["shortest paths"] += len(paths)
                st["max paths per instance"] = max(st["max paths per instance"], len(paths))
                for P in paths:
                    Sk = Skel(I, P)
                    if Sk.Up & Sk.L:
                        st["Up MEETS L FAIL"] += 1
                    proof8.lemma63_check(I, Sk, st)
                    # bad pairs (r5-core 6.4): y < x, x in N_F - A, y in N_E - B
                    nb = 0
                    for x in bits(Sk.NF_ & ~Sk.A):
                        for y in bits(Sk.NE_ & ~Sk.B):
                            if I.le[y][x] and not I.le[x][y]:
                                nb += 1
                    if nb:
                        st["paths with bad pairs"] += 1
                    for mode in ("proof", "stress"):
                        D, terms, nlev, status = proof8.levels(I, Sk, mode, st)
                        if status == "final":
                            if not zzconn(D):
                                st["FINAL D DOES NOT CONNECT IN ZZ FAIL (%s)" % mode] += 1
                        elif status == "error":
                            st["PROOF ERROR (%s) FAIL" % mode] += 1
            if every and inst_id % every == 0:
                idesc_check(I, yes, st, zzconn)
        if (pi + 1) % 10 == 0 or pi == len(pres) - 1:
            out("  preorder %d/%d  instances %d  P2 %d  yes %d  paths %d  %.0fs" % (
                pi + 1, len(pres), st["instances"], st["P2 instances"], st["yes"], st["shortest paths"],
                time.time() - t0))
    out("SUMMARY enum8 K=%d part %d/%d (%.0fs)" % (K, part, nparts, time.time() - t0))
    for key in sorted(st):
        out("  %s: %d" % (key, st[key]))
    fails = [key for key in st if key.endswith("FAIL") and st[key]]
    out("FAILURES: %s" % (", ".join(fails) if fails else "none"))
    if logf:
        logf.close()


if __name__ == "__main__":
    main()
