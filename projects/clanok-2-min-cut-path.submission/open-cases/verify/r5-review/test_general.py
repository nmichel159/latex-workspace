"""Checks of r4-general.md §5.1 (conversion, valid walks, Theorem 5'), §7.3 (forced-exit propagation, pruning, HYB
soundness) and §8 (Theorem R (a), (b), Corollary R') with own code (gswlib.py, zzlib.py).

Usage: python test_general.py MODE SEED COUNT
  MODE zz : random ZZ + P2 instances (ties, one-way relations, middle edges, middle witnesses), 4-11 middle elements
  MODE zzs: the same with sparse orders and many ties (more instances satisfy the hypothesis of Theorem R)
  MODE abs: random abstract switch forms (any hypergraph, any preorder on the switches, no P2), 3-9 switches
"""
import random
import sys
import time
from gswlib import SW, from_zz, random_zz_p2, random_abstract


def free_incomparable(G, fixed):
    free = [w for w in range(G.m) if w not in fixed]
    return all(not G.le[a][b] and not G.le[b][a] for i, a in enumerate(free) for b in free[i + 1:])


def check_R(G, fixed, yes, p2, stats, tag):
    """Theorem R (a), (b) for one fixing (assumed sound and closed); returns None if the hypothesis fails."""
    check_R_classes(G, fixed, yes, p2, stats, tag)
    if not free_incomparable(G, fixed):
        stats[tag + "_hyp_fail"] += 1
        return
    stats[tag + "_hyp"] += 1
    H, free = G.contract(fixed)
    yes2 = bool(H.solutions())
    if yes2 != yes:
        stats[tag + "_R_mismatch"] += 1
        print("THEOREM R MISMATCH", tag, yes, yes2, fixed)
    if p2:
        bad = H.p2_switch()
        if bad:
            stats[tag + "_P2_fail"] += 1
            print("P2 FAILS IN I*", tag, bad[:3])


def check_R_classes(G, fixed, yes, p2, stats, tag):
    """r4-general.md §9.1: only ties (no strict relations) among the free switches; the contraction is an instance
    of 2CH with classes (+ P2 between switches of different classes)."""
    free = [w for w in range(G.m) if w not in fixed]
    strict = any((G.le[a][b]) != (G.le[b][a]) for i, a in enumerate(free) for b in free[i + 1:])
    ties = any(G.le[a][b] and G.le[b][a] for i, a in enumerate(free) for b in free[i + 1:])
    if strict or not ties:
        return
    stats[tag + "_cls_hyp"] += 1
    H, fr = G.contract(fixed)
    if bool(H.solutions()) != yes:
        stats[tag + "_cls_mismatch"] += 1
        print("CLASSES VERSION MISMATCH", tag)
    if p2:
        for a in range(H.m):
            for b in range(a + 1, H.m):
                if not H.le[a][b] and not (H.E[a] & H.E[b]) and not (H.F[a] & H.F[b]):
                    stats[tag + "_cls_P2_fail"] += 1
                    print("CLASSES P2 FAIL", tag)


