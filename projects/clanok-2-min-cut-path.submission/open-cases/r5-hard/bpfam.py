"""Family BP_n (r5-hard.md Section 4, route R1): dense bad pairs hung on the rigid family R_{2n}.

Base R_{2n} (dc-hardness.md Section 2): switches x_1..x_2n, path side h_k = E(x_k) for odd k, F(x_k) for even k,
flip side Fl_k the other side; nodes s in h_1, t in h_2n, y_k in h_k & h_{k+1}; for p < q: z_pq in Fl_p & h_q if
q - p is odd, w_pq in Fl_p & Fl_q if q - p is even.  E-members a_j = x_{2j-1}, F-members b_i = x_{2i}.
New switches Y_i < b_i (i = 1..n) and X_j > a_j (j = 1..n), with Y_i < X_j for all i, j; middle edges Y_i - b_i,
a_j - X_j, Y_i - X_j (all i, j).  P2 witnesses of the new pairs:
  Y_i, Y_k:   upper middle witness X_1;            X_j, X_l: lower middle witness Y_1;
  Y_i, a_l:   upper middle witness X_l;            X_j, b_k: lower middle witness Y_k;
  Y_i, b_k (k != i): node n_ik in E(Y_i) & Fl(b_k);   X_j, a_l (l != j): node m_jl in F(X_j) & Fl(a_l).
Variant 'mirror' (route R1'): the same with the base reflected (z-nodes Fl_p & h_q for q < p), used to test whether
the cheap end moves.
"""
from hlib import Inst


def bp(n, with_bad=True, xwit="F"):
    I = Inst()
    L = 2 * n
    xs = ["x%d" % k for k in range(1, L + 1)]
    for k in range(1, L + 1):
        I.switch(xs[k - 1])

    def h(k, nd):
        (I.addE if k % 2 == 1 else I.addF)(xs[k - 1], nd)

    def fl(k, nd):
        (I.addF if k % 2 == 1 else I.addE)(xs[k - 1], nd)

    h(1, "s")
    h(L, "t")
    for k in range(1, L):
        h(k, ("y", k))
        h(k + 1, ("y", k))
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                fl(p, ("z", p, q))
                h(q, ("z", p, q))
            else:
                fl(p, ("w", p, q))
                fl(q, ("w", p, q))
    if not with_bad:
        return I.build()
    a = {j: xs[2 * j - 2] for j in range(1, n + 1)}
    b = {i: xs[2 * i - 1] for i in range(1, n + 1)}
    Y = {i: "Y%d" % i for i in range(1, n + 1)}
    X = {j: "X%d" % j for j in range(1, n + 1)}
    for i in range(1, n + 1):
        I.edge(Y[i], b[i])
    for j in range(1, n + 1):
        I.edge(a[j], X[j])
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            I.edge(Y[i], X[j])
    for i in range(1, n + 1):
        for k in range(1, n + 1):
            if k != i:
                I.addE(Y[i], ("n", i, k))
                I.addE(b[k], ("n", i, k))          # Fl(b_k) = E(b_k)
    for j in range(1, n + 1):
        for l in range(1, n + 1):
            if l != j:
                I.addF(X[j], ("m", j, l))
                I.addF(a[l], ("m", j, l))          # Fl(a_l) = F(a_l)
    return I.build()
