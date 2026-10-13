"""Family Z_k of Pi-instances: u-pendants x_1..x_k and v-pendants y_1..y_k form antichains in the residual
order; the only witness cut is {u} + X, which needs k generators on either side (refutes any bounded number of
generators).  Real edges: path u y1 x1 y2 x2 ... yk xk v, u-x_i, v-y_j.  Ears: x_i-y_j for every pair that is not
a path edge; u-x_i and v-y_j topped up so that W(u,x_i) = cut degree of x_i, W(v,y_j) = cut degree of y_j."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi
from explore_pi import gen_cuts, co_cut

def build(k):
    u, v = 0, 1
    X = [2 + i for i in range(k)]
    Y = [2 + k + j for j in range(k)]
    q = 2 + 2 * k
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
                add(x, y, 1)          # ear
    for x in X:
        cd = sum(W[x][y] for y in Y) + W[x][v]
        add(u, x, 1, True)
        add(u, x, cd - 1)
    for y in Y:
        cd = sum(W[y][x] for x in X) + W[y][u]
        add(v, y, 1, True)
        add(v, y, cd - 1)
    return pi.Inst(q, sorted(R), W, u, v), path

for k in range(1, 6):
    inst, path = build(k)
    res = pi.answer(inst)
    reach = res["reach"]
    wit = [A for A in res["cuts"] if pi.real_cut_path(inst, A) is not None]
    c1 = any(gen_cuts(inst, reach, [x]) in wit for x in range(inst.q)) or any(co_cut(inst, reach, [y]) in wit for y in range(inst.q))
    g2 = any(gen_cuts(inst, reach, [x, x2]) in wit for x in range(inst.q) for x2 in range(inst.q)) or any(co_cut(inst, reach, [y, y2]) in wit for y in range(inst.q) for y2 in range(inst.q))
    print("k=%d q=%d dist_ok=%s c=%d #mincuts=%d witnesses=%s minlen=%s one-generator=%s two-generators=%s" % (
        k, inst.q, inst.dist_ok(), res["c"], res["ncuts"], [[x for x in range(inst.q) if (A >> x) & 1] for A in wit], res["minlen"], c1, g2))