def main():
    mode, seed, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    from collections import Counter
    stats = Counter()
    t0 = time.time()
    done = 0
    while done < count:
        if mode in ("zz", "zzs"):
            nmid = rng.randint(4, 11)
            po = rng.choice((0.1, 0.25, 0.4)) if mode == "zz" else rng.choice((0.03, 0.08, 0.15))
            pt = rng.choice((0.0, 0.2, 0.5)) if mode == "zz" else rng.choice((0.3, 0.6))
            I = random_zz_p2(rng, nmid, rng.randint(0, 3), rng.randint(0, 3), po, pt,
                             rng.choice((0.15, 0.3, 0.5)))
            if I is None:
                continue
            assert not I.check() and not I.p2_failures()
            G = from_zz(I)
            p2 = True
        else:
            G = random_abstract(rng, rng.randint(3, 7), rng.randint(3, 9), rng.choice((0.2, 0.35, 0.5)),
                                rng.choice((0.1, 0.3, 0.5)), rng.choice((0.0, 0.3)))
            p2 = False
            I = None
        done += 1
        sols = G.solutions()
        yes = bool(sols)
        stats["yes" if yes else "no"] += 1
        # conversion (§5.1)
        if I is not None:
            zb = I.zz_brute()
            zs = I.zz_search()
            if not (zb == zs == yes):
                stats["conv_mismatch"] += 1
                print("CONVERSION MISMATCH", zb, zs, yes)
        # valid walks exist iff yes: exhaustive search with K = all sides, no declarations
        w = G.search5(G.sides, 10 ** 9, 0)
        if (w is not None) != yes:
            stats["validwalk_mismatch"] += 1
            print("VALID WALK MISMATCH")
        if w is not None:
            assert G.is_valid_walk(w)
            mv = G.walk_to_modes(w)
            assert G.is_downset_modes(mv) and G.connects(mv)
        # propagation and pruning (§7.3)
        fixed, status = G.prune()
        if status == "no":
            stats["prune_no"] += 1
            if yes:
                stats["prune_unsound"] += 1
                print("PRUNE SAYS NO ON A YES-INSTANCE")
        else:
            for sol in sols:
                for z, mo in fixed.items():
                    if sol[z] != mo:
                        stats["prune_unsound"] += 1
                        print("PRUNE FIXED A MODE THAT A SOLUTION VIOLATES", z, mo)
                        break
            stats["fixed_total"] += len(fixed)
            stats["switch_total"] += G.m
            if yes and len(fixed) == G.m:
                stats["rigid"] += 1
            check_R(G, fixed, yes, p2, stats, "own")
        # maximal sound fixing and random closed sub-fixings of it
        if yes:
            fmax = {z: sols[0][z] for z in range(G.m) if all(s[z] == sols[0][z] for s in sols)}
            assert G.closure(fmax) == fmax, "intersection of solutions not closed"
            check_R(G, fmax, yes, p2, stats, "max")
            for _ in range(3):
                sub = {z: mo for z, mo in fmax.items() if rng.random() < 0.5}
                sub = G.closure(sub)
                check_R(G, sub, yes, p2, stats, "sub")
        else:
            # on a no-instance every closed partial vector is (vacuously) sound
            for _ in range(3):
                part = {z: rng.randint(0, 1) for z in range(G.m) if rng.random() < 0.6}
                part = G.closure(part)
                if part is None:
                    continue
                check_R(G, part, yes, p2, stats, "noinst")
        # Theorem 5': random certificate sets K, bounds B, s
        for _ in range(6):
            K = [Y for Y in G.sides if rng.random() < rng.choice((0.2, 0.5, 0.8))]
            B = rng.randint(0, 6)
            s = rng.randint(0, 3)
            w = G.search5(K, B, s)
            stats["t5_runs"] += 1
            if w is not None:
                stats["t5_accept"] += 1
                if not G.is_valid_walk(w) or not yes:
                    stats["t5_unsound"] += 1
                    print("THEOREM 5' UNSOUND", K, B, s, w)
        # exhaustive rule walks (no state merging) on small instances
        if len(G.sides) <= 10:
            K = [Y for Y in G.sides if rng.random() < 0.5]
            B = rng.randint(0, 4)
            s = rng.randint(0, 2)
            for wk in G.all_rule_walks(K, B, s, 7):
                stats["t5_walks"] += 1
                if not G.is_valid_walk(wk):
                    stats["t5_unsound_walk"] += 1
                    print("RULE WALK NOT VALID", K, B, s, wk)
        # HYB soundness: prune, delete dead sides, search (here with the side set restricted)
        if status != "no":
            dead = {2 * z + (1 - mo) for z, mo in fixed.items()}
            H = SW(G.N, [0 if 2 * z in dead else G.E[z] for z in range(G.m)],
                   [0 if 2 * z + 1 in dead else G.F[z] for z in range(G.m)], G.le, G.s, G.t)
            for _ in range(3):
                K = [Y for Y in H.sides if rng.random() < 0.5]
                w = H.search5(K, rng.randint(1, 4), rng.randint(0, 2))
                if w is not None:
                    stats["hyb_accept"] += 1
                    if not yes or not G.is_valid_walk(w):
                        stats["hyb_unsound"] += 1
                        print("HYB UNSOUND")
            # completeness of the pruned instance: same answer (pruning removes no side used by a solution)
            if bool(H.solutions()) != yes:
                stats["pruned_answer_changed"] += 1
                print("PRUNED INSTANCE CHANGED ANSWER")
    print("mode %s seed %d count %d (%.0fs):" % (mode, seed, count, time.time() - t0), dict(sorted(stats.items())))


if __name__ == "__main__":
    main()
