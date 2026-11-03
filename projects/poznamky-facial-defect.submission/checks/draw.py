"""Barycentric (Tutte) drawing of a 3-connected plane graph given by its rotation system; prints TikZ coordinates."""
import json, math, sys
import numpy as np
from planemap import PlaneMap


def tutte(sigma, outer=None, rot=90.0, iters=0):
    g = PlaneMap(sigma)
    vert = g.vertices()
    faces = [[vert[d] for d in w] for w in g.faces()]
    if outer is None:
        outer = max(range(len(faces)), key=lambda i: len(faces[i]))
    of = faces[outer]
    n = g.nv
    pos = np.zeros((n, 2))
    k = len(of)
    fixed = set(of)
    for i, v in enumerate(of):
        a = math.radians(rot) + 2 * math.pi * i / k
        pos[v] = (math.cos(a), math.sin(a))
    adj = [[] for _ in range(n)]
    for (u, v) in g.edges():
        adj[u].append(v)
        adj[v].append(u)
    inner = [v for v in range(n) if v not in fixed]
    idx = {v: i for i, v in enumerate(inner)}
    w = {}
    for u in range(n):
        for v in adj[u]:
            w[(u, v)] = 1.0
    for _ in range(iters + 1):
        A = np.zeros((len(inner), len(inner)))
        b = np.zeros((len(inner), 2))
        for v in inner:
            i = idx[v]
            s = sum(w[(v, u)] for u in adj[v])
            A[i, i] = s
            for u in adj[v]:
                if u in idx:
                    A[i, idx[u]] -= w[(v, u)]
                else:
                    b[i] += w[(v, u)] * pos[u]
        sol = np.linalg.solve(A, b)
        for v in inner:
            pos[v] = sol[idx[v]]
        # reweight: longer edges get smaller weight next round (spreads the inner vertices)
        for (u, v) in list(w):
            d = np.linalg.norm(pos[u] - pos[v])
            w[(u, v)] = 1.0 / max(d, 1e-3) ** 0.0
    return g, pos, faces


if __name__ == "__main__":
    ex = json.load(open(sys.argv[1], encoding="utf-8"))
    name = sys.argv[2]
    outer = int(sys.argv[3]) if len(sys.argv) > 3 else None
    rot = float(sys.argv[4]) if len(sys.argv) > 4 else 90.0
    for e in ex:
        if e["name"].startswith(name):
            g, pos, faces = tutte(e["sigma"], outer, rot)
            print("% faces:", faces)
            for v in range(g.nv):
                print(f"  \\node[vertex] (v{v}) at ({pos[v][0]:.3f},{pos[v][1]:.3f}) {{}};")
            print("  \\draw[edge] " + " ".join(f"(v{u}) -- (v{v})" for (u, v) in g.edges()) + ";")
