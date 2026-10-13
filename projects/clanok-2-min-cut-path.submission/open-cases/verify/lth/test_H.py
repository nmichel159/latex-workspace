"""Theorem H of dc-hardness.md: own t-search vs brute force on general 2CH instances (agent verify-LTH).

Soundness (any instance, P2 or not): a yes of the t-search must be a yes of brute force, and its walk must be a
consistent certificate. Completeness (P2): if some solution has a shortest sequence of picked sides whose four group
partner families are each pierceable by t nodes, the t-search must say yes. On every yes-instance where the t-search
says no, need = min over solutions and shortest sequences of max over groups of the piercing number is computed and
must exceed t.
Families: rand (random sides + P2 repair), tree (subtrees of a random tree, Helly; checked), sparse (small sides),
nop2 (soundness only). Usage: python test_H.py <tag> <base seed> <instances per job> <jobs> <t> [procs]
"""
import sys
import random
import time
from multiprocessing import Pool

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *

FAMS = ["rand", "tree", "sparse", "nop2", "hardrand"]


def need_value(inst, sols):
    N = inst[0]
    best = None
    for modes in sols:
        for seq in shortest_sequences(inst, modes, limit=200):
            fam = group_partner_families(inst, seq)
            val = max(piercing_number(fam[g], N) for g in range(4))
            if best is None or val < best:
                best = val
                if best == 0:
                    return 0
    return best


def gen(fam, rng):
    if fam == "rand":
        N = rng.randint(4, 7); n = rng.randint(3, 8)
        return rand_2ch(rng, N, n, dens=rng.choice([0.2, 0.3, 0.45]), p_empty=0.1, p2=True)
    if fam == "sparse":
        N = rng.randint(5, 8); n = rng.randint(4, 9)
        return rand_2ch(rng, N, n, dens=0.15, p_empty=0.15, p2=True)
    if fam == "tree":
        N = rng.randint(4, 8); n = rng.randint(3, 8)
        inst, adj = rand_tree_2ch(rng, N, n, p_empty=0.1, maxsize=rng.choice([1, 2, 3]))
        return inst
    if fam == "nop2":
        N = rng.randint(4, 7); n = rng.randint(3, 8)
        return rand_2ch(rng, N, n, dens=rng.choice([0.2, 0.35]), p_empty=0.1, p2=False)
    if fam == "hardrand":
        N = rng.randint(5, 8); n = rng.randint(5, 9)
        best, bsc = None, -2
        for _ in range(25):
            inst = rand_2ch(rng, N, n, dens=rng.choice([0.15, 0.25]), p_empty=0.1, p2=True)
            if not relaxation_2ch(inst):
                continue
            ok, sols = brute_2ch(inst, all_solutions=True)
            sc = 100 if not ok else 50 - min(49, len(sols))
            if sc > bsc:
                best, bsc = inst, sc
        return best if best is not None else rand_2ch(rng, N, n, p2=True)
    raise ValueError(fam)


def job(args):
    fam, seed, count, tpar = args
    rng = random.Random(seed)
    st = {"n": 0, "p2": 0, "yes": 0, "no": 0, "helly": 0, "unsound": 0, "badcert": 0, "incomplete": 0,
          "miss_need_gt_t": 0, "relax_yes_no": 0}
    bad = []
    for _ in range(count):
        inst = gen(fam, rng)
        p2 = p2_2ch(inst)
        ok, sols = brute_2ch(inst, all_solutions=True)
        st["n"] += 1; st["p2"] += p2; st["yes" if ok else "no"] += 1
        if not ok and relaxation_2ch(inst):
            st["relax_yes_no"] += 1
        if fam == "tree":
            Es = [x[0] for x in inst[3]]; Fs = [x[1] for x in inst[3]]
            h = is_helly(Es) and is_helly(Fs)
            st["helly"] += h
            if not h:
                bad.append(("tree-not-helly", inst))
        H, wit = h_search(inst, tpar, want_witness=True)
        if H and wit is not None and not walk_is_consistent(inst, wit[1]):
            st["badcert"] += 1; bad.append(("badcert", inst, wit))
        if H and not ok:
            st["unsound"] += 1; bad.append(("unsound", inst, wit))
        if ok and not H and p2:
            nv = need_value(inst, sols)
            if nv is not None and nv <= tpar:
                st["incomplete"] += 1; bad.append(("incomplete", inst, nv))
            else:
                st["miss_need_gt_t"] += 1
    return fam, seed, st, bad


if __name__ == "__main__":
    tag, base, count, jobs, tpar = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    procs = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    tasks = [(FAMS[j % len(FAMS)], base + j, count, tpar) for j in range(jobs)]
    t0 = time.time()
    tot = {}
    out = open("results-H-%s.txt" % tag, "w")
    with Pool(min(procs, 8)) as pool:
        for fam, seed, st, bad in pool.imap_unordered(job, tasks):
            d = tot.setdefault(fam, {})
            for k, x in st.items():
                d[k] = d.get(k, 0) + x
            line = "%s seed %d t=%d: %s" % (fam, seed, tpar, st)
            print(line, flush=True)
            out.write(line + "\n")
            for b in bad:
                out.write("  BAD " + repr(b) + "\n")
                print("  BAD", b, flush=True)
            out.flush()
    out.write("\nTOTALS t=%d (%.0fs)\n" % (tpar, time.time() - t0))
    viol = 0
    for fam, d in sorted(tot.items()):
        out.write("%s: %s\n" % (fam, d))
        viol += d["unsound"] + d["badcert"] + d["incomplete"]
    out.write("violations: %d\n" % viol)
    out.close()
    print("violations:", viol, "time %.0fs" % (time.time() - t0))
