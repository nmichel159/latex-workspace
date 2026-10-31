"""Validation of the imported routines against exact solvers (task rule: check each imported routine on a few hundred
instances before relying on it).

Instances: random general ZZ + P2 (mixed.random_instance, modes low / up / mixed; gcert.random_inst with ties and
one-way comparabilities) and random 2CH + P2 (twoch.random_p2_instance), small enough for the enumeration of all
down-sets.  Checks per instance:
  exact: zz.exact (all down-sets) = zz.exact_dfs = gcert.exact = gcert.exact_downsets; for 2CH also brute force over
         mode vectors (swlib.exact_2ch) and the round trip zz_to_sw(sw_to_zz(.)) keeps the answer;
  guesses: portfolio.guess(K) finds a solution iff some solution down-set has g_low <= K or g_up <= K (definition,
         mixed.g_low / g_up over all solution down-sets) iff mixed.guess_low or mixed.guess_up finds one, K = 1, 2, 3;
  lattice2 / strict guess: sound; ladder.strict_guess 'yes' implies lattice2 'yes';
  GC (gcert.certificate, k = 2): sound (None on every no-instance); its walk re-checked;
  H1 (helly2ch.helly_solve): sound on 2CH instances;
  AC, PC (pcfast), PC (zz.pc_numpy), SPC, SPPC: never refute a yes-instance; pcfast = pc_numpy.
Usage: python validate.py SEED COUNT"""
import sys
import random
from common import zz, gcert, to_gc, sw_to_zz, zz_to_sw, check_walk, check_downset_solution
import mixed
import ladder
import pcfast
import variants
import twoch
import swlib
import helly2ch
from portfolio import Masks, guess, lattice2

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
stats = {}


def inc(k, d=1):
    stats[k] = stats.get(k, 0) + d


def gen():
    r = rng.random()
    if r < 0.35:
        mode = rng.choice(["low", "up", "mixed", "mixed"])
        z = mixed.random_instance(rng, mode, nm=rng.randint(2, 8))
        return "mixed-" + mode, z, None
    if r < 0.65:
        I = gcert.random_inst(rng, nm=rng.randint(2, 7))
        z = zz.ZZ(I.n, None, I.R, I.u, I.v, le=I.le)
        return "gcert", z, None
    while True:
        sw = twoch.random_p2_instance(rng, rng.randint(3, 5), rng.randint(2, 7), rng.uniform(0.1, 0.4),
                                      rng.uniform(0.1, 0.4))
        if sw[0] <= 9:
            break
    z, names = sw_to_zz(sw)
    return "2ch", z, sw


for it in range(count):
    kind, z, sw = gen()
    if z.n > 22:
        inc("skipped-large")
        continue
    inc("inst-" + kind)
    if z.p2_bad():
        inc("P2-violated(" + kind + ")")
    ex1 = zz.exact(z)[0]
    ex2 = zz.exact_dfs(z)[0]
    I = to_gc(z)
    ex3 = gcert.exact(I)
    ex4 = gcert.exact_downsets(I)
    if not (ex1 == ex2 == ex3 == ex4):
        inc("EXACT-DISAGREE")
        print("EXACT-DISAGREE", kind, ex1, ex2, ex3, ex4, flush=True)
        continue
    ex = ex1
    inc("yes" if ex else "no")
    if sw is not None:
        e2 = swlib.exact_2ch(sw) is not None
        if e2 != ex:
            inc("2CH-DISAGREE")
        r = zz_to_sw(z)
        if r is None:
            inc("ZZ2SW-NONE")
        else:
            sw2 = r[0]
            if (swlib.exact_2ch(sw2) is not None) != ex:
                inc("ROUNDTRIP-DISAGREE")
            if twoch.p2_ok(sw2[1], sw2[2]) != (not z.p2_bad()):
                inc("ROUNDTRIP-P2-DISAGREE")
        h = helly2ch.helly_solve(sw)
        if h and not ex:
            inc("H1-UNSOUND")
        inc("H1-yes" if h else "H1-no")
    M = Masks(z)
    sols = [D for D in zz.downsets(z) if zz.zigzag_in(z, D) is not None] if ex else []
    Inf = mixed.Info(z)
    for K in (1, 2, 3):
        g = guess(M, K)
        if g is not None and not check_downset_solution(z, g):
            inc("GUESS-UNSOUND")
        defn = any(mixed.g_low(Inf, D) <= K or mixed.g_up(Inf, D) <= K for D in sols)
        mx = (mixed.guess_low(z, K, Inf) is not None) or (mixed.guess_up(z, K, Inf) is not None)
        if (g is not None) != defn or defn != mx:
            inc("GUESS-MISMATCH-K%d" % K)
            print("GUESS-MISMATCH", K, g is not None, defn, mx, flush=True)
    lat = lattice2(M)
    if lat is not None and not check_downset_solution(z, lat):
        inc("LAT-UNSOUND")
    sg = ladder.strict_guess(z, Inf)
    if sg and lat is None:
        inc("STRICT-NOT-IN-LAT2")
    if sg and not ex:
        inc("STRICT-UNSOUND")
    c = gcert.certificate(I, 2)
    if c is not None:
        if not ex:
            inc("GC-UNSOUND")
        inc("GC2-yes")
    elif ex:
        inc("GC2-fail-on-yes")
    if c is not None and c[1] == "gen":
        masks = {"Gm": 0, "Pm": 0, "Gp": 0, "Pp": 0}
        for rname, x in c[2]:
            masks[rname] |= 1 << x
        w = gcert.general_search(I, masks["Gm"], masks["Pm"], masks["Gp"], masks["Pp"], 2, return_walk=True)
        if not check_walk(z, w):
            inc("GC-WALK-BAD")
    ac = zz.ac_answer(z)
    pc = pcfast.pc_answer(z) if ac else False
    pcn = zz.pc_numpy(z) if ac else False
    if pc != pcn:
        inc("PC-IMPL-DISAGREE")
    if ex and not (ac and pc):
        inc("AC/PC-UNSOUND")
    if not ex:
        inc("AC-fp" if ac else "AC-refutes")
        if ac:
            inc("PC-fp" if pc else "PC-refutes")
    if pc or (ex and z.n <= 14):
        s = variants.spc(z)
        if ex and not s:
            inc("SPC-UNSOUND")
        if not ex:
            inc("SPC-fp" if s else "SPC-refutes")
        L = z.n if z.n % 2 else z.n - 1
        sp = any(variants.pc_simple(z, LL) for LL in range(1, L + 1, 2))
        if ex and not sp:
            inc("SPPC-UNSOUND")
        if not ex:
            inc("SPPC-fp" if sp else "SPPC-refutes")
    if (it + 1) % 100 == 0:
        print(it + 1, dict(sorted(stats.items())), flush=True)
print("FINAL seed=%d count=%d" % (seed, count), dict(sorted(stats.items())), flush=True)
