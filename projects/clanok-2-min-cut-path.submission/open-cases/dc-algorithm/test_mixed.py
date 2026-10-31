"""Checks of dc-algorithm.md Section 11 (Lemma S, Theorem F+, Theorem F_omega) on random ZZ + P2 instances.

Usage: python test_mixed.py SEED COUNT MODE [NMAX]
MODE: low | up | mixed | lowB | upT (direction of the P2 witnesses, see mixed.p2_complete_dir).
For every instance: exact answer (all down-sets, and zz.exact_dfs); the 2-guess on the low side and on the up side;
for every globally shortest consistent zigzag found (one BFS path per down-set of least distance): the number of
minimal peak classes (mp), of maximal valley classes (mv), the clique numbers of the lower-only graph U and the
upper-only graph Lg, and Lemma S (two incomparable minimal peaks at distance >= 4 have no witness below both; two
incomparable maximal valleys at distance >= 4 have no witness above both).
"""
import sys
import random
import json
import zz
import mixed as mx


def main():
    seed, count, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    rng = random.Random(seed)
    st = dict(instances=0, yes=0, mismatch_exact=0, low2_wrong=0, up2_wrong=0, lemmaS_fail=0, bound_fail=0,
              max_mp=0, max_mv=0, min_glow_gt2=0, min_gup_gt2=0, both_gt2=0)
    hist_glow = {}
    hist_gup = {}
    worst = []
    for it in range(count):
        z = mx.random_instance(rng, mode, nm=rng.randint(2, nmax))
        I = mx.Info(z)
        kinds = mx.witness_kinds(z, I)
        assert all(mx.has_lower(k) or mx.has_upper(k) for k in kinds.values())
        if mode in ('low', 'lowB'):
            assert all(mx.has_lower(k) for k in kinds.values())
        if mode in ('up', 'upT'):
            assert all(mx.has_upper(k) for k in kinds.values())
        sols = mx.solutions(z, I)
        ex = bool(sols)
        ex2 = zz.exact_dfs(z)[0]
        st["instances"] += 1
        st["yes"] += ex
        if ex != ex2:
            st["mismatch_exact"] += 1
            print("EXACT MISMATCH", it, flush=True)
        gl = mx.guess_low(z, 2, I) is not None
        gu = mx.guess_up(z, 2, I) is not None
        if gl and not ex or gu and not ex:
            print("UNSOUND", it, flush=True)
        if mode in ('low', 'lowB') and gl != ex:
            st["low2_wrong"] += 1
            print("LOW2 WRONG", it, json.dumps(mx.to_json(z)), flush=True)
        if mode in ('up', 'upT') and gu != ex:
            st["up2_wrong"] += 1
            print("UP2 WRONG", it, json.dumps(mx.to_json(z)), flush=True)
        if not ex:
            continue
        wU = mx.clique_number(z.n, mx.lower_only_graph(z, I, kinds))
        wL = mx.clique_number(z.n, mx.upper_only_graph(z, I, kinds))
        Lmin, short = mx.globally_shortest(z, I, sols)
        for D, p in short:
            mp, mins = mx.minimal_peak_classes(I, p)
            mv, maxs = mx.maximal_valley_classes(I, p)
            st["max_mp"] = max(st["max_mp"], mp)
            st["max_mv"] = max(st["max_mv"], mv)
            if mp > 2 * wU or mv > 2 * wL:
                st["bound_fail"] += 1
                print("BOUND FAIL", it, mp, wU, mv, wL, flush=True)
            if mode in ('low', 'lowB') and mp > 2 or mode in ('up', 'upT') and mv > 2:
                st["bound_fail"] += 1
                print("F+ BOUND FAIL", it, flush=True)
            pos = {x: i for i, x in enumerate(p)}
            for a in range(z.n):
                if not (mins >> a) & 1:
                    continue
                for b in range(a + 1, z.n):
                    if (mins >> b) & 1 and abs(pos[a] - pos[b]) >= 4 and I.incomparable(a, b):
                        if mx.has_lower(kinds[(a, b)]):
                            st["lemmaS_fail"] += 1
                            print("LEMMA S FAIL (peaks)", it, flush=True)
            for a in range(z.n):
                if not (maxs >> a) & 1:
                    continue
                for b in range(a + 1, z.n):
                    if (maxs >> b) & 1 and abs(pos[a] - pos[b]) >= 4 and I.incomparable(a, b):
                        if mx.has_upper(kinds[(a, b)]):
                            st["lemmaS_fail"] += 1
                            print("LEMMA S FAIL (valleys)", it, flush=True)
        glow = min(mx.g_low(I, D) for D, _ in sols)
        gup = min(mx.g_up(I, D) for D, _ in sols)
        hist_glow[glow] = hist_glow.get(glow, 0) + 1
        hist_gup[gup] = hist_gup.get(gup, 0) + 1
        st["min_glow_gt2"] += glow > 2
        st["min_gup_gt2"] += gup > 2
        if glow > 2 and gup > 2:
            st["both_gt2"] += 1
            worst.append((z.n, json.dumps(mx.to_json(z))))
        # consistency of the guess with the generator numbers
        if gl != (glow <= 2) or gu != (gup <= 2):
            print("GUESS/GEN MISMATCH", it, gl, glow, gu, gup, flush=True)
    print(seed, mode, st, "hist g_low", dict(sorted(hist_glow.items())), "hist g_up", dict(sorted(hist_gup.items())),
          flush=True)
    for n, js in sorted(worst)[:3]:
        print("BOTH>2", n, js, flush=True)


if __name__ == "__main__":
    main()
