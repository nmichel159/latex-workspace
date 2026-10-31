"""Exhaustive search over small ZZ + P2 instances for the smallest counterexample to each candidate method.

Instances: n elements, u = 0, v = n-1; nb elements equivalent to u (class B), nt equivalent to v (class T), m middle
elements carrying a preorder (one representative per isomorphism type of the middle preorder); R any set of strict
comparable pairs except (u, v).  Only instances with P2 are kept.
Methods (all decided per instance):
  exact      own down-set enumeration (= gcert.exact on a sample, checked)
  contract   middle tie classes contracted to one element (edges united): a relaxation
  naive      the literal translation of Theorem H: (A2)/(A3) only for the element itself (x in M- / y in M+), any pins,
             all modes, |pi| <= 2  -- unsound with ties / comparabilities
  GC_k       gcert.certificate (sound), k = 0, 1, 2, 3
  H_k        gcert.certificate with piercers in B / T only (literal Theorem H pins), general mode, k <= 4
Output: for each failure type the smallest instance (n, |R|), overall and per structure (ties / oneway / midedge).
Usage: python enum_small.py NMAX [OUT]
"""
import sys
import itertools
import time
import json
import gcert


def preorders(m):
    """Isomorphism representatives of preorders on m points, as tuples of bit masks down[x] (a <= x)."""
    if m == 0:
        return [()]
    pairs = [(a, b) for a in range(m) for b in range(m) if a != b]
    seen = set()
    reps = []
    perms = list(itertools.permutations(range(m)))
    for mask in range(1 << len(pairs)):
        le = [[a == b for b in range(m)] for a in range(m)]
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                le[a][b] = True
        ok = all(not (le[a][b] and le[b][c]) or le[a][c] for a in range(m) for b in range(m) for c in range(m))
        if not ok:
            continue
        key = min(tuple(le[p[a]][p[b]] for a in range(m) for b in range(m)) for p in perms)
        if key in seen:
            continue
        seen.add(key)
        reps.append(le)
    return reps


