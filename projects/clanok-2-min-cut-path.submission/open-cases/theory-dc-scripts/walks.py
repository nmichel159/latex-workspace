"""Walk relaxations (polynomial) versus the truth on Pi-instances.
 W1: alternating real walk u = x0, x1, ..., v (v at an odd index, u only at index 0) with 'x_even does not
     reach x_odd' for consecutive vertices: BFS on (vertex, parity).
 W3: the same with the condition also for (x_t, x_{t+3}): BFS on triples (x_{t-2}, x_{t-1}, x_t) of the walk.
 Vertices of cl(u) can only be even, vertices that reach v only odd (implied by the conditions with u, v? no:
 we add them explicitly).
Usage: python walks.py SEED COUNT [families]"""
import sys, os, random
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def allowed(inst, reach, x, par):
    """x may stand at parity par (0 = even = A side)."""
    u, v = inst.u, inst.v
    if par == 0:
        return not (reach[x] >> v) & 1 and x != v
    return not (reach[u] >> x) & 1 and x != u

def ok(reach, a_par, a, b):
    """pair (a at parity a_par, b at the other parity)."""
    e, o = (a, b) if a_par == 0 else (b, a)
    return not (reach[e] >> o) & 1

def w1(inst, reach):
    q = inst.q
    seen = {(inst.u, 0)}
    dq = deque([(inst.u, 0)])
    while dq:
        x, p = dq.popleft()
        if x == inst.v and p == 1:
            return True
        for y in range(q):
            if inst.R[x][y] and allowed(inst, reach, y, 1 - p) and ok(reach, p, x, y) and (y, 1 - p) not in seen:
                if y == inst.u:
                    continue
                seen.add((y, 1 - p)); dq.append((y, 1 - p))
    return False

def w3(inst, reach):
    """states (a, b, c, parity of c) = last three walk vertices; start states built from u."""
    q = inst.q; u, v = inst.u, inst.v
    nb = [[y for y in range(q) if inst.R[x][y]] for x in range(q)]
    seen = set()
    dq = deque()
    # walks of length 1 and 2 first
    for x1 in nb[u]:
        if not (allowed(inst, reach, x1, 1) and ok(reach, 0, u, x1)):
            continue
        if x1 == v:
            return True
        for x2 in nb[x1]:
            if x2 in (u, v) or not (allowed(inst, reach, x2, 0) and ok(reach, 1, x1, x2)):
                continue
            st = (u, x1, x2, 0)
            if st not in seen:
                seen.add(st); dq.append(st)
    while dq:
        a, b, c, pc = dq.popleft()
        for d in nb[c]:
            pd = 1 - pc
            if d == u or not allowed(inst, reach, d, pd) or not ok(reach, pc, c, d):
                continue
            # pair (a, d): index distance 3, a has parity pd ^ 1 ... a's parity = pc ^ 1 ^ 1 ^ ... compute
            pa = pc  # a is two steps before c: same parity as c
            if not ok(reach, 1 - pd, a, d):
                continue
            if d == v and pd == 1:
                return True
            st = (b, c, d, pd)
            if st not in seen:
                seen.add(st); dq.append(st)
    return False

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "W1fp": 0, "W3fp": 0, "W1fn": 0, "W3fn": 0}
    ex = {}
    for it in range(count):
        q = rng.randint(6, 12)
        r = rng.random()
        if r < 0.6:
            inst = pi.planted_instance(rng, q, rng.randint(1, 4), rng.uniform(0.1, 0.9), rng.uniform(0.0, 0.25), rng.uniform(0, 0.3), rng.uniform(0.3, 1.0))
        else:
            inst = pi.random_instance(rng, q, rng.uniform(0.2, 0.7), rng.uniform(0.0, 0.3), max_mult=rng.randint(1, 3))
        if inst is None or not inst.dist_ok():
            continue
        try:
            res = pi.answer(inst, limit=50000)
        except RuntimeError:
            continue
        if res["c"] < 3:
            continue
        st["inst"] += 1
        t = res["yes"]; st["yes"] += t
        a1 = w1(inst, res["reach"]); a3 = w3(inst, res["reach"])
        if a1 and not t: st["W1fp"] += 1; ex.setdefault("W1fp", inst)
        if a3 and not t: st["W3fp"] += 1; ex.setdefault("W3fp", inst)
        if t and not a1: st["W1fn"] += 1; ex.setdefault("W1fn", inst)
        if t and not a3: st["W3fn"] += 1; ex.setdefault("W3fn", inst)
    print("seed", seed, st)
    for k, inst in sorted(ex.items()):
        print("  %s: q=%d real=%s ears=%s" % (k, inst.q, inst.real_edges(), inst.ears()))
