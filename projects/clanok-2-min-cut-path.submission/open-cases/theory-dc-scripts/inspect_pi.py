"""Print an instance of Pi: weights, flow, residual preorder, all minimum cuts with their real cut paths."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi

def build(q, real, ears, u=0, v=1):
    W = [[0] * q for _ in range(q)]
    for a, b in real:
        W[a][b] += 1; W[b][a] += 1
    for a, b, k in ears:
        W[a][b] += k; W[b][a] += k
    return pi.Inst(q, real, W, u, v)

def show(inst):
    res = pi.answer(inst)
    q = inst.q
    print("c =", res["c"], " deg_H:", [sum(inst.W[x]) for x in range(q)])
    reach = res["reach"]
    print("closures:", {x: [y for y in range(q) if (reach[x] >> y) & 1] for x in range(q)})
    for A in res["cuts"]:
        side = [x for x in range(q) if (A >> x) & 1]
        p = pi.real_cut_path(inst, A)
        thinA = all(any(inst.W[x][y] for y in range(q) if not (A >> y) & 1) for x in side)
        thinB = all(any(inst.W[x][y] for y in side) for x in range(q) if not (A >> x) & 1)
        print("  A =", side, "path", p, "thin u-side" if thinA else "", "thin v-side" if thinB else "")
    return res

if __name__ == "__main__":
    import ast
    q = int(sys.argv[1]); real = ast.literal_eval(sys.argv[2]); ears = ast.literal_eval(sys.argv[3])
    show(build(q, real, ears))
