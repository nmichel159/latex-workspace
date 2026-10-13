"""Variant Z'_k of the antichain family: the u-pendants x_i are joined by real edges to a bottom vertex w0
(tied to u by M ears) instead of u, and to u only by ears; the v-pendants y_j are joined to a top vertex z0
(tied to v by M ears) instead of v.  Missing distances to u and v are supplied by balanced ear pairs
(an ear to u together with an ear to v), which add a constant to every cut.
Question: is the long path still the only witness (then H1 fails: far incomparable evens, not u-neighbours)?"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def build(k, M=None):
    u, v = 0, 1
    X = [2 + i for i in range(k)]
    Y = [2 + k + j for j in range(k)]
    w0, z0 = 2 + 2 * k, 3 + 2 * k
    q = 4 + 2 * k
    W = [[0] * q for _ in range(q)]
    R = set()
    def add(a, b, w=1, real=False):
        W[a][b] += w; W[b][a] += w
        if real:
            R.add((min(a, b), max(a, b)))
    path = [u]
    for i in range(k):
        path += [Y[i], X[i]]
    path.append(v)
    for a, b in zip(path, path[1:]):
        add(a, b, 1, True)
    pe = {(min(a, b), max(a, b)) for a, b in zip(path, path[1:])}
    for x in X:
        for y in Y:
            if (min(x, y), max(x, y)) not in pe:
                add(x, y, 1)
    for x in X:
        cd = sum(W[x][y] for y in Y) + W[x][v]
        add(w0, x, 1, True)
        add(u, x, cd - 1)
    for y in Y:
        cd = sum(W[y][x] for x in X) + W[y][u]
        add(z0, y, 1, True)
        add(v, y, cd - 1)
    # w0 sends one unit to each x through the real edge: w0 must receive k units from u
    big = M if M is not None else 4 * k * k + 10
    add(u, w0, big)
    add(v, z0, big)
    inst = pi.Inst(q, sorted(R), W, u, v)
    # fix distances by balanced ear pairs (ear to u and ear to v) for vertices too far from u or v,
    # and ears between other far pairs that are comparable (checked afterwards)
    def far(a, b):
        return not inst.R[a][b] and inst.W[a][b] == 0 and not any(inst.R[a][z] and inst.R[z][b] for z in range(q))
    for x in range(q):
        if x in (u, v):
            continue
        if far(u, x) or far(v, x):
            add(u, x, 1); add(v, x, 1)
            inst = pi.Inst(q, sorted(R), W, u, v)
    return pi.Inst(q, sorted(R), W, u, v), path

if __name__ == "__main__":
    for k in range(2, 6):
        inst, path = build(k)
        q = inst.q
        bad = [(a, b) for a in range(q) for b in range(a + 1, q)
               if not inst.R[a][b] and inst.W[a][b] == 0 and not any(inst.R[a][z] and inst.R[z][b] for z in range(q))]
        res = pi.answer(inst)
        wit = [A for A in res["cuts"] if pi.real_cut_path(inst, A) is not None]
        print("k=%d q=%d far pairs=%s c=%d #mincuts=%d witnesses=%s minlen=%s" % (
            k, q, bad, res["c"], res["ncuts"], [[x for x in range(q) if (A >> x) & 1] for A in wit], res["minlen"]))
