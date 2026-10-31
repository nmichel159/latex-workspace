"""Y_k with tied mates and decoy branchings at both terminals (family YB_k), designed to defeat forced-exit
propagation and failed-literal probing while keeping every solution on the rigid spine.

Spine: R(E^k F^k) as in cfam.rword with tied mates m_c ~ x_c (c <= k), but s and t are replaced by y_0 and y_t:
h_1 contains y_0, h_2k contains y_t.  Branchings: switches b1, b2 (own classes) with E-sides {s, y_0}; g1, g2 (own
classes) with F-sides {y_t, t}.  P2 witnesses (private nodes):
  b vs E-member x_j: F_b & Fl_j;   b vs F-member x_q: E_b & Fl_q;   b vs mate m_c: E_b & E(m_c);
  g vs E-member x_j: F_g & Fl_j;   g vs F-member x_q: E_g & Fl_q;   g vs mate m_c: E_g & E(m_c);
  b vs g: E_b & E_g;   b1 vs b2: s;   g1 vs g2: t.
"""
import ccore as C
import cfam


def ybranch(k, contact=0, nb=2, ng=2, mate_contact_side=None):
    B = cfam.rword("E" * k + "F" * k, mates=True, tie=True, contact=contact, s="y0", t="yt")
    L = 2 * k
    Em = list(range(1, k + 1))
    Fm = list(range(k + 1, L + 1))
    bs = [B.switch(("b", i), cls=("b", i)) for i in range(nb)]
    gs = [B.switch(("g", i), cls=("g", i)) for i in range(ng)]
    for b in bs:
        B.add(b, 0, "s", "y0")
    for g in gs:
        B.add(g, 1, "yt", "t")
    xs = {j: B.byname[("x", j)] for j in range(1, L + 1)}
    ms = {c: B.byname[("m", c)] for c in Em}
    cnt = [0]

    def wit(u, v, ty):
        cnt[0] += 1
        nm = ("wit", cnt[0])
        B.add(u, ty, nm)
        B.add(v, ty, nm)

    for b in bs:
        for j in Em:
            wit(b, xs[j], 1)          # F_b & Fl_j (Fl_j = F(x_j) for an E-member)
        for q in Fm:
            wit(b, xs[q], 0)          # E_b & Fl_q (Fl_q = E(x_q) for an F-member)
        for c in Em:
            wit(b, ms[c], 0)          # E_b & E(m_c)
    for g in gs:
        for j in Em:
            wit(g, xs[j], 1)          # F_g & Fl_j
        for q in Fm:
            wit(g, xs[q], 0)          # E_g & Fl_q
        for c in Em:
            wit(g, ms[c], 0)          # E_g & E(m_c)
        for b in bs:
            wit(b, g, 0)              # E_b & E_g
    return B.inst()


if __name__ == "__main__":
    import sys
    import cdecide as D
    for k in range(2, 7):
        I = ybranch(k)
        sols = C.all_solutions(I) if I.k <= 20 else None
        st, fx = C.prune(I)
        L, paths = C.shortest_valid_paths(I)
        info = ""
        if sols is not None:
            spine = all(all(m[I.cl[I.byname_idx]] if False else True for _ in [0]) for m in sols)
        g = D.guided_cost(I, paths[0], 2, 1, 1)
        print("k=%d n=%d classes=%d N=%d P2=%s sols=%s prune=%s fixed=%d |P|=%d npaths=%d guided=%s" % (
            k, I.n, I.k, I.N, C.p2_ok(I), None if sols is None else len(sols), st, len(fx), L, len(paths), g),
            flush=True)


def ybranch_fake(k, contact=2, nfake=1, nb=2, ng=2):
    """YB_k plus nfake fake pairs: class D_i with switches d1 (E-side {s, phi_i}, behaves like a branch switch b)
    and d2 (F-side {phi_i, t}, behaves like g).  In every mode one of the two sides is missing, so the pair never
    connects s and t, but the relaxation (all free sides) always does."""
    B = cfam.rword("E" * k + "F" * k, mates=True, tie=True, contact=contact, s="y0", t="yt")
    L = 2 * k
    Em = list(range(1, k + 1))
    Fm = list(range(k + 1, L + 1))
    bs = [B.switch(("b", i), cls=("b", i)) for i in range(nb)]
    gs = [B.switch(("g", i), cls=("g", i)) for i in range(ng)]
    d1s, d2s = [], []
    for i in range(nfake):
        d1s.append(B.switch(("d1", i), cls=("D", i)))
        d2s.append(B.switch(("d2", i), cls=("D", i)))
    for b in bs + d1s:
        B.add(b, 0, "s")
    for b in bs:
        B.add(b, 0, "y0")
    for g in gs + d2s:
        B.add(g, 1, "t")
    for g in gs:
        B.add(g, 1, "yt")
    for i in range(nfake):
        B.add(d1s[i], 0, ("phi", i))
        B.add(d2s[i], 1, ("phi", i))
    xs = {j: B.byname[("x", j)] for j in range(1, L + 1)}
    ms = {c: B.byname[("m", c)] for c in Em}
    cnt = [0]

    def wit(u, v, ty):
        cnt[0] += 1
        nm = ("wit", cnt[0])
        B.add(u, ty, nm)
        B.add(v, ty, nm)

    lefts = bs + d1s      # E-live switches containing s
    rights = gs + d2s     # F-live switches containing t
    for b in lefts:
        for j in Em:
            wit(b, xs[j], 1)
        for q in Fm:
            wit(b, xs[q], 0)
        for c in Em:
            wit(b, ms[c], 0)
    for g in rights:
        for j in Em:
            wit(g, xs[j], 1)
        for q in Fm:
            wit(g, xs[q], 0)
        for c in Em:
            wit(g, ms[c], 0)
    # left vs right (different classes): E_b & E_g
    for b in lefts:
        for g in rights:
            if B.cl[b] != B.cl[g]:
                wit(b, g, 0)
    return B.inst()
