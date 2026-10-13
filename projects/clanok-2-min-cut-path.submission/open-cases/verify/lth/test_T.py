"""Theorem T (TIC with P2 is polynomial) and Theorem H with t = 1 on TIC: own algorithms vs brute force.

Usage: python test_T.py <tag> <base seed> <instances per job> <jobs> [procs]
Families (one per job, cycled): rand (random spans + P2 repair), pool (spans drawn from a small pool: repeated
spans, partner = own span), empty (many empty sides), zero (many spans of length 0), sat (P2-repaired encodings of
Theorem L(b)), rigidmut (mutated interval forms of R_L), nop2 (no P2: soundness only).
Every yes-answer of the algorithms is re-checked as a certificate; every disagreement is printed in full.
"""
import sys
import random
import time
from multiprocessing import Pool

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *
from families import rigid_tic
from satenc import rand_cnf, to_variant, encode_tic

FAMS = ["rand", "pool", "empty", "zero", "sat", "rigidmut", "nop2", "big", "hard"]


def gen(fam, rng):
    if fam == "rand":
        K = rng.randint(2, 9); n = rng.randint(2, 7)
        return K, rand_tic(rng, K, n, p_empty=0.1, p_zero=0.1, maxlen=rng.choice([1, 2, 3, K]))
    if fam == "pool":
        K = rng.randint(2, 8); n = rng.randint(3, 8)
        pool = [rand_span(rng, K, 0.1, rng.choice([1, 2, K])) for _ in range(rng.randint(2, 4))] + [None]
        sw = []
        for _ in range(n):
            E = rng.choice(pool)
            F = E if rng.random() < 0.25 else rng.choice(pool)
            if E is None and F is None:
                E = pool[0]
            sw.append((E, F))
        return K, repair_p2_tic(rng, K, sw)
    if fam == "empty":
        K = rng.randint(2, 9); n = rng.randint(2, 8)
        return K, rand_tic(rng, K, n, p_empty=0.4, p_zero=0.1, maxlen=rng.choice([1, 2, K]))
    if fam == "zero":
        K = rng.randint(2, 9); n = rng.randint(2, 8)
        return K, rand_tic(rng, K, n, p_empty=0.15, p_zero=0.45, maxlen=rng.choice([1, 2, K]))
    if fam == "sat":
        nv = rng.randint(1, 3); nc = rng.randint(1, 4)
        v2, c2 = to_variant(nv, rand_cnf(rng, nv, nc))
        K, sw, _ = encode_tic(v2, c2)
        if len(sw) > 11:
            return gen(fam, rng)
        return K, repair_p2_tic(rng, K, sw)
    if fam == "rigidmut":
        L = rng.randint(2, 7)
        K, sw = rigid_tic(L)
        sw = [list(x) for x in sw]
        for _ in range(rng.randint(1, 3)):
            w = rng.randrange(L); m = rng.randint(0, 1)
            sp = sw[w][m]
            if sp is None:
                continue
            op = rng.random()
            if op < 0.3:
                sw[w][m] = (sp[0], max(sp[0], sp[1] - 1))
            elif op < 0.6:
                sw[w][m] = (min(sp[1], sp[0] + 1), sp[1])
            elif op < 0.8:
                sw[w][m] = rand_span(rng, K)
            else:
                sw[w][m] = None
            if sw[w][0] is None and sw[w][1] is None:
                sw[w][m] = sp
        return K, repair_p2_tic(rng, K, [tuple(x) for x in sw])
    if fam == "nop2":
        K = rng.randint(2, 9); n = rng.randint(2, 7)
        return K, rand_tic(rng, K, n, p_empty=0.15, p_zero=0.1, maxlen=rng.choice([1, 2, K]), p2=False)
    if fam == "big":
        K = rng.randint(8, 14); n = rng.randint(7, 12)
        return K, rand_tic(rng, K, n, p_empty=0.1, p_zero=0.1, maxlen=rng.choice([1, 2, 3, 4]))
    if fam == "hard":
        return hill(rng)
    if fam == "chain":
        return chain_inst(rng)
    raise ValueError(fam)


def chain_inst(rng):
    """Planted minimal cover with r = 4..8 members (each group gets 2+ members), on distinct switches with random
    types; partners short and spread; P2 repaired only by extending partner spans or extra switches when possible."""
    r = rng.randint(4, 8)
    K = rng.randint(r + 1, 2 * r + 2)
    # left ends strictly increasing, right(I_a) < left(I_{a+2}), consecutive share a junction
    while True:
        cuts = sorted(rng.sample(range(1, K), r - 1))
        lefts = [0] + cuts
        ok = True
        spans = []
        for a in range(r):
            l = lefts[a]
            rr = K if a == r - 1 else lefts[a + 1] + rng.randint(0, 1)
            if a + 2 < r and rr >= lefts[a + 2]:
                rr = lefts[a + 2] - 1
            if rr < lefts[a + 1] if a + 1 < r else False:
                ok = False
            spans.append((l, rr))
        if ok and all(spans[a][1] >= spans[a + 1][0] for a in range(r - 1)) and \
                all(spans[a][1] < spans[a + 1][1] for a in range(r - 1)):
            break
    sw = []
    for a in range(r):
        part = None if rng.random() < 0.1 else rand_span(rng, K, 0.2, rng.choice([1, 2]))
        if rng.random() < 0.5:
            sw.append([spans[a], part])
        else:
            sw.append([part, spans[a]])
    for _ in range(rng.randint(0, 3)):
        sw.append([rand_span(rng, K, 0.2, 2), rand_span(rng, K, 0.2, 2)])
    rng.shuffle(sw)
    return K, repair_p2_tic(rng, K, [tuple(x) for x in sw])


