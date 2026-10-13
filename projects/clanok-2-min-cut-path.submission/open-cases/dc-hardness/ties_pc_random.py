"""AC / PC on random 2CHC + P2 no-instances (ties: members of one class forced into one mode, P2 only across
classes).  For every random instance: exact answer (brute force over class modes, cross-checked with the exact ZZ
search of the conversion), the member relaxation (classes ignored), AC, PC.  Counts by outcome; every PC false
positive is printed in full.
Usage: python ties_pc_random.py SEED COUNT [NMAX_MEMBERS]"""
import sys
import random
import time
import ties
import zz
import pcfast


def member_relaxed(inst):
    N, E, F, s, t, cls = inst
    from twoch import connected
    n = len(E)
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            return True
    return False


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 9
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "no": 0, "no_memberrelax_yes": 0, "ac_fp": 0, "pc_fp": 0, "mismatch": 0}
    t0 = time.time()
    for it in range(count):
        N = rng.randint(3, 7)
        n = rng.randint(3, nmax)
        k = rng.randint(2, min(n, 6))
        inst = ties.random_p2_instance(rng, N, n, k, rng.choice([0.15, 0.25, 0.35]), rng.choice([0.15, 0.25, 0.35]),
                                       fresh=rng.choice([0.3, 0.6, 0.9]))
        st["inst"] += 1
        b = ties.solve(inst) is not None
        z, _ = ties.to_zz(inst)
        e = zz.exact_dfs(z)[0]
        if b != e:
            st["mismatch"] += 1
            print("MISMATCH", ties.fmt(inst))
            continue
        if b:
            st["yes"] += 1
            continue
        st["no"] += 1
        if member_relaxed(inst):
            st["no_memberrelax_yes"] += 1
        ac = zz.ac_answer(z)
        if not ac:
            continue
        st["ac_fp"] += 1
        pc = pcfast.pc_answer(z)
        if pc:
            st["pc_fp"] += 1
            print("PC FALSE POSITIVE", ties.fmt(inst), flush=True)
    print(seed, st, "%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
