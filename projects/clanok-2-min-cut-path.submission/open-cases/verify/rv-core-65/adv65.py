"""Adversarial search against r5-core.md Section 6 (reviewer rv-core-65, own code: gsf, thy, planted).

Hill climbing with restarts over general switch form instances (P2 kept by repair after every mutation, yes-instances
only).  Every evaluated instance is checked exactly as in test_lemmas / test_thm65 on all its shortest valid paths
(cap); any failure is printed and the instance saved as JSON.  The climb maximises one target:
  span   : largest span max-min of the positions of S_x = A & NE(E#x) (x not in L) or its dual
           (Lemma 6.3 claims <= 8; the reviewer's sharper bound is <= 4)
  tools  : largest min(kE, kF) over shortest paths and minimum covers of the bad pairs
           (Theorem 6.5 claims <= k = floor(log2 m) + 1)
  phi    : largest |Phi| / |T| over the descriptions built from minimal covers (claimed <= 9; sharper <= 5)
  kappa  : largest kappa_min (least bad-pair vertex cover over the shortest paths), with GDESC(k, kappa_min, 9k)
           run exhaustively when m <= GD
  lp     : largest min(tau_E*, tau_F*) - kappa (Corollary 6.5' claims <= 2)

usage: python adv65.py TARGET SEED RESTARTS STEPS MMIN MMAX [GD] [OUTDIR]
"""
import sys
import os
import json
import math
import time
import random
import itertools
from collections import Counter
from fractions import Fraction
from gsf import Inst, bits, popcount, closure
from planted import planted_inst
from gsf import random_inst
from thy import (Stars, Skel, cov_E, cov_F, bad_pairs, min_vertex_cover, thm_desc_E, thm_desc_F, frac_cover,
                 min_cover, all_covers, gdesc)
import test_lemmas
import test_thm65


# ---- mutable representation ------------------------------------------------------------------------------------
class Raw:
    """Generating relations `base` (pairs a <= b), sides as node masks without private nodes, middle edges."""

    def __init__(self, m, N, s, t, base, E, F, medges):
        self.m, self.N, self.s, self.t = m, N, s, t
        self.base = set(base)
        self.E, self.F = list(E), list(F)
        self.med = set(medges)

    @staticmethod
    def from_inst(I):
        priv = I.private
        base = set()
        for a in range(I.m):
            for b in range(I.m):
                if a != b and I.le[a][b]:
                    base.add((a, b))
        E = [e & ~priv for e in I.E]
        F = [f & ~priv for f in I.F]
        return Raw(I.m, I.N, I.s, I.t, base, E, F, set(I.medges.keys()))

    def le(self):
        m = self.m
        le = [[a == b for b in range(m)] for a in range(m)]
        for a, b in self.base:
            le[a][b] = True
        for z, v in self.med:
            le[z][v] = True
        return closure(le)

    def build(self, name="adv"):
        le = self.le()
        for z, v in self.med:
            if le[v][z]:
                return None              # middle edge no longer strict
        # compact the regular nodes, then add private nodes
        used = 1 << self.s | 1 << self.t
        for x in self.E + self.F:
            used |= x
        idx = {}
        for nd in bits(used):
            idx[nd] = len(idx)

        def remap(x):
            r = 0
            for nd in bits(x):
                r |= 1 << idx[nd]
            return r
        E = [remap(x) for x in self.E]
        F = [remap(x) for x in self.F]
        N = len(idx)
        medges = {}
        for z, v in sorted(self.med):
            medges[(z, v)] = N
            F[z] |= 1 << N
            E[v] |= 1 << N
            N += 1
        I = Inst(N, idx[self.s], idx[self.t], le, E, F, medges, name)
        return I

    def copy(self):
        return Raw(self.m, self.N, self.s, self.t, set(self.base), list(self.E), list(self.F), set(self.med))

    def fresh(self):
        self.N += 1
        return self.N - 1


