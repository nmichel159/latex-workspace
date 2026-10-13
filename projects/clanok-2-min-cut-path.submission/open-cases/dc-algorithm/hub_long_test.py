"""Hub family with long routes (hubimp.hubimp(..., long=True)): exact, P2, AC, PC (walk CSP), PC of the simple-path
CSP for every odd L, SPC.  Usage: python hub_long_test.py"""
import time
import zz
import pcfast
import hubimp
import variants

if __name__ == "__main__":
    for strict in (False, True):
        for m, mp in ((1, 2), (2, 2)):
            z, names = hubimp.hubimp(m, mp, strict=strict, long=True)
            t0 = time.time()
            ex = zz.exact_dfs(z)[0]
            ac = zz.ac_answer(z)
            pc = pcfast.pc_answer(z) if ac else False
            print("hub long (%d,%d,%s): n=%d |R|=%d P2=%s exact=%s AC=%s PC=%s %.0fs"
                  % (m, mp, "strict" if strict else "classes", z.n, len(z.R), not z.p2_bad(), ex, ac, pc,
                     time.time() - t0), flush=True)
            t0 = time.time()
            ys = [L for L in range(1, z.n + 1, 2) if variants.pc_simple(z, L)]
            print("   simple-path PC non-empty for L in", ys, "%.0fs" % (time.time() - t0), flush=True)
            if m * mp <= 4:
                t0 = time.time()
                print("   SPC", variants.spc(z), "%.0fs" % (time.time() - t0), flush=True)
