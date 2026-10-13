"""Certificate that the K4 encoding with classes (k4c.py) has no P2 completion: a small set S of P2-violating member
pairs such that EVERY choice of a connector type for the pairs of S (a private node in the two E-sides or in the two
F-sides; reusing nodes only adds connectivity) turns the base instance into a yes-instance.  By monotonicity no
completion of the whole instance keeps the answer 'no'.

The set S is grown greedily: start from the empty set; while some assignment of options to S keeps the answer 'no'
(found by depth-first search with monotone pruning), take such an assignment, complete it greedily with the remaining
pairs (dead-dead options first), find the first pair whose both options give 'yes', and add to S that pair together with
the pairs whose connectors lie on the witnessing paths.
Usage: python k4c_core.py [ORDER_SEED]
"""
import sys
import random
import time
import gzz
import tools
import k4c


def build_with(base, conn):
    """conn: dict pair (i, l) -> 'E' or 'F'; one private node per pair.  Returns (inst, node -> pair)."""
    N, E, F, cls, s, t = base
    E, F = list(E), list(F)
    owner = {}
    for (i, l), T in sorted(conn.items()):
        z = N
        N += 1
        owner[z] = (i, l)
        if T == "E":
            E[i] |= 1 << z
            E[l] |= 1 << z
        else:
            F[i] |= 1 << z
            F[l] |= 1 << z
    return (N, E, F, cls, s, t), owner


def path_nodes(inst, modes):
    """Nodes shared by consecutive sides of a shortest s-t path of picked sides (BFS on sides)."""
    from collections import deque
    N, E, F, cls, s, t = inst
    sides = [F[i] if modes[cls[i]] else E[i] for i in range(len(E))]
    sides = [m for m in sides if m]
    start = [j for j, m in enumerate(sides) if (m >> s) & 1]
    par = {j: None for j in start}
    dq = deque(start)
    end = None
    while dq:
        j = dq.popleft()
        if (sides[j] >> t) & 1:
            end = j
            break
        for k in range(len(sides)):
            if k not in par and sides[j] & sides[k]:
                par[k] = j
                dq.append(k)
    seq = []
    while end is not None:
        seq.append(end)
        end = par[end]
    seq = seq[::-1]
    used = set()
    for a, b in zip(seq, seq[1:]):
        used |= set(gzz.bits_of(sides[a] & sides[b]))
    return used


def witness_pairs(inst, owner):
    modes = tools.bb_solve(inst)
    if modes is None:
        return None
    return {owner[x] for x in path_nodes(inst, modes) if x in owner}


def main():
    oseed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    order = None
    if oseed is not None:
        rng = random.Random(oseed)
        order = {(p, c): rng.sample([q for q in range(4) if q != p], 3) for p in range(4) for c in range(3)}
    base, info = k4c.build(order=order)
    mlab = info["mlab"]
    allpairs = gzz.p2_missing(base)

    def dead_first(p):
        ki, kl = mlab[p[0]][1], mlab[p[1]][1]
        if ki == "e" and kl == "e":
            return ["F", "E"]
        if ki == "f" and kl == "f":
            return ["E", "F"]
        return ["F", "E"]

    S = []
    t0 = time.time()
    while True:
        # depth-first search for an assignment of S keeping 'no'
        def dfs(k, conn):
            if k == len(S):
                return dict(conn)
            for T in dead_first(S[k]):
                conn[S[k]] = T
                inst, _ = build_with(base, conn)
                if tools.bb_solve(inst) is None:
                    r = dfs(k + 1, conn)
                    if r is not None:
                        return r
                del conn[S[k]]
            return None
        a = dfs(0, {})
        if a is None:
            print("CORE FOUND: every option assignment of these %d pairs gives a yes-instance:" % len(S))
            for p in S:
                print("  ", mlab[p[0]], mlab[p[1]])
            print("%.0fs" % (time.time() - t0))
            return S
        # greedy completion of a
        conn = dict(a)
        blocked = None
        for p in allpairs:
            if p in conn:
                continue
            placed = False
            for T in dead_first(p):
                conn[p] = T
                inst, _ = build_with(base, conn)
                if tools.bb_solve(inst) is None:
                    placed = True
                    break
                del conn[p]
            if not placed:
                blocked = p
                break
        if blocked is None:
            inst, _ = build_with(base, conn)
            print("COMPLETION FOUND keeping 'no'; P2:", gzz.p2_ok(inst))
            return None
        new = {blocked}
        for T in ("E", "F"):
            conn[blocked] = T
            inst, owner = build_with(base, conn)
            new |= witness_pairs(inst, owner)
            del conn[blocked]
        added = [p for p in new if p not in S]
        S.extend(added)
        print("core size", len(S), "(+%d)" % len(added), "%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