def repair_p2(R, rng):
    """Add witnesses until P2 holds (fresh common nodes or middle witnesses)."""
    I = R.build()
    if I is None:
        return None
    m = R.m
    for x in range(m):
        for y in range(x + 1, m):
            if I.comparable(x, y) or I.p2_witness(x, y) is not None:
                continue
            opts = ["E", "F"]
            lows = [z for z in range(m) if I.lt(z, x) and I.lt(z, y)]
            ups = [z for z in range(m) if I.lt(x, z) and I.lt(y, z)]
            if lows:
                opts.append("low")
            if ups:
                opts.append("up")
            o = rng.choice(opts)
            if o == "E":
                nd = R.fresh()
                R.E[x] |= 1 << nd
                R.E[y] |= 1 << nd
            elif o == "F":
                nd = R.fresh()
                R.F[x] |= 1 << nd
                R.F[y] |= 1 << nd
            elif o == "low":
                z = rng.choice(lows)
                R.med.add((z, x))
                R.med.add((z, y))
            else:
                z = rng.choice(ups)
                R.med.add((x, z))
                R.med.add((y, z))
            I = R.build()
    return I


def mutate(R, rng):
    R = R.copy()
    m = R.m
    op = rng.choice(["side", "side", "side", "fresh2", "rel", "rel", "unrel", "med", "unmed"])
    if op == "side":
        w = rng.randrange(m)
        nd = rng.randrange(R.N)
        if rng.random() < 0.5:
            R.E[w] ^= 1 << nd
        else:
            R.F[w] ^= 1 << nd
    elif op == "fresh2":
        a, b = rng.sample(range(m), 2)
        nd = R.fresh()
        (R.E if rng.random() < 0.5 else R.F)[a] |= 1 << nd
        (R.E if rng.random() < 0.5 else R.F)[b] |= 1 << nd
    elif op == "rel":
        le = R.le()
        a, b = rng.sample(range(m), 2)
        if not le[b][a]:
            R.base.add((a, b))
    elif op == "unrel":
        if R.base:
            R.base.discard(rng.choice(sorted(R.base)))
    elif op == "med":
        le = R.le()
        a, b = rng.sample(range(m), 2)
        if le[a][b] and not le[b][a]:
            R.med.add((a, b))
    elif op == "unmed":
        if R.med:
            R.med.discard(rng.choice(sorted(R.med)))
    return R


# ---- evaluation ------------------------------------------------------------------------------------------------
FAILKEYS = {
    "(E') FAILS", "(E') PICKS BUT DOES NOT CONNECT", "(E') |Phi| > 9|T|", "(F') FAILS",
    "(F') PICKS BUT DOES NOT CONNECT", "(F') |Phi| > 9|T|", "CASE lambda<1/2: NO COVER BY k F-TOOLS",
    "CASE lambda>=1/2: NO COVER BY k E-TOOLS", "COR 6.5' DESCRIPTION FAILS", "COR 6.5' FLIPS > 9 PER STAR",
    "COR 6.5' ROUNDING BOUND FAILS", "COR 6.5': ITEMS NOT COVERABLE BY CHEAP TOOLS",
    "COR 6.5': min LP cover > 2 + kappa", "DUALITY (STRICT ANCHORS) FAILS", "DUALITY FAILS ON R x C",
    "E-DESCRIPTION NOT A DOWN-SET", "EMPTY CASE (E) FAILS", "EMPTY CASE (F) FAILS", "F-DESCRIPTION NOT A DOWN-SET",
    "FACT (a) FAILS", "FACT (b) FAILS", "FACT (c) FAILS (outside Up, L)", "FACT (c) FAILS (shape)",
    "GDESC ACCEPTS A NO-INSTANCE", "GDESC(k, kappa_min, 9k) REJECTS A YES-INSTANCE", "LEMMA 6.2 FAILS",
    "LEMMA 6.3 DUAL FAILS", "LEMMA 6.3 FAILS", "LEMMA 6.4 FAILS", "LEMMA W (no middle edges) FAILS",
    "LITERAL (E) OR (F) FAILS", "MINIMAX STEP FAILS (tau_F >= 2 although lambda < 1/2)", "NEITHER SIDE COVERABLE",
    "PAIR WITH x <= y", "PICK CRITERION FAILS", "REMARK NE(E#) IDENTITY FAILS", "STRICT ANCHOR MEETS L OR B",
    "STRICT ANCHOR MEETS Up OR A", "P2 LOST (bug)",
    # reviewer's sharper claims (not claims of the reviewed text)
    "REVIEWER: SPAN > 4", "REVIEWER: |Phi| > 5|T|",
}


