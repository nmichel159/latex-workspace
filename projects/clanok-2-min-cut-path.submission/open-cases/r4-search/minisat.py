"""A small complete SAT solver (DPLL with unit propagation, clause learning omitted) for the CEGAR loops of
gadgets_b.py.  Literals: +v / -v for variables 1..n.  solve(n, clauses, assumptions) -> dict var -> bool or None.
Self-test: python minisat.py SEED COUNT (random 3-SAT against brute force)."""
import sys


def solve(n, clauses, fixed=None, prefer=None):
    """fixed: dict var -> bool (unit assumptions); prefer: dict var -> bool (branching polarity)."""
    assign = {}
    if fixed:
        assign.update(fixed)
    clauses = [list(c) for c in clauses]
    occ = {}
    for i, c in enumerate(clauses):
        for l in c:
            occ.setdefault(abs(l), []).append(i)
    trail = []

    def value(l):
        v = assign.get(abs(l))
        if v is None:
            return None
        return v if l > 0 else (not v)

    def propagate():
        changed = True
        while changed:
            changed = False
            for c in clauses:
                unassigned = None
                cnt = 0
                sat = False
                for l in c:
                    val = value(l)
                    if val is True:
                        sat = True
                        break
                    if val is None:
                        cnt += 1
                        unassigned = l
                if sat:
                    continue
                if cnt == 0:
                    return False
                if cnt == 1:
                    assign[abs(unassigned)] = unassigned > 0
                    trail.append(abs(unassigned))
                    changed = True
        return True

    sys.setrecursionlimit(100000)

    def rec():
        mark = len(trail)
        if not propagate():
            while len(trail) > mark:
                del assign[trail.pop()]
            return False
        # choose the most frequent unassigned variable in unsatisfied clauses
        score = {}
        for c in clauses:
            if any(value(l) is True for l in c):
                continue
            for l in c:
                if value(l) is None:
                    score[abs(l)] = score.get(abs(l), 0) + 1
        if not score:
            return True
        var = max(score, key=score.get)
        first = prefer.get(var, True) if prefer else True
        for val in (first, not first):
            assign[var] = val
            trail.append(var)
            if rec():
                return True
            # undo
            while len(trail) > mark:
                del assign[trail.pop()]
            # re-propagate the mark state
            if not propagate():
                while len(trail) > mark:
                    del assign[trail.pop()]
                return False
        while len(trail) > mark:
            del assign[trail.pop()]
        return False

    if rec():
        return {v: assign.get(v, prefer.get(v, True) if prefer else True) for v in range(1, n + 1)}
    return None


if __name__ == "__main__":
    import random
    import itertools
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    bad = 0
    for it in range(count):
        n = rng.randint(3, 10)
        m = rng.randint(1, 5 * n)
        cls = [[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(m)]
        r = solve(n, cls)
        bf = any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in cls)
                 for a in itertools.product([False, True], repeat=n))
        if (r is not None) != bf:
            bad += 1
        if r is not None and not all(any((l > 0) == r[abs(l)] for l in c) for c in cls):
            bad += 1
    print("random tests", count, "errors", bad)
