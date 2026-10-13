"""Families of dc-hardness.md rebuilt from the text (agent verify-LTH): R_L (2CH form), its interval (TIC) form,
the form with t added to every flip side, and the broken variants cut(L, k), tflip(L, k)."""


def rigid_2ch(L, t_in_flips=False, cut=None, tflip=None):
    """R_L: switches x_1..x_L; h_k is E for odd k, F for even k; Fl_k the other side.
    Nodes: s in h_1, t in h_L, y_k in h_k and h_{k+1}; z_pq in Fl_p and h_q (q - p odd), w_pq in Fl_p and Fl_q
    (q - p even). cut=k removes y_k; tflip=k moves t from h_L into Fl_k."""
    names = ["s", "t"] + [("y", k) for k in range(1, L)]
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            names.append(("z", p, q) if (q - p) % 2 else ("w", p, q))
    idx = {nm: i for i, nm in enumerate(names)}
    h = {k: 0 for k in range(1, L + 1)}
    fl = {k: 0 for k in range(1, L + 1)}

    def add(d, k, nm):
        d[k] |= 1 << idx[nm]

    add(h, 1, "s")
    if tflip is None:
        add(h, L, "t")
    else:
        add(fl, tflip, "t")
    for k in range(1, L):
        if cut == k:
            continue
        add(h, k, ("y", k)); add(h, k + 1, ("y", k))
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2:
                add(fl, p, ("z", p, q)); add(h, q, ("z", p, q))
            else:
                add(fl, p, ("w", p, q)); add(fl, q, ("w", p, q))
    if t_in_flips:
        for k in range(1, L + 1):
            add(fl, k, "t")
    sw = []
    for k in range(1, L + 1):
        sw.append((h[k], fl[k]) if k % 2 else (fl[k], h[k]))
    return (len(names), idx["s"], idx["t"], sw), names


def rigid_tic(L):
    """Interval form: line 0..L, switch k has h_k = [k-1, k] (type E for odd k) and Fl_k = [k, L]."""
    sw = []
    for k in range(1, L + 1):
        hk, flk = (k - 1, k), (k, L)
        sw.append((hk, flk) if k % 2 else (flk, hk))
    return L, sw


def alternating_modes(L):
    """Mode vector picking h_k for every k (E for odd k, F for even k)."""
    return tuple(0 if k % 2 else 1 for k in range(1, L + 1))