def nfail(st):
    return sum(st[k] for k in FAILKEYS if k in st)


def evaluate(I, target, gd, rng, st):
    """Run all checks on every shortest valid path (cap 20); return the score for `target` (None for no-instances)."""
    if I.s == I.t:
        return None
    if not I.p2():
        st["P2 LOST (bug)"] += 1
        return None
    r, paths = I.shortest_paths(cap=20)
    if r is None:
        return None
    m = I.m
    k = int(math.floor(math.log2(m))) + 1
    St = Stars(I)
    fails0 = nfail(st)
    best = Fraction(-1)
    kmin = None
    for P in paths:
        test_lemmas.check_path(I, St, P, st, 2)
        K = Skel(I, P)
        bp = bad_pairs(I, K)
        kap, covers = min_vertex_cover(bp)
        kmin = kap if kmin is None else min(kmin, kap)
        for x in range(m):
            for S in ((St.NEstar[x] & K.A) if not (K.L >> x) & 1 else 0,
                      (St.NFstar[x] & K.B) if not (K.Up >> x) & 1 else 0):
                if S:
                    ps = [K.pos[a] for a in bits(S)]
                    sp = max(ps) - min(ps)
                    st["max span (6.3)"] = max(st["max span (6.3)"], sp)
                    if sp > 4:
                        st["REVIEWER: SPAN > 4"] += 1
                    if target == "span":
                        best = max(best, Fraction(sp) + Fraction(popcount(S), 100))
        for X0, Y0 in covers[:4]:
            test_thm65.check_cover(I, St, K, set(X0), set(Y0), k, st, rng)
            if target in ("tools", "phi"):
                R_ = [x for x in bits(K.NFi) if x not in X0]
                C_ = [y for y in bits(K.NEi) if y not in Y0]
                if R_ and C_:
                    rows = [set(bits(cov_E(I, St, K, x))) & set(C_) for x in R_]
                    cols = [set(bits(cov_F(I, St, K, y))) & set(R_) for y in C_]
                    kE, _ = min_cover(rows, C_, min(len(R_), k + 1))
                    kF, _ = min_cover(cols, R_, min(len(C_), k + 1))
                    vals = [v for v in (kE, kF) if v is not None]
                    mk = min(vals) if vals else k + 2
                    if target == "tools":
                        best = max(best, Fraction(mk) + Fraction(kap, 10))
                    else:
                        for comb in all_covers(rows, C_, min(len(R_), k), cap=20):
                            T = [R_[i] for i in comb]
                            D, U, Phi = thm_desc_E(I, St, K, T, sorted(Y0))
                            best = max(best, Fraction(popcount(Phi), len(T)))
                            if popcount(Phi) > 5 * len(T):
                                st["REVIEWER: |Phi| > 5|T|"] += 1
                        for comb in all_covers(cols, R_, min(len(C_), k), cap=20):
                            T = [C_[i] for i in comb]
                            D, U, Phi = thm_desc_F(I, St, K, T, sorted(X0))
                            best = max(best, Fraction(popcount(Phi), len(T)))
                            if popcount(Phi) > 5 * len(T):
                                st["REVIEWER: |Phi| > 5|T|"] += 1
        test_thm65.check_cor65(I, St, K, kap, st)
        if target == "lp":
            taus = []
            for kind in (0, 1):
                items = bits(K.NEi if kind == 0 else K.NFi)
                tools = test_thm65.cheap_tools(I, St, K, kind)
                taus.append(frac_cover([set(bits(c)) for _, c, _ in tools], items) if items else Fraction(0))
            if None not in taus:
                best = max(best, min(taus) - kap)
    if target == "kappa":
        best = Fraction(kmin) + Fraction(len(paths), 1000)
        if m <= gd:
            st["GDESC runs"] += 1
            if not gdesc(I, St, k, kmin, 9 * k):
                st["GDESC(k, kappa_min, 9k) REJECTS A YES-INSTANCE"] += 1
    st["max kappa_min"] = max(st["max kappa_min"], kmin)
    if nfail(st) > fails0:
        return "FAIL"
    return best


