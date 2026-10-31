"""Exhaustive check of the relaxations on small NO-instances of general ZZ + P2 (agent r4-search).

Facts (proved in the report, Section 3.2): for a fixed preorder, (a) 'no-instance' is closed under removing real
edges; (b) P2 is closed under adding real edges; (c) 'AC (PC, SPC, SPPC) does not refute' is closed under adding real
edges (the CSP of a subset of edges is an induced sub-CSP with the same L, and consistency closures are monotone).
Hence a relaxation fails on some P2 no-instance with a given order iff it fails on some *maximal* no-instance (no
real edge can be added without creating a consistent zigzag) that satisfies P2.
Method: every preorder on q elements with u least and v greatest (middle poset up to isomorphism, class sizes and
the sizes of the classes of u and v up to automorphism); branch and bound over the strictly comparable pairs
enumerating the maximal no-instances (include a pair only if the result stays a no-instance; at a leaf every
excluded pair must create a yes-instance; prune when included + undecided edges violate P2 or when some excluded pair
can no longer create a yes-instance); leaves reduced to orbits under the automorphisms of the order; then AC, PC and,
if PC fails, SPC and SPPC.
Output: counts; relaxation failures written to runs/enum-no-q*.jsonl.
Usage: python enum_no.py Q"""
import sys
import json
import time
import itertools
from common import make_zz, HERE
import zz
import pcfast
import variants
from posets import posets
from enum_yes import size_assignments, build_order, order_aut


class LOrder:
    def __init__(self, q, le):
        self.q, self.le = q, le
        self.u, self.v = 0, q - 1
        self.pairs = [(a, b) for a in range(q) for b in range(q)
                      if le[a][b] and not le[b][a] and (a, b) != (0, q - 1)]
        self.P = len(self.pairs)
        self.pidx = {p: i for i, p in enumerate(self.pairs)}
        z0 = make_zz(q, le, [], 0, q - 1)
        self.downs = zz.downsets(z0)
        self.cuts = []
        for D in self.downs:
            m = 0
            for i, (a, b) in enumerate(self.pairs):
                if (D >> a) & 1 and not (D >> b) & 1:
                    m |= 1 << i
            self.cuts.append(m)
        self.p2req = []
        for x in range(q):
            for y in range(x + 1, q):
                if le[x][y] or le[y][x]:
                    continue
                opts = []
                for w in range(q):
                    if le[w][x] and not le[x][w] and le[w][y] and not le[y][w]:
                        opts.append((1 << self.pidx[(w, x)]) | (1 << self.pidx[(w, y)]))
                    elif le[x][w] and not le[w][x] and le[y][w] and not le[w][y]:
                        opts.append((1 << self.pidx[(x, w)]) | (1 << self.pidx[(y, w)]))
                self.p2req.append(opts)

    def connects_cut(self, m):
        adj = [0] * self.q
        while m:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            a, b = self.pairs[i]
            adj[a] |= 1 << b
            adj[b] |= 1 << a
        reach = 1
        fr = 1
        while fr:
            nw = 0
            x = fr
            while x:
                low = x & -x
                j = low.bit_length() - 1
                x ^= low
                nw |= adj[j]
            nw &= ~reach
            if (nw >> self.v) & 1:
                return True
            reach |= nw
            fr = nw
        return False

    def yes(self, emask):
        for c in self.cuts:
            if self.connects_cut(emask & c):
                return True
        return False

    def p2_ok(self, emask):
        for opts in self.p2req:
            if not any((emask & o) == o for o in opts):
                return False
        return True


def maximal_no(O, stats):
    P = O.P
    full = (1 << P) - 1
    out = []
    if not O.yes(full):
        # every edge set is a no-instance; the unique maximal one is the full set
        return [full]

    def rec(i, I, U, X):
        stats["nodes"] = stats.get("nodes", 0) + 1
        top = I | U
        if not O.p2_ok(top):
            return
        # every excluded pair must still be able to create a yes-instance
        x = X
        while x:
            low = x & -x
            x ^= low
            if not O.yes(top | low):
                return
        if i == P:
            # maximality: every excluded pair creates a yes-instance with I
            x = X
            while x:
                low = x & -x
                x ^= low
                if not O.yes(I | low):
                    return
            out.append(I)
            return
        bit = 1 << i
        U2 = U & ~bit
        if not O.yes(I | bit):
            rec(i + 1, I | bit, U2, X)
        rec(i + 1, I, U2, X | bit)

    rec(0, 0, full, 0)
    return out


def main():
    Q = int(sys.argv[1])
    t0 = time.time()
    fout = open("%s/runs/enum-no-q%d.jsonl" % (HERE, Q), "w")
    tot = {}
    for m in range(0, Q - 1):
        extra = Q - 2 - m
        Ps = posets(m)
        for pi, Pz in enumerate(Ps):
            for (b, t, sizes) in size_assignments(m, Pz, extra):
                q, le = build_order(m, Pz, b, t, sizes)
                O = LOrder(q, le)
                tot["orders"] = tot.get("orders", 0) + 1
                st = {}
                mx = maximal_no(O, st)
                tot["bb_nodes"] = tot.get("bb_nodes", 0) + st.get("nodes", 0)
                auts = order_aut(q, le)
                perms = [[O.pidx[(a[x], a[y])] for (x, y) in O.pairs] for a in auts]
                for R in mx:
                    canon = True
                    for perm in perms:
                        R2 = 0
                        mm = R
                        while mm:
                            low = mm & -mm
                            j = low.bit_length() - 1
                            mm ^= low
                            R2 |= 1 << perm[j]
                        if R2 < R:
                            canon = False
                            break
                    if not canon:
                        continue
                    if not O.p2_ok(R):
                        tot["maxno_noP2"] = tot.get("maxno_noP2", 0) + 1
                        continue
                    tot["maxno_P2"] = tot.get("maxno_P2", 0) + 1
                    edges = [O.pairs[j] for j in range(O.P) if (R >> j) & 1]
                    z = make_zz(q, le, edges, 0, q - 1)
                    assert not zz.exact_dfs(z)[0]
                    if not edges or not zz.ac_answer(z):
                        tot["AC_refutes"] = tot.get("AC_refutes", 0) + 1
                        continue
                    tot["AC_fp"] = tot.get("AC_fp", 0) + 1
                    rec = {"q": q, "le": [[int(x) for x in r] for r in le], "R": edges, "AC": True}
                    if pcfast.pc_answer(z):
                        tot["PC_fp"] = tot.get("PC_fp", 0) + 1
                        rec["PC"] = True
                        rec["SPC"] = bool(variants.spc(z))
                        L = q if q % 2 else q - 1
                        rec["SPPC"] = any(variants.pc_simple(z, LL) for LL in range(1, L + 1, 2))
                    else:
                        tot["PC_refutes"] = tot.get("PC_refutes", 0) + 1
                        rec["PC"] = False
                    fout.write(json.dumps(rec) + "\n")
                    fout.flush()
        print("[%.0fs] q=%d m=%d done: %s" % (time.time() - t0, Q, m, tot), flush=True)
    print("FINAL q=%d [%.0fs] %s" % (Q, time.time() - t0, tot), flush=True)


if __name__ == "__main__":
    main()
