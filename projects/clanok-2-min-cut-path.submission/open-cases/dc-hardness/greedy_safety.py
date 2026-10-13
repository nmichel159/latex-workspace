"""Test of two greedy rules for 2CH+P2 (= SW+P2).  C = component of s using committed sets only.
T1: if exactly one set of an undecided switch x meets C and the instance is solvable (with the commitments),
    it stays solvable after committing x to that set.
T2: if both sets of x meet C, it stays solvable after committing x to either set.
Random greedy runs from the empty commitment; every rule application is checked by brute force.
Usage: python greedy_safety.py SEED COUNT"""
import sys
import random
from twoch import connected, p2_ok, random_p2_instance, fmt_inst


def comp_of(hyper, s):
    comp = 1 << s
    changed = True
    rest = [h for h in hyper if h]
    while changed:
        changed = False
        keep = []
        for h in rest:
            if h & comp:
                comp |= h
                changed = True
            else:
                keep.append(h)
        rest = keep
    return comp


def solvable(inst, assign):
    N, E, F, s, t = inst
    n = len(E)
    free = [i for i in range(n) if assign[i] is None]
    for mask in range(1 << len(free)):
        hyper = []
        for i in range(n):
            if assign[i] is None:
                continue
            hyper.append(F[i] if assign[i] else E[i])
        for j, i in enumerate(free):
            hyper.append(F[i] if (mask >> j) & 1 else E[i])
        if connected(N, hyper, s, t):
            return True
    return False


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"T1_ok": 0, "T1_bad": 0, "T2_ok": 0, "T2_bad": 0}
    ex = {}
    for it in range(count):
        inst = random_p2_instance(rng, rng.randint(4, 8), rng.randint(3, 9), rng.uniform(0.1, 0.35), rng.uniform(0.1, 0.35))
        N, E, F, s, t = inst
        n = len(E)
        if not solvable(inst, [None] * n):
            continue
        assign = [None] * n
        while True:
            committed = [F[i] if assign[i] else E[i] for i in range(n) if assign[i] is not None]
            C = comp_of(committed, s)
            if (C >> t) & 1:
                break
            cand = [i for i in range(n) if assign[i] is None and ((E[i] & C) or (F[i] & C))]
            if not cand:
                break
            i = rng.choice(cand)
            a, b = bool(E[i] & C), bool(F[i] & C)
            if a and b:
                ok = []
                for m in (0, 1):
                    assign[i] = m
                    ok.append(solvable(inst, assign))
                assign[i] = None
                if all(ok):
                    st["T2_ok"] += 1
                else:
                    st["T2_bad"] += 1
                    ex.setdefault("T2", (fmt_inst(inst), list(assign), i))
                m = rng.choice([m for m in (0, 1) if ok[m]]) if any(ok) else 0
                assign[i] = m
            else:
                m = 0 if a else 1
                assign[i] = m
                if solvable(inst, assign):
                    st["T1_ok"] += 1
                else:
                    st["T1_bad"] += 1
                    ex.setdefault("T1", (fmt_inst(inst), list(assign), i))
                    assign[i] = 1 - m
    print(st)
    for k, v in ex.items():
        print(k, v)


if __name__ == "__main__":
    main()
