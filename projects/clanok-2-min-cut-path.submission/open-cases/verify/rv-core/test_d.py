"""Proposition D of r5-core.md 2.2, checked with the reviewer's own code.

usage: python test_d.py basic KMAX          (i)-(iii) and solution structure for k = 2..KMAX, all four variants
       python test_d.py hyb K kd ks s B [refined] [variants]   HYB with these maximal parameters (all smaller
                                            parameter choices are included in the enumeration)
"""
import sys
import time
from fams import yfam
from sw import prune, hyb, bits

VARIANTS = [(c, bk) for c in (False, True) for bk in (False, True)]


def vname(c, bk):
    return ("Y'^d" if c else "Y^d") + ("/back" if bk else "")


def basic(KMAX):
    for k in range(2, KMAX + 1):
        for (c, bk) in VARIANTS:
            G = yfam(k, contact=c, d=True, back=bk)
            bad = G.p2_violations()
            sols = G.solutions()
            desc = []
            for D in sols:
                Fm = sorted(G.names[w] for w in bits(D))
                desc.append(",".join(Fm))
            # expected: x_q (q > k) in F, d either
            exp = set()
            base = ",".join(sorted(G.names[G.x[q]] for q in range(k + 1, 2 * k + 1)))
            exp.add(base)
            exp.add(",".join(sorted([G.names[G.x[q]] for q in range(k + 1, 2 * k + 1)] + ["d"])))
            fx = prune(G)
            fxs = sorted("%s:%s" % (G.names[w], mo) for w, mo in fx.items())
            # without d
            G0 = yfam(k, contact=c, d=False)
            fx0 = prune(G0)
            print("k=%d %-10s switches=%d nodes=%d P2-bad=%d solutions=%d expected=%s pruned=%s | without d: "
                  "solutions=%d pruned %d/%d" % (k, vname(c, bk), G.m, G.N, len(bad), len(sols),
                                                 set(desc) == exp, fxs, len(G0.solutions()), len(fx0), G0.m),
                  flush=True)


def run_hyb(k, kd, ks, s, B, refined, variants):
    for (c, bk) in variants:
        G = yfam(k, contact=c, d=True, back=bk)
        t0 = time.time()
        r = hyb(G, kd, ks, s, B, refined=refined, want=True)
        print("k=%d %-10s HYB%s(kd=%d, ks=%d, s=%d, B=%d): %s  [%.1fs]" % (
            k, vname(c, bk), "-refined" if refined else "", kd, ks, s, B,
            "ACCEPT" if r else "reject", time.time() - t0), flush=True)
        if r:
            print("   certificate/walk:", r[-1] if not isinstance(r, bool) else r)


if __name__ == "__main__":
    if sys.argv[1] == "basic":
        basic(int(sys.argv[2]))
    else:
        k, kd, ks, s, B = map(int, sys.argv[2:7])
        refined = len(sys.argv) > 7 and sys.argv[7] == "refined"
        var = VARIANTS
        if len(sys.argv) > 8:
            var = [VARIANTS[int(i)] for i in sys.argv[8].split(",")]
        run_hyb(k, kd, ks, s, B, refined, var)
