"""Smoke test: the family G_k of theory-dc.md Theorem 8 (built here from its definition), a 4-cycle,
and K_4 with a pendant path (bridges)."""
import time
from checks import check_graph


def Gk(k):
    x = list(range(2 * k + 2))
    a = list(range(2 * k + 2, 3 * k + 2))
    b = list(range(3 * k + 2, 4 * k + 2))
    E = set()
    for i in range(2 * k + 1):
        E.add((x[i], x[i + 1]))
    ev = x[0::2]
    od = x[1::2]
    for S in (ev, od):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                E.add((S[i], S[j]))
    u, v = x[0], x[2 * k + 1]
    for i in range(1, k + 1):
        E.add((a[i - 1], u))
        E.add((a[i - 1], x[2 * i]))
        E.add((b[i - 1], x[2 * i - 1]))
        E.add((b[i - 1], v))
    return 4 * k + 2, sorted((min(p), max(p)) for p in [tuple(e) for e in E]), u, v


if __name__ == "__main__":
    for k in (1, 2):
        n, E, u, v = Gk(k)
        t = time.time()
        st, vi = check_graph(n, E, ordered=True, do_cp=(k == 1))
        print("G_%d" % k, n, dict(st), "violations", len(vi), vi[:3], "%.1fs" % (time.time() - t))
    st, vi = check_graph(4, [(0, 1), (1, 2), (2, 3), (0, 3)])
    print("C4", dict(st), vi[:3])
    E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    st, vi = check_graph(6, E)
    print("K4+tail", dict(st), vi[:3])