def score(K, sw):
    """Prefer instances whose relaxation is yes and that have few solutions; no-instances score highest."""
    inst = tic_to_2ch(K, sw)
    if not relaxation_2ch(inst):
        return -1
    ok, sols = brute_tic(K, sw, all_solutions=True)
    if not ok:
        return 100
    return 50 - min(len(sols), 49)


def mutate(rng, K, sw):
    sw = [list(x) for x in sw]
    w = rng.randrange(len(sw)); m = rng.randint(0, 1)
    sp = sw[w][m]
    op = rng.random()
    if sp is None or op < 0.25:
        sw[w][m] = rand_span(rng, K, 0.1, rng.choice([1, 2, 3]))
    elif op < 0.5:
        sw[w][m] = (sp[0], max(sp[0], sp[1] - 1))
    elif op < 0.75:
        sw[w][m] = (min(sp[1], sp[0] + 1), sp[1])
    elif op < 0.85:
        sw[w][m] = None
    else:
        sw[w][m] = (max(0, sp[0] - 1), min(K, sp[1] + 1))
    if sw[w][0] is None and sw[w][1] is None:
        sw[w][m] = sp if sp is not None else (0, 0)
    return repair_p2_tic(rng, K, [tuple(x) for x in sw])


def hill(rng):
    K = rng.randint(6, 12); n = rng.randint(6, 10)
    sw = rand_tic(rng, K, n, p_empty=0.1, p_zero=0.05, maxlen=rng.choice([1, 2, 3]))
    best = score(K, sw)
    for _ in range(60):
        cand = mutate(rng, K, sw)
        sc = score(K, cand)
        if sc >= best:
            sw, best = cand, sc
    return K, sw


def check_chain(K, sw, chain):
    """chain = tuple of span ids; distinct switches, covers the line."""
    sws = [i >> 1 for i in chain]
    if len(set(sws)) != len(sws):
        return False
    spans = [sw[i >> 1][i & 1] for i in chain]
    if spans[0][0] != 0 or spans[-1][1] != K:
        return False
    return all(spans[a][1] >= spans[a + 1][0] for a in range(len(spans) - 1))


def job(args):
    fam, seed, count = args
    rng = random.Random(seed)
    st = {"n": 0, "yes": 0, "no": 0, "relax_yes_no": 0, "T_bad": 0, "H_bad": 0, "Tfull_bad": 0,
          "Tfull_runs": 0, "p2": 0, "bad_cert": 0}
    bad = []
    for it in range(count):
        K, sw = gen(fam, rng)
        p2 = p2_tic(sw)
        st["n"] += 1
        st["p2"] += p2
        ans, _ = brute_tic(K, sw)
        inst = tic_to_2ch(K, sw)
        assert ans == brute_2ch(inst)[0], ("TIC/2CH mismatch", K, sw)
        st["yes" if ans else "no"] += 1
        if not ans and relaxation_2ch(inst):
            st["relax_yes_no"] += 1
        T, wit = tic_T(K, sw, want_witness=True)
        if T and wit is not None and not check_chain(K, sw, wit[1]):
            st["bad_cert"] += 1
            bad.append(("badcert-T", K, sw, wit))
        if T and not ans:
            st["T_bad"] += 1
            bad.append(("T-unsound", K, sw, wit))
        if p2 and ans and not T:
            st["T_bad"] += 1
            bad.append(("T-incomplete", K, sw))
        if not p2 and ans and not T:
            st["noP2_T_miss"] = st.get("noP2_T_miss", 0) + 1
        if K <= 6 and it % 4 == 0:
            st["Tfull_runs"] += 1
            Tf = tic_T(K, sw, full_guesses=True)
            if Tf != T:
                st["Tfull_bad"] += 1
                bad.append(("T-full-differs", K, sw, T, Tf))
        H, hw = h_search(inst, 1, want_witness=True)
        if H and hw is not None and not walk_is_consistent(inst, hw[1]):
            st["bad_cert"] += 1
            bad.append(("badcert-H", K, sw, hw))
        if H and not ans:
            st["H_bad"] += 1
            bad.append(("H-unsound", K, sw, hw))
        if p2 and ans and not H:
            st["H_bad"] += 1
            bad.append(("H-incomplete", K, sw))
    return fam, seed, st, bad


if __name__ == "__main__":
    tag, base, count, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    fams = sys.argv[6].split(",") if len(sys.argv) > 6 else FAMS
    tasks = [(fams[j % len(fams)], base + j, count) for j in range(jobs)]
    t0 = time.time()
    tot = {}
    out = open("results-T-%s.txt" % tag, "w")
    with Pool(min(procs, 8)) as pool:
        for fam, seed, st, bad in pool.imap_unordered(job, tasks):
            d = tot.setdefault(fam, {})
            for k, x in st.items():
                d[k] = d.get(k, 0) + x
            line = "%s seed %d: %s" % (fam, seed, st)
            print(line, flush=True)
            out.write(line + "\n")
            for b in bad:
                out.write("  BAD " + repr(b) + "\n")
                print("  BAD", b, flush=True)
            out.flush()
    out.write("\nTOTALS (%.0fs)\n" % (time.time() - t0))
    viol = 0
    for fam, d in sorted(tot.items()):
        out.write("%s: %s\n" % (fam, d))
        viol += d["T_bad"] + d["H_bad"] + d["Tfull_bad"] + d["bad_cert"]
    out.write("violations: %d\n" % viol)
    out.close()
    print("violations:", viol, "time %.0fs" % (time.time() - t0))
