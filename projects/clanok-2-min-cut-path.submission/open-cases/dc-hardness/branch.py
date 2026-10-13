"""Branch-and-prune search for 2CH (contracted SW) and a hill climb for instances that make it branch a lot.

search(inst): DFS over switches; a node is pruned when s, t are disconnected in the relaxation (undecided switches
contribute both sets).  Branch variable: an undecided switch with a set meeting the current component of s in the
relaxation-free graph (committed sets only), preferring switches with exactly one such set.  Returns
(answer, number of search nodes).  Exact (it is a complete search).
Usage: python branch.py SEED STEPS NSW NNODE"""
import sys
import random
from twoch import connected, p2_ok, solve


def comp_of(N, hyper, s):
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


def search(inst, limit=10 ** 6):
    N, E, F, s, t = inst
    n = len(E)
    count = [0]

    def rec(assign):
        count[0] += 1
        if count[0] > limit:
            raise RuntimeError("limit")
        relax = []
        committed = []
        for i in range(n):
            if assign[i] is None:
                relax += [E[i], F[i]]
            else:
                h = F[i] if assign[i] else E[i]
                relax.append(h)
                committed.append(h)
        if not connected(N, relax, s, t):
            return False
        C = comp_of(N, committed, s)
        if (C >> t) & 1:
            return True
        # undecided switches touching C
        cand = []
        for i in range(n):
            if assign[i] is None:
                a = bool(E[i] & C)
                b = bool(F[i] & C)
                if a or b:
                    cand.append((0 if a != b else 1, i, a, b))
        if not cand:
            return False
        cand.sort()
        _, i, a, b = cand[0]
        order = []
        if a:
            order.append(0)
        if b:
            order.append(1)
        for m in order:
            assign[i] = m
            if rec(assign):
                assign[i] = None
                return True
            assign[i] = None
        # also: switch i not used at all from C now -> the other mode (it may matter elsewhere)
        other = [m for m in (0, 1) if m not in order]
        for m in other:
            assign[i] = m
            if rec(assign):
                assign[i] = None
                return True
            assign[i] = None
        return False

    ans = rec([None] * n)
    return ans, count[0]


def random_inst(rng, N, n, p):
    E = [sum(1 << x for x in range(N) if rng.random() < p) for _ in range(n)]
    F = [sum(1 << x for x in range(N) if rng.random() < p) for _ in range(n)]
    return [N, E, F, 0, 1]


def repair_p2(rng, inst):
    N, E, F, s, t = inst
    E = E[:]
    F = F[:]
    n = len(E)
    for i in range(n):
        for l in range(i + 1, n):
            if not ((E[i] & E[l]) or (F[i] & F[l])):
                # use an existing node if possible
                x = rng.randrange(N)
                if rng.random() < 0.5:
                    E[i] |= 1 << x
                    E[l] |= 1 << x
                else:
                    F[i] |= 1 << x
                    F[l] |= 1 << x
    return [N, E, F, s, t]


def mutate(rng, inst):
    N, E, F, s, t = inst
    E = E[:]
    F = F[:]
    n = len(E)
    for _ in range(rng.randint(1, 3)):
        i = rng.randrange(n)
        x = rng.randrange(N)
        if rng.random() < 0.5:
            E[i] ^= 1 << x
        else:
            F[i] ^= 1 << x
    return [N, E, F, s, t]


def main():
    seed, steps, nsw, nnode = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    cur = repair_p2(rng, random_inst(rng, nnode, nsw, 0.15))
    ans, cnt = search(cur)
    best = cnt
    print("start", ans, cnt, flush=True)
    for st in range(steps):
        cand = mutate(rng, cur)
        if not p2_ok(cand[1], cand[2]):
            cand = repair_p2(rng, cand)
        try:
            ans, cnt = search(cand)
        except RuntimeError:
            print("limit hit at step", st, cand, flush=True)
            continue
        if cnt >= best:
            cur = cand
            if cnt > best:
                print("step %d nodes %d answer %s" % (st, cnt, ans), flush=True)
            best = cnt
    print("best", best, cur)


if __name__ == "__main__":
    main()
