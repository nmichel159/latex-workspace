"""Double-mate family OB (r5-core.md Section 4.2): a critical-run base with down-mates and up-mates whose sides can
only be covered by expensive centres.

Base word E^K F^M E^K2 (positions 0..r-1).  P2 of the base:
  same type, |a - b| >= 2: partner-partner link;
  first-block E-member c and run F-member q: contact c -> q (X'_c meets X_q);
  run F-member q and last-block E-member c': contact q -> c' (X'_q meets X_c'), and with back=True also
  c' -> q (X'_c' meets X_q);
  first-block and last-block E-members: same type (partner link).
Down-mates y_i < q_i (q_i run positions), i < k:
  E(y_i): meets X_c for c in S_i (private sets of the last block, size `sz`) and the partner X'_q of every run
          F-member q != q_i (P2 with q);
  F(y_i): meets X'_c for every E-member c not in S_i (P2 with c); down-mates pairwise by F-F links.
Up-mates z_j > a_j (a_j first-block positions), j < k, and y_i < z_j for all i, j:
  F(z_j): meets X_q for q in T_j (private sets of the run, size `sz`) and X'_c for every E-member c != a_j;
  E(z_j): meets X'_q for every run F-member q not in T_j; up-mates pairwise by E-E links.
"""
from gplant import GPlanted


def ob(K, M, K2, k, sz, back=True, mates=True, decoy=False):
    typ = [0] * K + [1] * M + [0] * K2
    r = len(typ)
    first = list(range(K))
    run = list(range(K, K + M))
    last = list(range(K + M, r))
    pl = GPlanted(typ)
    for a in range(r):
        for b in range(a + 1, r):
            if typ[a] == typ[b]:
                if b >= a + 2:
                    pl.link(pl.par(a), pl.par(b))
                continue
            # cross pair (a < b)
            if a in first and b in run:
                pl.link(pl.par(a), pl.mem(b))
            elif a in run and b in last:
                pl.link(pl.par(a), pl.mem(b))
                if back:
                    pl.link(pl.par(b), pl.mem(a))
            else:
                raise ValueError("unexpected cross pair")
    info = {"first": first, "run": run, "last": last, "down": [], "up": []}
    if not mates:
        return pl, info
    assert k * sz <= K2 and k * sz <= M and k <= M and k <= K
    owners_d = [run[(i * M) // k] for i in range(k)]
    owners_u = [first[(j * K) // k] for j in range(k)]
    S = [last[i * sz:(i + 1) * sz] for i in range(k)]
    T = [run[j * sz:(j + 1) * sz] for j in range(k)]
    ys, zs = [], []
    for i in range(k):
        y = pl.add_switch(("y", i))
        ys.append(y)
        pl.le(y, owners_d[i])
    for j in range(k):
        z = pl.add_switch(("z", j))
        zs.append(z)
        pl.le(owners_u[j], z)
    for y in ys:
        for z in zs:
            pl.le(y, z)
    Em = [c for c in range(r) if typ[c] == 0]
    for i, y in enumerate(ys):
        for c in S[i]:
            pl.link((y, 0), pl.mem(c))
        for q in run:
            if q != owners_d[i]:
                pl.link((y, 0), pl.par(q))
        for c in Em:
            if c not in S[i]:
                pl.link((y, 1), pl.par(c))
    for i in range(k):
        for i2 in range(i + 1, k):
            pl.link((ys[i], 1), (ys[i2], 1))
    for j, z in enumerate(zs):
        for q in T[j]:
            pl.link((z, 1), pl.mem(q))
        for c in Em:
            if c != owners_u[j]:
                pl.link((z, 1), pl.par(c))
        for q in run:
            if q not in T[j]:
                pl.link((z, 0), pl.par(q))
    for j in range(k):
        for j2 in range(j + 1, k):
            pl.link((zs[j], 0), (zs[j2], 0))
    info.update(down=ys, up=zs, owners_d=owners_d, owners_u=owners_u, S=S, T=T)
    return pl, info