def start(rng, mmin, mmax):
    while True:
        m = rng.randint(mmin, mmax)
        if rng.random() < 0.6:
            r = rng.randint(3, max(3, m - 3))
            rest = m - r
            nu = rng.randint(1, max(1, rest // 2))
            nd = rest - nu
            I = planted_inst(rng, r=r, n_up=nu, n_down=nd, n_free=0, p_rel=0.4, p_bad=rng.choice([0.6, 1.0]),
                             p_tie=0.05, p_side=0.12, p_contact=0.2, p_med=rng.choice([0.2, 0.5]))
        else:
            I = random_inst(rng, m, p_order=rng.choice([0.3, 0.5]), p_side=0.15, p_med=rng.choice([0.2, 0.5]))
        if I.p2() and I.s != I.t and I.shortest_paths(cap=1)[0]:
            return I


def main():
    target = sys.argv[1]
    seed, restarts, steps, mmin, mmax = (int(a) for a in sys.argv[2:7])
    gd = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    outdir = sys.argv[8] if len(sys.argv) > 8 else os.path.join("runs", "adv")
    os.makedirs(outdir, exist_ok=True)
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    overall = Fraction(-1)
    for rs in range(restarts):
        I = start(rng, mmin, mmax)
        R = Raw.from_inst(I)
        I = R.build()
        sc = evaluate(I, target, gd, rng, st)
        st["evaluations"] += 1
        if sc == "FAIL":
            fn = os.path.join(outdir, "fail-%s-%d-%d-start.json" % (target, seed, rs))
            json.dump(I.to_json(), open(fn, "w"))
            print("FAILURE at start, saved", fn, dict(st), flush=True)
            continue
        for stp in range(steps):
            R2 = mutate(R, rng)
            I2 = repair_p2(R2, rng)
            if I2 is None or I2.m != R.m:
                continue
            sc2 = evaluate(I2, target, gd, rng, st)
            st["evaluations"] += 1
            if sc2 == "FAIL":
                fn = os.path.join(outdir, "fail-%s-%d-%d-%d.json" % (target, seed, rs, stp))
                json.dump(I2.to_json(), open(fn, "w"))
                print("FAILURE saved", fn, flush=True)
                for key in sorted(st):
                    if key in FAILKEYS:
                        print("   ", key, st[key], flush=True)
                break
            if sc2 is None:
                continue
            if sc2 >= sc:
                if sc2 > sc:
                    st["improvements"] += 1
                R, sc, I = R2, sc2, I2
                if sc > overall:
                    overall = sc
                    fn = os.path.join(outdir, "best-%s-%d.json" % (target, seed))
                    d = I.to_json()
                    d["score"] = str(sc)
                    json.dump(d, open(fn, "w"))
        print("  restart %d (%.0fs): score %s (m %d), overall %s; %s" % (rs, time.time() - t0, sc, I.m, overall,
              {kk: v for kk, v in st.items() if kk in FAILKEYS or "max" in kk or kk == "evaluations"}), flush=True)
    print("adv65 target %s seed %d restarts %d steps %d m %d-%d gd %d (%.0fs): best %s"
          % (target, seed, restarts, steps, mmin, mmax, gd, time.time() - t0, overall))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