def build_le(nb, m, nt, mle):
    n = nb + m + nt
    le = [[False] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if a == b or a < nb or b >= nb + m:
                le[a][b] = True
    for a in range(m):
        for b in range(m):
            if mle[a][b]:
                le[nb + a][nb + b] = True
    return le


def flags(I):
    mid = I.full & ~(I.B | I.T)
    ties = any(bin(I.down[x] & I.up[x] & mid).count("1") > 1 for x in gcert.bits(mid))
    oneway = any((I.down[x] & mid) & ~(I.up[x]) for x in gcert.bits(mid))
    midedge = any((mid >> a) & 1 and (mid >> b) & 1 for a, b in I.R)
    return ("T" if ties else "") + ("O" if oneway else "") + ("E" if midedge else "") or "sw"


def contract(I):
    """Contract each middle class to its least-index member; returns gcert.Inst."""
    n = I.n
    rep = {}
    mid = I.full & ~(I.B | I.T)
    for x in range(n):
        if (mid >> x) & 1:
            cls = I.down[x] & I.up[x]
            rep[x] = min(gcert.bits(cls))
        else:
            rep[x] = x
    keep = sorted(set(rep.values()))
    idx = {x: i for i, x in enumerate(keep)}
    le = [[I.le[a][b] for b in keep] for a in keep]
    R = set()
    for a, b in I.R:
        R.add((idx[rep[a]], idx[rep[b]]))
    return gcert.Inst(len(keep), le, R, idx[I.u], idx[I.v])


def naive_search(I, Gm, Pm, Gp, Pp):
    """Like gcert.general_search but (A2)/(A3) required for the element itself only (Theorem H literally)."""
    n = I.n
    Dm = I.downclose(Gm | Pm)
    Up = I.upclose(Gp | Pp)
    Mm = sum(1 << y for y in range(n) if I.lo[y] & Pm)
    Mp = sum(1 << x for x in range(n) if I.hi[x] & Pp)
    okv = okp = 0
    for x in range(n):
        if not (Up >> x) & 1:
            if (Dm >> x) & 1 or not (I.peakcap >> x) & 1 or (Mm >> x) & 1:
                okv |= 1 << x
        if not (Dm >> x) & 1:
            if (Up >> x) & 1 or not (I.valcap >> x) & 1 or (Mp >> x) & 1:
                okp |= 1 << x
    if not (okv >> I.u) & 1 or not (okp >> I.v) & 1:
        return None
    from collections import deque
    start = (I.u, 1, 0, 0)
    seen = {start}
    dq = deque([start])
    while dq:
        x, val, sp, sv = dq.popleft()
        nb = (I.hi[x] & okp) if val else (I.lo[x] & okv)
        for y in gcert.bits(nb):
            sp2, sv2 = sp, sv
            if val:
                if (Mm >> y) & 1:
                    if sv & I.up[y]:
                        continue
                    sp2 |= 1 << y
            else:
                if (Mp >> y) & 1:
                    if sp & I.down[y]:
                        continue
                    sv2 |= 1 << y
            st = (y, 1 - val, sp2, sv2)
            if st in seen:
                continue
            if y == I.v and val:
                return True
            seen.add(st)
            dq.append(st)
    return None


def naive(I, k=2):
    n = I.n
    roles = ([("Gm", x) for x in range(n)] + [("Pm", x) for x in range(n) if I.hi[x]] +
             [("Gp", x) for x in range(n)] + [("Pp", x) for x in range(n) if I.lo[x]])
    for size in range(k + 1):
        for combo in itertools.combinations(roles, size):
            masks = {"Gm": 0, "Pm": 0, "Gp": 0, "Pp": 0}
            for r, x in combo:
                masks[r] |= 1 << x
            if naive_search(I, masks["Gm"], masks["Pm"], masks["Gp"], masks["Pp"]):
                return combo
    return None


def relaxed(I):
    """Is there an alternating u-v walk at all (consistency ignored)?"""
    from collections import deque
    st = (I.u, 1)
    seen = {st}
    dq = deque([st])
    while dq:
        x, val = dq.popleft()
        for y in gcert.bits(I.hi[x] if val else I.lo[x]):
            if y == I.v and val:
                return True
            s2 = (y, 1 - val)
            if s2 not in seen:
                seen.add(s2)
                dq.append(s2)
    return False


def main():
    nmax = int(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else None
    best = {}
    counts = {}
    t0 = time.time()

    def record(kind, I, extra=""):
        fl = flags(I)
        for key in ((kind, "any"), (kind, fl)):
            sz = (I.n, len(I.R))
            if key not in best or sz < best[key][0]:
                best[key] = (sz, gcert.describe(I) + extra)
        counts[(kind, fl)] = counts.get((kind, fl), 0) + 1

    for n in range(3, nmax + 1):
        for nb in range(1, n - 1):
            for nt in range(1, n - nb):
                m = n - nb - nt
                for mle in preorders(m):
                    le = build_le(nb, m, nt, mle)
                    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
                    strict = [(a, b) for a in range(n) for b in range(n) if lt[a][b] and (a, b) != (0, n - 1)]
                    # middle-only equivalence check for P2 pairs
                    inc = [(x, y) for x in range(n) for y in range(x + 1, n) if not le[x][y] and not le[y][x]]
                    base = gcert.Inst(n, le, [], 0, n - 1)
                    Ds = gcert.downsets(base)
                    for mask in range(1 << len(strict)):
                        lo = [0] * n
                        hi = [0] * n
                        for i, (a, b) in enumerate(strict):
                            if (mask >> i) & 1:
                                hi[a] |= 1 << b
                                lo[b] |= 1 << a
                        if any(not ((lo[x] & lo[y]) or (hi[x] & hi[y])) for x, y in inc):
                            continue
                        R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
                        I = gcert.Inst(n, le, R, 0, n - 1)
                        ex = any(gcert.cut_path(I, D) is not None for D in Ds)
                        counts[("all", "yes" if ex else "no")] = counts.get(("all", "yes" if ex else "no"), 0) + 1
                        if not ex:
                            if gcert.pinned_search(I, I.full, 0, False) is None and                                     gcert.pinned_search(I, 0, I.full, True) is None and not relaxed(I):
                                continue
                            if flags(I).startswith("T") or "T" in flags(I):
                                C = contract(I)
                                if gcert.exact(C):
                                    record("contract-false-yes", I)
                            if naive(I) is not None:
                                record("naive-unsound", I)
                            continue
                        c = None
                        for k in range(4):
                            c = gcert.certificate(I, k)
                            if c is not None:
                                break
                        if c is None:
                            record("GC3-miss", I)
                            c = (4,)
                        if c[0] >= 1:
                            record("GC0-miss", I)
                        if c[0] >= 2:
                            record("GC1-miss", I)
                        if c[0] >= 3:
                            record("GC2-miss", I)
                        h = gcert.certificate(I, 4, modes=("gen",), piercers_only="H")
                        if h is None:
                            record("H4-miss", I)
        print("n <=", n, "done", "%.0fs" % (time.time() - t0), {k: v for k, v in counts.items() if k[0] == "all"},
              flush=True)
        lines = []
        for key in sorted(best, key=str):
            lines.append("%s %s %s" % (key, best[key][0], best[key][1]))
        for key in sorted(counts, key=str):
            lines.append("count %s %d" % (key, counts[key]))
        text = "\n".join(lines)
        print(text, flush=True)
        if out:
            with open(out, "w") as f:
                f.write("enum_small.py, n <= %d\n" % n + text + "\n")


if __name__ == "__main__":
    main()
